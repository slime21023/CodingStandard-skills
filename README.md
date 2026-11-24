# CodingStandard Skills

Agent skills that encode team coding standards. Each skill tells a coding agent
how to write, refactor, test, and review code in one language.

## Skills

| Skill | Language | Focus |
| --- | --- | --- |
| `c3-coding-guidelines` | C3 | Data-oriented code, native Optional/Fault errors, allocators and memory safety, FFI, generics, macros |
| `cpp-coding-guidelines` | C++20 | Data and functions first, explicit ownership and RAII, Expected with appropriate exceptions, CMake-based C++20 Modules |
| `develop-readable-typescript` | TypeScript | Readable, type-safe code; `Result` / discriminated unions for expected failures; exceptions for unexpected ones |
| `go-coding-guidelines` | Go | Concrete types, small consumer-owned interfaces, explicit errors, safe concurrency |
| `kotlin-coding-guidelines` | Kotlin 1.9+ | Official conventions, explicit null safety, readable control flow, restrained scope functions and idioms, precise exceptions |
| `nim-coding-guidelines` | Nim 2.2+ | Data-oriented modules and public APIs, Result/Option/Exception error handling, metaprogramming, memory management |
| `python-coding-guidelines` | Python 3.13+ | Functions and immutable data, type hints, Result-based error flows, dataclasses, async programming, minimal abstractions |
| `rust-coding-guidelines` | Rust 2024+ | Explicit borrowing, concrete types, minimal APIs, traits, unsafe code, async/concurrency |
| `testing-principles` | Any | Language-agnostic testing: when tests are required, what to cover, deterministic design, test doubles, honest reporting |

Each skill ships one-topic-per-file references under `references/`, queryable with mq.

## Installation

Install every skill in this repository:

```bash
bunx skills add slime21023/CodingStandard-skills
```

Install a single skill:

```bash
bunx skills add slime21023/CodingStandard-skills --skill go-coding-guidelines
```

List the skills without installing:

```bash
bunx skills add slime21023/CodingStandard-skills --list
```

`npx skills add` works the same way.

## Repository Layout

```text
skills/
  <skill-name>/
    SKILL.md
    references/
      index.md
      <topic>.md
    agents/
    assets/           # Optional
templates/topic.md
scripts/check_topics.py
CONTRIBUTING.md
AGENTS.md
```

## Query Topics with mq

Install [`mq`](https://github.com/harehare/mq) to query topics from the repository root. It is optional for using a skill. To find the error-handling topic for each language and read the Rust example:

```bash
mq '.yaml | frontmatter | select(self, get("topic") == "errors") | get("id")' skills/*/references/*.md
mq -A 'section::by_title("Recommended Pattern")' skills/rust-coding-guidelines/references/errors.md
```

See [the mq recipes](AGENTS.md#mq-queries) for PowerShell and queries by tag and section. The [topic checker](CONTRIBUTING.md#checking-topics) validates document structure without compiling snippets.

## Adding a Skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter containing `name`
   (matching the directory) and `description` (when the skill should trigger).
2. Create topics from [`templates/topic.md`](templates/topic.md) per
   [`CONTRIBUTING.md`](CONTRIBUTING.md), list them in `references/index.md`,
   and run the [topic checker](CONTRIBUTING.md#checking-topics).
3. Verify discovery with `bunx skills add . --list`.

## Rule Levels

The skills share a common vocabulary:

- **MUST**: required; exceptions need a justification.
- **SHOULD**: the default; adjust only with a concrete reason.
- **AVOID**: not the default; use only when constraints justify it.
- **REVIEW SIGNAL**: a readability prompt for review, never a violation or a numeric limit.
