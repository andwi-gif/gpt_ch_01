from mev_agentic_ai.domain.cpmm import get_amount_out, apply_cpmm_swap, invariant, simulate_triangular_path
from mev_agentic_ai.domain.models import Token, Pool, SwapLeg, TriangularPath


def _pool(a="ETH", b="USDC"):
    return Pool("p1", "uni", Token(a, a, 18), Token(b, b, 6), 1_000_000, 2_000_000, 30)


def test_amount_out_fee_and_no_fee():
    assert get_amount_out(1000, 1_000_000, 2_000_000, 0) > get_amount_out(1000, 1_000_000, 2_000_000, 30)


def test_swap_and_invariant_non_decrease():
    p = _pool()
    k0 = invariant(p)
    p2, sw = apply_cpmm_swap(p, "ETH", 1000)
    assert sw.amount_out_raw > 0
    assert invariant(p2) >= k0


def test_triangular_exactly_three_swaps():
    pools = {
        "a": Pool("a", "uni", Token("ETH","ETH",18), Token("USDC","USDC",6), 1_000_000, 2_000_000, 30),
        "b": Pool("b", "uni", Token("USDC","USDC",6), Token("DAI","DAI",18), 2_000_000, 2_000_000, 30),
        "c": Pool("c", "uni", Token("DAI","DAI",18), Token("ETH","ETH",18), 2_000_000, 1_000_000, 30),
    }
    path = TriangularPath("t", (SwapLeg("a","ETH","USDC"), SwapLeg("b","USDC","DAI"), SwapLeg("c","DAI","ETH")))
    res = simulate_triangular_path(path, pools, 1000)
    assert res.success
    assert len(res.swaps) == 3
