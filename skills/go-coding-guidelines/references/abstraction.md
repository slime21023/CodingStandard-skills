---
id: go/abstraction
title: "Interfaces"
summary: "Define interfaces at consumers with genuine substitution needs."
language: go
topic: abstraction
tags: [interfaces, public-api]
related: [go/data-and-functions]
snippets: unverified
---

# Interfaces

## Summary

Define interfaces at consumers with genuine substitution needs. A payment provider is a real runtime boundary; a pure calculation usually is not.

## When to Use

Use this when a caller needs interchangeable behavior. For structs, functions, and methods, see [Structs, Functions, and Methods](data-and-functions.md).

## Rules

- **MUST** Prefer concrete types until an actual consumer needs a behavioral contract.
- **SHOULD** Keep interfaces small and near their consumers; implementations normally return concrete types.
- **AVOID** Avoid one interface per struct, IUserService or UserServiceImpl naming, and speculative adapters.

## Recommended Pattern

```go
// orders/checkout.go
package orders

import "context"

type PaymentGateway interface {
    Charge(ctx context.Context, orderID string, amountCents int64) error
}

func Checkout(ctx context.Context, gateway PaymentGateway, orderID string, amountCents int64) error {
    return gateway.Charge(ctx, orderID, amountCents)
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Provider-owned mega-interface | Couples checkout to unused methods | Define just Charge at the consumer |
| An interface for every struct | Adds navigation without substitution | Return concrete implementations |
| Test-only speculative adapter | Reshapes stable production code | Replace only real boundaries |

## Checklist

- Identify a real substitution boundary.
- Keep the interface near its consumer.
- Declare only methods the consumer uses.
- Keep concrete provider constructors concrete.

## References

- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
