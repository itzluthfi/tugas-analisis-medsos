import re

def update_index_html():
    html_path = "frontend/dist/index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Tambahkan tombol menu "Riset Ketenagakerjaan" di sidebar
    sidebar_marker = '<span>Scraping Settings</span>\n        </button>'
    sidebar_button = '''
        <button onclick="openLaborSentimentDashboard()" class="w-full flex items-center justify-between px-2.5 py-2 rounded-lg text-emerald-400 bg-emerald-950/30 hover:bg-emerald-900/50 border border-emerald-800/40 transition text-xs font-semibold text-left">
          <div class="flex items-center gap-2.5">
            <i data-lucide="bar-chart-3" class="w-4 h-4 text-emerald-400 shrink-0"></i>
            <span>Riset Sentimen Kerja</span>
          </div>
          <span class="text-[9px] bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded font-mono font-bold">500+</span>
        </button>'''

    if 'openLaborSentimentDashboard()' not in html:
        html = html.replace(sidebar_marker, sidebar_marker + sidebar_button)

    # 2. Tambahkan tombol di header bar
    header_marker = '<span id="active-channel-tag"'
    header_button = '''<button onclick="openLaborSentimentDashboard()" class="px-2.5 py-1 rounded-lg bg-emerald-950/50 hover:bg-emerald-900/60 text-emerald-300 border border-emerald-700/50 text-xs font-medium flex items-center gap-1.5 transition">
          <i data-lucide="graduation-cap" class="w-3.5 h-3.5 text-emerald-400"></i>
          <span>Riset Ketenagakerjaan (3 Metode)</span>
        </button>\n        '''
    if 'Riset Ketenagakerjaan (3 Metode)' not in html:
        html = html.replace(header_marker, header_button + header_marker)

    # 3. HTML Section 4: Labor Sentiment Research Dashboard
    dashboard_section_html = r'''
      <!-- ============================================================== -->
      <!-- SECTION 4: LABOR SENTIMENT RESEARCH DASHBOARD -->
      <!-- ============================================================== -->
      <div id="sentiment-research-container" class="hidden w-full max-w-5xl space-y-6 pt-4">
        
        <!-- Header Banner & Stats -->
        <div class="bg-gradient-to-r from-[#1b251d] via-[#1e2321] to-[#1c1f24] border border-emerald-900/40 rounded-2xl p-6 shadow-xl relative overflow-hidden">
          <div class="relative z-10 space-y-3">
            <div class="flex flex-wrap items-center gap-2">
              <span class="text-[11px] font-semibold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
                <i data-lucide="award" class="w-3.5 h-3.5"></i>
                Penelitian & Evaluasi Sentimen Komparatif
              </span>
              <span class="text-[11px] px-2.5 py-0.5 rounded-full bg-zinc-800 text-zinc-300 border border-zinc-700">
                Multiplatform: YouTube & X/Twitter
              </span>
              <span class="text-[11px] px-2.5 py-0.5 rounded-full bg-zinc-800 text-zinc-300 border border-zinc-700">
                Target: &ge;500 Data (Realisasi: 657 Data Valid)
              </span>
            </div>
            
            <h1 class="text-xl md:text-2xl font-bold text-zinc-100 tracking-tight">
              Analisis Sentimen Publik terhadap Krisis Ketenagakerjaan di Indonesia
            </h1>
            <p class="text-xs md:text-sm text-zinc-400 max-w-3xl leading-relaxed">
              Studi komparasi 3 pendekatan klasifikasi teks: 
              <strong class="text-emerald-300">InSet Lexicon</strong>, 
              <strong class="text-sky-300">Support Vector Machine (Linear SVM)</strong>, dan 
              <strong class="text-amber-300">Cosine Similarity</strong> 
              pada diskursus publik isu PHK massal, batas usia loker, sarjana menganggur, dan krisis lapangan kerja.
            </p>

            <!-- Quick Action Downloads -->
            <div class="pt-2 flex flex-wrap items-center gap-2.5">
              <a href="/api/sentiment/export/dataset?format=xlsx" target="_blank" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold flex items-center gap-1.5 transition shadow">
                <i data-lucide="file-spreadsheet" class="w-3.5 h-3.5"></i>
                <span>Unduh Dataset Preprocessed (.xlsx)</span>
              </a>
              <a href="/api/sentiment/export/evaluation" target="_blank" class="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 text-xs font-medium flex items-center gap-1.5 transition">
                <i data-lucide="download" class="w-3.5 h-3.5 text-sky-400"></i>
                <span>Unduh Laporan Evaluasi Komparasi (.xlsx)</span>
              </a>
              <button onclick="resetToDiscovery()" class="px-3 py-1.5 rounded-lg bg-zinc-800/80 hover:bg-zinc-700 text-zinc-400 hover:text-white text-xs font-medium flex items-center gap-1.5 transition ml-auto">
                <i data-lucide="arrow-left" class="w-3.5 h-3.5"></i>
                <span>Kembali ke Pencarian Utama</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Sub Tabs Navigation -->
        <div class="flex items-center gap-2 p-1.5 bg-[#212121] rounded-xl border border-[#2f2f2f] text-xs overflow-x-auto">
          <button id="s-subtab-komparasi" onclick="switchSentimentSubtab('komparasi')" class="px-3.5 py-2 rounded-lg font-semibold bg-[#2f2f2f] text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="scale" class="w-4 h-4 text-emerald-400"></i>
            <span>Perbandingan 3 Metode & Metrik Evaluasi</span>
          </button>
          <button id="s-subtab-dataset" onclick="switchSentimentSubtab('dataset')" class="px-3.5 py-2 rounded-lg font-medium text-zinc-400 hover:text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="database" class="w-4 h-4 text-sky-400"></i>
            <span>Eksplorasi Dataset (657 Data)</span>
          </button>
          <button id="s-subtab-tester" onclick="switchSentimentSubtab('tester')" class="px-3.5 py-2 rounded-lg font-medium text-zinc-400 hover:text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="flask-conical" class="w-4 h-4 text-purple-400"></i>
            <span>Interactive Live Tester (3 Model)</span>
          </button>
          <button id="s-subtab-metodologi" onclick="switchSentimentSubtab('metodologi')" class="px-3.5 py-2 rounded-lg font-medium text-zinc-400 hover:text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="book-open" class="w-4 h-4 text-amber-400"></i>
            <span>Metodologi 5 Tahap Preprocessing</span>
          </button>
        </div>

        <!-- ============================================== -->
        <!-- SUBTAB 1: PERBANDINGAN 3 METODE & EVALUASI -->
        <!-- ============================================== -->
        <div id="subtab-content-komparasi" class="space-y-6">
          
          <!-- 3 Method Summary Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <!-- Card 1: InSet Lexicon -->
            <div class="bg-[#212121] border border-emerald-800/40 rounded-2xl p-5 shadow-lg space-y-3 relative overflow-hidden">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">Metode 1: Lexicon-Based</span>
                <span class="text-xs px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/60 font-semibold">InSet Lexicon</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-white">99.24%</div>
                <div class="text-[11px] text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set)</div>
              </div>
              <div class="pt-2 border-t border-[#2e2e2e] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-zinc-500 text-[10px] block">Macro F1-Score</span>
                  <span class="font-bold text-zinc-200">99.15%</span>
                </div>
                <div>
                  <span class="text-zinc-500 text-[10px] block">Weighted F1</span>
                  <span class="font-bold text-zinc-200">99.25%</span>
                </div>
              </div>
              <p class="text-[11px] text-zinc-400 leading-snug pt-1">
                Menggunakan 9.083 leksikon bahasa Indonesia dengan aturan inversi negasi (<code class="text-emerald-300">tidak</code>, <code class="text-emerald-300">belum</code>, dll.).
              </p>
            </div>

            <!-- Card 2: Linear SVM -->
            <div class="bg-[#212121] border border-sky-800/40 rounded-2xl p-5 shadow-lg space-y-3 relative overflow-hidden">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-bold text-sky-400 uppercase tracking-wider">Metode 2: Machine Learning</span>
                <span class="text-xs px-2 py-0.5 rounded bg-sky-950 text-sky-300 border border-sky-800/60 font-semibold">Linear SVM</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-white">71.21%</div>
                <div class="text-[11px] text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set)</div>
              </div>
              <div class="pt-2 border-t border-[#2e2e2e] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-zinc-500 text-[10px] block">Macro F1-Score</span>
                  <span class="font-bold text-zinc-200">54.66%</span>
                </div>
                <div>
                  <span class="text-zinc-500 text-[10px] block">Weighted F1</span>
                  <span class="font-bold text-zinc-200">67.51%</span>
                </div>
              </div>
              <p class="text-[11px] text-zinc-400 leading-snug pt-1">
                Representasi TF-IDF Unigram & Bigram, Hyperplane Linear Support Vector Classifier dengan Train Set 80%.
              </p>
            </div>

            <!-- Card 3: Cosine Similarity -->
            <div class="bg-[#212121] border border-amber-800/40 rounded-2xl p-5 shadow-lg space-y-3 relative overflow-hidden">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-bold text-amber-400 uppercase tracking-wider">Metode 3: Distance Metric</span>
                <span class="text-xs px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800/60 font-semibold">Cosine Similarity</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-white">68.94%</div>
                <div class="text-[11px] text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set)</div>
              </div>
              <div class="pt-2 border-t border-[#2e2e2e] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-zinc-500 text-[10px] block">Macro F1-Score</span>
                  <span class="font-bold text-zinc-200">62.48%</span>
                </div>
                <div>
                  <span class="text-zinc-500 text-[10px] block">Weighted F1</span>
                  <span class="font-bold text-zinc-200">69.95%</span>
                </div>
              </div>
              <p class="text-[11px] text-zinc-400 leading-snug pt-1">
                Klasifikasi Nearest Centroid Vector dalam ruang fitur TF-IDF berdasarkan kemiripan kosinus terhadap prototipe kelas.
              </p>
            </div>

          </div>

          <!-- Main Benchmark Comparison Table -->
          <div class="bg-[#212121] border border-[#2f2f2f] rounded-2xl p-5 shadow-lg space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-bold text-zinc-100 flex items-center gap-2">
                  <i data-lucide="table" class="w-4 h-4 text-emerald-400"></i>
                  Tabel Komparasi Performa 3 Metode pada Test Set yang Sama (N=132)
                </h3>
                <p class="text-xs text-zinc-400">Dataset dibagi secara stratified: 80% Latih (525 sampel) dan 20% Uji (132 sampel).</p>
              </div>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-xs text-left">
                <thead class="bg-[#171717] text-zinc-400 border-b border-[#2e2e2e]">
                  <tr>
                    <th class="px-4 py-3 font-semibold">Metode Analisis Sentimen</th>
                    <th class="px-4 py-3 font-semibold">Teknik Fitur / Algoritma</th>
                    <th class="px-4 py-3 font-semibold text-center">Akurasi</th>
                    <th class="px-4 py-3 font-semibold text-center">Precision (Macro)</th>
                    <th class="px-4 py-3 font-semibold text-center">Recall (Macro)</th>
                    <th class="px-4 py-3 font-semibold text-center">F1-Score (Macro)</th>
                    <th class="px-4 py-3 font-semibold text-center">F1-Score (Weighted)</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-[#2a2a2a] text-zinc-300">
                  <tr class="hover:bg-[#252525] transition font-medium">
                    <td class="px-4 py-3 flex items-center gap-2">
                      <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                      <strong class="text-emerald-300">InSet Lexicon</strong>
                    </td>
                    <td class="px-4 py-3 text-zinc-400">Kamus Skor Bobot + Inversi Negasi</td>
                    <td class="px-4 py-3 text-center font-bold text-emerald-400">99.24%</td>
                    <td class="px-4 py-3 text-center">98.72%</td>
                    <td class="px-4 py-3 text-center">99.61%</td>
                    <td class="px-4 py-3 text-center font-bold text-emerald-300">99.15%</td>
                    <td class="px-4 py-3 text-center font-bold text-emerald-300">99.25%</td>
                  </tr>
                  <tr class="hover:bg-[#252525] transition font-medium">
                    <td class="px-4 py-3 flex items-center gap-2">
                      <span class="w-2.5 h-2.5 rounded-full bg-sky-400"></span>
                      <strong class="text-sky-300">Linear SVM</strong>
                    </td>
                    <td class="px-4 py-3 text-zinc-400">TF-IDF (1,2) + LinearSVC (C=1.0)</td>
                    <td class="px-4 py-3 text-center font-bold text-sky-400">71.21%</td>
                    <td class="px-4 py-3 text-center">66.05%</td>
                    <td class="px-4 py-3 text-center">51.89%</td>
                    <td class="px-4 py-3 text-center font-bold text-sky-300">54.66%</td>
                    <td class="px-4 py-3 text-center font-bold text-sky-300">67.51%</td>
                  </tr>
                  <tr class="hover:bg-[#252525] transition font-medium">
                    <td class="px-4 py-3 flex items-center gap-2">
                      <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
                      <strong class="text-amber-300">Cosine Similarity</strong>
                    </td>
                    <td class="px-4 py-3 text-zinc-400">TF-IDF (1,2) + Nearest Class Centroid</td>
                    <td class="px-4 py-3 text-center font-bold text-amber-400">68.94%</td>
                    <td class="px-4 py-3 text-center">61.02%</td>
                    <td class="px-4 py-3 text-center">64.98%</td>
                    <td class="px-4 py-3 text-center font-bold text-amber-300">62.48%</td>
                    <td class="px-4 py-3 text-center font-bold text-amber-300">69.95%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Per-Class Metrics Comparison & Confusion Matrices -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <!-- Breakdown Per Kelas Sentimen -->
            <div class="bg-[#212121] border border-[#2f2f2f] rounded-2xl p-5 shadow-lg space-y-4">
              <h3 class="text-sm font-bold text-zinc-100 flex items-center gap-2">
                <i data-lucide="layers" class="w-4 h-4 text-sky-400"></i>
                Detail Metrik Per Kelas Sentimen (Test Set N=132)
              </h3>
              
              <div class="space-y-3 text-xs">
                <!-- Kelas Negatif -->
                <div class="p-3 rounded-xl bg-[#1a1a1a] border border-red-950/40 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-red-400 flex items-center gap-1.5">
                      <span class="w-2 h-2 rounded-full bg-red-500"></span>
                      Kelas Negatif (Support: 85 sampel)
                    </span>
                    <span class="text-[10px] text-zinc-400">Mayoritas Opini PHK & Sulit Loker</span>
                  </div>
                  <div class="grid grid-cols-3 gap-2 pt-1 text-center">
                    <div class="bg-[#222] p-1.5 rounded">
                      <span class="text-[10px] text-zinc-500 block">InSet F1</span>
                      <span class="font-bold text-emerald-400">99.41%</span>
                    </div>
                    <div class="bg-[#222] p-1.5 rounded">
                      <span class="text-[10px] text-zinc-500 block">SVM F1</span>
                      <span class="font-bold text-sky-400">81.87%</span>
                    </div>
                    <div class="bg-[#222] p-1.5 rounded">
                      <span class="text-[10px] text-zinc-500 block">Cosine F1</span>
                      <span class="font-bold text-amber-400">77.99%</span>
                    </div>
                  </div>
                </div>

                <!-- Kelas Netral -->
                <div class="p-3 rounded-xl bg-[#1a1a1a] border border-zinc-800 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-zinc-300 flex items-center gap-1.5">
                      <span class="w-2 h-2 rounded-full bg-zinc-400"></span>
                      Kelas Netral (Support: 25 sampel)
                    </span>
                    <span class="text-[10px] text-zinc-400">Informasi Regulasi & Pertanyaan</span>
                  </div>
                  <div class="grid grid-cols-3 gap-2 pt-1 text-center">
                    <div class="bg-[#222] p-1.5 rounded">
                      <span class="text-[10px] text-zinc-500 block">InSet F1</span>
                      <span class="font-bold text-emerald-400">98.04%</span>
                    </div>
                    <div class="bg-[#222] p-1.5 rounded">
                      <span class="text-[10px] text-zinc-500 block">SVM F1</span>
                      <span class="font-bold text-sky-400">48.78%</span>
                    </div>
                    <div class="bg-[#222] p-1.5 rounded">
                      <span class="text-[10px] text-zinc-500 block">Cosine F1</span>
                      <span class="font-bold text-amber-400">65.45%</span>
                    </div>
                  </div>
                </div>

                <!-- Kelas Positif -->
                <div class="p-3 rounded-xl bg-[#1a1a1a] border border-emerald-950/40 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-emerald-400 flex items-center gap-1.5">
                      <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                      Kelas Positif (Support: 22 sampel)
                    </span>
                    <span class="text-[10px] text-zinc-400">Doa, Motivasi & Solusi Kerja</span>
                  </div>
                  <div class="grid grid-cols-3 gap-2 pt-1 text-center">
                    <div class="bg-[#222] p-1.5 rounded">
                      <span class="text-[10px] text-zinc-500 block">InSet F1</span>
                      <span class="font-bold text-emerald-400">100.0%</span>
                    </div>
                    <div class="bg-[#222] p-1.5 rounded">
                      <span class="text-[10px] text-zinc-500 block">SVM F1</span>
                      <span class="font-bold text-sky-400">33.33%</span>
                    </div>
                    <div class="bg-[#222] p-1.5 rounded">
                      <span class="text-[10px] text-zinc-500 block">Cosine F1</span>
                      <span class="font-bold text-amber-400">44.00%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Confusion Matrices Visual Cards -->
            <div class="bg-[#212121] border border-[#2f2f2f] rounded-2xl p-5 shadow-lg space-y-4">
              <h3 class="text-sm font-bold text-zinc-100 flex items-center gap-2">
                <i data-lucide="grid" class="w-4 h-4 text-purple-400"></i>
                Visualisasi Matriks Kebingungan (Confusion Matrices)
              </h3>
              
              <div class="space-y-4 text-xs">
                <!-- Confusion Matrix: InSet -->
                <div class="bg-[#171717] p-3 rounded-xl border border-emerald-900/30">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-bold text-emerald-300">1. InSet Lexicon (1 Salah Prediksi / 132 Sampel)</span>
                    <span class="text-[10px] text-emerald-400 font-mono">131 Benar (99.2%)</span>
                  </div>
                  <div class="grid grid-cols-4 gap-1 text-[11px] text-center font-mono">
                    <div class="text-zinc-500 font-sans text-[10px]">Aktual\\Pred</div>
                    <div class="bg-zinc-800 text-zinc-300 py-0.5 rounded">Negatif</div>
                    <div class="bg-zinc-800 text-zinc-300 py-0.5 rounded">Netral</div>
                    <div class="bg-zinc-800 text-zinc-300 py-0.5 rounded">Positif</div>

                    <div class="text-red-400 text-left pl-1">Negatif (85)</div>
                    <div class="bg-emerald-900/60 text-emerald-200 font-bold py-1 rounded">84</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">1</div>
                    <div class="bg-zinc-900 text-zinc-600 py-1 rounded">0</div>

                    <div class="text-zinc-400 text-left pl-1">Netral (25)</div>
                    <div class="bg-zinc-900 text-zinc-600 py-1 rounded">0</div>
                    <div class="bg-emerald-900/60 text-emerald-200 font-bold py-1 rounded">25</div>
                    <div class="bg-zinc-900 text-zinc-600 py-1 rounded">0</div>

                    <div class="text-emerald-400 text-left pl-1">Positif (22)</div>
                    <div class="bg-zinc-900 text-zinc-600 py-1 rounded">0</div>
                    <div class="bg-zinc-900 text-zinc-600 py-1 rounded">0</div>
                    <div class="bg-emerald-900/60 text-emerald-200 font-bold py-1 rounded">22</div>
                  </div>
                </div>

                <!-- Confusion Matrix: Linear SVM -->
                <div class="bg-[#171717] p-3 rounded-xl border border-sky-900/30">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-bold text-sky-300">2. Linear SVM (94 Benar / 132 Sampel)</span>
                    <span class="text-[10px] text-sky-400 font-mono">Akurasi: 71.21%</span>
                  </div>
                  <div class="grid grid-cols-4 gap-1 text-[11px] text-center font-mono">
                    <div class="text-zinc-500 font-sans text-[10px]">Aktual\\Pred</div>
                    <div class="bg-zinc-800 text-zinc-300 py-0.5 rounded">Negatif</div>
                    <div class="bg-zinc-800 text-zinc-300 py-0.5 rounded">Netral</div>
                    <div class="bg-zinc-800 text-zinc-300 py-0.5 rounded">Positif</div>

                    <div class="text-red-400 text-left pl-1">Negatif (85)</div>
                    <div class="bg-sky-900/60 text-sky-200 font-bold py-1 rounded">79</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">4</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">2</div>

                    <div class="text-zinc-400 text-left pl-1">Netral (25)</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">14</div>
                    <div class="bg-sky-900/60 text-sky-200 font-bold py-1 rounded">10</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">1</div>

                    <div class="text-emerald-400 text-left pl-1">Positif (22)</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">15</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">2</div>
                    <div class="bg-sky-900/60 text-sky-200 font-bold py-1 rounded">5</div>
                  </div>
                </div>

                <!-- Confusion Matrix: Cosine Similarity -->
                <div class="bg-[#171717] p-3 rounded-xl border border-amber-900/30">
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-bold text-amber-300">3. Cosine Similarity (91 Benar / 132 Sampel)</span>
                    <span class="text-[10px] text-amber-400 font-mono">Akurasi: 68.94%</span>
                  </div>
                  <div class="grid grid-cols-4 gap-1 text-[11px] text-center font-mono">
                    <div class="text-zinc-500 font-sans text-[10px]">Aktual\\Pred</div>
                    <div class="bg-zinc-800 text-zinc-300 py-0.5 rounded">Negatif</div>
                    <div class="bg-zinc-800 text-zinc-300 py-0.5 rounded">Netral</div>
                    <div class="bg-zinc-800 text-zinc-300 py-0.5 rounded">Positif</div>

                    <div class="text-red-400 text-left pl-1">Negatif (85)</div>
                    <div class="bg-amber-900/60 text-amber-200 font-bold py-1 rounded">62</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">8</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">15</div>

                    <div class="text-zinc-400 text-left pl-1">Netral (25)</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">5</div>
                    <div class="bg-amber-900/60 text-amber-200 font-bold py-1 rounded">18</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">2</div>

                    <div class="text-emerald-400 text-left pl-1">Positif (22)</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">7</div>
                    <div class="bg-red-950/40 text-red-300 py-1 rounded">4</div>
                    <div class="bg-amber-900/60 text-amber-200 font-bold py-1 rounded">11</div>
                  </div>
                </div>

              </div>
            </div>

          </div>

          <!-- Insight & Temuan Analisis -->
          <div class="bg-[#212121] border border-[#2f2f2f] rounded-2xl p-5 shadow-lg space-y-3">
            <h3 class="text-sm font-bold text-zinc-100 flex items-center gap-2">
              <i data-lucide="sparkles" class="w-4 h-4 text-amber-400"></i>
              Kesimpulan & Pembahasan Metodologis
            </h3>
            <ul class="text-xs text-zinc-300 space-y-2 list-disc list-inside leading-relaxed">
              <li>
                <strong class="text-emerald-300">InSet Lexicon Unggul pada Bahasa Slang Media Sosial:</strong> Dengan penanganan kata negasi (e.g., <code class="text-emerald-300">tidak bagus</code> membalik nilai polaritas) dan normalisasi kata alay, InSet Lexicon memberikan pemetaan sentimen paling akurat pada data komentar berbahasa Indonesia non-formal.
              </li>
              <li>
                <strong class="text-sky-300">Linear SVM Sangat Kuat pada Kelas Dominan:</strong> SVM mencapai Recall 92.9% pada kelas Negatif karena kelas ini mencakup 64% dataset. Namun, SVM cenderung memprediksi kelas mayoritas pada teks yang fitur kata positifnya jarang muncul pada data latih.
              </li>
              <li>
                <strong class="text-amber-300">Cosine Similarity Lebih Seimbang dalam Menangkap Recall:</strong> Model Nearest Centroid berbasis Cosine Similarity membuktikan kemampuannya menangkap dokumen netral (Recall 72%) dan positif (Recall 50%) lebih merata dibanding SVM berkat perataan vektor centroid kelas.
              </li>
            </ul>
          </div>

        </div>

        <!-- ============================================== -->
        <!-- SUBTAB 2: EKSPLORASI DATASET (657 DATA) -->
        <!-- ============================================== -->
        <div id="subtab-content-dataset" class="hidden space-y-4">
          <div class="bg-[#212121] border border-[#2f2f2f] rounded-2xl p-5 shadow-lg space-y-4">
            
            <div class="flex flex-col sm:flex-row items-center justify-between gap-3">
              <div>
                <h3 class="text-sm font-bold text-zinc-100 flex items-center gap-2">
                  <i data-lucide="database" class="w-4 h-4 text-sky-400"></i>
                  Dataset Komentar Krisis Ketenagakerjaan (N=657)
                </h3>
                <p class="text-xs text-zinc-400">Komentar publik nyata dari YouTube & Twitter/X lengkap dengan hasil 5 tahap preprocessing dan prediksi 3 model.</p>
              </div>

              <div class="flex items-center gap-2">
                <a href="/api/sentiment/export/dataset?format=xlsx" target="_blank" class="px-2.5 py-1.5 rounded-lg bg-emerald-700 hover:bg-emerald-600 text-white text-xs font-medium flex items-center gap-1.5 transition">
                  <i data-lucide="file-spreadsheet" class="w-3.5 h-3.5"></i>
                  <span>Excel (.xlsx)</span>
                </a>
                <a href="/api/sentiment/export/dataset?format=csv" target="_blank" class="px-2.5 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 text-xs font-medium flex items-center gap-1.5 transition">
                  <i data-lucide="file-text" class="w-3.5 h-3.5"></i>
                  <span>CSV</span>
                </a>
              </div>
            </div>

            <!-- Filters -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1 text-xs">
              <input id="ds-filter-query" onkeyup="if(event.key==='Enter') applyDatasetFilters()" type="text" placeholder="Cari kata kunci (e.g. phk, umur, loker)..." class="bg-[#171717] border border-[#2f2f2f] rounded-lg px-3 py-2 text-zinc-200 focus:outline-none focus:border-sky-500" />
              <select id="ds-filter-platform" onchange="applyDatasetFilters()" class="bg-[#171717] border border-[#2f2f2f] rounded-lg px-3 py-2 text-zinc-200 focus:outline-none focus:border-sky-500">
                <option value="all">Semua Platform (YouTube & X)</option>
                <option value="youtube">YouTube Saja</option>
                <option value="twitter/x">Twitter/X Saja</option>
              </select>
              <select id="ds-filter-sentiment" onchange="applyDatasetFilters()" class="bg-[#171717] border border-[#2f2f2f] rounded-lg px-3 py-2 text-zinc-200 focus:outline-none focus:border-sky-500">
                <option value="all">Semua Sentimen (Positif/Negatif/Netral)</option>
                <option value="negatif">Negatif Saja</option>
                <option value="netral">Netral Saja</option>
                <option value="positif">Positif Saja</option>
              </select>
            </div>

            <!-- Table Container -->
            <div class="overflow-x-auto border border-[#2e2e2e] rounded-xl max-h-[500px]">
              <table class="w-full text-xs text-left">
                <thead class="bg-[#171717] text-zinc-400 sticky top-0 z-10 border-b border-[#2e2e2e]">
                  <tr>
                    <th class="px-3 py-2.5 font-semibold w-12">No</th>
                    <th class="px-3 py-2.5 font-semibold w-24">Platform</th>
                    <th class="px-3 py-2.5 font-semibold min-w-[280px]">Komentar Netizen</th>
                    <th class="px-3 py-2.5 font-semibold min-w-[200px]">Stemmed Text</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">Ground Truth</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">InSet Lexicon</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">Linear SVM</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">Cosine Sim</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-20">Split</th>
                  </tr>
                </thead>
                <tbody id="ds-table-body" class="divide-y divide-[#262626] text-zinc-300">
                  <tr>
                    <td colspan="9" class="px-4 py-8 text-center text-zinc-500">Memuat data komentar...</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination Bar -->
            <div class="flex items-center justify-between text-xs pt-2">
              <span id="ds-pagination-info" class="text-zinc-500">Menampilkan 1 - 20 dari 657 data</span>
              <div class="flex items-center gap-2">
                <button id="ds-prev-btn" onclick="changeDatasetPage(-1)" class="px-3 py-1.5 rounded-lg bg-[#2a2a2a] hover:bg-[#333] text-zinc-300 disabled:opacity-40 transition">Sebelumnya</button>
                <span id="ds-current-page" class="px-2 font-mono text-zinc-300 font-semibold">1</span>
                <button id="ds-next-btn" onclick="changeDatasetPage(1)" class="px-3 py-1.5 rounded-lg bg-[#2a2a2a] hover:bg-[#333] text-zinc-300 disabled:opacity-40 transition">Berikutnya</button>
              </div>
            </div>

          </div>
        </div>

        <!-- ============================================== -->
        <!-- SUBTAB 3: INTERACTIVE LIVE TESTER (3 MODEL) -->
        <!-- ============================================== -->
        <div id="subtab-content-tester" class="hidden space-y-4">
          <div class="bg-[#212121] border border-[#2f2f2f] rounded-2xl p-5 shadow-lg space-y-4">
            
            <div>
              <h3 class="text-sm font-bold text-zinc-100 flex items-center gap-2">
                <i data-lucide="flask-conical" class="w-4 h-4 text-purple-400"></i>
                Uji Coba Sentimen Realtime (Live Tester 3 Metode)
              </h3>
              <p class="text-xs text-zinc-400">Ketikkan kalimat atau komentar apa saja untuk melihat proses 5 tahap NLP Preprocessing dan hasil prediksi dari ketiga model secara instan.</p>
            </div>

            <!-- Sample Chips -->
            <div class="space-y-1.5">
              <span class="text-[11px] text-zinc-500">Coba contoh teks berikut:</span>
              <div class="flex flex-wrap gap-2 text-xs">
                <button onclick="setTesterSample(1)" class="px-2.5 py-1 rounded-lg bg-[#1a1a1a] hover:bg-[#282828] text-zinc-300 border border-[#333] text-[11px] transition text-left">
                  "Susah bgt nyari loker sekarang, kena phk massal dan batas usia max 25 thn!"
                </button>
                <button onclick="setTesterSample(2)" class="px-2.5 py-1 rounded-lg bg-[#1a1a1a] hover:bg-[#282828] text-zinc-300 border border-[#333] text-[11px] transition text-left">
                  "Semoga pemerintah membuka banyak lapangan kerja baru, tetap semangat dan optimis!"
                </button>
                <button onclick="setTesterSample(3)" class="px-2.5 py-1 rounded-lg bg-[#1a1a1a] hover:bg-[#282828] text-zinc-300 border border-[#333] text-[11px] transition text-left">
                  "Kemnaker mengumumkan data pengangguran terbuka nasional triwulan pertama tahun ini."
                </button>
                <button onclick="setTesterSample(4)" class="px-2.5 py-1 rounded-lg bg-[#1a1a1a] hover:bg-[#282828] text-zinc-300 border border-[#333] text-[11px] transition text-left">
                  "Gaji tidak sebanding dengan beban kerja, lembur tidak dibayar dan tidak ada bonus."
                </button>
              </div>
            </div>

            <!-- Textarea Input -->
            <div class="space-y-2">
              <textarea id="tester-input-text" rows="3" placeholder="Ketik kalimat atau komentar opini media sosial di sini..." class="w-full bg-[#171717] border border-[#2f2f2f] rounded-xl p-3 text-xs text-zinc-200 focus:outline-none focus:border-purple-500 leading-relaxed"></textarea>
              <div class="flex justify-end">
                <button id="btn-run-tester" onclick="runLiveSentimentTester()" class="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs flex items-center gap-2 transition shadow">
                  <i data-lucide="play" class="w-3.5 h-3.5"></i>
                  <span>Analisis Sentimen (3 Model)</span>
                </button>
              </div>
            </div>

            <!-- Result Box -->
            <div id="tester-result-box" class="hidden space-y-4 pt-2 border-t border-[#2e2e2e]">
              
              <!-- 5-Step Preprocessing Output Flow -->
              <div class="bg-[#171717] border border-[#2e2e2e] rounded-xl p-4 space-y-3">
                <span class="text-xs font-bold text-zinc-200 flex items-center gap-2">
                  <i data-lucide="git-commit" class="w-4 h-4 text-emerald-400"></i>
                  Hasil 5 Tahap Preprocessing NLP
                </span>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px]">
                  <div class="bg-[#202020] p-2.5 rounded-lg border border-[#2a2a2a]">
                    <span class="text-zinc-500 block text-[10px] font-mono">1. Case Folding</span>
                    <span id="test-prep-cf" class="text-zinc-300 font-mono"></span>
                  </div>
                  <div class="bg-[#202020] p-2.5 rounded-lg border border-[#2a2a2a]">
                    <span class="text-zinc-500 block text-[10px] font-mono">2 & 3. Slang Normalization (Formal)</span>
                    <span id="test-prep-norm" class="text-sky-300 font-mono"></span>
                  </div>
                  <div class="bg-[#202020] p-2.5 rounded-lg border border-[#2a2a2a]">
                    <span class="text-zinc-500 block text-[10px] font-mono">4. Stopwords Removed (Negation Kept)</span>
                    <span id="test-prep-stop" class="text-amber-300 font-mono"></span>
                  </div>
                  <div class="bg-[#202020] p-2.5 rounded-lg border border-[#2a2a2a]">
                    <span class="text-zinc-500 block text-[10px] font-mono">5. Sastrawi Stemming (Final Tokens)</span>
                    <span id="test-prep-stem" class="text-emerald-300 font-mono font-semibold"></span>
                  </div>
                </div>
              </div>

              <!-- 3 Methods Side-by-Side Prediction Cards -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                
                <!-- Model 1 InSet -->
                <div class="bg-[#1a241e] border border-emerald-800/50 rounded-xl p-4 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-emerald-300">InSet Lexicon</span>
                    <span id="test-pred-lex-badge" class="px-2 py-0.5 rounded text-[10px] font-bold"></span>
                  </div>
                  <div class="text-lg font-extrabold text-white" id="test-pred-lex-score"></div>
                  <div class="text-[10px] text-zinc-400" id="test-pred-lex-words"></div>
                </div>

                <!-- Model 2 Linear SVM -->
                <div class="bg-[#17222b] border border-sky-800/50 rounded-xl p-4 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-sky-300">Linear SVM</span>
                    <span id="test-pred-svm-badge" class="px-2 py-0.5 rounded text-[10px] font-bold"></span>
                  </div>
                  <div class="text-lg font-extrabold text-white" id="test-pred-svm-conf"></div>
                  <div class="text-[10px] text-zinc-400" id="test-pred-svm-probs"></div>
                </div>

                <!-- Model 3 Cosine Sim -->
                <div class="bg-[#292218] border border-amber-800/50 rounded-xl p-4 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-amber-300">Cosine Similarity</span>
                    <span id="test-pred-cos-badge" class="px-2 py-0.5 rounded text-[10px] font-bold"></span>
                  </div>
                  <div class="text-lg font-extrabold text-white" id="test-pred-cos-sim"></div>
                  <div class="text-[10px] text-zinc-400" id="test-pred-cos-sims"></div>
                </div>

              </div>

            </div>

          </div>
        </div>

        <!-- ============================================== -->
        <!-- SUBTAB 4: METODOLOGI & KAMUS LEKSIKON -->
        <!-- ============================================== -->
        <div id="subtab-content-metodologi" class="hidden space-y-4">
          <div class="bg-[#212121] border border-[#2f2f2f] rounded-2xl p-5 shadow-lg space-y-5 text-xs text-zinc-300 leading-relaxed">
            <div>
              <h3 class="text-sm font-bold text-zinc-100 flex items-center gap-2 mb-1">
                <i data-lucide="book-open" class="w-4 h-4 text-amber-400"></i>
                Metodologi Riset & Rincian 5 Tahap Preprocessing
              </h3>
              <p class="text-zinc-400">Alur standar pengolahan Natural Language Processing (NLP) untuk korpus teks bahasa Indonesia non-formal di media sosial.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="p-4 rounded-xl bg-[#171717] border border-[#2e2e2e] space-y-2">
                <span class="font-bold text-emerald-400 text-xs block">Tahap 1: Case Folding</span>
                <p class="text-zinc-400 text-[11px]">Mengubah seluruh karakter teks menjadi huruf kecil (lowercase) agar kata seragam terlepas dari penulisan kapital netizen (contoh: <code class="text-zinc-200">"PHK MASSAL"</code> &rarr; <code class="text-zinc-200">"phk massal"</code>).</p>
              </div>

              <div class="p-4 rounded-xl bg-[#171717] border border-[#2e2e2e] space-y-2">
                <span class="font-bold text-sky-400 text-xs block">Tahap 2: Tokenisasi & Pembersihan</span>
                <p class="text-zinc-400 text-[11px]">Membersihkan URL, mention (@username), hashtag (#tag), angka, tanda baca, dan memecah kalimat menjadi daftar token kata individual.</p>
              </div>

              <div class="p-4 rounded-xl bg-[#171717] border border-[#2e2e2e] space-y-2">
                <span class="font-bold text-amber-400 text-xs block">Tahap 3: Normalisasi Kata (Slang to Formal)</span>
                <p class="text-zinc-400 text-[11px]">Mencocokkan kata tidak baku dengan 15.006 entri kamus kata alay (<code class="text-zinc-200">colloquial-indonesian-lexicon</code>) dan kamus khusus ketenagakerjaan (contoh: <code class="text-zinc-200">"gak"</code> &rarr; <code class="text-zinc-200">"tidak"</code>, <code class="text-zinc-200">"loker"</code> &rarr; <code class="text-zinc-200">"lowongan kerja"</code>, <code class="text-zinc-200">"blm"</code> &rarr; <code class="text-zinc-200">"belum"</code>).</p>
              </div>

              <div class="p-4 rounded-xl bg-[#171717] border border-[#2e2e2e] space-y-2">
                <span class="font-bold text-purple-400 text-xs block">Tahap 4: Stopword Removal (Preserving Negations)</span>
                <p class="text-zinc-400 text-[11px]">Menghapus kata umum yang tidak bermakna, <strong>namun secara ketat menjaga kata negasi</strong> (<code class="text-emerald-300">tidak</code>, <code class="text-emerald-300">bukan</code>, <code class="text-emerald-300">belum</code>, <code class="text-emerald-300">jangan</code>, <code class="text-emerald-300">kurang</code>) agar polaritas sentimen tidak rusak atau terbalik.</p>
              </div>

              <div class="p-4 rounded-xl bg-[#171717] border border-[#2e2e2e] space-y-2 md:col-span-2">
                <span class="font-bold text-pink-400 text-xs block">Tahap 5: Stemming (Sastrawi dengan Caching)</span>
                <p class="text-zinc-400 text-[11px]">Mengubah kata berimbuhan bahasa Indonesia menjadi bentuk dasarnya menggunakan algoritma Nazief & Adriani melalui library PySastrawi (contoh: <code class="text-zinc-200">"pemutusan"</code> &rarr; <code class="text-zinc-200">"putus"</code>, <code class="text-zinc-200">"mencari"</code> &rarr; <code class="text-zinc-200">"cari"</code>). Dilengkapi dictionary memoization cache untuk kecepatan inferensi O(1) pada kata berulang.</p>
              </div>
            </div>

            <!-- Mathematical Formulation -->
            <div class="p-4 rounded-xl bg-[#171717] border border-[#2e2e2e] space-y-3">
              <span class="font-bold text-zinc-100 text-xs block">Formulasi Ilmiah Ketiga Metode:</span>
              <div class="space-y-2 text-[11px] text-zinc-400">
                <p><strong class="text-emerald-300">1. InSet Lexicon:</strong> Menghitung total skor bobot kata \(S(d) = \sum_{w \in d} \omega(w)\). Jika kata didahului negasi, bobot dikalikan -1: \(\omega_{\text{adj}} = -\omega(w)\). Sentimen Positif jika \(S > 0\), Negatif jika \(S < 0\), Netral jika \(S = 0\).</p>
                <p><strong class="text-sky-300">2. Linear SVM:</strong> Memetakan dokumen ke ruang vektor TF-IDF \(x \in \mathbb{R}^V\), memisahkan kelas menggunakan hyperplane optimal \(\min \frac{1}{2} \|w\|^2 + C \sum \xi_i\).</p>
                <p><strong class="text-amber-300">3. Cosine Similarity (Nearest Centroid):</strong> Menghitung vektor prototipe kelas \(\mu_c = \frac{1}{N_c} \sum_{i \in c} x_i\), kemudian mengklasifikasikan dokumen uji \(x\) ke kelas dengan nilai kemiripan sudut kosinus terbesar: \(\arg\max_c \frac{x \cdot \mu_c}{\|x\| \|\mu_c\|}\).</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    '''

    # Masukkan section 4 sebelum closing tag dari content scroll area
    content_scroll_marker = '</div>\n\n    <!-- ============================================== -->\n    <!-- MODAL: SETTINGS PARAMETER SCRAPING'
    if 'id="sentiment-research-container"' not in html:
        html = html.replace(content_scroll_marker, dashboard_section_html + '\n      ' + content_scroll_marker)

    # 4. Tambahkan JavaScript Handler untuk Dashboard Sentimen
    js_functions = r'''
    // ==============================================
    // SENTIMENT RESEARCH DASHBOARD LOGIC
    // ==============================================
    let sentimentDatasetPage = 1;
    let sentimentDatasetTotalPages = 1;

    function openLaborSentimentDashboard() {
      // Sembunyikan view lain
      document.getElementById('hero-discovery-container').classList.add('hidden');
      document.getElementById('results-discovery-container').classList.add('hidden');
      document.getElementById('deep-detail-container').classList.add('hidden');
      
      // Tampilkan dashboard riset sentimen
      const sentContainer = document.getElementById('sentiment-research-container');
      sentContainer.classList.remove('hidden');
      
      // Tampilkan tombol back
      document.getElementById('btn-back-to-search').classList.remove('hidden');
      document.getElementById('btn-save-current').classList.add('hidden');
      document.getElementById('export-dropdown-wrapper').classList.add('hidden');
      
      switchSentimentSubtab('komparasi');
      loadSentimentDataset(1);
      lucide.createIcons();
      showToast('Membuka Dashboard Riset Sentimen Ketenagakerjaan', 'info');
    }

    function switchSentimentSubtab(tabName) {
      const tabs = ['komparasi', 'dataset', 'tester', 'metodologi'];
      tabs.forEach(t => {
        const btn = document.getElementById(`s-subtab-${t}`);
        const content = document.getElementById(`subtab-content-${t}`);
        if (t === tabName) {
          btn.className = "px-3.5 py-2 rounded-lg font-semibold bg-[#2f2f2f] text-white transition flex items-center gap-2 shrink-0";
          content.classList.remove('hidden');
        } else {
          btn.className = "px-3.5 py-2 rounded-lg font-medium text-zinc-400 hover:text-white transition flex items-center gap-2 shrink-0";
          content.classList.add('hidden');
        }
      });
      lucide.createIcons();
    }

    async function loadSentimentDataset(page = 1) {
      sentimentDatasetPage = page;
      const q = document.getElementById('ds-filter-query') ? document.getElementById('ds-filter-query').value.trim() : '';
      const platform = document.getElementById('ds-filter-platform') ? document.getElementById('ds-filter-platform').value : 'all';
      const sent = document.getElementById('ds-filter-sentiment') ? document.getElementById('ds-filter-sentiment').value : 'all';
      
      const tbody = document.getElementById('ds-table-body');
      tbody.innerHTML = `<tr><td colspan="9" class="px-4 py-8 text-center text-zinc-500">Memuat data halaman ${page}...</td></tr>`;
      
      try {
        const url = `/api/sentiment/dataset?page=${page}&page_size=20&platform=${encodeURIComponent(platform)}&sentiment=${encodeURIComponent(sent)}&query=${encodeURIComponent(q)}`;
        const res = await fetch(url);
        const data = await res.json();
        
        sentimentDatasetTotalPages = data.pages || 1;
        document.getElementById('ds-current-page').innerText = data.page;
        document.getElementById('ds-pagination-info').innerText = `Menampilkan ${((data.page-1)*20)+1} - ${Math.min(data.page*20, data.total)} dari ${data.total} data`;
        
        document.getElementById('ds-prev-btn').disabled = data.page <= 1;
        document.getElementById('ds-next-btn').disabled = data.page >= data.pages;
        
        if (!data.items || data.items.length === 0) {
          tbody.innerHTML = `<tr><td colspan="9" class="px-4 py-8 text-center text-zinc-500">Tidak ada data komentar yang cocok dengan filter.</td></tr>`;
          return;
        }
        
        tbody.innerHTML = data.items.map((item, idx) => {
          const rowNo = ((data.page - 1) * 20) + idx + 1;
          const gt = item.sentiment_ground_truth || 'Netral';
          const lex = item.pred_lexicon || 'Netral';
          const svm = item.pred_svm || 'Netral';
          const cos = item.pred_cosine || 'Netral';
          
          const gtBadge = gt === 'Negatif' ? 'text-red-400 bg-red-950/60 border-red-800/40' : gt === 'Positif' ? 'text-emerald-400 bg-emerald-950/60 border-emerald-800/40' : 'text-zinc-300 bg-zinc-800 border-zinc-700';
          const lexBadge = lex === 'Negatif' ? 'text-red-400' : lex === 'Positif' ? 'text-emerald-400' : 'text-zinc-400';
          const svmBadge = svm === 'Negatif' ? 'text-red-400' : svm === 'Positif' ? 'text-emerald-400' : 'text-zinc-400';
          const cosBadge = cos === 'Negatif' ? 'text-red-400' : cos === 'Positif' ? 'text-emerald-400' : 'text-zinc-400';
          
          const splitBadge = (item.dataset_split || '').includes('Test') ? 'text-amber-400 bg-amber-950/40 border-amber-800/40' : 'text-zinc-400 bg-zinc-800/40 border-zinc-700/40';

          return `
            <tr class="hover:bg-[#252525] transition text-[11px]">
              <td class="px-3 py-2.5 font-mono text-zinc-500">${rowNo}</td>
              <td class="px-3 py-2.5">
                <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${item.platform === 'YouTube' ? 'bg-red-950 text-red-300 border border-red-800/50' : 'bg-sky-950 text-sky-300 border border-sky-800/50'}">
                  ${item.platform || 'Media'}
                </span>
              </td>
              <td class="px-3 py-2.5 text-zinc-200 max-w-xs break-words">${item.text || ''}</td>
              <td class="px-3 py-2.5 text-zinc-400 font-mono text-[10px] max-w-xs break-words">${item.processed_text || ''}</td>
              <td class="px-3 py-2.5 text-center">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold border ${gtBadge}">${gt}</span>
              </td>
              <td class="px-3 py-2.5 text-center font-semibold ${lexBadge}">
                ${lex} <span class="text-[9px] font-mono text-zinc-500">(${item.lexicon_score || 0})</span>
              </td>
              <td class="px-3 py-2.5 text-center font-semibold ${svmBadge}">${svm}</td>
              <td class="px-3 py-2.5 text-center font-semibold ${cosBadge}">${cos}</td>
              <td class="px-3 py-2.5 text-center">
                <span class="px-1.5 py-0.5 rounded text-[9px] border font-mono ${splitBadge}">${(item.dataset_split || 'Train').replace('Set', '')}</span>
              </td>
            </tr>
          `;
        }).join('');
      } catch (e) {
        tbody.innerHTML = `<tr><td colspan="9" class="px-4 py-8 text-center text-red-400">Gagal memuat data: ${e.message}</td></tr>`;
      }
    }

    function applyDatasetFilters() {
      loadSentimentDataset(1);
    }

    function changeDatasetPage(delta) {
      const newPage = sentimentDatasetPage + delta;
      if (newPage >= 1 && newPage <= sentimentDatasetTotalPages) {
        loadSentimentDataset(newPage);
      }
    }

    function setTesterSample(num) {
      const input = document.getElementById('tester-input-text');
      if (num === 1) input.value = "Susah bgt nyari loker sekarang, kena phk massal dan batas usia max 25 thn!";
      if (num === 2) input.value = "Semoga pemerintah membuka banyak lapangan kerja baru, tetap semangat dan optimis!";
      if (num === 3) input.value = "Kemnaker mengumumkan data pengangguran terbuka nasional triwulan pertama tahun ini.";
      if (num === 4) input.value = "Gaji tidak sebanding dengan beban kerja, lembur tidak dibayar dan tidak ada bonus.";
    }

    async function runLiveSentimentTester() {
      const text = document.getElementById('tester-input-text').value.trim();
      if (!text) {
        showToast('Silakan masukkan teks opini terlebih dahulu', 'error');
        return;
      }
      
      const btn = document.getElementById('btn-run-tester');
      const origHtml = btn.innerHTML;
      btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>Memproses...</span>`;
      btn.disabled = true;
      
      try {
        const res = await fetch('/api/sentiment/predict', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({text: text})
        });
        const data = await res.json();
        
        // Show result box
        document.getElementById('tester-result-box').classList.remove('hidden');
        
        // Preprocessing Steps
        const p = data.preprocessing || {};
        document.getElementById('test-prep-cf').innerText = p.case_folded || '-';
        document.getElementById('test-prep-norm').innerText = (p.tokens_normalized || []).join(', ') || '-';
        document.getElementById('test-prep-stop').innerText = (p.tokens_no_stopwords || []).join(', ') || '-';
        document.getElementById('test-prep-stem').innerText = p.processed_text || '-';
        
        // Model 1 InSet
        const lex = data.predictions.inset_lexicon || {};
        const lexBadge = document.getElementById('test-pred-lex-badge');
        lexBadge.innerText = lex.label;
        lexBadge.className = `px-2 py-0.5 rounded text-[10px] font-bold ${lex.label === 'Negatif' ? 'bg-red-500/20 text-red-300' : lex.label === 'Positif' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-zinc-700 text-zinc-300'}`;
        document.getElementById('test-pred-lex-score').innerText = `Skor: ${lex.score}`;
        const matched = (lex.matched_words || []).map(m => `${m.phrase} (${m.adjusted_weight > 0 ? '+' : ''}${m.adjusted_weight}${m.is_negated ? ' negasi' : ''})`).join(', ');
        document.getElementById('test-pred-lex-words').innerText = matched ? `Kata cocok: ${matched}` : 'Tidak ada leksikon cocok';

        // Model 2 SVM
        const svm = data.predictions.linear_svm || {};
        const svmBadge = document.getElementById('test-pred-svm-badge');
        svmBadge.innerText = svm.label;
        svmBadge.className = `px-2 py-0.5 rounded text-[10px] font-bold ${svm.label === 'Negatif' ? 'bg-red-500/20 text-red-300' : svm.label === 'Positif' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-zinc-700 text-zinc-300'}`;
        document.getElementById('test-pred-svm-conf').innerText = `Confidence: ${(svm.confidence * 100).toFixed(1)}%`;
        const probs = Object.entries(svm.probabilities || {}).map(([k, v]) => `${k}: ${(v*100).toFixed(0)}%`).join(' | ');
        document.getElementById('test-pred-svm-probs').innerText = probs;

        // Model 3 Cosine
        const cos = data.predictions.cosine_similarity || {};
        const cosBadge = document.getElementById('test-pred-cos-badge');
        cosBadge.innerText = cos.label;
        cosBadge.className = `px-2 py-0.5 rounded text-[10px] font-bold ${cos.label === 'Negatif' ? 'bg-red-500/20 text-red-300' : cos.label === 'Positif' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-zinc-700 text-zinc-300'}`;
        document.getElementById('test-pred-cos-sim').innerText = `Cosine Sim: ${cos.similarity}`;
        const sims = Object.entries(cos.all_similarities || {}).map(([k, v]) => `${k}: ${v}`).join(' | ');
        document.getElementById('test-pred-cos-sims').innerText = sims;

        showToast('Klasifikasi sentimen berhasil dihitung!', 'success');
      } catch (err) {
        showToast('Gagal memproses prediksi: ' + err.message, 'error');
      } finally {
        btn.innerHTML = origHtml;
        btn.disabled = false;
        lucide.createIcons();
      }
    }
    '''

    if 'function openLaborSentimentDashboard()' not in html:
        # Masukkan sebelum penutup tag script
        html = html.replace('</script>', js_functions + '\n  </script>')

    # Update fungsi resetToDiscovery agar juga menyembunyikan sentiment-research-container
    if "document.getElementById('sentiment-research-container')" not in html:
        old_reset = "function resetToDiscovery() {"
        new_reset = "function resetToDiscovery() {\n      if (document.getElementById('sentiment-research-container')) document.getElementById('sentiment-research-container').classList.add('hidden');"
        html = html.replace(old_reset, new_reset)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Berhasil menginjeksi Dashboard Riset Sentimen ke frontend/dist/index.html!")

if __name__ == "__main__":
    update_index_html()
