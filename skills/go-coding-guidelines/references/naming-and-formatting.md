---
id: go/naming-and-formatting
title: "Naming and Formatting"
summary: "Use idiomatic Go names and gofmt."
language: go
topic: naming-and-formatting
tags: [naming, formatting]
related: [go/tooling]
snippets: unverified
---

# Naming and Formatting

## Summary

Use idiomatic Go names and gofmt. Let formatting tools handle layout so reviewers can focus on behavior.

## When to Use

Use this when choosing identifiers and formatting code. For formatting and checks, see [Formatting and Checks](tooling.md).

## Rules

- **MUST** Format touched files with gofmt; use exported PascalCase, unexported camelCase, and conventional initialisms such as ID and HTTP.
- **SHOULD** Use concise lowercase package names without underscores; avoid stutter such as user.NewUser.
- **SHOULD** Match name clarity to scope; i, err, ctx, db, r, w, and short receivers are fine in obvious local contexts.
- **AVOID** Avoid cryptic abbreviations, verbose names, and generic common, util, or helpers packages.

## Recommended Pattern

```go
// catalog/product.go
package catalog

const maxSearchResults = 50

type Product struct {
    ID         string
    Name       string
    PriceCents int64
}

// FindProductByID returns the matching product, if any.
func FindProductByID(products []Product, productID string) (Product, bool) {
    for _, product := range products {
        if product.ID == productID {
            return product, true
        }
    }
    return Product{}, false
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Id or Http | Breaks initialism consistency | Write ID or HTTP |
| catalog.CatalogProduct | Repeats package context | Use catalog.Product |
| util package | Hides its responsibility | Name the actual capability |

## Checklist

- Format touched files with gofmt.
- Check exported and unexported casing.
- Preserve standard initialisms.
- Remove package-name stutter.

## References

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
