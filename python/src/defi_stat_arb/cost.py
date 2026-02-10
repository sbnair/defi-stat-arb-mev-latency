def mev_haircut_bps(latency_ms: int, base_bps_at_100ms: float) -> float:
    # Simple monotone rule: slower => larger haircut (MEV competition + stale quotes).
    if latency_ms <= 30:
        return 0.35 * base_bps_at_100ms
    if latency_ms <= 100:
        return 1.00 * base_bps_at_100ms
    if latency_ms <= 200:
        return 1.75 * base_bps_at_100ms
    return 2.50 * base_bps_at_100ms

def gas_cost_usd(gas_used: int, gas_price_gwei: float, eth_price_usd: float) -> float:
    gas_cost_eth = gas_used * (gas_price_gwei * 1e9) / 1e18
    return gas_cost_eth * eth_price_usd
