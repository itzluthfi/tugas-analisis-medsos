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
    'Referer': 'https://www.instagram.com/'
}

params = {
    'query_hash': '97b41c52301f77ce508f55e66d17620e',
    'variables': json.dumps({'shortcode': 'DVlqOj_ksgC', 'first': 50})
}
r = requests.get('https://www.instagram.com/graphql/query/', headers=headers, params=params)
data = r.json()['data']['shortcode_media']
print("Caption:", (data.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', ''))[:50])

parent_comments = data.get('edge_media_to_parent_comment') or data.get('edge_media_to_comment')
if parent_comments:
    print('Total comments count:', parent_comments.get('count'))
    page_info = parent_comments.get('page_info', {})
    print('has_next_page:', page_info.get('has_next_page'))
    print('end_cursor:', page_info.get('end_cursor'))
    edges = parent_comments.get('edges', [])
    print(f'Fetched {len(edges)} comments in this page!')
    for e in edges[:5]:
        node = e['node']
        user = node.get('owner', {}).get('username', 'user')
        txt = node.get('text', '').replace('\n', ' ')
        print(f" - @{user}: {txt[:60]}")
