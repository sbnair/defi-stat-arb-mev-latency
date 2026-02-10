import numpy as np
import pandas as pd

def pivot_prices(prices: pd.DataFrame, pair: str) -> pd.DataFrame:
    p = prices[prices["pair"] == pair].copy()
    wide = p.pivot_table(index="ts", columns="dex", values="mid").sort_index()
    return wide.ffill().dropna()

def spread_log(p1: pd.Series, p2: pd.Series) -> pd.Series:
    return np.log(p1) - np.log(p2)

def rolling_zscore(x: pd.Series, lookback: int) -> pd.Series:
    mu = x.rolling(lookback).mean()
    sd = x.rolling(lookback).std(ddof=0)
    return (x - mu) / sd
