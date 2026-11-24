---
name: kotlin-coding-guidelines
description: Apply moderately conservative, general-purpose Kotlin 1.9+ coding guidelines when writing, editing, refactoring, or reviewing Kotlin (.kt, .kts) code. Follow official Kotlin formatting and the v0.3 rules for names, types, null safety, functions, control flow, lambdas, scope functions, collections, idioms, classes, and exceptions. Distinguish MUST from SHOULD and never convert code-review signals into numerical limits.
---

# Kotlin Coding Guidelines

Apply the **general Kotlin v0.3** standard to Kotlin 1.9+ code; preserve the project's existing Kotlin version and compatibility requirements. Prioritize explicit intent, readable control flow, and understandable abstraction over clever brevity.

## Workflow

1. Identify the Kotlin files and relevant code to create, change, or review.
2. Select topics from [the topic index](references/index.md) as described in Topic Retrieval. Follow the project-specific contract and any user requirements without adding unsupported architectural mandates.
3. While coding, apply every relevant MUST and use SHOULD to guide judgment.
4. While reviewing, report actual MUST issues separately from optional SHOULD improvements. Describe concrete consequences; avoid generic style complaints.
5. Preserve behavior, public API contracts, and intentional interop behavior during refactoring. Do not expand scope to architecture or engineering practices.
6. After editing, run the project's existing build, lint, and test commands when available. Report what actually ran; never claim checks passed unless executed.

## Rule Levels

- **MUST:** Follow by default; make an exception only for a clear language, interoperability, or technical constraint, and be able to explain it.
- **SHOULD:** Prefer in ordinary cases; depart when the alternative is demonstrably clearer in context.
- **AVOID:** Not the default; use only when constraints justify it.
- **REVIEW SIGNAL:** Discuss clarity, not compliance. Never impose numerical thresholds.

## Core Rules

- **MUST** use official Kotlin formatting.
- **MUST** make names match their effects.
- **MUST** declare `T?` only when absence is valid, and do not mask unverified nulls with `!!`.
- **MUST** not swallow exceptions.
- **MUST** rethrow `CancellationException` if caught.
- **MUST** give scope functions an unambiguous receiver and return value.
- **SHOULD** use `val` by default.
- **SHOULD** use exhaustive `when` for finite states without a catch-all `else`.

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
mq '.code("kotlin")' references/errors.md
mq '.yaml | frontmatter | select(self, get("tags") | contains("cancellation")) | get("id")' references/*.md
```

Without `mq`, open only the selected files or heading ranges. Do not install tools to read these references.

## Decision priorities

1. Correctness and explicit semantic contracts.
2. Kotlin official conventions.
3. Clear names, shallow comprehensible control flow, and visible side effects.
4. Appropriate use of Kotlin idioms and scope functions.
5. Concision only when it does not obscure meaning.

## Code Review signals — not hard limits

- Function length: Can the reader grasp inputs, steps, output, and side effects?
- Nesting depth: Would guard clauses, named conditions, or intermediate values help?
- Scope Function count: Are receivers (`this`/`it`) and returns unmistakable?
- Abstraction layers: Does each layer add meaning or create navigation overhead?

Do not mandate fixed counts, line limits, or abstraction-depth thresholds.

Judge whether the next reader can easily understand and modify the code, not whether it uses the most Kotlin idioms or fits a line count.

## Explicit exclusions

This skill does not prescribe architecture, module or package boundaries, dependency injection, design patterns, testing strategy, CI, lint selection, performance targets, or team or agent workflows. Leave those decisions to the developer and project; running the checks the project already defines is still required.
