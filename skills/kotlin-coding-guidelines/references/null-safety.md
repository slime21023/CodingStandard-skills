---
id: kotlin/null-safety
title: Null Safety
summary: Declare nullable types only for real absence and make both the present and absent cases explicit.
language: kotlin
topic: null-safety
tags: [null-safety, types, control-flow]
related: [kotlin/errors, kotlin/control-flow]
snippets: unverified
---

# Null Safety

## Summary

A nullable type declares that missing data is legitimate. Make the choice between handling absence and rejecting invalid input obvious, and resolve platform-type uncertainty before it reaches the rest of the Kotlin code.

## When to Use

Use this topic for optional values, nullable receiver chains, safe casts, or Java platform types. For choosing what to catch or how to handle coroutine cancellation, see [Exceptions and Preconditions](errors.md).

## Rules

- **MUST** declare `T?` only when absence is a valid state; do not arbitrarily relax non-null parameters or properties to nullable types.
- **MUST** define what happens when a nullable value is present and when it is absent. Do not rely on unchecked assumptions that it is non-null.
- **MUST** not use `!!` to conceal an unverified source of nulls.
- **SHOULD** choose the clearest of `?.`, `?:`, a smart cast, an explicit `if`, or an early return.
- **SHOULD** use `as?` for a safe cast and use `as` only when the type contract is established by an understandable precondition.
- **SHOULD** assign Java platform types such as `String!` to an explicit `T` or `T?` at the boundary according to the actual Java contract. Do not let unknown nullability spread through the Kotlin code.
- **SHOULD** prefer a direct Elvis expression or `if` for a simple null check or early return instead of reaching for `?.let` by default.
- **SHOULD** introduce meaningful intermediate values when a safe-call chain mixes transformations, side effects, defaults, and exceptions.
- **SHOULD** use `requireNotNull` when the caller is responsible for supplying a non-null value, and `checkNotNull` when the value reflects a runtime state invariant. Do not treat them as interchangeable to save a line.

Exceptions: Use `!!` only if a clear, maintainable invariant guarantees non-nullness and the reason is apparent in nearby code.

## Recommended Pattern

Reading a shipping city can treat an absent order or address as normal. An operation requiring a shippable order can reject an argument that lacks its address.

```kotlin
// src/main/kotlin/shop/orders/ShippingCity.kt
package shop.orders

data class Address(val city: String)
data class Order(val id: String, val shippingAddress: Address?)

fun shippingCity(order: Order?): String {
    val address = order?.shippingAddress ?: return "Missing address"
    return address.city
}

fun requireShippingAddress(order: Order): Address =
    requireNotNull(order.shippingAddress) { "Order ${order.id} requires a shipping address" }
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| `T?` where absence is invalid | Callers must handle a state the API should not permit. | Declare `T` and enforce the contract at the boundary. |
| `shippingAddress!!` | The call may fail without saying whether absence was expected. | Use an explicit absent branch or the correct precondition check. |
| `?.let` around a null guard | A trivial branch acquires a nested scope. | Use `?: return` or a direct `if` instead. |
| A Java platform type propagates past an adapter | Its apparent nullability is not guaranteed. | Declare `T` or `T?` explicitly where the value enters Kotlin. |
| `checkNotNull` for bad caller input | The exception misrepresents a caller error as invalid internal state. | Use `requireNotNull` for the caller precondition. |

## Checklist

- Distinguish nullable absence from invalid input in each contract.
- Show the behavior of both the present and absent paths.
- Resolve unverified Java nullability at the API boundary.
- Prefer a direct Elvis guard or `if` for straightforward null checks.
- Check that each assertion matches either a caller precondition or a state invariant.

## Related

- [Exceptions and Preconditions](errors.md): use the same input-versus-state distinction for non-null conditions and other preconditions.
- [Control Flow](control-flow.md): combine nullable values with guards and status branches.

## References

- [Kotlin Null Safety](https://kotlinlang.org/docs/null-safety.html)
- [Kotlin Exceptions](https://kotlinlang.org/docs/exceptions.html)
