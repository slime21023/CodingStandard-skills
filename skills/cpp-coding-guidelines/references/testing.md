---
id: cpp/testing
title: "Testing"
summary: "Test changed behavior and compile consumers of public modules."
language: cpp
topic: testing
tags: [testing, build, errors]
related: [cpp/errors]
snippets: unverified
---

# Testing

## Summary

Test changed behavior and compile consumers of public modules. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for behavior changes and public module work. For expected and exceptions, see [Expected and Exceptions](errors.md).

## Rules

- **MUST** test changed behavior and regression cases; test an importing consumer when changing public Modules.
- **SHOULD** Use supported ASan, UBSan, or TSan configurations as appropriate and separately where required.

## Recommended Pattern

Save the header from [Expected and Exceptions](errors.md#recommended-pattern) and configure the project with the directory containing the pinned `tl/expected.hpp`. Build, then run `ctest --test-dir build --output-on-failure`.

```cpp
// tests/discount_test.cpp
#include "discount.hpp"

int main() {
    const Product product{500};
    const auto partial = apply_discount(product, 200);
    if (!partial || partial->price_cents != 300) return 1;
    const auto boundary = apply_discount(product, 500);
    if (!boundary || boundary->price_cents != 0) return 1;
    const auto negative = apply_discount(product, -1);
    if (negative || negative.error() != DiscountError::NegativeAmount) return 1;
    const auto excess = apply_discount(product, 501);
    if (excess || excess.error() != DiscountError::ExceedsPrice) return 1;
    return 0;
}
```

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.28)
project(shop_tests LANGUAGES CXX)
find_path(TL_EXPECTED_INCLUDE_DIR tl/expected.hpp REQUIRED)
enable_testing()
add_executable(discount_test tests/discount_test.cpp)
target_compile_features(discount_test PRIVATE cxx_std_20)
target_include_directories(discount_test PRIVATE src "${TL_EXPECTED_INCLUDE_DIR}")
add_test(NAME discount COMMAND discount_test)
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Asserting only happy path | Misses error contracts | Cover boundaries and failure causes |
| Assertions compiled away | Release run proves nothing | Use explicit failure output or a test framework |
| Module producer checks only | Misses user-visible exports | Compile an importing target |

## Checklist

- Test ordinary and exact-price discounts.
- Check both recoverable errors.
- Compile an importing consumer after public module changes.
- Run supported sanitizers when they cover the risk.

## References

- [CMake add_test](https://cmake.org/cmake/help/latest/command/add_test.html)
- [CMake C++ Modules](https://cmake.org/cmake/help/latest/manual/cmake-cxxmodules.7.html)
