from mev_agentic_ai.llm.mock import mock_llm_response

def test_llm_mock_path_schema():
    out = mock_llm_response("path")
    assert "path_index" in out and "confidence" in out and "reason" in out
