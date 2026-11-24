---
id: c3/data-and-functions
title: "Data and Control Flow"
summary: "Use simple value types and keep computation in ordinary functions."
language: c3
topic: data-and-functions
tags: [data, functions, control-flow]
related: [c3/abstraction]
snippets: unverified
---

# Data and Control Flow

## Summary

Use simple value types and keep computation in ordinary functions. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for domain values and ordinary transformations. For generics, interfaces, and macros, see [Generics, Interfaces, and Macros](abstraction.md).

## Rules

- **SHOULD** Prefer simple structs and ordinary functions. Use methods only for operations closely tied to a receiver value.
- **SHOULD** Keep structs cohesive; prefer value semantics where appropriate and avoid hidden mutable global state.
- **MUST** Do not emulate complex class hierarchies with struct subtyping.
- **SHOULD** Keep functions focused. Prefer guard conditions and early returns to deeply nested statements.
- **SHOULD** Treat more than three nesting levels as a refactoring signal, not an automatic prohibition.
- **MUST** Do not use nested ternary expressions. Use named intermediate variables for complex conditions.
- **SHOULD** Make mutation and side effects apparent. Do not generate meaningless getter/setter layers.

## Recommended Pattern

```c3
// src/totals.c3
module shop::orders @private;

struct OrderLine @public
{
	String product_id;
	long quantity;
	long unit_price_cents;
}

// Call with validated lines whose products and sum fit in long.
fn long order_total_cents(OrderLine[] lines) @public
{
	long total = 0;
	foreach (line : lines)
	{
		total += line.quantity * line.unit_price_cents;
	}
	return total;
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Class hierarchy with subtyping | Obscures value semantics | Use cohesive plain structs |
| Nested ternary | Hides branches | Name a condition and use a guard |
| Hidden global state | Makes effects nonlocal | Pass explicit inputs |

## Checklist

- Keep struct fields cohesive.
- Keep transformations independent of global state.
- Review deep nesting without imposing a hard limit.
- Make effects and valid arithmetic ranges explicit.

## References

- [C3 language reference](https://c3-lang.org/all/)
