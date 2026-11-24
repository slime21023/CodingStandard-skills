---
id: cpp/errors
title: "Expected and Exceptions"
summary: "Return typed Expected values for recoverable operations in C++20."
language: cpp
topic: errors
tags: [errors, result, exceptions]
related: [cpp/data-and-functions]
snippets: unverified
---

# Expected and Exceptions

## Summary

Return typed Expected values for recoverable operations in C++20. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for validation, parsing, and recoverable I/O failures. For data, functions, and parameters, see [Data, Functions, and Parameters](data-and-functions.md).

## Rules

- **MUST** return explicit results for expected recoverable parsing, validation, I/O, and network failure; do not use Exceptions for normal branching.
- **MUST** use a reviewed, pinned third-party Expected implementation in C++20, such as `tl::expected`, rather than build a new generic Result framework.
- **SHOULD** maintain consistent Result naming; test public Module aliases and do not assume effortless migration to `std::expected`.
- **MUST** represent useful error causes with `enum class` or structured types, not opaque `bool` or silently empty values.
- **MUST** check Expected success before accessing value/error; preserve contextual errors. Use `std::optional` only when absence is not failure.
- **MUST** reserve Exceptions for exceptional failures, impossible constructors, or existing library contracts; catch at meaningful boundaries and never swallow silently.
- **MUST** not let destructor exceptions escape; use `noexcept` only when warranted. Handle programmer errors as defects, not pretend-recoverable results.

Note: Use `std::optional` only for normal absence. A constructor that cannot establish its invariant can throw or use a fallible Expected factory according to its contract. Fix programmer defects rather than returning fake recoverable failures. For public Result aliases, verify a real importing consumer and do not promise transparent migration to `std::expected`.

## Dependencies

Use a vetted, version-pinned [`tl::expected`](https://github.com/TartanLlama/expected) implementation as the initial candidate. Before adding it, review version, license, compiler support, public reachability, module integration, and project dependency policy.

## Recommended Pattern

```cpp
// src/discount.hpp
#pragma once
#include <cstdint>
#include <tl/expected.hpp>

struct Product {
    std::int64_t price_cents;
};

enum class DiscountError {
    NegativeAmount,
    ExceedsPrice,
};

[[nodiscard]] inline tl::expected<Product, DiscountError>
apply_discount(Product product, std::int64_t amount_cents) {
    if (amount_cents < 0) {
        return tl::unexpected(DiscountError::NegativeAmount);
    }
    if (amount_cents > product.price_cents) {
        return tl::unexpected(DiscountError::ExceedsPrice);
    }
    product.price_cents -= amount_cents;
    return product;
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| std::expected with C++20 | Requires a later standard | Use the reviewed pinned Expected dependency |
| std::optional for validation failure | Loses the cause | Return typed Expected |
| Exception for common branching | Makes the expected contract implicit | Return a recoverable result |

## Checklist

- Keep expected failures inspectable.
- Check success before accessing an Expected value.
- Preserve meaningful context.
- Handle exceptions at meaningful boundaries.

## References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [tl::expected](https://github.com/TartanLlama/expected)
- [WG21 std::expected](https://www.open-std.org/jtc1/sc22/WG21/docs/papers/2022/p0323r12.html)
