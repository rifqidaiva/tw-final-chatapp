# Tugas Akhir Teknologi Web

## Setup dan Menjalankan Proyek

Ikuti langkah-langkah berikut untuk mengatur dan menjalankan proyek ini:

1. **Clone Repository**

   Clone repository ini ke komputer Anda menggunakan perintah berikut:

   ```bash
   git clone <URL_REPOSITORY>
   ```

   Gantilah `<URL_REPOSITORY>` dengan URL repository proyek ini.

2. **Masuk ke Direktori Proyek**

   Pindah ke direktori proyek yang telah di-clone:

   ```bash
   cd tw-final-chatapp
   ```

3. **Buat Virtual Environment**

   Buat virtual environment untuk mengisolasi dependensi proyek:

   ```bash
   python -m venv venv
   ```

4. **Aktifkan Virtual Environment**

   Aktifkan virtual environment:

   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies**

   Install semua dependensi yang diperlukan dari file `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

6. **Jalankan Aplikasi**

   Jalankan aplikasi dengan perintah berikut:

   ```bash
   python app.py
   ```

7. **Akses Aplikasi**

   Buka browser Anda dan akses aplikasi melalui URL:

   ```
   http://127.0.0.1:5000
   ```

   Gantilah port `5000` jika aplikasi menggunakan port yang berbeda.

8. **Nonaktifkan Virtual Environment**

   Setelah selesai menggunakan aplikasi, Anda dapat menonaktifkan virtual environment dengan perintah:

   ```bash
   deactivate
   ```
