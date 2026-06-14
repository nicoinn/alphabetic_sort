"""
Benchmark: number-to-word conversion with and without multithreading.

Usage:
    python benchmarks/bench.py [--workers N] [--size N] [--json PATH]

Outputs a Markdown summary to stdout and optionally a JSON result file.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# Ensure the repo root is on the path when run directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from alphabetic_sort import alphabetic_sort


def _bench(numbers: list, lang: str, workers: int, runs: int = 5) -> float:
    """Return median elapsed seconds over `runs` repetitions."""
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        alphabetic_sort(numbers, lang=lang, workers=workers)
        times.append(time.perf_counter() - t0)
    times.sort()
    return times[len(times) // 2]


def main() -> None:
    parser = argparse.ArgumentParser(description="alphabetic_sort benchmark")
    parser.add_argument("--workers", type=int, default=1, help="Thread-pool size (1 = no threading)")
    parser.add_argument("--size", type=int, default=500, help="Number of integers to sort")
    parser.add_argument("--runs", type=int, default=7, help="Repetitions per measurement")
    parser.add_argument("--json", type=str, default=None, help="Write JSON result to this path")
    args = parser.parse_args()

    numbers = list(range(-args.size // 2, args.size // 2))
    lang = "en"

    elapsed = _bench(numbers, lang, workers=args.workers, runs=args.runs)
    ms = elapsed * 1000

    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
    # Detect free-threaded builds (no GIL)
    gil = getattr(sys, "_is_gil_enabled", lambda: True)()
    build_tag = "free-threaded" if not gil else "standard"

    label = "threading" if args.workers > 1 else "single-thread"
    print(f"Python {py_ver} ({build_tag}) | {label} (workers={args.workers}) | "
          f"{args.size} numbers | {ms:.1f} ms")

    if args.json:
        result = {
            "python": py_ver,
            "build": build_tag,
            "workers": args.workers,
            "size": args.size,
            "ms": round(ms, 2),
        }
        Path(args.json).write_text(json.dumps(result))


if __name__ == "__main__":
    main()
