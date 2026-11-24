---
id: rust/modules-and-api
title: "Modules and Public APIs"
summary: "Organize small modules by capability and expose only stable contracts."
language: rust
topic: modules-and-api
tags: [modules, public-api, documentation]
related: [rust/abstraction]
snippets: unverified
---

# Modules and Public APIs

## Summary

Organize small modules by capability and expose only stable contracts. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when exposing or reorganizing a feature. For traits and generics, see [Traits and Generics](abstraction.md).

## Rules

- **SHOULD** Keep related code together and start with small capability modules; avoid speculative layers or crate splits.
- **SHOULD** Default to private. Use pub(crate) for necessary crate-wide access and pub only for intentional external contracts.
- **SHOULD** Use explicit public types and signatures without leaking implementation details.
- **SHOULD** Add /// documentation to public items and describe Errors, Panics, and examples as applicable.

## Recommended Pattern

```rust
// src/orders/mod.rs
/// Submit an order ID through the injected persistence boundary.
///
/// # Errors
/// Returns the error reported by the submission boundary.
pub fn place_order<E>(order_id: &str, submit: impl FnOnce(&str) -> Result<(), E>) -> Result<(), E> {
    submit(normalize_order_id(order_id))
}

fn normalize_order_id(order_id: &str) -> &str {
    order_id.trim()
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| pub on internal helpers | Freezes the implementation | Keep private unless a caller needs it |
| Crate per trivial feature | Adds cross-crate overhead | Organize with modules first |
| Undocumented fallibility | Leaves caller contract ambiguous | Add an Errors section |

## Checklist

- Check every exported symbol has an external role.
- Keep implementation details private.
- Document meaningful errors and panics.
- Add a use example when it clarifies the contract.

## References

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Rust Book](https://doc.rust-lang.org/book/)
