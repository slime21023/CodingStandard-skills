---
id: python/tooling
title: "Tooling and Dependencies"
summary: "Keep Python tooling and dependencies explicit and reproducible."
language: python
topic: tooling
tags: [tooling, testing, dependencies]
related: [python/testing]
snippets: unverified
---

# Tooling and Dependencies

## Summary

Keep Python tooling and dependencies explicit and reproducible. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when setting up a project or validating a change. For testing, see [Testing](testing.md).

## Rules

- **SHOULD** Use Ruff for formatting/linting and one consistent checker (mypy or Pyright).
- **SHOULD** Use `pyproject.toml`, isolated environments, and a project-wide dependency management workflow.
- **SHOULD** Prefer the standard library; justify third-party dependencies by real need, maintenance, license, and compatibility.
- **SHOULD** Prefer reproducible lock files for applications and compatible dependency ranges for distributable libraries.
- **SHOULD** Separate development-only dependencies and optional features appropriately.
- **MUST** Do not change dependency tooling or the minimum Python version without user authorization.

## Recommended Pattern

For a new project, record its supported Python version in `pyproject.toml`.

```toml
# pyproject.toml
[project]
name = "shop"
version = "0.1.0"
requires-python = ">=3.13"
```

Adapt checks to the existing project layout.

```shell
ruff check .
ruff format --check .
mypy src
pytest
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Mixed type checkers | Gives inconsistent diagnostics | Select one checker |
| Test dependencies in runtime requirements | Increases installation cost | Separate development requirements |
| Unsupported version change | Breaks target projects | Keep the declared compatibility floor |

## Checklist

- Use an isolated environment.
- Keep runtime and development dependencies distinct.
- Run the configured formatter, linter, checker, and tests.
- Report any checks not run.

## References

- [Writing pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [Mypy documentation](https://mypy.readthedocs.io/en/stable/)
