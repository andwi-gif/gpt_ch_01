from decimal import Decimal
from mev_agentic_ai.domain.profit import (
    compute_conservative_margin_usd_for_c1,
    compute_profit_components,
    compute_roi,
)


def test_profit_positive_and_negative():
    c = compute_profit_components(100,120,Decimal('10'),Decimal('12'),100_000,Decimal('5'),Decimal('2000'),Decimal('0.1'),Decimal('1'),True)
    assert c.realized_net_profit_usd > 0
    c2 = compute_profit_components(100,101,Decimal('10'),Decimal('10.1'),1_000_000,Decimal('100'),Decimal('2000'))
    assert c2.realized_net_profit_usd < 0


def test_roi_and_failed_cost_margin():
    assert compute_roi(Decimal('1'), Decimal('10')) == Decimal('0.1')
    assert compute_roi(Decimal('1'), Decimal('0')) == Decimal('0')
    m = compute_conservative_margin_usd_for_c1(Decimal('5'), Decimal('2'), Decimal('1'), Decimal('3'))
    assert m == Decimal('-1')
