import json, openpyxl, sys

# --- 115 current-year data from official Excel ---
wb = openpyxl.load_workbook('115quota.xlsx', read_only=True)
ws = wb['聯登校系資料']
rows115 = []
for r in ws.iter_rows(min_row=2, values_only=True):
    if r[2] and '15外語群英語類' in str(r[2]):
        rows115.append({
            'code': str(r[3]),
            'school': str(r[1]).strip(),
            'dept': str(r[5]).strip(),
            'quota': r[6],
            'weights': {
                'chinese': float(r[13]), 'english': float(r[14]),
                'math': float(r[15]), 'pro1': float(r[16]), 'pro2': float(r[17]),
            },
        })
print(f'115: {len(rows115)} english-group depts', file=sys.stderr)

# --- historical data ---
hist = json.load(open('english_group.json', encoding='utf-8'))

def key(school, dept):
    return school.strip() + '|' + dept.strip().replace('（', '(').replace('）', ')')

hist_by_key = {}
for h in hist:
    hist_by_key.setdefault(key(h['school'], h['dept']), {})[h['year']] = h

merged = []
matched_hist_keys = set()
for d in rows115:
    k = key(d['school'], d['dept'])
    hy = hist_by_key.get(k, {})
    if hy:
        matched_hist_keys.add(k)
    history = {}
    for y in (112, 113, 114):
        h = hy.get(y)
        if h:
            history[str(y)] = {
                'weights': h['weights'], 'quota': h['quota'],
                'admitted': h['admitted'], 'cutoff': h['cutoff'],
                'tiebreak': h['tiebreak'],
            }
    merged.append({**d, 'history': history})

no_hist = [d for d in merged if not d['history']]
print(f'depts with no history match: {len(no_hist)}', file=sys.stderr)
for d in no_hist:
    print('  NO-HIST:', d['school'], d['dept'], file=sys.stderr)

with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=1)
print('saved dashboard_data.json:', len(merged), 'depts', file=sys.stderr)
