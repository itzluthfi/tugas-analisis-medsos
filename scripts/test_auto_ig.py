import requests
import json
import urllib.parse
import re

with open('config/instagram_cookies.json', 'r', encoding='utf-8') as f:
    cookies = json.load(f)

cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Cookie': cookie_str,
    'x-ig-app-id': '936619743392459',
    'x-csrftoken': cookies.get('csrftoken', ''),
    'x-requested-with': 'XMLHttpRequest',
    'Referer': 'https://www.instagram.com/'
}

# 1. Test topsearch endpoint
queries = ['solarlangka', 'kelangkaanbbm', 'antreanspbu', 'bbmlangka']
for q in queries:
    url = f"https://www.instagram.com/api/v1/fbsearch/topsearch/?context=blended&query={urllib.parse.quote(q)}"
    try:
        r = requests.get(url, headers=headers, timeout=8)
        print(f"Query '{q}': status {r.status_code}")
        if r.status_code == 200:
            rj = r.json()
            hashtags = [h.get('hashtag', {}).get('name') for h in rj.get('hashtags', [])]
            print(f"  Hashtags found: {hashtags}")
            places = [p.get('place', {}).get('title') for p in rj.get('places', [])]
            print(f"  Places: {places[:3]}")
    except Exception as e:
        print(f"Error {q}: {e}")

# 2. Test hashtag sections
for tag in ['solarlangka', 'antreanbbm', 'bbmlangka']:
    url = f"https://www.instagram.com/api/v1/tags/web_info/?tag_name={tag}"
    try:
        r = requests.get(url, headers=headers, timeout=8)
        print(f"Tag info '{tag}': status {r.status_code}")
        if r.status_code == 200:
            rj = r.json()
            count = rj.get('data', {}).get('media_count', 0)
            print(f"  Media count for #{tag}: {count}")
    except Exception as e:
        print(f"Error tag {tag}: {e}")
