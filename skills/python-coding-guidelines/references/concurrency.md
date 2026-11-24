---
id: python/concurrency
title: "Async and Concurrency"
summary: "Use structured concurrency only where concurrent I/O helps."
language: python
topic: concurrency
tags: [async, concurrency, cancellation]
related: [python/errors]
snippets: unverified
---

# Async and Concurrency

## Summary

Use structured concurrency only where concurrent I/O helps. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for a finite batch of concurrent I/O; keep ordinary calculations synchronous. For result and error boundaries, see [Result and Error Boundaries](errors.md).

## Rules

- **SHOULD** Follow Sync by Default; use `asyncio` when non-blocking I/O benefits the program.
- **SHOULD** Use `asyncio.TaskGroup` for related tasks; define timeouts, concurrency limits, and cleanup explicitly.
- **MUST** Do not block an event loop with synchronous I/O or CPU-heavy work; use suitable thread/process strategies where needed.
- **SHOULD** Keep event loop, task, executor, and resource lifecycles under application control.
- **SHOULD** Propagate task cancellation; use `try/finally` for reliable cleanup.
- **AVOID** Avoid untracked background tasks and unnecessary conversion of synchronous call chains to async.

Note: This bounds active requests, not the number of queued tasks. Use a bounded producer and worker queue for large or streaming input.

## Recommended Pattern

```python
# src/shop/catalog/prices.py
import asyncio
from collections.abc import Awaitable, Callable, Sequence


async def fetch_prices(
    product_ids: Sequence[str], fetch: Callable[[str], Awaitable[int]]
) -> list[int]:
    slots = asyncio.Semaphore(4)

    async def fetch_one(product_id: str) -> int:
        async with slots:
            return await fetch(product_id)

    async with asyncio.timeout(5):
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(fetch_one(product_id)) for product_id in product_ids]
    return [task.result() for task in tasks]
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Detached tasks | Failures or shutdown can be lost | Use an owning task group |
| Unlimited I/O | Overloads the dependency | Bound concurrent requests |
| Blocking disk call in async function | Stalls the loop | Use a suitable executor or stay synchronous |

## Checklist

- Give each task a supervisor.
- Bound requests and set a timeout.
- Preserve cancellation and release resources.
- Keep event loop setup at the application boundary.

## References

- [asyncio tasks](https://docs.python.org/3/library/asyncio-task.html)
