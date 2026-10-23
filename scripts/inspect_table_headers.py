with open('frontend/dist/index.html', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="ds-filter-sentiment"')
if pos != -1:
    print(text[pos:pos+2500])
