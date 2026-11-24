---
id: nim/testing
title: "Testing"
summary: "Use native unit tests and check both behavior and error categories."
language: nim
topic: testing
tags: [testing, errors]
related: [nim/errors]
snippets: unverified
---

# Testing

## Summary

Use native unit tests and check both behavior and error categories. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for changed behavior or a fixed defect. For option, result, and exceptions, see [Option, Result, and Exceptions](errors.md).

## Rules

- **SHOULD** Add `std/unittest` tests (and integration tests when relevant) for main behavior, expected failures, and boundary cases. Add regression tests for fixed bugs.
- **SHOULD** Inspect existing tests, exports, and Nimble configuration. Use an integration check when it exercises a real boundary.

## Recommended Pattern

Save the implementation from [Option, Result, and Exceptions](errors.md#recommended-pattern) under `src/shop/catalog.nim`. Add `src` to the module path in the package test configuration (or pass `--path:src`).

```nim
# tests/t_discount.nim
import std/unittest
import results
import shop/catalog

suite "discount":
  let product = Product(id: "p1", priceCents: 500)

  test "returns the discounted price, including zero at the boundary":
    for (amount, expected) in [(200'i64, 300'i64), (500'i64, 0'i64)]:
      let result = applyDiscount(product, amount)
      require result.isOk
      check result.get.priceCents == expected

  test "distinguishes negative and excessive amounts":
    for (amount, expected) in [(-1'i64, DiscountError.NegativeAmount),
                            (501'i64, DiscountError.ExceedsPrice)]:
      let result = applyDiscount(product, amount)
      require result.isErr
      check result.error == expected
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Only successful branch | Leaves typed errors unproved | Assert each error kind |
| get without checking isOk | Test crashes before a clear assertion | Require success first |
| Test new private helper only | Misses consumer behavior | Drive the public function |

## Checklist

- Cover exact-price and partial discount.
- Assert both failure categories.
- Reproduce bugs with regression tests.
- Exercise relevant entry points.

## References

- [std/unittest](https://nim-lang.org/docs/unittest.html)
- [nim-results](https://github.com/arnetheduck/nim-results)
