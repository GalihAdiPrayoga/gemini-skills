# AGENTS.md — {{PROJECT_NAME}}

Execution checklist untuk AI agents. **`CLAUDE.md` = aturan & referensi; file ini = checklist eksekusi; `SECURITY.md` = kebijakan security.**

> Repo ini punya `SessionStart` hook di `.claude/settings.json` yang otomatis cek marker protokol tiap sesi baru dibuka — supaya standardisasi ini tidak bergantung pada siapa pun mengingat untuk membacanya. Kalau Anda melihat pesan "belum punya protokol AI-agent", itu artinya marker di `CLAUDE.md` hilang atau berubah — jangan hapus heading `## ⚙️ Alur Kerja Wajib` dari `CLAUDE.md`.

---

## 🚨 Mandatory Pre-Task Checklist — NO EXCEPTIONS

### Step 1: Load Project Context
```bash
git status --short --branch
git log --oneline -5
```
- [ ] Baca `CLAUDE.md` penuh — catat stack, arsitektur, aturan, dan forbidden actions
- [ ] Baca `AGENTS.md` ini — cek coordination note, who owns what, shared-file risk
- [ ] Jika task menyentuh schema/migration: baca migrasi terbaru
- [ ] Jika task menyentuh payment/checkout: baca spec di `docs/superpowers/specs/`
- [ ] Jika task menyentuh auth: review auth sections di `CLAUDE.md`
- [ ] Jika task menyentuh webhook: review idempotency rules

### Step 2: Declare Intent
Sebelum coding, nyatakan secara eksplisit:
1. **Files yang akan disentuh** — list lengkap
2. **Shared-file risk** — apakah ada file yang sedang dikerjakan agent lain?
3. **Constraints dari `CLAUDE.md`** — rule apa yang berlaku untuk task ini?
4. **Security concerns** — apakah task ini menyentuh auth, input, secrets, DB writes, upload?

### Step 3: Security Gate

Untuk setiap task yang menyentuh area di bawah, jawab SEMUA pertanyaan sebelum coding:

| Area | Mandatory Check |
|---|---|
| **Auth / RBAC** | Endpoint dilindungi? Role check server-side? Tidak percaya client? |
| **Input Validation** | Semua input divalidasi Zod sebelum ke DB/service? |
| **Secret Handling** | Tidak ada env var bocor ke client via `NEXT_PUBLIC_`? |
| **DB Access** | Semua Prisma/ORM calls lewat `server/repositories/` saja? |
| **Webhook** | Handler idempoten? Token/signature diverifikasi sebelum proses? |
| **File Upload** | File type + size divalidasi server-side? Path traversal dicegah? |
| **Error Responses** | Tidak ada stack trace/internal path/PII di client-facing error? |
| **Mutation Safety** | Tidak ada DB mutation dari GET handlers? |
| **XSS Prevention** | Tidak ada `dangerouslySetInnerHTML` tanpa sanitasi? |
| **CSRF** | State-changing action dilindungi (bukan GET)? |
| **Rate Limiting** | Public/abuse-prone endpoints dibatasi? |
| **Data Ownership** | Caller diverifikasi MEMILIKI record (bukan sekadar authenticated)? |

> ⚠️ **HARD STOP**: Jika ada security check yang tidak yakin, selesaikan SEBELUM menulis kode. Jangan lanjut dengan asumsi "fix it later" untuk security.

### Step 4: Post-Implementation Validation
```bash
# Selalu jalankan sebelum klaim task complete:
{{VALIDATE_CMDS}}
```
Jika command tidak bisa dijalankan, sampaikan ke user apa yang perlu divalidasi.

### Step 5: Docs-as-Code — Definition of Done
Task belum "selesai" sampai docs mencerminkan realita. Update dalam **commit yang sama** dengan code change.

| Trigger | File yang di-update |
|---|---|
| Sprint selesai | `CLAUDE.md` § Status Sprint |
| Env variable baru | `CLAUDE.md` § Environment Variables |
| Keputusan arsitektur baru | `CLAUDE.md` § Keputusan Arsitektur |
| Fitur baru deploy | `CLAUDE.md` § Fitur yang Sudah Dibangun |
| Migration schema | Kedua file + nama migration + tanggal |
| Rule baru dilarang | `CLAUDE.md` § Yang TIDAK Boleh Dilakukan |

### Step 6: Commit (Conventional Commits)
Format: `<type>(scope): summary` — `feat | fix | docs | chore | refactor | test | perf`.
Satu commit = satu perubahan logis, scope sempit. Jangan pernah commit secrets/tokens/credentials.

### Security Tooling (jalankan sebelum commit/PR relevan)
```bash
semgrep --config auto <path>                 # auth/payment/webhook/upload/input/permission
gitleaks protect --staged --no-banner        # sebelum commit config/env/docs/credentials
trivy fs --scanners vuln,secret,misconfig .  # Dockerfile/image/dependencies
```

