import numpy as np
import pandas as pd

def equity_curve(trades) -> pd.Series:
    if not trades:
        return pd.Series(dtype=float)
    eq = pd.Series([t.pnl_usd for t in trades], index=[t.exit_ts for t in trades]).sort_index().cumsum()
    return eq

def max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    peak = equity.cummax()
    dd = equity - peak
    return float(dd.min())

def sharpe_from_trade_pnl(trades, periods_per_year: float = 252.0) -> float:
    if len(trades) < 10:
        return float("nan")
    r = np.array([t.pnl_usd for t in trades], dtype=float)
    mu = r.mean()
    sd = r.std(ddof=1)
    if sd == 0:
        return float("nan")
    return float((mu / sd) * np.sqrt(periods_per_year))
