---
name: nim-coding-guidelines
description: Apply concise, data-oriented Nim 2.2+ coding standards when creating, editing, refactoring, testing, or reviewing Nim (.nim) and Nimble (.nimble) code. Use for Nim module and public API design, Result/Option/Exception error handling, metaprogramming, memory management, and Code Agent code quality checks.
---

# Nim Coding Guidelines

Apply these rules as project defaults. Honor explicit user requirements and established repository conventions when they conflict; make significant deviations visible rather than silently rewriting unrelated code. Prefer clear Nim idioms to patterns copied from other languages.

## Working process

1. Inspect the affected Nimble configuration, relevant modules, public symbols, tests, and local conventions before editing.
2. Make the smallest focused change. Reuse existing data structures and packages; do not introduce extra layers, macros, abstractions, or dependencies without a real need.
3. Preserve the public API and its failure contract unless the task requires a change. Add or adjust tests for changed behavior, errors, and boundary cases.
4. Run the relevant semantic/style checks, tests, and compilation. Report what ran, the results, and any unverified checks. Never claim tests passed without running them.

## Language, naming, and data

- Target **Nim 2.2 or newer** and the default **ORC** memory manager. Do not change memory management or disable runtime safety checks without measured, justified need.
- Follow NEP-1: two-space indentation, no tabs, a roughly 80-character line-length target, `PascalCase` for types and pure enum members, and `camelCase` for procedures, functions, fields, and variables.
- Use descriptive names. Avoid cryptic abbreviations, identifiers differentiated only by underscores/case, and clever compressed expressions.
- Prefer `let`; use `var` only when reassignment is needed and `const` for compile-time values.
- Prefer value `object`, `enum`, `tuple`, and standard collections. Use `ref object` only when identity or reference semantics are necessary.
- Prefer data and functions, composition over inheritance, and concrete types over unnecessary dispatch via `method`. Avoid hidden mutable global state.
- Public records may expose plain data; hide fields whose changes could violate invariants and provide validated construction or update functions.

## Procedures and control flow

- Use `func` for side-effect-free calculations and `proc` for I/O, logging, and other effects.
- Prefer return values to `var` output parameters. Make mutation intentional and local.
- Keep each routine focused; prefer guard clauses and early returns to nested conditions. Use Nim's implicit `result` or final expressions when clear, and explicit `return` for meaningful control flow.
- Avoid deeply nested `if` expressions, obscure operator tricks, and large expressions when named intermediate values improve reading.
- Function length, argument count, and nesting depth are review signals, not arbitrary automated limits.

## Modules and public APIs

- Organize Nimble modules by feature/domain, keeping small packages flat and splitting only as responsibilities grow. Avoid circular dependencies and generic `common`/`utils`/`manager` dumping grounds.
- Export only necessary symbols with `*`. For libraries, keep an intentional public entry module and selectively `export` stable APIs.
- Give public routines explicit parameter/result types, documented failure behavior, and `##` doc comments. Do not export internal mutable state or implementation details merely for convenience.
- Consider compatibility before changing public names, types, or semantics.

## Errors and asynchronous behavior

- Use `std/options.Option[T]` for ordinary absence, **`results.Result[T, E]`** for expected recoverable failures, and Exception for unexpected failures.
- Standardize on the third-party [`arnetheduck/nim-results`](https://github.com/arnetheduck/nim-results) package (Nimble package `results`). Do not invent a second generic Result or silently switch Result implementations.
- Prefer meaningful typed error categories. Every Result must be handled or propagated; use the package's `?` propagation helper only when it keeps flow straightforward.
- Catch only specific expected `CatchableError` descendants at I/O and dependency boundaries, then convert to a meaningful Result. Never use empty bare `except`, swallow failures, treat `Defect` as a normal business error, or log the same failure at every layer.
- Where useful, enforce an exception-free synchronous API with `{.raises: [].}` and verify compilation. Do **not** assume this guarantee holds for `std/asyncdispatch` async procedures.
- Await asynchronous work or explicitly handle it (e.g., `asyncCheck` where appropriate); never blindly `discard` a Future.

## Abstraction and performance

- Choose the least powerful mechanism that solves the problem: `func`/`proc`, then necessary generics, then `template`, then `macro`.
- Introduce macros, converters, DSLs, raw pointers, custom allocators, or unsafe pragmas only with a concrete use case and documented tradeoffs.
- Profile before optimizing; retain safety checks, regression tests, and readable code.

## Minimum quality gate

- Add `std/unittest` tests (and integration tests when relevant) for main behavior, expected failures, and boundary cases. Add regression tests for fixed bugs.
- Check all relevant entry points, not just one file. Typical commands (adapt paths to the repository):
  - `nim check --styleCheck:error src/project.nim`
  - `nimble test`
  - `nim c -d:release src/main.nim` for executable entry points; compile a suitable test/example entry for a library.
- Do not hide warnings, skip tests, or weaken checks to make a build pass.

## When additional examples are useful

Read [references/nim-patterns.md](references/nim-patterns.md) when creating a Nimble package, designing a public Result-returning API, adapting exceptions, or preparing a check/test workflow.

## Final report

Summarize the code/API changes, the reason for any new abstraction or dependency, the exact checks performed and results, and remaining limitations. Keep the report brief and factual.
