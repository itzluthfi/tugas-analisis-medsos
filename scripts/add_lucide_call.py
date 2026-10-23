with open('frontend/dist/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pattern = r"(\}\)\.join\(''\);)(\s*\}\s*catch\s*\(e\)\s*\{\s*tbody\.innerHTML\s*=\s*`<tr><td colspan=\"8\")"

match = re.search(pattern, text)
if match:
    replacement = match.group(1) + "\n        lucide.createIcons();" + match.group(2)
    text = text[:match.start()] + replacement + text[match.end():]
    print("Added lucide.createIcons() to loadSentimentDataset successfully!")
else:
    print("Pattern not matched.")

with open('frontend/dist/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
