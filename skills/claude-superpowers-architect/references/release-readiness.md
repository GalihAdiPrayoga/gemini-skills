# Release Readiness

Use this checklist before calling a Claude superpowers plugin ready.

## Installation

- Clear installation steps.
- Supported Claude/Claude Code versions or assumptions.
- Required environment variables documented.
- Optional dependencies separated from required dependencies.
- Failure mode for missing dependency documented.

## Configuration

- Example config included.
- Safe defaults used.
- Dangerous capabilities disabled by default.
- Permissions documented.
- Path and monorepo configuration documented.

## Documentation

- README explains what the plugin does and does not do.
- Commands are listed with examples.
- Hooks are listed with triggers and side effects.
- MCP tools are listed with read/write class.
- Subagents are listed with responsibilities.
- Context files are explained.

## Testing

- Test prompts cover normal flows.
- Test prompts cover ambiguous requests.
- Test prompts cover tool failure.
- Test prompts cover prompt injection attempts.
- Tests cover install and uninstall.
- Manual QA checklist exists when automated tests are not possible.

## Safety

- Destructive operations require approval.
- Externally visible actions require approval.
- Secrets are not logged.
- Tool output is treated as untrusted.
- Rollback path is documented.
- Audit trail exists for high-impact actions.

## Release Artifacts

- Version number.
- Changelog.
- Migration notes for breaking changes.
- Known limitations.
- Troubleshooting section.
- Example workflows.

## Go or No-Go

No-go if any of these are true:
- The plugin can delete, publish, deploy, email, or update external systems without approval.
- The plugin has no validation path.
- The plugin has no failure handling for unavailable tools.
- The plugin relies on a giant context file with unclear precedence.
- The plugin claims production readiness but has no test scenarios.
