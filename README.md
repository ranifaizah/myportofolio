Nama : Rani Faizah A

NPM : 2506624013

Kelas : PBP D


### Tugas 1

1. Iya, pada tugas dan tutorial ini saya menggunakan beberapa elemen semantik HTML 5 seperti <header>,<nav>,<main>,<section> , dan <footer>,  meskipun saya belum sempat menggunakan <article> atau <aside> sejauh ini elemen semantik HTML5 yang telah saya gunakantelah membantu saya dalam keterbacaan struktur kode sehingga saya bisa tahu uang mana profile,skills,dan experience tanpa perlu merauh comment satu-satu untuk menandakannya. Kalau dari segi aksesisbilitas browser jadinya bisa lebih paham struktur kode saya mulai dari konten utama yang mana, navigasi yang mana, dan footer yang mana sudah bisa diketahui tanpa harus menebak.

2. Tantangan tata letak yang saya temukan adalah ketika mengubah tampilan desktop ke mobile, terutama agar menjaganya tetap responsive karena, dari tutorial kita menggunakan CSS grid 2 kolom. Namun, kalau di pindah di mobile akan jadi sempit sehingga saya menemukan solusinya lewat membaca ulang kode di mana saya menemukan query @media, ternyata query tersebut mengubah total grid nya menjadi 1 kolom vertikal. Untuk mengevaluasi elemen mana yang perlu di prioritaskan saya mencari elemen mana yang paling butuh ruang horizontal dan elemen mana yang masih bisa menyempit sendiri. Ada juga beberappa elemen seperti .skills-grid dan .experience-list yang menggunakan flexbox dengan flexwrap sehingga ototmatis bisa menyesuaikan jumlah kolom tanpa perlu query khusus.

3. Batasan yang terasa adalah bahwa saya diharuskan menyajikan informasi secara ringkas dan lengkap karena semua konten akan langsung tampil tanpa perlu interaksi dari user. Jadi, untuk ke depannya saya ingin mencoba menambahkan fungsionalitas dinamis seperti expand/collapse atau menambahkan integrasi desain yang lebih lucu dari figma.

Ai disclosure: menggunakan AI untuk dokumentasi kode yang belum saya pahami dari tutorial 1 serta meminta bantuan untuk memahami elemen-elemen dan fungsionalitas dari kode css yang terdapat pada tutorial 1.
refrensi untuk membangun dan menyelesaikan tugas 1 kebanyakan saya ambil dari video youtube dan tampilan dari pinterest 

### Tugas 2

1. Ketika seorang pengguna membuka halaman portofolio baru di browser, Django memproses permintaan tersebut melalui arsitektur MVT (Model-View-Template) dengan alur kerja berikut:
 - Pertama browser mengirim request ketika pengguna mengetik link menuju http://localhost:8000/skills/. Browser kemudian akan mengirim request ke Django yang sedang berjalan 
 - urls.py proyek menerima dan meneruskan request
Django pertama-tama mengecek urls.py di level proyek, perannya bertindak sebagai direktori pusat routing proyek dan melakukan proses include('main.urls') sehingga kalau URL yang diminta cocok dengan pattern kosong (''), Django akan lanjut mencocokkan sisa URL-nya (skills/) ke dalam urls.py milik app main. Jadi peran urls.py proyek adalah sebagai router utama yang mendelegasikan request ke app yang sesuai. 
- App urls.py berperan untuk menentukan endpoint atau sub-halaman spesifik di dalam modul aplikasi terkait. Dalam prosesnya urls.py di level aplikasi (app/urls.py) akan menerima request yang diteruskan dari proyek, lalu mencocokkan sisa path (misalnya "show_skills/"). Ketika pola cocok, Django mengarahkan request tersebut ke fungsi atau kelas view yang telah ditentukan.
- View menjadi otak yang menjembatani data dan tampilan. Dia akan menerima request , memproses logika apa pun yang diperlukan (seperti otentikasi atau pemfilteran), lalu memanggil model untuk mengambil data portofolio dari data base.
- Model berinteraksi langsung dengan basis data melalui sistem ORM (Object-Relational Mapping) Django.Model menerjemahkan perintah dari view menjadi kueri SQL untuk mengambil data portofolio (seperti judul proyek, deskripsi, teknologi yang digunakan, dan tautan gambar) dari tabel database, lalu mengembalikan data tersebut ke view.
- Template merender html. render(request, 'skills.html', context) memanggil Django Template Engine, yang membaca file skills.html, lalu mengganti tag-tag templat ({{ skill.name }}, {% for %}, dll) dengan data asli dari context. Peran template adalah presentasi — mengubah data mentah jadi markup HTML yang bisa ditampilkan browser, termasuk menangani kondisi kosong lewat {% empty %}.
- Respons HTTP ke Browser: Hasil rendering (HTML lengkap) dibungkus jadi HTTP response oleh Django, dikirim balik ke browser. Browser menerima HTML tersebut, memparsingnya, memuat CSS/font/asset terkait, dan menampilkan halaman jadi ke pengguna.

