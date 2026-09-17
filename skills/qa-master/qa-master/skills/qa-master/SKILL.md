---
name: qa-master
description: Use when asked to QA, verify, investigate bugs, run pre-deploy checks, assess production readiness, validate UI/API/security behavior, execute live or staging smoke tests, or decide GO/NO-GO for a code change.
---

# QA Master - Adversarial Quality Gate and Executor

## Mission

QA Master is a go/no-go decision system. It verifies the right repository, branch, deployment target, user flow, security boundary, and regression risk before giving any approval.

Do not treat QA as a checklist. Treat it as an evidence-based release gate.

## Operating Rules

1. Verify context before testing.
2. Test the deployed target when the change is already deployed.
3. Run security gates before deploy for sensitive changes.
4. Never report PASS without command, browser, scanner, or probe evidence.
5. Do not skip gates silently. Every skipped gate needs a reason in the final report.
6. Secret findings are hard blockers.
7. Build failure is a blocker unless the user explicitly asks for investigation mode.
8. Security reviewer BLOCK, critical scanner finding, or broken authorization is NO-GO.
9. A live target that does not update is BLOCK for deployed QA.
10. Use the strongest available test harness before creating new tests.

## Scope Classification

Classify every change before selecting tiers.

```text
surface | examples | risk
ui | pages, components, forms, tables, charts | visual, a11y, regression
api | route handlers, server actions, webhooks | input, auth, contracts, abuse
auth | login, session, token, middleware | account takeover, bypass
permission | RBAC, tenant, branch, owner access | privilege escalation
db | schema, Prisma, SQL, migration | data loss, integrity, performance
env | secrets, config, deploy variables | leak, wrong target, outage
dependency | package changes, lockfile changes | CVE, supply chain
payment | checkout, billing, webhook | fraud, double charge
upload | file handling, parsing, storage | malware, path traversal, leakage
ai | prompts, tools, automation | prompt injection, data exposure
```

## Tier Selection

| Situation | Required tiers |
|---|---|
| Tiny non-sensitive hotfix | T0 + T1 |
| UI or feature change | T0 + T1 + T2 + T5 + T8 |
| API, server action, or user input | T0 + T1 + T2 + T3 + T4 + T5 |
| Auth, RBAC, payment, webhook, upload, schema, env | T0 + T1 + T2 + T3 + T4 + T5 + T6 + T7 |
| Pre-deploy, production readiness, deploy branch, or live QA | T0 through T14 |
| Bug report | T0 + targeted T3/T4/T5/T6 + regression check |
| Hotfix after incident | T0 + T1 + targeted security + live smoke + regression |
| Launch, campaign, or expected-traffic-spike readiness | T0 + T1 + T2 + T7 + T11 + T12 |
| New personal-data field, form, or user-facing tracking | T0 + T1 + T3 + T13 |

If uncertain, choose the higher tier.

**T10 is additive, not alternative.** Whenever the commit message, PR description, or user request claims a specific correctness or security guarantee — "implement concurrency control," "prevent race condition," "atomic," "thread-safe," "fix IDOR," "add RBAC," "enforce ownership," "idempotent," "prevent duplicate," "fix data loss," or equivalent — add T10 on top of whatever tiers the table above already selected, regardless of diff size. A two-line fix can carry the same false sense of security as a thousand-line one.

**T11-T14 are additive too.** Add T11 (production readiness) whenever the change reaches a live target with real users. Add T12 (load/scale) whenever the endpoint is public, payment-related, or expected to see concurrent or spiky traffic. Add T13 (compliance/privacy/standards) whenever personal data or an accessibility-sensitive surface is touched, or when findings must be defensible against a named external standard. Add T14 (exploratory) whenever time allows, especially for anything new and user-facing — treat it as the layer that finds what no script above was written to catch.

## Status Language

Use only these verdicts.

```text
PASS  = evidence supports expected behavior
WARN  = issue exists, but not release blocking
BLOCK = release must stop until fixed
SKIP  = not run, with explicit reason
INFO  = observation only
```

Never write “secure”. Write “no findings in tools run” when scans return clean.

## T0 - Context, Repository, Branch, Target

Question: Am I testing the right thing?

Run first, in the intended repository.

```bash
pwd
git status --short --branch
git remote -v
git log --oneline -10
git diff --name-only HEAD~1
git diff --stat HEAD~1
```

Check nested repositories when docs or folder structure suggest them.

