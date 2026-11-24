---
id: c3/resources-and-memory
title: "Memory and Resources"
summary: "Keep temporary allocations scoped and give returned storage an explicit owner."
language: c3
topic: resources-and-memory
tags: [ownership, memory, resources]
related: [c3/unsafe-and-ffi]
snippets: unverified
---

# Memory and Resources

## Summary

Keep temporary allocations scoped and give returned storage an explicit owner. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when a file buffer or allocator crosses an API boundary. For pointers and ffi, see [Pointers and FFI](unsafe-and-ffi.md).

## Rules

- **SHOULD** Prefer stack values, then scoped temporary allocation with @pool, then explicit allocators for long-lived dynamic data.
- **SHOULD** Make allocation and release responsibilities clear. Name allocator arguments allocator; prefer allocator-first public APIs.
- **SHOULD** Use defer for deterministic cleanup of owned resources.
- **MUST** Never allow a pointer or slice to temporary memory to escape its valid @pool lifetime.
- **MUST** Never pass temporary references to another thread if their lifetime cannot be guaranteed.
- **SHOULD** Document whether returned pointers and slices are borrowed or owned, and who releases owned allocations.
- **SHOULD** Treat borrowed/owned as explicit contracts; C3 does not enforce Rust-style ownership rules.
- **AVOID** Avoid needless heap allocation or copying, but profile before complex optimization.

Note: If no intermediate work needs temporary storage, use `file::load(allocator, path)` directly to avoid the illustrative copy.

## Recommended Pattern

```c3
// src/catalog_load.c3
module shop::catalog @private;
import std::io::file;

<*
 @return "Catalog bytes allocated by allocator; caller frees them."
 @return? file::load!
*>
fn String? load_catalog(Allocator allocator, String path) @public
{
	String owned;
	@pool()
	{
		char[] bytes = file::load(tmem, path)!;
		owned = ((String)bytes).copy(allocator);
	};
	return owned;
}

fn sz? catalog_size(Allocator allocator, String path) @public
{
	String catalog = load_catalog(allocator, path)!;
	defer catalog.free(allocator);
	return catalog.len;
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Returning a slice allocated in @pool | Refers to freed storage on exit | Copy only when ownership escapes |
| Allocator hidden behind a return | Caller cannot release bytes correctly | Pass an explicit allocator |
| Deferred cleanup uses the wrong allocator | Violates ownership | Release using the supplied allocator |

## Checklist

- Prefer stack storage where practical.
- Keep @pool allocations within their lifetime.
- Name owners and allocators in API contracts.
- Defer cleanup and preserve failure behavior.

## References

- [C3 memory management](https://c3-lang.org/language-common/memory/)
- [C3 file API](https://github.com/c3lang/c3c/blob/v0.8.6/lib/std/io/file.c3)
