---
id: go/errors
title: "Errors"
summary: "Return native Go errors and wrap only where callers should inspect the cause."
language: go
topic: errors
tags: [errors, result]
related: [go/data-and-functions]
snippets: unverified
---

# Errors

## Summary

Return native Go errors and wrap only where callers should inspect the cause. A typed or sentinel cause lets callers recover without parsing error text.

## When to Use

Use this for fallible operations and adapter boundaries. For structs, functions, and methods, see [Structs, Functions, and Methods](data-and-functions.md).

## Rules

- **MUST** Use (T, error) for ordinary failures; do not introduce a generic Result framework.
- **MUST** Deliberately handle or propagate errors; never discard one just to shorten code.
- **SHOULD** Add operation context with fmt.Errorf; use %w when wrapping is part of the caller-facing contract and inspect with errors.Is or errors.As.
- **SHOULD** Prefer lowercase error messages without terminal punctuation, except proper nouns.
- **AVOID** Avoid business panic, string matching, swallowing errors, and redundant log-and-return at every layer.

Note: The example uses integer cents. Both amount errors also match `ErrInvalidDiscount` through `errors.Is`.

## Recommended Pattern

```go
// orders/discount.go
package orders

import (
    "errors"
    "fmt"
)

var ErrInvalidDiscount = errors.New("invalid discount")
var ErrNegativeAmount = fmt.Errorf("negative amount: %w", ErrInvalidDiscount)
var ErrExceedsPrice = fmt.Errorf("amount exceeds price: %w", ErrInvalidDiscount)

type Product struct {
    ID string
    PriceCents int64
}

// ApplyDiscount returns a discounted copy without modifying product.
func ApplyDiscount(product Product, amountCents int64) (Product, error) {
    switch {
    case product.PriceCents < 0:
        return Product{}, fmt.Errorf("discount product %s: %w", product.ID, ErrInvalidDiscount)
    case amountCents < 0:
        return Product{}, fmt.Errorf("discount product %s: %w", product.ID, ErrNegativeAmount)
    case amountCents > product.PriceCents:
        return Product{}, fmt.Errorf("discount product %s: %w", product.ID, ErrExceedsPrice)
    }
    product.PriceCents -= amountCents
    return product, nil
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Matching error text | Locks callers to diagnostics | Use errors.Is |
| Panic on invalid discount | Treats recoverable input as a defect | Return an error |
| Wrapping private dependency errors | Exposes them as API | Wrap only when intentional |

## Checklist

- Return a native error on recoverable failure.
- Keep error categories inspectable.
- Preserve useful operation context.
- Handle each returned error deliberately.

## References

- [Go error wrapping](https://go.dev/blog/go1.13-errors)
