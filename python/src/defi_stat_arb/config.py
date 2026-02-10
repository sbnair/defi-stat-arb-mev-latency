from dataclasses import dataclass

@dataclass(frozen=True)
class StrategyConfig:
    pair: str = "WETH-USDC"
    entry_z: float = 2.0
    exit_z: float = 0.5
    lookback: int = 500
    notional_usd: float = 10_000.0

@dataclass(frozen=True)
class ExecCostConfig:
    latency_ms: int = 100
    slip_bps: float = 5.0
    mev_haircut_bps_at_100ms: float = 8.0
    min_edge_after_cost_bps: float = 5.0

@dataclass(frozen=True)
class ChainConfig:
    # Arbitrum: blocks ~0.25s (useful for narrative + plots)
    approx_block_time_s: float = 0.25

@dataclass(frozen=True)
class BacktestConfig:
    strategy: StrategyConfig = StrategyConfig()
    costs: ExecCostConfig = ExecCostConfig()
    chain: ChainConfig = ChainConfig()
