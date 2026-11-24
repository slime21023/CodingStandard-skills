---
id: rust/testing
title: "Testing"
summary: "Cover observable behavior, boundaries, and relevant concurrency outcomes."
language: rust
topic: testing
tags: [testing, errors]
related: [rust/errors]
snippets: unverified
---

# Testing

## Summary

Cover observable behavior, boundaries, and relevant concurrency outcomes. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when changing public behavior, fixing bugs, or changing task lifetime. For errors, see [Errors](errors.md).

## Rules

- **SHOULD** Keep unit tests near the code, integration tests under tests/, and useful public examples as doctests.
- **MUST** Cover success, important failure, and boundary cases for each changed behavior; add a regression test for a fixed defect.
- **SHOULD** Test cancellation, timeouts, completion, and limits without fragile timing assumptions.
- **AVOID** Avoid arbitrary coverage quotas and production refactors solely to accommodate tests.

## Recommended Pattern

Save the implementation from [Errors](errors.md#recommended-pattern) as the sibling `discount.rs`.

```rust
// src/catalog/discount_tests.rs
#[cfg(test)]
#[path = "discount.rs"]
mod discount;

#[cfg(test)]
mod tests {
    use super::discount::{DiscountError, Product, apply_discount};

    #[test]
    fn discount_accepts_regular_and_exact_price_amounts() {
        for (amount, expected) in [(200, 300), (500, 0)] {
            let product = Product { id: "p1".into(), price_cents: 500 };
            assert_eq!(apply_discount(product, amount).map(|value| value.price_cents), Ok(expected));
        }
    }

    #[test]
    fn discount_distinguishes_invalid_amounts() {
        for (amount, expected) in [(-1, DiscountError::NegativeAmount), (501, DiscountError::ExceedsPrice)] {
            let product = Product { id: "p1".into(), price_cents: 500 };
            assert_eq!(apply_discount(product, amount), Err(expected));
        }
    }
}
```

Run this file with `rustc --edition 2024 --test src/catalog/discount_tests.rs`, then run the produced test binary. In a crate, normally place the tests beside the implementation in its existing module tree.

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Assertions use private helper state | Does not verify the outward contract | Assert the returned result |
| Test sleeps to wait for work | Ordering is nondeterministic | Synchronize with events |
| Missing exact-price case | Leaves the valid boundary unproved | Assert the zero-price result |

## Checklist

- Exercise ordinary and boundary successes.
- Distinguish both expected errors.
- Test public API behavior in integration tests.
- Keep concurrency checks independent and deterministic.

## References

- [Rust testing](https://doc.rust-lang.org/book/ch11-00-testing.html)
