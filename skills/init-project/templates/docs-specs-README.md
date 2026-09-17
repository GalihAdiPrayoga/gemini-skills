# Specs — {{PROJECT_NAME}}

Dokumen spesifikasi desain/arsitektur, dihasilkan oleh `/spec-writer` dari hasil `/brainstorm`.

## Kapan sebuah fitur butuh spec

- Fitur baru yang menyentuh permukaan sensitif: **{{SENSITIVE_SURFACES}}**
- Perubahan arsitektur atau schema
- Apa pun yang ambigu cukup untuk butuh `/brainstorm` dulu

Perubahan kecil / bugfix satu file **tidak** butuh spec — langsung ke plan atau eksekusi.

## Naming convention

```
YYYY-MM-DD-{slug-fitur}-design.md
```

Contoh: `2026-07-25-checkout-dp-design.md`

## Isi minimal sebuah spec

- **Problem & goal** — kenapa fitur ini dibuat
- **Scope** — apa yang masuk, apa yang sengaja di luar scope
- **Desain** — arsitektur, data flow, keputusan teknis dan alasannya
- **Permukaan sensitif** — auth/payment/webhook/upload/schema yang tersentuh, dan mitigasinya
- **Open questions** — yang belum terjawab, dibawa ke sesi `/plan-writer`

## Alur

```
/brainstorm  →  /spec-writer  →  simpan di sini  →  /plan-writer
```

Spec adalah **sumber kebenaran** untuk plan yang mengikutinya. Jika plan menyimpang dari spec, update spec dulu — jangan biarkan keduanya kontradiksi diam-diam.
