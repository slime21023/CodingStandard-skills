---
id: kotlin/data-and-functions
title: Functions
summary: Give each function a clear purpose and expose its inputs, return contract, and effects at the call site.
language: kotlin
topic: data-and-functions
tags: [data, functions, public-api, review]
related: [kotlin/naming-and-formatting, kotlin/types, kotlin/control-flow]
snippets: unverified
---

# Functions

## Summary

A function should make its main purpose and observable behavior easy to understand from its declaration and its calls. Use an expression body for a direct computation and a block when explicit steps help, rather than optimizing for line count.

## When to Use

Use this topic to design signatures, argument ordering, default values, or function bodies. For casing and the requirement that names match behavior, see [Formatting and Naming](naming-and-formatting.md).

## Rules

- **MUST** make caller-visible preconditions, the meaning of the return value, and observable behavior clear through the signature, names, and any necessary documentation.
- **SHOULD** give each function one readily described main purpose. Consider splitting unrelated stages, but keep them together if separation would only make the reader jump between functions.
- **SHOULD** use an expression body for a single clear operation. Use a block body for several steps, branching, or side effects.
- **SHOULD** omit `Unit` return types unless an explicit type or interoperability requires them.
- **SHOULD** use default arguments instead of overloads that differ only in supplied defaults.
- **MUST** make parameter names match their meaning and avoid positional calls that obscure what their arguments denote.
- **SHOULD** use named arguments for adjacent Booleans, numbers, or other arguments of the same type that serve different roles.
- **SHOULD** avoid using a Boolean parameter alone to switch between substantially different behaviors. Use clearer function names or types at the API level when appropriate.
- **SHOULD** order parameters by their role, typically putting primary inputs before optional settings.
- **SHOULD** keep public return types stable and understandable; do not let callers depend on an accidentally inferred concrete type.
- **REVIEW SIGNAL** In a long function, check whether its main purpose and the way its data changes are still easy to follow.
- **REVIEW SIGNAL** With many parameters, check whether each parameter's role is evident.
- **REVIEW SIGNAL** Across several layers of helpers, check that each abstraction reduces cognitive load rather than just forwarding the call.
- **REVIEW SIGNAL** When one line does many operations, consider whether named intermediate values would make it easier to read.

Note: These review signals are not violations or hard limits. Judge whether a reader can see the inputs, main steps, output, and side effects without effort, not how many lines the function has.

Exceptions: Use overloads for defaults when the Java interoperability contract calls for them.

## Recommended Pattern

`orderTotalCents` states what it returns and performs a single pure computation. This example assumes each line total and the sum fit in a `Long`.

```kotlin
// src/main/kotlin/shop/orders/OrderTotals.kt
package shop.orders

data class OrderLine(
    val productId: String,
    val quantity: Int,
    val unitPriceCents: Long,
)

fun orderTotalCents(lines: List<OrderLine>): Long =
    lines.sumOf { line -> line.quantity * line.unitPriceCents }
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Several unlabeled numeric arguments | Readers cannot tell quantity from price. | Use meaningful parameter names and named arguments. |
| A Boolean flag selects unrelated operations | The call hides what will actually happen. | Give the operations distinct names or encode the choice in a suitable type. |
| Several overloads that only add defaults | The same behavior is scattered across declarations. | Prefer default arguments unless the interop contract requires overloads. |
| One tall chain of forwarding helpers | Readers must navigate without learning new information. | Keep related steps together unless the abstraction clarifies them. |
| A compact expression that mixes steps and effects | The order and outcome of work are easy to miss. | Use a block and name the important intermediate values. |

## Checklist

- State caller-visible preconditions, outputs, and effects in the function contract.
- Choose an expression or block body based on the work it needs to show.
- Label arguments that are easy to confuse at the call site.
- Put primary inputs before optional settings where practical.
- Expose a stable public return type instead of an accidental implementation type.
- Review length and abstraction for clarity rather than enforcing counts.

## Related

- [Formatting and Naming](naming-and-formatting.md): name functions for their actual effects.
- [Variables, Types, and Declarations](types.md): select explicit types and minimum visibility for declarations.
- [Control Flow](control-flow.md): make the branches of a computation or command easy to follow.

## References

- [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- [Kotlin Idioms](https://kotlinlang.org/docs/idioms.html)
