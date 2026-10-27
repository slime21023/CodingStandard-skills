---
name: cpp-coding-guidelines
description: Apply C++20 coding guidelines when creating, modifying, refactoring, testing, or reviewing C++ code, packages, APIs, and CMake-based C++20 Modules projects. Favor data and functions, explicit ownership and RAII, third-party Expected with appropriate Exceptions, concrete types, readable code, and verified changes.
---

# C++ Coding Guidelines

Follow the user's C++ Coding Guidelines v1.0: **simple, explicit, safe, readable C++20**. Preserve the user's task scope and established project conventions; do not refactor unrelated code just to impose stylistic preferences.

## Workflow

1. Inspect relevant code, existing conventions, project constraints, toolchain, Module layout, dependencies, and tests.
2. Identify data, behavior, invariants, ownership, lifetime, failure modes, and the smallest necessary public API.
3. Implement the narrowest correct change, preferring the rules below. State the practical reason for exceptions.
4. Format, build, test, and inspect diagnostics when available. For public Module changes, compile an importing consumer target.
5. Report exactly which checks ran, their results, and any limitations. Never claim an unrun check passed.

## Core rules

- **C++20 baseline:** Never require C++23-only facilities such as `std::expected` or assume `import std` is portable.
- **Data and functions first:** Prefer `struct` for independent data and Free Functions for transformations and algorithms. Use `class` to maintain invariants, encapsulate mutable state, or own resources.
- **Concrete types first:** Use Virtual Interfaces only for real runtime substitutability. Avoid speculative factories, one-implementation interfaces, unnecessary layers, and deep inheritance.
- **Explicit ownership:** Prefer values, `std::vector`, and `std::array`. Use `std::unique_ptr` for necessary unique dynamic ownership and `std::shared_ptr` only for truly shared lifetime. Treat raw pointers as non-owning by default.
- **RAII and lifetime:** Tie resources to owner objects. Do not return dangling references or preserve expired `std::span` / `std::string_view`. Prefer Rule of Zero.
- **Errors:** Return a vetted, version-pinned third-party Expected for recoverable failures in C++20 (initial candidate: `tl::expected`). Reserve Exceptions for exceptional failures and existing API contracts. Never ignore errors.
- **Modules first:** Use C++20 Named Modules for new project-defined interfaces and CMake `FILE_SET CXX_MODULES`. Use narrow Header/Adapter boundaries for third-party, C ABI, or toolchain constraints.
- **Readability:** Name variables and functions fully, use early returns and braces, and keep side effects explicit. Avoid nested ternaries, excessive nesting, hidden magic, and needlessly dense code.
- **Genericity:** Use Templates only for genuine multi-type requirements; prefer normal functions, standard facilities, and meaningful Concepts.
- **Performance:** Pick sound algorithms and data layouts before optimization. Require measurements for complex allocators, pools, SIMD, or lock-free algorithms.

## Naming and API defaults

| Element | Style |
| --- | --- |
| Type, struct, class | `PascalCase` |
| Function, variable, namespace | `snake_case` |
| Private member | `snake_case_` |
| Named constant | `kPascalCase` |
| Macro, when unavoidable | `UPPER_SNAKE_CASE` |

Use `const`, `nullptr`, `enum class`, `explicit`, and `[[nodiscard]]` when appropriate. Use `auto` when type clarity improves. Pass cheap values by value, read-only large values by `const T&`, mutating inputs by `T&`, and nullable non-owning objects by `T*`.

## Reference routing

- **Before substantial C++ implementation/review:** Read [references/guidelines.md](references/guidelines.md), containing all 36 rules and checklist.
- **Before Modules, CMake, public interface, or toolchain work:** Read [references/modules.md](references/modules.md).
- **Before Expected, Exceptions, constructors, ownership or lifetime-sensitive APIs:** Read [references/errors-and-ownership.md](references/errors-and-ownership.md).

Apply relevant references without adding unnecessary dependencies or broadening the task. Explicitly note when Modules compilation or a third-party Expected API cannot be verified in the available environment.
