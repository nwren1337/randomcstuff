import argparse
import json
import matplotlib.pyplot as plt
from pathlib import Path

TESTDATA = Path(__file__).parent / "testdata"
ALGORITHMS = ["insertion", "merge", "quick"]
DATA_TYPES = ["random", "ascending", "descending"]
COLORS = {"insertion": "tab:blue", "merge": "tab:orange", "quick": "tab:green"}


def resolve_epoch(epoch: int | None) -> int:
    candidates = list(TESTDATA.glob("results-*.json"))
    if not candidates:
        raise FileNotFoundError(f"No results-<epoch>.json files found in {TESTDATA}")
    if epoch is not None:
        return epoch
    return max(int(p.stem.split("-")[1]) for p in candidates)


parser = argparse.ArgumentParser(description="Plot sorting algorithm benchmark results.")
parser.add_argument("--epoch", type=int, default=None, help="Epoch timestamp of the results file to plot (default: most recent)")
args = parser.parse_args()

epoch = resolve_epoch(args.epoch)
data_file = TESTDATA / f"results-{epoch}.json"
if not data_file.exists():
    raise FileNotFoundError(f"{data_file} not found")

data = json.loads(data_file.read_text())


def extract_runtime(data_type: str, alg: str) -> tuple[list[int], list[float], list[float]]:
    rows = sorted(
        ((int(sz), v) for sz, v in data.get(data_type, {}).items()
         if alg in v and "status" not in v[alg]),
        key=lambda x: x[0],
    )
    sizes = [r[0] for r in rows]
    means = [r[1][alg]["runtime_mean_ms"] for r in rows]
    stddevs = [r[1][alg]["runtime_stddev_ms"] for r in rows]
    return sizes, means, stddevs


handles = [plt.Line2D([0], [0], color=COLORS[alg], marker="o", label=alg) for alg in ALGORITHMS]


def has_runtime_data(data_type: str) -> bool:
    return any(
        alg in v and "status" not in v[alg]
        for v in data.get(data_type, {}).values()
        for alg in ALGORITHMS
    )


# Figure 1: runtime scaling — only plot data types that have results
active_types = [dt for dt in DATA_TYPES if has_runtime_data(dt)]
if active_types:
    fig, axes = plt.subplots(1, len(active_types), figsize=(5 * len(active_types), 5), sharey=True, squeeze=False)
    for ax, dt in zip(axes[0], active_types):
        for alg in ALGORITHMS:
            sizes, means, stddevs = extract_runtime(dt, alg)
            if sizes:
                ax.errorbar(sizes, means, yerr=stddevs, label=alg,
                            color=COLORS[alg], marker="o", capsize=3)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(dt)
        ax.set_xlabel("array size")
        ax.grid(True, which="both", alpha=0.3)

    axes[0][0].set_ylabel("runtime (ms)")
    fig.legend(handles=handles, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.0))
    fig.suptitle("Sorting algorithm runtime scaling", y=1.05)
    plt.tight_layout()
    out = TESTDATA / f"runtime_scaling-{epoch}.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved testdata/{out.name}")
else:
    print("Skipping runtime scaling chart — no data")


# Figure 2: CPU counters for random data
COUNTERS = ["cycles", "instructions", "cache_misses", "branch_misses"]
counter_rows = {
    counter: {
        alg: sorted(
            ((int(sz), v[alg][counter])
             for sz, v in data.get("random", {}).items()
             if alg in v and "status" not in v[alg] and v[alg].get(counter) is not None),
            key=lambda x: x[0],
        )
        for alg in ALGORITHMS
    }
    for counter in COUNTERS
}
if any(rows for alg_rows in counter_rows.values() for rows in alg_rows.values()):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, counter in zip(axes.flat, COUNTERS):
        for alg in ALGORITHMS:
            rows = counter_rows[counter][alg]
            if rows:
                ax.plot([r[0] for r in rows], [r[1] for r in rows],
                        label=alg, color=COLORS[alg], marker="o")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(counter.replace("_", " "))
        ax.set_xlabel("array size")
        ax.grid(True, which="both", alpha=0.3)

    fig.legend(handles=handles, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.0))
    fig.suptitle("CPU counters — random data", y=1.05)
    plt.tight_layout()
    out = TESTDATA / f"cpu_counters-{epoch}.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved testdata/{out.name}")
else:
    print("Skipping CPU counters chart — no random data")
