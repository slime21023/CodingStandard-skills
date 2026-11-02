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

## Installation

### 1. Interactive Selection (互動式勾選安裝)

In an interactive terminal, `bunx skills add` launches an interactive menu to choose which skills and target agents to install:

```bash
# Remote install from GitHub
bunx skills add slime21023/CodingStandard-skills

# Local install (from inside this repo)
bun run install:skills
# or
bunx skills add .
```

You will be prompted to:
1. **Select skills**: Toggle specific skills (`Space` to toggle, `Enter` to confirm).
2. **Select agents**: Choose target AI agents (Claude Code, Cursor, Windsurf, Codex, Antigravity, GitHub Copilot, etc.).
3. **Scope**: Choose between `Project` (`.agents/skills/`) or `Global` (`~/.<agent>/skills/`).

> **Note for AI IDE Terminals (Cursor, Antigravity, etc.)**:
> When running inside an AI Agent environment, the default `skills` CLI auto-detects the agent and switches to non-interactive mode (auto-installing all skills). Run `bun run install:skills` or use the CLI flags below to force specific selections.

---

### 2. Selective Installation via Flags (指定特定 Skill 與 Agent)

Install specific skills:

```bash
bunx skills add slime21023/CodingStandard-skills --skill go-coding-guidelines python-coding-guidelines
```

Install to specific agents:

```bash
bunx skills add slime21023/CodingStandard-skills -a claude-code cursor
```

Install globally across all projects:

```bash
bunx skills add slime21023/CodingStandard-skills -g
```

Install all skills to all agents non-interactively:

```bash
bunx skills add slime21023/CodingStandard-skills --all
```

---

### 3. List Available Skills (列出可用 Skills)

Preview skills and their descriptions without installing:

```bash
bunx skills add slime21023/CodingStandard-skills --list
# or locally
bun run skills:list
```

`npx skills add` works identically if using Node.js / npm.

---

## Repository Scripts

If you cloned this repository locally:

```bash
# Interactive skill & agent installer (cleans IDE agent flags)
bun run install:skills

# Validate all skills (frontmatter, naming, and link integrity)
bun run validate

# List all available skills
bun run skills:list
```

## Repository Layout

```text
skills/
  <skill-name>/
    SKILL.md          # Entry point: frontmatter (name, description) + workflow
    references/       # Optional: detailed guidelines loaded on demand
    agents/           # Optional: agent interface metadata (openai.yaml)
    assets/           # Optional: icons and other static files
scripts/
  install.mjs         # Interactive installer wrapper
  validate.mjs        # Skill schema and link validator
package.json          # Node/Bun package definition and scripts
.gitignore            # Prevents committing local installed agent skills
```

## Adding a Skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter containing `name`
   (matching the directory) and `description` (when the skill should trigger).
2. Put long-form rules in `references/` and link to them from `SKILL.md`.
3. Verify discovery with `bun run validate` and `bun run skills:list`.

## Rule Levels

The skills share a common vocabulary:

- **MUST**: required; exceptions need a justification.
- **SHOULD**: the default; adjust only with a concrete reason.
- **AVOID**: not the default; use only when constraints justify it.
