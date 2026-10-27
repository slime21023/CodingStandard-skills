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
| `nim-coding-guidelines` | Nim 2.2+ | Data-oriented modules and public APIs, Result/Option/Exception error handling, metaprogramming, memory management |
| `rust-coding-guidelines` | Rust 2024+ | Explicit borrowing, concrete types, minimal APIs, traits, unsafe code, async/concurrency |

## Installation

Install every skill in this repository:

```bash
bunx skills add <owner>/<repo>
```

Install a single skill:

```bash
bunx skills add <owner>/<repo> --skill go-coding-guidelines
```

List the skills without installing:

```bash
bunx skills add <owner>/<repo> --list
```

Install from a local checkout:

```bash
bunx skills add /path/to/CodingStandard-skills
```

Replace `<owner>/<repo>` with this repository's GitHub path. `npx skills add`
works the same way.

## Repository Layout

```text
skills/
  <skill-name>/
    SKILL.md          # Entry point: frontmatter (name, description) + workflow
    references/       # Optional: detailed guidelines loaded on demand
    agents/           # Optional: agent interface metadata (openai.yaml)
    assets/           # Optional: icons and other static files
```

## Adding a Skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter containing `name`
   (matching the directory) and `description` (when the skill should trigger).
2. Put long-form rules in `references/` and link to them from `SKILL.md`.
3. Verify discovery with `bunx skills add . --list`.

## Rule Levels

The skills share a common vocabulary:

- **MUST**: required; exceptions need a justification.
- **SHOULD**: the default; adjust only with a concrete reason.
- **AVOID**: not the default; use only when constraints justify it.
