# Analisis Sentimen Multi-Paradigma: Krisis Ketenagakerjaan di Indonesia

Sistem riset komparasi analisis sentimen opini publik terhadap isu ketenagakerjaan di Indonesia (PHK massal, aturan batas usia loker, sarjana menganggur, dan pesangon) melalui multiplatform media sosial.

Sistem ini membandingkan **6 metode klasifikasi lintas paradigma**:
1. **Lexicon-Based**: InSet Lexicon (9.083 leksikon berbobot + proteksi jendela negasi)
2. **Machine Learning (Hybrid)**: Hybrid SVM (TF-IDF + InSet Lexicon Valence Score)
3. **Machine Learning (Baseline)**: Linear SVM (Pure TF-IDF Unigram & Bigram)
4. **Distance Metric**: Cosine Similarity (Nearest Class Centroid Prototype dalam ruang TF-IDF)
5. **Deep Learning**: PyTorch Neural BiLSTM dengan Word-Level Attention Pooling (*Explainable AI*)
6. **X-Shot Learning**: Few-Shot Contextual Reasoning dengan 4 tahap *Chain-of-Thought (CoT)*

---

## Hasil Evaluasi Komparatif (Test Set N=124)

Pengujian dilakukan pada partisi data uji identik (20% Stratified Split dari 617 data riil valid):

| Paradigma | Metode & Algoritma | Akurasi | Precision (Macro) | Recall (Macro) | F1-Score (Macro) | F1-Score (Weighted) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Lexicon-Based** | InSet Lexicon | **99.19%** | 98.67% | 98.41% | **98.51%** | 99.19% |
| **Machine Learning (Hybrid)** | Hybrid SVM (TF-IDF + InSet) | **92.74%** | 90.15% | 87.30% | **87.71%** | 92.36% |
| **Machine Learning (Baseline)** | Linear SVM (TF-IDF) | **70.16%** | 64.66% | 49.50% | 51.74% | 65.74% |
| **Distance Metric** | Cosine Similarity | **67.74%** | 58.03% | 59.67% | 58.73% | 68.39% |
| **Deep Learning** | Neural BiLSTM (Attention) | **64.52%** | 58.42% | 63.78% | 58.58% | 66.48% |
| **X-Shot Learning** | X-Shot Reasoning (CoT) | **44.35%** | **73.98%** | 48.94% | 39.40% | 45.88% |

---

## Fitur Utama Aplikasi

- **Interactive Step-by-Step Simulator**: Visualisasi tiap tahapan NLP (Raw &rarr; Case Folding &rarr; Slang Norm &rarr; Negation Stopwords &rarr; Sastrawi Stemming &rarr; Live 6-Model Output + Word Attention Heatmap + Chain-of-Thought).
- **Tabel & Audit Ground Truth**: Menampilkan 617 komentar dengan ikon status centang hijau (`check`) dan silang merah (`x`), filter miskalsifikasi per model, dan unduh data Excel/CSV instan.
- **Diagram Alir & Arsitektur Sidang**: Flowchart interaktif untuk kebutuhan presentasi dan sidang tugas akhir/skripsi.
- **Antarmuka Bersih & Seragam**: Slate/Zinc monochromatic theme, Dark Mode & Light Mode, serta 100% Lucide SVG Icons asli tanpa Unicode emojis.

---

## Struktur Direktori

```text
├── config/                     # Pengaturan aplikasi & API keys
├── data/
│   ├── dataset_ketenagakerjaan_preprocessed.csv   # Dataset 617 data + prediksi semua model
│   ├── dataset_ketenagakerjaan_preprocessed.xlsx  # Versi Excel bukti ground truth
│   ├── evaluasi_komparasi_sentimen.json           # Laporan metrik evaluasi lengkap
│   ├── evaluasi_komparasi_sentimen.xlsx           # Laporan evaluasi multi-sheet
│   └── lexicon/                                   # InSet Lexicon & Colloquial Slang Lexicon
├── frontend/
│   └── dist/
│       └── index.html         # Single-Page Web Dashboard (Tailwind + Lucide)
├── pipeline/
│   ├── preprocessing.py       # 5-stage NLP Preprocessor dengan audit transformasi
│   ├── inset_lexicon.py       # InSet Lexicon Classifier + Negation Inversion
│   ├── classifiers.py         # Linear SVM, Hybrid SVM, Cosine Sim, BiLSTM, & X-Shot
│   ├── evaluator.py           # Komputasi akurasi, Macro/Weighted F1, & Confusion Matrix
│   ├── service.py             # Singleton service backend
│   └── run_full_analysis.py   # Skrip pelatihan & evaluasi komparatif dataset
├── scrapers/                  # Modul scraper multiplatform (YouTube & Instagram)
├── server.py                  # Server FastAPI daemon (REST API)
└── requirements.txt           # Dependensi Python
```

---

## Cara Menjalankan

1. **Install Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan Pelatihan & Evaluasi Pipeline (Opsional):**
   ```bash
   python pipeline/run_full_analysis.py
   ```

3. **Jalankan Web Server:**
   ```bash
   python server.py
   ```

4. Buka peramban di `http://127.0.0.1:8000` dan pilih modul **Riset Sentimen Kerja**.
