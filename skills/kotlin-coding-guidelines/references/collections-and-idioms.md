---
id: kotlin/collections-and-idioms
title: Collections and Idioms
summary: Use familiar Kotlin collection operations and syntax when they make data transformations and effects clearer.
language: kotlin
topic: collections-and-idioms
tags: [collections, data, functions]
related: [kotlin/control-flow, kotlin/lambdas-and-scope-functions, kotlin/types]
snippets: unverified
---

# Collections and Idioms

## Summary

Use standard collection operations to express data transformations and ordinary loops to make effects visible. Choose Kotlin idioms for their meaning, not for how many characters they save.

## When to Use

Use this topic when transforming collections, choosing eager or lazy evaluation, or introducing destructuring, extensions, or overloaded operators. For more on guard clauses and loop exits, see [Control Flow](control-flow.md).

## Rules

- **MUST** make collection results and side effects distinguishable. Do not surprise readers with deferred execution or repeated traversal.
- **SHOULD** use standard operations such as `map`, `filter`, `associate`, and `groupBy` for clear transformations or selections.
- **SHOULD** prefer a `for` loop over `forEach` when iteration is mainly for effects such as changing external state.
- **SHOULD** keep each step of a collection chain easy to follow. When multiple transforms are mixed with effects and branches, introduce named intermediate results or use a regular loop.
- **SHOULD** use `Sequence` only when input size, lazy evaluation, or avoiding intermediate collections provides a real benefit; it is not the default just for looking more idiomatic.
- **MUST** not use operator overloading, `infix`, or obscure extension names in ways that mislead a typical reader about behavior.
- **SHOULD** use string templates instead of simple concatenation. Use `trimIndent()` or `trimMargin()` for multiline text as appropriate.
- **SHOULD** use destructuring only when the components' meanings are clear. Access properties by name if the meaning of `componentN` is not obvious.
- **SHOULD** write extensions for behavior that genuinely belongs to the receiver; avoid an API that resembles an existing member but behaves differently.
- **SHOULD** use `typealias` to name repeated, hard-to-read types, not to put another name around every ordinary type.
- **SHOULD** overload an operator only when its meaning is intuitive in the domain. Predictability matters more than brevity.
- **SHOULD** use familiar features such as data classes, string templates, ranges, and smart casts where they help. Do not treat shorter syntax as a measure of quality.

## Recommended Pattern

For a large catalog, filter and map through a sequence so there is no intermediate list of active products. Collect the sequence before returning, use an explicit loop for notifications, and destructure an entry whose component roles are clear.

```kotlin
// src/main/kotlin/shop/catalog/CatalogViews.kt
package shop.catalog

data class Product(
    val id: String,
    val name: String,
    val priceCents: Long,
    val isActive: Boolean,
)

fun activeProductNames(products: List<Product>): List<String> =
    products.asSequence()
        .filter { it.isActive }
        .map { it.name }
        .toList()

data class Customer(val id: String, val acceptsUpdates: Boolean)

fun notifyCustomers(
    customers: List<Customer>,
    message: String,
    sendNotification: (Customer, String) -> Unit,
) {
    for (customer in customers) {
        if (!customer.acceptsUpdates) continue
        sendNotification(customer, message)
    }
}

fun formatProductStock(entry: Map.Entry<String, Int>): String {
    val (productId, quantity) = entry
    return "$productId: $quantity in stock"
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Notifications sent inside `map` | A transform hides a side effect. | Use a loop for notifications and keep the transform separate. |
| A reused lazy sequence performs work twice | Each traversal can repeat the computation and its effects. | Materialize once at the appropriate boundary or avoid deferring side effects. |
| Several ambiguous components destructured at once | Meaning depends on knowing their positions. | Read the named properties instead. |
| An overloaded operator changes external state unexpectedly | Ordinary operator syntax promises an operation readers already understand. | Use a named operation that communicates its effect. |

## Checklist

- Identify which operations return transformed data and which perform effects.
- Make evaluation timing and repeated traversal explicit.
- Use a sequence only when laziness or intermediate allocation matters.
- Name destructured components for their actual roles.
- Confirm extensions, operators, and `infix` calls behave as their spelling suggests.

## Related

- [Control Flow](control-flow.md): make effects and loop exits straightforward.
- [Lambdas and Scope Functions](lambdas-and-scope-functions.md): keep collection lambdas and their effects understandable.
- [Variables, Types, and Declarations](types.md): distinguish read-only collection interfaces from immutability.

## References

- [Kotlin Idioms](https://kotlinlang.org/docs/idioms.html)
- [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
