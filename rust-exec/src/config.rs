use serde::Deserialize;

#[derive(Clone, Deserialize)]
pub struct Config {
    pub ws_rpc: String,
    pub http_rpc: String,
    pub pair: String,
    pub entry_z: f64,
    pub exit_z: f64,
    pub latency_ms: u64,
    pub mev_haircut_bps_at_100ms: f64,
    pub min_edge_after_cost_bps: f64,
}

pub fn load(path: &str) -> anyhow::Result<Config> {
    let s = std::fs::read_to_string(path)?;
    Ok(toml::from_str(&s)?)
}
