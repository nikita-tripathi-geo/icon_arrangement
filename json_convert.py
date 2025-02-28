import json
import math
import csv

with open("converted_sortly-list.csv", "r", encoding="utf-8", newline="") as csvfile:
    # open file
    reader = csv.reader(csvfile)

    icons = []

    for row in reader:
        # print(row)
        icons.append({
                "id": int(row[0]),
                "name": row[1],
                "width": math.ceil(float(row[2])),
                "height": math.ceil(float(row[3])),
                "priority": 0,
            })

with open("icons.json", "w", encoding="utf-8") as file:
    json.dump(icons, file)
