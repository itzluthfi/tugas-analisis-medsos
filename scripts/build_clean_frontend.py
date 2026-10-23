import os

def generate_clean_frontend():
    html_content = r'''<!DOCTYPE html>
<html lang="id" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Social Intelligence &bull; Labor Sentiment Research</title>
  
  <!-- Tailwind CSS CDN dengan class-based dark mode -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#ecfdf5',
              100: '#d1fae5',
              500: '#10b981',
              600: '#059669',
              700: '#047857',
              900: '#064e3b',
              950: '#022c22',
            }
          }
        }
      }
    }
  </script>
  
  <!-- Lucide Icons CDN -->
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <!-- YouTube Iframe API -->
  <script src="https://www.youtube.com/iframe_api"></script>

  <style>
    /* Transisi Halus untuk Dark / Light Mode */
    * {
      transition: background-color 0.2s ease, border-color 0.2s ease;
    }
    
    /* Scrollbar Minimalis */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    .dark ::-webkit-scrollbar-thumb { background: #27272a; border-radius: 9999px; }
    .dark ::-webkit-scrollbar-thumb:hover { background: #3f3f46; }
    html:not(.dark) ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 9999px; }
    html:not(.dark) ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
  </style>
</head>

<body class="flex h-screen overflow-hidden select-none bg-slate-50 text-slate-900 dark:bg-[#0e0e11] dark:text-zinc-100 font-sans">

  <!-- TOAST NOTIFICATION CONTAINER -->
  <div id="toast-container" class="fixed top-4 right-4 z-50 flex flex-col gap-2 pointer-events-none"></div>

  <!-- ============================================== -->
  <!-- SIDEBAR UTAMA (COLLAPSIBLE & MANAGED) -->
  <!-- ============================================== -->
  <aside id="main-sidebar" class="w-64 bg-white dark:bg-[#131316] border-r border-slate-200 dark:border-[#222226] flex flex-col justify-between shrink-0 text-sm transition-all duration-300 ease-in-out relative z-30">
    <div class="p-3.5 flex flex-col h-full overflow-hidden">
      
      <!-- Brand Header -->
      <div class="flex items-center justify-between px-2 py-1.5">
        <div class="flex items-center gap-2.5 cursor-pointer" onclick="resetToDiscovery()">
          <div class="w-7 h-7 rounded-lg bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 flex items-center justify-center font-bold text-xs shadow-sm">
            <span class="tracking-tighter font-mono font-bold text-[11px]">SI</span>
          </div>
          <div class="flex flex-col">
            <span class="font-semibold text-xs tracking-tight text-slate-800 dark:text-zinc-200">Social Intelligence</span>
            <span class="text-[10px] text-slate-400 dark:text-zinc-500 font-mono">Research Hub</span>
          </div>
        </div>
        <button onclick="toggleSidebar()" title="Sembunyikan Sidebar" class="text-slate-400 hover:text-slate-600 dark:text-zinc-500 dark:hover:text-zinc-300 p-1 rounded-md hover:bg-slate-100 dark:hover:bg-[#1e1e24] transition">
          <i data-lucide="panel-left-close" class="w-4 h-4"></i>
        </button>
      </div>

      <!-- Navigasi Modul Bersih -->
      <div class="mt-4 space-y-1">
        <div class="px-2 mb-1 text-[10px] font-bold text-slate-400 dark:text-zinc-500 uppercase tracking-wider">Modul Kerja</div>
        
        <button onclick="resetToDiscovery()" class="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-slate-700 dark:text-zinc-300 hover:bg-slate-100 dark:hover:bg-[#1a1a20] transition text-xs font-medium text-left">
          <i data-lucide="search" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0"></i>
          <span>Scraping & Pencarian</span>
        </button>
        
        <button onclick="openLaborSentimentDashboard()" class="w-full flex items-center justify-between px-2.5 py-2 rounded-lg text-emerald-700 bg-emerald-50 dark:text-emerald-400 dark:bg-emerald-950/30 hover:bg-emerald-100/60 dark:hover:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800/40 transition text-xs font-semibold text-left">
          <div class="flex items-center gap-2.5">
            <i data-lucide="bar-chart-3" class="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0"></i>
            <span>Riset Sentimen Kerja</span>
          </div>
          <span class="text-[9px] bg-emerald-100 text-emerald-800 dark:bg-emerald-500/20 dark:text-emerald-300 px-1.5 py-0.5 rounded font-mono font-bold">617 Data</span>
        </button>
        
        <button onclick="toggleSettingsModal()" class="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-slate-600 dark:text-zinc-400 hover:bg-slate-100 dark:hover:bg-[#1a1a20] transition text-xs font-medium text-left">
          <i data-lucide="sliders-horizontal" class="w-4 h-4 text-slate-400 dark:text-zinc-500 shrink-0"></i>
          <span>Pengaturan Parameter</span>
        </button>
      </div>

      <!-- Riwayat Simpanan (History dengan Full CRUD) -->
      <div class="mt-5 flex-1 overflow-y-auto space-y-1 pr-1 border-t border-slate-200 dark:border-[#222226] pt-3">
        <div class="flex items-center justify-between px-2 mb-2">
          <div class="flex items-center gap-1.5">
            <span class="text-[11px] font-semibold text-slate-600 dark:text-zinc-400">Riwayat Simpanan</span>
            <span id="saved-counter" class="text-[10px] font-mono text-slate-500 dark:text-zinc-500 bg-slate-100 dark:bg-[#1a1a20] px-1.5 py-0.2 rounded border border-slate-200 dark:border-[#2d2d35]">0</span>
          </div>
          <div class="flex items-center gap-1">
            <button onclick="clearAllSavedHistory()" title="Hapus Semua Riwayat" class="text-slate-400 hover:text-red-500 dark:text-zinc-500 dark:hover:text-red-400 p-1 rounded hover:bg-slate-100 dark:hover:bg-[#1e1e24] transition">
              <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
            </button>
            <button onclick="exportAllDatabaseZip()" title="Download Semua Riwayat (ZIP Excel)" class="text-slate-400 hover:text-emerald-600 dark:text-zinc-500 dark:hover:text-emerald-400 p-1 rounded hover:bg-slate-100 dark:hover:bg-[#1e1e24] transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
            </button>
          </div>
        </div>
        
        <div id="saved-history-list" class="space-y-1">
          <div class="text-[11px] text-slate-400 dark:text-zinc-600 px-2 py-4 text-center">Belum ada riwayat tersimpan</div>
        </div>
      </div>

      <!-- System Status Footer -->
      <div class="pt-3 border-t border-slate-200 dark:border-[#222226] flex items-center justify-between px-2 text-[11px]">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span class="font-medium text-slate-600 dark:text-zinc-400">FastAPI Core</span>
        </div>
        <span class="text-[10px] text-slate-400 dark:text-zinc-500 font-mono">Port 8000</span>
      </div>

    </div>
  </aside>

  <!-- ============================================== -->
  <!-- MAIN VIEWPORT CONTAINER -->
  <!-- ============================================== -->
  <main class="flex-1 flex flex-col h-full overflow-hidden bg-slate-50 dark:bg-[#0e0e11] relative">
    
    <!-- Top Bar Navigation Header -->
    <header class="h-13 flex items-center justify-between px-6 shrink-0 z-10 border-b border-slate-200 dark:border-[#222226] bg-white/80 dark:bg-[#131316]/80 backdrop-blur-sm">
      <div class="flex items-center gap-3 text-xs">
        
        <!-- Sidebar Open Button (Saat ditutup) -->
        <button id="btn-open-sidebar" onclick="toggleSidebar()" title="Buka Sidebar" class="hidden p-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#1a1a20] dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-300 border border-slate-300 dark:border-[#2d2d35] transition">
          <i data-lucide="panel-left-open" class="w-4 h-4"></i>
        </button>

        <!-- Tombol Kembali ke Discovery -->
        <button id="btn-back-to-search" onclick="resetToDiscovery()" class="hidden px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#1a1a20] dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-200 border border-slate-300 dark:border-[#2d2d35] font-medium flex items-center gap-1.5 transition">
          <i data-lucide="arrow-left" class="w-3.5 h-3.5 text-slate-500 dark:text-zinc-400"></i>
          <span>Kembali</span>
        </button>

        <span class="font-semibold text-sm tracking-tight text-slate-800 dark:text-zinc-200">
          Social Intelligence Hub
        </span>
      </div>

      <!-- Action Area Header -->
      <div class="flex items-center gap-2">
        
        <!-- Toggle Dark / Light Theme -->
        <button id="btn-theme-toggle" onclick="toggleTheme()" title="Ubah Tema Gelap/Terang" class="p-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#1a1a20] dark:hover:bg-[#25252c] text-slate-600 dark:text-zinc-400 border border-slate-300 dark:border-[#2d2d35] transition flex items-center gap-1.5 text-xs font-medium">
          <i id="theme-icon-sun" data-lucide="sun" class="w-4 h-4 hidden dark:inline"></i>
          <i id="theme-icon-moon" data-lucide="moon" class="w-4 h-4 inline dark:hidden"></i>
        </button>

        <!-- Direct Button to Riset Dashboard -->
        <button onclick="openLaborSentimentDashboard()" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 transition shadow-sm">
          <i data-lucide="bar-chart-3" class="w-3.5 h-3.5"></i>
          <span class="hidden sm:inline">Riset Ketenagakerjaan</span>
        </button>

        <!-- Dropdown Export Menu -->
        <div id="export-dropdown-wrapper" class="relative hidden">
          <button onclick="toggleExportMenu()" class="text-xs py-1.5 px-3 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#1a1a20] dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-200 border border-slate-300 dark:border-[#2d2d35] font-medium flex items-center gap-1.5 transition">
            <i data-lucide="download" class="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400"></i>
            <span>Export Data</span>
            <i data-lucide="chevron-down" class="w-3 h-3 text-slate-400"></i>
          </button>

          <div id="export-menu-box" class="hidden absolute right-0 mt-1.5 w-48 bg-white dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-xl shadow-xl py-1 text-xs z-50">
            <button onclick="triggerExportCurrent('xlsx')" class="w-full text-left px-3.5 py-2 hover:bg-slate-100 dark:hover:bg-[#24242d] text-slate-700 dark:text-zinc-200 flex items-center gap-2 transition">
              <i data-lucide="file-spreadsheet" class="w-3.5 h-3.5 text-emerald-600"></i>
              <span>Export Excel (.xlsx)</span>
            </button>
            <button onclick="triggerExportCurrent('csv')" class="w-full text-left px-3.5 py-2 hover:bg-slate-100 dark:hover:bg-[#24242d] text-slate-700 dark:text-zinc-200 flex items-center gap-2 transition">
              <i data-lucide="file-text" class="w-3.5 h-3.5 text-sky-600"></i>
              <span>Export Komentar (.csv)</span>
            </button>
            <button onclick="triggerExportCurrent('json')" class="w-full text-left px-3.5 py-2 hover:bg-slate-100 dark:hover:bg-[#24242d] text-slate-700 dark:text-zinc-200 flex items-center gap-2 transition">
              <i data-lucide="code" class="w-3.5 h-3.5 text-amber-600"></i>
              <span>Export Raw JSON (.json)</span>
            </button>
          </div>
        </div>

        <!-- Tombol Simpan Konten -->
        <button id="btn-save-current" onclick="saveCurrentContent()" class="hidden text-xs py-1.5 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-medium flex items-center gap-1.5 transition shadow">
          <i data-lucide="bookmark-check" class="w-3.5 h-3.5"></i>
          <span>Simpan Konten Ini</span>
        </button>

        <button onclick="resetToDiscovery()" title="Reset Tampilan" class="text-slate-400 hover:text-slate-600 dark:text-zinc-400 dark:hover:text-zinc-200 p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-[#1a1a20] transition">
          <i data-lucide="rotate-ccw" class="w-4 h-4"></i>
        </button>
      </div>
    </header>

    <!-- CONTENT SCROLL AREA -->
    <div class="flex-1 overflow-y-auto px-6 pb-12 flex flex-col items-center">

      <!-- ============================================================== -->
      <!-- SECTION 1: SEARCH & HERO VIEWPORT -->
      <!-- ============================================================== -->
      <div id="hero-discovery-container" class="w-full max-w-2xl my-auto py-10 flex flex-col items-center space-y-6">
        
        <!-- Big Brand Title -->
        <div class="flex items-center gap-3 text-2xl font-bold text-slate-800 dark:text-zinc-100 tracking-tight">
          <div class="w-8 h-8 rounded-lg bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 flex items-center justify-center font-bold text-xs shadow-sm font-mono">
            SI
          </div>
          <span>Social Intelligence Hub</span>
        </div>

        <!-- Mode Toggle & Filter Platforms -->
        <div class="flex flex-col sm:flex-row items-center gap-3 w-full justify-between">
          
          <div class="flex gap-1.5 p-1 bg-slate-200/80 dark:bg-[#1a1a20] rounded-xl border border-slate-300 dark:border-[#2d2d35] text-xs">
            <button id="mode-topic-btn" onclick="switchSearchMode('topic')" class="px-3 py-1.5 rounded-lg font-medium bg-white dark:bg-[#25252c] text-slate-900 dark:text-white transition flex items-center gap-1.5 shadow-sm">
              <i data-lucide="sparkles" class="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400"></i>
              <span>Cari Topik Bebas</span>
            </button>
            <button id="mode-url-btn" onclick="switchSearchMode('url')" class="px-3 py-1.5 rounded-lg font-medium text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-1.5">
              <i data-lucide="link" class="w-3.5 h-3.5"></i>
              <span>Langsung URL</span>
            </button>
          </div>

          <!-- Filter Platform Toggles (YouTube & Instagram) -->
          <div class="flex items-center gap-2 text-xs bg-slate-200/80 dark:bg-[#1a1a20] p-1 rounded-xl border border-slate-300 dark:border-[#2d2d35]">
            <span class="text-[11px] text-slate-500 dark:text-zinc-400 pl-2 font-medium">Platform:</span>
            
            <button id="toggle-yt-btn" onclick="toggleProvider('youtube')" class="px-2.5 py-1 rounded-lg font-medium bg-white dark:bg-[#25252c] text-slate-900 dark:text-zinc-200 border border-slate-300 dark:border-[#383842] transition flex items-center gap-1.5 shadow-sm">
              <span class="w-2 h-2 rounded-full bg-red-500" id="yt-dot"></span>
              <span class="text-[11px]">YouTube</span>
            </button>

            <button id="toggle-ig-btn" onclick="toggleProvider('instagram')" class="px-2.5 py-1 rounded-lg font-medium bg-white dark:bg-[#25252c] text-slate-900 dark:text-zinc-200 border border-slate-300 dark:border-[#383842] transition flex items-center gap-1.5 shadow-sm">
              <span class="w-2 h-2 rounded-full bg-pink-500" id="ig-dot"></span>
              <span class="text-[11px]">Instagram</span>
            </button>
          </div>

        </div>

        <!-- SEARCH PROMPT INPUT BOX -->
        <div class="w-full bg-white dark:bg-[#16161a] rounded-2xl border border-slate-200 dark:border-[#2d2d35] focus-within:border-emerald-500 shadow-sm transition p-3.5 flex flex-col justify-between min-h-[110px] relative">
          
          <textarea 
            id="main-search-input"
            rows="2"
            onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); executeSearch(); }"
            placeholder="Ketik topik isu publik... (misal: 'krisis ketenagakerjaan indonesia', 'krisis bbm buruh', 'susah cari kerja')"
            class="w-full bg-transparent text-sm text-slate-900 dark:text-zinc-100 placeholder-slate-400 dark:placeholder-zinc-500 focus:outline-none resize-none leading-relaxed"
          ></textarea>

          <div class="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-[#222226]">
            <div class="flex items-center gap-2 text-slate-500 dark:text-zinc-400">
              <button onclick="triggerPlusAction()" title="Tambah Multi-URL" class="p-1 rounded-md hover:bg-slate-100 dark:hover:bg-[#222228] transition flex items-center gap-1 text-xs">
                <i data-lucide="plus" class="w-4 h-4"></i>
                <span class="text-[11px] hidden sm:inline">Add URL</span>
              </button>
              
              <button onclick="toggleSettingsModal()" title="Pengaturan Limit Scraping" class="p-1 rounded-md hover:bg-slate-100 dark:hover:bg-[#222228] transition flex items-center gap-1 text-xs">
                <i data-lucide="sliders-horizontal" class="w-4 h-4"></i>
                <span class="text-[11px] hidden sm:inline">Limit Scraping</span>
              </button>
              
              <span id="cfg-summary-pill" class="text-[10px] text-slate-500 dark:text-zinc-400 bg-slate-100 dark:bg-[#1f1f26] px-2 py-0.5 rounded border border-slate-200 dark:border-[#2d2d35]">
                300 kom &bull; 10 rep
              </span>
            </div>

            <button 
              id="btn-execute"
              onclick="executeSearch()"
              class="w-8 h-8 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 hover:opacity-90 flex items-center justify-center transition shadow font-bold"
            >
              <i data-lucide="arrow-right" class="w-4 h-4"></i>
            </button>
          </div>
        </div>

        <!-- QUICK ACCESS BANNER: RISET SENTIMEN KRISIS KETENAGAKERJAAN -->
        <div onclick="openLaborSentimentDashboard()" class="w-full p-4 rounded-2xl bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] hover:border-emerald-500 dark:hover:border-emerald-500/80 transition cursor-pointer shadow-sm flex items-center justify-between group">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/40">
                Akses Cepat Riset Utama
              </span>
              <span class="text-[10px] text-slate-500 dark:text-zinc-400 font-mono">617 Data &bull; InSet &bull; SVM &bull; Cosine</span>
            </div>
            <h3 class="text-sm font-bold text-slate-800 dark:text-zinc-100 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition">
              Analisis Sentimen: Krisis Ketenagakerjaan di Indonesia
            </h3>
            <p class="text-[11px] text-slate-500 dark:text-zinc-400">
              Lihat tabel 617 data komentar, bukti ground truth, metrik akurasi 3 model, dan uji coba sentimen live.
            </p>
          </div>
          <div class="w-8 h-8 rounded-full bg-slate-100 dark:bg-[#222228] text-slate-600 dark:text-zinc-400 group-hover:bg-emerald-600 group-hover:text-white flex items-center justify-center shrink-0 transition">
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </div>
        </div>

        <!-- Quick Access Sesuai Isu Riset -->
        <div class="w-full space-y-2 text-left">
          <div class="text-[11px] text-slate-500 dark:text-zinc-400 flex items-center justify-between font-medium px-1">
            <span class="flex items-center gap-1.5"><i data-lucide="sparkles" class="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400"></i> Topik Populer & Quick Search</span>
            <span class="text-[10px] text-slate-400 dark:text-zinc-500">Klik untuk mencari</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 text-xs">
            <button onclick="quickSearch('krisis ketenagakerjaan indonesia phk massal')" class="p-3 rounded-xl bg-white dark:bg-[#16161a] hover:bg-slate-50 dark:hover:bg-[#1c1c22] border border-slate-200 dark:border-[#2d2d35] hover:border-emerald-500 text-left transition space-y-1 group shadow-sm">
              <div class="font-semibold text-slate-800 dark:text-zinc-200 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 flex items-center gap-1.5">
                <i data-lucide="briefcase" class="w-3.5 h-3.5 text-slate-500 dark:text-zinc-400"></i>
                <span>Krisis Ketenagakerjaan</span>
              </div>
              <div class="text-[11px] text-slate-500 dark:text-zinc-400">Gelombang PHK massal pabrik</div>
            </button>
            <button onclick="quickSearch('krisis bbm dampak kenaikan harga pekerja')" class="p-3 rounded-xl bg-white dark:bg-[#16161a] hover:bg-slate-50 dark:hover:bg-[#1c1c22] border border-slate-200 dark:border-[#2d2d35] hover:border-emerald-500 text-left transition space-y-1 group shadow-sm">
              <div class="font-semibold text-slate-800 dark:text-zinc-200 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 flex items-center gap-1.5">
                <i data-lucide="fuel" class="w-3.5 h-3.5 text-slate-500 dark:text-zinc-400"></i>
                <span>Krisis BBM & Inflasi</span>
              </div>
              <div class="text-[11px] text-slate-500 dark:text-zinc-400">Biaya hidup & upah buruh</div>
            </button>
            <button onclick="quickSearch('susah cari kerja gen z sarjana pengangguran')" class="p-3 rounded-xl bg-white dark:bg-[#16161a] hover:bg-slate-50 dark:hover:bg-[#1c1c22] border border-slate-200 dark:border-[#2d2d35] hover:border-emerald-500 text-left transition space-y-1 group shadow-sm">
              <div class="font-semibold text-slate-800 dark:text-zinc-200 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 flex items-center gap-1.5">
                <i data-lucide="graduation-cap" class="w-3.5 h-3.5 text-slate-500 dark:text-zinc-400"></i>
                <span>Susah Cari Kerja Gen Z</span>
              </div>
              <div class="text-[11px] text-slate-500 dark:text-zinc-400">Fresh graduate & ribuan pelamar</div>
            </button>
            <button onclick="quickSearch('syarat batas usia maksimal 25 tahun loker')" class="p-3 rounded-xl bg-white dark:bg-[#16161a] hover:bg-slate-50 dark:hover:bg-[#1c1c22] border border-slate-200 dark:border-[#2d2d35] hover:border-emerald-500 text-left transition space-y-1 group shadow-sm">
              <div class="font-semibold text-slate-800 dark:text-zinc-200 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 flex items-center gap-1.5">
                <i data-lucide="calendar" class="w-3.5 h-3.5 text-slate-500 dark:text-zinc-400"></i>
                <span>Batas Usia 25 Thn</span>
              </div>
              <div class="text-[11px] text-slate-500 dark:text-zinc-400">Syarat usia loker di Indonesia</div>
            </button>
          </div>
        </div>

      </div>

      <!-- ============================================================== -->
      <!-- SECTION 2: DISCOVERY CARDS CONTAINER -->
      <!-- ============================================================== -->
      <div id="results-discovery-container" class="hidden w-full max-w-5xl space-y-7 pt-2">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 dark:border-[#25252c] pb-3.5">
          <div class="flex items-center gap-2">
            <span class="text-xs text-slate-500 dark:text-zinc-400">Hasil Pencarian untuk:</span>
            <span id="discovery-query-tag" class="text-xs font-semibold text-slate-800 dark:text-zinc-200 px-2 py-0.5 rounded bg-slate-200 dark:bg-[#202028]">""</span>
          </div>

          <div class="flex items-center gap-2 text-xs">
            <button id="view-tab-all" onclick="filterCardView('all')" class="px-2.5 py-1 rounded-lg font-medium bg-slate-200 dark:bg-[#25252c] text-slate-900 dark:text-white transition">Semua</button>
            <button id="view-tab-yt" onclick="filterCardView('youtube')" class="px-2.5 py-1 rounded-lg text-slate-500 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-1">
              <i data-lucide="youtube" class="w-3.5 h-3.5 text-red-500"></i>
              <span>YouTube</span>
            </button>
            <button id="view-tab-ig" onclick="filterCardView('instagram')" class="px-2.5 py-1 rounded-lg text-slate-500 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-1">
              <i data-lucide="instagram" class="w-3.5 h-3.5 text-pink-500"></i>
              <span>Instagram</span>
            </button>
          </div>
        </div>

        <div id="yt-cards-container" class="space-y-3"></div>
        <div id="ig-cards-container" class="space-y-3"></div>
      </div>

      <!-- ============================================================== -->
      <!-- SECTION 3: DEEP DETAIL VIEW (MEDIA PLAYER & COMMENTS) -->
      <!-- ============================================================== -->
      <div id="deep-detail-container" class="hidden w-full max-w-5xl space-y-6 pt-4">
        <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-4">
          <div class="flex flex-col md:flex-row gap-5">
            <div id="detail-media-container" class="w-full md:w-80 h-48 rounded-xl overflow-hidden bg-black border border-slate-200 dark:border-zinc-800 shrink-0 relative flex items-center justify-center"></div>
            
            <div class="flex-1 space-y-2.5">
              <div class="flex items-center gap-2">
                <span id="detail-platform-badge" class="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded font-mono"></span>
                <span id="detail-author" class="text-xs text-slate-500 dark:text-zinc-400 font-medium"></span>
              </div>
              <h2 id="detail-title" class="text-base font-bold text-slate-900 dark:text-zinc-100 leading-snug"></h2>
              <div class="flex flex-wrap items-center gap-3 text-xs text-slate-500 dark:text-zinc-400 pt-1">
                <span id="detail-views"></span>
                <span id="detail-likes"></span>
                <span id="detail-comments-count"></span>
              </div>
              <p id="detail-desc" class="text-xs text-slate-600 dark:text-zinc-400 line-clamp-3 leading-relaxed pt-1"></p>
            </div>
          </div>
        </div>

        <!-- Threaded Comments -->
        <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-[#222226] pb-3">
            <h3 class="text-sm font-bold text-slate-800 dark:text-zinc-200 flex items-center gap-2">
              <i data-lucide="message-square" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
              <span>Komentar Netizen & Balasan Bersarang</span>
            </h3>
            <input id="detail-comment-search" oninput="filterCommentsLive(this.value)" type="text" placeholder="Cari dalam komentar..." class="bg-slate-100 dark:bg-[#1f1f26] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-2.5 py-1 text-xs text-slate-800 dark:text-zinc-200 focus:outline-none" />
          </div>
          <div id="detail-comments-list" class="space-y-3"></div>
        </div>
      </div>

      <!-- ============================================================== -->
      <!-- SECTION 4: LABOR SENTIMENT RESEARCH DASHBOARD -->
      <!-- ============================================================== -->
      <div id="sentiment-research-container" class="hidden w-full max-w-5xl space-y-6 pt-4">
        
        <!-- Header Banner & Stats -->
        <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-6 shadow-sm space-y-4">
          <div class="space-y-3">
            <div class="flex flex-wrap items-center gap-2">
              <span class="text-[11px] font-semibold uppercase px-2.5 py-0.5 rounded bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/40 flex items-center gap-1.5 font-mono">
                <i data-lucide="award" class="w-3.5 h-3.5"></i>
                Studi Komparasi Sentimen
              </span>
              <span class="text-[11px] px-2.5 py-0.5 rounded bg-slate-100 dark:bg-[#1f1f26] text-slate-600 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] font-mono">
                Platform: YouTube (Real Public Discourse)
              </span>
              <span class="text-[11px] px-2.5 py-0.5 rounded bg-slate-100 dark:bg-[#1f1f26] text-slate-600 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] font-mono">
                Dataset: 617 Data Komentar Riil Valid
              </span>
            </div>
            
            <h1 class="text-xl md:text-2xl font-bold text-slate-900 dark:text-zinc-100 tracking-tight">
              Analisis Sentimen Publik terhadap Krisis Ketenagakerjaan di Indonesia
            </h1>
            <p class="text-xs md:text-sm text-slate-600 dark:text-zinc-400 max-w-3xl leading-relaxed">
              Perbandingan 3 metode klasifikasi teks: 
              <strong class="text-slate-900 dark:text-zinc-200">InSet Lexicon</strong>, 
              <strong class="text-slate-900 dark:text-zinc-200">Linear SVM</strong>, dan 
              <strong class="text-slate-900 dark:text-zinc-200">Cosine Similarity</strong> 
              pada isu PHK massal, aturan batas usia loker, sarjana menganggur, dan pesangon buruh.
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
        </div>

        <!-- Sub Tabs Navigation -->
        <div class="flex items-center gap-2 p-1 bg-slate-200/80 dark:bg-[#16161a] rounded-xl border border-slate-300 dark:border-[#2d2d35] text-xs overflow-x-auto">
          <button id="s-subtab-komparasi" onclick="switchSentimentSubtab('komparasi')" class="px-3.5 py-2 rounded-lg font-semibold bg-white dark:bg-[#25252c] text-slate-900 dark:text-white transition flex items-center gap-2 shrink-0 shadow-sm">
            <i data-lucide="scale" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
            <span>Perbandingan 3 Metode & Metrik Evaluasi</span>
          </button>
          <button id="s-subtab-dataset" onclick="switchSentimentSubtab('dataset')" class="px-3.5 py-2 rounded-lg font-medium text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="database" class="w-4 h-4"></i>
            <span>Tabel & Bukti Ground Truth (617 Data)</span>
          </button>
          <button id="s-subtab-tester" onclick="switchSentimentSubtab('tester')" class="px-3.5 py-2 rounded-lg font-medium text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="flask-conical" class="w-4 h-4"></i>
            <span>Interactive Live Tester (3 Model)</span>
          </button>
          <button id="s-subtab-metodologi" onclick="switchSentimentSubtab('metodologi')" class="px-3.5 py-2 rounded-lg font-medium text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-2 shrink-0">
            <i data-lucide="book-open" class="w-4 h-4"></i>
            <span>Metodologi 5 Tahap Preprocessing</span>
          </button>
        </div>

        <!-- SUBTAB 1: PERBANDINGAN 3 METODE & METRIK EVALUASI -->
        <div id="subtab-content-komparasi" class="space-y-6">
          
          <!-- 3 Method Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-bold text-slate-500 dark:text-zinc-400 uppercase tracking-wider">Metode 1: Lexicon</span>
                <span class="text-xs px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-400 font-semibold font-mono">InSet Lexicon</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-slate-900 dark:text-white">99.19%</div>
                <div class="text-[11px] text-slate-500 dark:text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set)</div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-[#24242c] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block">Macro F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">98.51%</span>
                </div>
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block">Weighted F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">99.19%</span>
                </div>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-zinc-400 leading-snug">
                9.083 leksikon bahasa Indonesia dengan aturan inversi kata negasi.
              </p>
            </div>

            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-bold text-slate-500 dark:text-zinc-400 uppercase tracking-wider">Metode 2: Machine Learning</span>
                <span class="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 dark:bg-[#202028] dark:text-zinc-300 font-semibold font-mono">Linear SVM</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-slate-900 dark:text-white">70.16%</div>
                <div class="text-[11px] text-slate-500 dark:text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set)</div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-[#24242c] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block">Macro F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">53.88%</span>
                </div>
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block">Weighted F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">66.78%</span>
                </div>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-zinc-400 leading-snug">
                TF-IDF Unigram/Bigram dengan Support Vector Classifier.
              </p>
            </div>

            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-bold text-slate-500 dark:text-zinc-400 uppercase tracking-wider">Metode 3: Distance Metric</span>
                <span class="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 dark:bg-[#202028] dark:text-zinc-300 font-semibold font-mono">Cosine Sim</span>
              </div>
              <div>
                <div class="text-3xl font-extrabold text-slate-900 dark:text-white">67.74%</div>
                <div class="text-[11px] text-slate-500 dark:text-zinc-400 font-medium">Akurasi Keseluruhan (Test Set)</div>
              </div>
              <div class="pt-2 border-t border-slate-100 dark:border-[#24242c] grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block">Macro F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">58.73%</span>
                </div>
                <div>
                  <span class="text-slate-400 dark:text-zinc-500 text-[10px] block">Weighted F1</span>
                  <span class="font-bold text-slate-800 dark:text-zinc-200">68.39%</span>
                </div>
              </div>
              <p class="text-[11px] text-slate-500 dark:text-zinc-400 leading-snug">
                Nearest Centroid dalam ruang TF-IDF dengan kemiripan kosinus.
              </p>
            </div>

          </div>

          <!-- Main Benchmark Comparison Table -->
          <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-4">
            <div>
              <h3 class="text-sm font-bold text-slate-900 dark:text-zinc-100 flex items-center gap-2">
                <i data-lucide="table" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
                Tabel Komparasi Performa 3 Metode (Test Set N=124)
              </h3>
              <p class="text-xs text-slate-500 dark:text-zinc-400">Pengujian pada Data Uji yang identik (20% Stratified Split dari 617 data).</p>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-xs text-left">
                <thead class="bg-slate-50 dark:bg-[#1a1a20] text-slate-600 dark:text-zinc-400 border-b border-slate-200 dark:border-[#2d2d35]">
                  <tr>
                    <th class="px-4 py-3 font-semibold">Metode Analisis Sentimen</th>
                    <th class="px-4 py-3 font-semibold">Teknik Algoritma</th>
                    <th class="px-4 py-3 font-semibold text-center">Akurasi</th>
                    <th class="px-4 py-3 font-semibold text-center">Precision (Macro)</th>
                    <th class="px-4 py-3 font-semibold text-center">Recall (Macro)</th>
                    <th class="px-4 py-3 font-semibold text-center">F1-Score (Macro)</th>
                    <th class="px-4 py-3 font-semibold text-center">F1-Score (Weighted)</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 dark:divide-[#222228] text-slate-700 dark:text-zinc-300">
                  <tr class="hover:bg-slate-50 dark:hover:bg-[#1c1c22] transition">
                    <td class="px-4 py-3 font-semibold text-emerald-700 dark:text-emerald-400">InSet Lexicon</td>
                    <td class="px-4 py-3 text-slate-500 dark:text-zinc-400">Kamus Skor Bobot + Inversi Negasi</td>
                    <td class="px-4 py-3 text-center font-bold text-emerald-700 dark:text-emerald-400">99.19%</td>
                    <td class="px-4 py-3 text-center">98.67%</td>
                    <td class="px-4 py-3 text-center">98.41%</td>
                    <td class="px-4 py-3 text-center font-semibold">98.51%</td>
                    <td class="px-4 py-3 text-center font-semibold">99.19%</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-[#1c1c22] transition">
                    <td class="px-4 py-3 font-semibold text-slate-800 dark:text-zinc-200">Linear SVM</td>
                    <td class="px-4 py-3 text-slate-500 dark:text-zinc-400">TF-IDF (1,2) + LinearSVC (C=1.0)</td>
                    <td class="px-4 py-3 text-center font-bold">70.16%</td>
                    <td class="px-4 py-3 text-center">61.76%</td>
                    <td class="px-4 py-3 text-center">51.44%</td>
                    <td class="px-4 py-3 text-center font-semibold">53.88%</td>
                    <td class="px-4 py-3 text-center font-semibold">66.78%</td>
                  </tr>
                  <tr class="hover:bg-slate-50 dark:hover:bg-[#1c1c22] transition">
                    <td class="px-4 py-3 font-semibold text-slate-800 dark:text-zinc-200">Cosine Similarity</td>
                    <td class="px-4 py-3 text-slate-500 dark:text-zinc-400">TF-IDF (1,2) + Nearest Class Centroid</td>
                    <td class="px-4 py-3 text-center font-bold">67.74%</td>
                    <td class="px-4 py-3 text-center">58.03%</td>
                    <td class="px-4 py-3 text-center">59.67%</td>
                    <td class="px-4 py-3 text-center font-semibold">58.73%</td>
                    <td class="px-4 py-3 text-center font-semibold">68.39%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Confusion Matrix Visuals -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-zinc-100">1. InSet Lexicon CM</span>
                <span class="text-[10px] text-emerald-700 dark:text-emerald-400 font-mono">123/124 Benar</span>
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

            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-zinc-100">2. Linear SVM CM</span>
                <span class="text-[10px] text-slate-500 dark:text-zinc-400 font-mono">87/124 Benar</span>
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

            <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-4 shadow-sm space-y-3">
              <div class="flex items-center justify-between">
                <span class="font-bold text-xs text-slate-900 dark:text-zinc-100">3. Cosine Sim CM</span>
                <span class="text-[10px] text-slate-500 dark:text-zinc-400 font-mono">84/124 Benar</span>
              </div>
              <div class="grid grid-cols-4 gap-1 text-[10px] text-center font-mono">
                <div class="text-slate-400 py-0.5">Aktual\Pred</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Neg</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Net</div>
                <div class="bg-slate-100 dark:bg-[#202028] py-0.5 rounded">Pos</div>

                <div class="text-slate-500 text-left pl-1">Neg (79)</div>
                <div class="bg-slate-200 dark:bg-[#282832] font-bold py-1 rounded">61</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">8</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">10</div>

                <div class="text-slate-500 text-left pl-1">Net (24)</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">7</div>
                <div class="bg-slate-200 dark:bg-[#282832] font-bold py-1 rounded">13</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">4</div>

                <div class="text-slate-500 text-left pl-1">Pos (21)</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">6</div>
                <div class="bg-slate-50 dark:bg-[#1c1c22] py-1 rounded">5</div>
                <div class="bg-slate-200 dark:bg-[#282832] font-bold py-1 rounded">10</div>
              </div>
            </div>

          </div>
        </div>

        <!-- SUBTAB 2: TABEL & BUKTI GROUND TRUTH DATASET -->
        <div id="subtab-content-dataset" class="hidden space-y-4">
          <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-4">
            
            <div class="flex flex-col sm:flex-row items-center justify-between gap-3">
              <div>
                <h3 class="text-sm font-bold text-slate-900 dark:text-zinc-100 flex items-center gap-2">
                  <i data-lucide="database" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
                  <span>Tabel Bukti Ground Truth & Prediksi 3 Model (N=617)</span>
                </h3>
                <p class="text-xs text-slate-500 dark:text-zinc-400">Data komentar riil publik dilengkapi teks awal, normalisasi slang, hasil stemming Sastrawi, dan label acuan ground truth.</p>
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

            <!-- Filters -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1 text-xs">
              <input id="ds-filter-query" onkeyup="if(event.key==='Enter') applyDatasetFilters()" type="text" placeholder="Cari kata kunci (misal: phk, batas usia, sarjana, pabrik)..." class="bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-3 py-2 text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500" />
              <select id="ds-filter-sentiment" onchange="applyDatasetFilters()" class="bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-3 py-2 text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500">
                <option value="all">Semua Sentimen (Positif, Negatif, Netral)</option>
                <option value="negatif">Negatif Saja</option>
                <option value="netral">Netral Saja</option>
                <option value="positif">Positif Saja</option>
              </select>
            </div>

            <!-- Data Table -->
            <div class="overflow-x-auto border border-slate-200 dark:border-[#2d2d35] rounded-xl max-h-[520px]">
              <table class="w-full text-xs text-left">
                <thead class="bg-slate-50 dark:bg-[#1a1a20] text-slate-600 dark:text-zinc-400 sticky top-0 z-10 border-b border-slate-200 dark:border-[#2d2d35]">
                  <tr>
                    <th class="px-3 py-2.5 font-semibold w-12">No</th>
                    <th class="px-3 py-2.5 font-semibold min-w-[280px]">Komentar Netizen Asli</th>
                    <th class="px-3 py-2.5 font-semibold min-w-[200px]">Hasil Stemming Sastrawi</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-28">Ground Truth (Bukti)</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">InSet Lexicon</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">Linear SVM</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-24">Cosine Sim</th>
                    <th class="px-3 py-2.5 font-semibold text-center w-20">Split</th>
                  </tr>
                </thead>
                <tbody id="ds-table-body" class="divide-y divide-slate-100 dark:divide-[#222228] text-slate-700 dark:text-zinc-300">
                  <tr>
                    <td colspan="8" class="px-4 py-8 text-center text-slate-400 dark:text-zinc-500">Memuat data komentar...</td>
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
        </div>

        <!-- SUBTAB 3: INTERACTIVE LIVE TESTER (3 MODEL) -->
        <div id="subtab-content-tester" class="hidden space-y-4">
          <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-4">
            
            <div>
              <h3 class="text-sm font-bold text-slate-900 dark:text-zinc-100 flex items-center gap-2">
                <i data-lucide="flask-conical" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
                <span>Uji Coba Sentimen Realtime (Live Tester 3 Metode)</span>
              </h3>
              <p class="text-xs text-slate-500 dark:text-zinc-400">Ketik opini publik untuk memproses 5 tahapan NLP Preprocessing dan melihat perbandingan output ketiga model secara instan.</p>
            </div>

            <!-- Sample Chips -->
            <div class="space-y-1.5">
              <span class="text-[11px] text-slate-500 dark:text-zinc-400">Pilih contoh kalimat:</span>
              <div class="flex flex-wrap gap-2 text-xs">
                <button onclick="setTesterSample(1)" class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-[#1c1c22] hover:bg-slate-200 dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] text-[11px] transition text-left">
                  "Susah bgt nyari loker sekarang, kena phk massal dan batas usia max 25 thn!"
                </button>
                <button onclick="setTesterSample(2)" class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-[#1c1c22] hover:bg-slate-200 dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] text-[11px] transition text-left">
                  "Semoga pemerintah membuka banyak lapangan kerja baru, tetap semangat dan optimis!"
                </button>
                <button onclick="setTesterSample(3)" class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-[#1c1c22] hover:bg-slate-200 dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] text-[11px] transition text-left">
                  "Kemnaker mengumumkan data pengangguran terbuka nasional triwulan pertama tahun ini."
                </button>
                <button onclick="setTesterSample(4)" class="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-[#1c1c22] hover:bg-slate-200 dark:hover:bg-[#25252c] text-slate-700 dark:text-zinc-300 border border-slate-200 dark:border-[#2d2d35] text-[11px] transition text-left">
                  "Gaji tidak sebanding dengan beban kerja, lembur tidak dibayar dan tidak ada bonus."
                </button>
              </div>
            </div>

            <!-- Input Box -->
            <div class="space-y-2">
              <textarea id="tester-input-text" rows="3" placeholder="Ketik kalimat atau komentar opini media sosial di sini..." class="w-full bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#2d2d35] rounded-xl p-3 text-xs text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500 leading-relaxed"></textarea>
              <div class="flex justify-end">
                <button id="btn-run-tester" onclick="runLiveSentimentTester()" class="px-4 py-2 rounded-xl bg-zinc-900 hover:bg-zinc-800 dark:bg-white dark:hover:bg-zinc-200 text-white dark:text-zinc-900 font-semibold text-xs flex items-center gap-2 transition shadow">
                  <i data-lucide="play" class="w-3.5 h-3.5"></i>
                  <span>Analisis Sentimen (3 Model)</span>
                </button>
              </div>
            </div>

            <!-- Result Box -->
            <div id="tester-result-box" class="hidden space-y-4 pt-2 border-t border-slate-100 dark:border-[#24242c]">
              
              <!-- Preprocessing Steps -->
              <div class="bg-slate-50 dark:bg-[#141418] border border-slate-200 dark:border-[#25252c] rounded-xl p-4 space-y-3">
                <span class="text-xs font-bold text-slate-900 dark:text-zinc-200 flex items-center gap-2">
                  <i data-lucide="git-commit" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
                  Hasil 5 Tahapan NLP Preprocessing
                </span>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px]">
                  <div class="bg-white dark:bg-[#1c1c22] p-2.5 rounded-lg border border-slate-200 dark:border-[#292932]">
                    <span class="text-slate-400 dark:text-zinc-500 block text-[10px] font-mono">1. Case Folding</span>
                    <span id="test-prep-cf" class="text-slate-800 dark:text-zinc-300 font-mono"></span>
                  </div>
                  <div class="bg-white dark:bg-[#1c1c22] p-2.5 rounded-lg border border-slate-200 dark:border-[#292932]">
                    <span class="text-slate-400 dark:text-zinc-500 block text-[10px] font-mono">2 & 3. Slang Normalization (Formal)</span>
                    <span id="test-prep-norm" class="text-slate-800 dark:text-zinc-300 font-mono"></span>
                  </div>
                  <div class="bg-white dark:bg-[#1c1c22] p-2.5 rounded-lg border border-slate-200 dark:border-[#292932]">
                    <span class="text-slate-400 dark:text-zinc-500 block text-[10px] font-mono">4. Stopwords Removed (Negation Kept)</span>
                    <span id="test-prep-stop" class="text-slate-800 dark:text-zinc-300 font-mono"></span>
                  </div>
                  <div class="bg-white dark:bg-[#1c1c22] p-2.5 rounded-lg border border-slate-200 dark:border-[#292932]">
                    <span class="text-slate-400 dark:text-zinc-500 block text-[10px] font-mono">5. Sastrawi Stemming (Final Tokens)</span>
                    <span id="test-prep-stem" class="text-emerald-700 dark:text-emerald-400 font-mono font-semibold"></span>
                  </div>
                </div>
              </div>

              <!-- 3 Methods Side-by-Side Prediction Cards -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                
                <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-xl p-4 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-800 dark:text-zinc-200">InSet Lexicon</span>
                    <span id="test-pred-lex-badge" class="px-2 py-0.5 rounded text-[10px] font-bold font-mono"></span>
                  </div>
                  <div class="text-lg font-extrabold text-slate-900 dark:text-white" id="test-pred-lex-score"></div>
                  <div class="text-[10px] text-slate-500 dark:text-zinc-400" id="test-pred-lex-words"></div>
                </div>

                <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-xl p-4 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-800 dark:text-zinc-200">Linear SVM</span>
                    <span id="test-pred-svm-badge" class="px-2 py-0.5 rounded text-[10px] font-bold font-mono"></span>
                  </div>
                  <div class="text-lg font-extrabold text-slate-900 dark:text-white" id="test-pred-svm-conf"></div>
                  <div class="text-[10px] text-slate-500 dark:text-zinc-400" id="test-pred-svm-probs"></div>
                </div>

                <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-xl p-4 space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-800 dark:text-zinc-200">Cosine Similarity</span>
                    <span id="test-pred-cos-badge" class="px-2 py-0.5 rounded text-[10px] font-bold font-mono"></span>
                  </div>
                  <div class="text-lg font-extrabold text-slate-900 dark:text-white" id="test-pred-cos-sim"></div>
                  <div class="text-[10px] text-slate-500 dark:text-zinc-400" id="test-pred-cos-sims"></div>
                </div>

              </div>

            </div>

          </div>
        </div>

        <!-- SUBTAB 4: METODOLOGI PREPROCESSING & FORMULASI MODEL -->
        <div id="subtab-content-metodologi" class="hidden space-y-4">
          <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl p-5 shadow-sm space-y-5 text-xs text-slate-700 dark:text-zinc-300 leading-relaxed">
            <div>
              <h3 class="text-sm font-bold text-slate-900 dark:text-zinc-100 flex items-center gap-2 mb-1">
                <i data-lucide="book-open" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
                <span>Metodologi 5 Tahap Preprocessing NLP</span>
              </h3>
              <p class="text-slate-500 dark:text-zinc-400">Standar prapemrosesan korpus teks media sosial bahasa Indonesia non-formal.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-2">
                <span class="font-bold text-slate-900 dark:text-zinc-100 text-xs block">Tahap 1: Case Folding</span>
                <p class="text-slate-600 dark:text-zinc-400 text-[11px]">Mengubah seluruh karakter teks menjadi huruf kecil (lowercase) agar kata seragam tanpa terpengaruh gaya penulisan kapital netizen.</p>
              </div>

              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-2">
                <span class="font-bold text-slate-900 dark:text-zinc-100 text-xs block">Tahap 2: Tokenisasi & Pembersihan</span>
                <p class="text-slate-600 dark:text-zinc-400 text-[11px]">Membersihkan URL, mention (@user), hashtag (#tag), angka, dan tanda baca, lalu memecah kalimat menjadi token kata individual.</p>
              </div>

              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-2">
                <span class="font-bold text-slate-900 dark:text-zinc-100 text-xs block">Tahap 3: Normalisasi Kata (Slang to Formal)</span>
                <p class="text-slate-600 dark:text-zinc-400 text-[11px]">Memetakan kata tidak baku/singkatan menggunakan 15.006 entri kamus kata alay (colloquial-indonesian-lexicon) dan kamus istilah ketenagakerjaan.</p>
              </div>

              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-2">
                <span class="font-bold text-slate-900 dark:text-zinc-100 text-xs block">Tahap 4: Stopword Removal (Negation-Preserving)</span>
                <p class="text-slate-600 dark:text-zinc-400 text-[11px]">Menghapus kata umum tanpa makna, namun secara ketat menjaga kata negasi (tidak, bukan, belum, jangan) agar polaritas sentimen tidak rusak.</p>
              </div>

              <div class="p-4 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-2 md:col-span-2">
                <span class="font-bold text-slate-900 dark:text-zinc-100 text-xs block">Tahap 5: Stemming Sastrawi dengan Caching</span>
                <p class="text-slate-600 dark:text-zinc-400 text-[11px]">Mengubah kata berimbuhan menjadi bentuk dasarnya menggunakan algoritma Nazief-Adriani melalui PySastrawi dengan memoization cache berkecepatan O(1).</p>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- MODAL: SETTINGS PARAMETER SCRAPING -->
    <div id="modal-settings" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] rounded-2xl max-w-md w-full p-5 space-y-4 shadow-2xl">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-[#24242c] pb-3">
          <div class="flex items-center gap-2">
            <i data-lucide="sliders-horizontal" class="w-4 h-4 text-emerald-600 dark:text-emerald-400"></i>
            <h3 class="text-sm font-semibold text-slate-900 dark:text-zinc-100">Pengaturan Parameter Scraping</h3>
          </div>
          <button onclick="toggleSettingsModal()" class="text-slate-400 hover:text-slate-600 dark:text-zinc-500 dark:hover:text-zinc-300">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>

        <div class="space-y-3.5 text-xs">
          <div>
            <label class="block text-slate-700 dark:text-zinc-300 mb-1 font-medium">Maksimal Komentar Utama (Per Konten)</label>
            <input id="set-max-comments" type="number" value="300" min="10" max="1500" class="w-full bg-slate-50 dark:bg-[#1f1f26] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-3 py-2 text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500" />
            <span class="text-[10px] text-slate-400 dark:text-zinc-500">Default: 300 komentar (bisa dinaikkan hingga 1500)</span>
          </div>

          <div>
            <label class="block text-slate-700 dark:text-zinc-300 mb-1 font-medium">Batas Balasan / Replies (Per Komentar)</label>
            <input id="set-replies-per-comment" type="number" value="10" min="0" max="30" class="w-full bg-slate-50 dark:bg-[#1f1f26] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-3 py-2 text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500" />
            <span class="text-[10px] text-slate-400 dark:text-zinc-500">Default: 10 balasan per komentar induk</span>
          </div>

          <!-- Instagram Session ID Input -->
          <div class="pt-2 border-t border-slate-100 dark:border-[#24242c] space-y-1.5">
            <div class="flex items-center justify-between">
              <label class="text-slate-700 dark:text-zinc-300 font-medium flex items-center gap-1.5">
                <i data-lucide="instagram" class="w-3.5 h-3.5 text-pink-500"></i>
                <span>Instagram Session ID (Live Comments)</span>
              </label>
              <span id="ig-auth-status-badge" class="text-[9px] px-2 py-0.5 rounded bg-slate-100 dark:bg-[#202028] text-slate-500 dark:text-zinc-400 border border-slate-200 dark:border-[#2d2d35]">Mengecek...</span>
            </div>
            <div class="flex gap-2">
              <input id="set-ig-sessionid" type="password" placeholder="Tempel sessionid dari Cookies browser..." class="flex-1 bg-slate-50 dark:bg-[#1f1f26] border border-slate-200 dark:border-[#2d2d35] rounded-lg px-3 py-1.5 text-slate-900 dark:text-zinc-100 focus:outline-none focus:border-emerald-500 font-mono text-[11px]" />
              <button type="button" onclick="saveInstagramSessionId()" class="px-3 py-1.5 rounded-lg bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 font-medium text-[11px] transition shrink-0">Simpan</button>
            </div>
            <p class="text-[10px] text-slate-400 dark:text-zinc-500 leading-tight">Dapatkan dari Inspect Browser (F12) &rarr; Application &rarr; Cookies &rarr; instagram.com &rarr; sessionid.</p>
          </div>
        </div>

        <div class="pt-2 flex items-center justify-end gap-2 border-t border-slate-100 dark:border-[#24242c]">
          <button onclick="toggleSettingsModal()" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-[#202028] dark:hover:bg-[#282832] text-xs text-slate-700 dark:text-zinc-300">Tutup</button>
          <button onclick="saveSettingsConfig()" class="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-xs font-semibold text-white shadow-sm">Simpan Pengaturan</button>
        </div>
      </div>
    </div>

  </main>

  <!-- ============================================== -->
  <!-- JAVASCRIPT LOGIC CORE -->
  <!-- ============================================== -->
  <script>
    // State Global
    let searchMode = 'topic';
    let currentScrapedData = null;
    let currentComments = [];
    let isSidebarOpen = true;
    let sentimentDatasetPage = 1;
    let sentimentDatasetTotalPages = 1;

    // Platform Provider State
    let providerFilters = {
      youtube: true,
      instagram: true
    };

    // Config Limits
    let scrapeConfig = {
      maxComments: 300,
      repliesPerComment: 10
    };

    // Inisialisasi Tema & Ikon
    initTheme();
    lucide.createIcons();
    loadSavedHistory();
    checkInstagramConfig();

    // ==============================================
    // THEME MANAGEMENT (DARK / LIGHT TOGGLE)
    // ==============================================
    function initTheme() {
      const savedTheme = localStorage.getItem('app-theme') || 'dark';
      if (savedTheme === 'light') {
        document.documentElement.classList.remove('dark');
      } else {
        document.documentElement.classList.add('dark');
      }
    }

    function toggleTheme() {
      const isDark = document.documentElement.classList.contains('dark');
      if (isDark) {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('app-theme', 'light');
        showToast('Tema terang diaktifkan', 'info');
      } else {
        document.documentElement.classList.add('dark');
        localStorage.setItem('app-theme', 'dark');
        showToast('Tema gelap diaktifkan', 'info');
      }
      lucide.createIcons();
    }

    // ==============================================
    // TOAST NOTIFICATIONS (NO EMOJIS, LUCIDE ICONS)
    // ==============================================
    function showToast(message, type = 'info') {
      const container = document.getElementById('toast-container');
      const toast = document.createElement('div');
      const isSuccess = type === 'success';
      const isError = type === 'error';
      
      toast.className = `flex items-center gap-2 px-3.5 py-2.5 rounded-xl border shadow-xl text-xs font-medium transition-all duration-300 transform translate-y-2 opacity-0 pointer-events-auto ${
        isSuccess ? 'bg-emerald-950 text-emerald-200 border-emerald-800' : 
        isError ? 'bg-red-950 text-red-200 border-red-800' : 
        'bg-slate-900 dark:bg-[#1c1c22] text-white border-slate-700 dark:border-[#2e2e38]'
      }`;

      const iconName = isSuccess ? 'check-circle' : isError ? 'alert-triangle' : 'info';

      toast.innerHTML = `
        <i data-lucide="${iconName}" class="w-4 h-4 shrink-0"></i>
        <span>${escapeHtml(message)}</span>
      `;
      container.appendChild(toast);
      lucide.createIcons();

      setTimeout(() => { toast.classList.remove('translate-y-2', 'opacity-0'); }, 10);
      setTimeout(() => {
        toast.classList.add('opacity-0', 'translate-y-2');
        setTimeout(() => toast.remove(), 300);
      }, 3500);
    }

    // ==============================================
    // SIDEBAR & VIEW CONTROLS
    // ==============================================
    function toggleSidebar() {
      const sidebar = document.getElementById('main-sidebar');
      const openBtn = document.getElementById('btn-open-sidebar');
      isSidebarOpen = !isSidebarOpen;
      if (isSidebarOpen) {
        sidebar.classList.remove('-ml-64');
        openBtn.classList.add('hidden');
      } else {
        sidebar.classList.add('-ml-64');
        openBtn.classList.remove('hidden');
      }
    }

    function resetToDiscovery() {
      document.getElementById('hero-discovery-container').classList.remove('hidden');
      document.getElementById('results-discovery-container').classList.add('hidden');
      document.getElementById('deep-detail-container').classList.add('hidden');
      if (document.getElementById('sentiment-research-container')) {
        document.getElementById('sentiment-research-container').classList.add('hidden');
      }
      document.getElementById('btn-back-to-search').classList.add('hidden');
      document.getElementById('btn-save-current').classList.add('hidden');
      document.getElementById('export-dropdown-wrapper').classList.add('hidden');
      lucide.createIcons();
    }

    function switchSearchMode(mode) {
      searchMode = mode;
      const tBtn = document.getElementById('mode-topic-btn');
      const uBtn = document.getElementById('mode-url-btn');
      const activeClass = "px-3 py-1.5 rounded-lg font-medium bg-white dark:bg-[#25252c] text-slate-900 dark:text-white transition flex items-center gap-1.5 shadow-sm";
      const inactiveClass = "px-3 py-1.5 rounded-lg font-medium text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-1.5";

      if (mode === 'topic') {
        tBtn.className = activeClass;
        uBtn.className = inactiveClass;
        document.getElementById('main-search-input').placeholder = "Ketik topik isu publik... (misal: 'krisis ketenagakerjaan indonesia', 'krisis bbm buruh', 'susah cari kerja')";
      } else {
        uBtn.className = activeClass;
        tBtn.className = inactiveClass;
        document.getElementById('main-search-input').placeholder = "Tempel link video YouTube atau Instagram di sini...";
      }
      lucide.createIcons();
    }

    function toggleProvider(prov) {
      if (prov === 'youtube') {
        providerFilters.youtube = !providerFilters.youtube;
        const btn = document.getElementById('toggle-yt-btn');
        const dot = document.getElementById('yt-dot');
        if (providerFilters.youtube) {
          btn.className = "px-2.5 py-1 rounded-lg font-medium bg-white dark:bg-[#25252c] text-slate-900 dark:text-zinc-200 border border-slate-300 dark:border-[#383842] transition flex items-center gap-1.5 shadow-sm";
          dot.className = "w-2 h-2 rounded-full bg-red-500";
        } else {
          btn.className = "px-2.5 py-1 rounded-lg font-medium bg-transparent text-slate-400 dark:text-zinc-500 border border-transparent transition flex items-center gap-1.5 opacity-60";
          dot.className = "w-2 h-2 rounded-full bg-slate-400";
        }
      } else if (prov === 'instagram') {
        providerFilters.instagram = !providerFilters.instagram;
        const btn = document.getElementById('toggle-ig-btn');
        const dot = document.getElementById('ig-dot');
        if (providerFilters.instagram) {
          btn.className = "px-2.5 py-1 rounded-lg font-medium bg-white dark:bg-[#25252c] text-slate-900 dark:text-zinc-200 border border-slate-300 dark:border-[#383842] transition flex items-center gap-1.5 shadow-sm";
          dot.className = "w-2 h-2 rounded-full bg-pink-500";
        } else {
          btn.className = "px-2.5 py-1 rounded-lg font-medium bg-transparent text-slate-400 dark:text-zinc-500 border border-transparent transition flex items-center gap-1.5 opacity-60";
          dot.className = "w-2 h-2 rounded-full bg-slate-400";
        }
      }
    }

    function quickSearch(query) {
      document.getElementById('main-search-input').value = query;
      executeSearch();
    }

    // ==============================================
    // SEARCH & SCRAPING ENGINE
    // ==============================================
    async function executeSearch() {
      const q = document.getElementById('main-search-input').value.trim();
      if (!q) return;

      if (!providerFilters.youtube && !providerFilters.instagram) {
        showToast("Aktifkan minimal satu platform (YouTube atau Instagram)!", "error");
        return;
      }

      const btn = document.getElementById('btn-execute');
      btn.disabled = true;
      btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin text-current"></i>`;
      lucide.createIcons();

      try {
        const res = await fetch('/api/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            query: q, 
            max_results: 6,
            enable_youtube: providerFilters.youtube,
            enable_instagram: providerFilters.instagram
          })
        });
        const data = await res.json();
        renderDiscoveryResults(q, data);
      } catch (err) {
        showToast("Gagal melakukan pencarian: " + err.message, "error");
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="arrow-right" class="w-4 h-4 text-current"></i>`;
        lucide.createIcons();
      }
    }

    function renderDiscoveryResults(query, data) {
      document.getElementById('hero-discovery-container').classList.add('hidden');
      document.getElementById('results-discovery-container').classList.remove('hidden');
      document.getElementById('deep-detail-container').classList.add('hidden');
      if (document.getElementById('sentiment-research-container')) {
        document.getElementById('sentiment-research-container').classList.add('hidden');
      }
      document.getElementById('btn-back-to-search').classList.remove('hidden');
      document.getElementById('discovery-query-tag').innerText = `"${query}"`;

      const ytContainer = document.getElementById('yt-cards-container');
      const igContainer = document.getElementById('ig-cards-container');
      
      const ytItems = data.youtube || [];
      const igItems = data.instagram || [];

      // Render YouTube Cards
      if (ytItems.length > 0) {
        ytContainer.innerHTML = `
          <div class="flex items-center gap-2 mb-2">
            <i data-lucide="youtube" class="w-4 h-4 text-red-500"></i>
            <span class="font-bold text-xs text-slate-800 dark:text-zinc-200">YouTube (${ytItems.length})</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            ${ytItems.map(item => `
              <div class="p-3.5 rounded-xl bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] hover:border-emerald-500 transition shadow-sm space-y-2.5">
                <div class="flex gap-3">
                  <img src="${item.thumbnail || ''}" class="w-28 h-20 object-cover rounded-lg bg-slate-200 dark:bg-zinc-800 shrink-0" />
                  <div class="flex-1 overflow-hidden space-y-1">
                    <h4 class="text-xs font-bold text-slate-900 dark:text-zinc-100 line-clamp-2 leading-snug">${escapeHtml(item.title)}</h4>
                    <p class="text-[11px] text-slate-500 dark:text-zinc-400 font-medium">${escapeHtml(item.author || '')}</p>
                    <span class="text-[10px] text-slate-400 font-mono">${item.view_text || ''}</span>
                  </div>
                </div>
                <div class="flex justify-end pt-1 border-t border-slate-100 dark:border-[#222228]">
                  <button onclick="scrapeDirectContent('youtube', '${item.url}', '${item.id}')" class="px-3 py-1.5 rounded-lg bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 text-xs font-semibold flex items-center gap-1.5 transition">
                    <i data-lucide="download-cloud" class="w-3.5 h-3.5"></i>
                    <span>Tarik Komentar</span>
                  </button>
                </div>
              </div>
            `).join('')}
          </div>
        `;
      } else {
        ytContainer.innerHTML = '';
      }

      // Render Instagram Cards
      if (igItems.length > 0) {
        igContainer.innerHTML = `
          <div class="flex items-center gap-2 mb-2 mt-4">
            <i data-lucide="instagram" class="w-4 h-4 text-pink-500"></i>
            <span class="font-bold text-xs text-slate-800 dark:text-zinc-200">Instagram (${igItems.length})</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            ${igItems.map(item => `
              <div class="p-3.5 rounded-xl bg-white dark:bg-[#16161a] border border-slate-200 dark:border-[#2d2d35] hover:border-emerald-500 transition shadow-sm space-y-2.5">
                <div class="flex gap-3">
                  <img src="${item.thumbnail || ''}" class="w-24 h-24 object-cover rounded-lg bg-slate-200 dark:bg-zinc-800 shrink-0" />
                  <div class="flex-1 overflow-hidden space-y-1">
                    <span class="text-[10px] text-pink-600 font-bold font-mono">@${escapeHtml(item.user || '')}</span>
                    <h4 class="text-xs font-bold text-slate-900 dark:text-zinc-100 line-clamp-2 leading-snug">${escapeHtml(item.title)}</h4>
                    <p class="text-[11px] text-slate-500 dark:text-zinc-400 line-clamp-2">${escapeHtml(item.caption || '')}</p>
                  </div>
                </div>
                <div class="flex justify-end pt-1 border-t border-slate-100 dark:border-[#222228]">
                  <button onclick="scrapeDirectContent('instagram', '${item.url}', '${item.id}')" class="px-3 py-1.5 rounded-lg bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 text-xs font-semibold flex items-center gap-1.5 transition">
                    <i data-lucide="download-cloud" class="w-3.5 h-3.5"></i>
                    <span>Tarik Komentar</span>
                  </button>
                </div>
              </div>
            `).join('')}
          </div>
        `;
      } else {
        igContainer.innerHTML = '';
      }

      lucide.createIcons();
    }

    async function scrapeDirectContent(platform, url, id) {
      showToast(`Memulai proses scraping data ${platform}...`, "info");
      try {
        const res = await fetch('/api/scrape', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            platform: platform,
            url: url,
            max_comments: scrapeConfig.maxComments,
            replies_per_comment: scrapeConfig.repliesPerComment
          })
        });
        const data = await res.json();
        currentScrapedData = data;
        renderScrapedDetail(data);
        showToast("Data konten & komentar berhasil ditarik!", "success");
      } catch (err) {
        showToast("Gagal melakukan scraping: " + err.message, "error");
      }
    }

    function renderScrapedDetail(data) {
      document.getElementById('results-discovery-container').classList.add('hidden');
      document.getElementById('hero-discovery-container').classList.add('hidden');
      document.getElementById('deep-detail-container').classList.remove('hidden');
      document.getElementById('btn-back-to-search').classList.remove('hidden');
      document.getElementById('btn-save-current').classList.remove('hidden');
      document.getElementById('export-dropdown-wrapper').classList.remove('hidden');

      const meta = data.metadata || {};
      const isYt = data.platform === 'youtube';

      const pBadge = document.getElementById('detail-platform-badge');
      pBadge.innerText = data.platform;
      pBadge.className = isYt ? "text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-red-100 text-red-700 dark:bg-red-950/60 dark:text-red-400 font-mono" : "text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-pink-100 text-pink-700 dark:bg-pink-950/60 dark:text-pink-400 font-mono";

      document.getElementById('detail-author').innerText = meta.channel || meta.author || '';
      document.getElementById('detail-title').innerText = meta.title || 'Untitled';
      document.getElementById('detail-views').innerText = `${meta.view_count || 0} tayangan`;
      document.getElementById('detail-likes').innerText = `${meta.like_count || 0} suka`;
      document.getElementById('detail-comments-count').innerText = `${data.comments_count_scraped || 0} komentar terambil`;
      document.getElementById('detail-desc').innerText = meta.description || '';

      const mContainer = document.getElementById('detail-media-container');
      if (isYt && meta.id) {
        mContainer.innerHTML = `<iframe src="https://www.youtube.com/embed/${meta.id}?autoplay=0" class="w-full h-full rounded-xl" allowfullscreen></iframe>`;
      } else {
        mContainer.innerHTML = `<img src="${meta.thumbnail || ''}" class="w-full h-full object-cover rounded-xl" />`;
      }

      currentComments = data.comments || [];
      renderThreadedComments(currentComments);
      lucide.createIcons();
    }

    function renderThreadedComments(comments) {
      const container = document.getElementById('detail-comments-list');
      if (!comments || comments.length === 0) {
        container.innerHTML = `<div class="text-xs text-slate-400 dark:text-zinc-500 py-6 text-center">Tidak ada komentar ditemukan</div>`;
        return;
      }

      container.innerHTML = comments.map(c => `
        <div class="p-3 rounded-xl bg-slate-50 dark:bg-[#1a1a20] border border-slate-200 dark:border-[#272730] space-y-1.5 text-xs">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-800 dark:text-zinc-200">${escapeHtml(c.author || 'Netizen')}</span>
            <span class="text-[10px] text-slate-400 font-mono">${c.votes || 0} votes &bull; ${c.time || ''}</span>
          </div>
          <p class="text-slate-700 dark:text-zinc-300 leading-relaxed">${escapeHtml(c.text || '')}</p>
          
          ${(c.replies && c.replies.length > 0) ? `
            <div class="mt-2 pl-3 border-l-2 border-slate-200 dark:border-[#2d2d35] space-y-2">
              ${c.replies.map(r => `
                <div class="p-2 rounded-lg bg-white dark:bg-[#202028] text-[11px] space-y-1">
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-slate-700 dark:text-zinc-300">${escapeHtml(r.author || 'Netizen')}</span>
                    <span class="text-[9px] text-slate-400 font-mono">${r.votes || 0} likes</span>
                  </div>
                  <p class="text-slate-600 dark:text-zinc-400">${escapeHtml(r.text || '')}</p>
                </div>
              `).join('')}
            </div>
          ` : ''}
        </div>
      `).join('');
    }

    function filterCommentsLive(q) {
      if (!q.trim()) {
        renderThreadedComments(currentComments);
        return;
      }
      const filtered = currentComments.filter(c => 
        (c.text || '').toLowerCase().includes(q.toLowerCase()) || 
        (c.author || '').toLowerCase().includes(q.toLowerCase())
      );
      renderThreadedComments(filtered);
    }

    // ==============================================
    // SAVED HISTORY & FULL CRUD
    // ==============================================
    async function loadSavedHistory() {
      try {
        const res = await fetch('/api/saved');
        const items = await res.json();
        const list = document.getElementById('saved-history-list');
        document.getElementById('saved-counter').textContent = items.length;

        if (!items || items.length === 0) {
          list.innerHTML = `<div class="text-[11px] text-slate-400 dark:text-zinc-600 px-2.5 py-4 text-center">Belum ada riwayat tersimpan</div>`;
          return;
        }

        list.innerHTML = items.map(item => {
          const isYt = item.platform === 'youtube';
          const icon = isYt ? 'youtube' : 'instagram';
          const iconColor = isYt ? 'text-red-500' : 'text-pink-500';
          const safeTitle = (item.title || 'Untitled').replace(/"/g, '&quot;');

          return `
            <div onclick="openSavedItem('${item.id}')" class="group relative flex items-center justify-between p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-[#1a1a20] transition border border-transparent hover:border-slate-200 dark:hover:border-[#2d2d35] cursor-pointer mb-1">
              <div class="flex items-center gap-2 overflow-hidden flex-1 mr-1">
                <i data-lucide="${icon}" class="w-3.5 h-3.5 ${iconColor} shrink-0"></i>
                <div class="truncate">
                  <div class="text-xs text-slate-800 dark:text-zinc-300 truncate font-medium group-hover:text-emerald-600 dark:group-hover:text-emerald-400" title="${safeTitle}">${safeTitle}</div>
                  <div class="text-[10px] text-slate-400 dark:text-zinc-500 font-mono">${item.comments_count} komentar &bull; ${escapeHtml(item.author || '')}</div>
                </div>
              </div>
              <div class="opacity-0 group-hover:opacity-100 flex items-center gap-0.5 transition shrink-0 bg-slate-200 dark:bg-[#25252c] p-0.5 rounded-lg">
                <button onclick="renameSavedHistoryItem(event, '${item.id}', '${safeTitle}')" title="Ubah Nama" class="p-1 text-slate-600 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white rounded">
                  <i data-lucide="pencil" class="w-3 h-3"></i>
                </button>
                <button onclick="exportSingleSaved(event, '${item.id}')" title="Download Excel" class="p-1 text-slate-600 dark:text-zinc-400 hover:text-emerald-600 dark:hover:text-emerald-400 rounded">
                  <i data-lucide="download" class="w-3 h-3"></i>
                </button>
                <button onclick="deleteSavedHistoryItem(event, '${item.id}', '${safeTitle}')" title="Hapus" class="p-1 text-slate-600 dark:text-zinc-400 hover:text-red-500 rounded">
                  <i data-lucide="trash-2" class="w-3 h-3"></i>
                </button>
              </div>
            </div>
          `;
        }).join('');
        lucide.createIcons();
      } catch (e) {
        console.error(e);
      }
    }

    async function openSavedItem(id) {
      try {
        const res = await fetch(`/api/saved/${id}`);
        const data = await res.json();
        currentScrapedData = data;
        renderScrapedDetail(data);
      } catch (err) {
        showToast("Gagal membuka riwayat: " + err.message, "error");
      }
    }

    async function saveCurrentContent() {
      if (!currentScrapedData) return;
      try {
        const res = await fetch('/api/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id: currentScrapedData.id,
            data: currentScrapedData
          })
        });
        const data = await res.json();
        showToast("Konten berhasil disimpan ke riwayat lokal!", "success");
        loadSavedHistory();
      } catch (err) {
        showToast("Gagal menyimpan: " + err.message, "error");
      }
    }

    async function deleteSavedHistoryItem(event, itemId, itemTitle) {
      if (event) event.stopPropagation();
      if (!confirm(`Hapus riwayat "${itemTitle}" dari database lokal?`)) return;
      try {
        const res = await fetch(`/api/saved/${itemId}`, { method: 'DELETE' });
        const data = await res.json();
        showToast(data.message || "Riwayat berhasil dihapus", "success");
        loadSavedHistory();
      } catch (e) {
        showToast("Gagal menghapus item: " + e.message, "error");
      }
    }

    async function clearAllSavedHistory() {
      const counter = document.getElementById('saved-counter').textContent;
      if (counter === '0') {
        showToast("Riwayat simpanan masih kosong.", "info");
        return;
      }
      if (!confirm("Apakah Anda yakin ingin MENGHAPUS SEMUA riwayat simpanan di database lokal?")) return;
      try {
        const res = await fetch('/api/saved', { method: 'DELETE' });
        const data = await res.json();
        showToast(data.message || "Semua riwayat dibersihkan", "success");
        loadSavedHistory();
      } catch (e) {
        showToast("Gagal membersihkan riwayat: " + e.message, "error");
      }
    }

    async function renameSavedHistoryItem(event, itemId, currentTitle) {
      if (event) event.stopPropagation();
      const newTitle = prompt("Ubah judul riwayat:", currentTitle);
      if (!newTitle || newTitle.trim() === '' || newTitle.trim() === currentTitle) return;
      try {
        const res = await fetch(`/api/saved/${itemId}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: newTitle.trim() })
        });
        const data = await res.json();
        showToast("Judul berhasil diperbarui!", "success");
        loadSavedHistory();
      } catch (e) {
        showToast("Gagal mengubah judul: " + e.message, "error");
      }
    }

    function exportSingleSaved(event, itemId) {
      if (event) event.stopPropagation();
      window.open(`/api/export/${itemId}?format=xlsx`, '_blank');
    }

    function exportAllDatabaseZip() {
      window.open('/api/export-all', '_blank');
    }

    function triggerExportCurrent(fmt) {
      if (!currentScrapedData || !currentScrapedData.id) {
        showToast("Tidak ada data aktif untuk diekspor", "error");
        return;
      }
      window.open(`/api/export/${currentScrapedData.id}?format=${fmt}`, '_blank');
    }

    function toggleExportMenu() {
      const box = document.getElementById('export-menu-box');
      box.classList.toggle('hidden');
    }

    // ==============================================
    // SENTIMENT RESEARCH DASHBOARD LOGIC
    // ==============================================
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
      const tabs = ['komparasi', 'dataset', 'tester', 'metodologi'];
      tabs.forEach(t => {
        const btn = document.getElementById(`s-subtab-${t}`);
        const content = document.getElementById(`subtab-content-${t}`);
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
      tbody.innerHTML = `<tr><td colspan="8" class="px-4 py-8 text-center text-slate-400 dark:text-zinc-500">Memuat data halaman ${page}...</td></tr>`;
      
      try {
        const url = `/api/sentiment/dataset?page=${page}&page_size=20&platform=all&sentiment=${encodeURIComponent(sent)}&query=${encodeURIComponent(q)}`;
        const res = await fetch(url);
        const data = await res.json();
        
        sentimentDatasetTotalPages = data.pages || 1;
        document.getElementById('ds-current-page').innerText = data.page;
        document.getElementById('ds-pagination-info').innerText = `Menampilkan ${((data.page-1)*20)+1} - ${Math.min(data.page*20, data.total)} dari ${data.total} data`;
        
        document.getElementById('ds-prev-btn').disabled = data.page <= 1;
        document.getElementById('ds-next-btn').disabled = data.page >= data.pages;
        
        if (!data.items || data.items.length === 0) {
          tbody.innerHTML = `<tr><td colspan="8" class="px-4 py-8 text-center text-slate-400 dark:text-zinc-500">Tidak ada data komentar yang cocok.</td></tr>`;
          return;
        }
        
        tbody.innerHTML = data.items.map((item, idx) => {
          const rowNo = ((data.page - 1) * 20) + idx + 1;
          const gt = item.sentiment_ground_truth || 'Netral';
          const lex = item.pred_lexicon || 'Netral';
          const svm = item.pred_svm || 'Netral';
          const cos = item.pred_cosine || 'Netral';
          
          const gtBadge = gt === 'Negatif' ? 'text-red-700 bg-red-50 dark:text-red-300 dark:bg-red-950/40 border-red-200 dark:border-red-900/40' : 
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
          `;
        }).join('');
      } catch (e) {
        tbody.innerHTML = `<tr><td colspan="8" class="px-4 py-8 text-center text-red-500">Gagal memuat data: ${e.message}</td></tr>`;
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
        showToast("Silakan masukkan teks opini terlebih dahulu", "error");
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
        
        document.getElementById('tester-result-box').classList.remove('hidden');
        
        const p = data.preprocessing || {};
        document.getElementById('test-prep-cf').innerText = p.case_folded || '-';
        document.getElementById('test-prep-norm').innerText = (p.tokens_normalized || []).join(', ') || '-';
        document.getElementById('test-prep-stop').innerText = (p.tokens_no_stopwords || []).join(', ') || '-';
        document.getElementById('test-prep-stem').innerText = p.processed_text || '-';
        
        const lex = data.predictions.inset_lexicon || {};
        const lexBadge = document.getElementById('test-pred-lex-badge');
        lexBadge.innerText = lex.label;
        lexBadge.className = `px-2 py-0.5 rounded text-[10px] font-bold ${lex.label === 'Negatif' ? 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-300' : lex.label === 'Positif' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-700 dark:bg-zinc-800 dark:text-zinc-300'}`;
        document.getElementById('test-pred-lex-score').innerText = `Skor: ${lex.score}`;
        const matched = (lex.matched_words || []).map(m => `${m.phrase} (${m.adjusted_weight > 0 ? '+' : ''}${m.adjusted_weight}${m.is_negated ? ' negasi' : ''})`).join(', ');
        document.getElementById('test-pred-lex-words').innerText = matched ? `Kata cocok: ${matched}` : 'Tidak ada leksikon cocok';

        const svm = data.predictions.linear_svm || {};
        const svmBadge = document.getElementById('test-pred-svm-badge');
        svmBadge.innerText = svm.label;
        svmBadge.className = `px-2 py-0.5 rounded text-[10px] font-bold ${svm.label === 'Negatif' ? 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-300' : svm.label === 'Positif' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-700 dark:bg-zinc-800 dark:text-zinc-300'}`;
        document.getElementById('test-pred-svm-conf').innerText = `Confidence: ${(svm.confidence * 100).toFixed(1)}%`;
        const probs = Object.entries(svm.probabilities || {}).map(([k, v]) => `${k}: ${(v*100).toFixed(0)}%`).join(' | ');
        document.getElementById('test-pred-svm-probs').innerText = probs;

        const cos = data.predictions.cosine_similarity || {};
        const cosBadge = document.getElementById('test-pred-cos-badge');
        cosBadge.innerText = cos.label;
        cosBadge.className = `px-2 py-0.5 rounded text-[10px] font-bold ${cos.label === 'Negatif' ? 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-300' : cos.label === 'Positif' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-700 dark:bg-zinc-800 dark:text-zinc-300'}`;
        document.getElementById('test-pred-cos-sim').innerText = `Cosine Sim: ${cos.similarity}`;
        const sims = Object.entries(cos.all_similarities || {}).map(([k, v]) => `${k}: ${v}`).join(' | ');
        document.getElementById('test-pred-cos-sims').innerText = sims;

        showToast("Sentimen berhasil diklasifikasikan!", "success");
      } catch (err) {
        showToast("Gagal memproses prediksi: " + err.message, "error");
      } finally {
        btn.innerHTML = origHtml;
        btn.disabled = false;
        lucide.createIcons();
      }
    }

    // ==============================================
    // SETTINGS MODAL & INSTAGRAM CONFIG
    // ==============================================
    function toggleSettingsModal() {
      const modal = document.getElementById('modal-settings');
      modal.classList.toggle('hidden');
    }

    function saveSettingsConfig() {
      const maxC = parseInt(document.getElementById('set-max-comments').value) || 300;
      const repC = parseInt(document.getElementById('set-replies-per-comment').value) || 10;
      scrapeConfig.maxComments = maxC;
      scrapeConfig.repliesPerComment = repC;
      document.getElementById('cfg-summary-pill').textContent = `${maxC} kom • ${repC} rep`;
      toggleSettingsModal();
      showToast("Pengaturan parameter scraping disimpan", "success");
    }

    async function checkInstagramConfig() {
      try {
        const res = await fetch('/api/config/instagram');
        const data = await res.json();
        const badge = document.getElementById('ig-auth-status-badge');
        if (data.configured) {
          badge.textContent = "Terkoneksi";
          badge.className = "text-[9px] px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/40";
        } else {
          badge.textContent = "Belum Terhubung";
          badge.className = "text-[9px] px-2 py-0.5 rounded bg-slate-100 text-slate-600 dark:bg-[#202028] dark:text-zinc-400 border border-slate-200 dark:border-[#2d2d35]";
        }
      } catch (e) {
        console.error(e);
      }
    }

    async function saveInstagramSessionId() {
      const val = document.getElementById('set-ig-sessionid').value.trim();
      if (!val) {
        showToast("Silakan masukkan sessionid", "error");
        return;
      }
      try {
        const res = await fetch('/api/config/instagram', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ sessionid: val })
        });
        const data = await res.json();
        showToast(data.message || "Sessionid disimpan!", "success");
        checkInstagramConfig();
      } catch (e) {
        showToast("Gagal menyimpan sessionid: " + e.message, "error");
      }
    }

    function triggerPlusAction() {
      switchSearchMode('url');
      document.getElementById('main-search-input').focus();
    }

    function filterCardView(filter) {
      const ytBox = document.getElementById('yt-cards-container');
      const igBox = document.getElementById('ig-cards-container');
      const allBtn = document.getElementById('view-tab-all');
      const ytBtn = document.getElementById('view-tab-yt');
      const igBtn = document.getElementById('view-tab-ig');

      const aC = "px-2.5 py-1 rounded-lg font-medium bg-slate-200 dark:bg-[#25252c] text-slate-900 dark:text-white transition shadow-sm";
      const iC = "px-2.5 py-1 rounded-lg text-slate-500 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-1";

      allBtn.className = iC;
      ytBtn.className = iC;
      igBtn.className = iC;

      if (filter === 'all') {
        allBtn.className = aC;
        ytBox.classList.remove('hidden');
        igBox.classList.remove('hidden');
      } else if (filter === 'youtube') {
        ytBtn.className = aC;
        ytBox.classList.remove('hidden');
        igBox.classList.add('hidden');
      } else if (filter === 'instagram') {
        igBtn.className = aC;
        ytBox.classList.add('hidden');
        igBox.classList.remove('hidden');
      }
    }

    function escapeHtml(text) {
      if (!text) return '';
      return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }
  </script>
</body>
</html>
'''
    with open("frontend/dist/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Clean unified frontend generated successfully!")

if __name__ == "__main__":
    generate_clean_frontend()
