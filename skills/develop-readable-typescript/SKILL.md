---
name: develop-readable-typescript
description: >-
  Apply readable, type-safe TypeScript engineering practices when implementing,
  modifying, debugging, refactoring, or reviewing TypeScript (.ts and .tsx)
  code. Use for tasks involving naming, control flow, functional and
  data-oriented design, error handling, module boundaries, and code quality.
---

# Develop Readable TypeScript

Write clear, type-safe, maintainable TypeScript. Optimize for understanding and
correctness rather than brevity, cleverness, or architectural ceremony.

## Workflow

1. Inspect relevant files, package and TypeScript configurations, lint setup, tests, and repository instructions.
2. Select topics from [the topic index](references/index.md) as described in Topic Retrieval.
3. Identify behavior, data contracts, and failure paths. Make the smallest coherent change within project constraints; do not add dependencies solely for style.
4. Use available project checks. Inspect script meaning before running them, and review names, side effects, types, promises, errors, tests, and scope.
5. Report what changed, checks that passed or failed, any unavailable checks, and justified exceptions.

## Rule Levels

- **MUST**: Required; justify any exception.
- **SHOULD**: The default; adjust only with a concrete reason.
- **AVOID**: Not the default; use only when constraints justify it.

## Core Rules

- **MUST** Preserve strict mode and public contracts.
- **MUST** Do not use any, assertions, or non-null assertions to evade checks.
- **MUST** Validate external input at runtime.
- **SHOULD** Prefer data and functions; use classes for state, lifecycle, or framework contracts.
- **MUST** Use Result or discriminated unions for expected failures, and exceptions for unexpected ones.
- **MUST** Await, return, or explicitly handle every Promise.
- **SHOULD** Use guard clauses; avoid nested ternaries.
- **MUST** Verify with the project checks, or use tsc --strict --noEmit without a project configuration.

## Topic Retrieval

1. Open [references/index.md](references/index.md) and choose at most three topics by summary and tags.
2. Read each selected topic's `Summary`, `Rules`, and `Checklist` first.
3. Read `Recommended Pattern` when writing code, `Pitfalls` when reviewing or debugging, and `Tooling` or `Dependencies` when changing build or dependency setup.
4. Follow `related` IDs only when the selected topics do not answer the task.
5. Never load every topic file.

## Extract Only What You Need

If `mq` is available, run these from this skill's directory:

```shell
mq -A 'section::by_title("Rules")' references/errors.md
mq -A 'section::by_title("Checklist")' references/errors.md
mq '.code("typescript")' references/errors.md
mq '.yaml | frontmatter | select(self, get("tags") | contains("errors")) | get("id")' references/*.md
```

Without `mq`, open only the selected files or heading ranges. Do not install tools to read these references.

## Task-Specific Checks

### Implementation
- Identify success, expected failure, and unexpected exception paths.
- Add or update behavior-focused tests, including meaningful failure cases.
- Avoid introducing a design pattern without a concrete need.

### Refactoring
- Preserve observable behavior and API contracts, including thrown error
  types and messages; report any unavoidable change explicitly.
- Prefer narrow changes that improve naming, branches, or dependencies.
- Retain necessary stateful and framework patterns.

### Code Review
- Prioritize correctness, unsafe types, hidden side effects, error handling,
  unhandled Promises, unnecessary abstractions, and missing tests.
- Give actionable findings with precise locations and reasons.
- Distinguish material defects from optional stylistic suggestions.
