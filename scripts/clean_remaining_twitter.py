with open('frontend/dist/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update providerFilters
html = html.replace("twitter: true", "twitter: false")

# 2. Hide / remove view-tab-tw
import re
html = re.sub(r'<button id="view-tab-tw".*?</button>', '', html, flags=re.DOTALL)

# 3. Update search validation
html = html.replace('if (!providerFilters.youtube && !providerFilters.instagram && !providerFilters.twitter)', 'if (!providerFilters.youtube && !providerFilters.instagram)')
html = html.replace('"Gagal: Aktifkan minimal satu engine (YouTube, Instagram, atau X)!"', '"Gagal: Aktifkan minimal satu engine (YouTube atau Instagram)!"')

with open('frontend/dist/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Remaining Twitter references cleaned!")
