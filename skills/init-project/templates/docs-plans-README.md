# Plans — {{PROJECT_NAME}}

Implementation plan — breakdown task yang executable, dihasilkan dari spec di `docs/superpowers/specs/`.

## Kombinasi skill wajib saat membuat plan

```
/plan-writer  bersamaan dengan  superpowers:writing-plans-self-improvement-assistant
```

`/plan-writer` menyusun task breakdown dari spec. `writing-plans-self-improvement-assistant` berjalan **di samping**-nya untuk menambahkan planning memory berbasis bukti (pelajaran dari plan-plan sebelumnya di project ini) dan plan-quality linting — tanpa melemahkan disiplin `/plan-writer` sendiri. Jalankan keduanya, bukan salah satu.

## Naming convention

```
YYYY-MM-DD-{slug-fitur}.md
```

Harus merujuk ke spec dengan slug yang sama di `docs/superpowers/specs/`.

## Isi minimal sebuah plan

- **Referensi spec** — link ke file spec yang jadi sumber
- **Task list berurutan** — dengan dependency order eksplisit (task mana yang harus selesai dulu)
- **File manifest per task** — file mana yang akan disentuh, supaya sub-agent paralel tidak bentrok
- **Validation step per task** — command atau kriteria yang membuktikan task itu selesai
- **User approval checkpoint** — plan harus di-approve user sebelum eksekusi dimulai (Aturan Tim #1 di `CLAUDE.md`)

## Alur

```
spec  →  /plan-writer + superpowers:writing-plans-self-improvement-assistant  →  [user approve]  →  eksekusi
```

Setelah plan di-approve, lanjut ke eksekusi dengan `superpowers:subagent-driven-development` + `superpowers:sdd-self-improvement-assistant` — lihat `AGENTS.md` § Workflow Skills.
