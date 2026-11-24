---
id: typescript/concurrency
title: "Async and Side Effects"
summary: "Await, return, or explicitly handle every Promise."
language: typescript
topic: concurrency
tags: [async, concurrency, cancellation]
related: [typescript/errors]
snippets: unverified
---

# Async and Side Effects

## Summary

Await, return, or explicitly handle every Promise. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for remote work or asynchronous orchestration. For error semantics, see [Error Semantics](errors.md).

## Rules

- **MUST** every Promise must be awaited, returned, or have its error handling explicitly arranged; it must never be dropped by accident.
- **MUST** do not ignore exceptions without cause, and do not use empty `catch` blocks without a reason.
- **SHOULD** use `async` / `await` for multi-step async flows; async operations expected to fail may return `Promise<Result<T, E>>`.
- **SHOULD** avoid mutating input data in data transformations; keep side effects such as I/O, time, and randomness identifiable.
- **AVOID** hiding network requests, global state mutation, or storage writes inside pure data-transformation functions.

Note: Each fetch must honor the signal for cancellation to interrupt its work.

## Recommended Pattern

Uses the shared Result contract from [Error Semantics](errors.md#recommended-pattern). Set an explicit batch size and pass a caller-owned signal.

```typescript
// src/catalog/prices.ts
import type { Result } from "./discount.js";

type PriceError = { code: "UNAVAILABLE" };

export async function fetchPrices(
  ids: readonly string[],
  signal: AbortSignal,
  fetchPrice: (id: string, signal: AbortSignal) => Promise<Result<number, PriceError>>,
): Promise<Result<number[], PriceError>> {
  const prices: number[] = [];
  const limit = 4;
  for (let offset = 0; offset < ids.length; offset += limit) {
    signal.throwIfAborted();
    const batch = ids.slice(offset, offset + limit);
    const results = await Promise.allSettled(batch.map(async (id) => fetchPrice(id, signal)));
    for (const result of results) {
      if (result.status === "rejected") throw result.reason;
    }
    for (const result of results) {
      if (result.status === "fulfilled") {
        if (!result.value.ok) return result.value;
        prices.push(result.value.value);
      }
    }
  }
  signal.throwIfAborted();
  return { ok: true, value: prices };
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Dropped Promise | Lose asynchronous errors | Await or return it |
| Unbounded fan-out | Overloads the service | Use finite batches or limited workers |
| Hidden network call | Misleads callers about effects | Express I/O in the name and contract |

## Checklist

- Bound in-flight work.
- Propagate unexpected rejections.
- Give I/O the caller-owned cancellation signal.
- Document the expected failure contract.

## References

- [Promise.allSettled](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled)
- [AbortSignal](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)