```bash
git -C <nested-repo> status --short --branch 2>/dev/null || true
```

Record:

- repository path
- branch
- upstream ahead/behind
- current commit SHA
- deploy source branch
- local, preview, staging, or production target
- target URL, usually `QA_BASE`
- changed files
- changed surfaces
- selected tiers
- originating ticket, issue, or requirement reference, if one exists — record "none provided" rather than omitting the line

If target is unknown, infer from project config and docs. If still unknown, test local and mark deploy smoke as SKIP with reason.

## T1 - Fast Correctness and Secret Gate

Question: Does the code pass basic correctness and secret checks?

```bash
npx tsc --noEmit
npm run lint
gitleaks detect --source . --no-banner --redact --exit-code 1
```

If the project has a small relevant test command, run it here.

```bash
npm test -- --runInBand
# or
npm run test -- --run
```

Decision rules:

- Gitleaks finding = BLOCK. Stop and tell the user to rotate exposed credentials.
- Type or lint failure = BLOCK unless user requested investigation mode.
- Missing command = WARN or SKIP with exact reason.

## T2 - Build, Dependency, and Config Gate

Question: Can this build safely and do dependencies/configs pass basic checks?

```bash
npm run build
npm audit --audit-level=high
trivy fs . --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1
```

If dependencies changed, record:

- package name
- version
- lockfile change
- audit result
- reason the dependency is needed

If `trivy` is missing, report it as SKIP with the install command. Do not silently ignore it.

## T3 - Security Deep Scan

Question: Did sensitive code introduce exploitable behavior?

Run for sensitive surfaces. If uncertain, scan `src/`.

```bash
semgrep --config auto <changed-sensitive-paths>
gitleaks detect --source . --log-opts="HEAD~20..HEAD" --no-banner --redact --exit-code 1
```

Manual pattern checks. Read every finding before classifying.

```bash
# XSS and dynamic execution
grep -rn "dangerouslySetInnerHTML\|eval(\|new Function(" src/ --include="*.ts" --include="*.tsx" || true

# raw database access
grep -rn 'prisma\.\$queryRaw\|prisma\.\$executeRaw' src/ --include="*.ts" || true

# server actions
grep -rn "'use server'\|\"use server\"" src/ --include="*.ts" --include="*.tsx" || true

# API route handlers
grep -rn "export async function \(GET\|POST\|PUT\|PATCH\|DELETE\)" src/app/api --include="*.ts" || true

# environment boundary
grep -rn "process\.env\." src/app --include="*.ts" --include="*.tsx" | grep -v "NEXT_PUBLIC_\|route\.ts\|server" || true

# hardcoded credentials
grep -rn "Bearer \|Basic \|sk_live\|sk_test\|password.*=.*['\"]" src/ --include="*.ts" --include="*.tsx" | grep -v "process.env\|placeholder\|example\|test" || true
```

For auth, API, upload, payment, webhook, RBAC, tenant, or branch logic, dispatch or request targeted security review when available.

Security review input must include:

```text
repo path
branch
commit SHA
diff range
changed files
target URL
test outputs
known risks
```

Classify findings:

- credential leak = BLOCK
- auth bypass = BLOCK
- cross-tenant or cross-branch access = BLOCK
- unsanitized dynamic HTML with user input = BLOCK or WARN based on exploitability
- raw SQL with untrusted input = BLOCK
- missing rate limit on public mutation = WARN or BLOCK based on abuse risk

## T4 - API Adversarial and Contract Tests

Question: Can bad clients, replays, or races break it?

For each changed endpoint or server action, create a probe table.

```text
case | payload/auth | expected | actual | verdict
```

Minimum probes:

- no auth
- malformed auth
- wrong role
- wrong tenant, branch, or owner
- missing origin or forged origin when relevant
- malformed JSON
- `null`, array body, empty object
- missing required fields
- invalid type, range, enum, and size
- unknown fields
- duplicate request
- 5 to 20 parallel duplicate mutations for sensitive writes
- rate-limit behavior for public endpoints
- response shape and backward compatibility

Example curl probe:

```bash
curl -s -o /tmp/qa_body.txt -w "%{http_code}\n" -X POST "$URL" \
  -H "Origin: $ORIGIN" \
  -H "Content-Type: application/json" \
  -d '{"bad":true}'
cat /tmp/qa_body.txt
```

Do not over-trust status code. Inspect body, database state, audit logs, emails, files, and UI side effects for mutations.

