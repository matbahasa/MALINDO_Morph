# MALINDO Morph

**Bahasa Melayu** ([Bahasa Indonesia](#pendahuluan-1) mengikuti bahasa Melayu)

## Pendahuluan
MALINDO Morph merupakan kamus morfologi untuk bahasa Melayu dan bahasa Indonesia.  Kamus MALINDO Morph dilesenkan dengan pelesenan [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.ms).  Untuk maklumat terperinci mengenai MALINDO Morph, sila rujuk makalah di bawah ini.

## Sumber rujukan
- Nomoto, Hiroki, Hannah Choi, David Moeljadi and Francis Bond. 2018. [MALINDO Morph: Morphological dictionary and analyser for Malay/Indonesian](http://lrec-conf.org/workshops/lrec2018/W29/pdf/8_W29.pdf). Kiyoaki Shirai (ed.) _Proceedings of the LREC 2018 Workshop "The 13th Workshop on Asian Language Resources"_, 36-43.
- (bkn maklumat dasar dan lema) Nomoto, Hiroki. 2020. [Towards genuine stemming and lemmatization in Malay/Indonesian](https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/F4-3.pdf). _Proceedings of the Twenty-Sixth Annual Meeting of the Association for Natural Language Processing_, 1033-1036.

## Format
`ID [TAB] Akar [TAB] Bentuk lahir [TAB] Awalan/proklitik [TAB] Akhiran/enklitik [TAB] Apitan [TAB] Penggandaan [TAB] Sumber [TAB] Dasar [TAB] Lema`

- Kolum "sumber" ditambah mulai versi 20180917.
- Kolum "dasar" dan "lema" ditambah mulai versi 20190923.

### ID
`ID` terdiri daripada dua unsur, iaitu

- Jenis sumber: `cc` (**c**ore, **c**hecked), `ec` (**e**xpanded, **c**hecked) atau `ex` (**e**xpanded, **x** (tidak) checked); diikuti dengan tanda sempang (`-`) dan
- Nombor siri

### Jenis penggandaan
Terdapat empat jenis penggandaan yang dibezakan dalam kamus MALINDO Morph, iaitu

- `R-penuh`: Penggandaan penuh seperti _kadang-kadang_ (berdasarkan _kadang_).
- `R-separa`: Penggandaan separa seperti _lelaki_ (berdasarkan _laki_).
- `R-ritma`: Penggandaan berentak seperti _teka-teki_ (berdasarkan _teka_).
  - `R-ritma_mjmk`: Penggandaan berentak yang merupakan kata majmuk, iaitu gabungan dua perkataan seperti _asal-usul_.
- `0`: Tidak melibatkan penggandaan.

### Jenis sumber

- `Kamus`: _Kamus Dewan (edisi keempat)_ dan _Kamus Besar Bahasa Indonesia (edisi kelima)_.
- `Leipzig`: [Koleksi Korpus Leipzig](http://wortschatz.uni-leipzig.de/en/download)
- `Frogstory-David`: [Indonesian Frog Storytelling Corpus](https://github.com/davidmoeljadi/corpus-frog-storytelling) oleh David Moeljadi.
- `Melayu-Standard-Lisan`: [Korpus Variasi Bahasa Melayu: Standard Lisan](https://github.com/matbahasa/Melayu_Standard_Lisan)
- `Melayu-Sabah`: [Korpus Variasi Bahasa Melayu: Sabah](https://github.com/matbahasa/Melayu_Sabah)
- `Melayu-Sarawak`: [Korpus Variasi Bahasa Melayu: Sarawak](https://github.com/matbahasa/Melayu_Sarawak)
- `Melayu-Brunei`: [Korpus Variasi Bahasa Melayu: Brunei](https://github.com/matbahasa/Melayu_Brunei)
- `Indo-Jakarta-Lisan`: [Korpus Variasi Bahasa Melayu: Jakarta Lisan](https://github.com/matbahasa/)
- `Lain`

### Notasi

- `+`: campur
- `@`: atau

### Contoh
    cc-4023	ada	mengada-adakan	meN-	-kan	0	R-penuh	Kamus	ada-adakan	mengada-adakan
    ec-7280	ada	diada-adakan	di-	-kan	0	R-penuh	Leipzig	ada-adakan	mengada-adakan
    ec-48506	tanggungjawab	dipertanggungjawabkannya	di-+per-	-kan+-nya	0	0	Leipzig	dia+pertanggungjawabkan	dia+mempertanggungjawabkan
    ec-48508	tanggungjawab	kebertanggungjawabannya	ber-	-nya	ke--an	0	Leipzig	kebertanggungjawaban+dia	kebertanggungjawaban+dia
    cc-27899	gunting	gunting	0	0	0	0	Kamus	gunting	gunting@menggunting
    (Lema adalah "gunting" untuk kata nama dan "menggunting" untuk kata kerja.)

## Versi
|Versi|Jumlah garis|Butir-butir|
|:---|---:|:---|
|20180312|232,546|cc 84,403; ec 47,399; ex 100,744|
|20180418|232,516|cc 84,404; ec 47,400; ex 100,712|
|20180817|232,503|cc 84,404; ec 47,400; ex 100,699|
|20180917|233,390|cc 84,429; ec 48,262; ex 100,699|
|20181125|233,374|cc 84,410; ec 48,274; ex 100,690|
|20190129|233,372|cc 84,410; ec 48,347; ex 100,615|
|20190923|234,274|cc 84,415; ec 49,686; ex 100,173|
|20200917|234,567|cc 84,419; ec 53,072; ex  97,076|
|20211116|241,911|cc 85,010; ec 60,634; ex  96,267|
|20221221|246,525|cc 85,644; ec 65,005; ex  95,876|

---
**Bahasa Indonesia**

## Pendahuluan
MALINDO Morph merupakan kamus morfologi untuk bahasa Melayu dan bahasa Indonesia. Kamus MALINDO Morph dilisensikan dengan lisensi [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.id). Untuk informasi terperinci tentang MALINDO Morph, mohon merujuk kepada makalah di bawah ini.

## Sumber rujukan
- Nomoto, Hiroki, Hannah Choi, David Moeljadi and Francis Bond. 2018. [MALINDO Morph: Morphological dictionary and analyser for Malay/Indonesian](http://lrec-conf.org/workshops/lrec2018/W29/pdf/8_W29.pdf). Kiyoaki Shirai (ed.) _Proceedings of the LREC 2018 Workshop "The 13th Workshop on Asian Language Resources"_, 36-43.
- (ttg informasi dasar dan lema) Nomoto, Hiroki. 2020. [Towards genuine stemming and lemmatization in Malay/Indonesian](https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/F4-3.pdf). _Proceedings of the Twenty-Sixth Annual Meeting of the Association for Natural Language Processing_, 1033-1036.

## Format
`ID [TAB] Bentuk dasar (_root_) [TAB] Bentuk jadian [TAB] Prefiks/proklitik [TAB] Sufiks/enklitik [TAB] Konfiks [TAB] Reduplikasi [TAB] Sumber [TAB] Dasar ("stem") [TAB] Lema`

- Kolum "sumber" ditambah mulai versi 20180917.
- Kolum "dasar" dan "lema" ditambah mulai versi 20190923.

### ID
`ID` terdiri dari dua unsur, yaitu:

- Jenis sumber: `cc` (**c**ore, **c**hecked), `ec` (**e**xpanded, **c**hecked), atau `ex` (**e**xpanded, **x** (tidak) checked); diikuti dengan tanda penghubung (`-`) dan
- Nomor seri

### Jenis reduplikasi
Terdapat empat jenis reduplikasi yang dibedakan dalam kamus MALINDO Morph, yaitu

- `R-penuh`: Reduplikasi penuh atau dwilingga seperti _kadang-kadang_ (berdasarkan _kadang_).
- `R-separa`: Reduplikasi sebagian atau dwipurwa seperti _lelaki_ (berdasarkan _laki_).
- `R-ritma`: Reduplikasi berubah bunyi atau dwilingga salin suara seperti _teka-teki_ (berdasarkan _teka_).
  - `R-ritma_mjmk`: Reduplikasi berubah bunyi yang merupakan kata majemuk, yaitu gabungan dua kata seperti _asal-usul_.
- `0`: Tidak melibatkan reduplikasi.

### Jenis sumber

- `Kamus`: _Kamus Dewan (edisi keempat)_ dan _Kamus Besar Bahasa Indonesia (edisi kelima)_.
- `Leipzig`: [Koleksi Korpus Leipzig](http://wortschatz.uni-leipzig.de/en/download)
- `Frogstory-David`: [Indonesian Frog Storytelling Corpus](https://github.com/davidmoeljadi/corpus-frog-storytelling) oleh David Moeljadi.
- `Melayu-Standard-Lisan`: [Korpus Variasi Bahasa Melayu: Standard Lisan](https://github.com/matbahasa/Melayu_Standard_Lisan)
- `Melayu-Sabah`: [Korpus Variasi Bahasa Melayu: Sabah](https://github.com/matbahasa/Melayu_Sabah)
- `Melayu-Sarawak`: [Korpus Variasi Bahasa Melayu: Sarawak](https://github.com/matbahasa/Melayu_Sarawak)
- `Melayu-Brunei`: [Korpus Variasi Bahasa Melayu: Brunei](https://github.com/matbahasa/Melayu_Brunei)
- `Indo-Jakarta-Lisan`: [Korpus Variasi Bahasa Melayu: Jakarta Lisan](https://github.com/matbahasa/)
- `Lain`

### Notasi

- `+`: campur
- `@`: atau

### Contoh
    cc-4023	ada	mengada-adakan	meN-	-kan	0	R-penuh	Kamus	ada-adakan	mengada-adakan
    ec-7280	ada	diada-adakan	di-	-kan	0	R-penuh	Leipzig	ada-adakan	mengada-adakan
    ec-48507	tanggung jawab	dipertanggungjawabkannya	di-+per-	-kan+-nya	0	0	Leipzig	dia+pertanggungjawabkan	dia+mempertanggungjawabkan
    ec-48509	tanggung jawab	kebertanggungjawabannya	ber-	-nya	ke--an	0	Leipzig	kebertanggungjawaban+dia	kebertanggungjawaban+dia
    cc-27899	gunting	gunting	0	0	0	0	Kamus	gunting	gunting@menggunting
    (Lemanya adalah "gunting" untuk nomina dan "menggunting" untuk verba.)

## Versi
|Versi|Jumlah baris|Rincian|
|:---|---:|:---|
|20180312|232.546|cc 84.403; ec 47.399; ex 100.744|
|20180418|232.516|cc 84.404; ec 47.400; ex 100.712|
|20180817|232.503|cc 84.404; ec 47.400; ex 100.699|
|20180917|233.390|cc 84.429; ec 48.262; ex 100.699|
|20181125|233.374|cc 84.410; ec 48.274; ex 100.690|
|20190129|233.372|cc 84.410; ec 48.347; ex 100.615|
|20190923|234.274|cc 84.415; ec 49.686; ex 100.173|
|20200917|234.567|cc 84.419; ec 53.072; ex  97.076|
|20211116|241.911|cc 85.010; ec 60.634; ex  96.267|
|20221221|246.525|cc 85.644; ec 65.005; ex  95.876|
