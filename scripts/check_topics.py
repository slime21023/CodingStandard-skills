#!/usr/bin/env python3
"""Validate skill references with mq's Markdown and YAML parser."""

import json
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

SKILLS = {
    "go-coding-guidelines": ("go", "go"),
    "rust-coding-guidelines": ("rust", "rust"),
    "c3-coding-guidelines": ("c3", "c3"),
    "cpp-coding-guidelines": ("cpp", "cpp"),
    "develop-readable-typescript": ("typescript", "typescript"),
    "python-coding-guidelines": ("python", "python"),
    "kotlin-coding-guidelines": ("kotlin", "kotlin"),
    "nim-coding-guidelines": ("nim", "nim"),
    "testing-principles": ("testing", "any"),
}
TOPICS = {
    "naming-and-formatting",
    "data-and-functions",
    "control-flow",
    "types",
    "null-safety",
    "errors",
    "modules-and-api",
    "abstraction",
    "resources-and-memory",
    "concurrency",
    "unsafe-and-ffi",
    "lambdas-and-scope-functions",
    "collections-and-idioms",
    "testing",
    "tooling",
    "test-scope",
    "test-design",
    "test-delivery",
}
TAGS = {
    "naming",
    "formatting",
    "data",
    "functions",
    "control-flow",
    "types",
    "null-safety",
    "errors",
    "result",
    "option",
    "exceptions",
    "modules",
    "public-api",
    "interfaces",
    "generics",
    "metaprogramming",
    "classes",
    "ownership",
    "memory",
    "resources",
    "concurrency",
    "async",
    "cancellation",
    "unsafe",
    "ffi",
    "lambdas",
    "collections",
    "testing",
    "tooling",
    "dependencies",
    "build",
    "documentation",
    "review",
}
HEADINGS = (
    "Summary",
    "When to Use",
    "Rules",
    "Dependencies",
    "Tooling",
    "Recommended Pattern",
    "Pitfalls",
    "Testing",
    "Checklist",
    "Related",
    "References",
)
REQUIRED = {
    "Summary",
    "When to Use",
    "Rules",
    "Recommended Pattern",
    "Pitfalls",
    "Checklist",
    "References",
}
METADATA_KEYS = (
    "id",
    "title",
    "summary",
    "language",
    "topic",
    "tags",
    "related",
    "snippets",
)
CODE_TAGS = {"shell", "text", "json", "toml", "yaml", "cmake"}
RULE_LEVELS = {"MUST", "SHOULD", "AVOID", "REVIEW SIGNAL"}
DOCUMENT_QUERY = "[frontmatter(first(filter(self, fn(n): is_yaml(n);))), self]"


