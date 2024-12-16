import re
from bert_score import score as bert_score
from sentence_transformers import SentenceTransformer, util


class ScoreCalculator:
    """Utility class to calculate similarity, BERTScore, and validate accuracy."""

    def __init__(self):
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

    def compute_similarity(self, generated_response: str, expected_output: str) -> float:
        """Compute cousine similarity (whole text comparison) between generated and expected outputs."""
        generated_embedding = self.sentence_model.encode(generated_response, convert_to_tensor=True)
        expected_embedding = self.sentence_model.encode(expected_output, convert_to_tensor=True)
        return util.pytorch_cos_sim(generated_embedding, expected_embedding).item()

    def compute_bertscore(self, generated_response: str, expected_output: str) -> float:
        """Compute BERTScore (accuracy on token level) between generated and expected outputs."""
        P, R, F1 = bert_score([generated_response], [expected_output], lang="en", verbose=False)
        return F1.item()