## T5 - Behavioral E2E and User Flow

Question: Does the real user flow work?

Discover the existing harness.

```bash
ls e2e playwright.config.* package.json 2>/dev/null || true
cat package.json
cat e2e/package.json 2>/dev/null || true
```

Prefer existing tests. Use `npm --prefix` for isolated E2E packages.

```bash
npm --prefix e2e install
npm --prefix e2e exec playwright install chromium
QA_BASE=<target-url> npm --prefix e2e exec playwright test -- --reporter=list
```

Installing E2E dependencies can modify `package-lock.json` even when the only goal was running tests. If `npm --prefix e2e install` (or any install step above) changes the lockfile, report that diff in the final report — do not leave a dirtied lockfile uncommitted and unreported.

If the root project owns Playwright:

```bash
npx playwright install chromium
QA_BASE=<target-url> npx playwright test --reporter=list
```

### Dogfood as a real user (isolated identity)

Run this whenever no existing harness covers the changed flow, whenever the change is new enough that scripted assertions do not exist yet, or whenever you need ground truth beyond what a browser script or a single curl probe proves. This is not optional filler — a feature can pass every scripted check and still not actually work end-to-end for the person who is meant to use it, especially right after a large or newly-merged batch of changes. Do this against the actual target (local, staging, or production per T0), not a mocked environment.

1. **Create a disposable, clearly-labeled identity for the relevant persona** using the project's own real provisioning path (its admin API, a seed script, or equivalent) — never reuse a real customer's account or a shared team login. Label it so it is unmistakably QA data, e.g. an email like `qa-<feature>-<timestamp>@<internal-marker>.test`.

   ```bash
   # illustrative shape — adapt to the project's actual auth/user-provisioning mechanism
   # (Supabase admin.createUser, a Prisma seed, an internal signup endpoint with a test flag, etc.)
   ```

2. **Obtain a real, working session for that identity** (a real access token / cookie / login), the same kind the actual frontend would hold — not a service-role or admin bypass token, unless the persona under test genuinely has elevated access.

3. **Walk the full flow in the real sequence a user would follow**, not isolated single-endpoint calls: sign in → the actual feature steps in order → whatever happens next (a second device loading the same data, a different role reacting to the change, a follow-up action). If the feature involves more than one persona interacting (requester/approver, two collaborators editing the same resource, buyer/seller), exercise both sides and the interaction between them, not just one in isolation.

4. **Verify the outcome independently of the API's own response.** A 200/201 status or a "success" JSON body is a claim, not proof — confirm the actual persisted result by reading it back through a separate path (a fresh GET, a direct read-only DB query, a re-render of the page) before treating the step as PASS. This is the same discipline as T4's "do not over-trust status code," applied to a full flow instead of one request.

5. **Never trigger real-world side effects with cost or external reach** — a real payment charge, a real SMS/WhatsApp/push send, an email to a real inbox outside the disposable identity you created — unless the user has explicitly authorized it for this test. Prefer sandbox/test-mode credentials for those specific steps when the project has them; otherwise skip that sub-step and say so in the report rather than guessing it is safe.

6. **Delete everything the walkthrough created before finishing** — the disposable identity, any records it produced, any files it uploaded. Record what was created and confirm removal in the final report; do not leave throwaway QA data sitting in a shared, staging, or production environment.

Must cover:

- changed happy path
- critical regression around the changed area
- empty state
- loading state
- error state
- mobile viewport for UI changes
- keyboard navigation for UI changes
- the dogfood walkthrough above for any newly-merged or newly-claimed feature without existing scripted coverage
- login/session behavior when relevant

When credentials must not be logged, use interactive browser tooling instead of printing secrets.

## T6 - RBAC, Authorization, and Data Isolation Matrix

Question: Can each role only access what it should?

Required for dashboards, internal tools, auth, permissions, staff apps, tenants, branches, and owner-scoped data.

Build this matrix.

```text
role | route/action | own scope | other scope | expected | actual | verdict
```

Minimum checks:

- unauthenticated user is denied or redirected
- lowest role is denied for privileged route/action
- allowed role can access own scope
- same allowed role cannot access other branch, tenant, owner, or organization
- UI gating matches server/API enforcement
- direct API call cannot bypass hidden UI controls
- object IDs from another scope are rejected

Example matrix:

