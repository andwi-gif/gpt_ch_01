from mev_agentic_ai.llm.mock import mock_llm_response

def run_benchmark(task: str) -> dict:
    return mock_llm_response(task)
