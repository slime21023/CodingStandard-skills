---
id: c3/errors
title: "Optionals and Faults"
summary: "Use C3 optionals and typed faults for ordinary recoverable failures."
language: c3
topic: errors
tags: [errors, option]
related: [c3/data-and-functions]
snippets: unverified
---

# Optionals and Faults

## Summary

Use C3 optionals and typed faults for ordinary recoverable failures. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this for validation and recoverable I/O. For data and control flow, see [Data and Control Flow](data-and-functions.md).

## Rules

- **SHOULD** Use native C3 T?, void?, and fault for expected recoverable failures.
- **SHOULD** Handle or propagate relevant optional failures; never silently discard them.
- **SHOULD** Use ?? only when a meaningful fallback is part of the function contract.
- **SHOULD** Reserve panic for unrecoverable failures or violated invariants, not ordinary business errors.
- **MUST** Do not introduce a generic Result framework; use a dedicated data type only when structured diagnostic detail is necessary.
- **SHOULD** Preserve the meaning of faults across module and FFI boundaries.

Note: `excuse` declares named values of type `fault`. Propagate with `!` or handle with `if (catch ...)`.

## Recommended Pattern

```c3
// src/discount.c3
module shop::catalog @private;

excuse NEGATIVE_AMOUNT @public, EXCEEDS_PRICE @public;

struct Product @public
{
	String id;
	long price_cents;
}

<* @return "A discounted copy; prices are integer minor units." *>
fn Product? apply_discount(Product product, long amount_cents) @public
{
	if (amount_cents < 0) return NEGATIVE_AMOUNT~;
	if (amount_cents > product.price_cents) return EXCEEDS_PRICE~;
	product.price_cents -= amount_cents;
	return product;
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Force-unwrapping a business outcome | Can terminate the program | Check or propagate the fault |
| Generic foreign Result wrapper | Duplicates native control flow | Use T? and fault |
| Fallback that was never promised | Masks failure | Use ?? only for a meaningful default |

## Checklist

- Give each failure an inspectable fault.
- Check or propagate every optional failure.
- Reserve panic for unrecoverable problems.
- Preserve fault semantics at boundaries.

## References

- [C3 optionals](https://c3-lang.org/language-common/optionals-essential/)
- [C3 excuse declaration change](https://c3-lang.org/blog/c3_0_8_4_last_renaming/)
