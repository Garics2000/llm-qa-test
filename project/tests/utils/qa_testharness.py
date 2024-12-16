import time
from typing import Optional, Tuple
from dotenv import load_dotenv

from ..data.knowledge_base import KNOWLEDGE_BASE
from ..utils.score_calculator import ScoreCalculator
from ..utils.logger import Logger
from ..utils.retrival_helper import RetrievalQAHelper
from ..config import TestConfig


class QATestHarness:
    """Test harness for RetrievalQA system"""

    def __init__(self):
        load_dotenv()
        self.config = TestConfig.from_env()
        self.logger = Logger(log_dir=self.config.log_dir, log_file=self.config.log_file)
        self.score_calculator = ScoreCalculator()
        self.retrieval_helper = RetrievalQAHelper(KNOWLEDGE_BASE)

    def execute_query(self, input_query: str) -> Tuple[str, float]:
        """Execute query and measure response time"""
        start_time = time.time()
        response = self.retrieval_helper.query(input_query)
        response_time = time.time() - start_time
        return response, response_time

    def compute_metrics(self, generated_response: str, expected_output: str) -> Tuple[float, float]:
        """Compute similarity and BERTScore metrics"""
        return (
            self.score_calculator.compute_similarity(generated_response, expected_output),
            self.score_calculator.compute_bertscore(generated_response, expected_output)
        )

    def validate_response(
            self,
            input_query: str,
            generated_response: str,
            expected_output: str,
            similarity: float,
            bertscore: float,
            similarity_threshold: float,
            bertscore_threshold: float
    ) -> None:
        """Validate response based on multiple criteria"""
        passed = (
                similarity >= similarity_threshold and
                bertscore >= bertscore_threshold
        )

        self.logger.log_result(
            input_query=input_query,
            expected_output=expected_output,
            generated_response=generated_response,
            similarity=similarity,
            bertscore=bertscore,
            similarity_threshold=similarity_threshold,
            bertscore_threshold=bertscore_threshold,
            passed=passed
        )

        assert passed, self._format_validation_error_message(
            input_query, similarity, similarity_threshold, bertscore,
            bertscore_threshold, generated_response, expected_output
        )

    def validate_performance(
            self,
            input_query: str,
            generated_response: str,
            response_time: Optional[float] = None
    ) -> None:
        """Validate model performance (so far only as response time)"""
        time_check = response_time is None or response_time <= self.config.query_max_time

        self.logger.log_result(
            input_query=input_query,
            expected_output="Response time tests only",
            generated_response=generated_response,
            response_time=response_time,
            passed=time_check
        )

        assert time_check, self._format_performance_error_message(
            input_query, self.config.query_max_time, response_time
        )

    def _format_validation_error_message(self, input_query: str, similarity: float,
                                         similarity_threshold: float, bertscore: float, bertscore_threshold: float,
                                         generated: str, expected: str) -> str:
        """Format error message for validation checks"""
        error_parts = [f"Test failed for input: {input_query}\n"]

        # Check each threshold and add to error message only if failed
        if similarity < similarity_threshold:
            error_parts.append(f"Similarity {similarity:.2f} below threshold {similarity_threshold:.2f}")

        if bertscore < bertscore_threshold:
            error_parts.append(f"BERTScore {bertscore:.2f} below threshold {bertscore_threshold:.2f}")

        if len(error_parts) > 1:
            error_parts.append(f"\nGenerated: {generated}")
            error_parts.append(f"Expected: {expected}")

        return "\n".join(error_parts)

    def _format_performance_error_message(self, input_query: str, threshold: float, response_time: float) -> str:
        return (
            f"Test failed for input: {input_query}\n"
            f"Response time {response_time: 2f} exceeded {threshold: 2f} seconds.\n"

        )