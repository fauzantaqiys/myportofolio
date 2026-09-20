# Laporan Tugas

## Tugas 1

### 1. Apakah kamu menggunakan elemen HTML5 semantik untuk bagian Experience? Mengapa elemen tersebut dipilih dan bagaimana elemen tersebut meningkatkan struktur serta aksesibilitas halaman web kamu?

Ya, saya menggunakan elemen semantik seperti `<section>` untuk memisahkan bagian experience dari bagian profile/hero secara jelas. Saya juga menggunakan tag `<time>` dengan atribut `datetime` untuk bagian tanggal rentang pengalaman. Elemen `<section>` membantu menstrukturkan halaman web agar lebih rapi dan mudah dibaca oleh mesin pencari, sedangkan penggunaan tag `<time>` membuat struktur tanggal jadi jauh lebih akurat dan ramah *screen reader* untuk meningkatkan aksesibilitas bagi pengguna disabilitas.

### 2. Jelaskan proses penentuan desain CSS untuk bagian Experience! Masalah apa yang kamu hadapi saat mengatur tata letak (misalnya, alignment, responsivitas, atau kerapihan), dan bagaimana kamu menyelesaikannya?

Saya ingin membuat bagian experience ini punya tampilan *ocean-blue theme* yang rapi dengan bentuk kartu linimasa (timeline). Dalam setiap kartu, saya memasukkan judul posisi, nama organisasi, tanggal, dan logo organisasi.

Masalah yang sempat muncul adalah saat mengatur tata letak kartu agar tetap rapi saat ukuran layar mengecil (mode mobile). Kalau di desktop kartunya sejajar ke samping (flexbox/grid dengan logo di kanan), di layar HP tampilannya jadi terlalu sempit dan teksnya terhimpit. Masalah ini saya selesaikan dengan menambahkan `@media (max-width: 600px)` pada CSS, jadi di layar HP tata letaknya otomatis berubah menjadi *single column* (satu kolom ke bawah) agar gambar dan teksnya tidak keluar garis dan tetap enak dibaca.

### 3. Mengapa aplikasi web berbasis Django dapat disebut sebagai situs web statis ketika hanya menyajikan HTML, CSS, dan aset gambar tanpa melibatkan database, form, atau dynamic rendering? Sebutkan kelebihan dan keterbatasan pendekatan ini!

Aplikasi web Django ini disebut statis karena setiap kali ada yang mengakses URL-nya, server hanya langsung mengirimkan file HTML, CSS, dan gambar yang sudah "jadi" dan tersimpan di folder `static` atau `templates`, tanpa ada proses ambil data dari database (seperti `models.py`) atau manipulasi data berdasarkan input pengguna.

- **Kelebihan:** proses load halaman jadi super cepat, hemat memori server, dan sangat aman karena tidak ada celah serangan database (seperti SQL Injection).
- **Keterbatasan:** kodenya tidak fleksibel. Kalau saya mau menambah pengalaman atau mengubah data diri, saya harus edit manual berkas `.html`-nya secara langsung lalu melakukan commit dan deploy ulang, bukan tinggal isi form dari sistem.

### AI Disclosure & Reflection

Penggunaan AI (Gemini) dalam pengerjaan Tugas 1 ini diterapkan secara transparan sebagai asisten diskusi (*thought partner*), alat verifikasi, pembantu *troubleshoot*, serta untuk penulisan kode.

**1. Strategi Prompting & Peran AI**

- **Pengecekan Aksesibilitas & Semantik:** Berkonsultasi mengenai kelayakan struktur HTML dan penggunaan tag semantik `<time>` untuk nilai maksimal pada rubrik.
- **Troubleshooting Environment & Git:** Berdiskusi saat mengalami kendala eksekusi terminal PowerShell serta penanganan alur commit Git bertahap.
- **Eksplorasi CSS Layouting:** Mendiskusikan pendekatan `@media` query dan Flexbox/Grid untuk mengatasi masalah tampilan responsive card pada mode mobile.
- **Penyusunan Kode:** Memanfaatkan Generative AI untuk membantu menuliskan draf awal struktur kode HTML dan CSS, yang kemudian saya sesuaikan, sempurnakan, dan uji secara mandiri agar sesuai dengan kebutuhan tampilan portofolio serta kriteria tugas.

---

## Tugas 2

### 1. Alur MVT pada Halaman Baru

