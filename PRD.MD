PRD — Alanka Management System
Sistem Manajemen Freelance CCTV, Jaringan, dan IT
1. Informasi Umum

Nama aplikasi: Alanka Management System

Jenis aplikasi: Web Application

Tujuan utama: Membantu pengelolaan usaha freelance yang bergerak di bidang:

Instalasi CCTV
Instalasi dan maintenance jaringan/LAN
Penjualan perangkat jaringan
Maintenance perangkat IT
Pengadaan barang
Pembuatan quotation/penawaran
Pengelolaan project
Pencatatan pemasukan dan pengeluaran
Penagihan customer

Aplikasi ditujukan untuk penggunaan internal oleh pemilik/teknisi dan admin/finance.

2. Tujuan Sistem

Sistem dibuat untuk menggantikan proses manual menggunakan spreadsheet menjadi satu aplikasi terpusat.

Sistem harus mampu:

Menyimpan data customer.
Menyimpan data produk dan jasa.
Mengelola harga modal dan harga jual.
Membuat quotation.
Menghitung HPP, profit, dan margin.
Menyimpan draft quotation.
Menyimpan revisi quotation.
Menghasilkan quotation dalam bentuk PDF.
Mengubah quotation yang disetujui menjadi project.
Mengelola kebutuhan pembelian project.
Mencatat invoice dan pembayaran.
Mencatat pengeluaran.
Mencatat pekerjaan maintenance.
Menampilkan ringkasan kondisi bisnis melalui dashboard.
3. Teknologi
Backend

Python + FastAPI

Python digunakan sebagai bahasa utama untuk:

Business logic
Perhitungan quotation
HPP
Margin
API
PDF generation
Authentication/authorization logic
Database

PostgreSQL

Database dapat menggunakan Supabase PostgreSQL.

Storage

Supabase Storage digunakan untuk:

File PDF quotation
Foto pekerjaan
Dokumen invoice
Dokumen project

Database hanya menyimpan informasi/referensi file, bukan file secara langsung.

Frontend

Untuk tahap awal:

HTML
CSS
JavaScript
Jinja2

Tidak perlu menggunakan frontend framework yang kompleks terlebih dahulu.

Jika aplikasi berkembang besar, frontend dapat dikembangkan kemudian.

Version Control

Git + GitHub

Deployment

Backend dapat dideploy pada platform yang mendukung Python/FastAPI.

Database tetap menggunakan PostgreSQL/Supabase.

4. Prinsip Pengembangan

Aplikasi harus mengikuti prinsip:

Simple
   ↓
Clean
   ↓
Modular
   ↓
Easy to Maintain
   ↓
Easy to Expand

Hindari:

Satu file Python terlalu besar.
Logic database bercampur dengan tampilan.
Perhitungan quotation ditulis langsung di HTML.
Duplikasi kode.
Database terlalu kompleks.
Fitur yang belum diperlukan.

Setiap bagian aplikasi harus memiliki fungsi yang jelas.

5. Struktur Program

Struktur utama:

alanka/
│
├── app/
│   ├── main.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── quotation.py
│   │   ├── project.py
│   │   ├── purchase.py
│   │   ├── invoice.py
│   │   ├── payment.py
│   │   ├── expense.py
│   │   └── maintenance.py
│   │
│   ├── schemas/
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── quotation.py
│   │   ├── project.py
│   │   └── finance.py
│   │
│   ├── routes/
│   │   ├── dashboard.py
│   │   ├── customers.py
│   │   ├── products.py
│   │   ├── quotations.py
│   │   ├── projects.py
│   │   ├── purchases.py
│   │   ├── invoices.py
│   │   ├── finance.py
│   │   └── maintenance.py
│   │
│   ├── services/
│   │   ├── quotation_service.py
│   │   ├── calculation_service.py
│   │   ├── pdf_service.py
│   │   └── finance_service.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── customers/
│   │   ├── products/
│   │   ├── quotations/
│   │   ├── projects/
│   │   ├── purchases/
│   │   ├── invoices/
│   │   ├── finance/
│   │   └── maintenance/
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
├── database/
│   ├── migrations/
│   └── seed.sql
│
├── tests/
│
├── .env
├── .env.example
├── requirements.txt
├── README.md
└── .gitignore
6. Database

Database dibuat sederhana dan hanya menggunakan tabel inti.

users
roles

customers

products

quotations
quotation_items
quotation_versions

