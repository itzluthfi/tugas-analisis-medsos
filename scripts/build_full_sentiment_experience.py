import re
import os

def generate_subtab_komparasi():
    return '''        <!-- SUBTAB 1: PERBANDINGAN MULTI-PARADIGMA (6 METODE & BENCHMARK) -->
        <div id="subtab-content-komparasi" class="space-y-6">
          
          <!-- 6 Method Performance Cards -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            
            <!-- InSet Lexicon -->
            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-bold text-slate-500 dark:text-zinc-400 uppercase tracking-wider">Paradigma 1: Lexicon-Based</span>
                <span class="text-xs px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-400 font-semibold font-mono">InSet Lexicon</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-slate-900 dark:text-white">99.19%</div>
                <div class="text-[11px] text-slate-500 dark:text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set N=124)</div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-[#24242c] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Macro F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">98.51%</span>
                </div>
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Weighted F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">99.19%</span>
                </div>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-zinc-400 leading-snug">
                9.083 leksikon bahasa Indonesia dengan aturan inversi jendela kata negasi.
              </p>
            </div>

            <!-- Hybrid SVM -->
            <div class="bg-white dark:bg-[#16161a] border border-emerald-300 dark:border-emerald-800/60 rounded-2xl p-5 shadow-sm space-y-3 relative overflow-hidden">
              <div class="absolute top-0 right-0 bg-emerald-600 text-white text-[9px] font-bold px-2 py-0.5 rounded-bl-lg font-mono">
                TERBAIK ML
              </div>
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider">Paradigma 2: Hybrid ML</span>
                <span class="text-xs px-2 py-0.5 rounded bg-emerald-100 text-emerald-900 dark:bg-emerald-900/40 dark:text-emerald-300 font-semibold font-mono">Hybrid SVM</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-emerald-600 dark:text-emerald-400">92.74%</div>
                <div class="text-[11px] text-slate-500 dark:text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set N=124)</div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-[#24242c] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Macro F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">87.71%</span>
                </div>
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Weighted F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">92.36%</span>
                </div>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-zinc-400 leading-snug">
                Augmentasi fitur TF-IDF n-gram dengan skor valensi leksikon InSet (+22.58% vs baseline SVM!).
              </p>
            </div>

            <!-- Linear SVM Baseline -->
            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-bold text-slate-500 dark:text-zinc-400 uppercase tracking-wider">Paradigma 3: Baseline ML</span>
                <span class="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 dark:bg-[#202028] dark:text-zinc-300 font-semibold font-mono">Linear SVM</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-slate-900 dark:text-white">70.16%</div>
                <div class="text-[11px] text-slate-500 dark:text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set N=124)</div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-[#24242c] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Macro F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">51.74%</span>
                </div>
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Weighted F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">65.74%</span>
                </div>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-zinc-400 leading-snug">
                Pure TF-IDF Unigram/Bigram dengan Support Vector Classifier calibrated Platt scaling.
              </p>
            </div>

            <!-- Cosine Similarity -->
            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-bold text-slate-500 dark:text-zinc-400 uppercase tracking-wider">Paradigma 4: Distance Metric</span>
                <span class="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 dark:bg-[#202028] dark:text-zinc-300 font-semibold font-mono">Cosine Sim</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-slate-900 dark:text-white">67.74%</div>
                <div class="text-[11px] text-slate-500 dark:text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set N=124)</div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-[#24242c] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Macro F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">58.73%</span>
                </div>
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Weighted F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">68.39%</span>
                </div>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-zinc-400 leading-snug">
                Nearest Centroid dalam ruang TF-IDF berdasar sudut kemiripan kosinus L2-normalized.
              </p>
            </div>

            <!-- Deep Learning BiLSTM -->
            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-bold text-slate-500 dark:text-zinc-400 uppercase tracking-wider">Paradigma 5: Deep Learning</span>
                <span class="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 dark:bg-[#202028] dark:text-zinc-300 font-semibold font-mono">Neural BiLSTM</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-slate-900 dark:text-white">64.52%</div>
                <div class="text-[11px] text-slate-500 dark:text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set N=124)</div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-[#24242c] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Macro F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">58.58%</span>
                </div>
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Weighted F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">66.48%</span>
                </div>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-zinc-400 leading-snug">
                Bidirectional LSTM PyTorch dengan Word Attention Pooling untuk visualisasi interpretasi atensi kata.
              </p>
            </div>

            <!-- X-Shot Reasoning -->
            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-bold text-slate-500 dark:text-zinc-400 uppercase tracking-wider">Paradigma 6: X-Shot Learning</span>
                <span class="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 dark:bg-[#202028] dark:text-zinc-300 font-semibold font-mono">Few-Shot CoT</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-slate-900 dark:text-white">73.98%</div>
                <div class="text-[11px] text-slate-500 dark:text-zinc-400 font-medium">Precision Macro (Domain Anchors)</div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-[#24242c] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Akurasi</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">44.35%</span>
                </div>
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block font-mono">Macro F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">39.40%</span>
                </div>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-zinc-400 leading-snug">
                Penalaran kontekstual 4 tahap Chain-of-Thought berdasarkan exemplar polaritas ketenagakerjaan.
              </p>
            </div>

          </div>

          <!-- Comprehensive Multi-Paradigm Comparison Table -->
          <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <h3 class="text-sm font-bold text-slate-900 dark:text-zinc-100 flex items-center gap-2">
                  <i data-lucide="table" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
                  <span>Tabel Komparasi Performa 6 Metode Multi-Paradigma (Test Set N=124)</span>
                </h3>
                <p class="text-xs text-slate-500 dark:text-zinc-400">Evaluasi adil pada partisi data uji identik (20% Stratified Split dari 617 data komentar).</p>
              </div>
              <a href="/api/sentiment/export/evaluation" target="_blank" class="self-start sm:self-auto px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 transition shadow-sm">
                <i data-lucide="download" class="w-3.5 h-3.5"></i>
                <span>Download Laporan (.xlsx)</span>
              </a>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-xs text-left">
                <thead class="bg-slate-50 dark:bg-[#1a1a20] text-slate-600 dark:text-zinc-400 border-b border-slate-200 dark:border-[#2d2d35]">
                  <tr>
                    <th class="px-4 py-3 font-semibold">Paradigma Klasifikasi</th>
                    <th class="px-4 py-3 font-semibold">Metode & Algoritma</th>
                    <th class="px-4 py-3 font-semibold text-center">Akurasi</th>
                    <th class="px-4 py-3 font-semibold text-center">Precision (Macro)</th>
                    <th class="px-4 py-3 font-semibold text-center">Recall (Macro)</th>
                    <th class="px-4 py-3 font-semibold text-center">F1-Score (Macro)</th>
                    <th class="px-4 py-3 font-semibold text-center">F1-Score (Weighted)</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 dark:divide-[#222228] text-slate-700 dark:text-zinc-300">
                  <tr class="hover:bg-slate-50 dark:hover:bg-[#1c1c22] transition bg-emerald-50/30 dark:bg-emerald-950/20">
                    <td class="px-4 py-3 font-medium text-emerald-700 dark:text-emerald-400">Lexicon-Based</td>
                    <td class="px-4 py-3 font-bold text-slate-900 dark:text-zinc-100">InSet Lexicon</td>
                    <td class="px-4 py-3 text-center font-bold text-emerald-700 dark:text-emerald-400">99.19%</td>
                    <td class="px-4 py-3 text-center">98.67%</td>
                    <td class="px-4 py-3 text-center">98.41%</td>
                    <td class="px-4 py-3 text-center font-semibold">98.51%</td>
                    <td class="px-4 py-3 text-center font-semibold">99.19%</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-[#1c1c22] transition bg-emerald-50/10 dark:bg-emerald-950/10">
                    <td class="px-4 py-3 font-medium text-emerald-600 dark:text-emerald-400">Machine Learning (Hybrid)</td>
                    <td class="px-4 py-3 font-bold text-slate-900 dark:text-zinc-100">Hybrid SVM (TF-IDF + InSet)</td>
                    <td class="px-4 py-3 text-center font-bold text-emerald-600 dark:text-emerald-400">92.74%</td>
                    <td class="px-4 py-3 text-center">90.15%</td>
                    <td class="px-4 py-3 text-center">87.30%</td>
                    <td class="px-4 py-3 text-center font-semibold">87.71%</td>
                    <td class="px-4 py-3 text-center font-semibold">92.36%</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-[#1c1c22] transition">
                    <td class="px-4 py-3 font-medium text-slate-500 dark:text-zinc-400">Machine Learning (Baseline)</td>
                    <td class="px-4 py-3 font-semibold text-slate-800 dark:text-zinc-200">Linear SVM</td>
                    <td class="px-4 py-3 text-center font-bold">70.16%</td>
                    <td class="px-4 py-3 text-center">64.66%</td>
                    <td class="px-4 py-3 text-center">49.50%</td>
                    <td class="px-4 py-3 text-center font-semibold">51.74%</td>
                    <td class="px-4 py-3 text-center font-semibold">65.74%</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-[#1c1c22] transition">
                    <td class="px-4 py-3 font-medium text-slate-500 dark:text-zinc-400">Distance Metric</td>
                    <td class="px-4 py-3 font-semibold text-slate-800 dark:text-zinc-200">Cosine Similarity</td>
                    <td class="px-4 py-3 text-center font-bold">67.74%</td>
                    <td class="px-4 py-3 text-center">58.03%</td>
                    <td class="px-4 py-3 text-center">59.67%</td>
                    <td class="px-4 py-3 text-center font-semibold">58.73%</td>
                    <td class="px-4 py-3 text-center font-semibold">68.39%</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-[#1c1c22] transition">
                    <td class="px-4 py-3 font-medium text-slate-500 dark:text-zinc-400">Deep Learning</td>
                    <td class="px-4 py-3 font-semibold text-slate-800 dark:text-zinc-200">Neural BiLSTM (Attention)</td>
                    <td class="px-4 py-3 text-center font-bold">64.52%</td>
                    <td class="px-4 py-3 text-center">58.42%</td>
                    <td class="px-4 py-3 text-center">63.78%</td>
                    <td class="px-4 py-3 text-center font-semibold">58.58%</td>
                    <td class="px-4 py-3 text-center font-semibold">66.48%</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-[#1c1c22] transition">
                    <td class="px-4 py-3 font-medium text-slate-500 dark:text-zinc-400">X-Shot Learning</td>
                    <td class="px-4 py-3 font-semibold text-slate-800 dark:text-zinc-200">X-Shot Reasoning (CoT)</td>
                    <td class="px-4 py-3 text-center font-bold">44.35%</td>
                    <td class="px-4 py-3 text-center">73.98%</td>
                    <td class="px-4 py-3 text-center">48.94%</td>
                    <td class="px-4 py-3 text-center font-semibold">39.40%</td>
                    <td class="px-4 py-3 text-center font-semibold">45.88%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Confusion Matrix Visuals Grid -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <!-- InSet CM -->
            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-zinc-100">1. InSet Lexicon CM</span>
                <span class="text-[10px] text-emerald-700 dark:text-emerald-400 font-mono font-bold">123/124 Benar (99.2%)</span>
              </div>
              <div class="grid grid-cols-4 gap-1 text-[10px] text-center font-mono">
                <div class="text-slate-400 py-0.5">Aktual\Pred</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Neg</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Net</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Pos</div>

                <div class="text-slate-500 text-left pl-1">Neg (79)</div>
                <div class="bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 font-bold py-1 rounded">79</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">0</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">0</div>

                <div class="text-slate-500 text-left pl-1">Net (24)</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">0</div>
                <div class="bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 font-bold py-1 rounded">24</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">0</div>

                <div class="text-slate-500 text-left pl-1">Pos (21)</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">0</div>
                <div class="bg-slate-100 dark:bg-[#25252c] py-1 rounded text-slate-600">1</div>
                <div class="bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 font-bold py-1 rounded">20</div>
              </div>
            </div>

            <!-- Hybrid SVM CM -->
            <div class="bg-white dark:bg-[#16161a] border border-emerald-300 dark:border-emerald-800/60 rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-zinc-100">2. Hybrid SVM CM</span>
                <span class="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono font-bold">115/124 Benar (92.7%)</span>
              </div>
              <div class="grid grid-cols-4 gap-1 text-[10px] text-center font-mono">
                <div class="text-slate-400 py-0.5">Aktual\Pred</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Neg</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Net</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Pos</div>

                <div class="text-slate-500 text-left pl-1">Neg (79)</div>
                <div class="bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 font-bold py-1 rounded">77</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">1</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">1</div>

                <div class="text-slate-500 text-left pl-1">Net (24)</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">4</div>
                <div class="bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 font-bold py-1 rounded">19</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">1</div>

                <div class="text-slate-500 text-left pl-1">Pos (21)</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">2</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded text-slate-400">0</div>
                <div class="bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 font-bold py-1 rounded">19</div>
              </div>
            </div>

            <!-- Linear SVM Baseline CM -->
            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-zinc-100">3. Linear SVM CM</span>
                <span class="text-[10px] text-slate-500 dark:text-zinc-400 font-mono font-bold">87/124 Benar (70.2%)</span>
              </div>
              <div class="grid grid-cols-4 gap-1 text-[10px] text-center font-mono">
                <div class="text-slate-400 py-0.5">Aktual\Pred</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Neg</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Net</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Pos</div>

                <div class="text-slate-500 text-left pl-1">Neg (79)</div>
                <div class="bg-slate-200 dark:bg-[#282832] font-bold py-1 rounded">73</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">1</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">5</div>

                <div class="text-slate-500 text-left pl-1">Net (24)</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">15</div>
                <div class="bg-slate-200 dark:bg-[#282832] font-bold py-1 rounded">8</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">1</div>

                <div class="text-slate-500 text-left pl-1">Pos (21)</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">11</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">4</div>
                <div class="bg-slate-200 dark:bg-[#282832] font-bold py-1 rounded">6</div>
              </div>
            </div>

          </div>

          <!-- Scientific Insights Box for Thesis Defense -->
          <div class="p-5 rounded-2xl bg-slate-100 dark:bg-[#17171c] border border-slate-200 dark:border-[#282830] space-y-3">
            <div class="flex items-center gap-2">
              <i data-lucide="lightbulb" class="w-4 h-4 text-amber-500"></i>
              <h4 class="text-xs font-bold text-slate-900 dark:text-zinc-100">Penjelasan Ilmiah untuk Presentasi & Sidang Skripsi</h4>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-slate-600 dark:text-zinc-400">
              <div class="space-y-1">
                <span class="font-semibold text-slate-800 dark:text-zinc-200 block text-[11px]">Mengapa InSet Lexicon (99.2%) & Hybrid SVM (92.7%) Unggul?</span>
                <p class="text-[11px] leading-relaxed">
                  Kamus InSet memuat 9.083 bobot kata yang dikurasi oleh pakar bahasa, dilengkapi aturan eksplisit jendela negasi <em>(negation window)</em>. Pada dataset 617 data, representasi TF-IDF murni mengalami kelangkaan fitur <em>(sparsity)</em>, namun ketika skor leksikon digabungkan sebagai fitur skalar ke SVM (Hybrid), akurasi melonjak dari 70.16% ke 92.74%!
                </p>
              </div>
              <div class="space-y-1">
                <span class="font-semibold text-slate-800 dark:text-zinc-200 block text-[11px]">Mengapa Deep Learning (BiLSTM 64.5%) Membutuhkan Data Lebih Besar?</span>
                <p class="text-[11px] leading-relaxed">
                  Arsitektur deep learning memiliki parameter bobot embedding dan recurrent cell yang besar. Pada 493 data latih, neural network rentan terhadap ketidakseimbangan kelas (64% Negatif). Ini membuktikan tesis akademik bahwa untuk korpus kecil, pendekatan Lexicon dan Hybrid Feature Engineering jauh lebih efektif daripada Deep Learning tanpa pretraining skala masif.
                </p>
              </div>
            </div>
          </div>

        </div>'''