2. Kalau data skill/experience ditulis langsung di HTML (misal <li>Python</li>, <li>Django</li> ditulis manual satu-satu di skills.html), ini menimbulkan beberapa masalah seperti: 
- Pemisahan Logika Data dan Presentasi. Template (HTML) seharusnya hanya bertanggung jawab untuk menampilkan antarmuka pengguna (presentation layer), sedangkan Model bertanggung jawab atas struktur data (data layer). Jika data portofolio ditulis langsung di dalam template, kode HTML akan tercampur dengan konten statis yang kaku. Hal ni melanggar prinsip dasar arsitektur MVT (Model-View-Template) yang dianut Django, di mana tiap layer harusnya independen dan bisa diganti tanpa mengganggu layer lain.
- Sulit di-maintain saat data berubah. Misalnya, salah satu skill berubah dari "intermediate" ke "advanced". Kalau hardcode di HTML, kita harus buka file template, cari baris yang tepat, edit manual, lalu deploy ulang. Kalau datanya ada di model (database), bisa di update lewat Django admin atau shell.
- Tidak scalable. Jika data ditulis langsung di template, aplikasi akan sangat sulit dikembangkan jika jumlah proyek bertambah banyak. Setiap kali ada portofolio baru, pengembang harus menulis ulang elemen HTML secara manual. Dengan model, penambahan ratusan proyek baru dapat ditangani secara otomatis oleh satu blok kode template yang sama melalui perulangan (looping).
- Tidak bisa dimanipulasi secara dinamis, Kalau data ada di model, kita bisa melakukan filtering, sorting, atau searching lewat ORM (Skill.objects.filter(category='programming'), .order_by('-added_at'), dll). Kalau hardcode di HTML, semua kemampuan ini hilang dan data menjadi statis, tidak bisa difilter berdasarkan input pengguna, tidak bisa diurutkan secara dinamis.
- Rawan duplikasi dan inkonsistensi, kalau ada dua halaman yang menampilkan data yang sama (misal skill muncul di halaman utama dan halaman skills terpisah), hardcode berarti data yang sama ditulis dua kali di dua file berbeda. Kalau salah satu diupdate tapi yang lain lupa, terjadi inkonsistensi. Dengan model sebagai satu sumber data (single source of truth), semua halaman yang 

3. Makemigrations berfungsi untuk menerjemahkan perubahan kode pada file models.py menjadi file cetak biru (migration file), sedangkan migrate berfungsi untuk mengeksekusi cetak biru tersebut agar perubahan struktur diterapkan secara nyata ke dalam basis data.

Contoh Kasus yang Mengharuskan Keduanya

Misalnya  ingin menambah field baru years_of_experience ke model Skill:
class Skill(models.Model):
    ...
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='intermediate')
    years_of_experience = models.PositiveIntegerField(default=0)   # <-- field baru
    icon = models.URLField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

setelah membuat kode tersebut langkah pertama yang harus dilakukan adalah menjalankan
python manage.py makemigrations main
Django mendeteksi ada field baru years_of_experience di model Skill, lalu membuat file migrasi baru, misal main/migrations/0002_skill_years_of_experience.py, isinya kurang lebih instruksi AddField untuk menambah kolom tersebut ke tabel main_skill.

