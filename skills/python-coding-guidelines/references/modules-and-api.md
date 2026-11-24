---
id: python/modules-and-api
title: "Modules, Packages, and Public APIs"
summary: "Keep feature modules cohesive and type their public contracts."
language: python
topic: modules-and-api
tags: [modules, public-api, types]
related: [python/abstraction]
snippets: unverified
---

# Modules, Packages, and Public APIs

## Summary

Keep feature modules cohesive and type their public contracts. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when organizing a package or exposing an operation. For abstraction and metaprogramming, see [Abstraction and Metaprogramming](abstraction.md).

## Rules

- **SHOULD** Organize by feature. Keep simple functionality in simple modules and split only when responsibilities justify it.
- **AVOID** Avoid default `controllers/services/repositories/interfaces` layering, circular imports, hidden initialization, and catch-all `utils.py` files.
- **SHOULD** Prefer `src/` layout for installable packages; simple scripts may stay flat.
- **SHOULD** Type all public function parameters and returns, plus important internal functions.
- **SHOULD** Mark implementation details with `_`; expose stable package APIs explicitly in `__init__.py` as useful.
- **SHOULD** Use `__all__` to clarify exports when appropriate; it is not access control.
- **AVOID** Avoid exposing mutable internal state and unnecessary third-party types in public interfaces.
- **SHOULD** Prefer `list[str]`, `dict[str, int]`, and `T | None`; minimize `Any`, `cast`, and type-checking suppressions.
- **SHOULD** Treat external files, JSON, CLI arguments, and network payloads as untrusted until validated.

## Recommended Pattern

```python
# src/shop/orders/placement.py
from collections.abc import Callable


def place_order(order_id: str, submit: Callable[[str], None]) -> None:
    """Submit an order ID after removing surrounding whitespace."""
    submit(_normalize_id(order_id))


def _normalize_id(order_id: str) -> str:
    return order_id.strip()
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Default service layers | Split a simple feature across files | Keep related behavior together |
| Imported module performs I/O | Surprises consumers | Move initialization to an explicit entry |
| Untrusted payload cast | Does not validate the data | Check the shape at runtime |

## Checklist

- Keep the public operation small.
- Type parameters and return values.
- Hide implementation-only state.
- Preserve existing imports and public contracts.

## References

- [PEP 8](https://peps.python.org/pep-0008/)
- [Typing](https://docs.python.org/3/library/typing.html)
