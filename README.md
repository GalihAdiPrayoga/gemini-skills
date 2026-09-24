# 🌌 Gemini & Antigravity Autonomous AI System Suite

Repository resmi kumpulan **Cognitive Architecture (`GEMINI.md`, `AGENTS.md`)**, **53 Modular Skills**, **Plugins**, **Rules**, dan **Extensions / MCP** untuk ekosistem AI **Gemini CLI** & **Antigravity IDE**.

---

## ⚡ Quick 1-Command Installation via NPX

Kamu bisa menginstall dan menyinkronkan seluruh skills, plugins, rules, dan extensions langsung ke direktori `.gemini` di sistem (Windows, macOS, Linux) tanpa perlu clone manual:

```bash
npx -y github:GalihAdiPrayoga/gemini-skills
```

### 🔍 Cara Kerja Installer Otomatis (`bin/cli.js`):
1. **Deteksi Otomatis Direktori `.gemini`:**
   - Mengecek variabel lingkungan `GEMINI_HOME` jika didefinisikan.
   - Pada **Windows**: Otomatis mendeteksi folder `%USERPROFILE%\.gemini` (misal: `C:\Users\<User>\.gemini`).
   - Pada **macOS & Linux**: Otomatis mendeteksi folder home `~/.gemini`.
   - Jika folder belum ada, installer akan membuat struktur folder baru secara otomatis.
2. **Sinkronisasi Multi-Level (Dual Compatibility):**
   - Menyalin berkas langsung ke root `.gemini/` (untuk **Gemini CLI**).
   - Secara otomatis membuat mirror ke `.gemini/config/` (untuk **Antigravity IDE**).
3. **Zero External Dependencies:**
   - Menggunakan murni modul standar Node.js (`fs`, `path`, `os`), ringan, cepat, dan aman dieksekusi di lingkungan bersih pasca install ulang OS.

---

## 🛠️ Opsi & Parameter CLI

| Parameter | Alias | Deskripsi |
|---|---|---|
| `--target <path>` | `-t` | Menentukan lokasi folder target `.gemini` secara spesifik (kustom). |
| `--dry-run` | - | Mensimulasikan proses instalasi tanpa menulis berkas ke disk. |
| `--help` | `-h` | Menampilkan panduan bantuan dan daftar opsi CLI. |

### Contoh Penggunaan Khusus:
```bash
# Menentukan folder target kustom
npx -y github:GalihAdiPrayoga/gemini-skills --target "D:\MyConfigs\.gemini"

# Simulasi preview berkas sebelum instalasi riil
npx -y github:GalihAdiPrayoga/gemini-skills --dry-run
```

---

## 📂 Struktur Repositori & Pemetaan Direktori

```
gemini-skills/
│
├── bin/
│   └── cli.js            # Node.js Zero-Dependency NPX Executable
├── package.json          # Manifest NPX & CLI binary definition
│
├── GEMINI.md             # Highest-Level Cognitive Instruction Architecture & Autonomous Protocol
├── AGENTS.md             # Global Settings, Core Agent Context, UI/UX Intelligence & Collaboration Manual
│
├── rules/                # Standar aturan & panduan eksekusi
│   ├── ecc.md            # Enterprise Coding Craft & Backend Robustness
│   ├── superpowers.md    # TDD & Multi-Agent Parallel Execution Rules
│   └── ui-ux-pro-max.md  # Automatic UI/UX Design Intelligence & Motion Blueprint
│
├── plugins/              # Paket plugin integrasi
│   ├── ecc/              # Enterprise backend & database pattern plugin
│   ├── superpowers/      # Parallel agent orchestration plugin
│   └── ui-ux-pro-max/    # Comprehensive design tokens & search intelligence engine
│
├── skills/               # 53 Modular Engineering & Creative Skills
│   ├── animate/          ├── animate-expo/         ├── animation-vocabulary/
│   ├── apple-design/     ├── ask-sonner/           ├── banner-design/
│   ├── brainstorm/       ├── brainstorming/        ├── brand/
│   ├── canvas-design/    ├── claude-md-improver/   ├── claude-superpowers-architect/
│   ├── context7-mcp/     ├── design/               ├── design-system/
│   ├── dispatching-parallel-agents/                ├── ecc/
│   ├── emil-design-eng/  ├── executing-plans/      ├── find-animation-opportunities/
│   ├── finishing-a-development-branch/             ├── frontend-design/
│   ├── impeccable/       ├── improve-animations/   ├── init-project/
│   ├── natural-ui-copy/  ├── pick-ui-library/      ├── plan-writer/
│   ├── prototype/        ├── qa-master/            ├── receiving-code-review/
│   ├── requesting-code-review/                     ├── review-animations/
│   ├── sdd-self-improvement-assistant/             ├── skill-router/
│   ├── skill-upgrader/   ├── slides/               ├── spec-writer/
│   ├── subagent-driven-development/                ├── superpowers/
│   ├── systematic-debugging/                       ├── template-convert/
│   ├── test-driven-development/                    ├── ui-styling/
│   ├── ui-ux-pro-max/    ├── using-git-worktrees/  ├── using-superpowers/
│   ├── verification-before-completion/             ├── weekly-report/
│   ├── write-swift/      ├── writing-plans/        ├── writing-plans-self-improvement-assistant/
│   └── writing-skills/
│
├── extensions/           # 10 Runtime Extensions & MCP Workflows
│   ├── caveman/          # High-density token & terse output engine
│   ├── chrome-devtools-mcp/ # Live browser DOM & CSS debugging via CDP
│   ├── clasp/            # Google Apps Script automation
│   ├── claude-code-workflows/ # Multi-agent orchestration workflows & templates
│   ├── conductor/        # Background task & service conductor
│   ├── context7/         # Context7 documentation & code query MCP
│   ├── last30days-skill/ # Research & news aggregation
│   ├── ponytail/         # Senior developer simplification & anti-bloat
│   └── superpowers/      # Parallel agent orchestration & TDD loop
│
└── public/               # Template publik & aset desain
    └── templates/        # Template artboard & layout
```

---

## ⚡ Alur Kerja Utama (Mandatory Engineering Protocol)

1. **Context & Spec:** Membaca konteks atau membuat formal spec via `/spec-writer`.
2. **Implementation Plan:** Menyusun rencana langkah demi langkah via `/plan-writer`.
3. **Autonomous Execution:** Eksekusi kode via parallel sub-agents dengan TDD.
4. **Verification & QA:** Validasi output nyata, pengujian Playwright / unit test, dan self-code review.

---

## 🔄 Pemulihan Pasca Install Ulang OS (Disaster Recovery)

Jika kamu baru saja menginstall ulang Windows atau berganti perangkat:
1. Pastikan **Node.js** dan **Git** sudah terpasang.
2. Buka Terminal / PowerShell / Git Bash, lalu jalankan:
   ```bash
   npx -y github:GalihAdiPrayoga/gemini-skills
   ```
3. Seluruh arsitektur kognitif, aturan, dan 53 skills langsung aktif dan siap digunakan oleh Gemini CLI dan Antigravity IDE.

---

## 🔒 Lisensi & Privasi

Dikelola secara resmi oleh **Muhammad Galih Adi Prayoga** ([@GalihAdiPrayoga](https://github.com/GalihAdiPrayoga)).  
Lisensi: **MIT License**.
