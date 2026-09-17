#!/usr/bin/env python3
"""Audit a ChatGPT skill folder for upgrade readiness.

This script performs deterministic structural checks and lightweight content
heuristics. It is intended to support, not replace, manual real-case review.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class CheckResult:
    category: str
    score: int
    max_score: int
    findings: list[str]
    recommendations: list[str]


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
KEY_VALUE_RE = re.compile(r"^([a-zA-Z0-9_-]+):\s*(.*)$")


SECTION_KEYWORDS = {
    "workflow": ["workflow", "process", "step", "decision tree", "langkah"],
    "edge_cases": ["edge case", "failure", "fallback", "missing", "ambiguous", "invalid", "error", "partial"],
    "outputs": ["output", "deliverable", "final response", "template", "format"],
    "validation": ["validate", "validation", "test", "checklist", "verify", "package"],
    "tools": ["tool", "connector", "file_search", "web", "script", "api", "calendar", "gmail"],
    "examples": ["example", "sample", "scenario", "real case", "use case"],
}

ANTI_PATTERNS = [
    ("todo", "contains TODO placeholders"),
    ("[todo", "contains template TODO placeholders"),
    ("be helpful", "uses generic assistant guidance"),
    ("best practices", "uses vague best-practices language"),
    ("handle anything", "claims overly broad capability"),
    ("do anything", "claims overly broad capability"),
]


SPECIFIC_TRIGGER_TERMS = [
    "use when", "when asked", "file", "zip", "folder", "skill.md", "workflow",
    "audit", "upgrade", "refactor", "validate", "package", "real case",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(content: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}, content, ["SKILL.md has missing or invalid YAML-style frontmatter"]

    frontmatter_text = match.group(1)
    body = content[match.end():]
    data: dict[str, str] = {}

    for line in frontmatter_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        kv = KEY_VALUE_RE.match(line)
        if not kv:
            errors.append(f"frontmatter line is not simple key/value syntax: {line}")
            continue
        key, value = kv.group(1), kv.group(2).strip()
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        data[key] = value

    return data, body, errors


def count_keyword_groups(text: str, groups: dict[str, list[str]]) -> dict[str, int]:
    lowered = text.lower()
    return {
        name: sum(1 for keyword in keywords if keyword in lowered)
        for name, keywords in groups.items()
    }


def list_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*") if p.is_file()]


def audit_structure(root: Path) -> CheckResult:
    findings: list[str] = []
    recs: list[str] = []
    score = 0

    if (root / "SKILL.md").exists():
        score += 2
        findings.append("SKILL.md exists")
    else:
        findings.append("SKILL.md is missing")
        recs.append("add a required SKILL.md entrypoint")

    if (root / "agents" / "openai.yaml").exists():
        score += 1
        findings.append("agents/openai.yaml exists")
    else:
        findings.append("agents/openai.yaml is missing")
        recs.append("add agents/openai.yaml with a human-readable display_name")

    files = list_files(root)
    placeholder_files = [p for p in files if p.name in {"example.py", "api_reference.md", "example_asset.txt"}]
    if not placeholder_files:
        score += 1
    else:
        findings.append("placeholder files detected: " + ", ".join(str(p.relative_to(root)) for p in placeholder_files))
        recs.append("remove generated placeholder files that are not used by the target workflow")

    if len(files) > 1:
        score += 1
        findings.append(f"skill contains {len(files)} files")
    else:
        recs.append("add supporting references or scripts only if they improve repeatability")

    return CheckResult("structure", min(score, 5), 5, findings, recs)


def audit_frontmatter(content: str) -> CheckResult:
    data, _body, errors = parse_frontmatter(content)
    findings = list(errors)
    recs: list[str] = []
    score = 0

    name = data.get("name", "").strip()
    description = data.get("description", "").strip()

    if name:
        findings.append(f"name: {name}")
        if re.fullmatch(r"[a-z0-9-]+", name):
            score += 1
        else:
            recs.append("rewrite name using lowercase hyphen-case")
    else:
        recs.append("add a frontmatter name")

    if description:
        findings.append(f"description length: {len(description)} characters")
        if 160 <= len(description) <= 900:
            score += 1
        else:
            recs.append("rewrite description to be specific, trigger-rich, and under 1024 characters")

        lowered = description.lower()
        trigger_hits = [term for term in SPECIFIC_TRIGGER_TERMS if term in lowered]
        if len(trigger_hits) >= 4:
            score += 2
            findings.append("description includes concrete trigger terms: " + ", ".join(trigger_hits[:8]))
        else:
            recs.append("add concrete trigger phrases, input types, and target tasks to the description")

        if "when" in lowered or "use" in lowered:
            score += 1
        else:
            recs.append("state when the skill should be used in the frontmatter description")
    else:
        recs.append("add a frontmatter description")

    return CheckResult("frontmatter trigger quality", min(score, 5), 5, findings, recs)


def audit_body(body: str) -> list[CheckResult]:
    counts = count_keyword_groups(body, SECTION_KEYWORDS)
    lowered = body.lower()
    results: list[CheckResult] = []

    workflow_recs = []
    workflow_score = min(5, counts["workflow"] + len(re.findall(r"^\s*\d+\.\s+", body, re.MULTILINE)))
    if workflow_score < 3:
        workflow_recs.append("add a clear step-by-step workflow with branch conditions")
    results.append(CheckResult("workflow reliability", workflow_score, 5, [f"workflow keyword hits: {counts['workflow']}"], workflow_recs))

    edge_recs = []
    edge_score = min(5, counts["edge_cases"])
    if edge_score < 3:
        edge_recs.append("add explicit handling for missing input, invalid files, ambiguity, tool failure, and partial outputs")
    results.append(CheckResult("edge-case readiness", edge_score, 5, [f"edge-case keyword hits: {counts['edge_cases']}"], edge_recs))

    output_recs = []
    output_score = min(5, counts["outputs"] + (1 if "```" in body else 0))
    if output_score < 3:
        output_recs.append("add an output contract with required sections, file names, or response template")
    results.append(CheckResult("output contract", output_score, 5, [f"output keyword hits: {counts['outputs']}"], output_recs))

    validation_recs = []
    validation_score = min(5, counts["validation"])
    if validation_score < 3:
        validation_recs.append("add validation steps and test scenarios before final delivery")
    results.append(CheckResult("validation", validation_score, 5, [f"validation keyword hits: {counts['validation']}"], validation_recs))

    resource_recs = []
    resource_score = 0
    if "references/" in lowered:
        resource_score += 2
    if "scripts/" in lowered or "python" in lowered:
        resource_score += 2
    if "assets/" in lowered:
        resource_score += 1
    if resource_score < 2:
        resource_recs.append("state how references, scripts, or assets should be used only when they materially help")
    results.append(CheckResult("resource organization", min(resource_score, 5), 5, [f"resource score signals: {resource_score}"], resource_recs))

    example_recs = []
    example_score = min(5, counts["examples"])
    if example_score < 2:
        example_recs.append("add 2-3 realistic user prompts or test scenarios")
    results.append(CheckResult("real-case examples", example_score, 5, [f"example keyword hits: {counts['examples']}"], example_recs))

    anti_findings = []
    anti_recs = []
    penalty = 0
    for needle, message in ANTI_PATTERNS:
        if needle in lowered:
            anti_findings.append(message)
            anti_recs.append("remove or replace: " + message)
            penalty += 1
    anti_score = max(0, 5 - penalty)
    if not anti_findings:
        anti_findings.append("no common anti-patterns detected")
    results.append(CheckResult("anti-pattern cleanup", anti_score, 5, anti_findings, anti_recs))

    return results


def format_result(result: CheckResult) -> str:
    lines = [f"### {result.category}", f"Score: {result.score}/{result.max_score}", ""]
    if result.findings:
        lines.append("Findings:")
        lines.extend(f"- {item}" for item in result.findings)
        lines.append("")
    if result.recommendations:
        lines.append("Recommendations:")
        lines.extend(f"- {item}" for item in result.recommendations)
        lines.append("")
    return "\n".join(lines)


def audit_skill(root: Path) -> tuple[int, str]:
    if not root.exists() or not root.is_dir():
        return 1, f"error: not a directory: {root}\n"

    skill_md = root / "SKILL.md"
    results: list[CheckResult] = [audit_structure(root)]

    if skill_md.exists():
        content = read_text(skill_md)
        frontmatter, body, _errors = parse_frontmatter(content)
        results.append(audit_frontmatter(content))
        results.extend(audit_body(body))
    else:
        frontmatter = {}

    total = sum(r.score for r in results)
    maximum = sum(r.max_score for r in results)
    percent = round((total / maximum) * 100) if maximum else 0

    if percent >= 85:
        readiness = "high"
    elif percent >= 60:
        readiness = "medium"
    else:
        readiness = "low"

    title = frontmatter.get("name", root.name) if isinstance(frontmatter, dict) else root.name
    lines = [
        f"# Skill Audit: {title}",
        "",
        f"Overall readiness: {readiness} ({total}/{maximum}, {percent}%)",
        "",
        "This audit checks structure and upgrade-readiness signals. Use manual review for domain-specific business logic.",
        "",
    ]
    for result in results:
        lines.append(format_result(result))

    return 0, "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit a ChatGPT skill folder for upgrade readiness.")
    parser.add_argument("skill_folder", help="Path to the skill folder containing SKILL.md")
    args = parser.parse_args(argv)

    code, report = audit_skill(Path(args.skill_folder).resolve())
    print(report)
    return code


if __name__ == "__main__":
    sys.exit(main())
