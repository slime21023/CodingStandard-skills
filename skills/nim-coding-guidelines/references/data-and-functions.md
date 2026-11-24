---
id: nim/data-and-functions
title: "Data, Procedures, and Control Flow"
summary: "Use value objects and make mutation and I/O visible."
language: nim
topic: data-and-functions
tags: [data, functions, control-flow]
related: [nim/abstraction]
snippets: unverified
---

# Data, Procedures, and Control Flow

## Summary

Use value objects and make mutation and I/O visible. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for value models and calculations. For abstraction, memory, and performance, see [Abstraction, Memory, and Performance](abstraction.md).

## Rules

- **SHOULD** Prefer value `object`, `enum`, `tuple`, and standard collections. Use `ref object` only when identity or reference semantics are necessary.
- **SHOULD** Prefer data and functions, composition over inheritance, and concrete types over unnecessary dispatch via `method`. Avoid hidden mutable global state.
- **SHOULD** Public records may expose plain data; hide fields whose changes could violate invariants and provide validated construction or update functions.
- **SHOULD** Use `func` for side-effect-free calculations and `proc` for I/O, logging, and other effects.
- **SHOULD** Prefer return values to `var` output parameters. Make mutation intentional and local.
- **SHOULD** Keep each routine focused; prefer guard clauses and early returns to nested conditions. Use Nim's implicit `result` or final expressions when clear, and explicit `return` for meaningful control flow.
- **AVOID** Avoid deeply nested `if` expressions, obscure operator tricks, and large expressions when named intermediate values improve reading.
- **SHOULD** Function length, argument count, and nesting depth are review signals, not arbitrary automated limits.

## Recommended Pattern

```nim
# src/shop/orders/totals.nim
type OrderLine* = object
  productId*: string
  quantity*: int64
  unitPriceCents*: int64

func orderTotalCents*(lines: openArray[OrderLine]): int64 =
  ## Sum validated lines whose total fits in int64.
  for line in lines:
    result += line.quantity * line.unitPriceCents
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| ref object for simple data | Adds reference semantics | Use a value object |
| I/O inside a calculation | Makes effects unclear | Extract an effectful proc |
| var output unnecessarily | Hides the produced value | Return a result |

## Checklist

- Use value semantics for plain records.
- Use func only for side-effect-free operations.
- Keep guards simple.
- Do not replace review judgment with quotas.

## References

- [Nim manual](https://nim-lang.org/docs/manual.html)
