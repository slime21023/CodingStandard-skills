---
id: rust/concurrency
title: "Async and Concurrency"
summary: "Choose the simplest execution model that meets concurrency needs."
language: rust
topic: concurrency
tags: [concurrency, async, cancellation]
related: [rust/testing]
snippets: unverified
---

# Async and Concurrency

## Summary

Choose the simplest execution model that meets concurrency needs. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for background work or bounded synchronous batches. For testing, see [Testing](testing.md).

## Rules

- **SHOULD** Stay synchronous by default; use async for substantial concurrent I/O and an appropriate parallel strategy for CPU work.
- **SHOULD** Let the application own its runtime; keep library cores independent when practical.
- **MUST** Give every task completion, cancellation, error, timeout, shutdown, and cleanup policies; do not permit unbounded unmanaged tasks.
- **SHOULD** Bound work with queues, semaphores, or equivalent backpressure. Prefer transferring data or sending messages to shared mutable state.
- **MUST** Do not hold synchronous mutex guards across await or block an executor for prolonged synchronous work; use suitable blocking workers instead.

Note: Inputs are validated so partial sums fit in `i64`. The atomic flag is only a stop signal; it does not publish other data.

## Recommended Pattern

```rust
// src/orders/batch.rs
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;

/// Sum at most one chunk per worker. Return None if cancelled.
pub fn batch_total(lines: &[i64], cancelled: &AtomicBool) -> Option<i64> {
    let chunk_size = lines.len().div_ceil(4).max(1);
    thread::scope(|scope| {
        let workers: Vec<_> = lines.chunks(chunk_size).map(|chunk| {
            scope.spawn(move || {
                let mut subtotal = 0;
                for value in chunk {
                    if cancelled.load(Ordering::Relaxed) {
                        return None;
                    }
                    subtotal += value;
                }
                Some(subtotal)
            })
        }).collect();
        let mut total = Some(0);
        for worker in workers {
            let subtotal = worker.join().unwrap_or_else(|panic| std::panic::resume_unwind(panic));
            total = total.zip(subtotal).map(|(left, right)| left + right);
        }
        total.filter(|_| !cancelled.load(Ordering::Relaxed))
    })
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Runtime created inside library | Competes with app lifecycle | Leave runtime to caller |
| Mutex held across await | Can deadlock or stall other tasks | End the lock scope before awaiting |
| Unlimited spawned work | Removes backpressure | Bound concurrent work and queued jobs |

## Checklist

- Check whether synchronous code suffices.
- Bound the number of workers.
- Join workers on cancellation.
- Keep blocking work off the async executor.

## References

- [Scoped threads](https://doc.rust-lang.org/std/thread/fn.scope.html)
- [Rust Book](https://doc.rust-lang.org/book/)
