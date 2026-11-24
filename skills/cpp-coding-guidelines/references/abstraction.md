---
id: cpp/abstraction
title: "Concrete Types and Templates"
summary: "Introduce abstraction only when actual variation requires it."
language: cpp
topic: abstraction
tags: [interfaces, generics, classes]
related: [cpp/data-and-functions]
snippets: unverified
---

# Concrete Types and Templates

## Summary

Introduce abstraction only when actual variation requires it. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this where providers actually differ at runtime or an algorithm genuinely supports multiple types. For data, functions, and parameters, see [Data, Functions, and Parameters](data-and-functions.md).

## Rules

- **MUST** favor concrete types; use Virtual Interfaces only for real runtime substitutability.
- **SHOULD** avoid deep inheritance, one-implementation interfaces, speculative factories, and empty manager/service wrappers.
- **MUST** use Templates only for genuinely generic code; prefer ordinary functions, standard utilities, and meaningful C++20 Concepts.

## Recommended Pattern

```cpp
// src/checkout.cpp
#include <cstdint>
#include <string>
#include <string_view>

class PaymentGateway {
public:
    virtual ~PaymentGateway() = default;
    virtual std::string charge(std::string_view order_id, std::int64_t amount_cents) = 0;
};

[[nodiscard]] std::string checkout(
    PaymentGateway& gateway, std::string_view order_id, std::int64_t amount_cents) {
    return gateway.charge(order_id, amount_cents);
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Virtual interface for one pure calculation | Adds unnecessary dispatch | Keep a concrete function |
| Speculative factory layers | More code paths without variation | Construct the concrete type directly |
| Unconstrained generic API | Accepts types with unclear contracts | Use a meaningful concept if genuine genericity remains |

## Checklist

- Confirm that runtime substitution is required.
- Keep the consumer contract minimal.
- Use ordinary functions where one concrete type suffices.
- Constrain genuine templates meaningfully.

## References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
