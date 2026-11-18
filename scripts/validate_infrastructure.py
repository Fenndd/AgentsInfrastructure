#!/usr/bin/env python3
"""Optional, read-only checks for the infrastructure source (Python stdlib only).

This checks repository structure and documented static preferences, not whether a
client loaded instructions or supports a model. Run with Python 3.11 or newer.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import tomllib
from urllib.parse import unquote, urlsplit

# Explicit invariants protect the approved combinations if policy and presets
# drift together. Preset values themselves are compared with the policy table.
CODEX_ROWS = [
    ("1", "gpt-6-luna", "max"),
    ("2", "gpt-6.1-sol", "medium"),
    ("3", "gpt-6.1-sol", "high"),
    ("4", "gpt-6-astra", "high"),
]
CLAUDE_ROWS = [
    ("1", "sonnet-high", "Sonnet 5.5", "high"),
    ("2", "sonnet-high", "Sonnet 5.5", "high"),
    ("3", "opus-medium", "Opus 5.5", "medium"),
    ("3", "opus-high", "Opus 5.5", "high"),
    ("4", "opus-max", "Opus 5.5", "max"),
]
REQUIRED_SOURCES = {
    "templates/AGENTS.md", "CLAUDE.md", "GEMINI.md", ".agents/skills/",
    ".claude/skills/", ".claude/agents/", ".editorconfig", ".gitattributes",
    ".gitignore", "docs/engineering/AI_ORCHESTRATION.md",
    "docs/engineering/DEVELOPMENT_WORKFLOW.md", "docs/engineering/TASK_FORMAT.md",
    "docs/engineering/AI_INFRASTRUCTURE_EVALUATION.md", "presets/codex-config.toml",
}


def unfenced(text: str) -> str:
    """Blank fenced examples, retaining line numbers for diagnostics."""
    result = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
                fence = None
            result.append("")
        elif match:
            fence = match[1]
            result.append("")
        else:
            result.append(line)
    return "\n".join(result)


def inline_links(text: str):
    """Yield real inline Markdown destinations, not code-span illustrations."""
    for number, line in enumerate(unfenced(text).splitlines(), 1):
        # Preserve links with code-formatted labels; remove standalone code spans.
        line = re.sub(r"(`+)(.*?)\1", lambda m: "" if "](" in m[2] else m[0], line)
        for match in re.finditer(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+['\"][^\n]*?['\"])?\s*\)", line):
            yield number, match[1].strip("<>")


def local_target(document: Path, destination: str) -> Path | None:
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return (document.parent / unquote(parsed.path)).resolve()


def check_links(root: Path) -> list[str]:
    errors = []
    for document in sorted(root.rglob("*.md")):
        relative = document.relative_to(root)
        if any(part in {".git", "node_modules", "__pycache__", ".venv"} for part in relative.parts):
            continue
        for line, destination in inline_links(document.read_text(encoding="utf-8-sig")):
            target = local_target(document, destination)
            if target is not None and not target.exists():
                errors.append(f"{relative}:{line}: broken local link: {destination}")
    return errors


def frontmatter(path: Path) -> dict[str, str]:
    """Read the simple scalar frontmatter used by this source, without YAML deps."""
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.S)
    if not match:
        raise ValueError("missing frontmatter")
    values = {}
    for line in match[1].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError("unsupported frontmatter line")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def check_skills(root: Path) -> list[str]:
    errors = []
    canonical = {p.parent.name: p for p in (root / ".agents/skills").glob("*/SKILL.md")}
    adapters = {p.parent.name: p for p in (root / ".claude/skills").glob("*/SKILL.md")}
    for name in sorted(canonical.keys() | adapters.keys()):
        if name not in canonical or name not in adapters:
            errors.append(f"skill {name}: missing canonical skill or Claude adapter")
            continue
        try:
            source, adapter = frontmatter(canonical[name]), frontmatter(adapters[name])
            if source.get("name") != name:
                errors.append(f"skill {name}: canonical frontmatter name does not match directory")
            for field in ("name", "description"):
                if not source.get(field) or source.get(field) != adapter.get(field):
                    errors.append(f"skill {name}: adapter {field} differs from canonical frontmatter")
            targets = {local_target(adapters[name], target) for _, target in inline_links(adapters[name].read_text(encoding="utf-8-sig"))}
            if canonical[name].resolve() not in targets:
                errors.append(f"skill {name}: adapter lacks a link to its canonical SKILL.md")
        except ValueError as exc:
            errors.append(f"skill {name}: {exc}")
    if not canonical:
        errors.append("no canonical skills found")
    return errors


def table_rows(text: str, header: str) -> list[list[str]]:
    """Read one table by its exact header, without depending on section prose."""
    lines = unfenced(text).splitlines()
    for index, line in enumerate(lines):
        if line.strip() != header:
            continue
        rows = []
        for row in lines[index + 2:]:
            if not row.strip().startswith("|"):
                break
            rows.append([cell.strip().strip("`") for cell in row.strip().strip("|").split("|")])
        return rows
    return []


def check_payload(root: Path) -> list[str]:
    readme = root / "README.md"
    if not readme.is_file():
        return ["README.md: missing source inventory"]
    rows = table_rows(readme.read_text(encoding="utf-8-sig"), "| Source | Destination | Purpose |")
    sources = {row[0] for row in rows if len(row) == 3}
    errors = [f"README.md: missing required payload source: {p}" for p in sorted(REQUIRED_SOURCES - sources)]
    for source in sorted(sources):
        if not (root / source).exists():
            errors.append(f"README.md: payload source does not exist: {source}")
    return errors


def check_routing(root: Path) -> list[str]:
    policy = root / "docs/engineering/AI_ORCHESTRATION.md"
    if not policy.is_file():
        return ["missing docs/engineering/AI_ORCHESTRATION.md"]
    text = policy.read_text(encoding="utf-8-sig")
    errors = []
    codex = []
    for row in table_rows(text, "| Tier | Model | Effort |"):
        if len(row) == 3:
            model = re.search(r"`([^`]+)`", row[1])
            codex.append((row[0], model[1] if model else row[1], row[2].split()[0]))
    if codex != CODEX_ROWS:
        errors.append("Codex policy table differs from approved tier/model/effort combinations")
    claude = [tuple(row[:4]) for row in table_rows(text, "| Tier | Preset | Model | Effort | Selection within tier |") if len(row) == 5]
    if claude != CLAUDE_ROWS:
        errors.append("Claude policy table differs from approved tier/preset/model/effort combinations")
    directory = root / ".claude/agents"
    expected_names = {row[1] for row in CLAUDE_ROWS}
    actual_names = {p.stem for p in directory.glob("*.md")}
    if actual_names != expected_names:
        errors.append("Claude preset inventory must be exactly: " + ", ".join(sorted(expected_names)))
    for _, name, model, effort in claude:
        path = directory / f"{name}.md"
        if not path.is_file():
            errors.append(f"Claude preset missing: {name}")
            continue
        try:
            values = frontmatter(path)
            fixed_model = "claude-" + model.lower().replace(" ", "-").replace(".", "-")
            if any(values.get(key) != value for key, value in (("name", name), ("model", fixed_model), ("effort", effort))):
                errors.append(f"Claude preset {name}: name/model/effort differs from policy")
        except ValueError as exc:
            errors.append(f"Claude preset {name}: {exc}")
    config = root / "presets/codex-config.toml"
    if config.exists():
        try:
            values = tomllib.loads(config.read_text(encoding="utf-8-sig"))
            # This exact source fragment sets executor defaults only. Do not
            # apply this restriction to a destination's general client config.
            expected = {"agents": {
                "default_subagent_model": "gpt-6.1-sol",
                "default_subagent_reasoning_effort": "medium",
            }}
            if values != expected:
                errors.append("presets/codex-config.toml: expected only [agents] fixed gpt-6.1-sol / medium executor defaults")
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"presets/codex-config.toml: invalid TOML: {exc}")
    return sorted(set(errors))


def validate(root: Path) -> list[str]:
    errors = []
    for check in (check_payload, check_skills, check_routing, check_links):
        errors.extend(check(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"root is not a directory: {root}")
    try:
        errors = validate(root)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"Infrastructure validation failed: {len(errors)} issue(s).", file=sys.stderr)
        return 1
    print("Infrastructure validation passed (static source checks only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
