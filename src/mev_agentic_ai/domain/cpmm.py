from __future__ import annotations

from dataclasses import replace

from mev_agentic_ai.domain.models import ArbitrageSimulationResult, Pool, SwapResult, TriangularPath


class DomainMathError(ValueError):
    pass


def get_amount_out(amount_in_raw: int, reserve_in_raw: int, reserve_out_raw: int, fee_bps: int) -> int:
    if amount_in_raw <= 0:
        raise DomainMathError("amount_in_raw must be positive")
    if reserve_in_raw <= 0 or reserve_out_raw <= 0:
        raise DomainMathError("reserves must be positive")
    fee_den = 10_000
    amount_in_with_fee = amount_in_raw * (fee_den - fee_bps)
    numerator = amount_in_with_fee * reserve_out_raw
    denominator = reserve_in_raw * fee_den + amount_in_with_fee
    out = numerator // denominator
    if out <= 0 or out >= reserve_out_raw:
        raise DomainMathError("insufficient reserve/output infeasible")
    return out


def _select_reserves(pool: Pool, token_in: str) -> tuple[int, int, bool]:
    if token_in == pool.token0.symbol:
        return pool.reserve0_raw, pool.reserve1_raw, True
    if token_in == pool.token1.symbol:
        return pool.reserve1_raw, pool.reserve0_raw, False
    raise DomainMathError("token not in pool")


def apply_cpmm_swap(pool: Pool, token_in: str, amount_in_raw: int) -> tuple[Pool, SwapResult]:
    reserve_in, reserve_out, in_is_token0 = _select_reserves(pool, token_in)
    amount_out = get_amount_out(amount_in_raw, reserve_in, reserve_out, pool.fee_bps)
    if in_is_token0:
        updated = replace(pool, reserve0_raw=pool.reserve0_raw + amount_in_raw, reserve1_raw=pool.reserve1_raw - amount_out)
        token_out = pool.token1.symbol
        rin_after, rout_after = updated.reserve0_raw, updated.reserve1_raw
    else:
        updated = replace(pool, reserve1_raw=pool.reserve1_raw + amount_in_raw, reserve0_raw=pool.reserve0_raw - amount_out)
        token_out = pool.token0.symbol
        rin_after, rout_after = updated.reserve1_raw, updated.reserve0_raw
    return updated, SwapResult(amount_in_raw, amount_out, token_in, token_out, rin_after, rout_after)


def invariant(pool: Pool) -> int:
    return pool.reserve0_raw * pool.reserve1_raw


def simulate_triangular_path(path: TriangularPath, pools: dict[str, Pool], amount_in_raw: int) -> ArbitrageSimulationResult:
    if not path.is_continuous() or not path.is_cycle_closed():
        return ArbitrageSimulationResult(False, amount_in_raw, amount_in_raw, path.legs[0].token_in, path.legs[-1].token_out, tuple(), "broken path")
    amount = amount_in_raw
    updated = dict(pools)
    swaps: list[SwapResult] = []
    for leg in path.legs:
        pool = updated[leg.pool_id]
        pool2, swap = apply_cpmm_swap(pool, leg.token_in, amount)
        updated[leg.pool_id] = pool2
        amount = swap.amount_out_raw
        if swap.token_out != leg.token_out:
            return ArbitrageSimulationResult(False, amount_in_raw, amount, path.legs[0].token_in, swap.token_out, tuple(swaps), "token mismatch")
        swaps.append(swap)
    return ArbitrageSimulationResult(True, amount_in_raw, amount, path.legs[0].token_in, path.legs[-1].token_out, tuple(swaps))
