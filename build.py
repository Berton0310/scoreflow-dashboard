import json

data = json.load(open('data/dashboard_data.json', encoding='utf-8'))
tpl = open('template.html', encoding='utf-8').read()
html = tpl.replace('/*__DATA__*/', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
open('index.html', 'w', encoding='utf-8').write(html)
print('index.html built,', len(data), 'depts')
