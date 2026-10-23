with open('frontend/dist/index.html', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'<div id="[^"]*"', html)
for m in matches:
    if 'container' in m or 'view' in m or 'section' in m:
        print(m)
