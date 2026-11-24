# CodingStandard Skills

Agent skills that encode team coding standards, with language-specific coding
guidelines and language-agnostic testing principles.

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

### 1. Interactive Selection (互動式勾選安裝)

In an interactive terminal, `bunx skills add` launches an interactive menu to choose which skills and target agents to install:

```bash
# Remote install from GitHub
bunx skills add slime21023/CodingStandard-skills

# Local install (from inside this repo)
bun run install:skills
# or with Node.js 22.20+ and bundled npm
node scripts/install.mjs
# or call the CLI directly
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

From a local checkout, omit the source to install skills from this repository:

```bash
bun run install:skills --skill go-coding-guidelines python-coding-guidelines
```

To use a different source with the wrapper, pass it before the flags.

Install to specific agents:

```bash
bunx skills add slime21023/CodingStandard-skills -a claude-code cursor
```

Install globally across all projects:

```bash
bunx skills add slime21023/CodingStandard-skills -g
```

Install every skill while keeping agent selection in an interactive terminal:

```bash
bunx skills add slime21023/CodingStandard-skills --skill '*'
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
# or locally with Node.js
node scripts/install.mjs --list
```

For direct CLI calls, `npx skills add <source>` is the Node.js alternative to
`bunx skills add <source>`. The local wrapper defaults to this repository when
you omit `<source>`.

---

## Repository Scripts

If you cloned this repository locally:

```bash
# Interactive skill & agent installer (cleans IDE agent flags)
bun run install:skills

# Validate all skills (frontmatter, naming, and link integrity)
bun run validate

# Validate topic structure (see CONTRIBUTING.md for prerequisites)
python3 scripts/check_topics.py

# List all available skills
bun run skills:list
```

On Windows, run `py -3 scripts/check_topics.py` instead of the `python3` command.

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
scripts/
  install.mjs
  validate.mjs
  check_topics.py
templates/topic.md
package.json
.gitignore
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
3. Run `bun run validate` to check skill metadata and links, then verify
   discovery with `bun run skills:list`.

## Rule Levels

The skills share a common vocabulary:

- **MUST**: required; exceptions need a justification.
- **SHOULD**: the default; adjust only with a concrete reason.
- **AVOID**: not the default; use only when constraints justify it.
- **REVIEW SIGNAL**: a readability prompt for review, never a violation or a numeric limit.
