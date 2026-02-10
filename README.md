git clone https://github.com/<you>/defi-stat-arb-mev-latency-arbitrum
cd defi-stat-arb-mev-latency-arbitrum

# Python backtest
cd python
pip install -r requirements.txt
python -m defi_stat_arb.cli --prices ../data/sample/prices_sample.csv --gas ../data/sample/gas_sample.csv

# Rust executor skeleton
cd ../rust-exec
cargo run --release
