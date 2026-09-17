# AI Agent Protocol — {{PROJECT_NAME}}

Binds `AGENTS.md` (checklist), `CLAUDE.md` (rules), `SECURITY.md` (policy).

## 1. Development Workflow
1. **Understand** — restate the task; read relevant docs. Don't work from memory.
2. **Inspect** — `git status --short --branch`; read affected files; note existing patterns.
3. **Plan** — declare files, shared-file risk, constraints, security surface. Risky/new features: `/brainstorm` → `/spec-writer` → `/plan-writer` + `superpowers:writing-plans-self-improvement-assistant` first — see `CLAUDE.md` § Pipeline Wajib and `AGENTS.md` § Workflow Skills for the full skill-combination table.
4. **Implement** — `superpowers:subagent-driven-development` + `superpowers:sdd-self-improvement-assistant` for plan-driven work; minimal, reviewable change following the project's architecture either way.
5. **Validate** — run available checks ({{VALIDATE_CMDS}}, security scans) and `/qa-master` before deploy. Never claim success without reading output.
6. **Report** — Summary · Files changed · Validation run · Risks found · Not verified · Next steps.

## 2. Tool Usage Priority
| Priority | Tool | Use for |
|---|---|---|
| 1 | Context7 MCP | up-to-date library/framework/API docs before version-dependent code |
| 2 | GitHub MCP | issues, PRs, Actions, repo workflow |
| 3 | Playwright MCP | UI smoke testing when a UI flow changes |
| 4 | Semgrep | SAST on security-sensitive code |
| 5 | Gitleaks CLI | secret scan before commits touching config/env/docs |
| 6 | Trivy CLI | Dockerfile / deps / filesystem / misconfig |
| 7 | OpenAPI MCP | only if an API contract exists (read/test, no mutating calls) |
| 8 | DB MCP | **staging read-only only** — never production/write/migration |

> Tool unavailable → record as a **missing dependency** + manual install, continue with a safe fallback. Don't stop.

## 3. Feature Completion Checklist
- [ ] build passes · lint/typecheck clean (where available)
- [ ] security scan run where the CLI is available
- [ ] critical flow tested (manual or automated)
- [ ] relevant docs updated in the same change (docs-as-code)
- [ ] risks + unverified items documented

## 4. Forbidden Behavior
- No production deploy; no reading/printing/committing secret files; no production database access.
- No destructive commands (`rm -rf`, `DROP`/`TRUNCATE`, prod migration, storage deletion).
- No new dependency without justification (why / alternatives / risk / maintenance signal).
- No large business-logic change without understanding the existing flow first.
