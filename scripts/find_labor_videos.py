import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrapers.youtube_scraper import YouTubeScraper

scraper = YouTubeScraper()
queries = [
    'susah cari kerja gen z cnbc indonesia',
    'gelombang phk massal kompas tv',
    'badai phk buruh metro tv',
    'krisis ketenagakerjaan indonesia narasi',
    'phk massal pabrik tekstil tutup'
]

found = {}
for q in queries:
    res = scraper.search_videos(q, max_results=4)
    for r in res:
        vid = r['id']
        if vid not in found:
            found[vid] = r
            print(f"{vid} | {r.get('channel', '')} | {r.get('title', '')}")
