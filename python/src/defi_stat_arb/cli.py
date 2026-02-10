import argparse
from .config import BacktestConfig
from .data import load_prices, load_gas
from .features import pivot_prices
from .backtest import run_backtest_uniswap_vs_curve
from .metrics import equity_curve, sharpe_from_trade_pnl, max_drawdown

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prices", default="../../data/sample/prices_sample.csv")
    ap.add_argument("--gas", default="../../data/sample/gas_sample.csv")
    args = ap.parse_args()

    cfg = BacktestConfig()

    prices = load_prices(args.prices)
    gas = load_gas(args.gas)
    wide = pivot_prices(prices, cfg.strategy.pair)

    trades = run_backtest_uniswap_vs_curve(
        wide_prices=wide,
        gas=gas,
        lookback=cfg.strategy.lookback,
        entry_z=cfg.strategy.entry_z,
        exit_z=cfg.strategy.exit_z,
        latency_ms=cfg.costs.latency_ms,
        notional_usd=cfg.strategy.notional_usd,
        slip_bps=cfg.costs.slip_bps,
        mev_bps_at_100ms=cfg.costs.mev_haircut_bps_at_100ms,
        min_edge_after_cost_bps=cfg.costs.min_edge_after_cost_bps,
    )

    eq = equity_curve(trades)
    print("trades:", len(trades))
    print("sharpe:", sharpe_from_trade_pnl(trades))
    print("max_drawdown_usd:", max_drawdown(eq))
    if not eq.empty:
        print("final_pnl_usd:", float(eq.iloc[-1]))

if __name__ == "__main__":
    main()
