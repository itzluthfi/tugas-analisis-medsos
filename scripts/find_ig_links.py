import urllib.request
import urllib.parse
import json
import re
from bs4 import BeautifulSoup
import yt_dlp

def find_instagram_links():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    queries = [
        'site:instagram.com/reel/ "solar" "antre" "spbu"',
        'site:instagram.com/p/ "solar langka" "pekanbaru" OR "bali" OR "medan"',
        'site:instagram.com/reel/ "kelangkaan bbm" OR "bbm langka"',
        'site:instagram.com/reel/ "pertalite langka" OR "antrean spbu"',
        'site:instagram.com/reel/ "bahlil" "bbm" "subsidi"'
    ]
    
    found_urls = set()
    for q in queries:
        try:
            url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req, timeout=8)
            soup = BeautifulSoup(resp.read().decode('utf-8', errors='ignore'), 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                m = re.search(r'uddg=([^&]+)', href)
                if m:
                    target = urllib.parse.unquote(m.group(1))
                    m_ig = re.search(r'(https://www\.instagram\.com/(?:reel|p)/[A-Za-z0-9_-]+/)', target)
                    if m_ig:
                        found_urls.add(m_ig.group(1))
        except Exception as e:
            print(f"Error querying '{q}': {e}")
            
    print(f"Total unique Instagram URLs found: {len(found_urls)}")
    for u in sorted(found_urls):
        print("  *", u)
    return list(found_urls)

if __name__ == "__main__":
    links = find_instagram_links()
