---
id: cpp/concurrency
title: "Concurrency and Performance"
summary: "Own thread lifetimes and protect shared state explicitly."
language: cpp
topic: concurrency
tags: [concurrency, resources]
related: [cpp/resources-and-memory]
snippets: unverified
---

# Concurrency and Performance

## Summary

Own thread lifetimes and protect shared state explicitly. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for explicitly owned workers and shared data. For ownership and lifetime, see [Ownership and Lifetime](resources-and-memory.md).

## Rules

- **MUST** manage thread lifetimes and shared mutable data; `volatile` is not synchronization. Prefer `std::jthread` for basic thread ownership.
- **MUST** validate algorithmic correctness and profile before nontrivial micro-optimizations.
- **SHOULD** Validate thread lifetime and synchronization before introducing pools or lock-free techniques.

Note: This drains currently available work with one bounded worker. The caller owns the stop source; stopping prevents further pops, not an already dequeued callback.

## Recommended Pattern

```cpp
// src/order_queue.cpp
#include <deque>
#include <mutex>
#include <stop_token>
#include <thread>

void drain_orders(std::deque<int>& pending, std::mutex& mutex,
                  void (*process)(int) noexcept, std::stop_token stop) {
    for (;;) {
        int order_id;
        {
            std::lock_guard lock(mutex);
            if (stop.stop_requested() || pending.empty()) {
                return;
            }
            order_id = pending.front();
            pending.pop_front();
        }
        process(order_id);
    }
}

void process_queue(std::deque<int>& pending, std::mutex& mutex,
                   void (*process)(int) noexcept, std::stop_token stop) {
    std::jthread worker([&] { drain_orders(pending, mutex, process, stop); });
    worker.join();
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| volatile used as lock | Does not synchronize shared memory | Use a mutex or atomics |
| Callback while holding queue lock | Can deadlock or serialize work | Release the lock before processing |
| Detached worker borrowing locals | References can dangle | Join before values go out of scope |

## Checklist

- Give each worker an owner and completion path.
- Protect queue access with the same mutex.
- Define cooperative stop behavior.
- Profile before complicating synchronization.

## References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
