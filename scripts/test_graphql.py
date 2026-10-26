import requests
import json

with open('config/instagram_cookies.json', 'r', encoding='utf-8') as f:
    cookies = json.load(f)

cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Cookie': cookie_str,
    'x-ig-app-id': '936619743392459',
    'x-csrftoken': cookies.get('csrftoken', ''),
    'x-asbd-id': '129477',
    'x-requested-with': 'XMLHttpRequest',
    'Referer': 'https://www.instagram.com/reel/DVlqOj_ksgC/',
    'content-type': 'application/x-www-form-urlencoded'
}

doc_ids = ['27234427476213202', '17888487470205420', '8845758582119845']

for doc_id in doc_ids:
    print(f"\n--- Testing doc_id: {doc_id} ---")
    data = {
        'variables': json.dumps({'shortcode': 'DVlqOj_ksgC', 'first': 50}),
        'doc_id': doc_id
    }
    try:
        res = requests.post('https://www.instagram.com/graphql/query', headers=headers, data=data, timeout=10)
        print("Status:", res.status_code)
        if res.status_code == 200:
            rj = res.json()
            print("Full rj:", json.dumps(rj)[:500])
            if 'data' in rj and rj['data'] is not None:
                data_obj = rj['data']
                media = data_obj.get('xdt_shortcode_media') or data_obj.get('shortcode_media') or {}
                parent = media.get('edge_media_to_parent_comment') or {}
                edges = parent.get('edges', [])
                print(f"Retrieved {len(edges)} comments!")
                for e in edges[:5]:
                    node = e.get('node', {})
                    user = node.get('owner', {}).get('username', 'user')
                    txt = node.get('text', '').replace('\n', ' ')
                    print(f"  @{user}: {txt[:70]}")
                break
            else:
                print("No data field:", res.text[:200])
        else:
            print("Failed:", res.text[:200])
    except Exception as ex:
        print("Error:", ex)
