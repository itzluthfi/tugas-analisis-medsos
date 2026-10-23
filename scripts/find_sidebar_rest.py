with open('frontend/dist/index.html', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="main-sidebar"')
print(text[pos+1000:pos+3500])
