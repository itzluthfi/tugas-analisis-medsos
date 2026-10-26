import requests
import json
import re

with open('config/instagram_cookies.json', 'r', encoding='utf-8') as f:
    cookies = json.load(f)

cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Cookie': cookie_str,
}

r = requests.get('https://www.instagram.com/explore/tags/solarlangka/', headers=headers)
print("Status:", r.status_code, "Len:", len(r.text))

# Search for shortcodes
m = re.findall(r'"code":"([^"]+)"', r.text)
print("Codes found:", len(m), m[:10])

# Search for shortcode in JSON blobs
m_sc = re.findall(r'"shortcode":"([^"]+)"', r.text)
print("Shortcodes found:", len(m_sc), m_sc[:10])

# Search for media PK
m_pk = re.findall(r'"pk":"?(\d+)"?', r.text)
print("PKs found:", len(m_pk), m_pk[:10])

# Search for caption texts
m_cap = re.findall(r'"text":"([^"]{20,100})"', r.text)
print("Captions found:", len(m_cap))
for c in m_cap[:3]:
    print(" -", c)
