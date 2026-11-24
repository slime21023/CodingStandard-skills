---
id: c3/naming-and-formatting
title: "Version, Naming, and Style"
summary: "Use a verified stable C3 compiler and clear names."
language: c3
topic: naming-and-formatting
tags: [naming, formatting, tooling]
related: [c3/tooling]
snippets: unverified
---

# Version, Naming, and Style

## Summary

Use a verified stable C3 compiler and clear names. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for source style or selecting a C3 compiler. For dependencies and checks, see [Dependencies and Checks](tooling.md).

## Rules

- **SHOULD** Use a pinned, verified stable C3 compiler release; do not silently switch versions or introduce nightly-only features.
- **SHOULD** Confirm unfamiliar syntax and standard-library APIs against the pinned release.
- **SHOULD** Use snake_case for modules, files, functions, methods, variables, fields, and macros.
- **SHOULD** Use PascalCase for types and structs, and UPPER_SNAKE_CASE for constants.
- **SHOULD** Use tabs and Allman-style braces. Use self as the method receiver name.
- **SHOULD** Choose descriptive names. Avoid unnecessary abbreviations and clever compressed expressions.
- **SHOULD** Comment on intent, invariants, ownership, lifetime, and non-obvious constraints rather than restating code.

Note: The C3 examples use the `excuse` spelling from C3 0.8.4 and later; respect the target project’s pinned release.

## Recommended Pattern

```c3
// src/products.c3
module shop::catalog @private;

const MAX_SEARCH_RESULTS = 50;

struct Product @public
{
	String id;
	String name;
	long price_cents;
}

fn Product? find_product_by_id(Product[] products, String product_id) @public
{
	foreach (product : products)
	{
		if (product.id == product_id) return product;
	}
	return NOT_FOUND~;
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Unpinned compiler | Syntax and library APIs can differ | Confirm the stable release |
| Camel case for fields | Conflicts with project naming | Use snake_case |
| Comment repeats the next line | Omits the contract | Explain constraints or lifetime |

## Checklist

- Inspect the pinned compiler version.
- Use snake_case and uppercase constants.
- Use tabs and Allman braces.
- Explain non-obvious invariants.

## References

- [C3 naming](https://c3-lang.org/language-fundamentals/naming/)
- [C3 optionals](https://c3-lang.org/language-common/optionals-essential/)
