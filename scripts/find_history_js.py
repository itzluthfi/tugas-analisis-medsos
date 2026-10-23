with open('frontend/dist/index.html', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async function loadSavedHistory')
if pos == -1:
    pos = text.find('function loadSavedHistory')
print('loadSavedHistory pos:', pos)
if pos != -1:
    print(text[pos:pos+1500])
