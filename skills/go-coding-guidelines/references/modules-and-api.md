---
id: go/modules-and-api
title: "Packages and Public APIs"
summary: "Start with small packages and split by actual capability."
language: go
topic: modules-and-api
tags: [modules, public-api, documentation]
related: [go/abstraction]
snippets: unverified
---

# Packages and Public APIs

## Summary

Start with small packages and split by actual capability. The package boundary is a contract, not a mandatory architecture diagram.

## When to Use

Use this when exposing or relocating package behavior. For interfaces, see [Interfaces](abstraction.md).

## Rules

- **SHOULD** Organize packages around capabilities and start flat; split at meaningful boundaries.
- **SHOULD** Use internal/ when it protects an implementation detail.
- **SHOULD** Prefer the standard library and keep the exported API minimal.
- **SHOULD** Document exported APIs and explain non-obvious invariants and decisions instead of restating code.
- **AVOID** Avoid default handler/service/repository layers and circular imports.

## Recommended Pattern

```go
// orders/place.go
package orders

import "strings"

// PlaceOrder submits one order ID through the provided persistence boundary.
func PlaceOrder(orderID string, submit func(string) error) error {
    return submit(normalizeOrderID(orderID))
}

func normalizeOrderID(orderID string) string {
    return strings.TrimSpace(orderID)
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Exported normalization helper | Freezes an internal choice | Keep it package-private |
| Default layers | Split a cohesive feature | Split only as responsibilities grow |
| Circular imports | Leave ownership ambiguous | Move shared behavior to its natural owner |

## Checklist

- Name packages by capability.
- Export only caller-facing symbols.
- Document the effect of the exported operation.
- Avoid import cycles and generic dumping grounds.

## References

- [Organizing a Go module](https://go.dev/doc/modules/layout)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
