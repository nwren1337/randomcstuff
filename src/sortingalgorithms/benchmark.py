import asyncio
import json
import argparse
import tempfile
import os
from pathlib import Path
from tqdm import tqdm

BINARY: str = "./build/srt_driver"
DATA_DIR: Path = Path("data")
OUTPUT: str = "testdata/results.json"

TIMEOUT_S: int = 120
MAX_CONCURRENT: int = 4
HYPERFINE_WARMUP: int = 2

ALGORITHMS: list[str] = ["i", "m", "q"]
ALGORITHM_NAMES: dict[str, str] = {"i": "insertion", "m": "merge", "q": "quick"}
DATA_TYPES: list[str] = ["random", "ascending", "descending"]
SIZES: list[int] = [10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000]

PERF_EVENTS: list[str] = ["cycles", "instructions", "cache-misses", "branch-misses"]


async def run_hyperfine(alg: str, filepath: Path, core: int) -> dict:
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".json")
    os.close(tmp_fd)

    try:
        proc = await asyncio.create_subprocess_exec(
            "hyperfine",
            "--export-json", tmp_path,
            "-w", str(HYPERFINE_WARMUP),
            f"taskset -c {core} {BINARY} -q -a {alg} {filepath}",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            _, stderr = await proc.communicate()
        except asyncio.CancelledError:
            proc.kill()
            await proc.wait()
            raise
        if proc.returncode != 0:
            raise RuntimeError(f"hyperfine: {stderr.decode().strip()}")

        with open(tmp_path) as f:
            data = json.load(f)
    finally:
        os.unlink(tmp_path)

    result = data["results"][0]
    return {
        "runtime_mean_ms": result["mean"] * 1000,
        "runtime_stddev_ms": result["stddev"] * 1000,
        "runtime_min_ms": result["min"] * 1000,
        "runtime_max_ms": result["max"] * 1000,
    }


async def run_perf(alg: str, filepath: Path, core: int) -> dict:
    proc = await asyncio.create_subprocess_exec(
        "taskset", "-c", str(core),
        "perf", "stat",
        "-e", ",".join(PERF_EVENTS),
        "-x", ",",
        BINARY, "-q", "-a", alg, str(filepath),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        _, stderr = await proc.communicate()
    except asyncio.CancelledError:
        proc.kill()
        await proc.wait()
        raise
    if proc.returncode != 0:
        raise RuntimeError(f"perf: {stderr.decode().strip()}")

    result: dict = {}
    for line in stderr.decode().splitlines():
        parts = line.split(",")
        if len(parts) < 3:
            continue
        value_str, _, event = parts[0], parts[1], parts[2]
        event = event.strip().split(":")[0]
        if event in PERF_EVENTS:
            try:
                result[event.replace("-", "_")] = int(value_str.strip())
            except ValueError:
                result[event.replace("-", "_")] = None

    return result


async def benchmark_one(
    alg: str, data_type: str, size: int, core: int, timeout: int, progress: tqdm
) -> tuple[str, str, str, dict]:
    filepath = DATA_DIR / f"{data_type}_array_{size}.bin"
    alg_name = ALGORITHM_NAMES[alg]

    if not filepath.exists():
        progress.update(1)
        return data_type, str(size), alg_name, {"status": "missing"}

    try:
        hyp = await asyncio.wait_for(run_hyperfine(alg, filepath, core), timeout=timeout)
        prf = await asyncio.wait_for(run_perf(alg, filepath, core), timeout=timeout)
        result = {**hyp, **prf}
    except asyncio.TimeoutError:
        result = {"status": "timeout"}
    except Exception as e:
        result = {"status": "error", "message": str(e)}

    progress.update(1)
    return data_type, str(size), alg_name, result


async def worker(
    core: int, queue: asyncio.Queue, results: list, timeout: int, progress: tqdm
) -> None:
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        alg, data_type, size = item
        result = await benchmark_one(alg, data_type, size, core, timeout, progress)
        results.append(result)
        queue.task_done()


async def main(sizes: list[int], timeout: int = TIMEOUT_S, concurrency: int = MAX_CONCURRENT) -> None:
    work_items = [
        (alg, data_type, size)
        for size in sizes
        for data_type in DATA_TYPES
        for alg in ALGORITHMS
    ]

    total = len(work_items)
    print(f"\nSorting algorithm benchmark")
    print(f"  tasks      : {total}  ({len(sizes)} sizes x {len(DATA_TYPES)} types x {len(ALGORITHMS)} algorithms)")
    print(f"  workers    : {concurrency}  (cores 0-{concurrency - 1})")
    print(f"  timeout    : {timeout}s per task")
    print()

    queue: asyncio.Queue = asyncio.Queue()
    for item in work_items:
        await queue.put(item)
    for _ in range(concurrency):
        await queue.put(None)  # shutdown sentinel per worker

    results: list = []
    with tqdm(total=total, desc="Benchmarking", unit="task", ncols=80) as progress:
        workers = [
            asyncio.create_task(worker(core, queue, results, timeout, progress))
            for core in range(concurrency)
        ]
        await asyncio.gather(*workers)

    output: dict = {}
    errors: list[str] = []
    for data_type, size, alg_name, data in results:
        output.setdefault(data_type, {}).setdefault(size, {})[alg_name] = data
        if data.get("status") in ("error", "timeout"):
            errors.append(f"  {data_type}/{size}/{alg_name}: {data.get('status')} {data.get('message', '')}")

    with open(OUTPUT, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults written to {OUTPUT}")
    if errors:
        print(f"\nWarnings ({len(errors)}):")
        print("\n".join(errors))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaling benchmark for sorting algorithms.")
    parser.add_argument(
        "--sizes", type=int, nargs="+", default=SIZES,
        help="Array sizes to benchmark (default: all)"
    )
    parser.add_argument(
        "--timeout", type=int, default=TIMEOUT_S,
        help=f"Per-task timeout in seconds (default: {TIMEOUT_S})"
    )
    parser.add_argument(
        "--concurrency", type=int, default=MAX_CONCURRENT,
        help=f"Max concurrent benchmarks (default: {MAX_CONCURRENT})"
    )
    args = parser.parse_args()
    asyncio.run(main(args.sizes, args.timeout, args.concurrency))
