---
id: cpp/tooling
title: "Formatting, Analysis, and CI"
summary: "Run checks on the actual supported compiler and generator configurations."
language: cpp
topic: tooling
tags: [tooling, formatting, build]
related: [cpp/modules-and-api]
snippets: unverified
---

# Formatting, Analysis, and CI

## Summary

Run checks on the actual supported compiler and generator configurations. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for build or handoff work. For c++20 modules and cmake, see [C++20 Modules and CMake](modules-and-api.md).

## Rules

- **MUST** run CI formatting, builds, tests, and declared Modules toolchain checks.
- **SHOULD** Use clang-format and clang-tidy where supported.
- **MUST** never hide diagnostics, swallow errors, or claim unrun checks succeeded.

## Recommended Pattern

Use the project's configured C++20 toolchain and preserve its checks.

```shell
clang-format --dry-run --Werror src/orders.cppm src/orders.cpp
cmake -S . -B build -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build build
clang-tidy -p build src/orders.cpp
ctest --test-dir build --output-on-failure
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Skipping warnings | Hides real defects | Fix findings or scope a justified exception |
| Claiming module support from another compiler | Results are toolchain-dependent | Check each supported target |
| Clean build only | Misses changed dependency scanning | Verify an incremental build too |

## Checklist

- Record compiler, library, generator, and CMake versions.
- Run format, analysis, build, and test checks as applicable.
- Check the claimed module configurations.
- Report unverified checks honestly.

## References

- [CMake C++ Modules](https://cmake.org/cmake/help/latest/manual/cmake-cxxmodules.7.html)
- [ClangFormat](https://clang.llvm.org/docs/ClangFormat.html)
- [clang-tidy](https://clang.llvm.org/extra/clang-tidy/)
