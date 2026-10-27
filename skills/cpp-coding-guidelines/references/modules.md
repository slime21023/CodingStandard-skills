# C++20 Modules and CMake

Read before introducing Modules, modifying exported APIs, CMake targets, or third-party compatibility boundaries.

## Design rules

- Prefer one named module per cohesive feature, not one per trivial file or class.
- Use `export module project.feature;` in the public `.cppm` interface and `module project.feature;` in `.cpp` implementations. Extensions are conventions rather than standard mandates.
- Export the minimal API. Keep helpers internal and prevent cyclic imports.
- Use CMake 3.28+ `FILE_SET CXX_MODULES` on Targets. Validate source visibility and transitive dependencies.
- For C APIs and third-party headers, use a narrow adapter or a required Global Module Fragment include. Do not assume `import std` or Header Units work in all C++20 environments.
- Validate the actual compiler, standard library, generator, clean builds, incremental builds, and importing consumer builds.

## Minimal module example

`src/geometry.cppm`:

```cpp
export module project.geometry;

export namespace project {
struct Rectangle {
    double width;
    double height;
};

double calculate_area(const Rectangle& rectangle);
}
```

`src/geometry.cpp`:

```cpp
module project.geometry;

namespace project {
double calculate_area(const Rectangle& rectangle) {
    return rectangle.width * rectangle.height;
}
}
```

`CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.28)
project(example LANGUAGES CXX)

add_library(geometry)
target_compile_features(geometry PUBLIC cxx_std_20)
set_target_properties(geometry PROPERTIES CXX_EXTENSIONS OFF)
target_sources(geometry
    PUBLIC FILE_SET CXX_MODULES FILES src/geometry.cppm
    PRIVATE src/geometry.cpp
)
```

The example is a design template. Do not claim it is universally buildable without testing a concrete toolchain.

## Compatibility review

1. Identify compiler, standard library, generator, CMake version, and build environment.
2. Confirm module scanning and exported/private `FILE_SET` visibility behavior.
3. Build clean and incrementally; compile a separate consumer that imports changed public modules.
4. Test third-party Header/Expected types used in exported interfaces, including template instantiation and ABI concerns.
5. Use documented Header/Adapter fallbacks where necessary, without broad rewrites.

Sources: [CMake C++ Modules](https://cmake.org/cmake/help/latest/manual/cmake-cxxmodules.7.html), [CMake FILE_SET](https://cmake.org/cmake/help/latest/command/target_sources.html), [Clang Standard Modules](https://clang.llvm.org/docs/StandardCPlusPlusModules.html).
