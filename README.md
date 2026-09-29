# Alanka Management System

Sistem manajemen internal untuk usaha freelance CCTV, jaringan, dan IT.
Aplikasi ini membantu mengelola customer, katalog produk dan jasa, quotation,
project, invoice, pembayaran, dan pengeluaran dalam satu tempat.

## Daftar isi

- [Fitur yang tersedia](#fitur-yang-tersedia)
- [Teknologi dan struktur proyek](#teknologi-dan-struktur-proyek)
- [Persiapan dan instalasi lokal](#persiapan-dan-instalasi-lokal)
- [Konfigurasi environment](#konfigurasi-environment)
- [Menjalankan aplikasi](#menjalankan-aplikasi)
- [Alur penggunaan sistem](#alur-penggunaan-sistem)
- [Panduan setiap modul](#panduan-setiap-modul)
- [Skenario testing](#skenario-testing)
- [Database dan deployment](#database-dan-deployment)
- [Dokumentasi terkait](#dokumentasi-terkait)
- [Catatan pengembangan](#catatan-pengembangan)

## Fitur yang tersedia

- Login internal dengan session.
- Dashboard ringkasan quotation, project, revenue, expense, profit, dan piutang.
- Data customer: nama, telepon, email, alamat, dan tipe customer.
- Katalog produk dan jasa: kode, harga modal, harga jual, kategori, satuan, dan stok.
- Pembuatan quotation dengan beberapa item, diskon, pajak, dan catatan.
- Perubahan status quotation.
- Download quotation dalam format PDF.
- Pembuatan project dari quotation yang berstatus `Approved`.
- Pembuatan invoice dengan tanggal jatuh tempo.
- Pencatatan pembayaran sebagian maupun pelunasan invoice.
- Pencatatan pengeluaran operasional.

> Modul pembelian, maintenance, multi-user, role management, upload dokumen,
> dan penyimpanan file eksternal masih merupakan pengembangan lanjutan.

## Teknologi dan struktur proyek

- Python 3.11 atau lebih baru
- FastAPI dan Uvicorn
- Jinja2 untuk server-side templates
- SQLAlchemy
- SQLite untuk pengembangan lokal
- PostgreSQL/Supabase untuk opsi deployment
- ReportLab untuk pembuatan PDF

Struktur penting:

```text
app/
├── app/
│   ├── main.py                 # route dan alur aplikasi
│   ├── database.py             # koneksi database
│   ├── models.py               # model SQLAlchemy
│   ├── services/
│   │   ├── calculation_service.py
│   │   └── pdf_service.py
│   ├── templates/              # halaman Jinja2
│   └── static/                 # CSS dan gambar
├── database/
│   ├── migrations/
│   └── README.md
├── alanka.db                   # database SQLite lokal
├── .env.example
├── PRD.MD
├── README.md
└── requirements.txt
```

## Persiapan dan instalasi lokal

Buka PowerShell pada folder proyek:

```powershell
cd "D:\KERJA\ALANKA\TEST\app"
```

Buat dan aktifkan virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Jika PowerShell menolak menjalankan script, gunakan policy hanya untuk sesi
terminal saat ini:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install dependency:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Konfigurasi environment

Salin `.env.example` menjadi `.env` jika ingin mengubah konfigurasi:

```powershell
Copy-Item .env.example .env
```

Konfigurasi default untuk lokal:

```env
DATABASE_URL=sqlite:///./alanka.db
SECRET_KEY=change-this-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
AUTO_CREATE_SCHEMA=true
```

Keterangan:

| Variabel | Fungsi |
|---|---|
| `DATABASE_URL` | URL koneksi database |
| `SECRET_KEY` | Kunci session aplikasi |
| `ADMIN_USERNAME` | Username login internal |
| `ADMIN_PASSWORD` | Password login internal |
| `AUTO_CREATE_SCHEMA` | Membuat tabel otomatis saat startup jika bernilai `true` |

Jangan commit `.env` atau password database ke repository.

## Menjalankan aplikasi

Jalankan development server:

```powershell
uvicorn app.main:app --reload
```

Buka alamat berikut di browser:

```text
http://127.0.0.1:8000
```

Login awal sesuai konfigurasi default:

```text
Username: admin
Password: admin123
```

URL utama:

| Halaman | URL |
|---|---|
| Login | `/login` |
| Dashboard | `/dashboard` |
| Customer | `/customers` |
| Products & Jasa | `/products` |
| Quotations | `/quotations` |
| Finance | `/finance` |

Tekan `Ctrl+C` pada terminal untuk menghentikan server.

## Alur penggunaan sistem

Alur operasional yang disarankan:

```text
Customer
   ↓
Produk & Jasa
   ↓
Buat Quotation
   ↓
Review dan ubah status menjadi Approved
   ↓
Buat Project
   ↓
Buat Invoice
   ↓
Catat Payment
   ↓
Cek Dashboard dan Profit
```

### 1. Siapkan customer

1. Buka menu **Customers**.
2. Isi nama, telepon, email, alamat, dan tipe customer.
3. Simpan data.

Customer diperlukan sebelum membuat quotation atau invoice.

### 2. Siapkan produk dan jasa

1. Buka **Products & Jasa**.
2. Isi kode, nama, tipe, kategori, satuan, harga modal, harga jual, dan stok.
3. Harga jual produk dan jasa dihitung otomatis: markup 20% untuk harga modal
   sampai dengan Rp350.000 dan markup 25% untuk harga modal di atas Rp350.000.

Saat startup pertama, aplikasi membuat data contoh customer dan katalog jika
database masih kosong.

### 3. Buat quotation

1. Buka **Quotations** lalu pilih **Buat quotation**.
2. Pilih customer.
3. Pilih satu atau beberapa produk/jasa dan isi quantity.
4. Isi diskon, pajak, dan catatan bila diperlukan.
5. Simpan quotation.
6. Buka detail quotation untuk memeriksa total, HPP, dan margin.
7. Ubah status sesuai proses bisnis, misalnya `Sent`, `Negotiation`, atau
   `Approved`.
8. Download PDF melalui detail quotation jika diperlukan.

### 4. Buat project dari quotation

Project hanya dapat dibuat dari quotation dengan status `Approved`.

1. Buka detail quotation yang sudah disetujui.
2. Isi nama project dan lokasi.
3. Simpan project.
4. Project akan terlihat pada dashboard.

### 5. Kelola Finance

Pada menu **Finance**:

1. Buat invoice dengan memilih customer, project opsional, total, dan jatuh
   tempo.
2. Status awal invoice adalah `Issued`.
3. Catat pembayaran dari form pada invoice terkait.
4. Pembayaran kurang dari total menghasilkan status `Partially Paid`.
5. Pembayaran yang mencapai atau melebihi total menghasilkan status `Paid`.
6. Catat biaya operasional melalui bagian **Catat pengeluaran**.
7. Periksa revenue, piutang, expense, dan profit pada dashboard.

Contoh:

```text
Invoice       Rp 5.000.000
Payment awal  Rp 2.000.000  → Partially Paid
Payment akhir Rp 3.000.000  → Paid
Expense       Rp   750.000
Profit        Rp 4.250.000
```

## Panduan setiap modul

### Dashboard

Dashboard menampilkan:

- `Gross revenue`: jumlah total invoice.
- `Outstanding`: total invoice dikurangi seluruh payment.
- `Gross profit`: revenue dikurangi expense.
- Jumlah project aktif dan project selesai.
- Quotation dan project terbaru.

### Customers

Menyimpan data pihak yang menerima produk, jasa, quotation, project, atau invoice.

### Products & Jasa

Menyimpan katalog barang dan layanan. Harga modal digunakan untuk menghitung
HPP dan analisis margin quotation.

### Quotations

Quotation memiliki nomor otomatis, item, quantity, diskon, pajak, status, dan
catatan. Quotation yang disetujui dapat menjadi dasar pembuatan project.

### Finance

Finance mencakup invoice, payment, dan expense. Invoice dapat dibayar bertahap.
Pencatatan payment harus dilakukan pada invoice yang sesuai agar outstanding
dan status terhitung dengan benar.

## Skenario testing

Testing saat ini dilakukan manual melalui browser. Gunakan urutan berikut untuk
memverifikasi alur utama:

1. Login dengan kredensial yang benar; pastikan masuk ke dashboard.
2. Akses `/finance` tanpa login; pastikan diarahkan ke `/login`.
3. Tambah satu customer dan satu produk/jasa.
4. Buat quotation dengan quantity lebih dari satu; pastikan total dan PDF dapat
   dibuka.
5. Ubah quotation menjadi `Approved`, lalu buat project.
6. Buat invoice `5000000`; pastikan invoice muncul dengan status `Issued`.
7. Catat payment `2000000`; pastikan status menjadi `Partially Paid`.
8. Catat payment `3000000`; pastikan status menjadi `Paid`.
9. Tambahkan expense `750000`; pastikan profit dashboard berkurang sebesar
   `750000`.
10. Logout, lalu pastikan halaman internal tidak bisa dibuka tanpa login.

Belum tersedia folder test otomatis pada versi ini. Dependency `pytest` dan
`httpx` sudah disediakan untuk pengembangan test berikutnya.

## Database dan deployment

### SQLite lokal

SQLite digunakan agar aplikasi dapat langsung dijalankan. Schema dibuat otomatis
saat startup jika `AUTO_CREATE_SCHEMA=true`. File database lokal adalah
`alanka.db`.

### PostgreSQL/Supabase

Panduan database tersedia di [database/README.md](database/README.md).
Ringkasnya:

1. Buat project PostgreSQL/Supabase.
2. Set `DATABASE_URL` ke connection string PostgreSQL.
3. Jalankan [001_initial_schema.sql](database/migrations/001_initial_schema.sql), lalu
   [002_add_customer_survey_description.sql](database/migrations/002_add_customer_survey_description.sql).
4. Set `AUTO_CREATE_SCHEMA=false`.
5. Jalankan aplikasi menggunakan konfigurasi tersebut.

Gunakan migration bernomor baru untuk perubahan schema berikutnya dan jangan
menghapus data production secara manual.

## Dokumentasi terkait

- [PRD.MD](PRD.MD): kebutuhan produk dan rencana pengembangan.
- [database/README.md](database/README.md): workflow SQLite dan PostgreSQL.
- [.env.example](.env.example): contoh konfigurasi environment.
- [requirements.txt](requirements.txt): dependency Python.
- [app/main.py](app/main.py): route dan alur request aplikasi.
- [app/models.py](app/models.py): struktur model database.

## Catatan pengembangan

- Ganti `SECRET_KEY`, username, dan password default sebelum production.
- Gunakan HTTPS dan secret manager pada deployment.
- Pastikan `.env`, credential database, dan database production tidak masuk
  version control.
- Saat menambah fitur database, buat migration baru dan perbarui dokumentasi.
- Saat menambah route baru, tambahkan link navigasi, validasi login, dan
  skenario testing yang relevan.
