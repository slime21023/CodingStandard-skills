---
id: python/testing
title: "Testing"
summary: "Test observable behavior with deterministic, focused cases."
language: python
topic: testing
tags: [testing, errors]
related: [python/errors]
snippets: unverified
---

# Testing

## Summary

Test observable behavior with deterministic, focused cases. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when changing behavior or fixing a defect. For result and error boundaries, see [Result and Error Boundaries](errors.md).

## Rules

- **SHOULD** Use pytest; test observable behavior rather than implementation details.
- **SHOULD** Cover Result `Ok`/`Err`, boundaries, important edge cases, and error propagation.
- **SHOULD** Add regression tests for bug fixes; use integration tests for significant I/O boundaries.
- **SHOULD** Mock external dependencies selectively; do not force arbitrary global coverage thresholds.

## Dependencies

Use `pytest` as a development dependency.

## Recommended Pattern

Save the two source files from [Result and Error Boundaries](errors.md#recommended-pattern). With the package installed or its `src` directory on the import path, run `pytest`.

```python
# tests/test_discount.py
import pytest

from shop.catalog.discount import DiscountError, Product, apply_discount
from shop.result import Err, Ok


@pytest.mark.parametrize("amount_cents,expected_cents", [(200, 300), (500, 0)])
def test_discount_price(amount_cents: int, expected_cents: int) -> None:
    result = apply_discount(Product("p1", 500), amount_cents)
    assert result == Ok(Product("p1", expected_cents))


@pytest.mark.parametrize("amount_cents,error", [
    (-1, DiscountError.NEGATIVE_AMOUNT),
    (501, DiscountError.EXCEEDS_PRICE),
])
def test_discount_rejection(amount_cents: int, error: DiscountError) -> None:
    assert apply_discount(Product("p1", 500), amount_cents) == Err(error)
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Test inspects helper calls | Couples tests to implementation | Assert returned values |
| Missing edge amount | Leaves the price boundary unproved | Check amount equal to price |
| Mocked domain calculation | Does not test actual behavior | Keep pure calculations real |

## Checklist

- Cover success and the exact-price boundary.
- Check each expected failure type.
- Add reproducing coverage for fixes.
- Test significant I/O boundaries with appropriate integration coverage.

## References

- [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html)
