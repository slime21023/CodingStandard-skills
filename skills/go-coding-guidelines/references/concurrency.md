---
id: go/concurrency
title: "Context, Concurrency, and Resources"
summary: "Give concurrent work a clear owner, bound, and completion strategy."
language: go
topic: concurrency
tags: [concurrency, cancellation, resources]
related: [go/testing]
snippets: unverified
---

# Context, Concurrency, and Resources

## Summary

Give concurrent work a clear owner, bound, and completion strategy. Cancellation is cooperative and does not replace joining workers.

## When to Use

Use this for request I/O, background work, and owned resources. For testing, see [Testing](testing.md).

## Rules

- **MUST** Give each goroutine an owner, a termination strategy, cancellation or joining, and synchronize shared mutable data.
- **SHOULD** Pass request-scoped context.Context as the first I/O parameter; do not routinely store it in structs.
- **SHOULD** Bound concurrent work and resources; use channels for communication and mutexes for direct shared-state protection as appropriate.
- **SHOULD** Release files and response bodies promptly; handle Close and flush failures when relevant.
- **AVOID** Avoid speculative goroutines, channels, pools, and optimization.

## Recommended Pattern

```go
// catalog/prices.go
package catalog

import (
    "context"
    "sync"
)

type PriceResult struct { Cents int64; Err error }

// FetchPrices returns one result per ID. fetch must honor cancellation.
func FetchPrices(ctx context.Context, ids []string, fetch func(context.Context, string) (int64, error)) []PriceResult {
    const limit = 4
    results := make([]PriceResult, len(ids))
    slots := make(chan struct{}, limit)
    var workers sync.WaitGroup
    for index, id := range ids {
        select {
        case slots <- struct{}{}:
            workers.Add(1)
            go func(index int, id string) {
                defer workers.Done()
                defer func() { <-slots }()
                cents, err := fetch(ctx, id)
                results[index] = PriceResult{Cents: cents, Err: err}
            }(index, id)
        case <-ctx.Done():
            for remaining := index; remaining < len(ids); remaining++ {
                results[remaining].Err = ctx.Err()
            }
            workers.Wait()
            return results
        }
    }
    workers.Wait()
    return results
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Unlimited fan-out | Exhausts capacity | Gate goroutine creation |
| Write to shared map | Races between workers | Use disjoint slots or synchronization |
| Discard Close error | Can miss a failed flush | Check it when it affects correctness |

## Checklist

- Bound work before launching goroutines.
- Make the callback obey the context.
- Join workers on normal and cancellation paths.
- Use disjoint result slots or protect shared state.

## References

- [Package context](https://pkg.go.dev/context)
- [Go race detector](https://go.dev/doc/articles/race_detector)
