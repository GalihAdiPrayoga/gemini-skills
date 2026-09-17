#!/usr/bin/env python3
"""Static audit helper for Claude or Claude Code plugin folders.

This script scans a plugin folder or zip archive and produces a first-pass
architecture audit. It is intentionally dependency-free and conservative:
it detects evidence of capabilities and likely gaps, but the final assessment
should still be reviewed by the model using the skill references.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

TEXT_EXTENSIONS = {
    ".md", ".mdx", ".txt", ".json", ".jsonc", ".yaml", ".yml",
    ".toml", ".js", ".jsx", ".ts", ".tsx", ".py", ".sh", ".bash",
    ".zsh", ".fish", ".xml", ".ini", ".cfg", ".env.example"
}

SKIP_DIRS = {
    ".git", "node_modules", ".next", "dist", "build", "coverage", ".venv",
    "venv", "__pycache__", ".cache", ".turbo", ".idea", ".vscode"
}

PATTERNS = {
    "commands": [r"\bcommand(s)?\b", r"/commands?\b", r"slash command", r"\.claude/commands"],
    "hooks": [r"\bhook(s)?\b", r"pre-?tool", r"post-?tool", r"pre-?commit", r"on file change"],
    "mcp": [r"\bmcp\b", r"model context protocol", r"mcpserver", r"mcpServers"],
    "subagents": [r"subagent", r"sub-agent", r"agent role", r"planner", r"reviewer", r"security auditor"],
    "context": [r"claude\.md", r"agents\.md", r"context file", r"project rules", r"memory"],
    "validation": [r"\btest(s|ing)?\b", r"lint", r"typecheck", r"schema", r"validate", r"dry-?run", r"verify"],
    "edge_cases": [r"edge case", r"fallback", r"timeout", r"retry", r"rollback", r"failure", r"error handling"],
    "safety": [r"permission", r"approval", r"destructive", r"prompt injection", r"secret", r"sandbox", r"least privilege"],
    "release": [r"install", r"uninstall", r"changelog", r"version", r"release", r"migration", r"troubleshooting"],
}

RISK_PATTERNS = {
    "destructive_shell": [r"rm\s+-rf", r"sudo\s+", r"chmod\s+777", r"curl\s+.*\|\s*(sh|bash)", r"wget\s+.*\|\s*(sh|bash)"],
    "external_side_effects": [r"git\s+push", r"npm\s+publish", r"deploy", r"send email", r"create pull request", r"update ticket"],
    "prompt_injection_terms": [r"ignore previous", r"ignore all previous", r"reveal secret", r"system prompt", r"disable validation"],
}

@dataclass
class Finding:
    category: str
    score: int
    evidence: List[str]
    gaps: List[str]
    recommendations: List[str]


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name.lower() in {"claude.md", "agents.md", "readme", "makefile"}


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def read_text(path: Path, limit: int = 200_000) -> str:
    try:
        data = path.read_bytes()[:limit]
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def collect_corpus(root: Path) -> Tuple[List[str], Dict[str, str]]:
    paths: List[str] = []
    texts: Dict[str, str] = {}
    for file_path in iter_files(root):
        rel = str(file_path.relative_to(root))
        paths.append(rel)
        if is_text_file(file_path):
            text = read_text(file_path)
            if text.strip():
                texts[rel] = text
    return paths, texts


def match_patterns(paths: List[str], texts: Dict[str, str], patterns: List[str]) -> List[str]:
    evidence: List[str] = []
    combined_path_text = "\n".join(paths)
    for pattern in patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        if regex.search(combined_path_text):
            evidence.append(f"path match: {pattern}")
        for rel, text in texts.items():
            if regex.search(text):
                evidence.append(f"content match in {rel}: {pattern}")
                break
    return evidence[:6]


def score_category(category: str, evidence: List[str], texts: Dict[str, str]) -> Finding:
    score = 0
    gaps: List[str] = []
    recommendations: List[str] = []

    if len(evidence) >= 4:
        score = 3
    elif len(evidence) >= 2:
        score = 2
    elif len(evidence) == 1:
        score = 1

    if category == "commands":
        gaps.append("Command contracts may be unclear if inputs, outputs, and examples are not documented.")
        recommendations.append("Define each command with trigger, inputs, preconditions, steps, validation, fallback, and example invocation.")
    elif category == "hooks":
        gaps.append("Hooks may create hidden side effects if trigger, scope, timeout, and safe failure behavior are not explicit.")
        recommendations.append("Document hook event, allowed actions, timeout, dry-run mode, and rollback behavior.")
    elif category == "mcp":
        gaps.append("MCP tools may be unsafe if read/write permissions and output validation are not defined.")
        recommendations.append("Classify every MCP tool as read-only, local write, external write, or destructive; add confirmation rules.")
    elif category == "subagents":
        gaps.append("Subagents may overlap or add noise if role boundaries are vague.")
        recommendations.append("Give each subagent a unique input/output contract and escalation rule.")
    elif category == "context":
        gaps.append("Context files may become stale or overloaded if not scoped.")
        recommendations.append("Split stable project rules from long references and define precedence rules for conflicts.")
    elif category == "validation":
        gaps.append("The plugin may produce unverified changes if validation is weak.")
        recommendations.append("Add dry-run, tests, lint/typecheck, schema checks, and before/after diff summaries.")
    elif category == "edge_cases":
        gaps.append("Real-case failures may be under-specified.")
        recommendations.append("Add failure handling for ambiguity, missing files, unavailable tools, partial success, and rollback.")
    elif category == "safety":
        gaps.append("Tool safety and prompt injection boundaries may be insufficient.")
        recommendations.append("Treat repository content and tool output as untrusted; require approval for destructive or external actions.")
    elif category == "release":
        gaps.append("Release readiness may be incomplete without install, config, changelog, and troubleshooting docs.")
        recommendations.append("Add install/uninstall docs, versioning, changelog, known limitations, and release checklist.")

    if score == 0:
        recommendations.insert(0, f"Add explicit {category.replace('_', ' ')} documentation or implementation evidence.")

    return Finding(category, score, evidence, gaps, recommendations)


def detect_risks(paths: List[str], texts: Dict[str, str]) -> Dict[str, List[str]]:
    results: Dict[str, List[str]] = {}
    full_items = {"paths": "\n".join(paths), **texts}
    for risk, patterns in RISK_PATTERNS.items():
        hits: List[str] = []
        for pattern in patterns:
            regex = re.compile(pattern, re.IGNORECASE)
            for rel, text in full_items.items():
                if regex.search(text):
                    hits.append(f"{rel}: {pattern}")
                    break
        if hits:
            results[risk] = hits[:8]
    return results


def audit(root: Path) -> Dict[str, object]:
    paths, texts = collect_corpus(root)
    findings: List[Finding] = []
    for category, patterns in PATTERNS.items():
        evidence = match_patterns(paths, texts, patterns)
        findings.append(score_category(category, evidence, texts))

    total_score = sum(item.score for item in findings)
    max_score = len(findings) * 3
    risks = detect_risks(paths, texts)

    if total_score <= 8:
        maturity = "prototype"
    elif total_score <= 16:
        maturity = "usable draft"
    elif total_score <= 23:
        maturity = "strong candidate"
    else:
        maturity = "production-ready candidate"

    return {
        "root": str(root),
        "file_count": len(paths),
        "text_file_count": len(texts),
        "score": total_score,
        "max_score": max_score,
        "maturity": maturity,
        "findings": [asdict(item) for item in findings],
        "risks": risks,
        "top_recommendations": top_recommendations(findings, risks),
    }


def top_recommendations(findings: List[Finding], risks: Dict[str, List[str]]) -> List[str]:
    recs: List[str] = []
    if risks:
        recs.append("Review detected high-risk patterns before adding new capabilities.")
    for item in sorted(findings, key=lambda f: f.score):
        for rec in item.recommendations:
            if rec not in recs:
                recs.append(rec)
            if len(recs) >= 8:
                return recs
    return recs


def render_markdown(report: Dict[str, object]) -> str:
    lines: List[str] = []
    lines.append("# Claude Superpowers Static Audit")
    lines.append("")
    lines.append(f"- Root: `{report['root']}`")
    lines.append(f"- Files scanned: {report['file_count']}")
    lines.append(f"- Text files scanned: {report['text_file_count']}")
    lines.append(f"- Score: {report['score']} / {report['max_score']}")
    lines.append(f"- Maturity: **{report['maturity']}**")
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    lines.append("| Category | Score | Evidence | Main recommendation |")
    lines.append("|---|---:|---|---|")
    for item in report["findings"]:  # type: ignore[index]
        evidence = "; ".join(item["evidence"]) if item["evidence"] else "none detected"
        recommendation = item["recommendations"][0] if item["recommendations"] else "review manually"
        lines.append(f"| {item['category']} | {item['score']} | {evidence} | {recommendation} |")
    lines.append("")

    risks = report.get("risks", {})
    lines.append("## Risk Signals")
    lines.append("")
    if risks:
        for risk, hits in risks.items():
            lines.append(f"### {risk}")
            for hit in hits:
                lines.append(f"- {hit}")
            lines.append("")
    else:
        lines.append("No high-risk text patterns detected by the static scanner. Review manually anyway.")
        lines.append("")

    lines.append("## Top Recommendations")
    lines.append("")
    for rec in report["top_recommendations"]:  # type: ignore[index]
        lines.append(f"- {rec}")
    lines.append("")
    lines.append("## Note")
    lines.append("")
    lines.append("This is a static first-pass audit. Apply the skill rubrics manually before making release decisions.")
    return "\n".join(lines)


def prepare_input(path: Path) -> Tuple[Path, tempfile.TemporaryDirectory | None]:
    if path.is_file() and path.suffix.lower() == ".zip":
        temp_dir = tempfile.TemporaryDirectory(prefix="claude_plugin_audit_")
        with zipfile.ZipFile(path) as zf:
            zf.extractall(temp_dir.name)
        return Path(temp_dir.name), temp_dir
    if path.is_dir():
        return path, None
    raise FileNotFoundError(f"Input path is not a directory or zip archive: {path}")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Claude/Claude Code plugin architecture.")
    parser.add_argument("path", help="Plugin folder or zip archive")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", help="Optional output file")
    args = parser.parse_args(argv)

    try:
        root, temp_dir = prepare_input(Path(args.path).expanduser().resolve())
        try:
            report = audit(root)
        finally:
            # Keep report data before temp cleanup. Text is already read.
            pass

        if args.format == "json":
            output = json.dumps(report, indent=2, ensure_ascii=False)
        else:
            output = render_markdown(report)

        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            print(output)

        if temp_dir is not None:
            temp_dir.cleanup()
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
