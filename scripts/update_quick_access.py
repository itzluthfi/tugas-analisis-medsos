with open('frontend/dist/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Placeholder
old_ph = 'placeholder="Ketik topik apa saja... (misal: \'open source github\' atau isu yang sedang ramai)"'
new_ph = 'placeholder="Ketik topik atau pilih Quick Access... (misal: \'krisis ketenagakerjaan indonesia\', \'krisis bbm buruh\', \'susah cari kerja\')"'
if old_ph in html:
    html = html.replace(old_ph, new_ph)
    print("Placeholder updated!")

# 2. Update Suggested Topics block
import re
pattern = r'<!-- Suggested Topics -->.*?</div>\s*</div>\s*</div>'

new_block = '''<!-- QUICK ACCESS BANNER: RISET SENTIMEN KRISIS KETENAGAKERJAAN -->
        <div onclick="openLaborSentimentDashboard()" class="w-full p-4 rounded-2xl bg-gradient-to-r from-emerald-950/60 via-[#1e2722] to-[#1c221e] border border-emerald-700/50 hover:border-emerald-500/80 transition cursor-pointer shadow-xl flex items-center justify-between group">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                Akses Cepat Riset Utama
              </span>
              <span class="text-[10px] text-zinc-400 font-mono">617 Data &bull; InSet &bull; SVM &bull; Cosine</span>
            </div>
            <h3 class="text-sm font-bold text-zinc-100 group-hover:text-emerald-300 transition">
              Analisis Sentimen: Krisis Ketenagakerjaan di Indonesia
            </h3>
            <p class="text-[11px] text-zinc-400">
              Lihat tabel 617 data komentar, metrik akurasi 3 model, confusion matrix, dan coba live tester sentimen.
            </p>
          </div>
          <div class="w-8 h-8 rounded-full bg-emerald-600/30 text-emerald-300 group-hover:bg-emerald-500 group-hover:text-white flex items-center justify-center shrink-0 transition">
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </div>
        </div>

        <!-- Suggested Topics / Quick Access Sesuai Topik Krisis -->
        <div class="w-full space-y-2 text-left">
          <div class="text-[11px] text-zinc-400 flex items-center justify-between font-medium px-1">
            <span class="flex items-center gap-1.5"><i data-lucide="sparkle" class="w-3.5 h-3.5 text-emerald-400"></i> Topik Populer & Quick Search Isu Publik</span>
            <span class="text-[10px] text-zinc-500">Klik untuk cari konten & scraping</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 text-xs">
            <button onclick="quickSearch('krisis ketenagakerjaan indonesia phk massal')" class="p-3 rounded-xl bg-[#212121]/60 hover:bg-[#252525] border border-[#2a2a2a] hover:border-emerald-700/50 text-left transition space-y-1 group">
              <div class="font-semibold text-zinc-200 group-hover:text-emerald-300 flex items-center gap-1.5">
                <i data-lucide="briefcase" class="w-3.5 h-3.5 text-emerald-400"></i>
                <span>Krisis Ketenagakerjaan</span>
              </div>
              <div class="text-[11px] text-zinc-500">Gelombang PHK massal & pabrik tutup</div>
            </button>
            <button onclick="quickSearch('krisis bbm dampak kenaikan harga pekerja')" class="p-3 rounded-xl bg-[#212121]/60 hover:bg-[#252525] border border-[#2a2a2a] hover:border-amber-700/50 text-left transition space-y-1 group">
              <div class="font-semibold text-zinc-200 group-hover:text-amber-300 flex items-center gap-1.5">
                <i data-lucide="fuel" class="w-3.5 h-3.5 text-amber-400"></i>
                <span>Krisis BBM & Inflasi</span>
              </div>
              <div class="text-[11px] text-zinc-500">Dampak biaya hidup & upah buruh</div>
            </button>
            <button onclick="quickSearch('susah cari kerja gen z sarjana pengangguran')" class="p-3 rounded-xl bg-[#212121]/60 hover:bg-[#252525] border border-[#2a2a2a] hover:border-sky-700/50 text-left transition space-y-1 group">
              <div class="font-semibold text-zinc-200 group-hover:text-sky-300 flex items-center gap-1.5">
                <i data-lucide="graduation-cap" class="w-3.5 h-3.5 text-sky-400"></i>
                <span>Susah Cari Kerja Gen Z</span>
              </div>
              <div class="text-[11px] text-zinc-500">Fresh graduate & ribuan pelamar loker</div>
            </button>
            <button onclick="quickSearch('syarat batas usia maksimal 25 tahun loker')" class="p-3 rounded-xl bg-[#212121]/60 hover:bg-[#252525] border border-[#2a2a2a] hover:border-purple-700/50 text-left transition space-y-1 group">
              <div class="font-semibold text-zinc-200 group-hover:text-purple-300 flex items-center gap-1.5">
                <i data-lucide="calendar" class="w-3.5 h-3.5 text-purple-400"></i>
                <span>Batas Usia 25 Thn</span>
              </div>
              <div class="text-[11px] text-zinc-500">Diskriminasi usia lowongan kerja</div>
            </button>
          </div>
        </div>
      </div>'''

match = re.search(pattern, html, flags=re.DOTALL)
if match:
    html = html[:match.start()] + new_block + html[match.end():]
    print("Replaced suggested topics block successfully!")
else:
    print("Regex match failed.")

with open('frontend/dist/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
