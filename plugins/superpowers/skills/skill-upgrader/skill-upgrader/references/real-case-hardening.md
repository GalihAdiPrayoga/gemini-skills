# Real-Case Hardening Guide

Use this guide when a skill looks valid but weak for real business usage.

## Real-Case Model

For each target skill, identify:

1. User role: who invokes it.
2. Business goal: why the output matters.
3. Input reality: what messy or incomplete input looks like.
4. Output acceptance: what a good result must include.
5. Failure modes: how the task breaks in real life.
6. Constraints: security, privacy, timeline, formatting, tools, package size, or review requirements.

## Hardening Questions

Ask or infer these questions:

- What happens if the user gives only partial input?
- What happens if the user gives too much input?
- What happens if multiple files conflict?
- What happens if the required connector is unavailable?
- What must be cited, validated, or tested?
- What should the skill refuse or redirect?
- What should be preserved from the original skill?
- What can be safely assumed?

## Edge-Case Categories

Add explicit handling for the categories that apply.

### Input Edge Cases

- Empty input.
- Partial draft.
- Wrong file type.
- Multiple candidate files.
- Archive contains more than one target skill.
- Pasted text lacks frontmatter.
- Old skill has invalid YAML.

### Workflow Edge Cases

- Required script fails.
- Validator fails.
- Tool returns incomplete output.
- Packaging exceeds size limit.
- Required connector is not enabled.
- User asks for unsupported asynchronous work.

### Business Edge Cases

- Conflicting stakeholder goals.
- Ambiguous department terms.
- Old policy or deprecated doc.
- Missing data ownership.
- Compliance-sensitive output.
- Output will be used by executives or clients.

## Hardening Patterns

### Pattern 1: Input Decision Tree

Use when the skill accepts more than one input type.

```markdown
1. If the user uploads a ZIP, inspect it first.
2. If the user pastes text, reconstruct missing structure.
3. If the user gives only an idea, ask for missing input/output details or state assumptions.
```

### Pattern 2: Validation Gate

Use when the skill creates a file or modifies structured content.

```markdown
Before final response:
- Confirm required files exist.
- Run validation.
- Test any scripts.
- Package with the required filename.
```

### Pattern 3: Partial But Honest Output

Use when the user expects progress but some data is missing.

```markdown
If complete execution is blocked, return the best completed artifact or draft, explain what was missing, and list exact next actions.
```

### Pattern 4: Realistic Test Scenarios

Use when no real case is supplied.

```markdown
Create 2-3 assumed test scenarios:
- Happy path.
- Messy input path.
- Failure or missing-data path.
```

## Real-Case Upgrade Checklist

Before packaging, confirm:

- The skill can start from realistic user prompts.
- It does not depend on unstated context.
- It explains how to handle incomplete input.
- It has a validation step.
- It has final output rules.
- It has no unused placeholder files.
- It preserves useful existing assets.
