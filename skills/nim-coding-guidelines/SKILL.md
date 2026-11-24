---
name: nim-coding-guidelines
description: Apply concise, data-oriented Nim 2.2+ coding standards when creating, editing, refactoring, testing, or reviewing Nim (.nim) and Nimble (.nimble) code. Use for Nim module and public API design, Result/Option/Exception error handling, metaprogramming, memory management, and Code Agent code quality checks.
---

# Nim Coding Guidelines

Apply these rules as project defaults. Honor explicit user requirements and established repository conventions when they conflict; make significant deviations visible rather than silently rewriting unrelated code. Prefer clear Nim idioms to patterns copied from other languages.

## Workflow

1. Inspect the affected Nimble configuration, modules, exports, tests, and local conventions.
2. Select topics from [the topic index](references/index.md) as described in Topic Retrieval.
3. Make the smallest focused change. Reuse existing data and packages; avoid speculative layers or dependencies. Preserve public and failure contracts unless the task changes them.
4. Add or update tests for changed behavior, errors, and boundaries. Run relevant semantic, style, test, and compilation checks.
5. Report changes, justified abstractions or dependencies, actual checks, and limits.

## Rule Levels

- **MUST**: Required; justify any exception.
- **SHOULD**: The default; adjust only with a concrete reason.
- **AVOID**: Not the default; use only when constraints justify it.

## Core Rules

- **MUST** Use Nim 2.2+ and ORC; do not change memory management or disable checks without measured justification.
- **MUST** Follow NEP-1.
- **SHOULD** Prefer value objects and use ref only for identity or reference semantics.
- **SHOULD** Use func for pure calculations and proc for effects.
- **MUST** Use Option for absence, results.Result for expected failures, and exceptions for unexpected failures.
- **MUST** Handle every Result and Future.
- **SHOULD** Prefer functions to generics, then templates and macros only as necessary.
- **SHOULD** Export only necessary symbols.
- **MUST** Run applicable nim check and nimble test commands and report honestly.

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
mq '.code("nim")' references/errors.md
mq '.yaml | frontmatter | select(self, get("tags") | contains("errors")) | get("id")' references/*.md
```

Without `mq`, open only the selected files or heading ranges. Do not install tools to read these references.
