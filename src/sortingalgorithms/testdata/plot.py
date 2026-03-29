import json
import matplotlib.pyplot as plt
from pathlib import Path

DATA_FILE = Path("results.json")
ALGORITHMS = ["insertion", "merge", "quick"]
DATA_TYPES = ["random", "ascending", "descending"]
COLORS = {"insertion": "tab:blue", "merge": "tab:orange", "quick": "tab:green"}

data = json.loads(DATA_FILE.read_text())


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


# Figure 1: runtime scaling per data type
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
for ax, dt in zip(axes, DATA_TYPES):
    for alg in ALGORITHMS:
        sizes, means, stddevs = extract_runtime(dt, alg)
        ax.errorbar(sizes, means, yerr=stddevs, label=alg,
                    color=COLORS[alg], marker="o", capsize=3)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(dt)
    ax.set_xlabel("array size")
    ax.grid(True, which="both", alpha=0.3)

axes[0].set_ylabel("runtime (ms)")
handles = [plt.Line2D([0], [0], color=COLORS[alg], marker="o", label=alg) for alg in ALGORITHMS]
fig.legend(handles=handles, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.0))
fig.suptitle("Sorting algorithm runtime scaling", y=1.05)
plt.tight_layout()
plt.savefig("runtime_scaling.png", dpi=150, bbox_inches="tight")
print("Saved runtime_scaling.png")


# Figure 2: CPU counters for random data
COUNTERS = ["cycles", "instructions", "cache_misses", "branch_misses"]
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, counter in zip(axes.flat, COUNTERS):
    for alg in ALGORITHMS:
        rows = sorted(
            ((int(sz), v[alg][counter])
             for sz, v in data.get("random", {}).items()
             if alg in v and "status" not in v[alg] and v[alg].get(counter) is not None),
            key=lambda x: x[0],
        )
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
plt.savefig("cpu_counters.png", dpi=150, bbox_inches="tight")
print("Saved cpu_counters.png")
