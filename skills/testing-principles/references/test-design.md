---
id: testing/test-design
title: Test Design
summary: Write deterministic and independent tests with focused assertions and test doubles only at real boundaries.
language: any
topic: test-design
tags: [testing, review]
related: [testing/test-scope, testing/test-delivery]
snippets: unverified
---

# Test Design

## Summary

Tests should fail when behavior changes, not when execution order, ambient state, or incidental output changes. Control external inputs, keep pure logic real, and give each test a clear scenario and one reason to fail.

## When to Use

Use this topic when implementing or reviewing tests, especially when they share state, call external services, or fail intermittently. If the question is which behaviors or edge cases to test, see [When to Test and What to Cover](test-scope.md).

## Rules

- **MUST** keep tests deterministic and independent: control time, randomness, network, filesystem, and environment; never rely on execution order or shared mutable state between tests.
- **SHOULD** give each test one reason to fail and a name that states the scenario and expected outcome.
- **SHOULD** structure each test as setup, action, and assertion, with assertions that make a failure self-explanatory.
- **SHOULD** replace only real boundaries such as network, storage, clocks, and external services with test doubles, and keep pure logic real; prefer simple fakes over interaction-verifying mocks.
- **SHOULD** assert error kind or code rather than full message text.
- **AVOID** asserting on incidental details such as log output, ordering that is not part of the contract, or exact formatting.
- **AVOID** editing a test only to make it pass, skipping or deleting failing tests, and chasing coverage percentages without meaningful assertions.

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| An assertion checks incidental log output or formatting | Copy edits can break the test without changing the contract. | Assert the outcome or error kind instead. |
| A test requires ordering outside the contract | It rejects valid outputs in a different order. | Compare the items without requiring an order. |
| A failing test is skipped, deleted, or weakened just to make it pass | The behavior it checked no longer has meaningful protection. | Diagnose the failure; fix the implementation or correct an assertion that disagrees with the contract. |
| Coverage rises without meaningful assertions | Executing a line does not prove that behavior is correct. | Assert the outcome each new case is meant to establish. |

## Checklist

- Control time, randomness, network, filesystem, and environment where they affect the outcome.
- Remove hidden shared state and dependencies on test order.
- Name the scenario and expected outcome, and give each test one reason to fail.
- Separate setup, action, and assertion, and make failures self-explanatory.
- Use doubles only at real boundaries and keep pure logic real.
- Assert error kinds or codes rather than incidental details.

## Related

- [When to Test and What to Cover](test-scope.md): Identify the public behavior the assertions should establish.
- [Tooling and Reporting](test-delivery.md): Use the existing runner and report the resulting evidence.
