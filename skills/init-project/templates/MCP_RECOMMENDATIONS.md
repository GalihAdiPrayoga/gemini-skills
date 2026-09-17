# MCP / Plugin Recommendations — {{PROJECT_NAME}}

Recommended tooling for safe AI-assisted development. For each: function · benefit · risk · suggested permission · when. CLIs need separate install (`uv` for Python MCP servers; `winget`/`brew`/`pip` for CLIs).

## P0 — Essential
- **Context7 MCP** — current library/API docs. Avoids stale-training mistakes. Read-only. Before version-dependent code. `npx -y @upstash/context7-mcp` (or HTTP `https://mcp.context7.com/mcp`).
- **GitHub MCP** — issues/PRs/Actions. Repo read + PR scope (no admin/secret). Token via env var. Remote: `https://api.githubcopilot.com/mcp/`.
- **Playwright MCP** — browser smoke tests. Staging URL only. `npx -y @playwright/mcp@latest`.
- **Semgrep** — SAST for auth/payment/webhook/input. Read-only. `uvx semgrep-mcp` (MCP) or `semgrep scan --config auto` (CLI).
- **Gitleaks CLI** — secret scanning. Pre-commit + CI. `gitleaks detect --source . --verbose`.
- **Trivy CLI** — vuln/secret/misconfig for deps + Dockerfile. `trivy fs .`.

## P1 — High value
- **Fetch MCP** — fetch URL → text for public-doc research. `uvx mcp-server-fetch`. (Built-in WebFetch may already cover this.)
- **OpenAPI MCP** — only if an API spec exists; read/test, no mutating calls.
- **DB MCP (staging read-only)** — query staging for debugging; never prod/write/migration.
- **Renovate / Dependabot** — automated dependency-update PRs (enabled in the GitHub repo, e.g. `.github/dependabot.yml`).
- **Socket.dev / OSV-Scanner** — supply-chain + known-vuln scanning before adding/upgrading deps.

## P2 — Observability / maturity
- **Sentry / GlitchTip** — error + performance monitoring (scrub PII).
- **Grafana / Prometheus / Loki** — metrics + logs + alerts when scale justifies.
- **Sourcegraph / code search** — cross-repo impact analysis.
- **OSSF Scorecard** — repo security posture over time (GitHub Action).
