import pdfplumber, re, json, sys

def parse_weights(s):
    s = s.replace('\n', '')
    pats = {
        'chinese': r'國文\*([\d.]+)',
        'english': r'英文\*([\d.]+)',
        'math': r'數學\*([\d.]+)',
        'pro1': r'專業\(一\)\*([\d.]+)',
        'pro2': r'專業\(二\)\*([\d.]+)',
    }
    out = {}
    for k, p in pats.items():
        m = re.search(p, s)
        out[k] = float(m.group(1)) if m else None
    return out

def num(s):
    s = (s or '').replace('\n', '').strip()
    if s in ('--', ''):
        return None
    try:
        return float(s)
    except ValueError:
        return None

def extract(pdf_path, year):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ''
            if '外語群英語類' not in text:
                continue
            for table in page.extract_tables():
                for r in table:
                    if not r or not r[0]:
                        continue
                    group = r[0].replace('\n', '')
                    if '外語群英語類' not in group:
                        continue
                    school = (r[3] or '').replace('\n', '')
                    dept = (r[4] or '').replace('\n', '')
                    w = parse_weights(r[5] or '')
                    rows.append({
                        'year': year,
                        'code': (r[1] or '').replace('\n', ''),
                        'school': school,
                        'dept': dept,
                        'weights': w,
                        'quota': num(r[6]),
                        'admitted': num(r[7]),
                        'cutoff': num(r[8]),
                        'tiebreak': num(r[9]),
                    })
    return rows

all_rows = []
for y in (112, 113, 114):
    rows = extract(f'{y}_up01.pdf', y)
    print(f'{y}: {len(rows)} rows', file=sys.stderr)
    all_rows.extend(rows)

with open('english_group.json', 'w', encoding='utf-8') as f:
    json.dump(all_rows, f, ensure_ascii=False, indent=1)
print('saved english_group.json, total', len(all_rows), file=sys.stderr)
