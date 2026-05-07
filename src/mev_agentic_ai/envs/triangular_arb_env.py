from dataclasses import dataclass
from decimal import Decimal

from mev_agentic_ai.domain.constraints import ConstraintChecker
from mev_agentic_ai.domain.models import ArbitrageAction, SwapLeg, TriangularPath, WalletState


@dataclass(slots=True)
class StepResult:
    reward: float
    done: bool
    info: dict


class TriangularArbEnv:
    def __init__(self) -> None:
        self.checker = ConstraintChecker()

    def reset(self, seed: int | None = None) -> dict:
        return {"seed": seed, "offline": True}

    def step(self, gross_gain: float, total_cost: float) -> StepResult:
        path = TriangularPath("stub", (SwapLeg("p", "ETH", "USDC"), SwapLeg("p", "USDC", "DAI"), SwapLeg("p", "DAI", "ETH")))
        action = ArbitrageAction(path=path, amount_in_raw=1, latency_seconds=Decimal("0"))
        check = self.checker.check(action=action, wallet=WalletState({"ETH": 1}), conservative_margin_usd=Decimal(str(gross_gain-total_cost)))
        return StepResult(reward=gross_gain - total_cost, done=True, info={"constraint_valid": check.ok, "failure_label": check.failure_label})
