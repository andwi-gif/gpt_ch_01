from decimal import Decimal
from mev_agentic_ai.domain.models import Token, TriangularPath, SwapLeg
from mev_agentic_ai.domain.constraints import ConstraintChecker


def test_domain_construction():
    t = Token(symbol='ETH', address='ETH', decimals=18, price_usd=Decimal('2000'))
    assert t.symbol == 'ETH'
    p = TriangularPath('p',(SwapLeg('a','ETH','USDC'),SwapLeg('b','USDC','DAI'),SwapLeg('c','DAI','ETH')))
    assert p.is_continuous() and p.is_cycle_closed()
    c = ConstraintChecker()
    assert c is not None