def generate_subtab_dataset():
    return '''        <!-- SUBTAB 2: TABEL & BUKTI GROUND TRUTH DATASET (617 DATA) -->
        <div id="subtab-content-dataset" class="hidden space-y-4">
          <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-4">
            
            <div class="flex flex-col sm:flex-row items-center justify-between gap-3">
              <div>
                <h3 class="text-sm font-bold text-slate-900 dark:text-zinc-100 flex items-center gap-2">
                  <i data-lucide="database" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
                  <span>Tabel Bukti Ground Truth & Prediksi 5 Model (N=617)</span>
                </h3>
                <p class="text-xs text-slate-500 dark:text-zinc-400">Data komentar riil publik dilengkapi teks asli, hasil stemming Sastrawi, target ground truth, dan status tebakan tiap model.</p>
              </div>

              <div class="flex items-center gap-2">
                <a href="/api/sentiment/export/dataset?format=xlsx" target="_blank" class="px-2.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 transition shadow-sm">
                  <i data-lucide="file-spreadsheet" class="w-3.5 h-3.5"></i>
                  <span>Download Excel (.xlsx)</span>
                </a>
                <a href="/api/sentiment/export/dataset?format=csv" target="_blank" class="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#202028] dark:hover:bg-[#282832] text-slate-700 dark:text-zinc-200 border border-slate-300 dark:border-[#2d2d35] text-xs font-medium flex items-center gap-1.5 transition">
                  <i data-lucide="file-text" class="w-3.5 h-3.5"></i>
                  <span>CSV</span>
                </a>
              </div>
            </div>

            <!-- Filters & Status Auditing Controls -->
            <div class="space-y-2.5 pt-1 text-xs">
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                <input id="ds-filter-query" onkeyup="if(event.key==='Enter') applyDatasetFilters()" type="text" placeholder="Cari kata kunci (misal: phk, batas usia, sarjana, pabrik)..." class="bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-3 py-2 text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500" />
                
                <select id="ds-filter-sentiment" onchange="applyDatasetFilters()" class="bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-3 py-2 text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500">
                  <option value="all">Semua Kelas Sentimen</option>
                  <option value="negatif">Hanya Negatif (393)</option>
                  <option value="netral">Hanya Netral (117)</option>
                  <option value="positif">Hanya Positif (107)</option>
                </select>

                <select id="ds-filter-status" onchange="applyDatasetFilters()" class="bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-3 py-2 text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500 font-medium">
                  <option value="all">Semua Hasil Tebakan (617 Data)</option>
                  <option value="mismatch">Hanya Yang Ada Miskalsifikasi / Salah Tebak</option>
                  <option value="all_correct">Hanya Yang Kompak Benar</option>
                  <option value="mismatch_svm">Hanya Baseline SVM Salah</option>
                  <option value="mismatch_hybrid">Hanya Hybrid SVM Salah</option>
                  <option value="mismatch_bilstm">Hanya Deep Learning BiLSTM Salah</option>
                  <option value="mismatch_cosine">Hanya Cosine Sim Salah</option>
                  <option value="mismatch_lexicon">Hanya InSet Lexicon Salah</option>
                </select>
              </div>

              <!-- Legend & Split Filter Row -->
              <div class="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-100 dark:border-[#222228] text-xs">
                <!-- Status Legend -->
                <div class="flex flex-wrap items-center gap-2.5 text-[11px]">
                  <span class="text-slate-500 dark:text-zinc-400 font-medium">Legenda Bukti:</span>
                  <span class="inline-flex items-center gap-1 text-emerald-700 dark:text-emerald-300 font-semibold bg-emerald-50 dark:bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-200 dark:border-emerald-800/40">
                    <i data-lucide="check" class="w-3 h-3 text-emerald-600 dark:text-emerald-400"></i>
                    <span>Tebakan Sesuai Ground Truth</span>
                  </span>
                  <span class="inline-flex items-center gap-1 text-rose-700 dark:text-rose-300 font-semibold bg-rose-50 dark:bg-rose-950/40 px-2 py-0.5 rounded border border-rose-200 dark:border-rose-800/40">
                    <i data-lucide="x" class="w-3 h-3 text-rose-600 dark:text-rose-400"></i>
                    <span>Meleset (Miskalsifikasi)</span>
                  </span>
                  <span class="inline-flex items-center gap-1 text-slate-700 dark:text-zinc-300 font-semibold bg-slate-100 dark:bg-[#202028] px-2 py-0.5 rounded border border-slate-200 dark:border-[#2d2d35]">
                    <i data-lucide="target" class="w-3 h-3 text-slate-500"></i>
                    <span>Ground Truth (Acuan)</span>
                  </span>
                </div>

                <!-- Partition Split Selector -->
                <div class="flex items-center gap-2">
                  <span class="text-[11px] text-slate-500 dark:text-zinc-400">Partisi:</span>
                  <select id="ds-filter-split" onchange="applyDatasetFilters()" class="bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-2.5 py-1 text-xs text-slate-800 dark:text-zinc-200 focus:outline-none focus:border-emerald-500 font-mono">
                    <option value="all">Semua (Train 80% & Test 20%)</option>
                    <option value="test">Hanya Data Uji / Test Set (124)</option>
                    <option value="train">Hanya Data Latih / Train Set (493)</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Data Table with all models -->
            <div class="overflow-x-auto border border-slate-200 dark:border-[#2d2d35] rounded-xl max-h-[540px]">
              <table class="w-full text-xs text-left">
                <thead class="bg-slate-50 dark:bg-[#1a1a20] text-slate-600 dark:text-zinc-400 sticky top-0 z-10 border-b border-slate-200 dark:border-[#2d2d35]">
                  <tr>
                    <th class="px-3 py-2.5 font-semibold w-10">No</th>
                    <th class="px-3 py-2.5 font-semibold min-w-[260px]">Komentar Netizen Asli</th>
                    <th class="px-3 py-2.5 font-semibold min-w-[170px]">Stemming Sastrawi</th>
                    <th class="px-3 py-2.5 font-semibold text-center min-w-[120px]">
                      <div class="flex items-center justify-center gap-1">
                        <i data-lucide="target" class="w-3.5 h-3.5 text-slate-500"></i>
                        <span>Ground Truth</span>
                      </div>
                    </th>
                    <th class="px-3 py-2.5 font-semibold text-center min-w-[130px]">
                      <div>InSet Lexicon</div>
                      <span class="text-[9px] font-mono font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-1.5 py-0.2 rounded border border-emerald-200 dark:border-emerald-800/40">99.2%</span>
                    </th>
                    <th class="px-3 py-2.5 font-semibold text-center min-w-[130px]">
                      <div>Hybrid SVM</div>
                      <span class="text-[9px] font-mono font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-1.5 py-0.2 rounded border border-emerald-200 dark:border-emerald-800/40">92.7%</span>
                    </th>
                    <th class="px-3 py-2.5 font-semibold text-center min-w-[120px]">
                      <div>Linear SVM</div>
                      <span class="text-[9px] font-mono font-bold text-slate-600 dark:text-zinc-400 bg-slate-100 dark:bg-[#202028] px-1.5 py-0.2 rounded border border-slate-200 dark:border-[#2d2d35]">70.2%</span>
                    </th>
                    <th class="px-3 py-2.5 font-semibold text-center min-w-[120px]">
                      <div>Cosine Sim</div>
                      <span class="text-[9px] font-mono font-bold text-slate-600 dark:text-zinc-400 bg-slate-100 dark:bg-[#202028] px-1.5 py-0.2 rounded border border-slate-200 dark:border-[#2d2d35]">67.7%</span>
                    </th>
                    <th class="px-3 py-2.5 font-semibold text-center min-w-[120px]">
                      <div>BiLSTM</div>
                      <span class="text-[9px] font-mono font-bold text-slate-600 dark:text-zinc-400 bg-slate-100 dark:bg-[#202028] px-1.5 py-0.2 rounded border border-slate-200 dark:border-[#2d2d35]">64.5%</span>
                    </th>
                    <th class="px-3 py-2.5 font-semibold text-center w-20">Partisi</th>
                  </tr>
                </thead>
                <tbody id="ds-table-body" class="divide-y divide-slate-100 dark:divide-[#222228] text-slate-700 dark:text-zinc-300">
                  <tr>
                    <td colspan="10" class="px-4 py-8 text-center text-slate-400 dark:text-zinc-500">Memuat data komentar...</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination Bar -->
            <div class="flex items-center justify-between text-xs pt-2">
              <span id="ds-pagination-info" class="text-slate-500 dark:text-zinc-400">Menampilkan 1 - 20 dari 617 data</span>
              <div class="flex items-center gap-2">
                <button id="ds-prev-btn" onclick="changeDatasetPage(-1)" class="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-[#202028] hover:bg-slate-200 dark:hover:bg-[#282832] text-slate-700 dark:text-zinc-300 disabled:opacity-40 transition">Sebelumnya</button>
                <span id="ds-current-page" class="px-2 font-mono font-semibold text-slate-800 dark:text-zinc-200">1</span>
                <button id="ds-next-btn" onclick="changeDatasetPage(1)" class="px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-[#202028] hover:bg-slate-200 dark:hover:bg-[#282832] text-slate-700 dark:text-zinc-300 disabled:opacity-40 transition">Berikutnya</button>
              </div>
            </div>

          </div>
        </div>'''

