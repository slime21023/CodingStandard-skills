---
id: rust/unsafe-and-ffi
title: "Unsafe"
summary: "Prefer safe Rust and isolate every justified low-level operation."
language: rust
topic: unsafe-and-ffi
tags: [unsafe, ffi, ownership]
related: [rust/resources-and-memory]
snippets: unverified
---

# Unsafe

## Summary

Prefer safe Rust and isolate every justified low-level operation. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this only when a justified native boundary has no safe API. For ownership and borrowing, see [Ownership and Borrowing](resources-and-memory.md).

## Rules

- **SHOULD** Keep operations safe by default; justify any FFI, low-level data structure, or measured performance need.
- **MUST** Minimize unsafe blocks and provide a SAFETY comment that explains why the preconditions hold.
- **MUST** Document caller obligations for unsafe fn in a Safety section and test and review the invariants.
- **MUST** Never use raw pointers, transmute, or unsafe to evade ownership or type design.

Note: The target must supply a C runtime with `strlen`. In Rust-only code use `key.to_bytes().len()` instead of introducing FFI.

## Recommended Pattern

```rust
// src/catalog/ffi.rs
use std::ffi::{CStr, c_char};

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

/// Count bytes before the terminating NUL.
pub fn catalog_key_len(key: &CStr) -> usize {
    // SAFETY: CStr guarantees a live NUL-terminated buffer for the call.
    unsafe { strlen(key.as_ptr()) }
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Passing arbitrary &str to strlen | Need not be NUL-terminated | Accept &CStr |
| Safety comment restates the operation | Does not establish soundness | Cite the enforced preconditions |
| Unsoundness fixed with transmute | Hides an invalid type relationship | Repair the boundary or use safe types |

## Checklist

- Check the native ABI and symbol.
- Restrict raw pointers to the boundary.
- Explain soundness immediately before the unsafe block.
- Review and test native lifetime invariants.

## References

- [Rustonomicon](https://doc.rust-lang.org/stable/nomicon/)
- [Unsafe extern blocks](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-extern.html)
