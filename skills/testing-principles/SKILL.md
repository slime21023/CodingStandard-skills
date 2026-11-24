---
name: testing-principles
description: Apply language-agnostic testing principles whenever tests are written, added, updated, run, or reviewed, and whenever a feature, bug fix, refactor, or public API change should be covered by tests, in any programming language or framework. Covers when tests are required, what to cover, deterministic and isolated test design, test doubles, reusing project conventions, and honest reporting of what ran.
---

# Testing Principles

Write tests that prove behavior, fail for one clear reason, and run the same way every time. These principles are independent of language and framework; follow the project's existing test tooling and conventions for the details.

## Workflow

1. Inspect existing tests, the test runner configuration, and naming and layout conventions before writing anything.
2. Select topics from [the topic index](references/index.md) as described in Topic Retrieval.
3. Decide whether the change requires tests and write or update them for the observable cases in [When to Test and What to Cover](references/test-scope.md).
4. Run the relevant tests with the project's own command. For a bug fix, confirm the new test fails without the fix and passes with it.
5. Review the tests against the selected topic checklists.
6. Report which tests were added, which commands ran and their results, and any result you could not obtain and why.

Follow explicit user requirements and established project conventions where they conflict with these defaults.

## Rule Levels

- **MUST:** Required; state the reason for any exception.
- **SHOULD:** Default approach; depart only for a concrete benefit.
- **AVOID:** Not the default; use only when constraints justify it.

## Core Rules

- **MUST** test new public behavior and bug fixes; prove a regression test fails without the fix and passes with it.
- **MUST** test observable behavior through public interfaces.
- **MUST** keep tests deterministic and independent.
- **MUST** reuse the project's test framework, layout, and commands; inspect commands before running them.
- **MUST** report what ran and its result, what failed, and what could not run and why.
- **SHOULD** give each test one reason to fail.

## Topic Retrieval

1. Open [references/index.md](references/index.md) and choose at most three topics by summary and tags.
2. Read each selected topic's `Summary`, `Rules`, and `Checklist` first.
3. Read `Recommended Pattern` when writing code, `Pitfalls` when reviewing or debugging, and `Tooling` or `Dependencies` when changing build or dependency setup.
4. Follow `related` IDs only when the selected topics do not answer the task.
5. Never load every topic file.

## Extract Only What You Need

If `mq` is available, run these from this skill's directory:

```shell
mq -A 'section::by_title("Rules")' references/test-design.md
mq -A 'section::by_title("Checklist")' references/test-design.md
mq '.yaml | frontmatter | select(self, get("tags") | contains("testing")) | get("id")' references/*.md
```

Without `mq`, open only the selected files or heading ranges. Do not install tools to read these references.
