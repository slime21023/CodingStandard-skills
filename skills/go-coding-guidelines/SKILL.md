---
name: go-coding-guidelines
description: Apply idiomatic, concise Go coding standards when creating, modifying, refactoring, testing, or reviewing Go (.go) code, and when designing Go packages, struct and method APIs, interfaces, error handling, or concurrency. Favor data and functions, concrete types, simple packages, explicit errors, and readable Code Agent output.
---

# Go Coding Guidelines

Create simple, explicit and maintainable Go code. Follow the user's accepted decisions: **data and independent functions first; interfaces only when necessary; package design starts simple and grows by real functionality**. This skill applies to implementation and code review, not to a mandatory project architecture.

## Workflow

1. Inspect repository instructions, `go.mod`, package boundaries, nearby code, and tests. Preserve existing contracts and local conventions unless asked to change them.
2. Select topics from [the topic index](references/index.md) as described in Topic Retrieval.
3. Make the smallest coherent change. Preserve unrelated code, public behavior, and dependencies.
4. Handle errors, cancellation, and resource lifetimes explicitly. Add or update meaningful tests for changed behavior.
5. Apply the selected checklists, format touched files, and run applicable checks. Report what ran, any limitations, and justified departures.

**Review-only or diagnosis requests do not authorize edits.** Report grounded findings in severity order and cite file locations; separate optional style observations from correctness issues.

## Rule Levels

- **MUST**: Non-negotiable for applicable code.
- **SHOULD**: Default approach; depart only for a concrete benefit or repository convention.
- **AVOID**: Not the default; use only if constraints justify the complexity.

## Core Rules

- **MUST** Format touched Go files with `gofmt`.
- **MUST** Use concrete types until a consumer needs a contract.
- **MUST** Use native `(T, error)` for ordinary failures, not a generic Result.
- **MUST** Handle or propagate every error.
- **MUST** Give goroutines an owner and termination strategy; cancel or join as appropriate and synchronize shared data.
- **SHOULD** Prefer data and independent functions; use methods for type-owned behavior.
- **SHOULD** Start packages small and split by real capability.
- **MUST** Run applicable checks when possible and report honestly.

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
mq '.code("go")' references/errors.md
mq '.yaml | frontmatter | select(self, get("tags") | contains("errors")) | get("id")' references/*.md
```

Without `mq`, open only the selected files or heading ranges. Do not install tools to read these references.