- **`urls.py` proyek & aplikasi:** Saat pengguna mengakses URL, permintaan pertama kali diterima oleh `urls.py` proyek yang akan meneruskannya ke `urls.py` aplikasi (`main`) untuk mencocokkan path.
- **View & Model:** Rute tersebut memanggil fungsi di `view`. `View` bertugas mengambil data ketertarikanmu dari `model` di basis data, lalu membungkusnya ke dalam *context*.
- **Template:** `View` mengirimkan *context* tersebut ke `template` (HTML), yang kemudian memproses perulangan data dan merendernya menjadi tampilan utuh di browser.

### 2. Alasan Data Disimpan di Model

Menyimpan data pada `model` memisahkan antara logika data dengan antarmuka, sehingga data tidak ditulis langsung (*hard-coded*) di dalam `template`. Dampaknya, kode menjadi lebih terstruktur, *reusable*, dan *scalable*. Pemeliharaan pun jauh lebih mudah karena kamu bisa menambah atau mengubah data portofolio kapan saja melalui basis data tanpa perlu menyentuh atau merusak kode HTML.

### 3. Perbedaan `makemigrations` dan `migrate`

- **`makemigrations`:** Perintah ini bertugas mendeteksi perubahan pada kode modelmu dan mencatatnya ke dalam sebuah berkas migrasi baru (sebagai instruksi).
- **`migrate`:** Perintah ini bertugas menerapkan atau mengeksekusi instruksi dari berkas migrasi tersebut ke dalam struktur basis data secara nyata.

**Contoh:** Kedua perintah ini wajib dijalankan ketika kamu baru saja membuat model `Interest` baru atau ketika kamu menambahkan field baru di dalamnya.

### AI Disclosure & Reflection

Dalam pengerjaan Tugas 2 ini, saya menggunakan bantuan AI (Gemini) sebagai rekan diskusi dan *debugging*. Strategi prompting yang saya lakukan adalah memberikan potongan kode progres saya untuk divalidasi konsepnya secara bertahap (Model, View, Template, hingga Unit Test). AI tidak memberikan kode mentah, melainkan membantu mengidentifikasi typo, menjelaskan alur migrasi Git, serta menemukan bug visual pada CSS yang diakibatkan oleh perbedaan huruf besar/kecil (*case-sensitive*). Pemecahan masalah dan penulisan kode tetap saya lakukan secara mandiri berdasarkan petunjuk dari AI dan modul tutorial.

**Chat log AI:** https://share.gemini.google/F7GtKP5Yawpd

---

## Tugas 3

### 1. Mengapa menggunakan ModelForm pada Django alih-alih membuat form HTML manual, dan mengapa `{% csrf_token %}` diwajibkan?

**Keunggulan ModelForm:** ModelForm adalah library bawaan Django yang berfungsi membuat *boilerplate* form secara otomatis berdasarkan struktur field yang sudah didefinisikan pada model. Dengan menggunakan kelas `Meta` (seperti `model = Project` dan penetapan `fields`), Django otomatis memetakan tipe data ke elemen HTML yang tepat (misalnya teks menjadi `TextInput` atau relasi menjadi dropdown). Hal ini mengeliminasi penulisan tag HTML manual yang repetitif, meminimalisasi error, dan secara otomatis menangani validasi serta penyimpanan data ke basis data cukup dengan perintah `form.save()`.

**Kewajiban `{% csrf_token %}`:** Token CSRF (*Cross-Site Request Forgery*) adalah token rahasia unik yang di-generate oleh server untuk melindungi aplikasi dari request palsu yang tidak terotorisasi. Penambahan tag ini diwajibkan oleh Django pada setiap form metode POST untuk mencegah peretas mencegat atau memanipulasi request dari pengguna yang terautentikasi dan mengirimkan data berbahaya ke server.

### 2. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?

Meskipun JSON dan XML sama-sama format teks murni yang *self-describing* dan *platform-independent*, JSON jauh lebih disukai saat ini, terutama pada arsitektur API modern, karena beberapa alasan utama:

- **Ukuran lebih ringkas:** XML mewajibkan *closing tag* (tag penutup) untuk setiap elemen data, yang membuat ukuran file-nya lebih besar (berat) untuk ditransmisikan. JSON menggunakan sintaks kurung kurawal berbasis *key-value* yang jauh lebih padat.
- **Performa dan integrasi:** Karena JSON diturunkan dari notasi objek JavaScript, format ini berintegrasi secara natural dan langsung dikenali oleh ekosistem frontend berbasis JavaScript. Selain itu, kecepatan *parsing* JSON oleh mesin jauh lebih tinggi dibandingkan XML.

