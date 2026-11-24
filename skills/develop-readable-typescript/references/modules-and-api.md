---
id: typescript/modules-and-api
title: "Modules"
summary: "Expose a small feature API and keep helpers private."
language: typescript
topic: modules-and-api
tags: [modules, public-api]
related: [typescript/data-and-functions]
snippets: unverified
---

# Modules

## Summary

Expose a small feature API and keep helpers private. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when organizing files or changing an export. For data, functions, and classes, see [Data, Functions, and Classes](data-and-functions.md).

## Rules

- **MUST** every module has a describable responsibility; its public types and functions should be small and explicit.
- **SHOULD** use ES Modules and `import type`; organize files by feature and responsibility.
- **AVOID** classes created only to group functions, Java-style getters/setters, deep inheritance, circular dependencies, and semantically empty `helpers.ts` / `utils.ts`.
- **AVOID** unconditionally adding Repository, Service, Manager, or other intermediate layers just to match an architectural pattern.

## Recommended Pattern

```typescript
// src/orders/placement.ts
/** Submit an order using the given persistence boundary. */
export function placeOrder(orderId: string, submit: (orderId: string) => void): void {
  submit(normalizeOrderId(orderId));
}

function normalizeOrderId(orderId: string): string {
  return orderId.trim();
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Everything exported | Freezes implementation choices | Export only the public operation |
| Circular imports | Make initialization order fragile | Move behavior to its owner |
| utils.ts with unrelated exports | Hides capability boundaries | Group by feature |

## Checklist

- Use ES module imports and exports.
- Use import type where only a type is needed.
- Document the public operation.
- Keep private helpers and state out of the contract.

## References

- [TypeScript modules](https://www.typescriptlang.org/docs/handbook/2/modules.html)
