---
id: typescript/testing
title: "Testing and Comments"
summary: "Test observable behavior, failure branches, and meaningful boundaries."
language: typescript
topic: testing
tags: [testing, documentation]
related: [typescript/errors]
snippets: unverified
---

# Testing and Comments

## Summary

Test observable behavior, failure branches, and meaningful boundaries. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for behavior changes or bug fixes. For error semantics, see [Error Semantics](errors.md).

## Rules

- **MUST** when fixing a bug, add a test that reproduces the failure (where applicable).
- **SHOULD** focus tests on observable behavior and boundary conditions; do not bind them to implementation details.
- **SHOULD** for Result, test the success path and the main error branches; for exceptions, test that they are thrown, translated, or logged at the correct boundary.
- **SHOULD** have comments explain "why, constraints, and trade-offs"; avoid restating what the code is doing.
- **SHOULD** keep changes focused; avoid incidental unrelated refactoring.
- **AVOID** using excessive comments to compensate for unclear names and function structure.

## Recommended Pattern

Use the source file from [Error Semantics](errors.md#recommended-pattern). This example uses the Node.js test runner and Node types for TypeScript.

```typescript
// test/discount.test.ts
import { deepStrictEqual } from "node:assert/strict";
import { test } from "node:test";
import { applyDiscount } from "../src/catalog/discount.js";

const product = { id: "p1", priceCents: 500 };

test("returns the discounted price and accepts the exact-price boundary", () => {
  deepStrictEqual(applyDiscount(product, 200), {
    ok: true, value: { id: "p1", priceCents: 300 },
  });
  deepStrictEqual(applyDiscount(product, 500), {
    ok: true, value: { id: "p1", priceCents: 0 },
  });
});

test("returns distinguishable errors for invalid discount amounts", () => {
  deepStrictEqual(applyDiscount(product, -1), {
    ok: false, error: { code: "NEGATIVE_AMOUNT" },
  });
  deepStrictEqual(applyDiscount(product, 501), {
    ok: false, error: { code: "EXCEEDS_PRICE" },
  });
});
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Only happy path | Misses failure contracts | Check expected codes and edges |
| Tests tied to helper calls | Harmless refactors break tests | Assert public outputs |
| Comments restate obscure statements | Complexity remains | Clarify the code then document constraints |

## Checklist

- Cover the exact-price boundary.
- Assert both expected error codes.
- Reproduce the defect before fixing it where applicable.
- Assert exceptions at the correct boundary.

## References

- [Node.js test runner](https://nodejs.org/api/test.html)
