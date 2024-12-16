import os
from dataclasses import dataclass


@dataclass
class TestConfig:
    similarity_threshold: float
    bertscore_threshold: float
    query_max_time: float
    log_dir: str
    log_file: str

    @classmethod
    def from_env(cls) -> 'TestConfig':
        return cls(
            similarity_threshold=float(os.getenv("SIMILARITY_THRESHOLD", 0.8)),
            bertscore_threshold=float(os.getenv("BERTSCORE_THRESHOLD", 0.8)),
            query_max_time=float(os.getenv("QUERY_MAX_TIME", 2.0)),
            log_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests", "reports")),
            log_file="test_results.json"
        )