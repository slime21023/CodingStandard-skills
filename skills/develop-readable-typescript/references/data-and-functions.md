---
id: typescript/data-and-functions
title: "Data, Functions, and Classes"
summary: "Keep calculations separate from I/O and shared state."
language: typescript
topic: data-and-functions
tags: [data, functions, classes]
related: [typescript/errors]
snippets: unverified
---

# Data, Functions, and Classes

## Summary

Keep calculations separate from I/O and shared state. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for domain models and transformations. For error semantics, see [Error Semantics](errors.md).

## Rules

- **SHOULD** represent ordinary data structures as `type` / objects; implement business rules as standalone functions and prefer composition.
- **SHOULD** separate pure computation and data transformation from I/O boundaries to ease testing.
- **SHOULD** use `class` only when there is a concrete need for **state encapsulation, resource lifecycle, or a framework contract**. Examples: Web Components, connection management, or a necessary Error subclass.
- **SHOULD** avoid mutating input data in data transformations; keep side effects such as I/O, time, and randomness identifiable.
- **SHOULD** Prefer composition over inheritance and avoid speculative layers.
- **AVOID** Do not group static helpers in a class.

Note: Functions first does not forbid objects, stateful code, or impure operations.

## Recommended Pattern

```typescript
// src/orders/totals.ts
export type OrderLine = {
  readonly productId: string;
  readonly quantity: number;
  readonly unitPriceCents: number;
};

// Call with validated quantities and prices whose total is a safe integer.
export function orderTotalCents(lines: readonly OrderLine[]): number {
  return lines.reduce((sum, line) => sum + line.quantity * line.unitPriceCents, 0);
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Class wrapping a pure function | Adds ceremony without ownership | Export the function |
| Hidden I/O in calculation | Makes behavior nonlocal | Put I/O at a boundary |
| Mutating input array | Changes caller state | Consume readonly inputs |

## Checklist

- State arithmetic assumptions.
- Keep transformation inputs explicit.
- Put I/O and state mutations at named boundaries.
- Use classes for a real lifecycle or contract.

## References

- [Object types](https://www.typescriptlang.org/docs/handbook/2/objects.html)
