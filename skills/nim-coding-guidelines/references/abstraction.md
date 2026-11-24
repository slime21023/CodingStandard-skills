---
id: nim/abstraction
title: "Abstraction, Memory, and Performance"
summary: "Choose the least powerful mechanism and preserve Nim runtime checks."
language: nim
topic: abstraction
tags: [interfaces, generics, metaprogramming, memory]
related: [nim/data-and-functions]
snippets: unverified
---

# Abstraction, Memory, and Performance

## Summary

Choose the least powerful mechanism and preserve Nim runtime checks. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when actual providers or type relationships justify generalizing. For data, procedures, and control flow, see [Data, Procedures, and Control Flow](data-and-functions.md).

## Rules

- **SHOULD** Target **Nim 2.2 or newer** and the default **ORC** memory manager. Do not change memory management or disable runtime safety checks without measured, justified need.
- **SHOULD** Choose the least powerful mechanism that solves the problem: `func`/`proc`, then necessary generics, then `template`, then `macro`.
- **SHOULD** Introduce macros, converters, DSLs, raw pointers, custom allocators, or unsafe pragmas only with a concrete use case and documented tradeoffs.
- **SHOULD** Profile before optimizing; retain safety checks, regression tests, and readable code.

## Recommended Pattern

```nim
# src/shop/billing/checkout.nim
proc checkout*[Gateway](gateway: Gateway; orderId: string; amountCents: int64): string =
  ## Return the provider receipt for this order.
  mixin charge
  result = gateway.charge(orderId, amountCents)

type LedgerGateway* = object
  prefix*: string

proc charge*(gateway: LedgerGateway; orderId: string; amountCents: int64): string =
  ## Record a positive charge in the caller's ledger namespace.
  if amountCents <= 0:
    raise newException(ValueError, "charge must be positive")
  result = gateway.prefix & ":" & orderId & ":" & $amountCents
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Macro for ordinary dispatch | Hides normal control flow | Use a proc or a necessary generic |
| Identity wrapper for a value | Adds lifecycle complexity | Keep the value object |
| Disabled checks to get a benchmark | Changes the safety contract | Keep checks and measure first |

## Checklist

- Keep ordinary code ordinary.
- Give generics a demonstrated shared capability.
- Preserve ORC and runtime checks.
- Justify any low-level optimization with measurements.

## References

- [Nim manual](https://nim-lang.org/docs/manual.html)
- [Nim memory management](https://nim-lang.org/docs/mm.html)