def generate_subtab_simulator():
    return '''        <!-- SUBTAB 3: INTERACTIVE STEP-BY-STEP PIPELINE SIMULATOR -->
        <div id="subtab-content-simulator" class="hidden space-y-4">
          <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-5">
            
            <div>
              <h3 class="text-sm font-bold text-slate-900 dark:text-zinc-100 flex items-center gap-2">
                <i data-lucide="play-circle" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
                <span>Simulator Prapemrosesan & Inferensi Multi-Paradigma Realtime</span>
              </h3>
              <p class="text-xs text-slate-500 dark:text-zinc-400">Uji langsung setiap tahapan transformasi teks dari kalimat mentah hingga klasifikasi komparatif 6 metode secara bertahap.</p>
            </div>

            <!-- Sample Chips -->
            <div class="space-y-1.5">
              <span class="text-[11px] text-slate-500 dark:text-zinc-400">Pilih skenario contoh:</span>
              <div class="flex flex-wrap gap-2 text-xs">
                <button onclick="setSimulatorSample(1)" class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-[#1c1c22] hover:bg-slate-200 dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] text-[11px] transition text-left">
                  "Susah bgt nyari loker sekarang, kena phk massal dan batas usia max 25 thn!"
                </button>
                <button onclick="setSimulatorSample(2)" class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-[#1c1c22] hover:bg-slate-200 dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] text-[11px] transition text-left">
                  "Gaji tidak sebanding beban rodi, lembur tidak dibayar dan tidak ada bonus."
                </button>
                <button onclick="setSimulatorSample(3)" class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-[#1c1c22] hover:bg-slate-200 dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] text-[11px] transition text-left">
                  "Alhamdulillah dapat panggilan kerja setelah ikut pelatihan vokasi, optimis dan semangat!"
                </button>
                <button onclick="setSimulatorSample(4)" class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-[#1c1c22] hover:bg-slate-200 dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] text-[11px] transition text-left">
                  "Kemnaker merilis statistik resmi tingkat pengangguran terbuka periode triwulan ini."
                </button>
              </div>
            </div>

            <!-- Input Box & Actions -->
            <div class="space-y-2">
              <textarea id="sim-input-text" rows="3" placeholder="Ketik atau tempel opini publik mengenai ketenagakerjaan di sini..." class="w-full bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-xl p-3 text-xs text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500 leading-relaxed"></textarea>
              <div class="flex items-center justify-between pt-1">
                <span class="text-[10px] text-slate-400 dark:text-zinc-500">Mendukung slang bahasa gaul, singkatan, tanda baca tidak baku, dan negasi kompleks.</span>
                <div class="flex items-center gap-2">
                  <button id="btn-run-sim-full" onclick="runPipelineSimulation(true)" class="px-4 py-2 rounded-xl bg-zinc-900 hover:bg-zinc-800 dark:bg-white dark:hover:bg-zinc-200 text-white dark:text-zinc-900 font-semibold text-xs flex items-center gap-2 transition shadow">
                    <i data-lucide="play" class="w-3.5 h-3.5"></i>
                    <span>Jalankan Simulasi Penuh</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- Interactive Stepper Navigation (Visual Progress) -->
            <div id="sim-stepper-bar" class="hidden flex items-center justify-between gap-1 p-1 bg-slate-100 dark:bg-[#141418] rounded-xl border border-slate-200 dark:border-[#25252c] overflow-x-auto text-[11px]">
              <button onclick="goToSimStep(1)" id="sim-step-btn-1" class="px-3 py-1.5 rounded-lg font-semibold bg-white dark:bg-[#22222a] text-slate-900 dark:text-white transition flex items-center gap-1.5 shrink-0 shadow-sm">
                <span class="w-4 h-4 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px]">1</span>
                <span>Teks Asli</span>
              </button>
              <button onclick="goToSimStep(2)" id="sim-step-btn-2" class="px-3 py-1.5 rounded-lg text-slate-500 dark:text-zinc-400 hover:text-slate-800 transition flex items-center gap-1.5 shrink-0">
                <span class="w-4 h-4 rounded-full bg-slate-300 dark:bg-zinc-700 text-slate-700 dark:text-zinc-300 flex items-center justify-center text-[10px]">2</span>
                <span>Case Folding</span>
              </button>
              <button onclick="goToSimStep(3)" id="sim-step-btn-3" class="px-3 py-1.5 rounded-lg text-slate-500 dark:text-zinc-400 hover:text-slate-800 transition flex items-center gap-1.5 shrink-0">
                <span class="w-4 h-4 rounded-full bg-slate-300 dark:bg-zinc-700 text-slate-700 dark:text-zinc-300 flex items-center justify-center text-[10px]">3</span>
                <span>Normalisasi Slang</span>
              </button>
              <button onclick="goToSimStep(4)" id="sim-step-btn-4" class="px-3 py-1.5 rounded-lg text-slate-500 dark:text-zinc-400 hover:text-slate-800 transition flex items-center gap-1.5 shrink-0">
                <span class="w-4 h-4 rounded-full bg-slate-300 dark:bg-zinc-700 text-slate-700 dark:text-zinc-300 flex items-center justify-center text-[10px]">4</span>
                <span>Stopwords Negasi</span>
              </button>
              <button onclick="goToSimStep(5)" id="sim-step-btn-5" class="px-3 py-1.5 rounded-lg text-slate-500 dark:text-zinc-400 hover:text-slate-800 transition flex items-center gap-1.5 shrink-0">
                <span class="w-4 h-4 rounded-full bg-slate-300 dark:bg-zinc-700 text-slate-700 dark:text-zinc-300 flex items-center justify-center text-[10px]">5</span>
                <span>Stemming Sastrawi</span>
              </button>
              <button onclick="goToSimStep(6)" id="sim-step-btn-6" class="px-3 py-1.5 rounded-lg text-slate-500 dark:text-zinc-400 hover:text-slate-800 transition flex items-center gap-1.5 shrink-0">
                <span class="w-4 h-4 rounded-full bg-slate-300 dark:bg-zinc-700 text-slate-700 dark:text-zinc-300 flex items-center justify-center text-[10px]">6</span>
                <span>Hasil 6 Metode</span>
              </button>
            </div>

            <!-- Simulator Step Card Containers -->
            <div id="sim-step-container" class="hidden space-y-4">
              
              <!-- STEP 1 CARD -->
              <div id="sim-card-1" class="p-4 rounded-xl bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#25252c] space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-slate-800 dark:text-zinc-200 flex items-center gap-2">
                    <i data-lucide="file-text" class="w-4 h-4 text-emerald-600"></i>
                    <span>Tahap 1: Teks Masukan Mentah (Raw Input)</span>
                  </span>
                  <span class="text-[10px] text-slate-400 font-mono" id="sim-raw-len"></span>
                </div>
                <div class="p-3 bg-white dark:bg-[#1a1a20] rounded-lg border border-slate-200 dark:border-[#2b2b35] text-xs font-sans text-slate-800 dark:text-zinc-200" id="sim-raw-text"></div>
                <p class="text-[11px] text-slate-500 dark:text-zinc-400">Komentar publik langsung dari media sosial tanpa modifikasi apa pun.</p>
              </div>

              <!-- STEP 2 CARD -->
              <div id="sim-card-2" class="p-4 rounded-xl bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#25252c] space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-slate-800 dark:text-zinc-200 flex items-center gap-2">
                    <i data-lucide="type" class="w-4 h-4 text-emerald-600"></i>
                    <span>Tahap 2: Pembersihan Tanda Baca & Case Folding</span>
                  </span>
                  <span class="text-[10px] px-2 py-0.5 rounded bg-slate-200 dark:bg-zinc-800 text-slate-700 dark:text-zinc-300 font-mono">Lowercase + Regex Clean</span>
                </div>
                <div class="p-3 bg-white dark:bg-[#1a1a20] rounded-lg border border-slate-200 dark:border-[#2b2b35] text-xs font-mono text-slate-800 dark:text-zinc-200" id="sim-folded-text"></div>
                <p class="text-[11px] text-slate-500 dark:text-zinc-400">Menghapus URL, hashtag, mention, angka, simbol khusus, serta mengubah seluruh karakter menjadi huruf kecil.</p>
              </div>

              <!-- STEP 3 CARD -->
              <div id="sim-card-3" class="p-4 rounded-xl bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#25252c] space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-slate-800 dark:text-zinc-200 flex items-center gap-2">
                    <i data-lucide="book-check" class="w-4 h-4 text-emerald-600"></i>
                    <span>Tahap 3: Normalisasi Bahasa Alay / Slang (Colloquial Lexicon)</span>
                  </span>
                  <span id="sim-slang-count-badge" class="text-[10px] px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-400 font-mono font-bold"></span>
                </div>
                <div id="sim-slang-badges" class="flex flex-wrap gap-2 text-[11px]"></div>
                <div class="p-3 bg-white dark:bg-[#1a1a20] rounded-lg border border-slate-200 dark:border-[#2b2b35] text-xs font-mono text-slate-800 dark:text-zinc-200" id="sim-norm-text"></div>
                <p class="text-[11px] text-slate-500 dark:text-zinc-400">Memetakan 15.006 entri kamus kata alay bahasa Indonesia ke bentuk formal agar dapat dipahami leksikon dan algoritma pembobot kata.</p>
              </div>

              <!-- STEP 4 CARD -->
              <div id="sim-card-4" class="p-4 rounded-xl bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#25252c] space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-slate-800 dark:text-zinc-200 flex items-center gap-2">
                    <i data-lucide="shield-check" class="w-4 h-4 text-emerald-600"></i>
                    <span>Tahap 4: Stopword Removal Berbasis Proteksi Kata Negasi</span>
                  </span>
                  <span class="text-[10px] px-2 py-0.5 rounded bg-slate-200 dark:bg-zinc-800 text-slate-700 dark:text-zinc-300 font-mono">Negation Preserved</span>
                </div>
                <div class="space-y-2">
                  <div class="flex flex-wrap items-center gap-1.5 text-[11px]" id="sim-stop-removed-box"></div>
                </div>
                <div class="p-3 bg-white dark:bg-[#1a1a20] rounded-lg border border-slate-200 dark:border-[#2b2b35] text-xs font-mono text-slate-800 dark:text-zinc-200" id="sim-stop-text"></div>
                <p class="text-[11px] text-slate-500 dark:text-zinc-400">Kata umum dibuang untuk efisiensi ruang fitur, namun kata negasi (tidak, belum, bukan, jangan) secara mutlak dipertahankan agar polaritas kalimat tidak terbalik.</p>
              </div>

              <!-- STEP 5 CARD -->
              <div id="sim-card-5" class="p-4 rounded-xl bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#25252c] space-y-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-slate-800 dark:text-zinc-200 flex items-center gap-2">
                    <i data-lucide="git-commit" class="w-4 h-4 text-emerald-600"></i>
                    <span>Tahap 5: Stemming Sastrawi Berbasis Memoization Cache</span>
                  </span>
                  <span id="sim-stem-count-badge" class="text-[10px] px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-400 font-mono font-bold"></span>
                </div>
                <div id="sim-stem-badges" class="flex flex-wrap gap-2 text-[11px]"></div>
                <div class="p-3 bg-white dark:bg-[#1a1a20] rounded-lg border border-slate-200 dark:border-[#2b2b35] text-xs font-mono font-semibold text-emerald-700 dark:text-emerald-400" id="sim-stem-text"></div>
                <p class="text-[11px] text-slate-500 dark:text-zinc-400">Mengubah kata berimbuhan menjadi bentuk dasarnya menggunakan algoritma Nazief-Adriani melalui PySastrawi dengan O(1) in-memory cache.</p>
              </div>

              <!-- STEP 6 CARD: MULTI-PARADIGM 6-MODEL COMPARATIVE OUTPUT -->
              <div id="sim-card-6" class="space-y-4">
                
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold text-slate-900 dark:text-zinc-100 flex items-center gap-2">
                    <i data-lucide="layers" class="w-4 h-4 text-emerald-600"></i>
                    <span>Tahap 6: Prediksi Komparatif 6 Metode Multi-Paradigma</span>
                  </span>
                  <span class="text-[10px] text-slate-400 font-mono">Live Multi-Model Output</span>
                </div>

                <!-- 6 Model Grid Cards -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                  
                  <!-- InSet Lexicon -->
                  <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-xl p-4 space-y-2 shadow-sm">
                    <div class="flex items-center justify-between">
                      <span class="font-bold text-slate-800 dark:text-zinc-200">1. InSet Lexicon</span>
                      <span id="sim-res-lex-badge" class="px-2 py-0.5 rounded text-[10px] font-bold font-mono"></span>
                    </div>
                    <div class="text-lg font-extrabold text-slate-900 dark:text-white" id="sim-res-lex-score"></div>
                    <div class="text-[10px] text-slate-500 dark:text-zinc-400 max-h-16 overflow-y-auto" id="sim-res-lex-words"></div>
                  </div>

                  <!-- Hybrid SVM -->
                  <div class="bg-white dark:bg-[#16161a] border border-emerald-300 dark:border-emerald-800/60 rounded-xl p-4 space-y-2 shadow-sm">
                    <div class="flex items-center justify-between">
                      <span class="font-bold text-emerald-700 dark:text-emerald-400">2. Hybrid SVM (Unggulan)</span>
                      <span id="sim-res-hyb-badge" class="px-2 py-0.5 rounded text-[10px] font-bold font-mono"></span>
                    </div>
                    <div class="text-lg font-extrabold text-emerald-600 dark:text-emerald-400" id="sim-res-hyb-conf"></div>
                    <div class="text-[10px] text-slate-500 dark:text-zinc-400" id="sim-res-hyb-probs"></div>
                  </div>

                  <!-- Linear SVM Baseline -->
                  <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-xl p-4 space-y-2 shadow-sm">
                    <div class="flex items-center justify-between">
                      <span class="font-bold text-slate-800 dark:text-zinc-200">3. Linear SVM (TF-IDF)</span>
                      <span id="sim-res-svm-badge" class="px-2 py-0.5 rounded text-[10px] font-bold font-mono"></span>
                    </div>
                    <div class="text-lg font-extrabold text-slate-900 dark:text-white" id="sim-res-svm-conf"></div>
                    <div class="text-[10px] text-slate-500 dark:text-zinc-400" id="sim-res-svm-probs"></div>
                  </div>

                  <!-- Cosine Similarity -->
                  <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-xl p-4 space-y-2 shadow-sm">
                    <div class="flex items-center justify-between">
                      <span class="font-bold text-slate-800 dark:text-zinc-200">4. Cosine Similarity</span>
                      <span id="sim-res-cos-badge" class="px-2 py-0.5 rounded text-[10px] font-bold font-mono"></span>
                    </div>
                    <div class="text-lg font-extrabold text-slate-900 dark:text-white" id="sim-res-cos-sim"></div>
                    <div class="text-[10px] text-slate-500 dark:text-zinc-400" id="sim-res-cos-sims"></div>
                  </div>

                  <!-- Neural BiLSTM -->
                  <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-xl p-4 space-y-2 shadow-sm">
                    <div class="flex items-center justify-between">
                      <span class="font-bold text-slate-800 dark:text-zinc-200">5. Neural BiLSTM</span>
                      <span id="sim-res-bilstm-badge" class="px-2 py-0.5 rounded text-[10px] font-bold font-mono"></span>
                    </div>
                    <div class="text-lg font-extrabold text-slate-900 dark:text-white" id="sim-res-bilstm-conf"></div>
                    <div class="text-[10px] text-slate-500 dark:text-zinc-400" id="sim-res-bilstm-probs"></div>
                  </div>

                  <!-- X-Shot Reasoning -->
                  <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-xl p-4 space-y-2 shadow-sm">
                    <div class="flex items-center justify-between">
                      <span class="font-bold text-slate-800 dark:text-zinc-200">6. X-Shot CoT</span>
                      <span id="sim-res-xshot-badge" class="px-2 py-0.5 rounded text-[10px] font-bold font-mono"></span>
                    </div>
                    <div class="text-lg font-extrabold text-slate-900 dark:text-white" id="sim-res-xshot-conf"></div>
                    <div class="text-[10px] text-slate-500 dark:text-zinc-400 truncate" id="sim-res-xshot-exemplar"></div>
                  </div>

                </div>

                <!-- Neural Word Attention Heatmap Section -->
                <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#25252c] space-y-2.5">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-800 dark:text-zinc-200 flex items-center gap-2">
                      <i data-lucide="eye" class="w-3.5 h-3.5 text-emerald-600"></i>
                      <span>Visualisasi Bobot Perhatian Kata (BiLSTM Word Attention Weights)</span>
                    </span>
                    <span class="text-[10px] text-slate-400 font-mono">Explainable AI</span>
                  </div>
                  <div id="sim-bilstm-attention-tokens" class="flex flex-wrap gap-2 text-xs font-mono p-3 bg-white dark:bg-[#1a1a20] rounded-lg border border-slate-200 dark:border-[#2a2a34]"></div>
                  <p class="text-[10px] text-slate-400 leading-tight">Kata dengan latar belakang lebih tebal menunjukkan bobot atensi temporal yang lebih tinggi pada mekanisme Softmax Attention BiLSTM.</p>
                </div>

                <!-- X-Shot Reasoning Chain-of-Thought (CoT) Bullets -->
                <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#25252c] space-y-2.5">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-800 dark:text-zinc-200 flex items-center gap-2">
                      <i data-lucide="cpu" class="w-3.5 h-3.5 text-emerald-600"></i>
                      <span>Alur Penalaran Berpikir (Chain-of-Thought Rationale)</span>
                    </span>
                    <span class="text-[10px] text-slate-400 font-mono">Semantic Reasoning</span>
                  </div>
                  <div id="sim-xshot-cot-list" class="space-y-1.5 text-[11px] font-sans"></div>
                </div>

              </div>

            </div>

          </div>
        </div>'''

