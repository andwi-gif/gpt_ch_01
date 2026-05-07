def net_profit(gross_gain: float, gas_cost: float, llm_cost: float, failed_tx_cost: float) -> float:
    return gross_gain - gas_cost - llm_cost - failed_tx_cost
