---
name: skill-upgrader
description: audit, harden, and upgrade existing chatgpt skills into production-ready versions for real business cases. use when asked to improve, upgrade, refactor, validate, package, or make another skill more powerful, especially when input is a skill.zip, a skill folder, pasted skill.md content, draft instructions, or a real-case failure. focuses on edge cases, workflow clarity, trigger descriptions, output consistency, tool and connector rules, validation, and producing a complete upgraded skill.zip.
---

# Skill Upgrader

## Overview

Use this skill to upgrade another ChatGPT skill so it performs better on real business cases, not only ideal examples. The main deliverable is a complete upgraded skill package named `skill.zip`, unless the user asks only for an audit or draft.

This skill is a meta-skill. It improves skill structure, trigger quality, workflow reliability, edge-case handling, output contracts, validation rules, resource organization, and real-case readiness.

## Operating Principles

- Treat vague requests like "make this skill more powerful" as a request to make the skill more reliable under real usage, ambiguity, missing inputs, edge cases, tool failures, and business constraints.
- Preserve the original skill's intent unless the user explicitly asks to change its scope.
- Prefer clear, reusable workflow instructions over motivational or generic language.
- Prefer compact `SKILL.md` instructions and move detailed rubrics, examples, or long checklists into `references/`.
- Add scripts only when deterministic checks or repeatable file operations materially improve reliability.
- Always remove placeholder files from initialized skills before packaging.
- Keep the final package at or below the 25 MB upload limit.

## Input Decision Tree

1. If the user provides a `.zip` skill archive:
   - Unpack it.
   - Locate `SKILL.md` files.
   - If exactly one skill is present, upgrade that skill.
   - If multiple skills are present, do not merge them. Ask the user which single skill should be upgraded, or return a clear note that one archive must contain one target skill for this workflow.

2. If the user provides a skill folder:
   - Inspect `SKILL.md`, `agents/openai.yaml`, `references/`, `scripts/`, and `assets/`.
   - Preserve useful resources.
   - Remove stale placeholder resources.

3. If the user pastes only `SKILL.md` content:
   - Reconstruct a valid skill folder.
   - Add `agents/openai.yaml`.
   - Add references or scripts only when they improve the upgraded skill.

4. If the user provides only an idea or draft instructions:
   - Build a new upgraded skill from the idea.
   - Ask for expected input, expected output, and connector/tool requirements when missing and necessary.
   - If the user wants immediate output and enough intent is available, make reasonable assumptions and state them.

## Upgrade Workflow

### 1. Normalize the target skill

Create or reconstruct a complete skill folder with this minimum structure:

```text
skill-name/
├── SKILL.md
└── agents/
    └── openai.yaml
```

Optional resources may include:

```text
references/  detailed rubrics, examples, schemas, business rules
scripts/     deterministic validators, parsers, generators, or converters
assets/      templates or files used in final outputs
```

### 2. Run the baseline audit

When a skill folder is available, run:

```bash
python scripts/skill_audit.py /path/to/target-skill
```

Use the audit as a starting point, not as the only source of truth. Also inspect the skill manually for business context, tool assumptions, edge cases, and real-case gaps.

For full audit criteria, consult `references/upgrade-rubric.md`.

### 3. Build the real-case model

Before rewriting, infer or collect:

- Real user who will invoke the skill.
- Business situation where the skill is used.
- Expected inputs and messy input variants.
- Expected output and acceptance criteria.
- Tools, connectors, files, or APIs involved.
- Failure modes such as missing data, conflicting instructions, invalid files, stale docs, ambiguous requests, permission errors, tool errors, or oversized assets.
- Validation checks that prove the upgraded skill worked.

If the user supplies real examples, map each example into happy path, edge cases, and expected output. If no examples are supplied, create 2-3 realistic test scenarios based on the skill's domain and mark them as assumptions.

For more guidance, consult `references/real-case-hardening.md`.

### 4. Redesign the frontmatter

The `description` is the trigger surface. It must include:

- What the skill does.
- When to use it.
- Concrete input types, file types, systems, or task phrases that should trigger it.
- Boundaries of scope.

Rules:

- Keep frontmatter lowercase where possible.
- Use only `name` and `description` unless the platform requires otherwise.
- Do not hide trigger instructions inside the body. The body is loaded only after the skill triggers.
- Avoid vague phrases like "make better", "advanced assistant", or unbounded capability claims.

### 5. Redesign the body workflow

Upgrade the body into a practical operating manual. Include these sections when relevant:

- Overview.
- Input decision tree.
- Step-by-step workflow.
- Tool and connector rules.
- Edge-case handling.
- Output contract.
- Validation checklist.
- Packaging or delivery rules.
- Examples only when they teach non-obvious behavior.

Use imperative instructions. Avoid explaining obvious ChatGPT capabilities.

### 6. Strengthen edge-case handling

Add explicit rules for:

- Missing or partial input.
- Contradictory requirements.
- Multiple files or multiple target skills.
- Stale or deprecated source material.
- Tool errors and fallback behavior.
- Ambiguous business terms.
- Oversized assets.
- Unsafe or unsupported requests.
- Cases where the output should be partial but honest instead of blocked.

### 7. Improve workflow reliability

For every important task step, define:

- Entry condition.
- Action.
- Decision branch.
- Validation signal.
- Expected output.

Use conditional workflows for tasks with multiple paths. Use deterministic scripts when the same check is fragile or repetitive.

### 8. Design a clear output contract

Before finalizing, define exactly what the skill should produce. For updated skills, the default is:

```text
skill.zip
```

When useful, also provide a short changelog with:

- What was upgraded.
- Important assumptions.
- Remaining limitations.
- How to test the upgraded skill on a real case.

For final response patterns, consult `references/output-contract.md`.

### 9. Validate and package

Before returning the upgraded skill:

1. Confirm `SKILL.md` exists and has valid frontmatter.
2. Confirm `agents/openai.yaml` exists.
3. Remove generated placeholder files that are not needed.
4. Test any included scripts with representative input.
5. Run the available skill validator or packaging script.
6. Package the final upgraded skill as exactly `skill.zip`.
7. Share the downloadable `skill.zip`.

## Quality Bar

A good upgraded skill must be:

- Triggerable: the description clearly says when to use it.
- Realistic: it handles messy real inputs, not just perfect examples.
- Operational: it tells ChatGPT what to do step by step.
- Bounded: it states what to do when scope is unclear or unsupported.
- Testable: it includes validation signals or sample scenarios.
- Efficient: it avoids dumping unnecessary context into `SKILL.md`.
- Packaged: it is delivered as a complete valid `skill.zip` when requested.

## Common Upgrade Moves

- Convert vague sections into decision trees.
- Move long domain rules into `references/`.
- Add a deterministic audit or validation script.
- Add realistic examples with messy inputs.
- Add output templates for consistency.
- Add fallback behavior for tool failure.
- Add clear constraints for package size, unsupported inputs, or unsafe requests.
- Rewrite the frontmatter description so the skill triggers at the right time.

## Anti-Patterns to Remove

- Unresolved setup placeholders from templates.
- Generic personality-only advice without task-specific meaning.
- Overly broad claims such as "handle all cases".
- Long theoretical background that is not used during execution.
- Hidden trigger instructions only in the body.
- Unused example files from skill initialization.
- Instructions that require unavailable tools or unspecified connectors.

## Final Response Rules

When returning an upgraded skill, keep the response short and include the link to `skill.zip`. Mention only the most important upgrades and any assumptions that matter.
