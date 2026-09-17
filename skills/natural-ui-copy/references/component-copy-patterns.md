# Component Copy Patterns

Template copy siap pakai untuk komponen UI yang paling sering dibutuhkan.
Semua contoh menggunakan konteks **platform digital / SaaS** secara umum —
sesuaikan nama produk, fitur, dan konteks spesifik kamu.

---

## Authentication

### Login Page

```
Headline: "Masuk ke [Nama Produk]"
Subheadline: — (tidak perlu, action sudah jelas)

Label email: "Email"
Placeholder email: "nama@email.com"

Label password: "Password"
Link forgot: "Lupa password?"

CTA utama: "Masuk"
CTA Google: "Lanjut dengan Google"

Separator: "atau"

Link ke signup: "Belum punya akun? Daftar gratis"
```

### Register Page

```
Headline: "Buat akun gratis"
Subheadline: "Tidak perlu kartu kredit."

Label nama: "Nama lengkap"
Placeholder: "Nama yang akan tampil di profil"

Label email: "Email kerja atau pribadi"

Label password: "Buat password"
Helper: "Minimal 8 karakter"

CTA: "Buat Akun"

Link ke login: "Sudah punya akun? Masuk"

Legal text: "Dengan mendaftar, kamu setuju dengan Syarat Layanan dan Kebijakan Privasi kami."
```

### Forgot Password

```
Headline: "Reset password"
Body: "Masukkan emailmu dan kami kirimkan link untuk reset password."

Label: "Email akun kamu"

CTA: "Kirim Link Reset"
Back link: "← Kembali ke halaman masuk"

// After submit:
Headline: "Cek emailmu"
Body: "Kami kirim link reset ke [email]. Link berlaku selama 30 menit."
Subtext: "Tidak ada email masuk? Cek folder spam atau [kirim ulang]."
```

---

## Onboarding

### Welcome Screen (Setelah Register)

```
Headline: "Halo, [Nama]! 👋"
Subheadline: "Yuk mulai dengan langkah pertama."

Step 1: "Lengkapi profilmu" 
Step 2: "Buat [item pertama]"
Step 3: "Bagikan ke orang pertama"

CTA: "Mulai Sekarang"
Skip: "Lewati untuk sekarang"
```

### Progress Indicator

```
// Saat dalam progress:
"Langkah 2 dari 4 — Detail Acara"

// Saat selesai satu step:
"✓ Profil selesai! Lanjut ke langkah berikutnya."

// Saat semua selesai:
"Selesai! Semuanya sudah siap."
```

---

## Dashboard

### Greeting

```
// Pagi (05:00–11:59):
"Selamat pagi, [Nama]."

// Siang (12:00–14:59):
"Selamat siang, [Nama]."

// Sore (15:00–17:59):
"Selamat sore, [Nama]."

// Malam (18:00–04:59):
"Selamat malam, [Nama]."
```

### Stats / Metrics

```
Label yang baik:
- "Total tamu diundang" (bukan "Guests")
- "Dibuka minggu ini" (bukan "Opens")
- "Menunggu konfirmasi" (bukan "Pending")
- "Sudah RSVP" (bukan "Responded")
```

---

## Empty States

### Template lengkap:

```tsx
// Komponen Empty State
<EmptyState
  icon={<MailOpen />}
  title="Belum ada [nama item]"
  description="[Satu kalimat tentang apa yang bisa mereka lakukan / value yang akan mereka dapat]"
  action={<Button>Buat [Nama Item] Pertama</Button>}
  secondaryAction={<Link>Pelajari cara kerja [fitur]</Link>}
/>
```

### Contoh per konteks:

**Daftar kosong (first time)**:
```
Icon: folder-open atau item-specific
Title: "Belum ada [item]"
Desc: "Buat [item] pertamamu dan mulai [benefit]."
CTA: "Buat [Item]"
```

