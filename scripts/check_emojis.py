import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('frontend/dist/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Broad emoji regex
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]')

lines = text.splitlines()
found_emojis = []
for i, line in enumerate(lines):
    matches = emoji_pattern.findall(line)
    if matches:
        found_emojis.append((i+1, matches, line.strip()))

print(f"Total lines with emojis: {len(found_emojis)}")
for lnum, ems, preview in found_emojis:
    print(f"Line {lnum}: {ems} -> {preview[:100]}")
