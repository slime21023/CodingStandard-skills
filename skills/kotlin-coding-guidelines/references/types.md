---
id: kotlin/types
title: Variables, Types, and Declarations
summary: Make reassignment, visibility, and data semantics clear by choosing the narrowest suitable Kotlin declaration.
language: kotlin
topic: types
tags: [types, data, classes, public-api]
related: [kotlin/control-flow, kotlin/data-and-functions]
snippets: unverified
---

# Variables, Types, and Declarations

## Summary

Choose `val` or `var` based on whether the binding must be reassigned, and show mutation capabilities and public types explicitly. Pick ordinary classes, data classes, sealed types, enums, and objects for their semantics rather than for brevity.

## When to Use

Use this topic when deciding what may change, declaring a value type, or modeling finite states. For branching over those states, see [Control Flow](control-flow.md).

## Rules

- **MUST** make `val` and `var` reflect whether reassignment is needed; do not declare everything `var` for convenience.
- **SHOULD** start with `val` and choose `var` only when the code actually reassigns the binding.
- **SHOULD** use `MutableList`, `MutableSet`, or `MutableMap` only when contents need to change through that reference; otherwise use the read-only `List`, `Set`, or `Map` interface.
- **SHOULD** infer a local type when its initializer makes the type clear; write it explicitly when the initializer or generic inference is hard to follow.
- **SHOULD** write explicit return types for externally visible functions and explicit types for externally visible properties and potentially ambiguous declarations. You can omit the type of a short, self-explanatory private function.
- **SHOULD** avoid broad use of `Any`, unchecked casts, or unnecessary explicit casts just to sidestep type design.
- **SHOULD** use `lateinit` or `lazy` only when delayed initialization is necessary; initialize directly at declaration when possible.
- **SHOULD** declare the minimum necessary visibility rather than accidentally making a declaration accessible more widely.
- **MUST** match the declaration form to the class's semantics; do not choose a shorter form that gives it inappropriate behavior.
- **SHOULD** use `data class` for value-like data suited to structural comparison. The generated `equals`, `hashCode`, `toString`, and `copy` are based on primary-constructor properties.
- **SHOULD** use `sealed class` or `sealed interface` for a finite set of mutually exclusive state variants where that representation helps; use `enum class` for a simple fixed set of constants. Do not introduce a hierarchy simply because there is more than one state.
- **SHOULD** use `object` when a single instance is needed; use a top-level function for stateless behavior when no wrapper class is needed.
- **SHOULD** keep the primary constructor, property initializers, and `init` blocks easy to trace. In more complex initialization, name intermediate values for what they mean.

Note: `val` prevents reassignment; it does not make the object immutable. Read-only collection interfaces do not guarantee deep immutability or prevent mutation through another reference. A data class's `copy()` is shallow and does not copy the contents of mutable references.

## Recommended Pattern

`OrderLine` has structural equality, each order state carries only its own fields, and `selectedIndex` can change only through `selectLine`.

```kotlin
// src/main/kotlin/shop/orders/OrderState.kt
package shop.orders

data class OrderLine(
    val productId: String,
    val quantity: Int,
    val unitPriceCents: Long,
)

sealed interface OrderState {
    data object Pending : OrderState
    data class Paid(val paidAtMillis: Long) : OrderState
    data class Cancelled(val reason: String) : OrderState
}

class OrderDraft(private val lines: List<OrderLine>) {
    var selectedIndex: Int? = null
        private set

    fun selectLine(index: Int) {
        require(index in lines.indices) { "No order line at index $index" }
        selectedIndex = index
    }
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| `var` on a binding that never changes | The declaration promises flexibility the code does not need. | Use `val`. |
| A `List` reference assumed to be immutable | Another holder can still mutate the backing collection. | Make the intended ownership and mutation behavior explicit. |
| An inferred public collection subtype | Callers may depend on an accidental implementation detail. | Declare the intended public type explicitly. |
| `data class` for an object that needs identity semantics | Generated structural equality describes the wrong behavior. | Use the declaration form that fits the object. |
| `copy()` assumed to duplicate mutable fields | Both copies can still point to the same mutable data. | Account for aliasing or copy that data explicitly when needed. |

## Checklist

- Mark a binding `var` only where it needs to be reassigned.
- Expose read-only collection interfaces when callers do not need mutation.
- Write explicit types for public or ambiguous declarations.
- Narrow visibility to what callers actually need.
- Verify that the generated behavior of a data class fits the type's contract.
- Choose a sealed type, enum, or object for its semantics, not its length.

## Related

- [Control Flow](control-flow.md): branch exhaustively over a finite set of states.
- [Functions](data-and-functions.md): keep public return types stable and understandable.

## References

- [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- [Kotlin Idioms](https://kotlinlang.org/docs/idioms.html)
