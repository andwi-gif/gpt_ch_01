def mock_llm_response(task: str) -> dict:
    if task == "path":
        return {"path_index": 0, "confidence": 0.5, "reason": "fixture"}
    if task == "constraints":
        return {"valid": True, "violations": [], "reason": "fixture"}
    if task == "profit":
        return {"gross_gain_usd": 1.0, "gas_cost_usd": 0.1, "llm_cost_usd": 0.0, "expected_net_profit_usd": 0.9, "confidence": 0.5}
    return {"failure_label": "unknown", "violated_constraints": [], "reason": "fixture"}
