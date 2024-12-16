from dataclasses import dataclass


@dataclass
class TestCase:
    input_query: str
    expected_output: str
    knowledge_key: str