```text
SUPER_ADMIN | /spv | all branches | all branches | allow | allow | PASS
SPV | /reports/branch-a | own branch | branch-b | deny other | deny | PASS
CS | /admin/users | none | none | deny | deny | PASS
anonymous | /dashboard | none | none | redirect | redirect | PASS
```

Missing test accounts or data = SKIP only if creation is impossible. Otherwise create minimal labeled QA data when allowed.

## T7 - Deploy Gate and Live Smoke

Question: Is the tested version really live?

Required when a branch triggers deploy or user asks for deployed QA.

Steps:

1. Identify deploy branch and target URL.
2. Confirm whether a push happened.
3. Wait for deploy completion through CI, Coolify, Vercel, GitHub checks, or endpoint polling. If the platform exposes Vercel Checks or GitHub Environment protection rules, treat any failed or blocked check as BLOCK for the deploy gate — do not proceed to live smoke against an environment the platform itself refused to promote.
4. Prove new version is live through route, asset, commit marker, health endpoint, or visible change.
5. Run live smoke on the target.

Polling example:

```bash
for i in $(seq 1 20); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$QA_BASE/<new-route>" --max-time 15)
  echo "attempt $i: $code"
  [ "$code" != "404" ] && [ "$code" != "000" ] && break
  sleep 30
done
```

Smoke probes:

```bash
curl -s -o /dev/null -w "%{http_code}\n" "$QA_BASE"
curl -s -o /dev/null -w "%{http_code}\n" "$QA_BASE/<new-route-or-api>"
```

If the deployed version is not updated, BLOCK deployed QA. Do not claim live validation. A failed Vercel Check or blocked GitHub Environment protection rule is the same failure mode — BLOCK for the same reason, since the target was never actually promoted.

## T8 - Accessibility, Visual, and Performance

Question: Did the UI remain usable, accessible, and reasonably fast?

For UI changes:

- keyboard tab through main controls
- verify visible focus state
- verify labels, roles, table semantics, dialogs, tabs, and aria attributes
- test desktop and mobile breakpoints
- capture screenshots when visual surface changed
- check route size from build output
- run automated accessibility checks when available
- run Lighthouse when available and useful

Useful probes:

```bash
npm ls @axe-core/playwright 2>/dev/null || echo "axe not installed"
npx lighthouse "$QA_BASE" --only-categories=performance,accessibility --chrome-flags="--headless" 2>/dev/null || true
```

Treat serious or critical accessibility violations on changed user-critical flows as WARN or BLOCK based on impact.

## T9 - Regression, Coverage, Mutation, and Contracts

Question: What else could break because of this change?

Run impact analysis.

```bash
git diff --name-only HEAD~1
for f in $(git diff --name-only HEAD~1); do
  b=$(basename "$f" .ts | sed 's/\.tsx$//')
  grep -rn "from.*$b\|import.*$b" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | head -20
done
```

Run supported test depth.

```bash
npm test -- --coverage
npm ls @stryker-mutator/core 2>/dev/null && npx stryker run
```

For contract systems:

- OpenAPI schema diff
- tRPC procedure compatibility
- Zod schema compatibility
- generated client updates
- response shape changes

For database changes:

- migration applies cleanly
- rollback path exists or is documented
- NOT NULL fields have safe defaults
- existing data remains valid
- indexes fit query patterns
- long locks are avoided
- destructive changes require explicit approval

For performance-sensitive paths:

```bash
grep -rn "\.findMany\|\.findFirst\|\.findUnique" src/server --include="*.ts" -l | xargs grep -l "forEach\|\.map(\|for .*of" 2>/dev/null || true
```

## T10 - Critical Claim & Blast-Radius Analysis

Question: Does this change actually deliver the correctness/security guarantee it claims — on every path that touches the affected resource, not just the one that was tested?

Mandatory whenever the trigger phrase in Tier Selection applies. A tier-by-tier PASS on T0-T9 does not prove a claimed guarantee holds: type checks, lint, build, and generic scanners cannot see whether an invariant is actually enforced everywhere it needs to be — that requires targeted reasoning about the specific claim, not more automated tooling.

### 1. State the invariant in one sentence

Write down exactly what must never happen if this code is correct — e.g. "two concurrent writes to the same record must never silently discard one of them," or "a user must never read another tenant's row through any route." If the claim cannot be stated this concretely, it is too vague to verify; ask for the specific guarantee before proceeding.

### 2. Enumerate every path that touches the same resource, not just the diffed one

