def wei_to_gwei(wei: int) -> float:
    return wei / 1_000_000_000


def gwei_to_wei(gwei: float) -> int:
    return int(gwei * 1_000_000_000)