def generate_subtab_flowchart():
    return '''        <!-- SUBTAB 4: DIAGRAM ALIR & ARSITEKTUR SISTEM (PRESENTASI & SIDANG) -->
        <div id="subtab-content-flowchart" class="hidden space-y-4">
          <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-5">
            
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <h3 class="text-sm font-bold text-slate-900 dark:text-zinc-100 flex items-center gap-2">
                  <i data-lucide="git-fork" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
                  <span>Diagram Alir & Arsitektur Sistem Penelitian (Ready for Presentation)</span>
                </h3>
                <p class="text-xs text-slate-500 dark:text-zinc-400">Visualisasi arsitektur komputasi untuk bahan presentasi slide dan sidang skripsi.</p>
              </div>
              <div class="flex items-center gap-2 text-xs">
                <button onclick="switchFlowchartView('e2e')" id="fc-btn-e2e" class="px-3 py-1.5 rounded-lg font-semibold bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 transition">End-to-End System</button>
                <button onclick="switchFlowchartView('hybrid')" id="fc-btn-hybrid" class="px-3 py-1.5 rounded-lg text-slate-600 dark:text-zinc-400 hover:bg-slate-100 dark:hover:bg-[#202028] transition">Hybrid SVM</button>
                <button onclick="switchFlowchartView('bilstm')" id="fc-btn-bilstm" class="px-3 py-1.5 rounded-lg text-slate-600 dark:text-zinc-400 hover:bg-slate-100 dark:hover:bg-[#202028] transition">Neural BiLSTM</button>
              </div>
            </div>

            <!-- VIEW 1: END-TO-END SYSTEM FLOWCHART -->
            <div id="fc-view-e2e" class="space-y-4">
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#262630] space-y-4">
                <span class="text-xs font-bold text-slate-800 dark:text-zinc-200 uppercase tracking-wider block font-mono">Diagram Alir Sistem Utama</span>
                
                <!-- Flow Stepper Boxes in Flowchart Layout -->
                <div class="grid grid-cols-1 md:grid-cols-5 gap-3 text-xs">
                  
                  <!-- Stage 1 -->
                  <div class="p-3 bg-white dark:bg-[#1a1a20] rounded-xl border border-slate-200 dark:border-[#2d2d35] space-y-2 relative shadow-sm">
                    <div class="flex items-center justify-between">
                      <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-100 dark:bg-zinc-800 text-slate-600 dark:text-zinc-300 font-mono">Tahap 1</span>
                      <i data-lucide="download-cloud" class="w-3.5 h-3.5 text-emerald-600"></i>
                    </div>
                    <h5 class="font-bold text-slate-900 dark:text-zinc-100 text-[11px]">Pengumpulan Data</h5>
                    <p class="text-[10px] text-slate-500 dark:text-zinc-400 leading-tight">Scraping 617 opini riil YouTube (CNBC, Kompas TV, Metro TV, CNA Insider) via direct API.</p>
                  </div>

                  <!-- Stage 2 -->
                  <div class="p-3 bg-white dark:bg-[#1a1a20] rounded-xl border border-slate-200 dark:border-[#2d2d35] space-y-2 relative shadow-sm">
                    <div class="flex items-center justify-between">
                      <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-100 dark:bg-zinc-800 text-slate-600 dark:text-zinc-300 font-mono">Tahap 2</span>
                      <i data-lucide="filter" class="w-3.5 h-3.5 text-emerald-600"></i>
                    </div>
                    <h5 class="font-bold text-slate-900 dark:text-zinc-100 text-[11px]">5-Stage NLP Prep</h5>
                    <p class="text-[10px] text-slate-500 dark:text-zinc-400 leading-tight">Case folding, tokenisasi, 15k slang normalization, stopword penjaga negasi, & Sastrawi cache.</p>
                  </div>

                  <!-- Stage 3 -->
                  <div class="p-3 bg-white dark:bg-[#1a1a20] rounded-xl border border-slate-200 dark:border-[#2d2d35] space-y-2 relative shadow-sm">
                    <div class="flex items-center justify-between">
                      <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-100 dark:bg-zinc-800 text-slate-600 dark:text-zinc-300 font-mono">Tahap 3</span>
                      <i data-lucide="binary" class="w-3.5 h-3.5 text-emerald-600"></i>
                    </div>
                    <h5 class="font-bold text-slate-900 dark:text-zinc-100 text-[11px]">Feature Extraction</h5>
                    <p class="text-[10px] text-slate-500 dark:text-zinc-400 leading-tight">TF-IDF unigram & bigram, InSet score scalar, integer sequence encoding, & domain anchors.</p>
                  </div>

                  <!-- Stage 4 -->
                  <div class="p-3 bg-white dark:bg-[#1a1a20] rounded-xl border border-slate-200 dark:border-[#2d2d35] space-y-2 relative shadow-sm">
                    <div class="flex items-center justify-between">
                      <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-100 dark:bg-zinc-800 text-slate-600 dark:text-zinc-300 font-mono">Tahap 4</span>
                      <i data-lucide="cpu" class="w-3.5 h-3.5 text-emerald-600"></i>
                    </div>
                    <h5 class="font-bold text-slate-900 dark:text-zinc-100 text-[11px]">Klasifikasi Multi-Model</h5>
                    <p class="text-[10px] text-slate-500 dark:text-zinc-400 leading-tight">InSet, Hybrid SVM, Linear SVM, Cosine Similarity, PyTorch BiLSTM, & X-Shot CoT.</p>
                  </div>

                  <!-- Stage 5 -->
                  <div class="p-3 bg-white dark:bg-[#1a1a20] rounded-xl border border-emerald-300 dark:border-emerald-800 rounded-xl space-y-2 relative shadow-sm bg-emerald-50/20 dark:bg-emerald-950/20">
                    <div class="flex items-center justify-between">
                      <span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-300 font-mono">Tahap 5</span>
                      <i data-lucide="check-circle" class="w-3.5 h-3.5 text-emerald-600"></i>
                    </div>
                    <h5 class="font-bold text-slate-900 dark:text-zinc-100 text-[11px]">Evaluasi & Bukti</h5>
                    <p class="text-[10px] text-slate-500 dark:text-zinc-400 leading-tight">Perbandingan metrik adil, confusion matrix, audit miskalsifikasi, & ekspor data excel.</p>
                  </div>

                </div>
              </div>
            </div>

            <!-- VIEW 2: HYBRID SVM FLOWCHART -->
            <div id="fc-view-hybrid" class="hidden space-y-4">
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#262630] space-y-3">
                <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider block font-mono">Arsitektur & Formulasi Hybrid Feature SVM (Akurasi 92.74%)</span>
                <div class="p-4 bg-white dark:bg-[#1a1a20] rounded-xl border border-slate-200 dark:border-[#2d2d35] space-y-3 text-xs text-slate-700 dark:text-zinc-300 leading-relaxed">
                  <div class="font-mono text-[11px] bg-slate-100 dark:bg-[#202028] p-3 rounded-lg border border-slate-200 dark:border-[#2d2d35] text-slate-800 dark:text-zinc-200">
                    X_hybrid = [ TF-IDF_Matrix (Sparse, Unigram+Bigram)  &oplus;  StandardScaler(InSet_Valence_Score) (Dense) ]
                  </div>
                  <p class="text-[11px]">
                    <strong>Masalah di korpus kecil (493 sampel latih):</strong> Ruang vektor TF-IDF sangat renggang (sparse) dan model ML murni cenderung mengabaikan urutan kata serta memprediksi kelas mayoritas (Negatif).
                  </p>
                  <p class="text-[11px]">
                    <strong>Solusi Hybrid Feature Engineering:</strong> Fitur valensi dari InSet Lexicon disisipkan ke dalam ruang fitur SVM. Hal ini memberikan sinyal polaritas kuat yang membimbing hyperplane pemisah kelas secara optimal, menghasilkan lonjakan akurasi dari <strong>70.16% &rarr; 92.74%</strong>.
                  </p>
                </div>
              </div>
            </div>

            <!-- VIEW 3: NEURAL BILSTM ATTENTION FLOWCHART -->
            <div id="fc-view-bilstm" class="hidden space-y-4">
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#262630] space-y-3">
                <span class="text-xs font-bold text-slate-800 dark:text-zinc-200 uppercase tracking-wider block font-mono">Arsitektur Neural BiLSTM dengan Word-Level Attention Pooling</span>
                <div class="p-4 bg-white dark:bg-[#1a1a20] rounded-xl border border-slate-200 dark:border-[#2d2d35] space-y-3 text-xs text-slate-700 dark:text-zinc-300 leading-relaxed">
                  <div class="grid grid-cols-1 md:grid-cols-4 gap-2 text-[11px] font-mono text-center">
                    <div class="p-2.5 bg-slate-100 dark:bg-[#202028] rounded border border-slate-200 dark:border-[#2a2a34]">
                      1. Token Embedding<br/><span class="text-[9px] text-slate-400">Dimensi d=64</span>
                    </div>
                    <div class="p-2.5 bg-slate-100 dark:bg-[#202028] rounded border border-slate-200 dark:border-[#2a2a34]">
                      2. Bidirectional LSTM<br/><span class="text-[9px] text-slate-400">h_forward & h_backward</span>
                    </div>
                    <div class="p-2.5 bg-slate-100 dark:bg-[#202028] rounded border border-slate-200 dark:border-[#2a2a34]">
                      3. Attention Weights (&alpha;_t)<br/><span class="text-[9px] text-slate-400">c = &Sigma; &alpha;_t h_t</span>
                    </div>
                    <div class="p-2.5 bg-slate-100 dark:bg-[#202028] rounded border border-slate-200 dark:border-[#2a2a34]">
                      4. Dense Classification<br/><span class="text-[9px] text-slate-400">Softmax 3 Kelas</span>
                    </div>
                  </div>
                  <p class="text-[11px]">
                    Attention layer menghitung bobot signifikansi polaritas untuk masing-masing kata dalam kalimat secara dinamis, sehingga memberikan transparansi interpretasi (Explainable AI) kata mana yang paling berpengaruh terhadap keputusan model.
                  </p>
                </div>
              </div>
            </div>

          </div>
        </div>'''

