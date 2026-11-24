---
id: cpp/data-and-functions
title: "Data, Functions, and Parameters"
summary: "Prefer structs for independent data and free functions for transformations."
language: cpp
topic: data-and-functions
tags: [data, functions, public-api]
related: [cpp/resources-and-memory]
snippets: unverified
---

# Data, Functions, and Parameters

## Summary

Prefer structs for independent data and free functions for transformations. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for domain data, calculations, and parameter choices. For ownership and lifetime, see [Ownership and Lifetime](resources-and-memory.md).

## Rules

- **MUST** prefer `struct` for independent data and Free Functions for algorithms and transformations.
- **MUST** use `class` for invariants, state protection, or resource lifetime encapsulation.
- **MUST** keep functions cohesive, side effects visible, and control flow simple; prefer Guard Clauses to nesting.
- **SHOULD** pass small cheap values by value, large read-only inputs by `const T&`, mutating inputs by `T&`, nullable non-owning objects by `T*`.

## Recommended Pattern

```cpp
// src/order_totals.cpp
#include <cstdint>
#include <span>
#include <string_view>

struct OrderLine {
    std::string_view product_id;
    std::int64_t quantity;
    std::int64_t unit_price_cents;
};

// The caller validates quantities and ensures products and sum fit in int64_t.
[[nodiscard]] std::int64_t order_total_cents(std::span<const OrderLine> lines) {
    std::int64_t total = 0;
    for (const OrderLine& line : lines) {
        total += line.quantity * line.unit_price_cents;
    }
    return total;
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| State-free calculation behind a class | Adds artificial ownership | Use a free function |
| Heavy immutable argument copied | Does unnecessary work | Pass by const reference or use a view |
| Boolean mode toggles unrelated behavior | Obscures effects | Split cohesive operations |

## Checklist

- Check whether a class protects an invariant or resource.
- Use a cheap value or borrowing contract deliberately.
- Keep calculations focused.
- Document value ranges that affect correctness.

## References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
