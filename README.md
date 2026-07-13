# 統測登記分發落點儀表板(15 外語群英語類)

輸入統測五科原始分數,自動用每個校系「該年度官方倍率」計算加權總分,
與 112–114 學年度最低錄取分數比較,判斷落點。

🌐 **線上版**:<https://berton0310.github.io/scoreflow-dashboard/>
(push 到 `main` 分支後由 GitHub Actions 自動部署)

## 使用方式

直接雙擊開啟 `index.html` 即可(資料已內嵌,免網路、免伺服器)。
分數會自動存在瀏覽器 localStorage。

## 資料來源(皆為官方)

| 檔案 | 內容 | 來源 |
|---|---|---|
| `data/112~114_up01.pdf` | 各校系錄取總成績統計表(倍率+最低錄取分) | 技專校院招生委員會聯合會 jctv.ntut.edu.tw |
| `data/115quota.xlsx` | 115 學年度志願代碼、名額、五科權重 | 115 聯合登記分發委員會 |
| `data/115_tech.pdf` | 115 學年度招生簡章全文 | 同上 |

## 重建流程

```
cd data
python extract.py      # PDF -> english_group.json (112-114 歷年資料)
python merge.py        # + 115quota.xlsx -> dashboard_data.json
cd ..
python build.py        # 注入 template.html -> index.html
```

(此機器請用 `C:\Users\berto\AppData\Local\Programs\Python\Python312\python.exe`,
需要 `pdfplumber`、`openpyxl`)

## 志願模擬排序

- 在表格點 ☆ 星號把想要的校系加入「我的志願模擬排序」面板
- 面板內可拖曳或用 ↑↓ 調整順序、✕ 移除、全部清除
- 選擇基準年(112/113/114)後,系統依分發規則(由第 1 志願往下、錄取第一個達標者)
  標出 🎯 預估落點
- 清單與順序自動存在瀏覽器 localStorage

## 判定標準

- 🟢 穩上:三年最低分皆超過,且對最近年度有 ≥3% 滿分的緩衝
- 🔵 有機會:超過最近年度最低分
- 🟡 邊緣:與最近年度最低分差距在 ±3% 內
- 🔴 困難:低於近年最低分
- ⚪ 無歷年資料:115 新設/更名系科,或歷年無錄取分數

## 注意

- 每年統測難度、名額、報名人數都不同,歷年分數僅供參考。
- 「未足額」= 該年錄取人數 < 名額(通常有登記就上),最低分參考價值低。
- 115 實際招生名額 115.7.27 公告,請以官方簡章為準。
