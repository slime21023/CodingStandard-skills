#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator  # noqa: UP035

# ---------------------------------------------------------------------------
# Domain Configuration & Constraints
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SkillSpec:
    prefix: str
    language: str

    @property
    def is_language_agnostic(self) -> bool:
        return self.language == "any"

    @property
    def comment_marker(self) -> str:
        return "#" if self.language in {"python", "nim"} else "//"


@dataclass(frozen=True)
class ParsedDocument:
    metadata: Any
    nodes: list[dict[str, Any]]


SKILLS: dict[str, SkillSpec] = {
    "go-coding-guidelines": SkillSpec("go", "go"),
    "rust-coding-guidelines": SkillSpec("rust", "rust"),
    "c3-coding-guidelines": SkillSpec("c3", "c3"),
    "cpp-coding-guidelines": SkillSpec("cpp", "cpp"),
    "develop-readable-typescript": SkillSpec("typescript", "typescript"),
    "python-coding-guidelines": SkillSpec("python", "python"),
    "kotlin-coding-guidelines": SkillSpec("kotlin", "kotlin"),
    "nim-coding-guidelines": SkillSpec("nim", "nim"),
    "testing-principles": SkillSpec("testing", "any"),
}

TOPICS = frozenset(
    {
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
)

TAGS = frozenset(
    {
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
)

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
HEADING_ORDER = {name: idx for idx, name in enumerate(HEADINGS)}

REQUIRED_HEADINGS = frozenset(
    {
        "Summary",
        "When to Use",
        "Rules",
        "Recommended Pattern",
        "Pitfalls",
        "Checklist",
        "References",
    }
)
FORBIDDEN_TOPIC_HEADINGS = (("testing", "Testing"), ("tooling", "Tooling"))

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
COMMON_CODE_TAGS = frozenset({"shell", "text", "json", "toml", "yaml", "cmake"})
RULE_LEVELS = frozenset({"MUST", "SHOULD", "AVOID", "REVIEW SIGNAL"})
PITFALLS_HEADER = ["Smell", "Why", "Fix"]

SUMMARY_LEN_RANGE = (1, 200)
TAGS_COUNT_RANGE = (1, 6)
MAX_CODE_BLOCK_LINES = 40
CHECKLIST_COUNT_RANGE = (4, 10)
PITFALLS_ROWS_RANGE = (3, 8)

DOCUMENT_QUERY = "[frontmatter(first(filter(self, fn(n): is_yaml(n);))), self]"


# ---------------------------------------------------------------------------
# Infrastructure: mq Document Reader & AST Helpers
# ---------------------------------------------------------------------------


class MqDocumentReader:
    """Encapsulates invoking the `mq` CLI to parse Markdown + YAML front matter."""

    def __init__(self, executable: str) -> None:
        self._executable = executable

    def read(self, path: Path) -> ParsedDocument:
        result = subprocess.run(
            [self._executable, "-A", "-F", "json", DOCUMENT_QUERY, path.as_posix()],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        if result.returncode:
            message = (
                result.stderr.strip() or f"mq exited with status {result.returncode}"
            )
            raise ValueError(message)

        metadata, nodes = json.loads(result.stdout)
        return ParsedDocument(metadata=metadata, nodes=nodes)


def extract_text(node: dict[str, Any]) -> str:
    if "values" in node:
        return "".join(extract_text(child) for child in node["values"])
    return node.get("value", "")


def iter_links(nodes: list[dict[str, Any]]) -> Iterator[str]:
    for node in nodes:
        if node["type"] == "Link":
            yield node["url"]
        yield from iter_links(node.get("values", ()))


def is_in_range(value: int, bounds: tuple[int, int]) -> bool:
    low, high = bounds
    return low <= value <= high


# ---------------------------------------------------------------------------
# Metadata Validation
# ---------------------------------------------------------------------------


def validate_metadata(path: Path, metadata: Any, spec: SkillSpec) -> list[str]:
    errors: list[str] = []
    topic = path.stem

    if topic not in TOPICS or topic.startswith("test-") != (spec.prefix == "testing"):
        errors.append(f"unknown topic: {topic}")

    if not isinstance(metadata, dict):
        errors.append("expected a front matter mapping")
        return errors

    if tuple(metadata) != METADATA_KEYS:
        errors.append("incorrect front matter keys or key order")

    expected_fields = (
        ("id", f"{spec.prefix}/{topic}"),
        ("language", spec.language),
        ("topic", topic),
        ("snippets", "unverified"),
    )
    for key, expected in expected_fields:
        if metadata.get(key) != expected:
            errors.append(f"{key} must be {expected}")

    summary = metadata.get("summary")
    if not isinstance(summary, str) or not is_in_range(len(summary), SUMMARY_LEN_RANGE):
        errors.append("summary must contain 1–200 characters")

    errors.extend(_validate_tags(metadata.get("tags")))
    errors.extend(_validate_related(metadata.get("related"), path.parent, spec.prefix))
    return errors


def _validate_tags(tags: Any) -> list[str]:
    if not isinstance(tags, list) or not is_in_range(len(tags), TAGS_COUNT_RANGE):
        return ["expected an array of 1–6 tags"]
    return [
        f"unknown tag: {tag}"
        for tag in tags
        if not isinstance(tag, str) or tag not in TAGS
    ]


def _validate_related(related: Any, topic_dir: Path, prefix: str) -> list[str]:
    if not isinstance(related, list):
        return ["related must be an array"]

    errors: list[str] = []
    for target in related:
        owner, _, name = (
            target.partition("/") if isinstance(target, str) else ("", "", "")
        )
        if (
            owner != prefix
            or name not in TOPICS
            or not (topic_dir / f"{name}.md").is_file()
        ):
            errors.append(f"unresolved related topic: {target}")
    return errors


# ---------------------------------------------------------------------------
# Section & Content Validation
# ---------------------------------------------------------------------------


def validate_sections(
    path: Path, nodes: list[dict[str, Any]], spec: SkillSpec
) -> list[str]:
    sections, heading_errors = _partition_h2_sections(nodes)
    errors = list(heading_errors)

    errors.extend(_validate_code_blocks(nodes, spec))
    errors.extend(_validate_required_and_forbidden_headings(path.stem, sections, spec))

    if (
        path.stem != "tooling"
        and not spec.is_language_agnostic
        and "Recommended Pattern" in sections
    ):
        errors.extend(
            _validate_recommended_pattern(sections["Recommended Pattern"], spec)
        )

    errors.extend(_validate_rules_section(sections["Rules"]))
    errors.extend(_validate_checklist_section(sections["Checklist"]))
    errors.extend(_validate_pitfalls_section(sections["Pitfalls"]))
    return errors


def _partition_h2_sections(
    nodes: list[dict[str, Any]],
) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    sections: dict[str, list[dict[str, Any]]] = defaultdict(list)
    errors: list[str] = []
    current_section: str | None = None
    last_order = -1

    for node in nodes:
        if node["type"] == "Heading" and node["depth"] == 2:
            current_section = extract_text(node)
            sections[current_section]  # Ensure empty sections are recorded
            if current_section not in HEADING_ORDER:
                errors.append(f"unexpected H2: {current_section}")
            else:
                position = HEADING_ORDER[current_section]
                if position <= last_order:
                    errors.append(f"duplicate or out-of-order H2: {current_section}")
                last_order = max(last_order, position)
        elif current_section is not None:
            sections[current_section].append(node)

    return sections, errors


def _validate_code_blocks(nodes: list[dict[str, Any]], spec: SkillSpec) -> list[str]:
    allowed_tags = COMMON_CODE_TAGS | (
        set() if spec.is_language_agnostic else {spec.language}
    )
    errors: list[str] = []

    for node in nodes:
        if node["type"] != "Code":
            continue
        tag = node.get("lang")
        if tag not in allowed_tags:
            errors.append(f"invalid code block language: {tag or '<missing>'}")
        value = node["value"]
        line_count = value.count("\n") + 1 if value else 0
        if line_count > MAX_CODE_BLOCK_LINES:
            errors.append(
                f"code block has {line_count} lines (maximum {MAX_CODE_BLOCK_LINES})"
            )

    return errors


def _validate_required_and_forbidden_headings(
    topic: str, sections: dict[str, list[dict[str, Any]]], spec: SkillSpec
) -> list[str]:
    required = (
        REQUIRED_HEADINGS - {"Recommended Pattern", "References"}
        if spec.is_language_agnostic
        else REQUIRED_HEADINGS
    )
    errors = [
        f"missing H2: {heading}"
        for heading in HEADINGS
        if heading in required and heading not in sections
    ]
    for forbidden_topic, heading in FORBIDDEN_TOPIC_HEADINGS:
        if topic == forbidden_topic and heading in sections:
            errors.append(f"unexpected H2 for {forbidden_topic}: {heading}")
    return errors


def _validate_recommended_pattern(
    section_nodes: list[dict[str, Any]], spec: SkillSpec
) -> list[str]:
    errors: list[str] = []
    first_block = next(
        (node for node in section_nodes if node["type"] == "Code"),
        {},
    )
    if first_block.get("lang") != spec.language:
        errors.append(f"first Recommended Pattern block must use {spec.language}")

    marker = spec.comment_marker
    prefix = f"{marker} "
    first_line = first_block.get("value", "").partition("\n")[0]
    has_path_comment = first_line.startswith(prefix) and bool(
        first_line[len(prefix) : len(prefix) + 1].strip()
    )
    if not has_path_comment:
        errors.append(
            f"first Recommended Pattern block needs a {marker} path comment"
        )
    return errors


def _validate_rules_section(section_nodes: list[dict[str, Any]]) -> list[str]:
    rules = [node for node in section_nodes if node["type"] == "List"]
    if not rules:
        return ["Rules needs at least one bullet"]

    errors: list[str] = []
    for rule in rules:
        first_child = next(iter(rule["values"]), {})
        is_valid_bullet = (
            not rule["ordered"]
            and rule["level"] == 0
            and first_child.get("type") == "Strong"
            and extract_text(first_child) in RULE_LEVELS
        )
        if not is_valid_bullet:
            errors.append("invalid Rules bullet prefix")
    return errors


def _validate_checklist_section(section_nodes: list[dict[str, Any]]) -> list[str]:
    bullet_count = sum(
        node["type"] == "List" and not node["ordered"] and node["level"] == 0
        for node in section_nodes
    )
    if not is_in_range(bullet_count, CHECKLIST_COUNT_RANGE):
        return ["Checklist needs 4–10 bullets"]
    return []


def _validate_pitfalls_section(section_nodes: list[dict[str, Any]]) -> list[str]:
    cells = [node for node in section_nodes if node["type"] == "TableCell"]
    header = [extract_text(node).strip() for node in cells if node["row"] == 0]
    data_rows = {node["row"] for node in cells if node["row"] > 0}
    if header != PITFALLS_HEADER or not is_in_range(
        len(data_rows), PITFALLS_ROWS_RANGE
    ):
        return ["Pitfalls needs a Smell / Why / Fix table with 3–8 data rows"]
    return []


# ---------------------------------------------------------------------------
# Topic & Skill Orchestration
# ---------------------------------------------------------------------------


def validate_topic(
    reader: MqDocumentReader,
    path: Path,
    spec: SkillSpec,
    catalog_lines: list[str] | None,
) -> list[str]:
    try:
        doc = reader.read(path)
    except (OSError, ValueError) as exc:
        return [f"{path.as_posix()}: cannot parse topic: {exc}"]

    issues: list[str] = []
    issues.extend(validate_metadata(path, doc.metadata, spec))
    issues.extend(validate_sections(path, doc.nodes, spec))

    title = doc.metadata.get("title") if isinstance(doc.metadata, dict) else None
    summary = doc.metadata.get("summary") if isinstance(doc.metadata, dict) else None

    h1_headings = [
        extract_text(node)
        for node in doc.nodes
        if node["type"] == "Heading" and node["depth"] == 1
    ]
    if not title or h1_headings != [title]:
        issues.append("expected one H1 matching title")

    for target in iter_links(doc.nodes):
        if target.startswith(("http://", "https://")):
            continue
        local_target = target.partition("#")[0]
        if local_target and not (path.parent / local_target).is_file():
            issues.append(f"unresolved link: {local_target}")

    if catalog_lines is not None:
        expected_row = f"| [{title}]({path.name}) | {summary} |"
        if sum(line.startswith(expected_row) for line in catalog_lines) != 1:
            issues.append("expected exactly one matching title and summary in index.md")

    return [f"{path.as_posix()}: {msg}" for msg in issues]


def validate_skill(
    reader: MqDocumentReader,
    skills_dir: Path,
    skill_name: str,
    spec: SkillSpec,
) -> tuple[list[str], int]:
    errors: list[str] = []
    entry = skills_dir / skill_name / "SKILL.md"
    try:
        if "references/index.md" not in entry.read_text(encoding="utf-8"):
            errors.append(f"{entry.as_posix()}: missing references/index.md link")
    except (OSError, ValueError) as exc:
        errors.append(f"{entry.as_posix()}: cannot read skill: {exc}")

    references_dir = entry.parent / "references"
    index_path = references_dir / "index.md"
    catalog_lines, catalog_errors = _inspect_catalog(reader, references_dir, index_path)
    errors.extend(catalog_errors)

    topics = sorted(
        path
        for path in references_dir.glob("*.md")
        if path != index_path and path.is_file()
    )
    if not topics:
        errors.append(f"{references_dir.as_posix()}: missing topics")

    for topic_path in topics:
        errors.extend(validate_topic(reader, topic_path, spec, catalog_lines))

    return errors, len(topics)


def _inspect_catalog(
    reader: MqDocumentReader, references_dir: Path, index_path: Path
) -> tuple[list[str] | None, list[str]]:
    if not index_path.is_file():
        return None, [f"{index_path.as_posix()}: missing catalog"]

    errors: list[str] = []
    try:
        catalog_lines = index_path.read_text(encoding="utf-8").splitlines()
        doc = reader.read(index_path)
        for target in iter_links(doc.nodes):
            if target.endswith(".md") and not (references_dir / target).is_file():
                errors.append(
                    f"{index_path.as_posix()}: unresolved catalog link: {target}"
                )
        return catalog_lines, errors
    except (OSError, ValueError) as exc:
        return None, [f"{index_path.as_posix()}: cannot inspect catalog: {exc}"]


def main() -> int:
    skills_dir = Path("skills")
    if not skills_dir.is_dir():
        print("run from the repository root", file=sys.stderr)
        return 2

    mq_executable = shutil.which("mq")
    if mq_executable is None:
        print("mq not found", file=sys.stderr)
        return 2

    reader = MqDocumentReader(mq_executable)
    errors = [
        f"{folder.as_posix()}/: unknown skill"
        for folder in sorted(skills_dir.iterdir())
        if folder.is_dir() and folder.name not in SKILLS
    ]

    total_topics = 0
    for skill_name, spec in SKILLS.items():
        skill_errors, topic_count = validate_skill(reader, skills_dir, skill_name, spec)
        errors.extend(skill_errors)
        total_topics += topic_count

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"OK: {total_topics} topic files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
