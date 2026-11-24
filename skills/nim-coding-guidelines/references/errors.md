---
id: nim/errors
title: "Option, Result, and Exceptions"
summary: "Keep absence, expected errors, and unexpected exceptions distinct."
language: nim
topic: errors
tags: [errors, result, option, exceptions, async]
related: [nim/data-and-functions]
snippets: unverified
---

# Option, Result, and Exceptions

## Summary

Keep absence, expected errors, and unexpected exceptions distinct. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for result-returning APIs, lookup, and effect boundaries. For data, procedures, and control flow, see [Data, Procedures, and Control Flow](data-and-functions.md).

## Rules

- **SHOULD** Use `std/options.Option[T]` for ordinary absence, **`results.Result[T, E]`** for expected recoverable failures, and Exception for unexpected failures.
- **SHOULD** Standardize on the third-party [`arnetheduck/nim-results`](https://github.com/arnetheduck/nim-results) package (Nimble package `results`). Do not invent a second generic Result or silently switch Result implementations.
- **SHOULD** Prefer meaningful typed error categories. Every Result must be handled or propagated; use the package's `?` propagation helper only when it keeps flow straightforward.
- **SHOULD** Catch only specific expected `CatchableError` descendants at I/O and dependency boundaries, then convert to a meaningful Result. Never use empty bare `except`, swallow failures, treat `Defect` as a normal business error, or log the same failure at every layer.
- **SHOULD** Where useful, enforce an exception-free synchronous API with `{.raises: [].}` and verify compilation. Do **not** assume this guarantee holds for `std/asyncdispatch` async procedures.
- **SHOULD** Await asynchronous work or explicitly handle it (e.g., `asyncCheck` where appropriate); never blindly `discard` a Future.

Note: Preserve useful operation context if the error code alone is insufficient. `{.raises: [].}` enforced on a suitable compiled synchronous routine is not a no-exception guarantee for `std/asyncdispatch`.

## Dependencies

Use the Nimble package [`results`](https://github.com/arnetheduck/nim-results) for typed expected failure. Lock a tested version using the project mechanism.

## Recommended Pattern

Use an explicitly selected version of the `results` package for this feature. Callers using the Result helper API should also import `results`.

```nim
# src/shop/catalog.nim
import results

type
  Product* = object
    id*: string
    priceCents*: int64
  DiscountError* {.pure.} = enum
    NegativeAmount, ExceedsPrice

func applyDiscount*(product: Product; amountCents: int64): Result[Product, DiscountError] =
  ## Return a discounted value or a typed validation error.
  if amountCents < 0:
    return Result[Product, DiscountError].err(DiscountError.NegativeAmount)
  if amountCents > product.priceCents:
    return Result[Product, DiscountError].err(DiscountError.ExceedsPrice)
  Result[Product, DiscountError].ok(
    Product(id: product.id, priceCents: product.priceCents - amountCents)
  )
```

### Ordinary absence

```nim
# src/shop/catalog_lookup.nim
import std/options

func findName(names: openArray[string]; target: string): Option[string] =
  for name in names:
    if name == target:
      return some(name)
  none(string)
```

### Adapter boundary

```nim
# src/shop/catalog_file.nim
import results

type CatalogError {.pure.} = enum
  CannotRead

proc loadCatalogText(path: string): Result[string, CatalogError] =
  try:
    return Result[string, CatalogError].ok(readFile(path))
  except IOError, OSError:
    return Result[string, CatalogError].err(CatalogError.CannotRead)
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Result for a normal lookup miss | Misrepresents legitimate absence | Return Option |
| Bare except | Can hide defects | Catch specific expected CatchableError types |
| Discarded Future | Drops failures and completion | Await or supervise it |

## Checklist

- Use only the agreed Result package.
- Keep expected errors typed.
- Handle or propagate every Result and Future.
- Limit exception translation to the dependency boundary.

## References

- [Nim manual](https://nim-lang.org/docs/manual.html)
- [nim-results](https://github.com/arnetheduck/nim-results)
- [Async dispatch](https://nim-lang.org/docs/asyncdispatch.html)