projects

purchases
purchase_items

invoices
payments

expenses

maintenance

Total sekitar 15 tabel utama.

7. Relasi Data Utama

Struktur hubungan:

CUSTOMER
   │
   ├──────── QUOTATION
   │              │
   │              └── QUOTATION_ITEMS
   │
   └──────── PROJECT
                  │
                  ├── PURCHASE
                  │       └── PURCHASE_ITEMS
                  │
                  ├── INVOICE
                  │       └── PAYMENT
                  │
                  └── MAINTENANCE

Produk digunakan oleh:

PRODUCT
   │
   ├── QUOTATION_ITEM
   │
   └── PURCHASE_ITEM
8. User dan Role

Sistem memiliki dua role utama:

Owner / Teknisi

Dapat:

Melihat seluruh data.
Mengelola produk.
Mengelola harga modal.
Mengelola harga jual.
Membuat quotation.
Melihat HPP.
Melihat margin.
Mengelola project.
Mengelola pembelian.
Mengelola maintenance.
Melihat laporan keuangan.
Admin / Finance

Dapat:

Mengelola customer.
Mengelola quotation.
Mengelola invoice.
Mencatat pembayaran.
Mencatat pengeluaran.
Melihat data project.
Mengelola administrasi.

Permission tidak perlu dibuat terlalu kompleks pada versi pertama.

9. Modul Customer

Data:

customers
├── id
├── name
├── phone
├── email
├── address
├── customer_type
├── notes
└── created_at

Customer type:

Pribadi
Perusahaan
Restaurant
Villa
Hotel
Toko
Lainnya

Fitur:

Tambah customer.
Edit customer.
Hapus/nonaktifkan customer.
Cari customer.
Lihat riwayat quotation.
Lihat riwayat project.
Lihat invoice.
Lihat maintenance.
10. Modul Produk & Jasa

Produk dan jasa menggunakan satu sistem master.

Data:

products
├── id
├── code
├── name
├── type
├── category
├── unit
├── cost_price
├── selling_price
├── stock
├── supplier
├── is_active
└── created_at

Type:

product
service

Contoh produk:

CCTV EZVIZ H6C Pro 3MP
CCTV EZVIZ H8C Pro 4MP
Kabel UTP Cat6
Switch PoE
Router
Access Point
Harddisk CCTV

Contoh jasa:

Instalasi CCTV
Instalasi LAN
Konfigurasi Router
Maintenance CCTV
Maintenance Network
Penarikan Kabel
11. Modul Quotation

Quotation merupakan modul utama aplikasi.

Alur:

Customer
   ↓
Create Quotation
   ↓
Tambah Produk/Jasa
   ↓
Hitung HPP
   ↓
Hitung Profit
   ↓
Hitung Margin
   ↓
Simpan Draft
   ↓
Revisi jika diperlukan
   ↓
Generate PDF
   ↓
Kirim Customer
   ↓
Approved

Quotation memiliki status:

Draft
Sent
Negotiation
Approved
Rejected
Expired
Cancelled
12. Perhitungan Quotation

Setiap quotation item menyimpan:

product_id
quantity
cost_price
selling_price
discount
subtotal
hpp

Rumus dasar:

Subtotal = Qty × Harga Jual

Total HPP = Qty × Harga Modal

Profit = Total Penjualan - Total HPP

Margin % = Profit / Total Penjualan × 100

Diskon dan pajak dapat ditambahkan sesuai kebutuhan.

Perhitungan dilakukan di backend Python, bukan di frontend saja.

13. Draft dan Revisi

Draft tidak membuat versi baru setiap kali autosave.

Contoh:

Draft
   ↓
Edit
   ↓
Autosave
   ↓
Edit
   ↓
Autosave

Tetap satu draft.

Jika user memilih:

Save as Revision

maka dibuat:

Revision 1
Revision 2
Revision 3

Versi lama tidak boleh berubah.

Setiap revision menyimpan snapshot:

Produk
Quantity
Harga modal
Harga jual
Diskon
HPP
Profit
Margin
Total

Dengan demikian quotation lama tetap memiliki data harga pada saat quotation tersebut dibuat.

14. PDF Quotation

Sistem dapat membuat PDF quotation berdasarkan data quotation.

PDF minimal berisi:

Logo / Nama Usaha

Nomor Quotation
Tanggal

Customer
Alamat
Kontak

Daftar Produk/Jasa

