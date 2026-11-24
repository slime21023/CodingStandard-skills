---
name: c3-coding-guidelines
description: Apply concise, data-oriented C3 coding standards when creating, editing, refactoring, testing, or reviewing C3 (.c3) code and C3 project configurations. Covers naming, structs and functions, modules, public APIs, native Optional/Fault errors, allocators, memory safety, FFI, generics, interfaces, macros, testing, dependencies, and Code Agent behavior.
---

# C3 Coding Guidelines

Apply these rules as project defaults. Honor explicit user instructions and established repository conventions when they conflict. Prefer idiomatic C3 to patterns copied from other languages.

## Workflow

1. Inspect relevant modules, project.json, stable compiler version, public APIs, instructions, and tests.
2. Select topics from [the topic index](references/index.md) as described in Topic Retrieval.
3. Make the smallest focused change. Reuse existing structures and preserve public contracts; do not add abstractions or dependencies without a real need.
4. Verify syntax, faults, pointer lifetimes, and allocator ownership. Add behavior tests and run available native build, test, and safety checks.
5. Report changes, any justified abstraction or dependency, exact outcomes, and remaining risks or unverified checks.

## Rule Levels

- **MUST**: Required; justify any exception.
- **SHOULD**: The default; adjust only with a concrete reason.
- **AVOID**: Not the default; use only when constraints justify it.

## Core Rules

- **MUST** Pin a verified stable compiler and verify unfamiliar syntax against that release.
- **SHOULD** Prefer simple structs and ordinary functions.
- **MUST** Use native T? and fault, handle or propagate failures, and do not add a generic Result framework.
- **MUST** State allocation and release ownership; never let temporary memory escape its pool.
- **SHOULD** Keep modules private by default.
- **AVOID** Avoid interfaces, generics, and macros without a demonstrated need.
- **MUST** Confine justified raw pointers and ABI details to small auditable boundaries.
- **MUST** Run applicable c3c builds and tests and report honestly.

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
mq '.code("c3")' references/errors.md
mq '.yaml | frontmatter | select(self, get("tags") | contains("errors")) | get("id")' references/*.md
```

Without `mq`, open only the selected files or heading ranges. Do not install tools to read these references.
