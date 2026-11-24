---
id: rust/abstraction
title: "Traits and Generics"
summary: "Start concrete and add polymorphism only for a real contract."
language: rust
topic: abstraction
tags: [interfaces, generics]
related: [rust/modules-and-api]
snippets: unverified
---

# Traits and Generics

## Summary

Start concrete and add polymorphism only for a real contract. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when interchangeable providers or type relationships are real. For modules and public apis, see [Modules and Public APIs](modules-and-api.md).

## Rules

- **SHOULD** Use concrete types until shared behavior, a generic algorithm, an extension contract, or interoperability requires more.
- **SHOULD** Use standard traits such as From, TryFrom, AsRef, and Debug when they express the contract.
- **SHOULD** Use generics or impl Trait for compile-time polymorphism and dyn Trait only when runtime polymorphism is needed.
- **AVOID** Avoid one trait per struct, trait creation solely for mocks, and speculative abstraction layers.

## Recommended Pattern

```rust
// src/billing/checkout.rs
pub trait PaymentGateway {
    type Error;

    fn charge(&self, order_id: &str, amount_cents: i64) -> Result<String, Self::Error>;
}

pub fn checkout<G: PaymentGateway>(
    gateway: &G,
    order_id: &str,
    amount_cents: i64,
) -> Result<String, G::Error> {
    gateway.charge(order_id, amount_cents)
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Trait for one pure helper | Adds no useful variation | Keep a concrete function |
| Custom conversion trait | Duplicates standard semantics | Use From or TryFrom |
| dyn for fixed provider | Indirect dispatch without a runtime need | Use a concrete type or generic |

## Checklist

- Identify the required substitution.
- Prefer standard traits when suitable.
- Keep the trait small.
- Choose compile-time or runtime dispatch deliberately.

## References

- [Rust Book](https://doc.rust-lang.org/book/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
