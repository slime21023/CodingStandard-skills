---
id: cpp/modules-and-api
title: "C++20 Modules and CMake"
summary: "Prefer named modules for new C++20 project interfaces."
language: cpp
topic: modules-and-api
tags: [modules, public-api, build]
related: [cpp/errors]
snippets: unverified
---

# C++20 Modules and CMake

## Summary

Prefer named modules for new C++20 project interfaces. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for target layouts and new named module interfaces. For expected and exceptions, see [Expected and Exceptions](errors.md).

## Rules

- **MUST** target C++20 as the minimum; do not introduce required C++23/26 facilities without explicit approval.
- **MUST** prefer C++20 Named Modules for new project-defined interfaces; conventionally use `.cppm` interfaces and `.cpp` implementation units.
- **MUST** use CMake 3.28+ for Modules with `FILE_SET CXX_MODULES`; record compiler, standard library, generator, and CMake versions.
- **MUST** verify clean and incremental builds on declared Modules toolchains; test each platform actually claimed as supported.
- **SHOULD** use Ninja/Ninja Multi-Config where suitable; do not assume portable Header Units, `import std`, or interchangeable BMIs.
- **MUST** provide narrow Header/Adapter boundaries for C APIs, third-party headers, ABI requirements, and toolchain limitations.
- **SHOULD** Keep one named module per cohesive feature, minimize exports and prevent cyclic imports.
- **SHOULD** Verify exported/private source visibility, transitive requirements, and third-party Expected type reachability with a real consumer.

Note: `.cppm` and `.cpp` are conventions. Use narrow headers or a global module fragment where necessary; do not assume portable header units or interoperable BMIs.

## Recommended Pattern

Use these three source files with the CMake project below. Record the compiler, standard library, generator, and CMake versions that pass clean and incremental builds.

```cpp
// src/orders.cppm
export module shop.orders;

export namespace shop {
/// Submit a positive order ID; return false without submitting an invalid ID.
bool place_order(int order_id, void (*submit)(int));
}
```

```cpp
// src/orders.cpp
module shop.orders;

namespace shop {
namespace {
bool valid_order_id(int order_id) {
    return order_id > 0;
}
}

bool place_order(int order_id, void (*submit)(int)) {
    if (!valid_order_id(order_id)) {
        return false;
    }
    submit(order_id);
    return true;
}
}
```

```cpp
// src/main.cpp
import shop.orders;

int received_order_id = 0;

void record_order(int order_id) {
    received_order_id = order_id;
}

int main() {
    const bool accepted = shop::place_order(42, record_order);
    return accepted && received_order_id == 42 ? 0 : 1;
}
```

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.28)
project(shop LANGUAGES CXX)

add_library(orders)
target_compile_features(orders PUBLIC cxx_std_20)
set_target_properties(orders PROPERTIES CXX_EXTENSIONS OFF)
target_sources(orders
    PUBLIC FILE_SET CXX_MODULES FILES src/orders.cppm
    PRIVATE src/orders.cpp
)

add_executable(shop_example src/main.cpp)
target_link_libraries(shop_example PRIVATE orders)
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Assuming universal import std | Toolchain support differs | Check the declared toolchain |
| Private helpers exported | Leaks implementation | Keep exports intentional |
| Build only module producer | Misses importer compatibility | Compile an importing target |

## Checklist

- Use FILE_SET CXX_MODULES on supported CMake.
- Verify clean and incremental builds.
- Compile an importing consumer.
- Isolate third-party header and ABI boundaries.

## References

- [CMake C++ Modules](https://cmake.org/cmake/help/latest/manual/cmake-cxxmodules.7.html)
- [CMake target_sources](https://cmake.org/cmake/help/latest/command/target_sources.html)
- [Clang modules](https://clang.llvm.org/docs/StandardCPlusPlusModules.html)
