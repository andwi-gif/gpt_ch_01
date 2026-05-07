from decimal import Decimal
from mev_agentic_ai.domain.constraints import ConstraintChecker
from mev_agentic_ai.domain.models import ArbitrageAction, SwapLeg, TriangularPath, WalletState, ArbitrageSimulationResult


def mk_action(lat='0', cyc=True, cont=True, amt=10):
    l1=SwapLeg('a','ETH','USDC')
    l2=SwapLeg('b','USDC' if cont else 'DAI','DAI')
    l3=SwapLeg('c','DAI','ETH' if cyc else 'USDC')
    return ArbitrageAction(TriangularPath('p',(l1,l2,l3)), amt, Decimal(lat))


def test_valid_passes():
    c=ConstraintChecker()
    r=c.check(mk_action(), WalletState({'ETH':100}), Decimal('1'))
    assert r.ok


def test_failures():
    c=ConstraintChecker()
    assert 'C1' in c.check(mk_action(), WalletState({'ETH':100}), Decimal('-1')).violation_codes
    assert 'C2' in c.check(mk_action(amt=200), WalletState({'ETH':100}), Decimal('1')).violation_codes
    sim=ArbitrageSimulationResult(False,1,1,'ETH','ETH',tuple(),'bad')
    assert 'C3' in c.check(mk_action(), WalletState({'ETH':100}), Decimal('1'), sim).violation_codes
    assert 'C4' in c.check(mk_action(cont=False), WalletState({'ETH':100}), Decimal('1')).violation_codes
    assert 'C5' in c.check(mk_action(cyc=False), WalletState({'ETH':100}), Decimal('1')).violation_codes
    assert 'C6' in c.check(mk_action(lat='13'), WalletState({'ETH':100}), Decimal('1')).violation_codes


def test_deterministic_multiple_violations():
    c=ConstraintChecker()
    a=mk_action(lat='13', cyc=False, cont=False, amt=200)
    r1=c.check(a, WalletState({'ETH':1}), Decimal('-1'))
    r2=c.check(a, WalletState({'ETH':1}), Decimal('-1'))
    assert r1.violation_codes == r2.violation_codes
