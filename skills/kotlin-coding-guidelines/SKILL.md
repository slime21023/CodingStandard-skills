---
name: kotlin-coding-guidelines
description: Apply moderately conservative, general-purpose Kotlin 1.9+ coding guidelines when writing, editing, refactoring, or reviewing Kotlin (.kt, .kts) code. Follow official Kotlin formatting and the v0.3 rules for names, types, null safety, functions, control flow, lambdas, scope functions, collections, idioms, classes, and exceptions. Distinguish MUST from SHOULD and never convert code-review signals into numerical limits.
---

# Kotlin Coding Guidelines

Apply the **general Kotlin v0.3** standard to Kotlin 1.9+ code; preserve the project's existing Kotlin version and compatibility requirements. Prioritize explicit intent, readable control flow, and understandable abstraction over clever brevity.

## Authoritative rules

Read [references/kotlin-v0.3.md](references/kotlin-v0.3.md) **in full** before writing, editing, refactoring, or reviewing Kotlin code. It contains all eight normative chapters, exceptions, examples, and the four Code Review signals. When rules appear to conflict, use the full reference and official Kotlin Coding Conventions as the source of truth.

- **MUST:** Follow by default; make an exception only for a clear language, interoperability, or technical constraint.
- **SHOULD:** Prefer in ordinary cases; depart when the alternative is demonstrably clearer in context.
- **Review Signal:** Discuss clarity, not compliance. Never impose numerical thresholds.

## Workflow

1. Identify the Kotlin files and relevant code to create, change, or review.
2. Read the normative reference. Follow the project-specific contract and any user requirements without adding unsupported architectural mandates.
3. While coding, apply every relevant MUST and use SHOULD to guide judgment.
4. While reviewing, report actual MUST issues separately from optional SHOULD improvements. Describe concrete consequences; avoid generic style complaints.
5. Preserve behavior, public API contracts, and intentional interop behavior during refactoring. Do not expand scope to architecture or engineering practices.
6. After editing, run the project's existing build, lint, and test commands when available. Report what actually ran; never claim checks passed unless executed.

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

## Explicit exclusions

This skill does not prescribe architecture, module boundaries, DI, design patterns, tests, CI, lint selection, performance targets, or Agent workflow policy. Leave those decisions to the developer and project; running the checks the project already defines is still required.
