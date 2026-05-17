"""Tiny in-process profiler for rectification options.

Accumulates `{class_name: (count, total_seconds)}` keyed by option class, then
prints a sorted summary so the slow options become obvious.
"""
from __future__ import annotations

import time
from contextlib import contextmanager

_timings: dict[str, dict[str, float]] = {}


def reset() -> None:
    _timings.clear()


def record(label: str, seconds: float) -> None:
    entry = _timings.setdefault(label, {"count": 0, "total": 0.0})
    entry["count"] += 1
    entry["total"] += seconds


@contextmanager
def measure(label: str):
    t0 = time.perf_counter()
    try:
        yield
    finally:
        record(label, time.perf_counter() - t0)


def summary() -> list[tuple[str, int, float]]:
    """Return [(label, count, total_seconds)] sorted by total desc."""
    return sorted(
        ((label, e["count"], e["total"]) for label, e in _timings.items()),
        key=lambda row: row[2],
        reverse=True,
    )


def format_summary() -> str:
    rows = summary()
    if not rows:
        return ""
    width = max(len(r[0]) for r in rows)
    lines = ["[profile] option timings (top down):"]
    for label, count, total in rows:
        lines.append(f"  {label:<{width}}  {count:>5}× {total:>7.2f}s")
    return "\n".join(lines)
