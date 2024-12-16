# LLM Question-Answer System Testing Framework

A solution for evaluating Large Language Model (LLM) based Question-Answering systems. The framework focuses on response quality and performance metrics using Llama as the LLM engine.

## Technical Stack

- Python 3.10
- Poetry for dependency management
- LLM engine
- pytest for test execution
- Allure for test reporting
- BERTScore and cosine similarity for response evaluation

## Prerequisites

- Python 3.10+
- Poetry
- LLM instance running locally or accessible via API
- Git (for version control)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up environment variables (create a `.env` file):
```env
LLM_API_URL=http://localhost:11434/api
LLM_MODEL=llama3.2
SIMILARITY_THRESHOLD=0.8
BERTSCORE_THRESHOLD=0.8
QUERY_MAX_TIME=2  # in seconds
```

## Configuration

### Environment Variables

| Variable             | Description                         | Default |
|----------------------|-------------------------------------|---------|
| LLM_API_URL          | URL for LLM API endpoint            | http://localhost:11434/api |
| LLM_MODEL            | Model version to use                | llama3.2 |
| SIMILARITY_THRESHOLD | Minimum acceptable similarity score | 0.8 |
| BERTSCORE_THRESHOLD  | Minimum acceptable BERTScore        | 0.8 |
| QUERY_MAX_TIME       | Maximum response time in seconds    | 2 |

## Testing Components

### Response Quality Testing
- Similarity scoring using cosine similarity
- Semantic evaluation using BERTScore
- Response content validation against knowledge base

### Performance Testing
- Response time measurement
- Timeout handling
- Performance benchmarking for different query types

## Test Execution

1. Run all tests:
```bash
poetry run pytest
```

2. Run specific test categories:
```bash
poetry run pytest -v -k "test_response_quality"  # Quality tests only
poetry run pytest -v -k "test_performance"       # Performance tests only
```

3. Generate Allure report:
```bash
poetry run pytest --alluredir=./allure-results
allure serve allure-results
```

## Test Results

### JSON Results
Test results are stored in `project/test/reports/test_results.json` with the following structure:
```json
{
    "input": "query text",
    "expected_output": "expected response",
    "generated_response": "actual response",
    "similarity": 0.85,
    "bertscore": 0.90,
    "response_time": 1.5,
    "result": "pass/fail"
}
```

### Allure Reports
- Detailed test execution history
- Response quality metrics visualization
- Performance timing analysis
- Test failure analysis

## Adding New Tests

1. Add test cases to `RESPONSE_QUALITY_TEST_CASES` or `PERFORMANCE_TEST_CASES`:
```python
TestCase("Your query", "Expected response", "knowledge_key")
```

2. Add corresponding knowledge base entries:
```python
KNOWLEDGE_BASE = {
    "knowledge_key": {
        "expected_response": "Expected response text",
        "required_keywords": ["key", "words"]
    }
}
```
