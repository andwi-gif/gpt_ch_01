from mev_agentic_ai.domain.models import Token
from mev_agentic_ai.domain.constraints import ConstraintChecker

def test_domain_construction():
    t = Token(symbol="ETH", decimals=18)
    assert t.symbol == "ETH"
    c = ConstraintChecker()
    assert c.check(2.0, 1.0).valid
