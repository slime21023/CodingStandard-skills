---
id: kotlin/naming-and-formatting
title: Formatting and Naming
summary: Use official Kotlin formatting and names that distinguish what a declaration represents from what it does.
language: kotlin
topic: naming-and-formatting
tags: [naming, formatting]
related: [kotlin/data-and-functions, kotlin/types]
snippets: unverified
---

# Formatting and Naming

## Summary

Consistent formatting makes the structure of Kotlin code easier to follow. Choose names that tell readers what a value represents or what a call does, and reserve constant casing for data that is actually constant.

## When to Use

Use this topic when naming packages, files, declarations, and members or when formatting Kotlin source. For which parts of a function's contract to expose in its signature, see [Functions](data-and-functions.md).

## Rules

- **MUST** follow official Kotlin formatting: indent with four spaces, not tabs; put opening braces on the same line as the declaration or control statement; and omit unnecessary semicolons.
- **MUST** not sacrifice readable layout to reduce line count. Break up complex parameters, conditions, or calls, and let an official-style formatter handle the details.
- **SHOULD** avoid wildcard imports such as `import foo.*` so readers can identify the imported names.
- **SHOULD** use trailing commas in multiline declarations and collection literals; at call sites, decide by readability and project consistency.
- **MUST** name packages in lowercase without underscores, as in `com.example.textparser`.
- **MUST** use `UpperCamelCase` for classes, interfaces, objects, and type aliases, as in `TextParser` or `ParseResult`.
- **MUST** use `lowerCamelCase` for functions, properties, local variables, and parameters, as in `parseText` or `itemCount`.
- **MUST** use `UPPER_SNAKE_CASE` for `const val` and for deeply immutable `val` declarations at the top level or inside an `object`, as in `MAX_RETRIES`.
- **MUST** not use constant casing for an ordinary `val` merely because it cannot be reassigned; use `defaultTimeout`, not `DEFAULT_TIMEOUT`.
- **SHOULD** name a file after its single primary type, such as `TextParser.kt`, or use a descriptive name for several related declarations, such as `StringExtensions.kt`.
- **MUST** use names that convey meaning or behavior. Do not invent abbreviations such as `usr`, `mgr`, or `proc`, or overuse vague names such as `data`, `info`, or `util`; familiar domain abbreviations such as URL, HTTP, and ID are acceptable.
- **MUST** name functions for what they actually do; in particular, do not hide an obvious side effect or make a mutation sound like a pure query.
- **SHOULD** use naturally readable Boolean names like `isReady` or `hasNext`, verbs for actions, and nouns for types.
- **SHOULD** follow official acronym casing: two-letter acronyms can be all caps in names such as `IOStream`, while longer acronyms are ordinary words, as in `HttpClient`.

Note: For formatting details not covered here, follow the official conventions and the project's existing consistent style. Examples illustrate intent, not the only permissible form.

Exceptions: Test names, interoperability declarations, names constrained by an existing external API, and class-style factory functions that construct objects can follow the relevant Kotlin convention or external contract.

## Recommended Pattern

Use `Id` inside the lookup name and `id` for the property. Keep the immutable result limit in constant casing and use it to stop searching once the result list is full.

```kotlin
// src/main/kotlin/shop/catalog/ProductSearch.kt
package shop.catalog

private const val MAX_SEARCH_RESULTS = 50

data class Product(
    val id: String,
    val name: String,
    val priceCents: Long,
)

fun findProductById(products: List<Product>, productId: String): Product? =
    products.firstOrNull { it.id == productId }

fun searchProducts(products: List<Product>, query: String): List<Product> =
    buildList {
        for (product in products) {
            if (product.name.contains(query, ignoreCase = true)) {
                add(product)
                if (size == MAX_SEARCH_RESULTS) break
            }
        }
    }
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Complex call compressed onto one line | The argument structure gets lost. | Wrap the arguments and use the project's official-style formatter. |
| `VAL_NAME` for any `val` | Read-only bindings can still hold mutable data. | Reserve uppercase names for constants and qualifying deeply immutable values. |
| `findProductById` updates external state | A query name conceals a mutation. | Separate the query from the update or name the side effect. |
| `CatalogHTTPClient` | A long acronym in capitals obscures word boundaries. | Use `CatalogHttpClient`. |
| `import shop.catalog.*` | The source obscures which names enter scope. | Import the names the file uses. |

## Checklist

- Apply four-space indentation, official brace placement, and readable line breaks.
- Check declaration casing and reserve constant casing for the right values.
- Replace vague or invented abbreviations with names that give the reader context.
- Make each action's name agree with its observable effects.
- Use explicit imports and project-consistent trailing commas at call sites.

## Related

- [Functions](data-and-functions.md): make a named operation's contract visible at the call site.
- [Variables, Types, and Declarations](types.md): distinguish assignment restrictions from data immutability.

## References

- [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
