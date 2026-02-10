from dataclasses import dataclass
import pandas as pd

from .features import spread_log, rolling_zscore
from .cost import mev_haircut_bps, gas_cost_usd

@dataclass
class Trade:
    entry_ts: pd.Timestamp
    exit_ts: pd.Timestamp
    pnl_usd: float
    gross_edge_bps: float
    net_edge_bps: float
    gas_usd: float

def _exec_ts(index: pd.DatetimeIndex, ts: pd.Timestamp, latency_ms: int) -> pd.Timestamp:
    target = ts + pd.Timedelta(milliseconds=latency_ms)
    j = index.searchsorted(target)
    if j >= len(index):
        return index[-1]
    return index[j]

def run_backtest_uniswap_vs_curve(
    wide_prices: pd.DataFrame,
    gas: pd.DataFrame,
    lookback: int,
    entry_z: float,
    exit_z: float,
    latency_ms: int,
    notional_usd: float,
    slip_bps: float,
    mev_bps_at_100ms: float,
    min_edge_after_cost_bps: float,
    gas_used_estimate: int = 220_000,
) -> list[Trade]:
    # Spread and signal
    s = spread_log(wide_prices["uniswap"], wide_prices["curve"])
    z = rolling_zscore(s, lookback).dropna()
    idx = z.index

    # Gas lookup
    g = gas.set_index("ts").sort_index()
    gas_price = g["gas_price_gwei"]
    eth_px = g["eth_price_usd"]

    in_pos = False
    entry_ts = None
    entry_spread = None
    trades: list[Trade] = []

    for ts in idx:
        if not in_pos:
            if z.loc[ts] >= entry_z or z.loc[ts] <= -entry_z:
                in_pos = True
                entry_ts = _exec_ts(idx, ts, latency_ms)
                entry_spread = s.loc[entry_ts]
        else:
            if abs(z.loc[ts]) <= exit_z:
                exit_ts = _exec_ts(idx, ts, latency_ms)
                exit_spread = s.loc[exit_ts]

                gross_edge_bps = (entry_spread - exit_spread) * 10_000.0
                gross_edge_bps -= slip_bps

                mev_bps = mev_haircut_bps(latency_ms, mev_bps_at_100ms)
                net_edge_bps = gross_edge_bps - mev_bps

                gp = float(gas_price.asof(exit_ts))
                ep = float(eth_px.asof(exit_ts))
                gas_usd = gas_cost_usd(gas_used_estimate, gp, ep)

                pnl_usd = (net_edge_bps / 10_000.0) * notional_usd - gas_usd

                # Guardrail: skip “paper trades” that wouldn’t be sent
                if net_edge_bps >= min_edge_after_cost_bps:
                    trades.append(Trade(entry_ts, exit_ts, pnl_usd, gross_edge_bps, net_edge_bps, gas_usd))

                in_pos = False
                entry_ts, entry_spread = None, None

    return trades
