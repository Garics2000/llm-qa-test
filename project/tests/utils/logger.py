import os
import json
import allure


class Logger:
    """Logger for tests results in structured format."""
    def __init__(self, log_dir: str, log_file: str):
        self.log_dir = os.path.abspath(log_dir)
        self.log_file = os.path.join(self.log_dir, log_file)
        self.logs = []

        # Ensure the log directory exists
        os.makedirs(self.log_dir, exist_ok=True)

    def log_result(self, input_query: str, passed: bool, expected_output: str, generated_response: str,
                   similarity: float = None, bertscore: float = None, similarity_threshold: float = None,
                   bertscore_threshold: float = None, response_time: float = None):

        result = {
            "input": input_query,
            "expected_output": expected_output,
            "generated_response": generated_response,
            "similarity": similarity,
            "bertscore": bertscore,
            "similarity_threshold": similarity_threshold,
            "bertscore_threshold": bertscore_threshold,
            "response_time": response_time,
            "result": "pass" if passed else "fail"
        }
        self.logs.append(result)

        # Add Allure logging for detailed tests reporting
        with allure.step(f"Test for input: {input_query}"):
            allure.attach(json.dumps(result, indent=4), name="Test Result", attachment_type=allure.attachment_type.JSON)

    def save_logs(self):
        """Saves logs to a JSON file."""
        try:
            print(f"Saving logs to file: {self.log_file}")
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            with open(self.log_file, "w") as f:
                json.dump(self.logs, f, indent=4)
            print("Logs saved successfully.")
        except Exception as e:
            print(f"Error while saving logs: {e}")