### 3. Jelaskan alur view yang mengembalikan JSON dan pentingnya proses serialization!

**Alur HTTP Request-Response:** Saat client meminta data (misal mengakses URL `/api/projects/`), rute `urls.py` akan memanggil fungsi view yang bersesuaian. View kemudian mengambil data dari basis data melalui model (contoh: `Project.objects.all()`). Data yang masih berupa kumpulan objek Python ini kemudian diubah menjadi format JSON menggunakan `serializers.serialize("json", ...)`. Terakhir, view membungkus data JSON tersebut ke dalam `HttpResponse` dengan header `content_type="application/json"` untuk dikembalikan ke peramban atau klien.

**Mengapa butuh serialization:** *Serialization* adalah proses mengubah objek data kompleks (seperti `QuerySet` spesifik milik Python/Django) menjadi format teks dasar. Proses ini mutlak diperlukan karena protokol HTTP standar yang digunakan server untuk berkomunikasi dengan client hanya dapat mengirimkan dan menerima format teks dasar (seperti JSON atau XML), bukan objek bahasa pemrograman spesifik.

### AI Disclosure & Reflection

Dalam pengerjaan Tugas 3 ini, saya menggunakan bantuan AI (Gemini) sebagai rekan diskusi, *debugging*, dan asisten penulisan kode. Strategi prompting yang saya lakukan adalah memberikan potongan kode progres saya untuk dievaluasi secara bertahap (terkait form pencarian, struktur template, dan styling). AI memberikan beberapa draf kode mentah (seperti penyempurnaan `base.html`, penambahan rute pada form ber-method GET, serta restrukturisasi keseluruhan file CSS agar tidak redundan), yang kemudian saya tinjau, pelajari, dan integrasikan ke dalam proyek. Selain itu, AI membantu menelaah cara kerja komponen native HTML5 `popover` untuk modal konfirmasi hapus data. Proses evaluasi dan penyelarasan akhir kode tetap saya lakukan secara mandiri berdasarkan hasil diskusi tersebut dan panduan dari modul tutorial.

**Detail strategi prompting & peran AI:**

- **Eksplorasi Komponen `django.forms`:** Mengidentifikasi kelas bawaan Django yang bisa diimpor, termasuk pemisahan peran antara Form Classes, Form Fields, dan Widgets (seperti `DateTimeInput`).
- **Implementasi Fitur Tanggal pada Form:** Membuat contoh awal form pemilih tanggal menggunakan `DateTimeField` dengan atribut widget `type: datetime-local` *native* HTML, serta menyematkan fungsi validasi silang (`clean()`).
- **Penyesuaian Skema Database (`models.py`):** Mengubah field `started_at` pada model `Experience` dengan menghapus `auto_now_add=True` dan menggantinya ke `default=timezone.now` agar nilainya bisa diinput secara manual melalui form.
- **Perbaikan Error Migrasi (Debugging Typo):** Menyelesaikan kendala `ImportError` saat menjalankan `makemigrations` akibat salah ketik komponen (`DataInput` yang seharusnya `DateTimeInput`) di dalam berkas `forms.py`.
- **Pemisahan Endpoint API Data (`views.py`):** Memecah fungsi pencarian data berbasis JSON dan XML menjadi fungsi spesifik per model (`show_json_interest`, `show_json_experience`, dsb.) agar data antarmodul tidak saling tertukar.
- **Sinkronisasi Jalur Routing (`urls.py`):** Memperbaiki jalur URL untuk mengakomodasi fungsi views terpisah, memperbaiki parameter pencarian UUID dari `interest_id` menjadi `experience_id`, serta membetulkan target fungsi hapus.
- **Penyusunan dan Tata Letak Template (`experience.html` & CSS):** Melengkapi halaman daftar pengalaman dengan fitur pencarian, tombol tambah data, visualisasi rentang waktu, dan integrasi modal hapus. AI membantu menemukan efisiensi dengan menggabungkan aturan CSS (`.experience-card, .interest-card`) agar tidak repetitif.
- **Integrasi Popover Konfirmasi Hapus Data:** Menelaah struktur komponen modal berbasis fitur *native* HTML5 `popover="auto"` yang dapat mengeksekusi fungsi *delete* dengan efisien tanpa ketergantungan *script* JavaScript tambahan.

**Chat log / referensi prompt:**

- https://share.gemini.google/dhy5nsoOBwts
- https://share.google/aimode/C8ykyD7AQfdmC34fQ