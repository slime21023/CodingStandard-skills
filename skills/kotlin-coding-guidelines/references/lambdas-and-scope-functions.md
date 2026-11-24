---
id: kotlin/lambdas-and-scope-functions
title: Lambdas and Scope Functions
summary: Keep lambda inputs, receiver changes, return values, and side effects easy to identify.
language: kotlin
topic: lambdas-and-scope-functions
tags: [lambdas, functions, review]
related: [kotlin/control-flow, kotlin/null-safety, kotlin/collections-and-idioms]
snippets: unverified
---

# Lambdas and Scope Functions

## Summary

Implicit parameters and receivers can make concise lambdas ambiguous. Name inputs when more than one value is in play, and choose a scope function based on both the object it operates on and what the call returns.

## When to Use

Use this topic when writing a lambda, configuring an object, or adding an effect to a value-producing call. For a straightforward nullable early return, see [Null Safety](null-safety.md).

## Rules

- **MUST** keep lambda receivers, parameters, and side effects unambiguous even if some names are omitted.
- **SHOULD** use `it` for a short, single-level lambda with a clear meaning; name parameters in nested lambdas or when several values are involved.
- **SHOULD** follow official formatting conventions for trailing lambdas and calls with a single lambda parameter. Use an explicit argument list if the trailing form makes the call's extent hard to see.
- **SHOULD** use labeled returns (`return@…`) only when local control flow needs them. If several labels interact, consider a regular loop or a separate function.
- **MUST** choose a scope function whose context object and return value match what readers expect from the operation.
- **SHOULD** prefer a plain local variable or statement if it makes the code clearer than a scope function.
- **SHOULD** avoid several implicit `this` and `it` bindings, particularly in nested `apply`, `run`, or `let` calls.
- **REVIEW SIGNAL** When scope functions are chained, nested, or used more often, check whether receiver switches, return values, and side effects are still obvious. Do not set a maximum count.

## Recommended Pattern

Use `apply` to configure the request and `also` to log without changing the returned object. Name both levels of a nested search so readers can tell a shelf from a product.

```kotlin
// src/main/kotlin/shop/catalog/CatalogRequests.kt
package shop.catalog

class CatalogRequest {
    var timeoutMillis: Long = 1_000
    var followRedirects: Boolean = false
}

fun configureAndLogCatalogRequest(log: (String) -> Unit): CatalogRequest {
    val request = CatalogRequest().apply {
        timeoutMillis = 3_000
        followRedirects = true
    }
    return request.also { configured ->
        log("Catalog request timeout: ${configured.timeoutMillis} ms")
    }
}

data class Product(val id: String, val name: String, val priceCents: Long)

fun findShelvesContainingProduct(
    shelves: List<List<Product>>,
    productId: String,
): List<List<Product>> =
    shelves.filter { shelf ->
        shelf.any { product -> product.id == productId }
    }
```

### Choosing a scope function

| Function | Common use | Context object in block | Returns |
| --- | --- | --- | --- |
| `let` | Transform a value or operate on a non-null value. | `it` | Lambda result |
| `run` | Compute a result from the receiver. | `this` | Lambda result |
| `with` | Group related operations on an existing object. | `this` | Lambda result |
| `apply` | Configure or initialize an object. | `this` | Object itself |
| `also` | Inspect or log a value or perform another side effect. | `it` | Object itself |

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Implicit `it` in both levels of a nested lambda | The innermost argument can be mistaken for the outer one. | Name both parameters. |
| `apply` chosen to compute a new result | The expression returns the original object, not the computed value. | Use an ordinary computation or a result-returning scope function. |
| Several nested scopes omit their receivers | Readers cannot tell which object a property or call belongs to. | Use named locals or make the receiver explicit. |
| Several labeled returns jump within a short chain | The exit targets cost more to trace than a straightforward loop. | Use a loop or extract a self-contained function. |

## Checklist

- Name lambda parameters when a reader might confuse them.
- Make the extent of a trailing lambda clear at the call site.
- Verify that each scope function returns the intended object or value.
- Keep context changes and side effects visible.
- Prefer plain statements over chained scopes when they read more directly.

## Related

- [Control Flow](control-flow.md): replace confusing labeled returns with explicit loop control.
- [Null Safety](null-safety.md): choose a direct null guard before reaching for `?.let`.
- [Collections and Idioms](collections-and-idioms.md): distinguish lambda-based transforms from iteration for effects.

## References

- [Kotlin Scope Functions](https://kotlinlang.org/docs/scope-functions.html)
- [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
