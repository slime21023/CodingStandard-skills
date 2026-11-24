---
id: typescript/errors
title: "Error Semantics"
summary: "Represent expected recoverable failures with typed results."
language: typescript
topic: errors
tags: [errors, result, exceptions]
related: [typescript/data-and-functions]
snippets: unverified
---

# Error Semantics

## Summary

Represent expected recoverable failures with typed results. Use exceptions for programming defects and unexpected failures; do not turn them into business errors.

## When to Use

Use this where the caller is expected to recover. For data, functions, and classes, see [Data, Functions, and Classes](data-and-functions.md).

## Rules

- **MUST** use a typed `Result<T, E>` or discriminated union for expected business failures that the caller can handle.
- **MUST** propagate unexpected failures (programming defects, violated invariants, unrecoverable system faults) as exceptions; do not silently turn them into success values or vague business errors.
- **SHOULD** use a uniform `Result<T, E>` shape for common operation failures; use a discriminated union that describes each state for mutually exclusive states (for example loading / ready / failed).
- **SHOULD** use explicit error codes or structured fields; avoid branching on error strings for control flow.
- **SHOULD** use `try/catch` at boundaries that can understand and handle the failure; convert only identified, recoverable external failures into expected errors, and let other failures continue to propagate.
- **AVOID** wrapping every small function in Result, catching and rethrowing the same exception repeatedly, and empty `catch` blocks.
- **SHOULD** Classify network and storage errors by whether recovery is part of the public contract.

## Recommended Pattern

```typescript
// src/catalog/discount.ts
export type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export type Product = { readonly id: string; readonly priceCents: number };
export type DiscountError = { code: "NEGATIVE_AMOUNT" | "EXCEEDS_PRICE" };

// Amount and price are safe integers in minor units at this boundary.
export function applyDiscount(
  product: Product,
  amountCents: number,
): Result<Product, DiscountError> {
  if (amountCents < 0) {
    return { ok: false, error: { code: "NEGATIVE_AMOUNT" } };
  }
  if (amountCents > product.priceCents) {
    return { ok: false, error: { code: "EXCEEDS_PRICE" } };
  }
  return { ok: true, value: { ...product, priceCents: product.priceCents - amountCents } };
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Converting every exception to Result | Hides bugs or unrecoverable failure | Translate only known cases |
| String comparison on message | Makes diagnostics part of the API | Use structured codes |
| Empty catch | Silently loses evidence | Handle at a meaningful boundary |

## Checklist

- Preserve the unexpected exception path.
- Check the discriminant before reading data.
- Use error codes for recovery.
- Do not wrap infallible helpers in Result.

## References

- [TypeScript narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
