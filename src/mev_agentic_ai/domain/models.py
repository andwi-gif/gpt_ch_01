from dataclasses import dataclass


@dataclass(slots=True)
class Token:
    symbol: str
    decimals: int


@dataclass(slots=True)
class Pool:
    pool_address: str
    token0: str
    token1: str
    fee_bps: int


@dataclass(slots=True)
class ArbitrageAction:
    path_id: str
    trade_fraction: float
