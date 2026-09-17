# {{PROJECT_NAME}}

> Ringkasan 1 kalimat tentang project ini. Stack: {{STACK}}. Status: Development.

**Spec lengkap:** `docs/superpowers/specs/`
**Sprint plans:** `docs/superpowers/plans/`
**Codemaps:** `docs/CODEMAPS/` — peta arsitektur untuk orientasi cepat agent baru

---

## ⚙️ Alur Kerja Wajib (Development Discipline)

Berlaku untuk SETIAP tugas — patuhi sebelum, selama, dan sesudah eksekusi.

### 1. Pipeline Wajib — 4 Fase Tanpa Shortcut

```
FASE 1        FASE 2                                  FASE 3                                        FASE 4
IDEASI    →  SPEC + PLANNING                     →   EKSEKUSI                                  →   QA & DEPLOY
/brainstorm  /spec-writer                             subagent-driven-development +                 /qa-master
             /plan-writer + writing-plans-             sdd-self-improvement-assistant
             self-improvement-assistant                [user approve plan dulu]
```

- **Fase 1 (Ideasi):** Fitur baru / ambigu → `/brainstorm` wajib. Sebelum atau bersamaan brainstorm, cek `~/.claude/skills/ecc/search-first/SKILL.md` — jangan bangun ulang tools/library/pattern yang sudah ada. Output = keputusan pendekatan yang disepakati.
- **Fase 2 (Spec + Planning):**
  - `/spec-writer` → bangun spesifikasi arsitektur yang benar untuk fitur ini, simpan di `docs/superpowers/specs/` (lihat README di folder itu untuk format).
  - `/plan-writer` **bersamaan dengan** `superpowers:writing-plans-self-improvement-assistant` → susun implementation plan mendetail dari spec tersebut, simpan di `docs/superpowers/plans/`. Skill kedua menambahkan planning memory berbasis bukti dari plan-plan sebelumnya di project ini — jalankan keduanya, jangan cuma salah satu.
  - User **harus approve plan** sebelum coding dimulai.
- **Fase 3 (Eksekusi):** `superpowers:subagent-driven-development` **bersamaan dengan** `superpowers:sdd-self-improvement-assistant` — setiap task plan dikerjakan oleh sub-agent terisolasi, dites, dan divalidasi, sambil recurring-issue learning dikumpulkan untuk mempertajam dispatch task berikutnya. Deklarasikan file yang disentuh. Tidak ada dua agent di file yang sama. Commit scope sempit per task. **Kalau task menyentuh flow UI/user-facing baru atau berubah:** tulis/perbarui E2E test di fase ini juga, ikuti `~/.claude/skills/ecc/e2e-testing/SKILL.md` (Page Object Model, config, flaky-test strategy) — jangan tunda sampai Fase 4.
- **Fase 4 (QA & Deploy):** `/qa-master` sebelum setiap deploy — evidence-based release gate T0-T9. T5-nya memvalidasi harness E2E yang **sudah dibangun** di Fase 3, bukan tempat pertama kali menulisnya. Untuk pre-launch besar atau audit kesiapan produksi yang lebih dalam dari `/qa-master`, tambahkan `~/.claude/skills/ecc/production-audit/SKILL.md`. Tidak ada deploy tanpa QA Report = GO.

> **Prinsip kombinasi skill:** kalau sebuah skill workflow punya pasangan `*-self-improvement-assistant`, jalankan keduanya bersamaan — skill utama mengerjakan tugasnya, pasangannya menambahkan project memory berbasis bukti tanpa melemahkan disiplin skill utama. Detail lengkap tabel kombinasi ada di `AGENTS.md` § Workflow Skills.

> **Pattern library ECC per fase:** Fase 1 → `search-first`. Fase 3 → `e2e-testing` (kalau UI berubah), `api-design` (kalau bikin/ubah endpoint), `error-handling` (lintas layer). Fase 4 → `deployment-patterns` (CI/CD, rollback), `production-audit` (audit mendalam), `github-ops` (PR/release/issue). Path dan penjelasan lengkap ada di `AGENTS.md` § ECC Skill Reference — jangan berasumsi isi skill dari nama baris ini saja.

