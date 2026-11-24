---
id: kotlin/errors
title: Exceptions and Preconditions
summary: Express caller preconditions and runtime failures precisely, and preserve coroutine cancellation.
language: kotlin
topic: errors
tags: [errors, exceptions, cancellation, null-safety]
related: [kotlin/null-safety, kotlin/data-and-functions]
snippets: unverified
---

# Exceptions and Preconditions

## Summary

Choose failures that describe what actually went wrong, and catch an exception only when the code can do something meaningful with it. Keep ordinary absence distinct from failure, and let cancellation propagate from suspending code.

## When to Use

Use this topic when checking caller input or internal state, handling an exception, or defining what a suspending function returns when data is missing. For designing a nullable contract or choosing a non-null assertion, see [Null Safety](null-safety.md).

## Rules

- **MUST** not silently swallow exceptions. If a catch does not rethrow, handle the failure in a clear and reasonable way.
- **MUST** use an exception that represents the real failure; do not obscure the cause with an unrelated exception type.
- **MUST** rethrow `CancellationException` if caught in coroutine code. `catch (e: Exception)`, `catch (e: Throwable)`, and `runCatching` can catch cancellation; do not turn it into a normal result and break structured concurrency.
- **SHOULD** use `require` for caller input preconditions and `check` for runtime state invariants. For their null-specific forms, apply the same distinction in [Null Safety](null-safety.md).
- **SHOULD** catch the specific exceptions the code can actually handle. Do not catch everything unconditionally just to return an ambiguous default.
- **SHOULD** use an explicit nullable return or another suitable Kotlin type when absence is normal; do not use exceptions for normal branches without a reason.
- **SHOULD** use a `try` expression for computing a single value when the result is clear. Use an explicit block when there are several cleanup actions, branches, or side effects.

Note: There is no requirement that all functions use `Result<T>`, custom exceptions, or another uniform failure model. Choose according to the API contract and project design.

## Recommended Pattern

The discount API rejects invalid caller input and permits a discount equal to the price. The catalog adapter maps only the source's documented missing-product exception to `null`; cancellation and unexpected failures still propagate.

```kotlin
// src/main/kotlin/shop/catalog/Catalog.kt
package shop.catalog

import kotlin.coroutines.cancellation.CancellationException

data class Product(val id: String, val name: String, val priceCents: Long)

fun applyDiscount(product: Product, amountCents: Long): Product {
    require(amountCents >= 0) { "Discount must be non-negative" }
    require(amountCents <= product.priceCents) { "Discount exceeds the price" }
    return product.copy(priceCents = product.priceCents - amountCents)
}

class ProductNotFoundException(id: String) : Exception("Product $id was not found")

/** Adapts a catalog fetch that reports absent IDs with [ProductNotFoundException]. */
class Catalog(private val fetchProduct: suspend (String) -> Product) {
    suspend fun loadProductOrNull(id: String): Product? {
        require(id.isNotBlank()) { "Product ID must not be blank" }
        return try {
            fetchProduct(id)
        } catch (cancelled: CancellationException) {
            throw cancelled
        } catch (notFound: ProductNotFoundException) {
            null
        }
    }
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| A broad catch returns `null` | Missing data, a broken dependency, and cancellation look the same. | Catch only the known absence case; propagate other failures. |
| `runCatching` around a suspending operation with an unconditional fallback | Cancellation can disappear into a normal result. | Preserve `CancellationException` instead of handling it as failure. |
| `check` rejects an invalid discount argument | It misidentifies a caller error as a broken state invariant. | Use `require` for invalid input. |
| Unrelated generic exception in place of a meaningful cause | Callers and diagnostics lose useful failure information. | Report the actual failure and retain its cause when translating. |

## Checklist

- Distinguish caller preconditions from program-state invariants.
- Check that exception types match the actual failure.
- Catch only failures that can be handled meaningfully.
- Preserve `CancellationException` across catches and result conversions.
- Represent ordinary absence explicitly rather than as an unexpected exception.

## Related

- [Null Safety](null-safety.md): handle normal absence and choose the appropriate null-specific precondition.
- [Functions](data-and-functions.md): show relevant preconditions and outputs in the function contract.

## References

- [Kotlin Exceptions](https://kotlinlang.org/docs/exceptions.html)
- [Kotlin Null Safety](https://kotlinlang.org/docs/null-safety.html)
