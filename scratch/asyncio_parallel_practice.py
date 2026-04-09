"""Simple asyncio practice: sequential vs parallel task execution.

Run:
    .venv/bin/python scratch/asyncio_parallel_practice.py

Try editing:
- The delay values in `delays`
- The task names
- `run_parallel` to use `asyncio.create_task`
"""

from __future__ import annotations

import asyncio
import time


async def fake_work(name: str, delay: float) -> str:
    """Pretend to do I/O work by waiting for `delay` seconds."""
    print(f"[{name}] starting ({delay}s)")
    await asyncio.sleep(delay)
    print(f"[{name}] finished")
    return f"{name} done"


async def run_sequential(delays: list[float]) -> list[str]:
    results: list[str] = []
    for index, delay in enumerate(delays, start=1):
        result = await fake_work(f"task-{index}", delay)
        results.append(result)
    return results


async def run_parallel(delays: list[float]) -> list[str]:
    coroutines = [fake_work(f"task-{index}", delay) for index, delay in enumerate(delays, start=1)]
    return await asyncio.gather(*coroutines)


async def main() -> None:
    delays = [1.0, 1.5, 2.0]

    print("\n--- Sequential ---")
    start = time.perf_counter()
    seq_results = await run_sequential(delays)
    seq_elapsed = time.perf_counter() - start
    print(f"results: {seq_results}")
    print(f"time: {seq_elapsed:.2f}s")

    print("\n--- Parallel (gather) ---")
    start = time.perf_counter()
    par_results = await run_parallel(delays)
    par_elapsed = time.perf_counter() - start
    print(f"results: {par_results}")
    print(f"time: {par_elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
