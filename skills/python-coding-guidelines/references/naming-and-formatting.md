---
id: python/naming-and-formatting
title: "Naming and Readability"
summary: "Use names that explain what values and operations mean."
language: python
topic: naming-and-formatting
tags: [naming, formatting, control-flow]
related: [python/errors]
snippets: unverified
---

# Naming and Readability

## Summary

Use names that explain what values and operations mean. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when naming or simplifying Python code. For result and error boundaries, see [Result and Error Boundaries](errors.md).

## Rules

- **SHOULD** Follow PEP 8: `snake_case` for variables/functions/modules; `PascalCase` for classes/type aliases; `UPPER_SNAKE_CASE` for constants; `_name` for internal members.
- **SHOULD** Use complete, meaningful names; avoid unnecessary abbreviations and built-in name shadowing.
- **SHOULD** Prefer guard clauses and early returns over deep nesting.
- **AVOID** Avoid nested conditional expressions, complex one-line comprehensions, and hidden side effects.
- **SHOULD** Add docstrings to clarify public contracts, surprising behavior, and non-obvious constraints—not to restate obvious code.

## Recommended Pattern

```python
# src/shop/catalog/products.py
from dataclasses import dataclass

MAX_SEARCH_RESULTS = 50


@dataclass(frozen=True, slots=True)
class Product:
    product_id: str
    name: str
    price_cents: int


def find_product_by_id(products: list[Product], product_id: str) -> Product | None:
    for product in products:
        if product.product_id == product_id:
            return product
    return None
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| prod_id | Obscures the domain name | Write product_id |
| list as a variable | Shadows the built-in type | Name the collection products |
| Nested conditional expression | Hides the main branch | Use a guard |

## Checklist

- Use PEP 8 casing.
- Name parameters for their role.
- Keep the guard path clear.
- Document the contract rather than the implementation.

## References

- [PEP 8](https://peps.python.org/pep-0008/)
