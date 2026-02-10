import matplotlib.pyplot as plt

def plot_sharpe_vs_latency(latencies_ms, sharpes, out_path):
    plt.figure(figsize=(7,4))
    plt.plot(latencies_ms, sharpes, marker="o")
    plt.xlabel("Latency (ms)")
    plt.ylabel("Sharpe (trade-level proxy)")
    plt.title("Sharpe degradation vs latency (Arbitrum)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
