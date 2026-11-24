---
id: nim/naming-and-formatting
title: "Naming and Style"
summary: "Follow NEP-1 and make names describe their purpose."
language: nim
topic: naming-and-formatting
tags: [naming, formatting]
related: [nim/tooling]
snippets: unverified
---

# Naming and Style

## Summary

Follow NEP-1 and make names describe their purpose. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for formatting and naming. For checks and dependencies, see [Checks and Dependencies](tooling.md).

## Rules

- **SHOULD** Follow NEP-1: two-space indentation, no tabs, a roughly 80-character line-length target, `PascalCase` for types and pure enum members, and `camelCase` for procedures, functions, fields, and variables.
- **SHOULD** Use descriptive names. Avoid cryptic abbreviations, identifiers differentiated only by underscores/case, and clever compressed expressions.
- **SHOULD** Prefer `let`; use `var` only when reassignment is needed and `const` for compile-time values.

## Recommended Pattern

```nim
# src/shop/products.nim
import std/options

const maxSearchResults = 50

type Product = object
  id: string
  name: string
  priceCents: int64

func findProductById(products: openArray[Product]; productId: string): Option[Product] =
  for product in products:
    if product.id == productId:
      return some(product)
  none(Product)
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Tab indentation | Conflicts with NEP-1 | Use two spaces |
| Names differ only by underscore or case | Nim identifiers can collide | Choose distinct semantic names |
| var for an immutable local | Misstates intended use | Prefer let |

## Checklist

- Use two-space indentation.
- Use PascalCase types and camelCase routines.
- Use descriptive identifiers.
- Declare reassignment only where needed.

## References

- [NEP-1](https://nim-lang.org/docs/nep1.html)
