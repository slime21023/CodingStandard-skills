---
id: testing/test-scope
title: When to Test and What to Cover
summary: Decide when tests are required and which observable behaviors and edge cases to cover.
language: any
topic: test-scope
tags: [testing, public-api, review]
related: [testing/test-design, testing/test-delivery]
snippets: unverified
---

# When to Test and What to Cover

## Summary

A change needs tests that establish what a caller can observe, not how the implementation works. Cover new public behavior, reproduce defects, and use relevant edge cases to make the contract explicit. A pure refactor can rely on existing tests if they actually exercise the changed code.

## When to Use

Use this topic when planning tests for a feature, bug fix, contract change, or refactor, or when reviewing the cases a suite covers. If the cases are already chosen and you need to make them deterministic and independent, see [Test Design](test-design.md).

## Rules

- **MUST** add or update tests when adding public behavior or fixing a bug.
- **MUST** make a bug-fix test reproduce the defect: it fails before the fix and passes after.
- **SHOULD** add or update tests when changing a public contract, error behavior, or boundary handling.
- **SHOULD** rely on existing tests for a pure refactor, but run them first and confirm they exercise the changed code; add tests where they do not.
- **MUST** test observable behavior through the public interface: inputs, outputs, and externally visible effects.
- **SHOULD** cover the normal path, boundary values, expected failure paths, and at least one invalid input for each behavior.
- **SHOULD** add malformed-input and boundary cases for parsers and other code that handles untrusted input; use property-based or fuzz testing when the language has mature tooling for it.
- **AVOID** testing private implementation details, so refactors do not break tests without changing behavior.

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| A test calls a private helper | Renaming or replacing the helper can break the test without changing behavior. | Exercise the public operation and assert its outcome. |
| A test snapshots a private data structure | The snapshot freezes an internal representation, not a public contract. | Assert the returned value or another visible effect. |
| A test requires a private call sequence | An equivalent implementation can reorder or bypass those calls. | Assert the externally visible effect of the operation. |

## Checklist

- Add or update tests for new public behavior and bug fixes.
- Confirm the regression test fails without the fix and passes with it.
- Assert observable behavior through the public interface.
- Cover normal, boundary, expected-failure, and invalid-input cases where relevant.
- Include malformed cases for parsers and other untrusted-input handlers.
- Run existing tests before a pure refactor and fill gaps in coverage of the changed code.

## Related

- [Test Design](test-design.md): Turn chosen cases into deterministic, focused tests.
- [Tooling and Reporting](test-delivery.md): Run the regression and related tests and report the observed results.
