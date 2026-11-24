---
id: c3/testing
title: "Testing"
summary: "Use native tests to verify public behavior, faults, and boundaries."
language: c3
topic: testing
tags: [testing, errors]
related: [c3/errors]
snippets: unverified
---

# Testing

## Summary

Use native tests to verify public behavior, faults, and boundaries. Use the example as a starting point, not as a substitute for the project contract.

## When to Use

Use this when changing behavior, fixing a defect, or changing memory- or ABI-sensitive work. For optionals and faults, see [Optionals and Faults](errors.md).

## Rules

- **SHOULD** Use native @test for unit tests; include test sources in project.json as appropriate.
- **SHOULD** Cover public APIs, success and failure cases, boundaries, and regressions for fixed bugs.
- **SHOULD** Exercise memory lifetime and FFI-sensitive code with supported safety checks and sanitizers when appropriate.
- **SHOULD** Keep debug safety checks enabled. Verify relevant release targets before delivery.

## Recommended Pattern

Include the implementation from [Optionals and Faults](errors.md#recommended-pattern) and this test in the project sources, and run `c3c test`.

```c3
// src/discount_test.c3
module shop::discount_test;
import shop::catalog;

fn void discount_contract() @test
{
	Product product = { .id = "p1", .price_cents = 500 };
	Product reduced = catalog::apply_discount(product, 200)!!;
	Product free_product = catalog::apply_discount(product, 500)!!;
	assert(reduced.price_cents == 300);
	assert(free_product.price_cents == 0);
	Product? negative = catalog::apply_discount(product, -1);
	if (catch err = negative)
	{
		assert(err == catalog::NEGATIVE_AMOUNT);
	}
	else
	{
		assert(false, "negative discount must fail");
	}
	Product? excessive = catalog::apply_discount(product, 501);
	if (catch err = excessive)
	{
		assert(err == catalog::EXCEEDS_PRICE);
	}
	else
	{
		assert(false, "discount above the price must fail");
	}
}
```

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| Test missing from project sources | Native runner cannot discover it | Include the test in project.json |
| Test compares formatted errors | Diagnostic edits break behavior tests | Compare the fault |
| Release-only checks | Miss useful lifetime diagnostics | Keep debug checks and suitable sanitizers |

## Checklist

- Exercise public success and exact-price boundaries.
- Assert both expected faults.
- Add regression cases for fixes.
- Check lifetimes and ABI-sensitive code with supported diagnostics.

## References

- [C3 build commands](https://c3-lang.org/build-your-project/build-commands/)
- [C3 optionals](https://c3-lang.org/language-common/optionals-essential/)