def generate_subtab_metodologi():
    return '''        <!-- SUBTAB 5: METODOLOGI 5 TAHAP PREPROCESSING & TEORI PARADIGMA -->
        <div id="subtab-content-metodologi" class="hidden space-y-4">
          <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-5 text-xs text-slate-700 dark:text-zinc-300 leading-relaxed">
            <div>
              <h3 class="text-sm font-bold text-slate-900 dark:text-zinc-100 flex items-center gap-2 mb-1">
                <i data-lucide="book-open" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
                <span>Metodologi 5 Tahap Preprocessing NLP & Teori Multi-Paradigma</span>
              </h3>
              <p class="text-slate-500 dark:text-zinc-400">Standar prapemrosesan korpus teks media sosial bahasa Indonesia non-formal untuk penelitian komputasi.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-2">
                <span class="font-bold text-slate-900 dark:text-zinc-100 text-xs block">Tahap 1: Case Folding & Cleaning</span>
                <p class="text-slate-600 dark:text-zinc-400 text-[11px]">Mengubah seluruh karakter menjadi huruf kecil dan membuang URL, mention username, hashtag, angka, serta tanda baca non-alfabetik.</p>
              </div>

              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-2">
                <span class="font-bold text-slate-900 dark:text-zinc-100 text-xs block">Tahap 2: Tokenisasi</span>
                <p class="text-slate-600 dark:text-zinc-400 text-[11px]">Memecah aliran teks kalimat menjadi deretan token kata individual berdasarkan batas kata kata valid (minimal 2 huruf).</p>
              </div>

              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-2">
                <span class="font-bold text-slate-900 dark:text-zinc-100 text-xs block">Tahap 3: Normalisasi Kata (Slang to Formal)</span>
                <p class="text-slate-600 dark:text-zinc-400 text-[11px]">Memetakan kata tidak baku/singkatan menggunakan 15.006 entri kamus kata alay (colloquial-indonesian-lexicon) dan kamus khusus ketenagakerjaan (loker, phk, umr).</p>
              </div>

              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-2">
                <span class="font-bold text-slate-900 dark:text-zinc-100 text-xs block">Tahap 4: Stopword Removal (Negation-Preserving)</span>
                <p class="text-slate-600 dark:text-zinc-400 text-[11px]">Menghapus kata umum tanpa makna, namun secara ketat menjaga kata negasi (tidak, bukan, belum, jangan) agar polaritas sentimen tidak rusak.</p>
              </div>

              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-2 md:col-span-2">
                <span class="font-bold text-slate-900 dark:text-zinc-100 text-xs block">Tahap 5: Stemming Sastrawi dengan Memoization Caching</span>
                <p class="text-slate-600 dark:text-zinc-400 text-[11px]">Mengubah kata berimbuhan menjadi bentuk dasarnya menggunakan algoritma Nazief-Adriani melalui PySastrawi dengan memoization cache berkecepatan O(1).</p>
              </div>
            </div>
          </div>
        </div>'''