**Hasil pencarian kosong**:
```
Icon: search atau magnifying-glass
Title: "Tidak ada hasil untuk "[kata kunci]""
Desc: "Coba kata kunci lain atau hapus beberapa filter."
CTA: "Hapus Filter"
Secondary: "Coba pencarian lain"
```

**Filter aktif, hasil kosong**:
```
Icon: filter
Title: "Tidak ada [item] yang cocok"
Desc: "Filter yang aktif menyembunyikan semua hasil. Coba ubah atau hapus filter."
CTA: "Reset Filter"
```

**Fitur terkunci / belum diaktifkan**:
```
Icon: lock
Title: "[Nama Fitur] tersedia di [Plan] ke atas"
Desc: "Upgrade untuk akses [benefit konkret], bukan hanya "lebih banyak fitur"."
CTA: "Lihat Paket"
Secondary: "Pelajari perbedaan paket"
```

---

## Form Patterns

### File Upload

```
// Idle state:
"Seret file ke sini atau klik untuk pilih"
Subtext: "JPG, PNG, atau PDF · Maks. 10MB"

// Dragging:
"Lepas file di sini"

// Uploading:
"Mengupload [nama-file.jpg]... 67%"

// Success:
"[nama-file.jpg] berhasil diupload ✓"
Helper: "Kamu bisa ganti file ini kapan saja"

// Error:
"File terlalu besar — maks. 10MB. Coba kompres dulu."
"Format ini belum didukung. Gunakan JPG atau PNG."
```

### Date Picker

```
Label: "Tanggal [acara/deadline/dll]"
Placeholder: "Pilih tanggal"
// Jangan gunakan "DD/MM/YYYY" sebagai placeholder — gunakan calendar picker
```

### Select / Dropdown

```
Placeholder: "Pilih [kategori]..." 
// atau
Placeholder: "-- Pilih satu --"
// JANGAN: "Select an option"
```

### Character Count

```
// Normal:
"240 karakter tersisa"

// Mendekati limit:
"Hanya 20 karakter lagi"

// Melebihi:
"Lebih 15 karakter dari batas maksimum"
```

---

## Notifikasi & Alerts

### Alert Banner

```
// Info:
"ℹ️ [Konteks netral yang perlu diketahui user]"

// Success:
"✓ [Konfirmasi apa yang berhasil, secara konkret]"

// Warning:
"⚠ [Sesuatu yang perlu perhatian, tapi belum error]"
Action (opsional): "Perbaiki Sekarang"

// Error:
"✕ [Apa yang salah + apa yang bisa dilakukan]"
Action: "Coba Lagi" atau "Hubungi Kami"
```

### Toast Notifications

```
// Durasi pendek (3 detik) — untuk aksi kecil:
"Tersimpan"
"Disalin ke clipboard"
"Link diperbarui"

// Durasi sedang (5 detik) — untuk aksi penting:
"Undangan dikirim ke 15 tamu"
"Foto profil diperbarui"

// Persistent (dismiss manual) — untuk error atau info penting:
"Koneksi terputus. Mengupload ulang..."
"Sesimu akan habis dalam 5 menit. [Perpanjang Sesi]"
```

---

## Modal & Dialog

### Confirmation Dialog (Aksi Aman)

```
Title: "Konfirmasi [aksi]?"
Body: "[Detail apa yang akan terjadi, informasi relevan]"
CTA: "[Aksi]" (primary)
Cancel: "Batal" (secondary)
```

### Confirmation Dialog (Aksi Destruktif)

```
Title: "Hapus [nama spesifik item]?"
Body: "Tindakan ini tidak bisa dibatalkan. 
       [Jelaskan konsekuensi: link, data, akses yang akan hilang]"
CTA: "Ya, Hapus" (destructive/red)
Cancel: "Batal" (secondary)

// Untuk aksi sangat destruktif, minta konfirmasi ketik:
Body tambahan: "Ketik nama undangan untuk konfirmasi:"
Input placeholder: "[nama undangan]"
CTA: disabled sampai input cocok
```

### Info Modal

