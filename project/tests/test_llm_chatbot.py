import os
import sys
import pytest

from .models import TestCase
from .utils.qa_testharness import QATestHarness

sys.path.append(os.path.dirname(__file__))

qa_test_harness = QATestHarness()

# Test cases data
RESPONSE_QUALITY_TEST_CASES = [
    TestCase("What is your return policy?", "Items can be returned within 30 days.", "return_policy"),
    TestCase("How can I track my order?", "You can track your order by visiting our website or contacting support.",
             "order_tracking"),
    TestCase("Do you offer international shipping?", "Yes, we ship to most countries worldwide.",
             "international_shipping"),
    TestCase("What is your refund process?",
             "Refunds are processed within 5-7 business days after the return is received.", "refund_process"),
    TestCase("How do I reset my account password?", "Click 'Forgot Password' on the login page to reset your password.",
             "password_reset"),
    # Edge cases
    TestCase("Can I exchange an item?", "Yes, exchanges are allowed within 30 days of purchase.", "item_exchange"),
    TestCase("How can I cancel my order?",
             "You can cancel your order by contacting customer support before it is shipped.", "order_cancellation"),
]

PERFORMANCE_TEST_CASES = [
    TestCase("Hi", "Hello! How can I help you today?", "greeting"),
    TestCase("Hello", "Hi! How may I assist you?", "greeting"),
    TestCase("Bye", "Good bye!", "greeting"),
    TestCase(
        "Summarize the history of the Roman Empire in 200 words.",
        "",  # Empty expected output as we only care about timing
        "complex_query"
    ),
    TestCase(
        "Explain quantum mechanics and its applications in modern technology.",
        "",
        "complex_query"
    )
]


@pytest.mark.parametrize("test_case", RESPONSE_QUALITY_TEST_CASES)
def test_response_quality(test_case: TestCase):
    response, response_time = qa_test_harness.execute_query(test_case.input_query)
    similarity, bertscore = qa_test_harness.compute_metrics(
        response, test_case.expected_output
    )

    qa_test_harness.validate_response(
        test_case.input_query,
        response,
        test_case.expected_output,
        similarity,
        bertscore,
        qa_test_harness.config.similarity_threshold,
        qa_test_harness.config.bertscore_threshold
    )


@pytest.mark.parametrize("test_case", PERFORMANCE_TEST_CASES)
def test_performance(test_case: TestCase):
    """Test response times for various query types"""
    response, response_time = qa_test_harness.execute_query(test_case.input_query)
    qa_test_harness.validate_performance(
        test_case.input_query,
        response,
        response_time
    )
