# Voice & Tone Guide

Tone bukan tentang selalu santai atau selalu formal. Tone adalah **respon
empati terhadap situasi user** — sama seperti cara bicara orang yang baik
akan berubah tergantung lawan bicara sedang senang, frustasi, atau bingung.

---

## The Tone Spectrum

```
← Lebih Serius                              Lebih Santai →
   [Error]  [Warning]  [Neutral]  [Success]  [Onboarding]
```

---

## Situasi → Tone → Contoh

### User Baru / Onboarding

**Situasi**: Mereka belum tahu apa-apa. Mungkin nervous. Ingin berhasil.

**Tone**: Hangat, encouraging, simple. Seperti teman yang sudah pernah lewat jalan ini.

**Kata-kata yang cocok**: "Mulai dari sini", "Mudah kok", "Tinggal satu langkah lagi", "Kamu bisa preview dulu sebelum kirim"

**Kata-kata yang dihindari**: "Configure", "Initialize", "Mandatory", "Required fields", "Submit"

**Contoh**:
```
❌ "Please complete all required fields to proceed with registration."
✅ "Isi tiga hal ini dan akunmu siap — butuh 2 menit."

❌ "Your account has been successfully created."
✅ "Selamat datang, [Nama]! Undangan pertamamu menunggu."
```

---

### User Aktif / Dalam Alur Kerja

**Situasi**: Mereka sedang fokus mengerjakan sesuatu. Setiap interupsi mengganggu.

**Tone**: Efisien, direct, minimal. Berikan informasi, bukan percakapan.

**Kata-kata yang cocok**: "Simpan", "Lanjut", "Preview", "Kirim", "Selesai"

**Contoh**:
```
❌ "Great job! You've successfully saved your changes to the invitation."
✅ "Tersimpan." (dengan timestamp jika relevan)

❌ "Would you like to proceed to the next step in the invitation creation process?"
✅ "Lanjut →"
```

---

### User Mengalami Error

**Situasi**: Mereka frustrated atau khawatir. Sesuatu tidak berjalan sesuai harapan.

**Tone**: Calm, clear, tidak menyalahkan. Fokus pada solusi, bukan masalah.

**Framework**: [Apa yang terjadi] + [Kenapa] + [Apa yang bisa dilakukan]

**Kata-kata yang cocok**: "Coba lagi", "Hubungi kami jika masalah berlanjut", "Perubahanmu aman"

**Kata-kata yang dihindari**: "Error!", "Failed", "Invalid", "You must", "You forgot"

**Contoh**:
```
❌ "Upload failed. Invalid file format."
✅ "Format file ini belum didukung. Coba upload JPG atau PNG (maks. 5MB)."

❌ "Error: Session expired. Please login again."
✅ "Sesimu habis karena terlalu lama tidak aktif. Masuk lagi — datamu aman."

❌ "Required field missing."
✅ "Nama acara belum diisi — ini akan muncul di header undangan."
```

---

### Aksi Destruktif (Hapus, Cancel, Irreversible)

**Situasi**: User mau melakukan sesuatu yang tidak bisa dibatalkan.

**Tone**: Serius, konkret, tidak dramatis. Beri konteks tanpa menakut-nakuti.

**Pattern**: Sebut spesifik apa yang akan dihapus/dibatalkan.

**Contoh**:
```
❌ "Are you sure? This action cannot be undone."
✅ "Hapus undangan 'Pernikahan Budi & Sari'? 
    Semua link yang sudah dibagikan akan berhenti bekerja."

❌ "Cancel subscription?"
✅ "Batalkan langganan Pro? Akses ke fitur premium berhenti di akhir bulan ini."
```

Dialog konfirmasi:
- Tombol confirm → sebutkan aksinya: "Ya, Hapus" / "Batalkan Langganan"
- Tombol cancel → "Batal" atau "Kembali", bukan "No" atau "Cancel"

---

### Empty State

**Situasi**: Belum ada konten. Bisa karena baru mulai atau hasil filter kosong.

**Tone**: Helpful dan inviting. Bukan sekedar laporan status.

**Dua jenis empty state**:

1. **First-time empty** (user baru, belum punya data):
   → Tone: encouraging, tunjukkan value, ajak mulai
   
2. **Search/filter empty** (ada data, tapi filter tidak cocok):
   → Tone: neutral, helpful, tawarkan alternatif

**Contoh**:
```
// First-time empty
❌ "No invitations found."
✅ Headline: "Belum ada undangan"
   Body: "Buat undangan pertamamu sekarang — pilih template, 
          isi detail acara, dan bagikan ke tamu."
   CTA: "Pilih Template"

// Search/filter empty
❌ "No results found for your search."
✅ Headline: "Tidak ada undangan yang cocok"
   Body: "Coba kata kunci lain atau hapus filter yang aktif."
   CTA: "Hapus Semua Filter"
```

---

### Success / Konfirmasi

**Situasi**: User berhasil melakukan sesuatu penting.

**Tone**: Positif, konkret, brief. Jangan over-celebrate hal kecil.

**Ukur intensitas pujian dengan bobot aksi**:
- Simpan draft → cukup "Tersimpan" dengan timestamp
- Kirim ke tamu → acknowledge effort, konfirmasi hasil
- Akun berhasil dibuat → welcome yang hangat

**Contoh**:
```
❌ "Amazing! Your invitation has been successfully sent!"
✅ "Undangan terkirim ke 28 tamu. Mereka bisa buka link-nya sekarang."

❌ "Settings updated!"
✅ "Pengaturan disimpan."

❌ "Congratulations on completing your profile!"
✅ "Profil lengkap. Sekarang tamu bisa lihat info kontakmu."
```

---

## Voice Consistency Rules

### Gunakan "kamu", bukan "Anda" (untuk produk consumer/casual)
Kecuali produk sangat formal (B2B enterprise, layanan pemerintah).

### Aktif, bukan pasif
```
❌ "Data Anda akan disimpan oleh sistem"
✅ "Kami simpan datamu secara otomatis"
```

### Konkret, bukan abstrak
```
❌ "Proses mungkin membutuhkan beberapa saat"
✅ "Biasanya selesai dalam 1–2 menit"
```

### Pendek, kecuali perlu panjang
Sebagian besar UI copy harus bisa dibaca dalam 3 detik.
Penjelasan panjang hanya untuk onboarding, tooltip, atau dokumentasi.

### Hindari double negative
```
❌ "Jangan lupa untuk tidak menonaktifkan notifikasi"
✅ "Aktifkan notifikasi agar kamu tidak ketinggalan update"
```

---

## Bahasa Indonesia Specifics

### Jangan mix-match tidak konsisten
Pilih salah satu dan konsisten di seluruh produk:
- "kamu" vs "Anda" (pilih berdasarkan tone produk)
- "unduh" vs "download" (pilih berdasarkan target user)
- "unggah" vs "upload"

Untuk produk tech consumer di Indonesia, mixing ringan OK untuk kata yang
sudah sangat umum: "upload", "download", "email", "link" biasanya lebih
natural dari padanannya.

### Angka dan format
- Gunakan titik untuk ribuan: 1.000, bukan 1,000
- Untuk range: "1–3 menit" dengan en-dash, bukan tanda minus
- Tanggal: "15 Januari 2025", bukan "01/15/2025"

### Sapaan
- Opening email: "Halo [Nama]," bukan "Dear [Nama],"
- Notifikasi: tanpa sapaan, langsung ke konten
