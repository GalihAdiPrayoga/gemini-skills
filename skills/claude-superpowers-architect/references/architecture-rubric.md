# Architecture Rubric

Use this rubric to evaluate whether a Claude or Claude Code plugin is only a prompt pack or a real-case-ready agentic system.

## Capability Categories

### 1. Commands
User-facing entrypoints that users invoke directly.

Strong command design includes:
- Clear command name and purpose.
- Expected inputs and optional flags.
- Preconditions and project state assumptions.
- Output format.
- Example invocation.
- Failure behavior.

Weak command design includes:
- Generic names such as `improve`, `fix`, or `analyze` without scope.
- Hidden side effects.
- No examples.
- No distinction between read-only and mutating operations.

### 2. Hooks
Automations triggered by events.

Strong hook design includes:
- Explicit event trigger.
- Scope limits.
- Dry-run mode for risky actions.
- Timeout and retry rules.
- Safe failure behavior.
- Logging.

Flag hooks that run shell commands, modify files, commit code, install packages, or call network services without guardrails.

### 3. MCP Tools
External tools that extend capability.

Strong MCP design includes:
- Tool inventory.
- Permission model.
- Read versus write separation.
- Input schema validation.
- Output validation.
- Fallback when unavailable.
- Confirmation for destructive or externally visible actions.

### 4. Subagents
Delegated roles with distinct responsibilities.

Strong subagent design includes:
- Unique role and decision boundary.
- Clear input and output contract.
- Escalation path when uncertain.
- No duplicated responsibilities.
- A coordinator that synthesizes results.

Common useful subagents:
- Planner: turns user intent into task plan.
- Implementer: edits code or config.
- Reviewer: checks correctness and maintainability.
- Tester: designs and runs tests.
- Security auditor: detects unsafe tool use and prompt injection.
- Release manager: validates docs, changelog, install, rollback.

### 5. Context Files
Persistent instructions and project knowledge.

Strong context design includes:
- Stable project rules in `CLAUDE.md` or `AGENTS.md`.
- Separate files for long references.
- Clear precedence rules.
- Minimal duplication.
- Versioned assumptions.

Weak context design includes:
- One giant file mixing rules, examples, secrets, and stale notes.
- No path-specific rules in a monorepo.
- No instruction for resolving conflict between docs.

### 6. Validation Layer
The plugin must verify its work.

Validation options:
- Static checks.
- Unit/integration tests.
- Type checks.
- Linting.
- Schema validation.
- Dry-run previews.
- Before/after diffs.
- Human approval checkpoints.

## Scoring

Score each category from 0 to 3:

- 0: missing.
- 1: mentioned but vague.
- 2: usable but incomplete.
- 3: real-case-ready with validation and failure handling.

Interpretation:

- 0-6: concept/prototype only.
- 7-12: usable draft, needs hardening.
- 13-18: strong plugin candidate.
- 19-21: production-ready architecture if implementation matches the design.

## Upgrade Priority

When many issues exist, fix in this order:

1. Dangerous actions without approval.
2. Missing triggers and input/output contracts.
3. Missing validation and fallback.
4. Missing real-case workflows.
5. Context file bloat or conflicts.
6. Poor release docs.
