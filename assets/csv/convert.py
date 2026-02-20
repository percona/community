import csv
import json

input_file = "Percona-Community-Live-Talks.csv"
output_file = "talks.json"

rows = []

with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)

    for row in reader:
        item = {headers[i]: row[i] if i < len(row) else "" for i in range(len(headers))}
        rows.append(item)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump({"talks": rows}, f, indent=2, ensure_ascii=False)

print("Done")
