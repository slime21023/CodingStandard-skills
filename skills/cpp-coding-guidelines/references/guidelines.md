# C++ Coding Guidelines v1.0 — Complete Rules

**MUST** = required for correctness, safety, and declared project contracts. **SHOULD** = preferred unless an explicit, justified exception applies. Apply incrementally to legacy code; do not rewrite unrelated files.

## Language and build

1. **MUST** target C++20 as the minimum; do not introduce required C++23/26 facilities without explicit approval.
2. **MUST** prefer C++20 Named Modules for new project-defined interfaces; conventionally use `.cppm` interfaces and `.cpp` implementation units.
3. **MUST** use CMake 3.28+ for Modules with `FILE_SET CXX_MODULES`; record compiler, standard library, generator, and CMake versions.
4. **MUST** verify clean and incremental builds on declared Modules toolchains; test each platform actually claimed as supported.
5. **SHOULD** use Ninja/Ninja Multi-Config where suitable; do not assume portable Header Units, `import std`, or interchangeable BMIs.
6. **MUST** provide narrow Header/Adapter boundaries for C APIs, third-party headers, ABI requirements, and toolchain limitations.

## Data, functions, APIs

7. **MUST** prefer `struct` for independent data and Free Functions for algorithms and transformations.
8. **MUST** use `class` for invariants, state protection, or resource lifetime encapsulation.
9. **MUST** favor concrete types; use Virtual Interfaces only for real runtime substitutability.
10. **SHOULD** avoid deep inheritance, one-implementation interfaces, speculative factories, and empty manager/service wrappers.
11. **MUST** keep functions cohesive, side effects visible, and control flow simple; prefer Guard Clauses to nesting.
12. **SHOULD** pass small cheap values by value, large read-only inputs by `const T&`, mutating inputs by `T&`, nullable non-owning objects by `T*`.

## Resource and lifetime safety

13. **MUST** default to values and `std::vector`/`std::array`; use `std::unique_ptr` for necessary unique dynamic ownership.
14. **MUST** reserve `std::shared_ptr` for genuinely shared lifetime, review cycles, and treat raw pointers as non-owning by default.
15. **MUST** manage resources with RAII; avoid raw owning `new`/`delete` in application code.
16. **MUST** prevent dangling references, pointers, spans, and string views. Document owner/view lifetime relations.
17. **SHOULD** follow Rule of Zero; define special members only as resource semantics require. Use Move intentionally.
18. **SHOULD** justify custom allocators, arenas, pools, SIMD, and lock-free schemes with evidence and tests.

## Expected and Exception errors

19. **MUST** return explicit results for expected recoverable parsing, validation, I/O, and network failure; do not use Exceptions for normal branching.
20. **MUST** use a reviewed, pinned third-party Expected implementation in C++20, such as `tl::expected`, rather than build a new generic Result framework.
21. **SHOULD** maintain consistent Result naming; test public Module aliases and do not assume effortless migration to `std::expected`.
22. **MUST** represent useful error causes with `enum class` or structured types, not opaque `bool` or silently empty values.
23. **MUST** check Expected success before accessing value/error; preserve contextual errors. Use `std::optional` only when absence is not failure.
24. **MUST** reserve Exceptions for exceptional failures, impossible constructors, or existing library contracts; catch at meaningful boundaries and never swallow silently.
25. **MUST** not let destructor exceptions escape; use `noexcept` only when warranted. Handle programmer errors as defects, not pretend-recoverable results.

## Genericity and readability

26. **MUST** use Templates only for genuinely generic code; prefer ordinary functions, standard utilities, and meaningful C++20 Concepts.
27. **MUST** use descriptive names, braces, and simple control flow; avoid nested ternaries, avoidable nesting, and hidden side effects.
28. **SHOULD** use `const`, `enum class`, `nullptr`, `explicit`, and `[[nodiscard]]`; limit C casts, macros, and opaque `auto`.
29. **MUST** use `PascalCase` types, `snake_case` functions/variables/namespaces, `snake_case_` private members, `kPascalCase` constants, `UPPER_SNAKE_CASE` macros.
30. **SHOULD** comment why, invariants, ownership, and tradeoffs; avoid describing obvious code.

## Concurrency, performance, verification

31. **MUST** manage thread lifetimes and shared mutable data; `volatile` is not synchronization. Prefer `std::jthread` for basic thread ownership.
32. **MUST** validate algorithmic correctness and profile before nontrivial micro-optimizations.
33. **MUST** test changed behavior and regression cases; test an importing consumer when changing public Modules.
34. **MUST** run CI formatting, builds, tests, and declared Modules toolchain checks.
35. **SHOULD** use `clang-format`, `clang-tidy`, and supported ASan/UBSan/TSan setups, separately where needed.
36. **MUST** never hide diagnostics, swallow errors, or claim unrun checks succeeded.

## Review checklist

- [ ] Meets C++20 and supported Modules toolchain constraints.
- [ ] Uses Struct/Free Functions by default; abstractions have specific reasons.
- [ ] Makes ownership, views, copy/move, and lifetimes explicit.
- [ ] Propagates Expected errors and handles Exception boundaries correctly.
- [ ] Keeps naming and control flow readable.
- [ ] Builds public Modules and third-party compatibility edges.
- [ ] Avoids speculative abstractions and unmeasured micro-optimization.
- [ ] Records real format/build/test results.

## References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [ClangFormat](https://clang.llvm.org/docs/ClangFormat.html)
- [clang-tidy](https://clang.llvm.org/extra/clang-tidy/)
