---
id: typescript/naming-and-formatting
title: "Naming and Declarations"
summary: "Make names reflect the data and the effects of code."
language: typescript
topic: naming-and-formatting
tags: [naming, formatting]
related: [typescript/tooling]
snippets: unverified
---

# Naming and Declarations

## Summary

Make names reflect the data and the effects of code. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for declarations and mechanical formatting. For tooling baseline, see [Tooling Baseline](tooling.md).

## Rules

- **MUST** use `camelCase` for variables and functions; use `PascalCase` for types, interfaces, and classes.
- **MUST** use meaningful names; avoid unnecessary abbreviations such as `usr`, `cfg`, and `tmp`.
- **SHOULD** give functions verb-oriented names, such as `findUser` and `calculateTotal`.
- **SHOULD** prefix booleans with `is`, `has`, `can`, `should`, etc.
- **SHOULD** use `const` by default; use `let` when reassignment is needed.
- **AVOID** `var`, Hungarian notation, and semantically empty Helper / Manager names.
- **SHOULD** Use Prettier for uniform formatting.

## Recommended Pattern

```typescript
// src/catalog/products.ts
export const maxSearchResults = 50;

export type Product = {
  readonly id: string;
  readonly name: string;
  readonly priceCents: number;
};

export function findProductById(
  products: readonly Product[],
  productId: string,
): Product | undefined {
  return products.find((product) => product.id === productId);
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Short opaque name | Requires the reader to infer purpose | Name the domain value |
| Reassignable local without reassignment | Hides a useful invariant | Use const |
| Formatting discussion in review | Distracts from behavior | Use the project formatter |

## Checklist

- Use camelCase for values and PascalCase for type names.
- Name flags so branches read naturally.
- Default to const.
- Use the project formatter.

## References

- [Everyday types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
- [Prettier](https://prettier.io/docs/)
