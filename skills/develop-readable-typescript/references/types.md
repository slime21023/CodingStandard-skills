---
id: typescript/types
title: "Type System"
summary: "Keep public types explicit and narrow unknown input before use."
language: typescript
topic: types
tags: [types, data, null-safety]
related: [typescript/errors]
snippets: unverified
---

# Type System

## Summary

Keep public types explicit and narrow unknown input before use. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for public type contracts and external input. For error semantics, see [Error Semantics](errors.md).

## Rules

- **MUST** enable `strict`; validate untrusted external data at runtime rather than relying on type assertions alone.
- **MUST** do not use `any` to evade checks. When truly needed, limit its scope and document the reason.
- **SHOULD** use `unknown` for unknown external values and narrow the type after validation.
- **SHOULD** allow type inference for local variables; give public functions and module boundaries clear types.
- **SHOULD** use `readonly`, literal unions, and discriminated unions where appropriate; use `satisfies` for configuration objects.
- **SHOULD** default to `type` for ordinary data shapes and unions; use `interface` when you actually need to extend a contract or use declaration merging. This is a **discussable team choice**, not a language rule.
- **AVOID** unnecessary `as T`, the non-null assertion `!`, and overly complex generics and type gymnastics.
- **AVOID** using TypeScript types in place of runtime validation of JSON / HTTP / user input.

Note: Defaulting to `type` over `interface` for ordinary data shapes is a team preference, not a language rule.

## Recommended Pattern

```typescript
// src/orders/state.ts
type OrderState =
  | { status: "pending" }
  | { status: "paid"; paidAtMillis: number }
  | { status: "cancelled"; reason: string };

export const tracking = { expireAfterDays: 7 } satisfies { expireAfterDays: number };

export function isOrderState(value: unknown): value is OrderState {
  if (typeof value !== "object" || value === null || !("status" in value)) {
    return false;
  }
  switch (value.status) {
    case "pending":
      return true;
    case "paid":
      return "paidAtMillis" in value && typeof value.paidAtMillis === "number"
        && Number.isFinite(value.paidAtMillis);
    case "cancelled":
      return "reason" in value && typeof value.reason === "string";
    default:
      return false;
  }
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| JSON cast | Does not validate runtime input | Check the actual shape |
| any at a boundary | Stops checking the consumers | Use unknown and narrow |
| Optional fields for all states | Allows incompatible combinations | Use a discriminated union |

## Checklist

- Keep strict mode enabled.
- Narrow unknown at the boundary.
- Make discriminants literal and explicit.
- Keep assertions narrow and justified.

## References

- [TypeScript narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [The satisfies operator](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html)
