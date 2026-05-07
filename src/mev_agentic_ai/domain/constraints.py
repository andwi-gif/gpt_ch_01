from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from mev_agentic_ai.domain.models import ArbitrageAction, ArbitrageSimulationResult, TriangularPath, WalletState
from mev_agentic_ai.domain.profit import ProfitComponents


@dataclass(slots=True, frozen=True)
class ConstraintConfig:
    max_latency_seconds: Decimal = Decimal("12")


@dataclass(slots=True, frozen=True)
class ConstraintViolation:
    code: str
    message: str


@dataclass(slots=True)
class ConstraintResult:
    ok: bool
    violation_codes: list[str] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)
    failure_label: str = "none"
    profit_components: ProfitComponents | None = None
    simulation_result: ArbitrageSimulationResult | None = None


class ConstraintChecker:
    def __init__(self, config: ConstraintConfig | None = None) -> None:
        self.config = config or ConstraintConfig()

    def check_c1_economic_rationality(self, conservative_margin_usd: Decimal) -> ConstraintViolation | None:
        if conservative_margin_usd <= 0:
            return ConstraintViolation("C1", "Economic rationality failed: gain <= gas+llm+failed cost")
        return None

    def check_c2_wallet_balance(self, wallet: WalletState, token_symbol: str, amount_in_raw: int) -> ConstraintViolation | None:
        if amount_in_raw > wallet.balances_raw.get(token_symbol, 0):
            return ConstraintViolation("C2", "Wallet balance insufficient")
        return None

    def check_c3_pool_reserve_feasibility(self, simulation_result: ArbitrageSimulationResult | None) -> ConstraintViolation | None:
        if simulation_result is not None and not simulation_result.success:
            return ConstraintViolation("C3", "Pool reserve feasibility failed")
        return None

    def check_c4_path_continuity(self, path: TriangularPath) -> ConstraintViolation | None:
        if not path.is_continuous():
            return ConstraintViolation("C4", "Path continuity failed")
        return None

    def check_c5_cycle_closure(self, path: TriangularPath) -> ConstraintViolation | None:
        if not path.is_cycle_closed():
            return ConstraintViolation("C5", "Path cycle closure failed")
        return None

    def check_c6_latency_budget(self, latency_seconds: Decimal) -> ConstraintViolation | None:
        if latency_seconds > self.config.max_latency_seconds:
            return ConstraintViolation("C6", "Latency budget exceeded")
        return None

    def check(self, action: ArbitrageAction, wallet: WalletState, conservative_margin_usd: Decimal, simulation_result: ArbitrageSimulationResult | None = None) -> ConstraintResult:
        violations = [
            self.check_c4_path_continuity(action.path),
            self.check_c5_cycle_closure(action.path),
            self.check_c2_wallet_balance(wallet, action.path.legs[0].token_in, action.amount_in_raw),
            self.check_c6_latency_budget(action.latency_seconds),
            self.check_c1_economic_rationality(conservative_margin_usd),
            self.check_c3_pool_reserve_feasibility(simulation_result),
        ]
        v = [x for x in violations if x is not None]
        result = ConstraintResult(ok=len(v) == 0, violation_codes=[i.code for i in v], messages=[i.message for i in v], simulation_result=simulation_result)
        if v:
            if "C2" in result.violation_codes:
                result.failure_label = "insufficient_wallet"
            elif "C3" in result.violation_codes:
                result.failure_label = "insufficient_reserve"
            elif "C6" in result.violation_codes:
                result.failure_label = "latency_expired"
            elif "C1" in result.violation_codes:
                result.failure_label = "gas_cost_exceeds_gain"
            elif "C4" in result.violation_codes or "C5" in result.violation_codes:
                result.failure_label = "path_not_cyclic"
            else:
                result.failure_label = "constraint_violation"
        return result
