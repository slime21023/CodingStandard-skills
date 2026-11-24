---
id: nim/modules-and-api
title: "Modules and Public APIs"
summary: "Group related code by feature and export only the public contract."
language: nim
topic: modules-and-api
tags: [modules, public-api, documentation]
related: [nim/abstraction]
snippets: unverified
---

# Modules and Public APIs

## Summary

Group related code by feature and export only the public contract. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for new Nimble packages and published module contracts. For abstraction, memory, and performance, see [Abstraction, Memory, and Performance](abstraction.md).

## Rules

- **SHOULD** Organize Nimble modules by feature/domain, keeping small packages flat and splitting only as responsibilities grow. Avoid circular dependencies and generic `common`/`utils`/`manager` dumping grounds.
- **SHOULD** Export only necessary symbols with `*`. For libraries, keep an intentional public entry module and selectively `export` stable APIs.
- **SHOULD** Give public routines explicit parameter/result types, documented failure behavior, and `##` doc comments. Do not export internal mutable state or implementation details merely for convenience.
- **SHOULD** Consider compatibility before changing public names, types, or semantics.
- **SHOULD** Keep a deliberate Nimble package entry point and connect it only to stable feature APIs.

## Recommended Pattern

Save the first module as `src/shop/orders.nim` and export the public operation through `src/shop.nim`.

```nim
# src/shop/orders.nim
import std/strutils

func normalizeOrderId(orderId: string): string =
  orderId.strip()

func placeOrder*(orderId: string): string =
  ## Return the normalized ID to place through the caller's storage boundary.
  normalizeOrderId(orderId)
```

```nim
# src/shop.nim
import shop/orders
export orders.placeOrder
```

```nim
# shop.nimble
version = "0.1.0"
author = "Shop contributors"
description = "Shop module examples"
license = "MIT"
srcDir = "src"
requires "nim >= 2.2"
```

```text
shop.nimble
src/
  shop.nim
  shop/
    orders.nim
tests/
  t_orders.nim
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Exporting all symbols | Makes internal choices into contracts | Export only the entry point |
| Flat utils grows across domains | Obscures ownership | Group actual capabilities |
| Exposing internal mutable state | Bypasses invariants | Keep mutable implementation details private |

## Checklist

- Use * only for intentional exports.
- Keep public signatures and failure behavior explicit.
- Add ## documentation to public routines.
- Check public names and behavior before changing them.

## References

- [Nim manual](https://nim-lang.org/docs/manual.html)
- [Nimble](https://nim-lang.github.io/nimble/)
