import pdfplumber
import json
import pandas as pd

# путь к PDF-файлу
pdf_path = "patents_data.pdf"  
patents_data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if not table:
            continue

        for row in table[1:]:  
            if len(row) < 13:  
                continue

            status = row[5]
            publ = row[7]
            title = row[4]

            # Исключаем "не публ." и "экспертиза п/с"
            if status and "не публ." in status.strip().lower():
                continue
            if publ and "экспертиза п/с" in publ.strip().lower():
                continue

            # Сохраняем только если есть название и статус
            if title and status:
                entry = {
                    "дата": row[3].strip() if row[3] else "", 
                    "название": row[4].strip() if row[4] else "",  
                    "статус документа": row[5].strip() if row[5] else "",  
                    "авторы": []  
                }

                for i in range(8, 19):
                    if i < len(row) and row[i] and row[i].strip():
                        entry["авторы"].append(row[i].strip())

                patents_data.append(entry)


json_path = "parsed_data.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(patents_data, f, ensure_ascii=False, indent=2)

# csv_data = []
# for entry in patents_data:
#     csv_entry = entry.copy()
#     csv_entry["авторы"] = ", ".join(entry["авторы"]) if isinstance(entry["авторы"], list) else entry["авторы"]
#     csv_data.append(csv_entry)

# df = pd.DataFrame(csv_data)
# csv_path = "parsed_data.csv"
# df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';')

print(f"   - JSON: {json_path} ({len(patents_data)} записей)")
#print(f"   - CSV: {csv_path} ({len(patents_data)} записей)")

