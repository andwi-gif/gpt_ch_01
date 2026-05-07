from decimal import Decimal
from mev_agentic_ai.domain.units import (
    eth_to_gwei, eth_to_wei, gwei_to_eth, token_decimal_to_raw,
    token_raw_to_decimal, token_raw_to_usd, usd_to_token_raw, wei_to_eth,
)


def test_wei_eth_roundtrip():
    assert eth_to_wei(Decimal("1")) == 10**18
    assert wei_to_eth(10**18) == Decimal("1")


def test_gwei_eth():
    assert gwei_to_eth(Decimal("1")) == Decimal("0.000000001")
    assert eth_to_gwei(Decimal("1")) == Decimal("1000000000")


def test_token_conversion_and_usd():
    raw = token_decimal_to_raw(Decimal("1.5"), 6)
    assert raw == 1_500_000
    assert token_raw_to_decimal(raw, 6) == Decimal("1.5")
    assert token_raw_to_usd(raw, 6, Decimal("1")) == Decimal("1.5")
    assert usd_to_token_raw(Decimal("1.5"), 6, Decimal("1")) == 1_500_000
