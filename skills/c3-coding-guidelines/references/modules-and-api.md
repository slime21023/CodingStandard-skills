---
id: c3/modules-and-api
title: "Modules and Public APIs"
summary: "Organize modules by responsibility and expose only intentional contracts."
language: c3
topic: modules-and-api
tags: [modules, public-api, documentation]
related: [c3/data-and-functions]
snippets: unverified
---

# Modules and Public APIs

## Summary

Organize modules by responsibility and expose only intentional contracts. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when defining or modifying module APIs. For data and control flow, see [Data and Control Flow](data-and-functions.md).

## Rules

- **SHOULD** Organize modules by feature or responsibility. Keep small projects flat and split only when needed.
- **SHOULD** Keep related data and behavior together; avoid circular dependencies and generic utility dumping grounds.
- **SHOULD** Explicitly declare a module for project source files.
- **SHOULD** Follow a private-by-default policy using module section visibility or declaration attributes as appropriate.
- **SHOULD** Mark only intentional public APIs public; document parameters, results, fault behavior, allocation, ownership, and lifetime.
- **SHOULD** Preserve stable public interfaces. Avoid exposing internal implementation details.
- **SHOULD** C3 permits import ... @public to access private declarations; do not use it to bypass a module's intended API boundary without an explicit architecture reason.

## Recommended Pattern

```c3
// src/place_order.c3
module shop::orders @private;

fn bool valid_order_id(int order_id)
{
	return order_id > 0;
}

excuse INVALID_ORDER_ID @public;

<*
@return "The accepted order number. No allocation or I/O."
@return? INVALID_ORDER_ID : "Non-positive order number."
*>
fn int? place_order(int order_id) @public
{
	if (!valid_order_id(order_id)) return INVALID_ORDER_ID~;
	return order_id;
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| No module declaration | Boundary depends on file naming | Declare the module explicitly |
| Import with @public to get a private symbol | Bypasses the contract | Use the public entry point |
| Generic utils module | Makes ownership unclear | Group by capability |

## Checklist

- Use private module defaults.
- Mark public entry points intentionally.
- Document input, output, faults, ownership, and lifetime.
- Preserve compatibility and avoid import cycles.

## References

- [C3 modules](https://c3-lang.org/language-fundamentals/modules/)
- [C3 optionals](https://c3-lang.org/language-common/optionals-essential/)
