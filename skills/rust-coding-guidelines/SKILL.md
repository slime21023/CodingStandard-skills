---
name: rust-coding-guidelines
description: Apply clear, idiomatic Rust 2024+ Stable coding standards when creating, editing, refactoring, testing, reviewing, or designing Rust (.rs) code, Cargo packages, modules, public APIs, ownership, traits, errors, unsafe code, and async/concurrency. Favor data and functions, explicit borrowing, concrete types, minimal APIs, and readable Code Agent output.
---

# Rust Coding Guidelines

Apply these standards to Rust work. Follow explicit user requirements and supported project constraints first.

## Workflow

1. Inspect relevant code and tests, Cargo.toml, edition, MSRV, features, and dependencies.
2. Select topics from [the topic index](references/index.md) as described in Topic Retrieval.
3. Make the smallest coherent change; respect conventions and public compatibility. Do not add speculative layers, abstractions, dependencies, or async.
4. Use idiomatic, descriptive code. Add focused tests and explain new dependencies, unsafe invariants, runtime coupling, or public API changes.
5. Run applicable checks and state what passed, what failed, and what could not run.

## Rule Levels

- **MUST**: Required; justify any exception.
- **SHOULD**: The default; adjust only with a concrete reason.
- **AVOID**: Not the default; use only when constraints justify it.

## Core Rules

- **MUST** Use Edition 2024, Stable Rust, and a declared MSRV of at least 1.85 for new projects; do not add nightly-only features.
- **SHOULD** Prefer struct and enum with functions; keep APIs private by default.
- **SHOULD** Borrow first and clone only for a clear ownership reason.
- **SHOULD** Use concrete types before traits or generics.
- **MUST** Use Result for recoverable failure and Option for absence; propagate clearly and avoid unwrap in ordinary production paths.
- **SHOULD** Stay synchronous by default and let the application own any runtime.
- **MUST** Document unsafe invariants with SAFETY comments; do not use unsafe to evade ownership.
- **MUST** Do not cure compiler errors with gratuitous clones, shared locks, or unsafe.
- **MUST** Run applicable formatting, Clippy, tests, and docs checks and report honestly.

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
mq '.code("rust")' references/errors.md
mq '.yaml | frontmatter | select(self, get("tags") | contains("errors")) | get("id")' references/*.md
```

Without `mq`, open only the selected files or heading ranges. Do not install tools to read these references.
