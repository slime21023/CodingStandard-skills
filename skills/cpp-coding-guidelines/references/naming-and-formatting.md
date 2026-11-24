---
id: cpp/naming-and-formatting
title: "Naming and Readability"
summary: "Use descriptive names and make control flow and side effects visible."
language: cpp
topic: naming-and-formatting
tags: [naming, formatting, control-flow]
related: [cpp/tooling]
snippets: unverified
---

# Naming and Readability

## Summary

Use descriptive names and make control flow and side effects visible. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when naming or simplifying new and touched code. For verification, see [Formatting, Analysis, and CI](tooling.md).

## Rules

- **MUST** use descriptive names, braces, and simple control flow; avoid nested ternaries, avoidable nesting, and hidden side effects.
- **SHOULD** use `const`, `enum class`, `nullptr`, `explicit`, and `[[nodiscard]]`; limit C casts, macros, and opaque `auto`.
- **MUST** use `PascalCase` types, `snake_case` functions/variables/namespaces, `snake_case_` private members, `kPascalCase` constants, `UPPER_SNAKE_CASE` macros.
- **SHOULD** comment why, invariants, ownership, and tradeoffs; avoid describing obvious code.

Note: The returned pointer borrows from `products`; neither it nor the string views may outlive their backing data.

## Recommended Pattern

```cpp
// src/catalog.cpp
#include <cstddef>
#include <cstdint>
#include <span>
#include <string_view>

namespace catalog {
constexpr std::size_t kMaxSearchResults = 50;

struct Product {
    std::string_view product_id;
    std::string_view name;
    std::int64_t price_cents;
};

[[nodiscard]] const Product* find_product_by_id(
    std::span<const Product> products, std::string_view product_id) {
    for (const Product& product : products) {
        if (product.product_id == product_id) {
            return &product;
        }
    }
    return nullptr;
}
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Variable named tmp | Hides its purpose | Name the domain role |
| Nested ternary | Hard to trace | Use braces and guards |
| C-style cast | Hides the intended conversion | Use an appropriate C++ cast only when needed |

## Checklist

- Use the prescribed casing for all identifiers.
- Use braces and readable guard clauses.
- Make side effects obvious.
- Document constraints rather than obvious statements.

## References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
