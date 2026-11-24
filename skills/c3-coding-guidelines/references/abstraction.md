---
id: c3/abstraction
title: "Generics, Interfaces, and Macros"
summary: "Add abstraction only to solve an actual reuse or dispatch problem."
language: c3
topic: abstraction
tags: [interfaces, generics, metaprogramming]
related: [c3/modules-and-api]
snippets: unverified
---

# Generics, Interfaces, and Macros

## Summary

Add abstraction only to solve an actual reuse or dispatch problem. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when checkout has genuinely interchangeable payment providers. For modules and public apis, see [Modules and Public APIs](modules-and-api.md).

## Rules

- **SHOULD** Use concrete types and ordinary functions first.
- **SHOULD** Introduce generics when actual cross-type reuse justifies them.
- **SHOULD** Use interfaces only when runtime polymorphism is necessary.
- **SHOULD** Use macros and compile-time reflection only when ordinary functions or generics are insufficient.
- **AVOID** Avoid speculative abstractions, macro-heavy control flow, and abstraction for a single implementation without a concrete need.

## Recommended Pattern

```c3
// src/checkout.c3
module shop::billing @private;

alias Charge = fn String?(String order_id, long amount_cents);

<* @return "The payment provider receipt, or the provider fault." *>
fn String? checkout(Charge charge, String order_id, long amount_cents) @public
{
	return charge(order_id, amount_cents);
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Macro wraps a simple call | Adds compile-time complexity | Use an ordinary function |
| Interface for only a concrete provider | Imposes a speculative boundary | Keep the concrete provider until substitution is real |
| Generic type without shared behavior | Hides the design | Use the concrete type |

## Checklist

- Start with ordinary functions.
- Identify actual reuse before adding generics.
- Use runtime dispatch only for real variation.
- Prefer macros only for work normal calls cannot express.

## References

- [C3 language reference](https://c3-lang.org/all/)