### 2. Konteks dulu — baca dokumentasi sebelum eksekusi
- Baca `CLAUDE.md` + `AGENTS.md` + spec/plan yang relevan sebelum menyentuh kode.
- Verifikasi fakta repo: `git status --short --branch`, `git log --oneline -10`.
- Jangan improvisasi di luar plan — jika butuh perubahan scope, update plan dulu.

### 2. Dokumentasi selalu sinkron (docs-as-code) — WAJIB
Setiap perubahan kode/arsitektur/schema/env/deploy **harus disertai update dokumentasi dalam commit yang sama**. Tugas belum "selesai" sampai dokumen mencerminkan kondisi nyata. Singkat, **bertanggal**, operasional; ganti catatan usang.

| Trigger | File yang di-update |
|---|---|
| Sprint selesai | `CLAUDE.md` § Status Sprint |
| Env variable baru | `CLAUDE.md` § Environment Variables |
| Keputusan arsitektur | `CLAUDE.md` § Keputusan Arsitektur |
| Fitur baru deploy | `CLAUDE.md` § Fitur yang Sudah Dibangun |
| Migration schema | Kedua file + nama migration + tanggal |
| Rule baru dilarang | `CLAUDE.md` § Yang TIDAK Boleh Dilakukan |

### 3. Security-first — setiap perubahan berpotensi berisiko
Permukaan sensitif: **{{SENSITIVE_SURFACES}}**.
- Spec dulu untuk permukaan sensitif — jangan hotfix buta.
- **Selalu** validasi & otorisasi **server-side** — jangan percaya nilai dari client (harga, role, stock, ID).
- Jalankan tooling sebelum commit relevan:
  ```bash
  semgrep --config auto <path>                 # auth/payment/webhook/upload/input
  gitleaks protect --staged --no-banner        # config/env/docs/credentials
  trivy fs --scanners vuln,secret,misconfig .  # Dockerfile/image/dependency
  ```
- **Jangan pernah** commit/hardcode secret, token, credentials — termasuk di docs & `.env.example`.

### 4. Bukti sebelum klaim
Jangan klaim build/lint/test/migration/QA/deploy berhasil tanpa menjalankan perintahnya dan membaca outputnya. Pisahkan `terkonfirmasi` vs `asumsi` vs `langkah berikutnya`.

### 5. Konvensi commit (Conventional Commits)
Format: `<tipe>(scope): ringkasan`. Tipe: `feat | fix | docs | chore | refactor | test | perf`.
Satu commit = satu perubahan logis, scope sempit.

### 6. 5 Aturan Tim — Non-Negotiable

| # | Aturan | Konsekuensi jika dilanggar |
|---|---|---|
| 1 | Tidak ada coding tanpa plan approved di `docs/superpowers/plans/` | Revert dan buat plan dulu |
| 2 | Tidak ada deploy tanpa `/qa-master` GO (bukan NO-GO) | Deploy ditolak |
| 3 | Tidak ada dua agent di file yang sama secara bersamaan | Koordinasi dulu via git status |
| 4 | Docs selalu sinkron dalam commit yang sama dengan code | Commit tidak diterima tanpa doc update |
| 5 | Secret terdeteksi = HARD STOP, rotate semua credential dulu | Jangan commit apapun sebelum selesai |

> **Pembagian:** `CLAUDE.md` = aturan & referensi; `AGENTS.md` = checklist eksekusi.

