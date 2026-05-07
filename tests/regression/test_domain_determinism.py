from decimal import Decimal
from mev_agentic_ai.domain.constraints import ConstraintChecker
from mev_agentic_ai.domain.models import ArbitrageAction, SwapLeg, TriangularPath, WalletState


def test_constraint_result_stable():
    c=ConstraintChecker()
    a=ArbitrageAction(TriangularPath('p',(SwapLeg('a','ETH','USDC'),SwapLeg('b','USDC','DAI'),SwapLeg('c','DAI','ETH'))),10,Decimal('0'))
    r=[c.check(a, WalletState({'ETH':100}), Decimal('1')).violation_codes for _ in range(5)]
    assert all(x==r[0] for x in r)
