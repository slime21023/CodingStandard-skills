# Expected, Exceptions, Ownership, and Lifetime

Read before changing error-returning APIs, constructors/destructors, resource management, or non-owning views.

## Error strategy

| Condition | Preferred representation |
| --- | --- |
| Recoverable parse/validation/I/O/network failure | Version-pinned third-party `expected<T, E>` and meaningful error `E` |
| Legitimate absence | `std::optional<T>` |
| Construction cannot establish required invariant | Exception or a fallible factory using Expected, according to contract |
| External/exceptional failure | Exception translated or handled at a meaningful boundary |
| Programmer bug | Fix the defect; use tests/assertions rather than a fake recoverable failure |

`std::expected` is C++23, not C++20. Recommended C++20 candidate: [`tl::expected`](https://github.com/TartanLlama/expected). Before introducing it, assess version, license, compiler support, public API reachability, module integration, and existing dependency policy. Do not silently add a new dependency to an existing project.

### Illustrative Expected contract

```cpp
#include <string_view>
#include <tl/expected.hpp>

enum class ParseError {
    empty_input,
    invalid_format,
};

struct Config {
    int retry_count;
};

tl::expected<Config, ParseError> parse_config(std::string_view text) {
    if (text.empty()) {
        return tl::unexpected(ParseError::empty_input);
    }
    // Only a contract example; replace with validated parsing logic.
    return Config{3};
}
```

Always inspect success before accessing value/error; preserve relevant error context. Public `Result<T, E>` aliases need actual importing-consumer tests and are not guaranteed compatible with future `std::expected` implementations.

## Ownership guide

| Intent | Default type |
| --- | --- |
| Normal owned object | Value / local / member |
| Growable owned collection | `std::vector<T>` |
| Unique dynamic ownership | `std::unique_ptr<T>` |
| Actual shared lifetime | `std::shared_ptr<T>` with cycle analysis |
| Non-null non-owning object | `T&` / `const T&` |
| Nullable non-owning object | `T*` / `const T*` |
| Non-owning contiguous view | `std::span<T>` |
| Non-owning string view | `std::string_view` |

- Use RAII for files, locks, system handles, and allocations.
- Never use raw pointers to hide ownership. Explicitly document owner/view lifetime relationships.
- Do not retain a non-owning view after its source expires, including through callbacks or asynchronous work.
- Favor Rule of Zero; define Copy/Move only for genuine resource semantics.
- Prevent destructor exception escape; mark `noexcept` only if valid.
- Validate thread lifetime and synchronization before introducing pools or lock-free techniques.

Sources: [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines), [WG21 std::expected](https://www.open-std.org/jtc1/sc22/WG21/docs/papers/2022/p0323r12.html), [tl::expected](https://github.com/TartanLlama/expected).
