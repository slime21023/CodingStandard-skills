---
id: c3/unsafe-and-ffi
title: "Pointers and FFI"
summary: "Keep raw pointers and ABI assumptions inside a narrow native boundary."
language: c3
topic: unsafe-and-ffi
tags: [unsafe, ffi, ownership]
related: [c3/resources-and-memory]
snippets: unverified
---

# Pointers and FFI

## Summary

Keep raw pointers and ABI assumptions inside a narrow native boundary. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this only when a C ABI dependency needs a focused adapter. For memory and resources, see [Memory and Resources](resources-and-memory.md).

## Rules

- **SHOULD** Prefer typed values, slices, and standard-library APIs.
- **SHOULD** Use raw pointers only when justified, keeping unsafe operations small and auditable.
- **SHOULD** Group external declarations and ABI-sensitive code into focused FFI boundary modules.
- **SHOULD** Validate external data, layouts, calling conventions, resource ownership, and release functions.
- **MUST** Do not add wrappers without actual safety or API clarity benefits.

Note: This uses the standard library’s `strlen` binding. For C3-only string length, use `key.len`; for C interop, define whether an embedded NUL is valid for the native API.

## Recommended Pattern

```c3
// src/catalog_ffi.c3
module shop::ffi @private;
import libc;

<* @return "Byte length before the first NUL in the catalog key." *>
fn usz catalog_key_len(String key) @public
{
	usz length;
	@pool()
	{
		ZString c_key = key.zstr_tcopy();
		length = libc::strlen(c_key);
	};
	return length;
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Raw String buffer passed directly to C | May lack a NUL terminator | Convert to ZString |
| C retains a temp pointer | Outlives the pool | Keep the borrow synchronous |
| Handwritten ABI type assumptions | Fail on other targets | Reuse the pinned libc declaration |

## Checklist

- Use typed slices outside the boundary.
- Verify the native ABI and signature.
- Keep native buffer lifetime explicit.
- Match owned resources with the release function.

## References

- [C interoperability](https://c3-lang.org/language-common/cinterop/)
- [C3 memory management](https://c3-lang.org/language-common/memory/)
