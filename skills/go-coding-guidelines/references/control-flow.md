---
id: go/control-flow
title: "Functions and Control Flow"
summary: "Keep the successful path shallow and side effects visible."
language: go
topic: control-flow
tags: [functions, control-flow]
related: [go/errors]
snippets: unverified
---

# Functions and Control Flow

## Summary

Keep the successful path shallow and side effects visible. Guard clauses make special cases obvious without imposing hard size limits.

## When to Use

Use this for branching and iteration. For errors, see [Errors](errors.md).

## Rules

- **SHOULD** Give each function a clear responsibility and favor guards and early returns.
- **SHOULD** Use switch for clear multiway branches; omit else after a terminating branch.
- **AVOID** Avoid deep nesting, opaque conditions, unrelated mode flags, and named or naked returns without a clarity benefit.
- **AVOID** Avoid arbitrary function length quotas.

Note: Go does not enforce enum exhaustiveness. Handle every known constant and define behavior for other values.

## Recommended Pattern

```go
// orders/shipping.go
package orders

type OrderStatus uint8
const (
    Pending OrderStatus = iota
    Paid
    Shipped
    Cancelled
)

type Address struct{ City string }
type Order struct {
    ID string
    Status OrderStatus
    ShippingAddress *Address
}

func OrderStatusLabel(status OrderStatus) string {
    switch status {
    case Pending: return "Pending"
    case Paid: return "Paid"
    case Shipped: return "Shipped"
    case Cancelled: return "Cancelled"
    }
    return "Unknown status"
}

func ShippingLabel(order Order) string {
    if order.Status == Cancelled {
        return "Cancelled"
    }
    if order.ShippingAddress == nil {
        return "Missing address"
    }
    return order.ShippingAddress.City + ": " + order.ID
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Success inside multiple if blocks | Hard to follow | Use guards |
| Implicit enum exhaustiveness | Go admits other values of the underlying type | Handle unknown values explicitly |
| Named results used only to shorten returns | Hide actual output | Return values explicitly |

## Checklist

- Trace the main path without nested guards.
- List every defined order status explicitly.
- Return after each exceptional case.
- Replace unrelated boolean modes with clear operations.

## References

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
