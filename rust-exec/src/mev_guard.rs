pub fn mev_haircut_bps(latency_ms: u64, base_bps_at_100ms: f64) -> f64 {
    let l = latency_ms as f64;
    if l <= 30.0 { 0.35 * base_bps_at_100ms }
    else if l <= 100.0 { 1.00 * base_bps_at_100ms }
    else if l <= 200.0 { 1.75 * base_bps_at_100ms }
    else { 2.50 * base_bps_at_100ms }
}
