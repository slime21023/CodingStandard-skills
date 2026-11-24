---
id: rust/naming-and-formatting
title: "Edition, Naming, and Formatting"
summary: "Use Stable Rust and state the actual supported Rust version."
language: rust
topic: naming-and-formatting
tags: [naming, formatting, tooling]
related: [rust/tooling]
snippets: unverified
---

# Edition, Naming, and Formatting

## Summary

Use Stable Rust and state the actual supported Rust version. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for source style and version baseline decisions. For dependencies and ci, see [Dependencies and CI](tooling.md).

## Rules

- **MUST** For new projects use the Rust 2024 edition on stable and do not add nightly-only features.
- **MUST** Declare the actual MSRV in Cargo.toml as rust-version; Edition 2024 requires at least Rust 1.85.
- **SHOULD** Follow rustfmt and use PascalCase for types, traits, and variants, snake_case for modules, functions, and variables, and SCREAMING_SNAKE_CASE for constants.
- **AVOID** Avoid unnecessary abbreviations and ambiguous names.

## Recommended Pattern

```rust
// src/catalog/products.rs
pub const MAX_SEARCH_RESULTS: usize = 50;

pub struct Product {
    pub id: String,
    pub name: String,
    pub price_cents: i64,
}

pub fn find_product_by_id<'products>(products: &'products [Product], product_id: &str) -> Option<&'products Product> {
    products.iter().find(|product| product.id == product_id)
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Undeclared MSRV | CI can drift from consumers | Set rust-version |
| Nightly feature on stable | Fails on the supported toolchain | Use stable facilities |
| Opaque abbreviated name | Obscures the contract | Name the domain value |

## Checklist

- Inspect the edition and MSRV.
- Use rustfmt and Rust casing conventions.
- Avoid nightly-only features.
- Confirm names describe data and behavior.

## References

- [Rust Style Guide](https://doc.rust-lang.org/stable/style-guide/)
- [Rust 2024 Edition](https://doc.rust-lang.org/edition-guide/rust-2024/index.html)