---

## Pembagian Peran Agent

### Claude Code (Utama)
- Fitur kompleks — multi-file, arsitektur baru
- Perubahan schema / migration Prisma
- Auth, payment, webhook, server actions
- Debug yang butuh konteks mendalam
- QA execution (`/qa-master`)

### Codex (Paralel — scope terbatas)
- Task independen dari Claude (cari task tanpa dependency di plan)
- UI components yang tidak menyentuh server
- Docs update, refactor terisolasi
- Test writing

### File yang TIDAK BOLEH dikerjakan paralel
```
prisma/schema.prisma
server/repositories/*.ts
middleware.ts
app/api/payment/** | app/api/order/**
```
→ Jika overlap: **koordinasi dulu**, jangan overwrite.

---

## Workflow Skills — Kapan Pakai Apa

Gunakan skills ini untuk memaksimalkan kualitas dan konsistensi kerja:

| Situasi | Skill yang dipakai |
|---|---|
| Ada ide fitur baru / masalah yang belum jelas | `/brainstorm` — ideation terstruktur |
| Butuh dokumen spec formal sebelum coding | `/spec-writer` — buat design doc |
| Butuh implementation plan yang executable | `/plan-writer` + `superpowers:writing-plans-self-improvement-assistant` — buat task breakdown + planning memory |
| Eksekusi plan yang sudah di-approve | `superpowers:subagent-driven-development` + `superpowers:sdd-self-improvement-assistant` — dispatch sub-agent per task + recurring-issue learning |
| QA sebelum commit / deploy / ada bug report | `/qa-master` — evidence-based release gate T0-T9 |
| Setup project baru / onboarding repo | `/init-project` — scaffold protokol |

> **Pipeline ideal untuk fitur signifikan:** `/brainstorm` → `/spec-writer` → `/plan-writer` + `superpowers:writing-plans-self-improvement-assistant` → [user approve] → `superpowers:subagent-driven-development` + `superpowers:sdd-self-improvement-assistant` → `/qa-master`

### Prinsip Kombinasi Skill — "Self-Improvement-Assistant" Pairing

Beberapa skill workflow punya pasangan `*-self-improvement-assistant` dari paket `superpowers`. Pasangan ini **tidak menggantikan** skill utama — dia berjalan **bersamaan**, menambahkan project memory berbasis bukti (evidence-based), deteksi recurring issue, dan pembelajaran plan-quality tanpa melemahkan disiplin skill utama.

| Skill utama | Pasangan self-improvement-assistant | Kapan dipakai bersamaan |
|---|---|---|
| `/plan-writer` | `superpowers:writing-plans-self-improvement-assistant` | Setiap kali menyusun implementation plan dari spec |
| `superpowers:subagent-driven-development` | `superpowers:sdd-self-improvement-assistant` | Setiap kali mengeksekusi plan yang sudah di-approve via sub-agent |

Belum ada pasangan self-improvement-assistant untuk `/brainstorm`, `/spec-writer`, atau `/qa-master` di skill library ini — jalankan skill-skill itu berdiri sendiri sampai pasangannya tersedia. Jangan memaksakan skill yang tidak relevan hanya demi "menggunakan kombo".

---

## ECC Specialized Agents — Kapan Dispatch

ECC agents sudah terinstall di `~/.claude/agents/`. Dispatch ke agent terspesialisasi alih-alih menangani semuanya di main session.

### Agent Dispatch Table

| Task Type | Agent |
|---|---|
| Perencanaan arsitektur fitur / multi-file | `code-architect` |
| System design, scalability decisions | `architect` |
| **TypeScript / JavaScript code review** | `typescript-reviewer` ← pakai ini setelah ubah .ts/.tsx |
| **React / JSX component review** | `react-reviewer` ← pakai ini setelah ubah komponen |
| **PostgreSQL schema, query, migration review** | `database-reviewer` ← pakai ini setelah ubah schema/query |
| **Security (auth / payment / webhook / input)** | `security-reviewer` ← pakai ini untuk surface sensitif |
| TDD enforcement — tulis tests dulu | `tdd-guide` |
| E2E browser flow testing (Playwright) | `e2e-runner` |
| Build / TypeScript compilation errors | `build-error-resolver` |
| React build failures | `react-build-resolver` |
| Performance bottlenecks, bundle size | `performance-optimizer` |
| Dead code, unused imports, cleanup | `refactor-cleaner` |
| General code review setelah task selesai | `code-reviewer` |

### ECC Skill Reference — Pattern Libraries

Sebelum menggunakan skill ECC, **baca SKILL.md-nya terlebih dahulu** dengan `view_file` pada path di bawah:

