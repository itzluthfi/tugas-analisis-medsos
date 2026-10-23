with open('frontend/dist/index.html', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="main-sidebar"')
print('Sidebar pos:', pos)
if pos != -1:
    print(text[pos:pos+2000])