```bash
# find every route/function that reads or writes the same table, key, or shared state the change touches
grep -rln "<table_or_resource_name>" src/ --include="*.ts" --include="*.tsx"
```

For every hit outside the current diff, ask: does it go through the same protected path, or a separate/legacy/raw one? A guard wired into a shared helper is worthless if a sibling handler bypasses that helper with its own raw read-modify-write.

### 3. Verify the guarantee is wired end-to-end, not just present at one layer

A lock, version column, or guarded RPC that exists in the database or a shared helper is not evidence the guarantee holds. Trace whether its *result* — success, conflict, or error — is actually checked and propagated by every caller, up through the HTTP response and, where relevant, into the frontend. A protection whose failure signal is silently discarded is functionally identical to no protection, and worse in practice because it also reports false success to the caller.

### 4. Reproduce the failure deterministically, not by racing real requests

Firing concurrent requests (`Promise.all`, parallel curl) to "prove" or "disprove" a race is unreliable — network and server latency can accidentally serialize requests that would collide under real production load, producing a false negative that looks like a clean PASS. Force the exact collision instead:

1. Capture two independent reads of the same state (two snapshots at the same version/timestamp).
2. Apply the first snapshot's write through the real code path and let it succeed.
3. Apply the second, now provably stale, snapshot's write through the same real code path.
4. Assert the guard rejects it — check the actual stored state afterward, not just the HTTP status code returned.

This proves the guard's behavior on demand instead of hoping to catch it mid-flight.

### 5. Verify against live state, not code comments or architecture docs

Code and comments describing one path as "primary" and another as "fallback" can be wrong in the deployed environment. Before scoring severity, confirm which path is actually exercised in production/staging data — a schema check, a feature-flag read, or a row count is usually enough. A "rare fallback" that turns out to be the only path actually live changes a WARN into a BLOCK.

### 6. Map the blast radius, not just the scenario that motivated the check

For any write to a shared or aggregate resource — a JSON/JSONB blob, a cache entry, a computed or derived value, a materialized view — identify every other writer to that same resource, not just the two callers involved in the obvious collision. A handler that reads-then-overwrites an entire shared object from a stale snapshot can destroy an unrelated concurrent write from a completely different feature, not only a same-feature collision. State the blast radius explicitly for every pair found: "X can be silently lost when Y writes concurrently," not just the pair that prompted the investigation.

### 7. Sibling-code audit after any single finding

The moment one instance of a bug pattern is confirmed, treat it as a hypothesis about the rest of the codebase, not a fact about one file:

```bash
# after confirming a pattern bug in one file, search for structurally identical code elsewhere
grep -rln "<the exact buggy pattern — a function name, call shape, or comment marker>" src/
```

Report every additional location found, even ones outside the original diff, ticket, or PR scope. A partial fix that leaves sibling instances unpatched is an open BLOCKER, not something to defer silently to a future pass.

Decision rules:

- A claimed guarantee not actually wired end-to-end = BLOCK, regardless of how the rest of the tiers scored.
- A guard whose failure result is silently discarded by a caller = BLOCK — this is worse than no guard, since it also produces false success.
- Sibling instances of a confirmed bug pattern outside the current diff = must be reported as findings, not silently deferred.
- A "fallback" path confirmed to be the only path live in production = escalate its risk to match actual usage, not documented intent.

## T11 - Production Readiness Review

Question: If this breaks in production, will the team know quickly, and can they recover without an emergency code fix?

Required for pre-deploy/production-readiness sweeps, and for any change to a payment, auth, or otherwise critical-path system landing on a live target with real users.

