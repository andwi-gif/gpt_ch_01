from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from mev_agentic_ai.domain.units import gas_cost_eth, gas_cost_usd


@dataclass(slots=True, frozen=True)
class ProfitComponents:
    initial_amount_raw: int
    final_amount_raw: int
    gross_gain_raw: int
    gross_gain_usd: Decimal
    gas_cost_eth: Decimal
    gas_cost_usd: Decimal
    llm_cost_usd: Decimal
    failed_tx_cost_usd: Decimal
    conservative_c1_margin_usd: Decimal
    realized_net_profit_usd: Decimal


def compute_gross_gain_usd(initial_usd: Decimal, final_usd: Decimal) -> Decimal:
    return final_usd - initial_usd


def compute_conservative_margin_usd_for_c1(gross_gain_usd: Decimal, gas_usd: Decimal, llm_usd: Decimal, failed_tx_usd: Decimal) -> Decimal:
    return gross_gain_usd - gas_usd - llm_usd - failed_tx_usd


def compute_realized_net_profit_usd(gross_gain_usd: Decimal, gas_usd: Decimal, llm_usd: Decimal, failed_tx_usd: Decimal, included: bool) -> Decimal:
    return gross_gain_usd - gas_usd - llm_usd if included else -failed_tx_usd


def compute_roi(net_profit_usd: Decimal, initial_usd: Decimal) -> Decimal:
    if initial_usd == 0:
        return Decimal("0")
    return net_profit_usd / initial_usd


def compute_profit_components(
    initial_amount_raw: int,
    final_amount_raw: int,
    initial_usd: Decimal,
    final_usd: Decimal,
    gas_used: int,
    gas_price_gwei: Decimal,
    eth_price_usd: Decimal,
    llm_cost_usd: Decimal = Decimal("0"),
    failed_tx_cost_usd: Decimal = Decimal("0"),
    included: bool = True,
) -> ProfitComponents:
    gross_gain_raw = final_amount_raw - initial_amount_raw
    gross_gain = compute_gross_gain_usd(initial_usd, final_usd)
    gas_eth = gas_cost_eth(gas_used, gas_price_gwei)
    gas_usd = gas_cost_usd(gas_used, gas_price_gwei, eth_price_usd)
    margin = compute_conservative_margin_usd_for_c1(gross_gain, gas_usd, llm_cost_usd, failed_tx_cost_usd)
    net = compute_realized_net_profit_usd(gross_gain, gas_usd, llm_cost_usd, failed_tx_cost_usd, included)
    return ProfitComponents(initial_amount_raw, final_amount_raw, gross_gain_raw, gross_gain, gas_eth, gas_usd, llm_cost_usd, failed_tx_cost_usd, margin, net)
