# Agent instructions

## Purpose

This repository provides English coding standards and focused examples for coding agents. Each skill bundles its own catalog and topic files. The examples are marked `unverified`: the repository checks their document structure, not compilation.

## Retrieval Protocol

Apply this protocol from the installed skill directory, not from the project being edited:

1. Open `references/index.md` and choose at most three topics by summary and tags.
2. Read each selected topic's `Summary`, `Rules`, and `Checklist` first.
3. Read `Recommended Pattern` when writing code, `Pitfalls` when reviewing or debugging, and `Tooling` or `Dependencies` when changing build or dependency setup.
4. Follow `related` IDs only when the selected topics do not answer the task.
5. Never load every topic file.

When `mq` is unavailable, use the catalog and a file reader to open only the selected files or heading ranges. Do not install tools just to read installed references.

## mq Queries

Run these examples from the repository root with [`mq`](https://github.com/harehare/mq). The queries match metadata values and exact headings; they do not rank results by relevance. Catalog files have no front matter, so metadata queries skip them.

### List topic metadata

```shell
mq '.yaml | frontmatter' skills/*/references/*.md
```

```powershell
$files = (Get-ChildItem skills -Recurse -File -Filter *.md | Where-Object { $_.Directory.Name -eq 'references' -and $_.Name -ne 'index.md' }).FullName
mq '.yaml | frontmatter' $files
```

### Find the same topic across languages

```shell
mq '.yaml | frontmatter | select(self, get("topic") == "errors") | get("id")' skills/*/references/*.md
```

```powershell
$files = (Get-ChildItem skills -Recurse -File -Filter *.md | Where-Object { $_.Directory.Name -eq 'references' -and $_.Name -ne 'index.md' }).FullName
mq '.yaml | frontmatter | select(self, get("topic") == "errors") | get("id")' $files
```

### Find topics by tag

```shell
mq '.yaml | frontmatter | select(self, get("tags") | contains("async")) | get("id")' skills/*/references/*.md
```

```powershell
$files = (Get-ChildItem skills -Recurse -File -Filter *.md | Where-Object { $_.Directory.Name -eq 'references' -and $_.Name -ne 'index.md' }).FullName
mq '.yaml | frontmatter | select(self, get("tags") | contains("async")) | get("id")' $files
```

### Inspect a topic outline

```shell
mq '.h(1..3)' skills/go-coding-guidelines/references/errors.md
```

```powershell
mq '.h(1..3)' skills/go-coding-guidelines/references/errors.md
```

### Extract one section

```shell
mq -A 'section::by_title("Recommended Pattern")' skills/rust-coding-guidelines/references/errors.md
```

```powershell
mq -A 'section::by_title("Recommended Pattern")' skills/rust-coding-guidelines/references/errors.md
```

### Collect one skill's checklists

```shell
mq -A 'section::by_title("Checklist")' skills/go-coding-guidelines/references/*.md
```

```powershell
$files = (Get-ChildItem skills/go-coding-guidelines/references -File -Filter *.md).FullName
mq -A 'section::by_title("Checklist")' $files
```

### Extract code blocks by language

```shell
mq '.code("python")' skills/python-coding-guidelines/references/errors.md
```

```powershell
mq '.code("python")' skills/python-coding-guidelines/references/errors.md
```

## Authoring

Follow [CONTRIBUTING.md](CONTRIBUTING.md), start from [the topic template](templates/topic.md), and run the [Python + mq topic checker](CONTRIBUTING.md#checking-topics) before committing.
