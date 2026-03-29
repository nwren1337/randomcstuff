import asyncio
import json
import argparse
import tempfile
import os
import shutil
import signal
import time
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, BarColumn, MofNCompleteColumn, TimeElapsedColumn
from rich.console import Group
from rich import box

BINARY: str = "./build/srt_driver"
DATA_DIR: Path = Path("data")
OUTPUT_DIR: str = "testdata"

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
            start_new_session=True,
        )
        try:
            _, stderr = await proc.communicate()
        except asyncio.CancelledError:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
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
        start_new_session=True,
    )
    try:
        _, stderr = await proc.communicate()
    except asyncio.CancelledError:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
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
    alg: str, data_type: str, size: int, core: int, timeout: int | None
) -> dict:
    filepath = DATA_DIR / f"{data_type}_array_{size}.bin"

    if not filepath.exists():
        return {"status": "missing"}

    try:
        hyp = await asyncio.wait_for(run_hyperfine(alg, filepath, core), timeout=timeout)
        prf = await asyncio.wait_for(run_perf(alg, filepath, core), timeout=timeout)
        return {**hyp, **prf}
    except asyncio.TimeoutError:
        return {"status": "timeout"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def viewport_start(task_states: list[dict], window: int) -> int:
    first_active = next(
        (i for i, s in enumerate(task_states) if s["status"] != "done"), len(task_states)
    )
    start = max(0, first_active - window // 3)
    return min(start, max(0, len(task_states) - window))


def make_display(task_states: list[dict], progress: Progress, window: int) -> Group:
    table = Table(box=box.SIMPLE, show_header=False, expand=True, padding=(0, 1))
    table.add_column("Task", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Time", justify="right", width=8)

    start = viewport_start(task_states, window)
    visible = task_states[start : start + window]

    if start > 0:
        table.add_row(f"[dim]... {start} tasks above ...[/dim]", "", "")

    for state in visible:
        match state["status"]:
            case "waiting":
                table.add_row(state["label"], "[dim]waiting[/dim]", "")
            case "running":
                elapsed = time.monotonic() - state["start"]
                table.add_row(state["label"], "[yellow]⟳ running[/yellow]", f"{elapsed:.0f}s")
            case "done":
                table.add_row(state["label"], "[green]✓[/green]", f"{state['elapsed']:.1f}s")
            case "timeout":
                table.add_row(state["label"], "[red]timeout[/red]", f"{state['elapsed']:.0f}s")
            case "error":
                table.add_row(state["label"], "[red]✗ error[/red]", "")
            case "missing":
                table.add_row(state["label"], "[dim]missing[/dim]", "")
            case "cancelled":
                table.add_row(state["label"], "[dim]cancelled[/dim]", "")

    return Group(table, progress)


async def worker(
    core: int,
    queue: asyncio.Queue,
    results: list,
    timeout: int,
    task_states: list[dict],
    rich_progress: Progress,
    progress_task: int,
) -> None:
    current_idx: int | None = None
    try:
        while True:
            item = await queue.get()
            if item is None:
                queue.task_done()
                break
            current_idx = item[0]
            idx, alg, data_type, size = item
            task_states[idx]["status"] = "running"
            task_states[idx]["start"] = time.monotonic()

            result = await benchmark_one(alg, data_type, size, core, timeout)

            elapsed = time.monotonic() - task_states[idx]["start"]
            task_states[idx]["elapsed"] = elapsed
            task_states[idx]["status"] = result.get("status", "done")
            results.append((data_type, str(size), ALGORITHM_NAMES[alg], result))
            rich_progress.advance(progress_task)
            queue.task_done()
    except asyncio.CancelledError:
        if current_idx is not None and task_states[current_idx]["status"] == "running":
            task_states[current_idx]["elapsed"] = time.monotonic() - task_states[current_idx]["start"]
            task_states[current_idx]["status"] = "cancelled"
        raise


async def main(sizes: list[int], data_types: list[str] = DATA_TYPES, algorithms: list[str] = ALGORITHMS, timeout: int | None = TIMEOUT_S, concurrency: int = MAX_CONCURRENT) -> None:
    work_items = [
        (alg, data_type, size)
        for size in sizes
        for data_type in data_types
        for alg in algorithms
    ]

    total = len(work_items)
    task_states: list[dict] = [
        {
            "label": f"{data_type}/{size}/{ALGORITHM_NAMES[alg]}",
            "status": "waiting",
            "start": 0.0,
            "elapsed": 0.0,
        }
        for alg, data_type, size in work_items
    ]

    console = Console()
    console.print(f"\nSorting algorithm benchmark")
    console.print(f"  tasks      : {total}  ({len(sizes)} sizes x {len(data_types)} types x {len(algorithms)} algorithms)")
    console.print(f"  workers    : {concurrency}  (cores 0-{concurrency - 1})")
    console.print(f"  timeout    : {f'{timeout}s' if timeout is not None else 'none'} per task")
    console.print()

    window = min(20, max(4, (shutil.get_terminal_size().lines or 40) - 10))

    progress = Progress(BarColumn(), MofNCompleteColumn(), TimeElapsedColumn(), console=console)
    progress_task = progress.add_task("", total=total)

    queue: asyncio.Queue = asyncio.Queue()
    results: list = []
    worker_tasks: list = []
    shutdown = asyncio.Event()
    loop = asyncio.get_running_loop()

    def _handle_sigint() -> None:
        if not shutdown.is_set():
            shutdown.set()
            for t in worker_tasks:
                t.cancel()

    loop.add_signal_handler(signal.SIGINT, _handle_sigint)

    try:
        with Live(make_display(task_states, progress, window), refresh_per_second=4, console=console, transient=True) as live:
            stop = asyncio.Event()

            async def updater() -> None:
                while not stop.is_set():
                    live.update(make_display(task_states, progress, window))
                    await asyncio.sleep(0.25)

            updater_task = asyncio.create_task(updater())

            for i, item in enumerate(work_items):
                await queue.put((i, *item))
            for _ in range(concurrency):
                await queue.put(None)

            worker_tasks[:] = [
                asyncio.create_task(
                    worker(core, queue, results, timeout, task_states, progress, progress_task)
                )
                for core in range(concurrency)
            ]
            await asyncio.gather(*worker_tasks, return_exceptions=True)

            for state in task_states:
                if state["status"] in ("waiting", "running"):
                    state["status"] = "cancelled"

            # fill in any tasks that never recorded a result (cancelled, waiting, etc.)
            recorded = {(dt, sz, alg) for dt, sz, alg, _ in results}
            for i, (alg, data_type, size) in enumerate(work_items):
                key = (data_type, str(size), ALGORITHM_NAMES[alg])
                if key not in recorded:
                    results.append((data_type, str(size), ALGORITHM_NAMES[alg], {"status": task_states[i]["status"]}))

            stop.set()
            await updater_task
    finally:
        loop.remove_signal_handler(signal.SIGINT)

    if shutdown.is_set():
        console.print("\n[yellow]Interrupted — partial results saved.[/yellow]")

    output: dict = {}
    errors: list[str] = []
    for data_type, size, alg_name, data in results:
        output.setdefault(data_type, {}).setdefault(size, {})[alg_name] = data
        if data.get("status") in ("error", "timeout", "cancelled"):
            errors.append(f"  {data_type}/{size}/{alg_name}: {data.get('status')} {data.get('message', '')}")

    epoch = int(time.time())
    output_path = f"{OUTPUT_DIR}/results-{epoch}.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    console.print(f"\nResults written to {output_path}")
    if errors:
        console.print(f"\nWarnings ({len(errors)}):")
        console.print("\n".join(errors))


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
    parser.add_argument(
        "--types", nargs="+", choices=DATA_TYPES, default=DATA_TYPES,
        help=f"Input data types to benchmark (default: all)"
    )
    parser.add_argument(
        "--algorithms", nargs="+", choices=list(ALGORITHM_NAMES.values()), default=list(ALGORITHM_NAMES.values()),
        help="Algorithms to benchmark (default: all)"
    )
    parser.add_argument(
        "--no-timeout", action="store_true",
        help="Disable per-task timeout and let each task run until completion"
    )
    args = parser.parse_args()
    alg_keys = [k for k, v in ALGORITHM_NAMES.items() if v in args.algorithms]
    timeout = None if args.no_timeout else args.timeout
    asyncio.run(main(args.sizes, args.types, alg_keys, timeout, args.concurrency))
