"""
Aggregate per-version JSON benchmark results into a Markdown table.

Usage:
    python benchmarks/report.py results/*.json

Writes a Markdown table to stdout, suitable for $GITHUB_STEP_SUMMARY.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: report.py results/*.json", file=sys.stderr)
        sys.exit(1)

    results = [load(p) for p in sys.argv[1:]]
    results.sort(key=lambda r: (r["python"], r["workers"]))

    # Group single vs threaded pairs for speedup calculation
    by_key: dict[tuple, dict] = {}
    for r in results:
        by_key[(r["python"], r["build"], r["workers"])] = r

    print("## Benchmark results\n")
    print(f"Input size: {results[0]['size']} numbers, language: `en`\n")
    print("| Python | Build | Mode | Time (ms) | vs single-thread |")
    print("|--------|-------|------|----------:|:----------------:|")

    for r in results:
        key_single = (r["python"], r["build"], 1)
        if r["workers"] == 1:
            speedup = "—"
        else:
            baseline = by_key.get(key_single)
            if baseline:
                ratio = baseline["ms"] / r["ms"]
                speedup = f"**{ratio:.2f}× faster**" if ratio >= 1.0 else f"{ratio:.2f}× (slower)"
            else:
                speedup = "n/a"

        mode = "single-thread" if r["workers"] == 1 else f"threaded (w={r['workers']})"
        print(f"| {r['python']} | {r['build']} | {mode} | {r['ms']:.1f} | {speedup} |")

    print()
    print("> Threaded benchmarks use `workers=4`. On GIL-enabled builds, threading adds overhead")
    print("> (shared interpreter lock serializes num2words calls). Free-threaded builds (3.13t+)")
    print("> achieve near-linear speedup.")


if __name__ == "__main__":
    main()
