---
name: python-coding-guidelines
description: Apply concise, data-oriented Python 3.13+ coding standards when creating, modifying, refactoring, testing, or reviewing Python code. Use for module design, public APIs, type hints, Result-based errors, dataclasses, async programming, dependencies, and Code Agent quality checks. Favor functions, immutable data, explicit error flows, minimal abstractions, and readability.
---

# Python Coding Guidelines

Apply these rules to Python code. Follow explicit user requirements and preserve established project conventions where compatible.

## Workflow

1. Inspect relevant code, tests, project configuration, public APIs, Result conventions, and compatibility requirements.
2. Select topics from [the topic index](references/index.md) as described in Topic Retrieval.
3. Make the smallest complete change. Preserve existing API, dependencies, Python version support, Result/exception behavior, and cancellation unless asked to change them.
4. Add or update behavior tests. Run the applicable lint, format, type, and test checks and inspect the diff for unnecessary complexity.
5. Report changes, actual checks and outcomes, and remaining risks.

## Rule Levels

- **MUST**: Required; justify any exception.
- **SHOULD**: The default; adjust only with a concrete reason.
- **AVOID**: Not the default; use only when constraints justify it.

## Core Rules

- **SHOULD** Prefer data structures and independent functions over classes.
- **SHOULD** Keep data flow, dependencies, side effects, and errors explicit.
- **SHOULD** Type public and important internal boundaries; infer obvious local values.
- **MUST** Use one Result model for expected failures and preserve unexpected exceptions.
- **SHOULD** Start with concrete types and minimal abstractions.
- **SHOULD** Prioritize readability, testability, and focused changes.
- **SHOULD** Default to Python 3.13+ for new projects; preserve existing compatibility.
- **MUST** Run applicable lint, format, type, and test checks and report honestly.

**Guiding rule:** Write straightforward typed Python with explicit Result errors, and add classes, abstraction, metaprogramming, or async only when justified.

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
mq '.code("python")' references/errors.md
mq '.yaml | frontmatter | select(self, get("tags") | contains("errors")) | get("id")' references/*.md
```

Without `mq`, open only the selected files or heading ranges. Do not install tools to read these references.
