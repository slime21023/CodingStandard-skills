---
name: cpp-coding-guidelines
description: Apply C++20 coding guidelines when creating, modifying, refactoring, testing, or reviewing C++ code, packages, APIs, and CMake-based C++20 Modules projects. Favor data and functions, explicit ownership and RAII, third-party Expected with appropriate Exceptions, concrete types, readable code, and verified changes.
---

# C++ Coding Guidelines

Follow the user's C++ Coding Guidelines v1.0: **simple, explicit, safe, readable C++20**. Preserve the user's task scope and established project conventions; do not refactor unrelated code just to impose stylistic preferences.

## Workflow

1. Inspect relevant code, project constraints, tests, and the compiler, generator, and module layout.
2. Select topics from [the topic index](references/index.md) as described in Topic Retrieval.
3. Identify data, invariants, ownership, lifetime, failure modes, and the smallest public API. Implement the narrowest correct change and state practical reasons for exceptions.
4. Format, build, test, and inspect diagnostics as available. Compile an importing consumer for public module changes.
5. Report the checks and outcomes, including any module-toolchain or third-party Expected checks you could not run.

## Rule Levels

- **MUST**: Required; justify any exception.
- **SHOULD**: The default; adjust only with a concrete reason.
- **AVOID**: Not the default; use only when constraints justify it.

## Core Rules

- **MUST** **C++20 baseline:** Never require C++23-only facilities such as `std::expected` or assume `import std` is portable.
- **SHOULD** **Data and functions first:** Prefer `struct` for independent data and Free Functions for transformations and algorithms. Use `class` to maintain invariants, encapsulate mutable state, or own resources.
- **SHOULD** **Concrete types first:** Use Virtual Interfaces only for real runtime substitutability. Avoid speculative factories, one-implementation interfaces, unnecessary layers, and deep inheritance.
- **MUST** **Explicit ownership:** Prefer values, `std::vector`, and `std::array`. Use `std::unique_ptr` for necessary unique dynamic ownership and `std::shared_ptr` only for truly shared lifetime. Treat raw pointers as non-owning by default.
- **MUST** **RAII and lifetime:** Tie resources to owner objects. Do not return dangling references or preserve expired `std::span` / `std::string_view`. Prefer Rule of Zero.
- **MUST** **Errors:** Return a vetted, version-pinned third-party Expected for recoverable failures in C++20 (initial candidate: `tl::expected`). Reserve Exceptions for exceptional failures and existing API contracts. Never ignore errors.
- **MUST** **Modules first:** Use C++20 Named Modules for new project-defined interfaces and CMake `FILE_SET CXX_MODULES`. Use narrow Header/Adapter boundaries for third-party, C ABI, or toolchain constraints.
- **SHOULD** **Readability:** Name variables and functions fully, use early returns and braces, and keep side effects explicit. Avoid nested ternaries, excessive nesting, hidden magic, and needlessly dense code.
- **SHOULD** **Genericity:** Use Templates only for genuine multi-type requirements; prefer normal functions, standard facilities, and meaningful Concepts.
- **SHOULD** **Performance:** Pick sound algorithms and data layouts before optimization. Require measurements for complex allocators, pools, SIMD, or lock-free algorithms.

## Topic Retrieval

1. Open [references/index.md](references/index.md) and choose at most three topics by summary and tags.
2. Read each selected topic's `Summary`, `Rules`, and `Checklist` first.
3. Read `Recommended Pattern` when writing code, `Pitfalls` when reviewing or debugging, and `Tooling` or `Dependencies` when changing build or dependency setup.
4. Follow `related` IDs only when the selected topics do not answer the task.
5. Never load every topic file.

## Extract Only What You Need

If `mq` is available, run these from this skill's directory:

```shell
mq -A 'section::by_title("Rules")' references/errors.md
mq -A 'section::by_title("Checklist")' references/errors.md
mq '.code("cpp")' references/errors.md
mq '.yaml | frontmatter | select(self, get("tags") | contains("errors")) | get("id")' references/*.md
```

Without `mq`, open only the selected files or heading ranges. Do not install tools to read these references.
