---
id: rust/errors
title: "Errors"
summary: "Use Result for recoverable failures and Option for normal absence."
language: rust
topic: errors
tags: [errors, result, option]
related: [rust/data-and-functions]
snippets: unverified
---

# Errors

## Summary

Use Result for recoverable failures and Option for normal absence. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for recoverable work or boundary diagnostics. For data, functions, and control flow, see [Data, Functions, and Control Flow](data-and-functions.md).

## Rules

- **MUST** Use Result<T, E> for recoverable errors and Option<T> for legitimate absence; use ? for straightforward propagation and retain error sources.
- **SHOULD** Use meaningful typed errors in library APIs; prefer std and use thiserror when it removes material boilerplate.
- **SHOULD** Use contextual diagnostics at application boundaries; use anyhow where useful without leaking it into a public library contract.
- **MUST** Never swallow errors, flatten them all into strings, or mask failures with unconditional defaults.
- **AVOID** Avoid unwrap() in normal production paths; use expect() only for a proven invariant with an explanation.
- **MUST** Do not panic for routine input or I/O failures.
- **SHOULD** Choose error variants around caller handling, not one error type per function.

## Dependencies

Prefer standard-library errors. Consider [`thiserror`](https://docs.rs/thiserror/) for library error definitions and [`anyhow`](https://docs.rs/anyhow/) for application-level diagnostic context.

## Recommended Pattern

```rust
// src/catalog/discount.rs
#[derive(Debug, PartialEq, Eq)]
pub struct Product {
    pub id: String,
    pub price_cents: i64,
}

#[derive(Debug, PartialEq, Eq)]
pub enum DiscountError {
    NegativeAmount,
    ExceedsPrice,
}

/// Return the adjusted product, or a typed validation error.
pub fn apply_discount(mut product: Product, amount_cents: i64) -> Result<Product, DiscountError> {
    if amount_cents < 0 {
        return Err(DiscountError::NegativeAmount);
    }
    if amount_cents > product.price_cents {
        return Err(DiscountError::ExceedsPrice);
    }
    product.price_cents -= amount_cents;
    Ok(product)
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Unconditional default | Converts failure into a plausible value | Return the original error |
| String-only cause | Loses branching and source information | Use a typed error with causal context |
| Public anyhow::Error by default | Makes recoverable contracts opaque | Expose a useful library error |

## Checklist

- Keep normal absence distinct.
- Make error variants meaningful to callers.
- Propagate without dropping causes.
- Reserve panics for real defects or invariants.

## References

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Rust Result](https://doc.rust-lang.org/std/result/)
