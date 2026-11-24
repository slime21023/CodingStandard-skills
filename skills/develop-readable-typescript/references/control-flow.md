---
id: typescript/control-flow
title: "Functions and Control Flow"
summary: "Use straightforward branches and keep the main path visible."
language: typescript
topic: control-flow
tags: [functions, control-flow]
related: [typescript/types]
snippets: unverified
---

# Functions and Control Flow

## Summary

Use straightforward branches and keep the main path visible. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when branching on status or refactoring complex conditions. For type system, see [Type System](types.md).

## Rules

- **MUST** a function's name must match its actual responsibility; side effects must not hide behind names that look like pure queries.
- **SHOULD** keep each function focused on a single goal that is easy to explain; prefer early returns.
- **SHOULD** extract complex conditions into semantically named variables or functions.
- **SHOULD** use the ternary operator only for simple value selection that reads at a glance.
- **SHOULD** when nesting exceeds two levels, actively consider splitting the function or returning early.
- **AVOID** nested ternaries, overly long functions, and semantically meaningless chained transformations.
- **AVOID** using hard line limits in place of judgment about responsibility and readability.

## Recommended Pattern

```typescript
// src/orders/shipping.ts
type OrderStatus = "pending" | "paid" | "shipped" | "cancelled";
type Order = { id: string; status: OrderStatus; address?: { city: string } };

export function orderStatusLabel(status: OrderStatus): string {
  switch (status) {
    case "pending": return "Pending";
    case "paid": return "Paid";
    case "shipped": return "Shipped";
    case "cancelled": return "Cancelled";
  }
}

export function shippingLabel(order: Order): string {
  if (order.status === "cancelled") return "Cancelled";
  if (!order.address) return "Missing address";
  return `${order.address.city}: ${order.id}`;
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Nested ternary | Obscures outcomes | Name conditions or use guards |
| Default hides new states | Misses compiler checking | Enumerate known cases |
| Query function writes state | Misleads callers | Name operations after effects |

## Checklist

- Trace the happy path.
- Name meaningful complex conditions.
- Expose effects in operation names.
- Check that all states have a branch.

## References

- [TypeScript narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
