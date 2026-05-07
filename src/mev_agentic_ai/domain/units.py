from decimal import Decimal, ROUND_FLOOR

WEI_PER_ETH = Decimal("1000000000000000000")
GWEI_PER_ETH = Decimal("1000000000")


def wei_to_eth(wei: int) -> Decimal:
    return Decimal(wei) / WEI_PER_ETH


def eth_to_wei(eth: Decimal) -> int:
    return int((eth * WEI_PER_ETH).to_integral_value(rounding=ROUND_FLOOR))


def gwei_to_eth(gwei: Decimal) -> Decimal:
    return gwei / GWEI_PER_ETH


def eth_to_gwei(eth: Decimal) -> Decimal:
    return eth * GWEI_PER_ETH


def token_raw_to_decimal(raw: int, decimals: int) -> Decimal:
    return Decimal(raw) / (Decimal(10) ** decimals)


def token_decimal_to_raw(amount: Decimal, decimals: int) -> int:
    return int((amount * (Decimal(10) ** decimals)).to_integral_value(rounding=ROUND_FLOOR))


def token_raw_to_usd(raw: int, decimals: int, price_usd: Decimal) -> Decimal:
    return token_raw_to_decimal(raw, decimals) * price_usd


def usd_to_token_raw(usd: Decimal, decimals: int, price_usd: Decimal) -> int:
    return token_decimal_to_raw(usd / price_usd, decimals)


def gas_cost_eth(gas_used: int, gas_price_gwei: Decimal) -> Decimal:
    return gwei_to_eth(Decimal(gas_used) * gas_price_gwei)


def gas_cost_usd(gas_used: int, gas_price_gwei: Decimal, eth_price_usd: Decimal) -> Decimal:
    return gas_cost_eth(gas_used, gas_price_gwei) * eth_price_usd
