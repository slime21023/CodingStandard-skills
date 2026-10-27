---
name: python-coding-guidelines
description: Apply concise, data-oriented Python 3.13+ coding standards when creating, modifying, refactoring, testing, or reviewing Python code. Use for module design, public APIs, type hints, Result-based errors, dataclasses, async programming, dependencies, and Code Agent quality checks. Favor functions, immutable data, explicit error flows, minimal abstractions, and readability.
---

# Python Coding Guidelines

Apply these rules to Python code. Follow explicit user requirements and preserve established project conventions where compatible.

## Core Principles

- Prefer data structures and independent functions over classes.
- Keep data flow, dependencies, side effects, and errors explicit.
- Type public and important internal boundaries; infer obvious local types.
- Use one Result model for expected failures; preserve exceptions for unexpected errors.
- Start with concrete types and minimal abstractions.
- Prioritize readability, testability, and focused changes.
- Default to Python 3.13+ for new projects; preserve existing compatibility requirements.

## Naming and Readability

- Follow PEP 8: `snake_case` for variables/functions/modules; `PascalCase` for classes/type aliases; `UPPER_SNAKE_CASE` for constants; `_name` for internal members.
- Use complete, meaningful names; avoid unnecessary abbreviations and built-in name shadowing.
- Prefer guard clauses and early returns over deep nesting.
- Avoid nested conditional expressions, complex one-line comprehensions, and hidden side effects.
- Add docstrings to clarify public contracts, surprising behavior, and non-obvious constraints—not to restate obvious code.

## Data, Functions, and Classes

- Write business logic as independent functions with explicit inputs and outputs.
- Use `@dataclass(frozen=True, slots=True)` for value objects by default; use mutable data only when justified.
- Do not mistake frozen fields for deep immutability.
- Use `TypedDict` to describe dictionary-shaped data statically, but validate untrusted inputs at runtime.
- Use `Enum` or `Literal` for finite states; use ordinary built-in collections for simple temporary data.
- Use classes when managing state, resource lifecycles, context managers, or externally required object protocols.
- Avoid unnecessary Manager, Service, Factory, and inheritance hierarchies.
- Never use mutable default arguments; use `default_factory` when appropriate.

## Result and Error Boundaries

Use a single project-level Result representation:

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Ok[T]:
    value: T


@dataclass(frozen=True, slots=True)
class Err[E]:
    error: E


type Result[T, E] = Ok[T] | Err[E]
```

- Return `Ok` on success and `Err` for expected, recoverable failure.
- Prefer structured errors with distinguishable codes/types, not message parsing.
- Catch specific external exceptions only at boundaries that can convert them into meaningful Result errors.
- Keep programmer mistakes, broken invariants, and unexpected failures as exceptions.
- Do not silently swallow exceptions or create a second incompatible Result abstraction.
- Do not force every helper to return Result or `unwrap()` ordinary failure branches.
- Convert Result to exit codes or protocol responses at application boundaries.
- Preserve cancellation (`asyncio.CancelledError`) and do not convert it to business `Err`.

## Modules, Packages, and Public APIs

- Organize by feature. Keep simple functionality in simple modules and split only when responsibilities justify it.
- Avoid default `controllers/services/repositories/interfaces` layering, circular imports, hidden initialization, and catch-all `utils.py` files.
- Prefer `src/` layout for installable packages; simple scripts may stay flat.
- Type all public function parameters and returns, plus important internal functions.
- Mark implementation details with `_`; expose stable package APIs explicitly in `__init__.py` as useful.
- Use `__all__` to clarify exports when appropriate; it is not access control.
- Avoid exposing mutable internal state and unnecessary third-party types in public interfaces.
- Prefer `list[str]`, `dict[str, int]`, and `T | None`; minimize `Any`, `cast`, and type-checking suppressions.
- Treat external files, JSON, CLI arguments, and network payloads as untrusted until validated.

## Abstraction and Metaprogramming

- Follow Concrete Types First.
- Introduce Protocol only for real substitutability needs, not single implementations.
- Use generics only when expressing meaningful relationships between types.
- Keep decorators simple, transparent, and compatible with introspection/type signatures.
- Avoid unnecessary reflection, metaclasses, monkey patching, and runtime code generation.
- Do not introduce design patterns solely for hypothetical future extensibility.

## Async and Concurrency

- Follow Sync by Default; use `asyncio` when non-blocking I/O benefits the program.
- Use `asyncio.TaskGroup` for related tasks; define timeouts, concurrency limits, and cleanup explicitly.
- Do not block an event loop with synchronous I/O or CPU-heavy work; use suitable thread/process strategies where needed.
- Keep event loop, task, executor, and resource lifecycles under application control.
- Propagate task cancellation; use `try/finally` for reliable cleanup.
- Avoid untracked background tasks and unnecessary conversion of synchronous call chains to async.

## Testing and Quality

- Use pytest; test observable behavior rather than implementation details.
- Cover Result `Ok`/`Err`, boundaries, important edge cases, and error propagation.
- Add regression tests for bug fixes; use integration tests for significant I/O boundaries.
- Mock external dependencies selectively; do not force arbitrary global coverage thresholds.
- Use Ruff for formatting/linting and one consistent checker (mypy or Pyright).
- Run applicable project checks, typically:

```bash
ruff check .
ruff format --check .
mypy src
pytest
```

Adapt commands to the actual project layout and tool configuration. Never claim tests passed unless executed.

## Dependencies and Configuration

- Use `pyproject.toml`, isolated environments, and a project-wide dependency management workflow.
- Prefer the standard library; justify third-party dependencies by real need, maintenance, license, and compatibility.
- Prefer reproducible lock files for applications and compatible dependency ranges for distributable libraries.
- Separate development-only dependencies and optional features appropriately.
- Do not change dependency tooling or the minimum Python version without user authorization.

## Code Agent Workflow

Before editing:
1. Inspect relevant source code, tests, and project configuration.
2. Identify established public APIs, result conventions, and compatibility constraints.
3. Plan the smallest complete change.

During editing:
1. Prefer data and functions with descriptive names.
2. Avoid unnecessary abstractions, deep nesting, clever one-liners, or unrelated refactoring.
3. Preserve Result/Exception and async cancellation semantics.
4. Do not silently change public APIs, dependencies, or Python version support.

After editing:
1. Add/update behavior-oriented tests.
2. Run available lint, format, type checks, and tests.
3. Inspect the diff for unnecessary complexity.
4. Report what changed, actual checks run, and remaining risks.

**Guiding rule:** Write straightforward typed Python with explicit Result errors, and introduce classes, abstraction, metaprogramming, or async only when justified.
