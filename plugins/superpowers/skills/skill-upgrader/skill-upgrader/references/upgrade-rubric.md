# Upgrade Rubric

Use this rubric when auditing or upgrading another skill. The goal is not to make the skill longer. The goal is to make it more reliable in real cases.

## Scoring Overview

Score each area from 0 to 5.

- 0 = missing or harmful
- 1 = present but vague
- 2 = usable only for ideal cases
- 3 = usable for common cases
- 4 = strong for real cases
- 5 = production-ready and testable

## 1. Trigger and Scope

Check whether the frontmatter description clearly explains:

- The task the skill performs.
- Specific user requests that should trigger it.
- File types, systems, domains, or workflows it handles.
- What is out of scope.

Upgrade moves:

- Replace generic language with concrete trigger phrases.
- Add input types and task contexts.
- Add boundaries so the skill does not trigger too broadly.

## 2. Input and Output Contract

Check whether the skill defines:

- Expected input.
- Allowed input variants.
- Required output.
- Output format.
- What to do when input is incomplete.

Upgrade moves:

- Add an input decision tree.
- Add output templates.
- Add assumptions and partial-output rules.

## 3. Workflow Reliability

Check whether the skill gives a clear sequence of actions.

Strong workflows include:

- Entry condition.
- Step-by-step process.
- Conditional branches.
- Validation step.
- Final delivery rules.

Upgrade moves:

- Convert paragraphs into ordered workflows.
- Add branch handling for different inputs.
- Add validation checkpoints after fragile steps.

## 4. Real-Case Readiness

Check whether the skill handles messy business situations:

- Missing data.
- Conflicting instructions.
- Multiple files.
- Stale docs.
- Tool failures.
- Permission limitations.
- Ambiguous business terms.
- Large assets.
- Unsupported input types.

Upgrade moves:

- Add explicit fallback rules.
- Add business-context discovery questions only when needed.
- Add realistic examples and negative examples.

## 5. Tool and Connector Rules

Check whether the skill states:

- Which tools or connectors to use.
- When to use them.
- What to do when they fail.
- What must never be done.

Upgrade moves:

- Add tool selection rules.
- Add source precedence.
- Add citation or validation requirements if the skill uses retrieved knowledge.

## 6. Resource Organization

Check whether the skill uses resources efficiently:

- `SKILL.md` contains only the control plane.
- Long guidance is moved into `references/`.
- Scripts are used for deterministic repetitive work.
- Assets are included only when needed.
- Placeholder files are removed.

Upgrade moves:

- Split long sections into references.
- Delete example placeholder files.
- Add scripts for validation, parsing, or packaging checks.

## 7. Output Quality and Consistency

Check whether outputs are predictable and useful.

Strong output contracts define:

- Required sections.
- Optional sections.
- Naming rules.
- File naming rules.
- Quality checklist.

Upgrade moves:

- Add final response templates.
- Add file naming conventions.
- Add a short changelog format.

## 8. Validation and Testing

Check whether the skill includes ways to verify success.

Strong validation includes:

- Structural validation.
- Representative test cases.
- Edge-case tests.
- Script tests when scripts are included.
- Packaging checks when the output is a skill archive.

Upgrade moves:

- Add a test checklist.
- Add a deterministic audit script.
- Add sample real-case prompts.

## Final Recommendation Labels

Use these labels in the audit summary:

- Critical: must fix before packaging.
- High: likely to fail in real cases.
- Medium: quality or consistency improvement.
- Low: polish or maintainability improvement.
