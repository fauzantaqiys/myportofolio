1. Apakah kamu menggunakan elemen HTML5 semantik untuk bagian Experience? Mengapa elemen tersebut dipilih dan bagaimana elemen tersebut meningkatkan struktur serta aksesibilitas halaman web kamu?

Ya, saya menggunakan elemen semantik seperti <section> untuk memisahkan bagian experience dari bagian profile/hero secara jelas. Saya juga menggunakan tag <time> dengan atribut datetime untuk bagian tanggal rentang pengalaman. Elemen <section> membantu menstrukturkan halaman web agar lebih rapi dan mudah dibaca oleh mesin pencari, sedangkan penggunaan tag <time> membuat struktur tanggal jadi jauh lebih akurat dan ramah screen reader untuk meningkatkan aksesibilitas bagi pengguna disabilitas.

2. Jelaskan proses penentuan desain CSS untuk bagian Experience! Masalah apa yang kamu hadapi saat mengatur tata letak (misalnya, alignment, responsivitas, atau kerapihan), dan bagaimana kamu menyelesaikannya?

Saya ingin membuat bagian experience ini punya tampilan ocean-blue theme yang rapi dengan bentuk kartu linimasa (timeline). Dalam setiap kartu, saya memasukkan judul posisi, nama organisasi, tanggal, dan logo organisasi. Masalah yang sempat muncul adalah saat mengatur tata letak kartu agar tetap rapi saat ukuran layar mengecil (mode mobile). Kalau di desktop kartunya sejajar ke samping (flexbox/grid dengan logo di kanan), di layar HP tampilannya jadi terlalu sempit dan teksnya terhimpit. Masalah ini saya selesaikan dengan menambahkan @media (max-width: 600px) pada CSS, jadi di layar HP tata letaknya otomatis berubah menjadi single column (satu kolom ke bawah) agar gambar dan teksnya tidak keluar garis dan tetap enak dibaca.

3. Mengapa aplikasi web berbasis Django dapat disebut sebagai situs web statis ketika hanya menyajikan HTML, CSS, dan aset gambar tanpa melibatkan database, form, atau dynamic rendering? Sebutkan kelebihan dan keterbatasan pendekatan ini!

Aplikasi web Django ini disebut statis karena setiap kali ada yang mengakses URL-nya, server hanya langsung mengirimkan file HTML, CSS, dan gambar yang sudah "jadi" dan tersimpan di folder static atau templates tanpa ada proses ambil data dari database (seperti models.py) atau manipulasi data berdasarkan input pengguna.

Kelebihannya adalah proses load halaman jadi super cepat, hemat memori server, dan sangat aman karena tidak ada celah serangan database (seperti SQL Injection). Keterbatasannya adalah kodenya tidak fleksibel—kalau saya mau menambah pengalaman atau mengubah data diri, saya harus edit manual berkas .html-nya secara langsung lalu melakukan commit dan deploy ulang, bukan tinggal isi form dari sistem.

AI Disclosure & Reflection
Penggunaan AI (Gemini) dalam pengerjaan Tugas 1 ini diterapkan secara transparan sebagai asisten diskusi (thought partner), alat verifikasi, pembantu troubleshoot, serta untuk penulisan kode.

1. Strategi Prompting & Peran AI
Pengecekan Aksesibilitas & Semantik: Berkonsultasi mengenai kelayakan struktur HTML dan penggunaan tag semantik <time> untuk nilai maksimal pada rubrik.

2. Troubleshooting Environment & Git: Berdiskusi saat mengalami kendala eksekusi terminal PowerShell serta penanganan alur commit Git bertahap.

3. Eksplorasi CSS Layouting: Mendiskusikan pendekatan @media query dan Flexbox/Grid untuk mengatasi masalah tampilan responsive card pada mode mobile.

4. Penyusunan Kode: Memanfaatkan Generative AI untuk membantu menuliskan draf awal struktur kode HTML dan CSS, yang kemudian saya sesuaikan, sempurnakan, dan uji secara mandiri agar sesuai dengan kebutuhan tampilan portofolio serta kriteria tugas.