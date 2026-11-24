---
id: cpp/resources-and-memory
title: "Ownership and Lifetime"
summary: "Make owners, views, and deterministic resource cleanup explicit."
language: cpp
topic: resources-and-memory
tags: [ownership, memory, resources]
related: [cpp/errors]
snippets: unverified
---

# Ownership and Lifetime

## Summary

Make owners, views, and deterministic resource cleanup explicit. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for files, locks, allocations, or borrowed views. For expected and exceptions, see [Expected and Exceptions](errors.md).

## Rules

- **MUST** default to values and `std::vector`/`std::array`; use `std::unique_ptr` for necessary unique dynamic ownership.
- **MUST** reserve `std::shared_ptr` for genuinely shared lifetime, review cycles, and treat raw pointers as non-owning by default.
- **MUST** manage resources with RAII; avoid raw owning `new`/`delete` in application code.
- **MUST** prevent dangling references, pointers, spans, and string views. Document owner/view lifetime relations.
- **SHOULD** follow Rule of Zero; define special members only as resource semantics require. Use Move intentionally.
- **SHOULD** justify custom allocators, arenas, pools, SIMD, and lock-free schemes with evidence and tests.
- **MUST** Keep borrowed views valid across callbacks and async work; never hide ownership in a raw pointer.
- **MUST** Do not let exceptions escape destructors.

Note: Use values and standard collections for ownership, `std::unique_ptr` for unique dynamic ownership, and `std::shared_ptr` only for shared lifetime. Use references for non-null borrowing, pointers for nullable borrowing, and `std::span` or `std::string_view` for views. The example treats an unavailable required catalog as exceptional; return Expected for recoverable I/O.

## Recommended Pattern

```cpp
// src/catalog_reader.cpp
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <span>
#include <stdexcept>
#include <vector>

struct Product {
    std::int64_t price_cents;
};

// The file contains validated integer prices, one per line.
[[nodiscard]] std::vector<Product> read_catalog(const std::filesystem::path& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::ios_base::failure("cannot open required catalog");
    }
    std::vector<Product> products;
    for (std::int64_t price_cents; input >> price_cents;) {
        products.push_back(Product{price_cents});
    }
    if (input.bad() || !input.eof()) {
        throw std::ios_base::failure("cannot read required catalog");
    }
    return products;
}

// Borrow only while the owning vector is live and has not reallocated.
[[nodiscard]] std::span<const Product> catalog_view(const std::vector<Product>& products) {
    return products;
}
std::span<const Product> catalog_view(const std::vector<Product>&&) = delete;
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Raw owning pointer | Hides destruction responsibility | Use a value or unique_ptr |
| Span outlives vector | Becomes dangling | Keep the owner live and stable |
| shared_ptr by default | Masks unclear ownership and permits cycles | Require an actual shared lifetime |

## Checklist

- Identify the owner and every borrower.
- Tie cleanup to RAII.
- Prefer Rule of Zero.
- Document and test view invalidation.

## References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
