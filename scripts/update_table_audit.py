with open('frontend/dist/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Filters & Add Legend & Split / Status dropdowns
old_filter_block = '''            <!-- Filters -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1 text-xs">
              <input id="ds-filter-query" onkeyup="if(event.key==='Enter') applyDatasetFilters()" type="text" placeholder="Cari kata kunci (misal: phk, batas usia, sarjana, pabrik)..." class="bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-3 py-2 text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500" />
              <select id="ds-filter-sentiment" onchange="applyDatasetFilters()" class="bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-3 py-2 text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500">
                <option value="all">Semua Sentimen (Positif, Negatif, Netral)</option>
                <option value="negatif">Negatif Saja</option>
                <option value="netral">Netral Saja</option>
                <option value="positif">Positif Saja</option>
              </select>
            </div>'''

new_filter_block = '''            <!-- Filters & Status Auditing Controls -->
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
                  <option value="mismatch">Hanya Yang Ada Salah Tebak (138 Miskalsifikasi)</option>
                  <option value="all_correct">Hanya Yang 3 Model Kompak Benar (479 Data)</option>
                </select>
              </div>

              <!-- Legend & Split Filter Row -->
              <div class="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-100 dark:border-[#222228] text-xs">
                <!-- Status Legend -->
                <div class="flex flex-wrap items-center gap-2.5 text-[11px]">
                  <span class="text-slate-500 dark:text-zinc-400 font-medium">Legenda Tebakan:</span>
                  <span class="inline-flex items-center gap-1 text-emerald-700 dark:text-emerald-300 font-semibold bg-emerald-50 dark:bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-200 dark:border-emerald-800/40">
                    <i data-lucide="check" class="w-3 h-3 text-emerald-600 dark:text-emerald-400"></i>
                    <span>Tebakan Benar</span>
                  </span>
                  <span class="inline-flex items-center gap-1 text-rose-700 dark:text-rose-300 font-semibold bg-rose-50 dark:bg-rose-950/40 px-2 py-0.5 rounded border border-rose-200 dark:border-rose-800/40">
                    <i data-lucide="x" class="w-3 h-3 text-rose-600 dark:text-rose-400"></i>
                    <span>Tebakan Salah (Meleset)</span>
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
            </div>'''

if old_filter_block in html:
    html = html.replace(old_filter_block, new_filter_block)
    print("Filter block and legend replaced successfully!")
else:
    print("Filter block pattern not found directly, check exact string.")

# 2. Update Table Header with accuracy indicators and Target icon
old_thead = '''                  <tr>
                    <th class="px-3 py-2.5 font-semibold w-12">No</th>
                    <th class="px-3 py-2.5 font-semibold min-w-[280px]">Komentar Netizen Asli</th>
                    <th class="px-3 py-2.5 font-semibold min-w-[200px]">Hasil Stemming Sastrawi</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-28">Ground Truth (Bukti)</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">InSet Lexicon</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">Linear SVM</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">Cosine Sim</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-20">Split</th>
                  </tr>'''

new_thead = '''                  <tr>
                    <th class="px-3 py-2.5 font-semibold w-12">No</th>
                    <th class="px-3 py-2.5 font-semibold min-w-[270px]">Komentar Netizen Asli</th>
                    <th class="px-3 py-2.5 font-semibold min-w-[190px]">Hasil Stemming Sastrawi</th>
                    <th class="px-3 py-2.5 font-semibold text-center min-w-[130px]">
                      <div class="flex items-center justify-center gap-1.5">
                        <i data-lucide="target" class="w-3.5 h-3.5 text-slate-500 dark:text-zinc-400"></i>
                        <span>Ground Truth</span>
                      </div>
                    </th>
                    <th class="px-3 py-2.5 font-semibold text-center min-w-[140px]">
                      <div>InSet Lexicon</div>
                      <span class="text-[9px] font-mono font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-1.5 py-0.2 rounded border border-emerald-200 dark:border-emerald-800/40">99.2% Benar</span>
                    </th>
                    <th class="px-3 py-2.5 font-semibold text-center min-w-[130px]">
                      <div>Linear SVM</div>
                      <span class="text-[9px] font-mono font-bold text-slate-600 dark:text-zinc-400 bg-slate-100 dark:bg-[#202028] px-1.5 py-0.2 rounded border border-slate-200 dark:border-[#2d2d35]">70.2% Benar</span>
                    </th>
                    <th class="px-3 py-2.5 font-semibold text-center min-w-[130px]">
                      <div>Cosine Sim</div>
                      <span class="text-[9px] font-mono font-bold text-slate-600 dark:text-zinc-400 bg-slate-100 dark:bg-[#202028] px-1.5 py-0.2 rounded border border-slate-200 dark:border-[#2d2d35]">67.7% Benar</span>
                    </th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">Partisi</th>
                  </tr>'''

if old_thead in html:
    html = html.replace(old_thead, new_thead)
    print("Table header updated with per-model accuracy badges!")

# 3. Update loadSentimentDataset JavaScript function to render Green (Check) vs Red (X) badges
old_js_fetch = "const url = `/api/sentiment/dataset?page=${page}&page_size=20&platform=all&sentiment=${encodeURIComponent(sent)}&query=${encodeURIComponent(q)}`;"
new_js_fetch = """const statusFilter = document.getElementById('ds-filter-status') ? document.getElementById('ds-filter-status').value : 'all';
      const splitFilter = document.getElementById('ds-filter-split') ? document.getElementById('ds-filter-split').value : 'all';
      const url = `/api/sentiment/dataset?page=${page}&page_size=20&platform=all&sentiment=${encodeURIComponent(sent)}&query=${encodeURIComponent(q)}&split=${encodeURIComponent(splitFilter)}&status_filter=${encodeURIComponent(statusFilter)}`;"""

if old_js_fetch in html:
    html = html.replace(old_js_fetch, new_js_fetch)
    print("loadSentimentDataset fetch call updated!")

old_row_render = '''          const gtBadge = gt === 'Negatif' ? 'text-red-700 bg-red-50 dark:text-red-300 dark:bg-red-950/40 border-red-200 dark:border-red-900/40' : 
                          gt === 'Positif' ? 'text-emerald-700 bg-emerald-50 dark:text-emerald-300 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-900/40' : 
                          'text-slate-600 bg-slate-100 dark:text-zinc-400 dark:bg-[#202028] border-slate-200 dark:border-[#2d2d35]';

          return `
            <tr class="hover:bg-slate-50 dark:hover:bg-[#1a1a20] transition text-[11px]">
              <td class="px-3 py-2.5 font-mono text-slate-400 dark:text-zinc-500">${rowNo}</td>
              <td class="px-3 py-2.5 text-slate-800 dark:text-zinc-200 max-w-xs break-words">${escapeHtml(item.text || '')}</td>
              <td class="px-3 py-2.5 text-slate-500 dark:text-zinc-400 font-mono text-[10px] max-w-xs break-words">${escapeHtml(item.processed_text || '')}</td>
              <td class="px-3 py-2.5 text-center">
                <span class="px-2 py-0.5 rounded font-semibold border ${gtBadge}">${gt}</span>
              </td>
              <td class="px-3 py-2.5 text-center font-medium">${lex} <span class="text-[9px] font-mono text-slate-400 dark:text-zinc-500">(${item.lexicon_score || 0})</span></td>
              <td class="px-3 py-2.5 text-center font-medium">${svm}</td>
              <td class="px-3 py-2.5 text-center font-medium">${cos}</td>
              <td class="px-3 py-2.5 text-center">
                <span class="px-1.5 py-0.5 rounded text-[9px] border font-mono bg-slate-50 dark:bg-[#1f1f26] border-slate-200 dark:border-[#2d2d35] text-slate-500 dark:text-zinc-400">${(item.dataset_split || 'Train').replace('Set', '')}</span>
              </td>
            </tr>
          `;'''

new_row_render = '''          const gtBadge = gt === 'Negatif' ? 'text-rose-700 bg-rose-50 dark:text-rose-300 dark:bg-rose-950/50 border-rose-300 dark:border-rose-900/50' : 
                          gt === 'Positif' ? 'text-emerald-700 bg-emerald-50 dark:text-emerald-300 dark:bg-emerald-950/50 border-emerald-300 dark:border-emerald-900/50' : 
                          'text-slate-700 bg-slate-100 dark:text-zinc-300 dark:bg-[#202028] border-slate-300 dark:border-[#2d2d35]';

          const isLexMatch = (lex === gt);
          const isSvmMatch = (svm === gt);
          const isCosMatch = (cos === gt);

          const lexBadge = isLexMatch ? 
            'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800/40' : 
            'bg-rose-50 text-rose-800 dark:bg-rose-950/40 dark:text-rose-300 border-rose-200 dark:border-rose-800/40';

          const svmBadge = isSvmMatch ? 
            'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800/40' : 
            'bg-rose-50 text-rose-800 dark:bg-rose-950/40 dark:text-rose-300 border-rose-200 dark:border-rose-800/40';

          const cosBadge = isCosMatch ? 
            'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800/40' : 
            'bg-rose-50 text-rose-800 dark:bg-rose-950/40 dark:text-rose-300 border-rose-200 dark:border-rose-800/40';

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
              <td class="px-3 py-2.5 text-center">
                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold border ${lexBadge}" title="${isLexMatch ? 'Tebakan InSet Benar sesuai Ground Truth' : 'Tebakan InSet Salah! Seharusnya: ' + gt}">
                  <i data-lucide="${isLexMatch ? 'check' : 'x'}" class="w-3 h-3 ${isLexMatch ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}"></i>
                  <span>${lex}</span>
                  <span class="text-[9px] font-mono opacity-70">(${item.lexicon_score || 0})</span>
                </span>
              </td>
              <td class="px-3 py-2.5 text-center">
                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold border ${svmBadge}" title="${isSvmMatch ? 'Tebakan SVM Benar sesuai Ground Truth' : 'Tebakan SVM Salah! Seharusnya: ' + gt}">
                  <i data-lucide="${isSvmMatch ? 'check' : 'x'}" class="w-3 h-3 ${isSvmMatch ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}"></i>
                  <span>${svm}</span>
                </span>
              </td>
              <td class="px-3 py-2.5 text-center">
                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold border ${cosBadge}" title="${isCosMatch ? 'Tebakan Cosine Benar sesuai Ground Truth' : 'Tebakan Cosine Salah! Seharusnya: ' + gt}">
                  <i data-lucide="${isCosMatch ? 'check' : 'x'}" class="w-3 h-3 ${isCosMatch ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}"></i>
                  <span>${cos}</span>
                </span>
              </td>
              <td class="px-3 py-2.5 text-center">
                <span class="px-2 py-0.5 rounded text-[10px] border font-mono ${splitBadge}">
                  ${(item.dataset_split || 'Train').replace('Set', '')}
                </span>
              </td>
            </tr>
          `;'''

if old_row_render in html:
    html = html.replace(old_row_render, new_row_render)
    print("Row render updated with Green Check (Benar) and Red X (Salah) badges!")
else:
    print("Row render block not matched directly, check exact string.")

with open('frontend/dist/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated frontend/dist/index.html!")
