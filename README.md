# Responsi Disdec Sys

**Nama:** Muhammad Java Arifin  
**NIM:** 235410073  

####  RESPONSI PRAKTIKUM SISTEM TERDISTRIBUSI DAN TERDESENTRALISASI IF-1 Genap 2025

Repositori ini disusun sebagai bentuk pemenuhan tugas responsi untuk mata kuliah Sistem Terdistribusi dan Terdesentralisasi. Dokumentasi ini mencakup tiga bagian utama: implementasi basis data terdistribusi, pengembangan antarmuka pemrograman aplikasi (REST API), serta analisis mekanisme konsensus pada teknologi *blockchain*.

---

#### (CPMK 1: 20%) Dengan menggunakan Docker, jalankan YugabyteDB dan kemudian buat 2 tabel dengan nama bebas dan isi kolom bebas. Isikan masing-masing 5 data. Buktikan bahwa 2 tabel dibuat dan data juga telah diisikan. Anda bisa menggunakan ysqlsh atau YugabyteDB UI. 

#### Menjalankan YugabyteDB di Docker
Untuk menjalankan *node* tunggal YugabyteDB, saya menggunakan perintah Docker berikut:

    docker run -d --name yugabyte -p7000:7000 -p9000:9000 -p5433:5433 -p9042:9042 yugabytedb/yugabyte:latest bin/yugabyted start --daemon=false

![](Images/Screenshot%202026-07-08%20111728.png)

Masuk ke dalam Lingkungan Shell (ysqlsh):

    docker exec -it yugabyte bash
![](Images/Screenshot%202026-07-08%20112529.png)

Membuat Tabel dan Menyisipkan Data:
Dua tabel independen (buku dan anggota) dirancang untuk mendemonstrasikan penyimpanan data relasional. Masing-masing tabel disisipkan lima entri data.

    CREATE TABLE buku (id INT PRIMARY KEY, judul VARCHAR(100), penulis VARCHAR(100));
    INSERT INTO buku VALUES 
    (1, 'Bumi Manusia', 'Pramoedya Ananta Toer'), 
    (2, 'Laskar Pelangi', 'Andrea Hirata'), 
    (3, 'Cantik Itu Luka', 'Eka Kurniawan'), 
    (4, 'Pulang', 'Tere Liye'), 
    (5, 'Filosofi Teras', 'Henry Manampiring');

    
    CREATE TABLE anggota (id INT PRIMARY KEY, nama VARCHAR(100), kota VARCHAR(50));
    INSERT INTO anggota VALUES 
    (1, 'Budi', 'Jakarta'), 
    (2, 'Siti', 'Bandung'), 
    (3, 'Andi', 'Surabaya'), 
    (4, 'Rina', 'Yogyakarta'), 
    (5, 'Joko', 'Semarang');\

![](Images/Screenshot%202026-07-08%20112730.png)

Berikut adalah luaran dari sistem yang membuktikan bahwa kedua tabel berhasil dibuat dan terdistribusi di dalam basis data:

![](Images/Screenshot%202026-07-08%20112825.png)

#### (CPMK 2: 40%) Buatlah REST API menggunakan Python yang akan mengekspos data yang telah anda buat tersebut menggunakan Python. Hasil bisa diakses melalui browser atau headless tool (curl) dalam format JSON.

Langkah-langkah Menjalankan API
1. Menginstal Dependensi (Pustaka yang dibutuhkan):

        pip install -r requirements.txt

    ![](Images/Screenshot%202026-07-08%20114505.png)

2. Menjalankan Server Aplikasi (Flask):

        python app.py
    
    ![](Images/Screenshot%202026-07-08%20114655.png)

    ![](Images/Screenshot%202026-07-08%20115723.png)


Pengujian Headless Tool (cURL)

1. Pemanggilan Endpoint /api/buku

        curl http://localhost:5000/api/buku

    ![](Images/Screenshot%202026-07-08%20115639.png)

2. Pemanggilan Endpoint /api/anggota

        curl http://localhost:5000/api/anggota

    ![](Images/Screenshot%202026-07-08%20115512.png)
    

#### (CPMK 3: 40%) Pilihlah blockchain L1 selain Solana. Jelaskan mekanisme konsensus yang digunakan dan buat diagram mekanisme konsensus blockchain tersebut. 

analisis ini difokuskan pada jaringan Layer-1 Ethereum, yang kini sepenuhnya beroperasi menggunakan mekanisme konsensus Proof of Stake (PoS) pasca-pembaruan The Merge.

#### Pemahaman Mekanisme Proof of Stake (Gasper)

Mekanisme PoS pada Ethereum (Gasper) meninggalkan konsep penambangan komputasi berat (Proof of Work) dan menggantinya dengan model validasi berbasis aset kripto (staking). Proses konsensusnya berjalan melalui tahapan berikut:

1. Validator & Staking: Entitas yang ingin mengamankan jaringan harus mengunci (stake) minimal 32 ETH untuk mendapatkan hak sebagai Validator.

2. Manajemen Waktu (Slot & Epoch): Waktu jaringan dibagi menjadi blok-blok kecil yang disebut Slot (berdurasi 12 detik), dan kumpulan 32 slot membentuk satu siklus yang disebut Epoch.

3. Proposer Acak: Pada setiap awal slot, protokol secara pseudo-acak memilih satu validator untuk bertindak sebagai Proposer. Proposer bertugas menyusun transaksi dari mempool menjadi sebuah blok baru.

4. Komite Attestation: Sekelompok validator lain dipilih secara acak untuk membentuk komite. Tugas mereka adalah memverifikasi usulan blok dari proposer. Jika blok tersebut valid secara kriptografis dan logika, mereka memberikan suara persetujuan (Attestation).

5. Hukuman (Slashing): Apabila terdapat validator yang bertindak anomali (misalnya mencoba memvalidasi dua rantai berbeda), sistem akan mengeksekusi penalti finansial (slashing) dengan menyita ETH yang mereka pertaruhkan.

#### Diagram Alir (Sequence Diagram) Konsensus

Berikut adalah representasi visual dari interaksi antar-entitas dalam satu putaran slot pada mekanisme konsensus Ethereum PoS:


```mermaid
sequenceDiagram
    autonumber
    participant M as Mempool
    participant V as Pool Validator (Staked)
    participant P as Block Proposer
    participant C as Komite (Attesters)
    participant B as Rantai Blockchain

    Note over V,B: Awal Slot (Durasi: 12 Detik)
    V->>P: Protokol memilih 1 Validator acak (Proposer)
    V->>C: Protokol membentuk Komite Validator acak
    
    P->>M: Mengekstrak transaksi yang mengantre
    P->>P: Menyusun & memvalidasi Blok Baru
    P->>B: Mengusulkan (Propose) Blok ke jaringan
    
    B-->>C: Menyiarkan (Broadcast) Blok usulan
    C->>C: Audit validitas transaksi dan State
    
    alt Blok Dinyatakan Valid
        C->>B: Mengirimkan Attestation (Suara Persetujuan)
        Note over B: Jika mencapai kuorum (>2/3 suara), blok diterima
    else Blok Terindikasi Manipulatif
        C->>B: Menolak usulan blok
        B->>P: Mengeksekusi penalti Slashing pada Proposer
    end