### Catatan Agent (DevSecOps)
- Ikuti `AGENTS.md` + `SECURITY.md` + `docs/AI_AGENT_PROTOCOL.md`.
- **Jangan** baca/tampilkan/commit file secret (`.env*`, `*.pem`, `*.key`, `id_rsa`, `id_ed25519`).
- Gunakan MCP/tool bila tersedia: **Context7** (dok library terbaru), **Playwright** (QA UI), **GitHub** (PR/CI), **Semgrep/Gitleaks/Trivy** (security scan).
- Jalankan `{{VALIDATE_CMDS}}` sebelum klaim selesai. Laporan akhir ringkas & jujur — jangan klaim 100% aman.

---

## Stack

| Area | Tech |
|---|---|
| Framework | {{STACK}} |
| Package Manager | {{PKG_MANAGER}} |
| Database / ORM | > isi sesuai project |
| Auth | > isi sesuai project |
| Storage | > isi sesuai project |
| Deployment | > isi sesuai project |

---

## Struktur Folder — Aturan Wajib

```
src/
├── app/           # Routes (Next.js App Router)
├── components/    # UI only — TIDAK boleh query DB langsung
├── features/      # Domain logic per fitur
├── server/
│   ├── actions/       # Server Actions (entry dari UI)
│   ├── services/      # Business logic
│   └── repositories/  # SATU-SATUNYA tempat ORM/DB dipanggil
└── lib/
    ├── validators/    # Zod schemas
    └── utils/
```

> **Aturan wajib:** Jangan call DB/ORM dari luar `server/repositories/`. Selalu lewat `server/repositories/`.

---

## Route Groups

| Group | URL Pattern | Auth |
|---|---|---|
| > isi sesuai project | | |

---

## Status Sprint

| Sprint | Topik | Status |
|---|---|---|
| Sprint 00 | Setup & Infrastructure | > isi |

---

## Fitur yang Sudah Dibangun

> Daftar fitur yang sudah live, format: `- **Nama Fitur ✅ (YYYY-MM-DD):** ringkasan 1 kalimat.`

---

## Dev Commands

```bash
# Dev server
{{PKG_MANAGER}} run dev

# Type check
npx tsc --noEmit

# Lint
{{PKG_MANAGER}} run lint

# Build
{{PKG_MANAGER}} run build
```

---

## Environment Variables

```
# Isi dengan semua env vars yang digunakan
# Format: VAR_NAME    Deskripsi singkat
```

> **Aturan:** Variabel dengan prefix `NEXT_PUBLIC_` = aman untuk client. Tanpa prefix = server-only secret. Jangan salah assign.

---

## Keputusan Arsitektur Penting

### Harga & Kalkulasi
> Selalu hitung server-side — jangan percaya angka dari client.

### Data Flow
> Definisikan di sini: dari mana data mengalir, siapa yang boleh menulis ke mana.

---

## Yang TIDAK Boleh Dilakukan

### Arsitektur & Data Flow
- Jangan call DB/ORM dari luar `server/repositories/`
- Jangan hitung nilai penting (harga, diskon, stok, role) di client
- > tambah larangan spesifik project

### Security — DILARANG KERAS
- Jangan expose secret ke client (prefix `NEXT_PUBLIC_` hanya untuk data publik)
- Jangan commit `.env*` ke repository
- Jangan return error message internal ke client (stack trace, query detail)
- Jangan skip validasi input di server actions / route handlers — selalu Zod
- Jangan trust nilai dari client untuk kalkulasi sensitif
- Jangan gunakan `dangerouslySetInnerHTML` tanpa sanitasi
- Jangan lakukan DB mutation dari GET handler

### Workflow & Docs
- Jangan mulai coding tanpa membaca `CLAUDE.md` dan `AGENTS.md`
- Jangan anggap migration/deploy/QA "lulus" tanpa menjalankan command-nya

---

## Checklist Go-Live

- [ ] Semua env vars sudah di-set di production
- [ ] Webhook URLs sudah didaftarkan ke provider yang sesuai
- [ ] Full flow test: end-to-end dari UI sampai DB
- [ ] Security scan bersih (semgrep, gitleaks, trivy)
- [ ] Monitoring & alerting aktif