```
Title: "[Topik yang jelas]"
Body: [Konten]
Close: "Tutup" atau "Mengerti"
// Jangan: "OK", "Yes", "Dismiss"
```

---

## Pricing & Upgrade

### Pricing Card

```
// Free tier:
Plan: "Gratis"
Price: "Rp 0 / bulan"
CTA: "Mulai Gratis"
Note: "Tidak perlu kartu kredit"

// Paid tier:
Plan: "Pro" (bukan "Premium" yang sudah terlalu umum)
Price: "Rp 99.000 / bulan"
CTA: "Coba Pro 14 Hari" (dengan trial) atau "Mulai Pro"
Note: "Batalkan kapan saja"

// Enterprise:
Plan: "Tim"
Price: "Harga khusus"
CTA: "Hubungi Kami"
```

### Upgrade Prompt (In-App)

```
// Saat user hit limit:
"Kamu sudah pakai 5 dari 5 undangan gratis."
Action: "Upgrade ke Pro untuk undangan tak terbatas →"

// Saat user mencoba fitur terkunci:
"[Nama Fitur] tersedia di paket Pro."
Desc: "[Satu kalimat benefit konkret fitur ini]"
Action: "Upgrade ke Pro — Rp 99.000/bulan"
Secondary: "Lihat semua fitur Pro"
```

---

## Email Templates

### Transactional Email

**Subject line patterns:**
```
Konfirmasi: "Akunmu sudah aktif, [Nama]"
Notifikasi: "[Nama] baru saja RSVP ke undanganmu"
Reminder: "Acara [nama] 3 hari lagi — ada yang perlu disiapkan?"
Reset: "Reset password kamu"
Invoice: "Tagihan bulan [bulan] — Rp [amount]"
```

**Opening:**
```
✅ "Halo [Nama],"
✅ "Hai [Nama]!"  (lebih casual)
❌ "Dear [Nama],"  (terlalu formal untuk produk consumer)
❌ "Kepada Yth. [Nama]"  (sangat formal, hanya untuk dokumen resmi)
```

**CTA dalam email:**
```
// Tombol harus standalone — bisa dipahami tanpa baca email penuh
"Buka Undangan" 
"Konfirmasi Kehadiran"
"Reset Password"
"Lihat Detail Tagihan"
```

**Footer:**
```
"Kamu menerima email ini karena terdaftar di [Nama Produk]."
"[Berhenti berlangganan] · [Pengaturan Notifikasi]"
```

---

## 404 & Error Pages

### 404 Page

```
Headline: "Halaman tidak ditemukan"
Body: "Link ini mungkin sudah dipindah, dihapus, atau salah ketik."
CTA: "Kembali ke Beranda"
Secondary: "Cari halaman"
```

### 500 / Server Error Page

```
Headline: "Ada yang tidak beres di pihak kami"
Body: "Tim kami sudah diberitahu dan sedang memperbaikinya. 
       Coba refresh dalam beberapa menit."
CTA: "Coba Refresh"
Secondary: "Hubungi Support"
```

### Maintenance Page

```
Headline: "[Nama Produk] sedang dalam pemeliharaan"
Body: "Kami sedang upgrade sistem. Estimasi selesai: [waktu]."
Subtext: "Follow @[handle] untuk update terbaru."
```

---

## Settings & Account

### Section Headers

```
// Gunakan bahasa yang user-centric, bukan system-centric:
✅ "Informasi Akun" (bukan "User Data")
✅ "Notifikasi" (bukan "Notification Settings")
✅ "Privasi & Keamanan" (bukan "Security Configuration")
✅ "Paket & Tagihan" (bukan "Subscription Management")
```

### Danger Zone

```
Section title: "Zona Bahaya"
Section desc: "Tindakan di bawah ini bersifat permanen dan tidak bisa dibatalkan."

Item: "Hapus Akun"
Desc: "Menghapus akun dan semua data secara permanen."
CTA: "Hapus Akun Saya"
```
