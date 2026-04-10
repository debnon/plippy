from __future__ import annotations

import asyncio
import random


# ---------------------------------------------------------------------------
# Simulated flaky operation
# ---------------------------------------------------------------------------

async def flaky_fetch(item_id: int) -> str:
    """Pretend to fetch something. Fails randomly on early attempts."""
    await asyncio.sleep(0.05)  # simulate I/O latency
    if random.random() < 0.6:  # 60% chance of transient failure
        raise ConnectionError(f"Transient error for item {item_id}")
    return f"result_for_{item_id}"


# ---------------------------------------------------------------------------
# Retry wrapper
# ---------------------------------------------------------------------------

async def with_retry(
    coro_factory,
    retries: int = 4,
    base_delay: float = 0.1,
) -> dict:
    for attempt in range(1, retries + 1):
        try:
            data = await coro_factory()
            return {"ok": True, "data": data, "attempt": attempt}

        except ConnectionError as e:
            # Retryable: transient network / I/O issue
            if attempt == retries:
                return {"ok": False, "error": str(e), "attempt": attempt}

            delay = base_delay * (2 ** (attempt - 1))
            jitter = delay * random.uniform(-0.2, 0.2)
            wait = delay + jitter
            print(f"  [retry] attempt {attempt} failed — waiting {wait:.2f}s before retry")
            await asyncio.sleep(wait)

        except Exception as e:
            # Non-retryable: don't bother retrying
            return {"ok": False, "error": f"[non-retryable] {e}", "attempt": attempt}


# ---------------------------------------------------------------------------
# Run multiple items in parallel, each with its own inline retry
# ---------------------------------------------------------------------------

async def main() -> None:
    random.seed(42)  # remove this line to see different random failures each run
    item_ids = [1, 2, 3, 4, 5]

    tasks = [
        asyncio.create_task(
            with_retry(lambda i=item_id: flaky_fetch(i), retries=4, base_delay=0.1)
        )
        for item_id in item_ids
    ]

    print("Processing items with inline retry...\n")

    successes = []
    failures = []

    for finished in asyncio.as_completed(tasks):
        result = await finished
        if result["ok"]:
            print(f"  OK after {result['attempt']} attempt(s): {result['data']}")
            successes.append(result)
        else:
            print(f"  FAILED after {result['attempt']} attempt(s): {result['error']}")
            failures.append(result)

    print(f"\nDone. {len(successes)} succeeded, {len(failures)} failed.")


if __name__ == "__main__":
    asyncio.run(main())
