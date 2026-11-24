---
id: python/errors
title: "Result and Error Boundaries"
summary: "Use one typed Result for expected failures and preserve unexpected exceptions."
language: python
topic: errors
tags: [errors, result, exceptions, cancellation]
related: [python/data-and-functions]
snippets: unverified
---

# Result and Error Boundaries

## Summary

Use one typed Result for expected failures and preserve unexpected exceptions. Do not force infallible helpers to return Result. Convert recoverable outcomes to protocol responses only at the application boundary.

## When to Use

Use this for recoverable validation or a boundary that can classify external errors. For data, functions, and classes, see [Data, Functions, and Classes](data-and-functions.md).

## Rules

- **SHOULD** Return `Ok` on success and `Err` for expected, recoverable failure.
- **SHOULD** Prefer structured errors with distinguishable codes/types, not message parsing.
- **SHOULD** Catch specific external exceptions only at boundaries that can convert them into meaningful Result errors.
- **SHOULD** Keep programmer mistakes, broken invariants, and unexpected failures as exceptions.
- **MUST** Do not silently swallow exceptions or create a second incompatible Result abstraction.
- **MUST** Do not force every helper to return Result or `unwrap()` ordinary failure branches.
- **SHOULD** Convert Result to exit codes or protocol responses at application boundaries.
- **SHOULD** Preserve cancellation (`asyncio.CancelledError`) and do not convert it to business `Err`.

## Recommended Pattern

Put the Result definitions in the first file and reuse them from all feature modules.

```python
# src/shop/result.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Ok[T]:
    value: T


@dataclass(frozen=True, slots=True)
class Err[E]:
    error: E


type Result[T, E] = Ok[T] | Err[E]
```

Use structured error categories at the public boundary.

```python
# src/shop/catalog/discount.py
from dataclasses import dataclass, replace
from enum import Enum, auto

from shop.result import Err, Ok, Result


@dataclass(frozen=True, slots=True)
class Product:
    product_id: str
    price_cents: int


class DiscountError(Enum):
    NEGATIVE_AMOUNT = auto()
    EXCEEDS_PRICE = auto()


def apply_discount(product: Product, amount_cents: int) -> Result[Product, DiscountError]:
    if amount_cents < 0:
        return Err(DiscountError.NEGATIVE_AMOUNT)
    if amount_cents > product.price_cents:
        return Err(DiscountError.EXCEEDS_PRICE)
    return Ok(replace(product, price_cents=product.price_cents - amount_cents))
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Second local Result type | Makes feature contracts incompatible | Import the project Result |
| Catch-all adapter | Converts defects into business errors | Catch only understood external failures |
| Treat cancellation as an error value | Breaks task supervision | Propagate CancelledError |

## Checklist

- Return distinguishable errors.
- Handle both Result branches.
- Translate expected failures only at meaningful boundaries.
- Let unexpected exceptions and cancellation propagate.

## References

- [PEP 695](https://peps.python.org/pep-0695/)
- [Python errors and exceptions](https://docs.python.org/3/tutorial/errors.html)
- [asyncio tasks](https://docs.python.org/3/library/asyncio-task.html)