Qty
Harga
Subtotal

Diskon
Pajak
Grand Total

Catatan
Syarat & Ketentuan

Nama Penanggung Jawab

File PDF dapat disimpan ke Supabase Storage jika diperlukan.

15. Modul Project

Quotation yang disetujui dapat dibuat menjadi project.

Quotation
    ↓
Approved
    ↓
Create Project

Data:

projects
├── id
├── customer_id
├── quotation_id
├── name
├── location
├── status
├── start_date
├── target_date
├── total_value
├── notes
└── created_at

Status:

Planning
Procurement
Installation
Testing
Completed
Cancelled
16. Modul Pembelian

Digunakan untuk membeli kebutuhan project.

Alur:

Project
   ↓
Purchase
   ↓
Supplier
   ↓
Barang
   ↓
Received

Data purchase:

purchases
├── id
├── project_id
├── supplier
├── purchase_date
├── total
├── status
└── notes

Item:

purchase_items
├── purchase_id
├── product_id
├── quantity
├── price
└── subtotal

Status:

Draft
Ordered
Received
Cancelled
17. Modul Invoice

Invoice dibuat berdasarkan project/quotation.

Data:

invoices
├── id
├── customer_id
├── project_id
├── invoice_number
├── invoice_date
├── due_date
├── total
├── status
└── notes

Status:

Draft
Issued
Partially Paid
Paid
Overdue
Cancelled
18. Modul Payment

Mencatat pembayaran customer.

payments
├── id
├── invoice_id
├── payment_date
├── amount
├── payment_method
└── notes

Payment method:

Cash
Transfer
Other

Sistem menghitung:

Invoice
- Total Payment
= Outstanding
19. Modul Pengeluaran

Digunakan untuk mencatat pengeluaran usaha.

Contoh:

Pembelian barang
Transportasi
Bensin
Operasional
Tools
Internet
Administrasi
Lainnya

Data:

expenses
├── id
├── project_id
├── category
├── amount
├── expense_date
├── description
└── notes
20. Modul Maintenance

Untuk pekerjaan setelah project selesai.

Data:

maintenance
├── id
├── customer_id
├── project_id
├── maintenance_date
├── type
├── status
├── cost
├── notes
└── created_at

Status:

Scheduled
On Progress
Completed
Cancelled
21. Dashboard

Dashboard menjadi ringkasan seluruh sistem.

Informasi:

Total Quotation
Quotation Aktif
Project Berjalan
Project Selesai
Total Omzet
Total Pengeluaran
Piutang
Estimasi Profit

Contoh:

OMZET
Rp25.000.000

PENGELUARAN
Rp12.000.000

GROSS PROFIT
Rp13.000.000

PIUTANG
Rp5.000.000

Dashboard tidak memiliki database khusus. Data diambil dari modul yang sudah ada.

22. Alur Bisnis Utama

Alur aplikasi secara keseluruhan:

CUSTOMER
   │
   ↓
QUOTATION
   │
   ├── Draft
   ├── Revision
   ├── Sent
   └── Approved
          │
          ↓
       PROJECT
          │
          ├── Procurement
          │
          ├── Installation
          │
          └── Completed
                 │
                 ↓
              INVOICE
                 │
                 ↓
              PAYMENT

Maintenance:

PROJECT COMPLETED
       ↓
   MAINTENANCE
23. Struktur Logic Backend

Business logic harus dipisahkan dari route.

Contoh:

routes/quotations.py
        ↓
quotation_service.py
        ↓
calculation_service.py
        ↓
database

Contoh fungsi:

create_quotation()
calculate_quotation()
calculate_hpp()
calculate_profit()
calculate_margin()
save_draft()
create_revision()
generate_pdf()

Dengan demikian kode lebih mudah dipelihara.

24. Security

Minimal:

Authentication.
Password tidak disimpan dalam plaintext.
Environment variable untuk credential.
Database menggunakan permission/RLS jika menggunakan Supabase.
Validasi input backend.
Role-based access.
File upload dibatasi.
Jangan menyimpan API key/credential di GitHub.

File .env tidak boleh masuk GitHub.

25. Database Migration

Semua perubahan database disimpan dalam:

database/migrations/

Contoh:

001_initial_schema.sql
002_add_quotation.sql
003_add_project.sql
004_add_finance.sql

Jangan mengubah struktur database production secara sembarangan melalui SQL manual.