| Kapan | Path SKILL.md |
|---|---|
| Menulis Prisma queries / schema / migration | `~/.claude/skills/ecc/prisma-patterns/SKILL.md` |
| React component patterns + hooks | `~/.claude/skills/ecc/react-patterns/SKILL.md` |
| TDD workflow step-by-step | `~/.claude/skills/ecc/tdd-workflow/SKILL.md` |
| Security review checklist | `~/.claude/skills/ecc/security-review/SKILL.md` |
| Security scanning | `~/.claude/skills/ecc/security-scan/SKILL.md` |
| Database migration safety | `~/.claude/skills/ecc/database-migrations/SKILL.md` |
| Post-implementation verification | `~/.claude/skills/ecc/verification-loop/SKILL.md` |
| Menulis/memperbarui E2E test (Page Object Model, config, flaky-test strategy) | `~/.claude/skills/ecc/e2e-testing/SKILL.md` |
| E2E untuk native desktop app (WPF/WinForms/Win32/Qt) — hanya kalau stack-nya desktop, bukan web | `~/.claude/skills/ecc/windows-desktop-e2e/SKILL.md` |
| Cari tools/library/pattern existing sebelum tulis kode baru (Fase 1) | `~/.claude/skills/ecc/search-first/SKILL.md` |
| Desain REST API — resource naming, status code, pagination, versioning, rate limit | `~/.claude/skills/ecc/api-design/SKILL.md` |
| Error handling lintas layer — typed errors, error boundary, retry, circuit breaker | `~/.claude/skills/ecc/error-handling/SKILL.md` |
| CI/CD pipeline, containerization, health check, rollback strategy | `~/.claude/skills/ecc/deployment-patterns/SKILL.md` |
| Audit kesiapan produksi mendalam — pre-launch, post-merge, "apa yang bisa rusak di prod?" | `~/.claude/skills/ecc/production-audit/SKILL.md` |
| PR/issue triage, release management, cek status CI via GitHub | `~/.claude/skills/ecc/github-ops/SKILL.md` |

> **Cara pakai:** Baca SKILL.md di path tersebut, lalu ikuti prosedurnya. Jangan berasumsi isi skill dari namanya saja.
> **Kapan wajib dibaca `e2e-testing`:** setiap kali Fase 3 (Eksekusi) menyentuh flow UI/user-facing yang baru atau berubah — tulis/perbarui E2E test **saat itu juga**, bukan menunggu ditemukan kosong saat `/qa-master` T5 (Behavioral E2E) berjalan. T5 memvalidasi harness yang sudah ada; skill ini yang mengajarkan cara membangunnya dengan benar.

### Onboarding & Ecosystem Tuning (sekali di awal, ulang setelah refactor besar)

| Kapan | Skill ECC |
|---|---|
| Project baru discaffold, ingin tahu skill/agent/MCP paling relevan untuk stack ini secara spesifik (bukan daftar generik di atas) | `~/.claude/skills/ecc/workspace-surface-audit/SKILL.md` |
| Struktur folder sudah stabil, butuh peta arsitektur untuk `docs/CODEMAPS/` | `~/.claude/skills/ecc/update-codemaps/SKILL.md` |

Keduanya opsional dan tidak dijalankan otomatis oleh `/init-project` — jalankan manual sekali project sudah punya kode nyata untuk diaudit/dipetakan.

### Aturan Dispatch
- Dispatch agent terspesialisasi **sebelum** klaim task selesai untuk area sensitif (auth/payment/schema/webhook).
- Setelah setiap coding task, dispatch `code-reviewer` atau reviewer stack-spesifik.
- Agents berjalan terisolasi — berikan file list + task context yang tepat, bukan session history.
- Untuk skill ECC: selalu `view_file` SKILL.md-nya dulu sebelum mengeksekusi workflow.

---

## DevSecOps — Role & Reporting

**Role:** senior full-stack engineer + DevSecOps reviewer. Optimasi untuk perubahan yang **minimal, reviewable, testable**; prefer open-source / low-ops solutions.

**Dependency Policy:** Jangan tambah package kecuali perlu. Jika menambah, nyatakan: **kenapa perlu · alternatif yang dipertimbangkan · risiko security/maintenance · sinyal popularitas/maintenance** (downloads, last release, maintainers).

**Format Respons Akhir (setiap task):**
Akhiri dengan: **Summary · Files changed · Validation commands run · Security/scalability risks found · Risks not fully verified · Recommended next steps.** Jangan pernah klaim project 100% secure.

---

## Current Coordination Note

> Update bagian ini setiap ada perubahan signifikan: sprint owner baru, branch merge, env/tunnel/DB berubah, migration penting, aturan deploy baru, integrasi external service, atau boundary yang ditetapkan user.
>
> Format: singkat, bertanggal, operasional. Replace catatan lama yang sudah tidak relevan.

- **Updated:** {{CURRENT_DATE}} — project initialized with agent protocol scaffold.
