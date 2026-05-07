def cpmm_output(reserve_in: float, reserve_out: float, amount_in: float, fee_bps: int) -> float:
    fee = fee_bps / 10_000
    amount_in_eff = amount_in * (1 - fee)
    return reserve_out - ((reserve_in * reserve_out) / (reserve_in + amount_in_eff))
