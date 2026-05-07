from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Mapping


@dataclass(slots=True, frozen=True)
class Token:
    symbol: str
    address: str
    decimals: int
    price_usd: Decimal | None = None


@dataclass(slots=True)
class Pool:
    pool_id: str
    dex: str
    token0: Token
    token1: Token
    reserve0_raw: int
    reserve1_raw: int
    fee_bps: int = 30


@dataclass(slots=True, frozen=True)
class SwapLeg:
    pool_id: str
    token_in: str
    token_out: str


@dataclass(slots=True, frozen=True)
class TriangularPath:
    path_id: str
    legs: tuple[SwapLeg, SwapLeg, SwapLeg]

    def is_continuous(self) -> bool:
        return self.legs[0].token_out == self.legs[1].token_in and self.legs[1].token_out == self.legs[2].token_in

    def is_cycle_closed(self) -> bool:
        return self.legs[2].token_out == self.legs[0].token_in


@dataclass(slots=True)
class WalletState:
    balances_raw: Mapping[str, int] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class GasState:
    gas_used: int
    gas_price_gwei: Decimal
    failed_tx_gas_used: int = 0


@dataclass(slots=True, frozen=True)
class ArbitrageAction:
    path: TriangularPath
    amount_in_raw: int
    latency_seconds: Decimal = Decimal("0")
    llm_cost_usd: Decimal = Decimal("0")


@dataclass(slots=True, frozen=True)
class SwapResult:
    amount_in_raw: int
    amount_out_raw: int
    token_in: str
    token_out: str
    reserve_in_after_raw: int
    reserve_out_after_raw: int


@dataclass(slots=True, frozen=True)
class ArbitrageSimulationResult:
    success: bool
    amount_in_raw: int
    amount_out_raw: int
    start_token: str
    end_token: str
    swaps: tuple[SwapResult, ...]
    reason: str | None = None