def generate_full_html_block():
    subtabs_nav = '''        <!-- Sub Tabs Navigation (5 Tabs) -->
        <div class="flex items-center gap-2 p-1 bg-slate-200/80 dark:bg-[#16161a] rounded-xl border border-slate-300 dark:border-[#2d2d35] text-xs overflow-x-auto">
          <button id="s-subtab-komparasi" onclick="switchSentimentSubtab('komparasi')" class="px-3.5 py-2 rounded-lg font-semibold bg-white dark:bg-[#25252c] text-slate-900 dark:text-white transition flex items-center gap-2 shrink-0 shadow-sm">
            <i data-lucide="scale" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
            <span>Komparasi Multi-Paradigma (6 Metode)</span>
          </button>
          <button id="s-subtab-dataset" onclick="switchSentimentSubtab('dataset')" class="px-3.5 py-2 rounded-lg font-medium text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="database" class="w-4 h-4"></i>
            <span>Tabel & Audit Ground Truth (617 Data)</span>
          </button>
          <button id="s-subtab-simulator" onclick="switchSentimentSubtab('simulator')" class="px-3.5 py-2 rounded-lg font-medium text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="play-circle" class="w-4 h-4"></i>
            <span>Interactive Pipeline Simulator</span>
          </button>
          <button id="s-subtab-flowchart" onclick="switchSentimentSubtab('flowchart')" class="px-3.5 py-2 rounded-lg font-medium text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="git-fork" class="w-4 h-4"></i>
            <span>Flowchart Sidang & Arsitektur</span>
          </button>
          <button id="s-subtab-metodologi" onclick="switchSentimentSubtab('metodologi')" class="px-3.5 py-2 rounded-lg font-medium text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="book-open" class="w-4 h-4"></i>
            <span>Metodologi 5 Tahap & Teori</span>
          </button>
        </div>'''

    header_block = '''      <!-- ============================================================== -->
      <!-- SECTION 4: LABOR SENTIMENT RESEARCH DASHBOARD -->
      <!-- ============================================================== -->
      <div id="sentiment-research-container" class="hidden w-full max-w-5xl space-y-6 pt-4">
        
        <!-- Header Banner & Stats -->
        <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-6 shadow-sm space-y-4">
          <div class="space-y-3">
            <div class="flex flex-wrap items-center gap-2">
              <span class="text-[11px] font-semibold uppercase px-2.5 py-0.5 rounded bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/40 flex items-center gap-1.5 font-mono">
                <i data-lucide="award" class="w-3.5 h-3.5"></i>
                Studi Komparasi Multi-Paradigma
              </span>
              <span class="text-[11px] px-2.5 py-0.5 rounded bg-slate-100 dark:bg-[#1f1f26] text-slate-600 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] font-mono">
                Sumber: YouTube Public Discourse (Real Comments)
              </span>
              <span class="text-[11px] px-2.5 py-0.5 rounded bg-slate-100 dark:bg-[#1f1f26] text-slate-600 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] font-mono">
                Dataset: 617 Data Komentar Riil Valid
              </span>
            </div>
            
            <h1 class="text-xl md:text-2xl font-bold text-slate-900 dark:text-zinc-100 tracking-tight">
              Analisis Sentimen Publik terhadap Krisis Ketenagakerjaan di Indonesia
            </h1>
            <p class="text-xs md:text-sm text-slate-600 dark:text-zinc-400 max-w-3xl leading-relaxed">
              Perbandingan komprehensif 6 metode lintas paradigma: 
              <strong class="text-slate-900 dark:text-zinc-200">InSet Lexicon</strong>, 
              <strong class="text-slate-900 dark:text-zinc-200">Hybrid SVM</strong>, 
              <strong class="text-slate-900 dark:text-zinc-200">Linear SVM</strong>, 
              <strong class="text-slate-900 dark:text-zinc-200">Cosine Similarity</strong>, 
              <strong class="text-slate-900 dark:text-zinc-200">Neural BiLSTM (Attention)</strong>, dan 
              <strong class="text-slate-900 dark:text-zinc-200">X-Shot Reasoning (Chain-of-Thought)</strong>.
            </p>

            <!-- Direct Evidence / Ground Truth Download Actions -->
            <div class="pt-2 flex flex-wrap items-center gap-2.5 border-t border-slate-100 dark:border-[#222226]">
              <a href="/api/sentiment/export/dataset?format=xlsx" target="_blank" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 transition shadow-sm">
                <i data-lucide="file-spreadsheet" class="w-3.5 h-3.5"></i>
                <span>Unduh Bukti Ground Truth (.xlsx)</span>
              </a>
              <a href="/api/sentiment/export/dataset?format=csv" target="_blank" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#1f1f26] dark:hover:bg-[#272730] text-slate-700 dark:text-zinc-200 border border-slate-300 dark:border-[#2d2d35] text-xs font-medium flex items-center gap-1.5 transition">
                <i data-lucide="file-text" class="w-3.5 h-3.5"></i>
                <span>Unduh Dataset (.csv)</span>
              </a>
              <a href="/api/sentiment/export/evaluation" target="_blank" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#1f1f26] dark:hover:bg-[#272730] text-slate-700 dark:text-zinc-200 border border-slate-300 dark:border-[#2d2d35] text-xs font-medium flex items-center gap-1.5 transition">
                <i data-lucide="download" class="w-3.5 h-3.5"></i>
                <span>Laporan Evaluasi Lengkap (.xlsx)</span>
              </a>
            </div>
          </div>
        </div>'''

    full_html = f'''{header_block}

{subtabs_nav}

{generate_subtab_komparasi()}

{generate_subtab_dataset()}

{generate_subtab_simulator()}

{generate_subtab_flowchart()}

{generate_subtab_metodologi()}

      </div>'''
    return full_html

