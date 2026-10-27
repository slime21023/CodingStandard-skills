---
name: c3-coding-guidelines
description: Apply concise, data-oriented C3 coding standards when creating, editing, refactoring, testing, or reviewing C3 (.c3) code and C3 project configurations. Covers naming, structs and functions, modules, public APIs, native Optional/Fault errors, allocators, memory safety, FFI, generics, interfaces, macros, testing, dependencies, and Code Agent behavior.
---

# C3 Coding Guidelines

Apply these rules as project defaults. Honor explicit user instructions and established repository conventions when they conflict. Prefer idiomatic C3 to patterns copied from other languages.

## Working process

1. Inspect the affected C3 modules, project.json, public APIs, compiler version, relevant tests, and local conventions.
2. Plan the smallest focused change. Reuse existing data structures and functions.
3. Preserve public API contracts unless the task explicitly calls for changing them. Test successes, expected failures, and boundary cases.
4. Run relevant compilation, native tests, and safety checks; report what ran and what could not be verified.

## Language version and style

- Use a pinned, verified stable C3 compiler release; do not silently switch versions or introduce nightly-only features.
- Confirm unfamiliar syntax and standard-library APIs against the pinned release.
- Use snake_case for modules, files, functions, methods, variables, fields, and macros.
- Use PascalCase for types and structs, and UPPER_SNAKE_CASE for constants.
- Use tabs and Allman-style braces. Use self as the method receiver name.
- Choose descriptive names. Avoid unnecessary abbreviations and clever compressed expressions.
- Comment on intent, invariants, ownership, lifetime, and non-obvious constraints rather than restating code.

## Data and control flow

- Prefer simple structs and ordinary functions. Use methods only for operations closely tied to a receiver value.
- Keep structs cohesive; prefer value semantics where appropriate and avoid hidden mutable global state.
- Do not emulate complex class hierarchies with struct subtyping.
- Keep functions focused. Prefer guard conditions and early returns to deeply nested statements.
- Treat more than three nesting levels as a refactoring signal, not an automatic prohibition.
- Do not use nested ternary expressions. Use named intermediate variables for complex conditions.
- Make mutation and side effects apparent. Do not generate meaningless getter/setter layers.

## Modules and public APIs

- Organize modules by feature or responsibility. Keep small projects flat and split only when needed.
- Keep related data and behavior together; avoid circular dependencies and generic utility dumping grounds.
- Explicitly declare a module for project source files.
- Follow a private-by-default policy using module section visibility or declaration attributes as appropriate.
- Mark only intentional public APIs public; document parameters, results, fault behavior, allocation, ownership, and lifetime.
- Preserve stable public interfaces. Avoid exposing internal implementation details.
- C3 permits import ... @public to access private declarations; do not use it to bypass a module's intended API boundary without an explicit architecture reason.

## Errors

- Use native C3 T?, void?, and fault for expected recoverable failures.
- Handle or propagate relevant optional failures; never silently discard them.
- Use ?? only when a meaningful fallback is part of the function contract.
- Reserve panic for unrecoverable failures or violated invariants, not ordinary business errors.
- Do not introduce a generic Result framework; use a dedicated data type only when structured diagnostic detail is necessary.
- Preserve the meaning of faults across module and FFI boundaries.

## Memory and resource management

- Prefer stack values, then scoped temporary allocation with @pool, then explicit allocators for long-lived dynamic data.
- Make allocation and release responsibilities clear. Name allocator arguments allocator; prefer allocator-first public APIs.
- Use defer for deterministic cleanup of owned resources.
- Never allow a pointer or slice to temporary memory to escape its valid @pool lifetime.
- Never pass temporary references to another thread if their lifetime cannot be guaranteed.
- Document whether returned pointers and slices are borrowed or owned, and who releases owned allocations.
- Treat borrowed/owned as explicit contracts; C3 does not enforce Rust-style ownership rules.
- Avoid needless heap allocation or copying, but profile before complex optimization.

## Pointer and FFI boundaries

- Prefer typed values, slices, and standard-library APIs.
- Use raw pointers only when justified, keeping unsafe operations small and auditable.
- Group external declarations and ABI-sensitive code into focused FFI boundary modules.
- Validate external data, layouts, calling conventions, resource ownership, and release functions.
- Do not add wrappers without actual safety or API clarity benefits.

## Abstraction

- Use concrete types and ordinary functions first.
- Introduce generics when actual cross-type reuse justifies them.
- Use interfaces only when runtime polymorphism is necessary.
- Use macros and compile-time reflection only when ordinary functions or generics are insufficient.
- Avoid speculative abstractions, macro-heavy control flow, and abstraction for a single implementation without a concrete need.

## Dependencies, tests, and quality

- Prefer the standard library. Keep third-party dependencies minimal, justified, pinned, and compatible with the compiler.
- Use native @test for unit tests; include test sources in project.json as appropriate.
- Cover public APIs, success and failure cases, boundaries, and regressions for fixed bugs.
- Exercise memory lifetime and FFI-sensitive code with supported safety checks and sanitizers when appropriate.
- Keep debug safety checks enabled. Verify relevant release targets before delivery.
- Typical project checks are: c3c build; c3c test; c3c build release. Adapt to actual targets.
- Do not silence warnings, weaken checks, or claim success to conceal failures.
- Benchmark or profile before making readability-reducing performance changes.

## Code Agent requirements

- Read relevant repository code and local instructions before editing.
- Keep changes minimal and on task. Never refactor unrelated code without authorization.
- Reuse existing structures and conventions; do not add interfaces, generics, macros, wrappers, or dependencies without a demonstrated need.
- Prefer complete descriptive identifiers and simple branching. Avoid excessive abbreviations, deep nesting, and nested ternaries.
- Verify optional/fault handling, pointer lifetime, allocator ownership, and defer cleanup.
- Verify compiler compatibility before using unfamiliar C3 syntax or APIs.
- Add or update tests for behavior changes; run available checks.
- Never claim to have executed a test that was not run.

## Final review and report

Verify naming, focused functions, intentional module/public boundaries, handled errors, valid resource lifetimes, necessary abstractions, and relevant passing checks.

Briefly report changes, any justified new abstraction or dependency, exact checks performed, results, and remaining risks or unverified items.

## Official references

- https://c3-lang.org/
- https://c3-lang.org/language-fundamentals/naming/
- https://c3-lang.org/language-fundamentals/modules/
- https://c3-lang.org/language-common/optionals-essential/
- https://c3-lang.org/language-common/memory/
- https://c3-lang.org/language-common/cinterop/
- https://c3-lang.org/build-your-project/build-commands/
