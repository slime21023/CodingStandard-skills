# C3 Topic Index

| Doc | Summary | Topic | Tags |
| --- | --- | --- | --- |
| [Version, Naming, and Style](naming-and-formatting.md) | Use a verified stable C3 compiler and clear names. | `naming-and-formatting` | `naming, formatting, tooling` |
| [Data and Control Flow](data-and-functions.md) | Use simple value types and keep computation in ordinary functions. | `data-and-functions` | `data, functions, control-flow` |
| [Modules and Public APIs](modules-and-api.md) | Organize modules by responsibility and expose only intentional contracts. | `modules-and-api` | `modules, public-api, documentation` |
| [Optionals and Faults](errors.md) | Use C3 optionals and typed faults for ordinary recoverable failures. | `errors` | `errors, option` |
| [Memory and Resources](resources-and-memory.md) | Keep temporary allocations scoped and give returned storage an explicit owner. | `resources-and-memory` | `ownership, memory, resources` |
| [Pointers and FFI](unsafe-and-ffi.md) | Keep raw pointers and ABI assumptions inside a narrow native boundary. | `unsafe-and-ffi` | `unsafe, ffi, ownership` |
| [Generics, Interfaces, and Macros](abstraction.md) | Add abstraction only to solve an actual reuse or dispatch problem. | `abstraction` | `interfaces, generics, metaprogramming` |
| [Testing](testing.md) | Use native tests to verify public behavior, faults, and boundaries. | `testing` | `testing, errors` |
| [Dependencies and Checks](tooling.md) | Keep C3 dependencies pinned and check the actual build targets. | `tooling` | `tooling, dependencies, build` |