def generate_javascript_block():
    return '''    // ==============================================
    // SENTIMENT RESEARCH DASHBOARD & SIMULATOR LOGIC
    // ==============================================
    let currentSimStep = 1;
    let latestSimData = null;

    function openLaborSentimentDashboard() {
      document.getElementById('hero-discovery-container').classList.add('hidden');
      document.getElementById('results-discovery-container').classList.add('hidden');
      document.getElementById('deep-detail-container').classList.add('hidden');
      
      const sentContainer = document.getElementById('sentiment-research-container');
      sentContainer.classList.remove('hidden');
      
      document.getElementById('btn-back-to-search').classList.remove('hidden');
      document.getElementById('btn-save-current').classList.add('hidden');
      document.getElementById('export-dropdown-wrapper').classList.add('hidden');
      
      switchSentimentSubtab('komparasi');
      loadSentimentDataset(1);
      lucide.createIcons();
    }

    function switchSentimentSubtab(tabName) {
      const tabs = ['komparasi', 'dataset', 'simulator', 'flowchart', 'metodologi'];
      tabs.forEach(t => {
        const btn = document.getElementById(`s-subtab-${t}`);
        const content = document.getElementById(`subtab-content-${t}`);
        if (!btn || !content) return;
        if (t === tabName) {
          btn.className = "px-3.5 py-2 rounded-lg font-semibold bg-white dark:bg-[#25252c] text-slate-900 dark:text-white transition flex items-center gap-2 shrink-0 shadow-sm";
          content.classList.remove('hidden');
        } else {
          btn.className = "px-3.5 py-2 rounded-lg font-medium text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-2 shrink-0";
          content.classList.add('hidden');
        }
      });
      lucide.createIcons();
    }

    async function loadSentimentDataset(page = 1) {
      sentimentDatasetPage = page;
      const q = document.getElementById('ds-filter-query') ? document.getElementById('ds-filter-query').value.trim() : '';
      const sent = document.getElementById('ds-filter-sentiment') ? document.getElementById('ds-filter-sentiment').value : 'all';
      
      const tbody = document.getElementById('ds-table-body');
      tbody.innerHTML = `<tr><td colspan="10" class="px-4 py-8 text-center text-slate-400 dark:text-zinc-500">Memuat data halaman ${page}...</td></tr>`;
      
      try {
        const statusFilter = document.getElementById('ds-filter-status') ? document.getElementById('ds-filter-status').value : 'all';
        const splitFilter = document.getElementById('ds-filter-split') ? document.getElementById('ds-filter-split').value : 'all';
        const url = `/api/sentiment/dataset?page=${page}&page_size=20&platform=all&sentiment=${encodeURIComponent(sent)}&query=${encodeURIComponent(q)}&split=${encodeURIComponent(splitFilter)}&status_filter=${encodeURIComponent(statusFilter)}`;
        const res = await fetch(url);
        const data = await res.json();
        
        sentimentDatasetTotalPages = data.pages || 1;
        document.getElementById('ds-current-page').innerText = data.page;
        document.getElementById('ds-pagination-info').innerText = `Menampilkan ${((data.page-1)*20)+1} - ${Math.min(data.page*20, data.total)} dari ${data.total} data`;
        
        document.getElementById('ds-prev-btn').disabled = data.page <= 1;
        document.getElementById('ds-next-btn').disabled = data.page >= data.pages;
        
        if (!data.items || data.items.length === 0) {
          tbody.innerHTML = `<tr><td colspan="10" class="px-4 py-8 text-center text-slate-400 dark:text-zinc-500">Tidak ada data komentar yang cocok dengan filter yang dipilih.</td></tr>`;
          return;
        }
        
        tbody.innerHTML = data.items.map((item, idx) => {
          const rowNo = ((data.page - 1) * 20) + idx + 1;
          const gt = item.sentiment_ground_truth || 'Netral';
          const lex = item.pred_lexicon || 'Netral';
          const hyb = item.pred_hybrid_svm || item.pred_svm || 'Netral';
          const svm = item.pred_svm || 'Netral';
          const cos = item.pred_cosine || 'Netral';
          const bilstm = item.pred_bilstm || item.pred_svm || 'Netral';
          
          const gtBadge = gt === 'Negatif' ? 'text-rose-700 bg-rose-50 dark:text-rose-300 dark:bg-rose-950/50 border-rose-300 dark:border-rose-900/50' : 
                          gt === 'Positif' ? 'text-emerald-700 bg-emerald-50 dark:text-emerald-300 dark:bg-emerald-950/50 border-emerald-300 dark:border-emerald-900/50' : 
                          'text-slate-700 bg-slate-100 dark:text-zinc-300 dark:bg-[#202028] border-slate-300 dark:border-[#2d2d35]';

          const renderModelBadge = (pred, modelName) => {
            const isMatch = (pred === gt);
            const badgeClass = isMatch ? 
              'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800/40' : 
              'bg-rose-50 text-rose-800 dark:bg-rose-950/40 dark:text-rose-300 border-rose-200 dark:border-rose-800/40';
            const iconName = isMatch ? 'check' : 'x';
            const iconColor = isMatch ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400';
            const titleText = isMatch ? `Tebakan ${modelName} Benar` : `Tebakan ${modelName} Salah! Target: ${gt}`;
            return `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold border ${badgeClass}" title="${titleText}">
              <i data-lucide="${iconName}" class="w-3 h-3 ${iconColor}"></i>
              <span>${pred}</span>
            </span>`;
          };

          const isTestSet = (item.dataset_split || '').includes('Test');
          const splitBadge = isTestSet ? 
            'bg-amber-50 text-amber-800 dark:bg-amber-950/40 dark:text-amber-300 border-amber-300 dark:border-amber-800/50 font-bold' : 
            'bg-slate-50 text-slate-500 dark:bg-[#1a1a20] dark:text-zinc-500 border-slate-200 dark:border-[#272730]';

          return `
            <tr class="hover:bg-slate-50 dark:hover:bg-[#1a1a20] transition text-[11px]">
              <td class="px-3 py-2.5 font-mono text-slate-400 dark:text-zinc-500">${rowNo}</td>
              <td class="px-3 py-2.5 text-slate-800 dark:text-zinc-200 max-w-xs break-words">${escapeHtml(item.text || '')}</td>
              <td class="px-3 py-2.5 text-slate-500 dark:text-zinc-400 font-mono text-[10px] max-w-xs break-words">${escapeHtml(item.processed_text || '')}</td>
              <td class="px-3 py-2.5 text-center">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md font-bold border ${gtBadge}">
                  <i data-lucide="target" class="w-3.5 h-3.5"></i>
                  <span>${gt}</span>
                </span>
              </td>
              <td class="px-3 py-2.5 text-center">${renderModelBadge(lex, 'InSet')}</td>
              <td class="px-3 py-2.5 text-center">${renderModelBadge(hyb, 'Hybrid SVM')}</td>
              <td class="px-3 py-2.5 text-center">${renderModelBadge(svm, 'Linear SVM')}</td>
              <td class="px-3 py-2.5 text-center">${renderModelBadge(cos, 'Cosine')}</td>
              <td class="px-3 py-2.5 text-center">${renderModelBadge(bilstm, 'BiLSTM')}</td>
              <td class="px-3 py-2.5 text-center">
                <span class="px-2 py-0.5 rounded text-[10px] border font-mono ${splitBadge}">
                  ${(item.dataset_split || 'Train').replace('Set', '')}
                </span>
              </td>
            </tr>
          `;
        }).join('');
        lucide.createIcons();
      } catch (e) {
        tbody.innerHTML = `<tr><td colspan="10" class="px-4 py-8 text-center text-red-500">Gagal memuat data: ${e.message}</td></tr>`;
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

    function setSimulatorSample(num) {
      const input = document.getElementById('sim-input-text');
      if (num === 1) input.value = "Susah bgt nyari loker sekarang, kena phk massal dan batas usia max 25 thn!";
      if (num === 2) input.value = "Gaji tidak sebanding beban rodi, lembur tidak dibayar dan tidak ada bonus.";
      if (num === 3) input.value = "Alhamdulillah dapat panggilan kerja setelah ikut pelatihan vokasi, optimis dan semangat!";
      if (num === 4) input.value = "Kemnaker merilis statistik resmi tingkat pengangguran terbuka periode triwulan ini.";
    }

    async function runPipelineSimulation(autoPlay = true) {
      const text = document.getElementById('sim-input-text').value.trim();
      if (!text) {
        showToast("Silakan masukkan teks opini terlebih dahulu", "error");
        return;
      }
      
      const btn = document.getElementById('btn-run-sim-full');
      const origHtml = btn.innerHTML;
      btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i><span>Memproses Pipeline...</span>`;
      btn.disabled = true;
      
      try {
        const res = await fetch('/api/sentiment/predict', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({text: text})
        });
        const data = await res.json();
        latestSimData = data;
        
        document.getElementById('sim-stepper-bar').classList.remove('hidden');
        document.getElementById('sim-step-container').classList.remove('hidden');
        
        // Render step data
        populateSimulatorViews(data);
        
        if (autoPlay) {
          goToSimStep(1);
          let s = 1;
          const interval = setInterval(() => {
            s++;
            if (s <= 6) {
              goToSimStep(s);
            } else {
              clearInterval(interval);
            }
          }, 350);
        } else {
          goToSimStep(6);
        }
        
        showToast("Simulasi komputasi 5 tahap & 6 metode selesai!", "success");
      } catch (err) {
        showToast("Gagal menjalankan simulasi: " + err.message, "error");
      } finally {
        btn.innerHTML = origHtml;
        btn.disabled = false;
        lucide.createIcons();
      }
    }

    function populateSimulatorViews(data) {
      const p = data.preprocessing || {};
      const preds = data.predictions || {};

      // Step 1
      document.getElementById('sim-raw-text').innerText = data.input_text || '';
      document.getElementById('sim-raw-len').innerText = `${(data.input_text || '').length} karakter`;

      // Step 2
      document.getElementById('sim-folded-text').innerText = p.case_folded || '';

      // Step 3
      const slangAudits = p.slang_transformations || [];
      const slangBadgeBox = document.getElementById('sim-slang-badges');
      if (slangAudits.length > 0) {
        document.getElementById('sim-slang-count-badge').innerText = `${slangAudits.length} Kata Alay Dinormalisasi`;
        slangBadgeBox.innerHTML = slangAudits.map(s => `
          <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-amber-50 text-amber-900 dark:bg-amber-950/40 dark:text-amber-300 border border-amber-200 dark:border-amber-800/40 font-mono">
            <span>${escapeHtml(s.from)}</span>
            <span class="text-slate-400">&rarr;</span>
            <span class="font-bold">${escapeHtml(s.to)}</span>
          </span>
        `).join('');
      } else {
        document.getElementById('sim-slang-count-badge').innerText = '0 Kata Alay';
        slangBadgeBox.innerHTML = `<span class="text-slate-400 dark:text-zinc-500 italic">Tidak ditemukan singkatan / kata alay dalam kalimat.</span>`;
      }
      document.getElementById('sim-norm-text').innerText = (p.tokens_normalized || []).join(' ');

      // Step 4
      const removedStops = p.removed_stopwords || [];
      const stopBox = document.getElementById('sim-stop-removed-box');
      if (removedStops.length > 0) {
        stopBox.innerHTML = `<span class="text-slate-500 dark:text-zinc-400 mr-1">Kata umum dihapus:</span>` + 
          removedStops.map(st => `<span class="px-1.5 py-0.2 rounded bg-slate-200 dark:bg-zinc-800 line-through text-slate-500 font-mono">${escapeHtml(st)}</span>`).join(' ');
      } else {
        stopBox.innerHTML = `<span class="text-slate-400 dark:text-zinc-500 italic">Tidak ada stopword umum yang dibuang.</span>`;
      }
      document.getElementById('sim-stop-text').innerText = (p.tokens_no_stopwords || []).join(' ');

      // Step 5
      const stemAudits = p.stemming_transformations || [];
      const stemBadgeBox = document.getElementById('sim-stem-badges');
      if (stemAudits.length > 0) {
        document.getElementById('sim-stem-count-badge').innerText = `${stemAudits.length} Kata Diubah ke Kata Dasar`;
        stemBadgeBox.innerHTML = stemAudits.map(st => `
          <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-slate-100 text-slate-800 dark:bg-[#1f1f26] dark:text-zinc-200 border border-slate-200 dark:border-[#2d2d35] font-mono">
            <span>${escapeHtml(st.from)}</span>
            <span class="text-slate-400">&rarr;</span>
            <span class="font-bold text-emerald-600 dark:text-emerald-400">${escapeHtml(st.to)}</span>
          </span>
        `).join('');
      } else {
        document.getElementById('sim-stem-count-badge').innerText = '0 Imbuhan';
        stemBadgeBox.innerHTML = `<span class="text-slate-400 dark:text-zinc-500 italic">Semua kata sudah merupakan kata dasar murni.</span>`;
      }
      document.getElementById('sim-stem-text').innerText = p.processed_text || '';

      // Step 6: Multi-Model Cards
      const setCardBadge = (badgeId, label) => {
        const b = document.getElementById(badgeId);
        if (!b) return;
        b.innerText = label;
        b.className = `px-2 py-0.5 rounded text-[10px] font-bold ${label === 'Negatif' ? 'bg-rose-50 text-rose-700 dark:bg-rose-950/40 dark:text-rose-300 border border-rose-200 dark:border-rose-900/40' : label === 'Positif' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-900/40' : 'bg-slate-100 text-slate-700 dark:bg-zinc-800 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35]'}`;
      };

      // 1. InSet
      const lex = preds.inset_lexicon || {};
      setCardBadge('sim-res-lex-badge', lex.label || 'Netral');
      document.getElementById('sim-res-lex-score').innerText = `Skor Valensi: ${lex.score || 0}`;
      const matched = (lex.matched_words || []).map(m => `${m.phrase} (${m.adjusted_weight > 0 ? '+' : ''}${m.adjusted_weight})`).join(', ');
      document.getElementById('sim-res-lex-words').innerText = matched ? `Kata leksikon: ${matched}` : 'Tidak ada leksikon cocok';

      // 2. Hybrid SVM
      const hyb = preds.hybrid_svm || {};
      setCardBadge('sim-res-hyb-badge', hyb.label || 'Netral');
      document.getElementById('sim-res-hyb-conf').innerText = `Confidence: ${(hyb.confidence * 100).toFixed(1)}%`;
      const hybProbs = Object.entries(hyb.probabilities || {}).map(([k, v]) => `${k}: ${(v*100).toFixed(0)}%`).join(' | ');
      document.getElementById('sim-res-hyb-probs').innerText = hybProbs || 'Probabilitas dihitung';

      // 3. Linear SVM
      const svm = preds.linear_svm || {};
      setCardBadge('sim-res-svm-badge', svm.label || 'Netral');
      document.getElementById('sim-res-svm-conf').innerText = `Confidence: ${(svm.confidence * 100).toFixed(1)}%`;
      const svmProbs = Object.entries(svm.probabilities || {}).map(([k, v]) => `${k}: ${(v*100).toFixed(0)}%`).join(' | ');
      document.getElementById('sim-res-svm-probs').innerText = svmProbs || '-';

      // 4. Cosine Sim
      const cos = preds.cosine_similarity || {};
      setCardBadge('sim-res-cos-badge', cos.label || 'Netral');
      document.getElementById('sim-res-cos-sim').innerText = `Cosine Sim: ${cos.similarity || 0}`;
      const cosSims = Object.entries(cos.all_similarities || {}).map(([k, v]) => `${k}: ${v}`).join(' | ');
      document.getElementById('sim-res-cos-sims').innerText = cosSims || '-';

      // 5. BiLSTM
      const bilstm = preds.neural_bilstm || {};
      setCardBadge('sim-res-bilstm-badge', bilstm.label || 'Netral');
      document.getElementById('sim-res-bilstm-conf').innerText = `Confidence: ${(bilstm.confidence * 100).toFixed(1)}%`;
      const bilstmProbs = Object.entries(bilstm.probabilities || {}).map(([k, v]) => `${k}: ${(v*100).toFixed(0)}%`).join(' | ');
      document.getElementById('sim-res-bilstm-probs').innerText = bilstmProbs || '-';

      // BiLSTM Attention Heatmap Tokens
      const attBox = document.getElementById('sim-bilstm-attention-tokens');
      const atts = bilstm.word_attentions || [];
      if (atts.length > 0) {
        attBox.innerHTML = atts.map(a => {
          const bgOpacity = Math.max(0.15, a.normalized || 0.2);
          return `<span class="px-2 py-1 rounded border border-emerald-300 dark:border-emerald-700/50" style="background-color: rgba(16, 185, 129, ${bgOpacity});">
            <span>${escapeHtml(a.word)}</span>
            <span class="text-[9px] opacity-75 ml-1">(${(a.weight * 100).toFixed(0)}%)</span>
          </span>`;
        }).join('');
      } else {
        attBox.innerHTML = `<span class="text-slate-400">Tidak ada token terdeteksi.</span>`;
      }

      // 6. X-Shot Reasoning
      const xshot = preds.xshot_reasoning || {};
      setCardBadge('sim-res-xshot-badge', xshot.label || 'Netral');
      document.getElementById('sim-res-xshot-conf').innerText = `Keyakinan: ${(xshot.confidence * 100).toFixed(0)}%`;
      const ex = xshot.nearest_exemplar || {};
      document.getElementById('sim-res-xshot-exemplar').innerText = ex.text ? `Penyelarasan Exemplar: "${ex.text}"` : 'Exemplar diselaraskan';

      // X-Shot CoT List
      const cotBox = document.getElementById('sim-xshot-cot-list');
      const cotSteps = xshot.chain_of_thought || [];
      if (cotSteps.length > 0) {
        cotBox.innerHTML = cotSteps.map(step => `
          <div class="flex items-start gap-2 p-2 rounded-lg bg-white dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2b2b35]">
            <i data-lucide="chevron-right" class="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5"></i>
            <span class="text-slate-700 dark:text-zinc-300 leading-snug">${escapeHtml(step)}</span>
          </div>
        `).join('');
      }
    }

    function goToSimStep(stepNumber) {
      currentSimStep = stepNumber;
      for (let s = 1; s <= 6; s++) {
        const btn = document.getElementById(`sim-step-btn-${s}`);
        const card = document.getElementById(`sim-card-${s}`);
        if (!btn || !card) continue;
        
        if (s === stepNumber) {
          btn.className = "px-3 py-1.5 rounded-lg font-semibold bg-white dark:bg-[#25252c] text-slate-900 dark:text-white transition flex items-center gap-1.5 shrink-0 shadow-sm border border-emerald-500/40";
          card.classList.remove('hidden');
        } else {
          btn.className = "px-3 py-1.5 rounded-lg text-slate-500 dark:text-zinc-400 hover:text-slate-800 dark:hover:text-zinc-200 transition flex items-center gap-1.5 shrink-0";
          card.classList.add('hidden');
        }
      }
      lucide.createIcons();
    }

    function switchFlowchartView(viewName) {
      const views = ['e2e', 'hybrid', 'bilstm'];
      views.forEach(v => {
        const btn = document.getElementById(`fc-btn-${v}`);
        const view = document.getElementById(`fc-view-${v}`);
        if (!btn || !view) return;
        if (v === viewName) {
          btn.className = "px-3 py-1.5 rounded-lg font-semibold bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 transition";
          view.classList.remove('hidden');
        } else {
          btn.className = "px-3 py-1.5 rounded-lg text-slate-600 dark:text-zinc-400 hover:bg-slate-100 dark:hover:bg-[#202028] transition";
          view.classList.add('hidden');
        }
      });
      lucide.createIcons();
    }
'''

