# Real-Case Workflow Patterns

Use these patterns to turn plugin features into usable workflows.

## Pattern 1: Investigate Before Acting

Use for bug fixing, refactoring, architecture changes, or migrations.

Workflow:
1. Read relevant files and context.
2. Build a hypothesis.
3. Identify affected modules.
4. Propose a change plan.
5. Make the smallest safe change.
6. Run validation.
7. Summarize diff, tests, and remaining risk.

Upgrade requirement:
- Never allow the plugin to edit code before it identifies affected files and validation strategy.

## Pattern 2: Read-Only First, Mutate Later

Use for MCP tools, database access, filesystem operations, GitHub actions, ticketing systems, email, calendar, and deployment tools.

Workflow:
1. Discover current state with read-only actions.
2. Present intended mutation.
3. Ask for approval unless prior approval is explicit.
4. Execute mutation.
5. Verify result.
6. Log what changed.

## Pattern 3: Business Workflow Translation

Use when the user gives a business goal such as improve payroll closing, automate support triage, prepare release, or build HR dashboard workflow.

Workflow:
1. Identify actors.
2. Identify business objects.
3. Identify state transitions.
4. Identify approvals.
5. Identify exceptions.
6. Identify audit trail.
7. Convert into command/hook/tool/subagent design.

## Pattern 4: Monorepo Safe Navigation

Use for large repositories.

Workflow:
1. Identify repo root and package boundaries.
2. Read local context files nearest the target path.
3. Detect package manager and build/test commands.
4. Avoid global edits unless required.
5. Run targeted validation before full validation.
6. Report which package was affected.

## Pattern 5: Release Assistant

Use when plugin helps release code, docs, or packages.

Workflow:
1. Check version and changelog.
2. Check tests and build.
3. Check breaking changes.
4. Check docs and migration notes.
5. Check rollback procedure.
6. Prepare release notes.
7. Require approval before publishing.

## Pattern 6: Security Review

Use when plugin touches secrets, permissions, auth, network calls, CI/CD, package installation, shell commands, or external APIs.

Workflow:
1. Identify trust boundaries.
2. Identify untrusted inputs.
3. Identify sensitive outputs.
4. Identify destructive actions.
5. Add approval gates.
6. Add logging and validation.
7. Recommend least-privilege permissions.