setelah itu jalankan perintah python manage.py migrate
Django membaca file migrasi tadi dan benar-benar mengeksekusi perintah SQL ALTER TABLE main_skill ADD COLUMN years_of_experience ... ke database. Setelah ini, kolom baru benar-benar ada di tabel, dan kamu bisa langsung memakai skill.years_of_experience di kode.

Kalau menjalankan makemigrations saja (tanpa migrate), file migrasi sudah ada, tapi database masih dalam struktur lama,kalau ingin mengakses skill.years_of_experience, akan muncul error karena kolom tersebut belum benar-benar ada di tabel.

Kalau menjalankan migrate saja (tanpa makemigrations setelah ubah model), Django tidak tahu ada perubahan yang perlu diterapkan, karena belum ada file migrasi baru yang dibuat untuk perubahan tersebut sehingga migrate hanya menjalankan migrasi yang sudah ada, bukan mendeteksi perubahan model secara otomatis.

Ai disclosure: Saya menggunakan claude AI untuk membantu menjelaskan struktur kode urls dan mengecek kesessuaian skills.html yang ingin saya buat agar fungsional seperti experience.html yang sudah dibuat saat tutorial. Saya juga menngunakan Claude AI untuk debugging beberapa line of code di mana saya meninggalkan potongan kode penting seperti import yang menyebabkan web menjadi error. Saya juga meminta bantuan saat membuat unit test dan meminta beberapa AI lain sebagai refrensi untuk jawaban refleksi tugas 2.




### Tugas 3
1. Kita menggunakan model form daripada html manual simpelnya karena model form itu lebih efisien. ModelForm bisa meng generate field langsung dari field model, jadi kalau kita ingin mengubah model (menambah/menghabpus suatu field), formnya tidak perlu kita tulis dari awal, berbeda dengan html manual di mana kita harus menulis setiap input sendiri sehingga rawan kesalahan dan bisa terjadi inkonsistensi. ModelForm juga memberikan kita validasi otomatis berbeda dengan html manual di mana kita harus menulis sendiri validasi di view sehingga rawan bug dan celah keamanan seperti user yang menginput data tak valid tapi tetap ter approve.

> kenapa wajib pakai {% csrf_token %}: Fungsinya sebagai layer protection dari CSRF (Cross-Site Request Forgery) 
{% csrf_token %} memastikan bahwa request POST benar-benar berasal dari form yang dibuat oleh aplikasi kita, bukan request palsu dari situs lain.

2. JSON  lebih sering digunakan karena formatnya lebih sederhana, ringkas, dan mudah diproses oleh JavaScript maupun bahasa pemrograman lainnya terutama XML. Hal ini bisa kita lihat dari JSON yang tidak butuh di closing berulang kali, tidak seperti XML sehingga lebih hemat bandwidth. JSON juga lebih mudah dibaca manusia karena strukturnya lebih flat dan tidak ada tag pembuka-penutup yang berulang. Namun,  bukan berarti XML sudah tidak digunakan. XML masih banyak digunakan pada sistem tertentu.

3. - Request masuk ke view (misal get_skills_json) lewat URL yang udah didaftarin di urls.py.
- View query data dari database lewat Django ORM, misal Skill.objects.all(). Hasilnya berupa QuerySet berisi objek Python (model instance), bukan format yang bisa langsung dikirim lewat HTTP sebagai teks
- Data ini di-serialize pakai serializers.serialize("json", data) ,mengubah objek Python/model menjadi string berformat JSON.
- String JSON idibungkus menjadi HttpResponse dengan content_type="application/json", agar browser/client tau bahwa isinya JSON, bukan HTML biasa.
- Response dikirim balik ke client (browser, JS fetch, atau aplikasi lain) yang bisa langsung parse JSON itu dan dipakai (misal ditampilkan, atau di-deserialize lagi untuk diolah lebih lanjut).

Kita melakukan serialization karena data yang diperoleh dari model Django berupa object atau QuerySet Python, sedangkan client membutuhkan format data yang dapat ditransmisikan melalui HTTP, seperti JSON. Serialization mengubah object tersebut menjadi representasi JSON sehingga dapat dikirim dan diproses oleh frontend atau aplikasi lain.

Ai disclosure: Saya menggunakan Claude AI untuk membantu saya memahami program yang saya buat dan program dari tutorial serta membantu mendebug segala error yang saya temukan dalam proses development tugas 3 