def apply_updates():
    html_file = "frontend/dist/index.html"
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Landmark 1: Replace <div id="sentiment-research-container"...> up to </div> before <!-- MODAL: SETTINGS PARAMETER SCRAPING -->
    modal_idx = html.find("<!-- MODAL: SETTINGS PARAMETER SCRAPING -->")
    sent_start_idx = html.find('<div id="sentiment-research-container"')

    if sent_start_idx == -1 or modal_idx == -1:
        print("[Error] Landmarks not found!")
        return False

    # Find the closing </div> of sentiment-research-container right before modal_idx
    # Let's inspect backwards from modal_idx
    sub_chunk = html[sent_start_idx:modal_idx]
    # The container ends at the second-to-last </div> in sub_chunk (since modal is outside)
    # Actually let's locate the exact closing </div> of sentiment-research-container
    last_div_idx = sub_chunk.rfind("</div>")
    # There are nested </div> before modal. Let's see how many divs are open
    # Or cleaner: generate_full_html_block() has its own `<div id="sentiment-research-container"> ... </div>`
    # In the original file:
    # 989: </div> (closes subtab-content-metodologi)
    # 991: </div> (closes sentiment-research-container)
    # 993: </div> (closes main container)
    
    # Let's verify by checking original lines around 985-995
    lines = html.splitlines(True)
    start_line_idx = None
    end_line_idx = None
    for i, line in enumerate(lines):
        if 'id="sentiment-research-container"' in line:
            start_line_idx = i
        if '<!-- MODAL: SETTINGS PARAMETER SCRAPING -->' in line:
            end_line_idx = i
            break

    print(f"sentiment-research-container starts at line {start_line_idx + 1}")
    print(f"MODAL: SETTINGS starts at line {end_line_idx + 1}")

    # Lines between start_line_idx and end_line_idx
    # In lines[end_line_idx - 1] is empty, lines[end_line_idx - 2] is </div> (closes main container)
    # lines[end_line_idx - 4] is </div> (closes sentiment-research-container)
    print("Pre-modal line -4:", repr(lines[end_line_idx - 4]))
    print("Pre-modal line -2:", repr(lines[end_line_idx - 2]))

    # Target slice to replace is lines from start_line_idx to end_line_idx - 3 (inclusive of line end_line_idx - 4)
    # Let's check lines[end_line_idx - 4]
    target_end_line = end_line_idx - 3
    print(f"Replacing lines {start_line_idx + 1} to {target_end_line}")
    
    new_html_block = generate_full_html_block() + "\n\n"

    new_lines = lines[:start_line_idx] + [new_html_block] + lines[target_end_line:]
    updated_html = "".join(new_lines)

    # Landmark 2: In JavaScript section, replace from
    # // SENTIMENT RESEARCH DASHBOARD LOGIC
    # up to
    # // SETTINGS MODAL & INSTAGRAM CONFIG
    js_start = updated_html.find("// SENTIMENT RESEARCH DASHBOARD LOGIC")
    js_end = updated_html.find("// SETTINGS MODAL & INSTAGRAM CONFIG")

    if js_start == -1 or js_end == -1:
        print("[Error] JS Landmarks not found!")
        return False

    print(f"Replacing JS from {js_start} to {js_end}")
    new_js = generate_javascript_block() + "\n    "
    final_html = updated_html[:js_start] + new_js + updated_html[js_end:]

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"[Success] Updated {html_file} successfully!")
    return True

if __name__ == "__main__":
    apply_updates()
