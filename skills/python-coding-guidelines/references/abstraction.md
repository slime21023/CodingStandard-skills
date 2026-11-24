---
id: python/abstraction
title: "Abstraction and Metaprogramming"
summary: "Add an abstraction only for real substitution or type relationships."
language: python
topic: abstraction
tags: [interfaces, generics, metaprogramming]
related: [python/modules-and-api]
snippets: unverified
---

# Abstraction and Metaprogramming

## Summary

Add an abstraction only for real substitution or type relationships. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when multiple payment providers must satisfy the same checkout boundary. For modules, packages, and public apis, see [Modules, Packages, and Public APIs](modules-and-api.md).

## Rules

- **SHOULD** Follow Concrete Types First.
- **SHOULD** Introduce Protocol only for real substitutability needs, not single implementations.
- **SHOULD** Use generics only when expressing meaningful relationships between types.
- **SHOULD** Keep decorators simple, transparent, and compatible with introspection/type signatures.
- **AVOID** Avoid unnecessary reflection, metaclasses, monkey patching, and runtime code generation.
- **MUST** Do not introduce design patterns solely for hypothetical future extensibility.

## Recommended Pattern

```python
# src/shop/billing/checkout.py
from typing import Protocol


class PaymentGateway(Protocol):
    def charge(self, order_id: str, amount_cents: int) -> str:
        """Charge an order and return a receipt ID."""


def checkout(gateway: PaymentGateway, order_id: str, amount_cents: int) -> str:
    return gateway.charge(order_id, amount_cents)
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Protocol for a pure helper | Adds no substitution value | Keep the concrete function |
| Generic with no type relationship | Adds type arguments without guarantees | Use concrete types |
| Opaque decorator | Hides effects and signature | Keep the original contract visible |

## Checklist

- Identify a real substitution point.
- Declare the smallest interface the caller needs.
- Keep decorators transparent.
- Avoid speculative extensibility.

## References

- [Typing](https://docs.python.org/3/library/typing.html)
