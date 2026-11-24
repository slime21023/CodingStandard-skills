---
id: rust/data-and-functions
title: "Data, Functions, and Control Flow"
summary: "Model data with structs and finite states with enums."
language: rust
topic: data-and-functions
tags: [data, functions, control-flow]
related: [rust/resources-and-memory]
snippets: unverified
---

# Data, Functions, and Control Flow

## Summary

Model data with structs and finite states with enums. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for modeling data and writing transformations. For ownership and borrowing, see [Ownership and Borrowing](resources-and-memory.md).

## Rules

- **SHOULD** Prefer structs and enums with independent functions; put type-owned operations in impl.
- **SHOULD** Keep normal flow shallow with guards, ?, let else, if let, or a relevant match.
- **SHOULD** Default to immutability, and use mut only when changing a value intentionally.
- **AVOID** Avoid hidden state, unnecessary interior mutability, and long iterator chains that obscure intent.
- **AVOID** Avoid allocation tricks, complex types, or low-level code for speculative performance.

## Recommended Pattern

```rust
// src/orders/totals.rs
pub struct OrderLine {
    pub product_id: String,
    pub quantity: i64,
    pub unit_price_cents: i64,
}

/// Sum validated order lines whose total fits in i64.
pub fn order_total_cents(lines: &[OrderLine]) -> i64 {
    lines.iter().map(|line| line.quantity * line.unit_price_cents).sum()
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Class-like wrapper around pure totals | Adds no invariant | Use a function |
| Nested option and error matches | Obscures the main path | Use a guard or ? |
| Unneeded interior mutability | Makes mutation easier to miss | Use immutable data by default |

## Checklist

- Separate data and computation.
- Document arithmetic assumptions.
- Choose transparent control flow.
- Keep mutations local and intentional.

## References

- [Rust Book](https://doc.rust-lang.org/book/)
- [Rust Style Guide](https://doc.rust-lang.org/stable/style-guide/)
