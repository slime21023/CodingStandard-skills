---
id: testing/test-delivery
title: Tooling and Reporting
summary: Use the project's existing test setup and report exactly what ran, what failed, and what could not run.
language: any
topic: test-delivery
tags: [testing, tooling, dependencies]
related: [testing/test-scope, testing/test-design]
snippets: unverified
---

# Tooling and Reporting

## Summary

Tests are easier to run and review when they follow the project's established setup. Inspect the commands, use the existing runner, and distinguish observed results from checks you could not run or did not run.

## When to Use

Use this topic when locating test commands, deciding what to deliver without a test setup, or reporting test results. If the question is whether the change calls for a new test, see [When to Test and What to Cover](test-scope.md).

## Rules

- **MUST** reuse the project's existing test framework, layout, and commands, and inspect what a command does before running it.
- **AVOID** adding a dependency solely to write tests.
- **SHOULD** deliver a runnable check script or list the intended test cases with expected results when no test setup exists, and say that no formal tests were run.
- **MUST** report honestly: name what ran and its result, what failed, and what could not be run and why.

## Pitfalls

| Smell | Why | Fix |
| --- | --- | --- |
| A new runner or assertion library is added just for these tests | It adds a dependency and departs from project conventions. | Use the existing runner and assertions. |
| A guessed command bypasses the configured runner | It may not discover the relevant tests or use the intended setup. | Inspect and use the project's command. |
| Planned or blocked tests are reported as passing | The reader cannot tell whether the behavior was verified. | Separate observed outcomes from what was not run and explain why. |

## Checklist

- Inspect the test framework, layout, and commands before writing or running tests.
- Reuse the project's test setup without adding unnecessary dependencies.
- Supply a runnable check script or cases with expected results if no test setup exists.
- Name the commands that actually ran and report their observed results and any failures.
- Identify what could not run and why, and state when no formal tests were run.

## Related

- [When to Test and What to Cover](test-scope.md): Choose the behaviors and cases that need evidence.
- [Test Design](test-design.md): Review how the tests are structured before delivery.
