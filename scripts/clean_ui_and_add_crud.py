import re

def clean_ui():
    html_path = "frontend/dist/index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # ==============================================================
    # 1. CLEAN SIDEBAR: REMOVE DUMMY CHANNELS AI SLOP & UPGRADE NAV
    # ==============================================================
    # Cari dan ganti blok Channels
    channels_pattern = r'<!-- Channels \(Kategori / Workspace Ruang Kerja Analisis\) -->.*?<!-- Saved Chats / History -->'
    clean_sidebar_nav = '''<!-- Menu Navigasi Modul -->
      <div class="mt-4 space-y-1">
        <div class="px-2.5 mb-1.5 text-[11px] font-semibold text-zinc-500 uppercase tracking-wider">Modul Kerja</div>
        <button onclick="resetToDiscovery()" class="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-zinc-200 bg-[#212121] hover:bg-[#262626] border border-[#2e2e2e] transition text-xs font-medium text-left">
          <i data-lucide="search" class="w-4 h-4 text-emerald-400 shrink-0"></i>
          <span>Scraping & Pencarian</span>
        </button>
        <button onclick="openLaborSentimentDashboard()" class="w-full flex items-center justify-between px-2.5 py-2 rounded-lg text-emerald-400 bg-emerald-950/40 hover:bg-emerald-900/50 border border-emerald-800/40 transition text-xs font-semibold text-left">
          <div class="flex items-center gap-2.5">
            <i data-lucide="bar-chart-3" class="w-4 h-4 text-emerald-400 shrink-0"></i>
            <span>Riset Sentimen Kerja</span>
          </div>
          <span class="text-[9px] bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded font-mono font-bold">617 Data</span>
        </button>
        <button onclick="toggleSettingsModal()" class="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-zinc-400 hover:text-zinc-200 hover:bg-[#212121] transition text-xs font-medium text-left">
          <i data-lucide="sliders-horizontal" class="w-4 h-4 text-zinc-400 shrink-0"></i>
          <span>Pengaturan Parameter</span>
        </button>
      </div>

      <!-- Saved Chats / History -->'''

    if re.search(channels_pattern, html, flags=re.DOTALL):
        html = re.sub(channels_pattern, clean_sidebar_nav, html, flags=re.DOTALL)
        print("Channels AI slop removed and replaced with clean module navigation!")

    # ==============================================================
    # 2. UPGRADE SAVED INTELLIGENCE HEADER IN SIDEBAR WITH CRUD ACTIONS
    # ==============================================================
    old_history_header = '''      <!-- Saved Chats / History -->
      <div class="mt-5 flex-1 overflow-y-auto space-y-1 pr-1">
        <div class="flex items-center justify-between px-2.5 mb-1.5">
          <span class="text-[11px] font-medium text-zinc-500">Saved Intelligence</span>
          <div class="flex items-center gap-1.5">
            <span id="saved-counter" class="text-[10px] text-zinc-500">0</span>
            <button onclick="exportAllDatabaseZip()" title="Download Semua Project (ZIP Excel)" class="text-zinc-500 hover:text-emerald-400 p-0.5 rounded hover:bg-[#202020] transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
            </button>
          </div>
        </div>'''

    new_history_header = '''      <!-- Saved Chats / History (Full CRUD) -->
      <div class="mt-5 flex-1 overflow-y-auto space-y-1 pr-1">
        <div class="flex items-center justify-between px-2.5 mb-2 border-b border-[#202020] pb-1.5">
          <div class="flex items-center gap-1.5">
            <span class="text-[11px] font-semibold text-zinc-400">Riwayat Simpanan</span>
            <span id="saved-counter" class="text-[10px] font-mono text-zinc-500 bg-[#212121] px-1.5 py-0.2 rounded border border-[#2d2d2d]">0</span>
          </div>
          <div class="flex items-center gap-1">
            <button onclick="clearAllSavedHistory()" title="Hapus Semua Riwayat" class="text-zinc-500 hover:text-red-400 p-1 rounded hover:bg-[#202020] transition">
              <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
            </button>
            <button onclick="exportAllDatabaseZip()" title="Download Semua Riwayat (ZIP Excel)" class="text-zinc-500 hover:text-emerald-400 p-1 rounded hover:bg-[#202020] transition">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
            </button>
          </div>
        </div>'''

    if old_history_header in html:
        html = html.replace(old_history_header, new_history_header)
        print("History header upgraded with CRUD actions!")

    # ==============================================================
    # 3. CLEAN BOTTOM PROFILE (REPLACE STATIC TB ANALYST AI SLOP)
    # ==============================================================
    old_profile_pattern = r'<!-- User Profile Footer -->\s*<div class="pt-3 border-t border-\[#202020\].*?</div>\s*</div>'
    new_profile = '''<!-- System Status Footer -->
        <div class="pt-2.5 border-t border-[#202020] flex items-center justify-between px-2 text-[11px]">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="font-medium text-zinc-400">FastAPI Engine</span>
          </div>
          <span class="text-[10px] text-zinc-500 font-mono">v2.0 &bull; Port 8000</span>
        </div>'''

    if re.search(old_profile_pattern, html, flags=re.DOTALL):
        html = re.sub(old_profile_pattern, new_profile, html, flags=re.DOTALL)
        print("Bottom profile AI slop replaced with clean system indicator!")

    # ==============================================================
    # 4. REMOVE X (TWITTER) BUTTON FROM FILTER ENGINE
    # ==============================================================
    tw_btn_pattern = r'<!-- Toggle Twitter/X -->\s*<button id="toggle-tw-btn".*?</button>'
    if re.search(tw_btn_pattern, html, flags=re.DOTALL):
        html = re.sub(tw_btn_pattern, '', html, flags=re.DOTALL)
        print("Twitter/X filter toggle removed from hero view!")

    # ==============================================================
    # 5. CLEAN TOP HEADER BAR: REMOVE DUMMY BADGES & TAGS
    # ==============================================================
    old_header_tag = '<span id="active-channel-tag"'
    # Remove #general-intelligence tag line
    html = re.sub(r'<span id="active-channel-tag".*?</span>', '', html)

    # Clean the model selector
    html = html.replace('<span class="font-semibold text-sm">social-intelligence-v2</span>', '<span class="font-semibold text-sm">Social Intelligence Hub</span>')

    # ==============================================================
    # 6. REWRITE loadSavedHistory WITH FULL INTERACTIVE CRUD FUNCTIONS
    # ==============================================================
    old_load_history_pattern = r'async function loadSavedHistory\(\)\s*\{.*?\}\s*async function openSavedItem\(id\)'
    
    new_load_history = '''async function loadSavedHistory() {
      try {
        const res = await fetch('/api/saved');
        const items = await res.json();
        const list = document.getElementById('saved-history-list');
        document.getElementById('saved-counter').textContent = items.length;

        if (!items || items.length === 0) {
          list.innerHTML = `<div class="text-[11px] text-zinc-600 px-2.5 py-4 text-center">Belum ada riwayat konten tersimpan</div>`;
          return;
        }

        list.innerHTML = items.map(item => {
          const isYt = item.platform === 'youtube';
          const icon = isYt ? 'youtube' : 'instagram';
          const iconColor = isYt ? 'text-red-400' : 'text-pink-400';
          const safeTitle = (item.title || 'Untitled').replace(/"/g, '&quot;');

          return `
            <div onclick="openSavedItem('${item.id}')" class="group relative flex items-center justify-between p-2 rounded-xl hover:bg-[#202020] transition border border-transparent hover:border-[#2d2d2d] cursor-pointer mb-1">
              <div class="flex items-center gap-2 overflow-hidden flex-1 mr-1">
                <i data-lucide="${icon}" class="w-3.5 h-3.5 ${iconColor} shrink-0"></i>
                <div class="truncate">
                  <div class="text-xs text-zinc-300 truncate font-medium group-hover:text-white" title="${safeTitle}">${safeTitle}</div>
                  <div class="text-[10px] text-zinc-500 font-mono">${item.comments_count} komentar &bull; ${item.author}</div>
                </div>
              </div>
              <div class="opacity-0 group-hover:opacity-100 flex items-center gap-0.5 transition shrink-0 bg-[#252525] p-0.5 rounded-lg border border-[#333]">
                <button onclick="renameSavedHistoryItem(event, '${item.id}', '${safeTitle}')" title="Ubah Nama" class="p-1 text-zinc-400 hover:text-white hover:bg-[#333] rounded">
                  <i data-lucide="pencil" class="w-3 h-3"></i>
                </button>
                <button onclick="exportSingleSaved(event, '${item.id}')" title="Download Excel" class="p-1 text-zinc-400 hover:text-emerald-400 hover:bg-[#333] rounded">
                  <i data-lucide="download" class="w-3 h-3"></i>
                </button>
                <button onclick="deleteSavedHistoryItem(event, '${item.id}', '${safeTitle}')" title="Hapus" class="p-1 text-zinc-400 hover:text-red-400 hover:bg-[#333] rounded">
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

    async function deleteSavedHistoryItem(event, itemId, itemTitle) {
      if (event) event.stopPropagation();
      if (!confirm(`Hapus riwayat "${itemTitle}" dari database lokal?`)) return;
      try {
        const res = await fetch(`/api/saved/${itemId}`, { method: 'DELETE' });
        const data = await res.json();
        showToast(data.message || 'Riwayat berhasil dihapus', 'success');
        loadSavedHistory();
      } catch (e) {
        showToast('Gagal menghapus item: ' + e.message, 'error');
      }
    }

    async function clearAllSavedHistory() {
      const counter = document.getElementById('saved-counter').textContent;
      if (counter === '0') {
        showToast('Riwayat simpanan masih kosong.', 'info');
        return;
      }
      if (!confirm('Apakah Anda yakin ingin MENGHAPUS SEMUA riwayat simpanan di database lokal?')) return;
      try {
        const res = await fetch('/api/saved', { method: 'DELETE' });
        const data = await res.json();
        showToast(data.message || 'Seluruh riwayat dibersihkan', 'success');
        loadSavedHistory();
      } catch (e) {
        showToast('Gagal membersihkan riwayat: ' + e.message, 'error');
      }
    }

    async function renameSavedHistoryItem(event, itemId, currentTitle) {
      if (event) event.stopPropagation();
      const newTitle = prompt('Ubah judul riwayat:', currentTitle);
      if (!newTitle || newTitle.trim() === '' || newTitle.trim() === currentTitle) return;
      try {
        const res = await fetch(`/api/saved/${itemId}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: newTitle.trim() })
        });
        const data = await res.json();
        showToast('Judul berhasil diubah!', 'success');
        loadSavedHistory();
      } catch (e) {
        showToast('Gagal mengubah judul: ' + e.message, 'error');
      }
    }

    function exportSingleSaved(event, itemId) {
      if (event) event.stopPropagation();
      window.open(`/api/export/${itemId}?format=xlsx`, '_blank');
    }

    async function openSavedItem(id)'''

    if re.search(old_load_history_pattern, html, flags=re.DOTALL):
        html = re.sub(old_load_history_pattern, new_load_history, html, flags=re.DOTALL)
        print("Full CRUD functions injected into frontend index.html!")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    print("UI cleanup and History CRUD completed successfully!")

if __name__ == "__main__":
    clean_ui()
