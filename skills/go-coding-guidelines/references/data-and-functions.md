---
id: go/data-and-functions
title: "Structs, Functions, and Methods"
summary: "Represent data directly and put transformations in functions."
language: go
topic: data-and-functions
tags: [data, functions, classes]
related: [go/abstraction]
snippets: unverified
---

# Structs, Functions, and Methods

## Summary

Represent data directly and put transformations in functions. Use methods when behavior belongs to a value or resource.

## When to Use

Use this for in-memory models and calculations. For interfaces, see [Interfaces](abstraction.md).

## Rules

- **SHOULD** Use structs for data and necessary state, and ordinary functions for transformations independent of state.
- **SHOULD** Use methods for type-owned behavior, mutation, invariants, resources, or interface implementation.
- **SHOULD** Use value receivers for suitable small value types; use pointer receivers for mutation or noncopyable state such as mutexes, consistently per type.
- **SHOULD** Make zero values useful; use constructors only for initialization, validation, or resource acquisition.
- **AVOID** Avoid automatic accessors, needless indirection, and hidden global mutable state.

## Recommended Pattern

```go
// orders/totals.go
package orders

type OrderLine struct {
    ProductID      string
    Quantity       int64
    UnitPriceCents int64
}

// OrderTotalCents sums validated lines whose totals fit in int64.
func OrderTotalCents(lines []OrderLine) int64 {
    var total int64
    for _, line := range lines {
        total += line.Quantity * line.UnitPriceCents
    }
    return total
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Static service wrapper | Adds no state or invariant | Use a function |
| Copied mutex | Breaks synchronization | Use a pointer receiver |
| Mandatory constructor | Makes useful zero values harder to use | Construct only when needed |

## Checklist

- Keep transformation inputs explicit.
- Check whether a method owns behavior.
- Match receivers to mutation and copy semantics.
- Document any arithmetic bounds.

## References

- [Effective Go](https://go.dev/doc/effective_go)
