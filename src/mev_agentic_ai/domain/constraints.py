from dataclasses import dataclass


@dataclass(slots=True)
class ConstraintResult:
    valid: bool
    label: str = "none"


class ConstraintChecker:
    """Deterministic scaffold checker for routing all executable actions."""

    def check(self, gross_gain: float, total_cost: float) -> ConstraintResult:
        if gross_gain <= total_cost:
            return ConstraintResult(valid=False, label="gas_cost_exceeds_gain")
        return ConstraintResult(valid=True)