def read_document(mq, path):
    result = subprocess.run(
        [mq, "-A", "-F", "json", DOCUMENT_QUERY, path.as_posix()],
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    if result.returncode:
        raise ValueError(
            result.stderr.strip() or f"mq exited with status {result.returncode}"
        )
    metadata, nodes = json.loads(result.stdout)
    return metadata, nodes


def text(node):
    if "values" in node:
        return "".join(text(child) for child in node["values"])
    return node.get("value", "")


def links(nodes):
    for node in nodes:
        if node["type"] == "Link":
            yield node["url"]
        yield from links(node.get("values", ()))


def check_metadata(path, metadata, prefix, language, error):
    topic = path.stem
    if topic not in TOPICS or topic.startswith("test-") != (prefix == "testing"):
        error(f"unknown topic: {topic}")
    if not isinstance(metadata, dict):
        error("expected a front matter mapping")
        return
    if tuple(metadata) != METADATA_KEYS:
        error("incorrect front matter keys or key order")
    for key, expected in (
        ("id", f"{prefix}/{topic}"),
        ("language", language),
        ("topic", topic),
        ("snippets", "unverified"),
    ):
        if metadata.get(key) != expected:
            error(f"{key} must be {expected}")
    summary = metadata.get("summary")
    if not isinstance(summary, str) or not 1 <= len(summary) <= 200:
        error("summary must contain 1–200 characters")
    tags = metadata.get("tags")
    if not isinstance(tags, list) or not 1 <= len(tags) <= 6:
        error("expected an array of 1–6 tags")
    else:
        for tag in tags:
            if not isinstance(tag, str) or tag not in TAGS:
                error(f"unknown tag: {tag}")
    related = metadata.get("related")
    if not isinstance(related, list):
        error("related must be an array")
    else:
        for target in related:
            owner, _, name = (
                target.partition("/") if isinstance(target, str) else ("", "", "")
            )
            if (
                owner != prefix
                or name not in TOPICS
                or not (path.parent / f"{name}.md").is_file()
            ):
                error(f"unresolved related topic: {target}")


def check_sections(path, nodes, language, error):
    sections = defaultdict(list)
    section = None
    order = -1
    allowed_tags = CODE_TAGS | ({language} if language != "any" else set())
    for node in nodes:
        kind = node["type"]
        if kind == "Heading" and node["depth"] == 2:
            section = text(node)
            sections[section]
            if section not in HEADINGS:
                error(f"unexpected H2: {section}")
            else:
                position = HEADINGS.index(section)
                if position <= order:
                    error(f"duplicate or out-of-order H2: {section}")
                order = max(order, position)
        elif section is not None:
            sections[section].append(node)
        if kind == "Code":
            tag = node.get("lang")
            if tag not in allowed_tags:
                error(f"invalid code block language: {tag or '<missing>'}")
            value = node["value"]
            length = value.count("\n") + 1 if value else 0
            if length > 40:
                error(f"code block has {length} lines (maximum 40)")

    required = (
        REQUIRED
        if language != "any"
        else REQUIRED - {"Recommended Pattern", "References"}
    )
    for heading in HEADINGS:
        if heading in required and heading not in sections:
            error(f"missing H2: {heading}")
    for topic, heading in (("testing", "Testing"), ("tooling", "Tooling")):
        if path.stem == topic and heading in sections:
            error(f"unexpected H2 for {topic}: {heading}")

    if (
        path.stem != "tooling"
        and language != "any"
        and "Recommended Pattern" in sections
    ):
        block = next(
            (
                node
                for node in sections["Recommended Pattern"]
                if node["type"] == "Code"
            ),
            {},
        )
        if block.get("lang") != language:
            error(f"first Recommended Pattern block must use {language}")
        marker = "#" if language in {"python", "nim"} else "//"
        first_line = block.get("value", "").partition("\n")[0]
        comment = marker + " "
        if (
            not first_line.startswith(comment)
            or not first_line[len(comment) : len(comment) + 1].strip()
        ):
            error(f"first Recommended Pattern block needs a {marker} path comment")

    rules = [node for node in sections["Rules"] if node["type"] == "List"]
    if not rules:
        error("Rules needs at least one bullet")
    for rule in rules:
        first = next(iter(rule["values"]), {})
        if (
            rule["ordered"]
            or rule["level"]
            or first.get("type") != "Strong"
            or text(first) not in RULE_LEVELS
        ):
            error("invalid Rules bullet prefix")
    checklist = sum(
        node["type"] == "List" and not node["ordered"] and node["level"] == 0
        for node in sections["Checklist"]
    )
    if not 4 <= checklist <= 10:
        error("Checklist needs 4–10 bullets")

    pitfall_nodes = sections["Pitfalls"]
    cells = [node for node in pitfall_nodes if node["type"] == "TableCell"]
    header = [text(node).strip() for node in cells if node["row"] == 0]
    rows = {node["row"] for node in cells if node["row"] > 0}
    if header != ["Smell", "Why", "Fix"] or not 3 <= len(rows) <= 8:
        error("Pitfalls needs a Smell / Why / Fix table with 3–8 data rows")


def check_topic(mq, path, prefix, language, catalog_lines, errors):
    def error(message):
        errors.append(f"{path.as_posix()}: {message}")

    try:
        metadata, nodes = read_document(mq, path)
    except (OSError, ValueError) as exc:
        error(f"cannot parse topic: {exc}")
        return
    check_metadata(path, metadata, prefix, language, error)
    check_sections(path, nodes, language, error)
    title = metadata.get("title") if isinstance(metadata, dict) else None
    summary = metadata.get("summary") if isinstance(metadata, dict) else None
    h1 = [
        text(node) for node in nodes if node["type"] == "Heading" and node["depth"] == 1
    ]
    if not title or h1 != [title]:
        error("expected one H1 matching title")
    for target in links(nodes):
        if target.startswith(("http://", "https://")):
            continue
        target = target.partition("#")[0]
        if target and not (path.parent / target).is_file():
            error(f"unresolved link: {target}")
    if catalog_lines is not None:
        row = f"| [{title}]({path.name}) | {summary} |"
        if sum(line.startswith(row) for line in catalog_lines) != 1:
            error("expected exactly one matching title and summary in index.md")


def main():
    skills_dir = Path("skills")
    if not skills_dir.is_dir():
        print("run from the repository root", file=sys.stderr)
        return 2
    mq = shutil.which("mq")
    if mq is None:
        print("mq not found", file=sys.stderr)
        return 2

    errors = []
    count = 0
    for folder in sorted(skills_dir.iterdir()):
        if folder.is_dir() and folder.name not in SKILLS:
            errors.append(f"{folder.as_posix()}/: unknown skill")
    for skill, (prefix, language) in SKILLS.items():
        entry = skills_dir / skill / "SKILL.md"
        try:
            if "references/index.md" not in entry.read_text(encoding="utf-8"):
                errors.append(f"{entry.as_posix()}: missing references/index.md link")
        except (OSError, ValueError) as exc:
            errors.append(f"{entry.as_posix()}: cannot read skill: {exc}")

        directory = entry.parent / "references"
        index = directory / "index.md"
        catalog_lines = None
        if not index.is_file():
            errors.append(f"{index.as_posix()}: missing catalog")
        else:
            try:
                catalog_lines = index.read_text(encoding="utf-8").splitlines()
                _, nodes = read_document(mq, index)
                for target in links(nodes):
                    if target.endswith(".md") and not (directory / target).is_file():
                        errors.append(
                            f"{index.as_posix()}: unresolved catalog link: {target}"
                        )
            except (OSError, ValueError) as exc:
                errors.append(f"{index.as_posix()}: cannot inspect catalog: {exc}")

        topics = sorted(
            path for path in directory.glob("*.md") if path != index and path.is_file()
        )
        if not topics:
            errors.append(f"{directory.as_posix()}: missing topics")
        for path in topics:
            check_topic(mq, path, prefix, language, catalog_lines, errors)
        count += len(topics)

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {count} topic files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
