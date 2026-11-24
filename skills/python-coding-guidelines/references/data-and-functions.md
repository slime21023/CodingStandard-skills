---
id: python/data-and-functions
title: "Data, Functions, and Classes"
summary: "Use explicit value objects and independent functions for domain calculations."
language: python
topic: data-and-functions
tags: [data, functions, classes]
related: [python/errors]
snippets: unverified
---

# Data, Functions, and Classes

## Summary

Use explicit value objects and independent functions for domain calculations. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when designing a business calculation or value type. For result and error boundaries, see [Result and Error Boundaries](errors.md).

## Rules

- **SHOULD** Write business logic as independent functions with explicit inputs and outputs.
- **SHOULD** Use `@dataclass(frozen=True, slots=True)` for value objects by default; use mutable data only when justified.
- **MUST** Do not mistake frozen fields for deep immutability.
- **SHOULD** Use `TypedDict` to describe dictionary-shaped data statically, but validate untrusted inputs at runtime.
- **SHOULD** Use `Enum` or `Literal` for finite states; use ordinary built-in collections for simple temporary data.
- **SHOULD** Use classes when managing state, resource lifecycles, context managers, or externally required object protocols.
- **AVOID** Avoid unnecessary Manager, Service, Factory, and inheritance hierarchies.
- **MUST** Never use mutable default arguments; use `default_factory` when appropriate.

## Recommended Pattern

```python
# src/shop/orders/totals.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderLine:
    product_id: str
    quantity: int
    unit_price_cents: int


def order_total_cents(lines: tuple[OrderLine, ...]) -> int:
    return sum(line.quantity * line.unit_price_cents for line in lines)
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Manager with no state | Adds a layer to a pure calculation | Use a function |
| Frozen record containing a list | Still permits mutation through the list | Use immutable values when required |
| Default list argument | Shares mutable state between calls | Use a factory or initialize locally |

## Checklist

- Make the value and its inputs explicit.
- Use functions for independent logic.
- Confirm immutable fields are actually immutable.
- Reserve classes for meaningful behavior or lifecycle.

## References

- [Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Typing](https://docs.python.org/3/library/typing.html)