26. GitHub Workflow

Gunakan:

main
development
feature/*

Workflow:

Develop
   ↓
feature branch
   ↓
Testing
   ↓
development
   ↓
Final testing
   ↓
main
27. Tahapan Pembangunan

Jangan membuat seluruh sistem sekaligus.

Tahap 1 — Foundation
Project Python
FastAPI
Database connection
Environment configuration
Basic authentication
Folder structure
Tahap 2 — Master Data
Customer
Product
Service
Category
Tahap 3 — Quotation
Create quotation
Add item
HPP
Profit
Margin
Discount
Draft
Autosave
Revision
Tahap 4 — PDF
Template quotation
Generate PDF
Download PDF
Storage
Tahap 5 — Project
Convert quotation → project
Project status
Project information
Tahap 6 — Purchasing
Purchase
Purchase item
Supplier
Status purchase
Tahap 7 — Finance
Invoice
Payment
Expense
Outstanding
Tahap 8 — Maintenance
Maintenance record
Maintenance status
Customer history
Tahap 9 — Dashboard
Omzet
Pengeluaran
Profit
Piutang
Quotation
Project
28. Fitur yang Tidak Dibuat di Versi Awal

Untuk menjaga aplikasi tetap sederhana, fitur berikut ditunda:

CRM kompleks
Lead automation
Notification system
Multi-company
Multi-warehouse
Advanced inventory
Accounting lengkap
Advanced analytics
Approval bertingkat
Task management kompleks
Mobile application
WhatsApp automation
Email automation
AI quotation

Fitur tersebut dapat ditambahkan setelah sistem dasar stabil.

29. Target MVP

Versi pertama dianggap selesai jika pengguna sudah dapat melakukan:

Login
  ↓
Tambah Customer
  ↓
Tambah Produk
  ↓
Buat Quotation
  ↓
Tambah Item
  ↓
Hitung HPP
  ↓
Hitung Profit & Margin
  ↓
Simpan Draft
  ↓
Buat Revision
  ↓
Generate PDF
  ↓
Approved
  ↓
Create Project
  ↓
Catat Pembelian
  ↓
Buat Invoice
  ↓
Catat Payment
  ↓
Catat Expense
  ↓
Lihat Dashboard
30. Prinsip Penting untuk AI Coding

Jika aplikasi dibangun menggunakan AI coding assistant seperti Antigravity, AI harus mengikuti aturan:

Jangan membuat file baru jika fungsi tersebut sudah tersedia.
Jangan membuat tabel database baru tanpa alasan yang jelas.
Jangan menggabungkan seluruh logic ke satu file.
Business logic harus berada di services.
Database model harus berada di models.
API route harus berada di routes.
Validasi request berada di schemas.
Tampilan berada di templates.
CSS dan JavaScript berada di static.
Database migration harus tersimpan di GitHub.
Jangan menghapus data production saat melakukan development.
Jangan mengubah struktur database tanpa migration.
Jangan menyimpan credential di source code.
Gunakan nama file dan fungsi yang konsisten.
Setiap fitur baru harus mengikuti struktur folder yang sudah ada.
31. Prinsip Data Quotation

Ini salah satu bagian terpenting dari sistem.

Harga master dapat berubah:

Harga Modal Produk
Rp500.000
      ↓
berubah menjadi
Rp550.000

Tetapi quotation lama tidak boleh ikut berubah.

Contoh:

Quotation #001

Harga Modal saat dibuat:
Rp500.000

Harga Jual:
Rp750.000

Walaupun master product kemudian menjadi:

Harga Modal:
Rp550.000

Quotation #001 tetap:

HPP = Rp500.000
Harga Jual = Rp750.000

Karena quotation menyimpan snapshot harga saat transaksi dibuat.

32. Prinsip Akhir Sistem

Aplikasi ini tidak ditujukan menjadi ERP besar.

Fokusnya adalah:

CUSTOMER
   ↓
QUOTATION
   ↓
PROJECT
   ↓
PURCHASE
   ↓
INVOICE
   ↓
PAYMENT
   ↓
FINANCE
   ↓
MAINTENANCE

Dengan Python sebagai backend utama dan PostgreSQL sebagai database.

Prioritas utama:

1. Struktur kode rapi
2. Database sederhana
3. Data aman
4. Perhitungan akurat
5. Mudah digunakan
6. Mudah dikembangkan
7. Mudah diperbaiki