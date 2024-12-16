import pytest
from .test_llm_chatbot import qa_test_harness


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    qa_test_harness.logger.save_logs()



