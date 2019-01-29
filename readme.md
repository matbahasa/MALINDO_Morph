# MALINDO Morph

**Bahasa Melayu** (Bahasa Indonesia mengikuti bahasa Melayu)

## Pendahuluan
MALINDO Morph merupakan kamus morfologi untuk bahasa Melayu dan bahasa Indonesia.  Kamus MALINDO Morph dilesenkan dengan pelesenan [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.ms).  Untuk maklumat terperinci mengenai MALINDO Morph, sila rujuk makalah di bawah ini.

## Sumber rujukan
Nomoto, Hiroki, Hannah Choi, David Moeljadi and Francis Bond. 2018. [MALINDO Morph: Morphological dictionary and analyser for Malay/Indonesian](http://lrec-conf.org/workshops/lrec2018/W29/pdf/8_W29.pdf). Kiyoaki Shirai (ed.) _Proceedings of the LREC 2018 Workshop "The 13th Workshop on Asian Language Resources"_, 36-43.

## Format
`ID [TAB] Akar [TAB] Bentuk lahir [TAB] Awalan/proklitik [TAB] Akhiran/enklitik [TAB] Apitan [TAB] Penggandaan [TAB] Sumber`

Kolum "sumber" ditambah mulai versi 20180917.

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

### Contoh
    cc-4023	ada	mengada-adakan	meN-	-kan	0	R-penuh Kamus
    ec-7280	ada	diada-adakan	di-	-kan	0	R-penuh Leipzig
    ex-89426	tanggungjawab	dipertanggungjawabkannya	di-+per-	-kan+-nya	0	0 Leipzig
    ex-89427	tanggungjawab	kebertanggungjawabannya	ber-	-nya	ke--an	0 Leipzig

## Versi
|Versi|Jumlah garis|Butir-butir|
|:---|---:|:---|
|20180312|232,546|cc 84,403; ec 47,399; ex 100,744|
|20180418|232,516|cc 84,404; ec 47,400; ex 100,712|
|20180817|232,503|cc 84,404; ec 47,400; ex 100,699|
|20180917|233,390|cc 84,429; ec 48,262; ex 100,699|
|20181125|233,374|cc 84,410; ec 48,274; ex 100,690|
|20190129|233,372|cc 84,410; ec 48,347; ex 100,615|

---
**Bahasa Indonesia**

## Pendahuluan
MALINDO Morph merupakan kamus morfologi untuk bahasa Melayu dan bahasa Indonesia. Kamus MALINDO Morph dilisensikan dengan lisensi [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.id). Untuk informasi terperinci tentang MALINDO Morph, mohon merujuk kepada makalah di bawah ini.

## Sumber rujukan
Nomoto, Hiroki, Hannah Choi, David Moeljadi and Francis Bond. 2018. [MALINDO Morph: Morphological dictionary and analyser for Malay/Indonesian](http://lrec-conf.org/workshops/lrec2018/W29/pdf/8_W29.pdf). Kiyoaki Shirai (ed.) _Proceedings of the LREC 2018 Workshop "The 13th Workshop on Asian Language Resources"_, 36-43.

## Format
`ID [TAB] Bentuk dasar [TAB] Bentuk jadian [TAB] Prefiks/proklitik [TAB] Sufiks/enklitik [TAB] Konfiks [TAB] Reduplikasi [TAB] Sumber`

Kolum "sumber" ditambah mulai versi 20180917.

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

### Contoh
    cc-4023	ada	mengada-adakan	meN-	-kan	0	R-penuh Kamus
    ec-7280	ada	diada-adakan	di-	-kan	0	R-penuh Leipzig
    ex-89426	tanggungjawab	dipertanggungjawabkannya	di-+per-	-kan+-nya	0	0 Leipzig
    ex-89427	tanggungjawab	kebertanggungjawabannya	ber-	-nya	ke--an	0 Leipzig

## Versi
|Versi|Jumlah baris|Rincian|
|:---|---:|:---|
|20180312|232.546|cc 84.403; ec 47.399; ex 100.744|
|20180418|232.516|cc 84.404; ec 47.400; ex 100.712|
|20180817|232.503|cc 84.404; ec 47.400; ex 100.699|
|20180917|233.390|cc 84.429; ec 48.262; ex 100.699|
|20181125|233.374|cc 84.410; ec 48.274; ex 100.690|
|20190129|233.372|cc 84.410; ec 48.347; ex 100.615|
