mod config;
mod mev_guard;

use anyhow::Context;
use ethers::providers::{Provider, Ws};
use futures_util::StreamExt;
use std::time::Instant;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cfg = config::load("Config.arbitrum.toml")?;
    let ws = Provider::<Ws>::connect(cfg.ws_rpc.clone())
        .await
        .context("ws connect failed")?;

    println!("connected to Arbitrum WS");

    let mut blocks = ws.subscribe_blocks().await?;
    while let Some(b) = blocks.next().await {
        let t0 = Instant::now();

        // TODO: update Uniswap/Curve/Balancer mid prices using pool state / events.
        // TODO: compute z-score from rolling window (keep ring buffer).
        // TODO: estimate gas + fees (Arbitrum has dual components; treat carefully). [page:1]
        // TODO: apply MEV haircut:
        // let mev_bps = mev_guard::mev_haircut_bps(cfg.latency_ms, cfg.mev_haircut_bps_at_100ms);

        println!("block {:?} processed in {:?}", b.number, t0.elapsed());
    }

    Ok(())
}
