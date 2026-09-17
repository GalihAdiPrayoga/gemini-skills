# Codemaps — {{PROJECT_NAME}}

Peta arsitektur token-lean: struktur folder, entry point, dan alur data — supaya agent baru bisa orientasi cepat tanpa membaca seluruh codebase.

## Kapan digenerate / diperbarui

- Setelah struktur folder awal stabil (selesai setup, sebelum fitur pertama)
- Setelah refactor besar yang mengubah struktur folder/modul
- Setelah sprint yang menambah domain/modul baru

Belum ada codemap di sini di titik ini — file ini cuma seed. Generate yang sebenarnya dengan skill ecc `update-codemaps` bila tersedia di environment Anda:

```
~/.claude/skills/ecc/update-codemaps
```

Kalau skill itu tidak tersedia, tulis manual: daftar folder utama + tanggung jawabnya (1-2 kalimat per folder), cukup untuk agent baru tahu "kode fitur X ada di mana" tanpa grep seluruh repo.

## Format yang disarankan

```
## <nama-folder>
Tanggung jawab: <1-2 kalimat>
Entry point: <file utama>
Bergantung pada: <folder/modul lain>
```

## Aturan

- Codemap **bukan** dokumentasi API lengkap — cukup untuk navigasi, bukan referensi detail.
- Update sebagai bagian dari docs-as-code — kalau struktur folder berubah signifikan, codemap ikut di-update di commit yang sama (lihat `AGENTS.md` § Docs-as-Code).
