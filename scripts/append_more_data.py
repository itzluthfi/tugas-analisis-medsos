import sys
import io
import os
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrapers.youtube_scraper import YouTubeScraper

scraper = YouTubeScraper()
more_videos = [
    {'id': 'FPpntVaAxVI', 'title': 'Ujian Anak Muda Dunia Susah Cari Kerja', 'channel': 'CNBC Indonesia'},
    {'id': 'fVccF9mKLLc', 'title': 'Badai PHK di Bulan Puasa', 'channel': 'METRO TV'},
    {'id': 'kAv-HwOAdSU', 'title': 'Gelombang PHK Menerjang Indonesia Ancaman Krisis', 'channel': 'KONTAN TV'},
    {'id': 'syz1LC83COk', 'title': 'Angka Pengangguran Naik Indonesia Hadapi Krisis', 'channel': 'CNBC Indonesia'}
]

df_existing = pd.read_csv('data/dataset_ketenagakerjaan_raw.csv')
print('Existing count:', len(df_existing))

new_comments = []
for v in more_videos:
    vid = v['id']
    url = f"https://www.youtube.com/watch?v={vid}"
    print(f"Scraping {v['channel']} - {v['title']} ({vid})...")
    try:
        cmts = scraper.get_comments(url, max_comments=100, replies_per_comment=5)
        print(f"  Got {len(cmts)} comments")
        for c in cmts:
            txt = (c.get('text') or '').strip()
            if txt and len(txt) > 5:
                new_comments.append({
                    'id': f"yt_{c.get('cid', len(new_comments))}",
                    'platform': 'YouTube',
                    'source_title': v['title'],
                    'author': c.get('author', 'Netizen'),
                    'text': txt,
                    'likes': c.get('votes', 0),
                    'timestamp': c.get('time', ''),
                    'url': url
                })
            for rep in c.get('replies', []):
                rtxt = (rep.get('text') or '').strip()
                if rtxt and len(rtxt) > 5:
                    new_comments.append({
                        'id': f"yt_{rep.get('cid', len(new_comments))}",
                        'platform': 'YouTube',
                        'source_title': f"Reply on {v['title'][:30]}",
                        'author': rep.get('author', 'Netizen'),
                        'text': rtxt,
                        'likes': rep.get('votes', 0),
                        'timestamp': rep.get('time', ''),
                        'url': url
                    })
    except Exception as e:
        print('  Error:', e)

df_new = pd.DataFrame(new_comments)
df_all = pd.concat([df_existing, df_new], ignore_index=True)
df_all.drop_duplicates(subset=['text'], inplace=True)
print(f"Total unique combined comments: {len(df_all)}")

df_all.to_csv('data/dataset_ketenagakerjaan_raw.csv', index=False, encoding='utf-8-sig')
df_all.to_excel('data/dataset_ketenagakerjaan_raw.xlsx', index=False)
print(f"Successfully saved dataset with {len(df_all)} rows to data/dataset_ketenagakerjaan_raw.csv and .xlsx")
