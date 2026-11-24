---
id: kotlin/control-flow
title: Control Flow
summary: Use traceable branches and loops, exhaustive state handling, and guards that make the normal path easy to see.
language: kotlin
topic: control-flow
tags: [control-flow, functions, review]
related: [kotlin/types, kotlin/null-safety, kotlin/collections-and-idioms]
snippets: unverified
---

# Control Flow

## Summary

Compressed branches and loops can hide both the path through the code and its side effects. Use exhaustive `when` expressions for finite states and guard clauses when they make the main path easier to follow.

## When to Use

Use this topic when writing a branch, loop, or early exit, or when a value is assembled from several branches. For choosing between an enum and a sealed type, see [Variables, Types, and Declarations](types.md).

## Rules

- **MUST** use explicit, traceable branches and loops. Do not hide significant side effects or control flow in compressed expressions.
- **SHOULD** use `if` for two branches and `when` for several discrete cases, without making a simple case verbose for the sake of form.
- **SHOULD** use exhaustive `when` for an `enum` or sealed type when all variants matter. Do not add a catch-all `else` that silently handles new variants.
- **SHOULD** use guards with early `return`, `continue`, or `break` to reduce unnecessary nesting. Keep a structured branch when an early exit makes the flow harder to understand.
- **SHOULD** use `indices`, `..<`, or `until` when indices are needed rather than hand-writing easily misread boundary arithmetic.
- **SHOULD** prefer `for` when the loop needs `break`, `continue`, or complex branching.
- **SHOULD** make the value produced by each branch immediately apparent when using `if`, `when`, or `try` as an expression.
- **SHOULD** avoid piling nested conditions and exception handling into one expression. Use local variables and blocks as needed.
- **REVIEW SIGNAL** When nesting increases, check whether an early exit, clearer conditions, or a named value would make the flow easier to follow. Do not set a maximum nesting depth.

## Recommended Pattern

A new `OrderStatus` requires a new label. In `shippingLabel`, the first guard handles cancellation; the second handles a missing address before formatting the normal result.

```kotlin
// src/main/kotlin/shop/orders/ShippingLabels.kt
package shop.orders

enum class OrderStatus { Pending, Paid, Shipped, Cancelled }

data class Address(val city: String)

data class Order(
    val id: String,
    val status: OrderStatus,
    val shippingAddress: Address?,
)

fun orderStatusLabel(status: OrderStatus): String =
    when (status) {
        OrderStatus.Pending -> "Pending"
        OrderStatus.Paid -> "Paid"
        OrderStatus.Shipped -> "Shipped"
        OrderStatus.Cancelled -> "Cancelled"
    }

fun shippingLabel(order: Order): String {
    if (order.status == OrderStatus.Cancelled) return "Cancelled"
    val address = order.shippingAddress ?: return "Missing address"
    return "${address.city}: ${order.id}"
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Generic `else` on a finite state type | New states silently receive the fallback. | Enumerate the states in an exhaustive `when`. |
| Happy path deep inside several conditions | The exceptional cases obscure the normal one. | Use guards where they make the main path clearer. |
| Hand-written `size - 1` index bound | Off-by-one errors are harder to spot. | Use `indices` or a standard half-open range. |
| Nested `try` and conditions in a single expression | The result and side effects are difficult to trace. | Break the expression into named values or clear blocks. |

## Checklist

- Choose the simplest branch construct that expresses the cases.
- Enumerate all variants when a finite-state branch must be exhaustive.
- Make loop exits and side effects apparent.
- Use Kotlin range operations for indexed loops.
- Review nesting for clarity instead of applying a fixed depth limit.

## Related

- [Variables, Types, and Declarations](types.md): choose a type that represents finite states explicitly.
- [Null Safety](null-safety.md): pick a direct nullable guard and show the absent path.
- [Collections and Idioms](collections-and-idioms.md): distinguish collection transforms from effectful iteration.

## References

- [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- [Kotlin Idioms](https://kotlinlang.org/docs/idioms.html)
