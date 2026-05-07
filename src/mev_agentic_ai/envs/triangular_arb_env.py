from dataclasses import dataclass
from mev_agentic_ai.domain.constraints import ConstraintChecker


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
        check = self.checker.check(gross_gain=gross_gain, total_cost=total_cost)
        return StepResult(reward=gross_gain - total_cost, done=True, info={"constraint_valid": check.valid, "failure_label": check.label})
