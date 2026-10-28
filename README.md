# Analisis Sentimen Multi-Paradigma: Krisis Kelangkaan BBM di Indonesia

Sistem riset komparasi analisis sentimen opini publik terhadap isu kelangkaan bahan bakar minyak (BBM: Pertalite, Solar, antrean panjang SPBU, penimbunan, dan disparitas harga) di Indonesia melalui multiplatform media sosial (YouTube & Instagram).

Sistem ini membandingkan **6 metode klasifikasi lintas paradigma**:
1. **Lexicon-Based**: InSet Lexicon (9.101 leksikon berbobot + proteksi jendela negasi)
2. **Machine Learning (Hybrid)**: Hybrid SVM (TF-IDF + InSet Lexicon Valence Score)
3. **Machine Learning (Baseline)**: Linear SVM (Pure TF-IDF Unigram & Bigram)
4. **Distance Metric**: Cosine Similarity (Nearest Class Centroid Prototype dalam ruang TF-IDF)
5. **Deep Learning**: PyTorch Neural BiLSTM dengan Word-Level Attention Pooling (*Explainable AI*)
6. **X-Shot Learning**: Few-Shot Contextual Reasoning dengan 4 tahap *Chain-of-Thought (CoT)*

---

## Hasil Evaluasi Komparatif (Test Set N=205)

Pengujian dilakukan pada partisi data uji identik (20% Stratified Split dari 1.022 data riil YouTube & Instagram):

| Paradigma | Metode & Algoritma | Akurasi | Precision (Macro) | Recall (Macro) | F1-Score (Macro) | F1-Score (Weighted) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Lexicon-Based** | InSet Lexicon | **83.90%** | **67.15%** | **68.18%** | **67.64%** | **84.09%** |
| **Machine Learning (Hybrid)** | Hybrid SVM (TF-IDF + InSet) | **76.59%** | 56.97% | 57.56% | 57.13% | 77.08% |
| **Machine Learning (Baseline)** | Linear SVM (TF-IDF) | **75.12%** | 51.62% | 51.37% | 51.49% | 74.99% |
| **Distance Metric** | Cosine Similarity | **67.32%** | 44.64% | 50.53% | 46.18% | 70.14% |
| **Deep Learning** | Neural BiLSTM (Attention) | **75.12%** | 51.62% | 51.37% | 51.49% | 74.99% |
| **X-Shot Learning** | X-Shot Reasoning (CoT) | **29.76%** | 40.78% | 42.78% | 23.41% | 32.29% |

---

## Fitur Utama Aplikasi

- **Interactive Step-by-Step Simulator**: Visualisasi tiap tahapan NLP (Raw &rarr; Case Folding &rarr; Slang Norm &rarr; Negation Stopwords &rarr; Sastrawi Stemming &rarr; Live 6-Model Output + Word Attention Heatmap + Chain-of-Thought).
- **Tabel & Audit Ground Truth**: Menampilkan 1.022 komentar dengan ikon status centang hijau (`check`) dan silang merah (`x`), filter misklasifikasi per model, dan unduh data Excel/CSV instan.
- **Diagram Alir & Arsitektur Sidang**: Flowchart interaktif untuk kebutuhan presentasi dan sidang tugas akhir/skripsi.
- **Antarmuka Bersih & Seragam**: Slate/Zinc monochromatic theme, Dark Mode & Light Mode, serta 100% Lucide SVG Icons asli tanpa Unicode emojis.

---

## Struktur Direktori

```text
├── config/                     # Pengaturan aplikasi & API keys
├── data/
│   ├── dataset_bbm_raw.csv                # Raw comments riil YouTube & Instagram
│   ├── dataset_bbm_ground_truth.csv       # Ground truth pelabelan
│   ├── dataset_bbm_preprocessed.csv       # Dataset 1.022 data + prediksi seluruh model
│   ├── dataset_bbm_preprocessed.xlsx      # Versi Excel bukti ground truth
│   ├── evaluasi_komparasi_sentimen.json   # Laporan metrik evaluasi lengkap
│   ├── evaluasi_komparasi_sentimen.xlsx   # Laporan evaluasi multi-sheet
│   └── lexicon/                           # InSet Lexicon & Colloquial Slang Lexicon
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

1. **Setup Environment dengan `uv`:**
   ```bash
   uv venv --python 3.12 .venv
   uv pip install -r requirements.txt
   uv pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```

2. **Jalankan Pelatihan & Evaluasi Pipeline (Opsional):**
   ```bash
   uv run python pipeline/run_full_analysis.py
   ```

3. **Jalankan Web Server:**
   ```bash
   uv run python server.py
   ```

4. Buka peramban di `http://127.0.0.1:8000` dan pilih tab **Riset Sentimen Kelangkaan BBM**.