1. **Rollback path.** Confirm this can be reverted fast — a previous image/tag redeploy, a documented migration-down path, or a flag to switch it off — without needing a new emergency code change. For database migrations, this ties into T9's rollback check; state explicitly if none exists rather than assuming one does.
2. **Staged rollout.** Is this change gated behind a feature flag, a percentage rollout, or a canary group, or does it go to 100% of users the moment it deploys? For payment, auth, or data-model changes, absence of staged rollout is at least a WARN — full-blast exposure of an unproven change to every user is itself a risk to name.
3. **Observability.** A failure that nobody can see is a failure that stays broken. Check that the new/changed code paths actually surface errors — not swallowed into a discarded `catch` (this is the same failure shape as T10's "guard result silently discarded," applied to error visibility instead of a conflict signal) — and that an error-tracking tool (Sentry or equivalent), if the project has one, actually covers the new paths.
   ```bash
   grep -rn "catch" <changed-files> --include="*.ts" --include="*.tsx" -A2 | grep -B2 "^\s*}" | grep -v "console\.\|throw\|return" || true
   ```
4. **Dependency-failure behavior.** For each new or changed call to an external dependency (third-party API, DB, cache, queue, another internal service), ask what happens when it is slow or unavailable: is there a bounded timeout, a bounded retry/backoff (not infinite), and a defined degraded behavior — or does it hang or crash the request? If this has never been tested, say so explicitly as an untested failure mode rather than assuming it is fine.
5. **Runbook.** For a genuinely new production-critical mechanism (a payment webhook relay, a cron job, a background worker), confirm there is at least a brief written note of what to do if it stops working. Absence is not automatically a blocker for a small team, but it must be named as a known gap, not silently skipped.

Decision rules:

- Payment, auth, or data-migration change with no rollback path = BLOCK.
- High-risk change with neither staged rollout nor a fast rollback path = WARN minimum; BLOCK if this area has a prior incident history.
- A new critical failure mode (e.g. a cron job that can silently stop running) with zero observability = WARN minimum.

## T12 - Load and Concurrency-at-Scale Testing

Question: Does this hold up under real concurrent load, not just the one or two colliding requests T10 forces?

Required for public-facing mutation endpoints, payment/checkout flows, anything expecting traffic spikes (launch day, a marketing push, a cron job processing a large batch), and any change to a lock, queue, or rate-limit mechanism.

1. Find a load tool the environment can actually run — prefer whatever is already a project devDependency, otherwise a single-binary tool needs no project changes to install.
   ```bash
   which k6 autocannon hey 2>/dev/null || echo "no load tool found - install autocannon (npm) or k6 (binary) before this tier"
   ```
2. Agree on a realistic concurrency target before running anything — ask the user, or infer from stated expected launch traffic or campaign size, rather than picking an arbitrary number. State the chosen target and its source in the report.
3. Run a short, bounded burst against the changed endpoint(s), against a target that can safely absorb it — never production without explicit authorization; prefer staging or an isolated slice created for this purpose.
   ```bash
   # illustrative — set concurrency (-c), duration (-d), method/body to match the agreed target and endpoint
   npx autocannon -c 50 -d 20 -m POST -H "Content-Type: application/json" -b '{"...":"..."}' "$QA_BASE/api/..."
   ```
4. Watch error rate under load, not just latency — and specifically re-check whether a concurrency guard proven correct at 2 requests in T10 still holds at realistic scale (does the same deterministic-conflict property survive 50 simultaneous writers, or does it start silently dropping writes instead of rejecting them?). Also watch for resource exhaustion (DB connection pool, memory, file descriptors).
5. Never point a load test at a third-party paid API (SMS/WhatsApp/payment gateway) — use sandbox/test-mode credentials for that specific dependency during the run, or mock it.

Decision rules:

- Error rate climbs sharply, rather than degrading gracefully, before the agreed target concurrency = BLOCK for that endpoint.
- A concurrency guard verified only at T10's 2-request scale, not at realistic load = state this explicitly as a residual, unverified risk — do not report it as a full PASS.
- Running a load test against production without explicit authorization = do not do it; ask first.

## T13 - Compliance, Privacy, and Standards Mapping

Question: Does this handle personal data correctly, and can the findings be defended against a named external standard if audited?

1. **PII inventory.** For every new or changed field, table, log line, or third-party call in scope, identify whether it stores or transmits personal data (name, email, phone, address, payment detail, government ID, biometric, precise location).
   ```bash
   grep -rniE "email|phone|no_?hp|ktp|nik|address|alamat|payment|card_number|date_of_birth" <changed-files> || true
   ```
2. **Retention and deletion.** Does the project have an existing lifecycle/archive job or a user-initiated delete/export flow? If the change adds a new place personal data is stored, confirm that existing path actually covers it — a new PII field no cleanup or deletion job knows about is a gap, not a detail.
3. **Consent and purpose.** For any new data collection visible to the end user (a new form field, a new analytics/tracking call), is there a clear stated purpose or existing privacy policy coverage? Flag silent new collection as WARN.
4. **Map findings to a named standard**, not only free text:
   - Security: cite the relevant CWE ID, and the OWASP ASVS requirement level (L1/L2/L3) where applicable.
   - Accessibility: cite the specific WCAG success criterion and level (e.g. "WCAG 2.2 SC 1.4.3 Contrast (Minimum), Level AA") instead of "accessibility issue."
5. **Cross-border data transfer.** If hosting or third-party providers (email/SMS/analytics) sit in a different jurisdiction than the user base, note it as a disclosed fact — a blocker only if the project has a stated compliance requirement (GDPR, a local data-protection law) that restricts it.

Decision rules:

- Newly stored PII with no retention/deletion path = WARN minimum; BLOCK if the project has a stated compliance requirement it must meet.
- A security or accessibility finding reported without a citable standard reference, when the audience needs audit traceability, is incomplete — add the mapping before finalizing the report.

## T14 - Exploratory Testing Session

Question: What would a skeptical, curious human notice that no script or checklist above was written to catch?

A light, deliberately unscripted pass layered on top of the tiers above — not a replacement for them. Run it whenever time allows, especially on anything new and user-facing.

1. Write a one-line charter before starting — the area and the specific risk being hunted (e.g. "explore the planner UI for any state that looks stale or contradicts what was just saved"). A charter with no stated risk turns into aimless clicking.
2. Timebox it — 10 to 30 minutes is typical.
3. Deliberately deviate from the happy path: double-click submit buttons, use the browser back button mid-flow, resize the window while a modal is open, paste unexpected content into a field, switch tabs and return, go offline mid-request. Scripted tests only ever check what someone thought to write down in advance — this is the pass that catches what nobody thought to script.
4. Log what was tried and what was noticed, including things that seemed fine — a short session log, not a formal test case.

Decision rules:

- Anything found here that reproduces is a finding like any other tier's — report it with reproduction steps.
- Skipping this tier under real time pressure is acceptable; mark it SKIP with the reason rather than silently omitting it.

## AI Review Tier

Use targeted review after automated evidence is collected.

Dispatch or request review based on changed files:

- `typescript-reviewer` for TypeScript, async behavior, types, and runtime edge cases
- `react-reviewer` for UI, state, rendering, and component behavior
- `a11y-architect` for accessibility-sensitive UI
- `database-reviewer` for Prisma, SQL, schema, migration, and query performance
- `security-reviewer` for auth, API, input, upload, webhook, RBAC, and tenant isolation
- `e2e-runner` for missing browser coverage
- `code-reviewer` for final broad pass

Give reviewers this context:

```text
repo path
branch
commit SHA
diff range
changed files
target URL
tiers already run
command outputs
browser results
known concerns
```

Fix BLOCK and HIGH findings before GO.

## Stop Conditions

Stop immediately when:

- a real secret is found
- build fails and user did not request investigation mode
- type/lint failure affects changed code and blocks runtime correctness
- critical or high exploitable security issue appears
- authorization allows cross-tenant, cross-branch, or cross-owner access
- deploy target does not update for deployed QA
- E2E failure proves a real product bug in a critical flow
- database migration risks data loss without approval
- a claimed correctness/security guarantee (concurrency, atomicity, RBAC, idempotency, dedup) is confirmed not to hold end-to-end
- a guard's conflict/error result is confirmed to be silently discarded by a caller, producing false success
- a payment, auth, or data-migration change has no rollback path
- error rate collapses well before the agreed load target on a public or payment-adjacent endpoint
- newly stored personal data has no retention/deletion coverage and the project has a stated compliance requirement

When stopping, report the evidence, impact, and next action.

## Final Report Format

Use this exact shape.

```text
QA REPORT - <project> - <timestamp>
Repo/branch: <repo> <branch> <ahead/behind>
Commit tested: <sha>
Ticket/requirement: <id or "none provided">
Target: <target-url or local> | Deploy source: <branch>
Scope: <changed files + surfaces>
Tiers selected: <T0,T1,...>
Tiers run: <T0,T1,...>

T0 Context: PASS/WARN/BLOCK/SKIP - <evidence>
T1 Fast: PASS/WARN/BLOCK/SKIP - types/lint/secrets/tests
T2 Build/Deps: PASS/WARN/BLOCK/SKIP - build/audit/trivy/config
T3 Security: PASS/WARN/BLOCK/SKIP - semgrep/gitleaks/manual/security review
T4 API: PASS/WARN/BLOCK/SKIP - adversarial/idempotency/race/contracts
T5 E2E: PASS/WARN/BLOCK/SKIP - N/M pass, flows, artifacts, dogfood walkthrough
T6 RBAC: PASS/WARN/BLOCK/SKIP - role matrix and isolation
T7 Deploy: PASS/WARN/BLOCK/SKIP - live proof and smoke
T8 A11y/Visual/Perf: PASS/WARN/BLOCK/SKIP - keyboard, axe, screenshots, perf
T9 Regression/Coverage/Contracts: PASS/WARN/BLOCK/SKIP - impact, coverage, DB, schema
T10 Critical Claim/Blast-Radius: PASS/WARN/BLOCK/SKIP - invariant stated, sibling paths checked, end-to-end wiring, deterministic reproduction, blast radius
T11 Production Readiness: PASS/WARN/BLOCK/SKIP - rollback, rollout, observability, dependency-failure behavior, runbook
T12 Load/Scale: PASS/WARN/BLOCK/SKIP - tool, target concurrency, error rate, guard behavior at scale
T13 Compliance/Privacy/Standards: PASS/WARN/BLOCK/SKIP - PII inventory, retention, consent, standard citations
T14 Exploratory: PASS/WARN/BLOCK/SKIP - charter, session notes, findings
AI Review: APPROVE/WARN/BLOCK/SKIP - <evidence>

BLOCKERS:
- ... or none

WARNINGS:
- ... or none

SKIPPED:
- <gate> - <reason>

EVIDENCE:
- command/browser/scanner highlights

GO/NO-GO: GO | NO-GO
Confidence: HIGH | MEDIUM | LOW - <reason>
Next actions:
1. ...
```

## Common Failure Patterns

Watch for these mistakes:

- testing parent repo while the feature lives in a nested repo
- testing local code after a deploy already happened
- trusting HTTP 200 without checking body and side effect
- testing happy path only for auth and permission work
- skipping Gitleaks, Semgrep, or Trivy because build passed
- ignoring branch mismatch between local and deploy source
- missing cross-tenant or cross-branch object ID tests
- creating new E2E tests before discovering existing harness
- claiming production readiness without live proof
- saying “all safe” instead of “tools run found no issues”
- installing E2E dependencies and not reporting the resulting `package-lock.json` diff
- treating a failed Vercel Check or blocked GitHub Environment protection rule as "still deploying" instead of BLOCK
- treating a clean T0-T9 pass (types, lint, build, generic scanners) as proof that a claimed guarantee — concurrency control, RBAC, idempotency, dedup — actually holds
- testing a race condition with real concurrent HTTP requests and treating a failure to reproduce it as proof of safety, instead of forcing the collision deterministically
- checking only that an underlying guard (DB constraint, version column, locking RPC) exists, without checking that every caller actually reads and propagates its result
- trusting code comments or architecture docs about which persistence path is "primary" vs "fallback" without confirming which one is actually live in production
- fixing one instance of a bug pattern and not searching the codebase for structurally identical sibling instances
- relying only on scripted E2E/API assertions for a brand-new feature and skipping a real hands-on walkthrough as the actual persona
- treating a 200/201 or a "success" response body as proof data persisted, instead of independently reading it back
- leaving disposable QA identities or test data behind in a shared, staging, or production environment after testing
- skipping load testing because functional tests passed, on an endpoint that will actually see concurrent or spiky traffic
- shipping a payment, auth, or data-migration change with no rollback path and calling it production-ready
- storing a new personal-data field without checking it is covered by an existing retention/deletion path
- reporting a security or accessibility finding as free text when the audience needs a citable standard reference (CWE, OWASP ASVS level, WCAG criterion) for audit

## Minimal Command Pack

Use this when the user wants fast but disciplined QA.

```bash
pwd
git status --short --branch
git remote -v
git log --oneline -10
git diff --stat HEAD~1
npx tsc --noEmit
npm run lint
gitleaks detect --source . --no-banner --redact --exit-code 1
npm run build
```

## Full Command Pack

Use this for pre-deploy or production readiness.

```bash
pwd
git status --short --branch
git remote -v
git log --oneline -10
git diff --name-only HEAD~1
git diff --stat HEAD~1
npx tsc --noEmit
npm run lint
gitleaks detect --source . --no-banner --redact --exit-code 1
npm run build
npm audit --audit-level=high
trivy fs . --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1
semgrep --config auto src/
gitleaks detect --source . --log-opts="HEAD~20..HEAD" --no-banner --redact --exit-code 1
npm test -- --coverage
```
