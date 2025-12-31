import csv
import json
from ..milsymbolpy import milsymbolpy as ms
import os
import re

SYMBOL_SIZE = 150
catalog = []

os.makedirs("output/symbols", exist_ok=True)


def gen_symbol(affiliation, id, echelon):
    affil_hr = "Friendly" if affiliation == "FR" else "Enemy"
    affil_code = "03" if affiliation == "FR" else "06"

    if len(id) == 12:
        sidc = f"13{affil_code}1000{echelon}{id}00000000"
    else:
        sidc = f"13{affil_code}1000{echelon}{id}00000000000000"

    print(sidc)

    if len(sidc) != 30:
        msg = f"Invalid SIDC: {sidc} (length is {len(sidc)})"
        raise ValueError(msg)

    s = ms.Symbol(sidc, {"size": SYMBOL_SIZE})
    desc = s.get_desc()
    desc = re.sub(r"\[..\] ", "", desc)
    png_fname = f"output/symbols/{sidc}.png"
    s.as_png(png_fname, training=True)

    catalog.append(
        {
            "id": sidc,
            "image": png_fname,
            "conversations": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {
                            "type": "text",
                            "text": "Identify the unit depicted in this MIL-STD-2525 symbol.",
                        },
                    ],
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{affil_hr} {desc}",
                        }
                    ],
                },
            ],
        }
    )


for affiliation in ["FR", "EN"]:
    with open("symbol_catalog.tsv", "r", newline="", encoding="utf-8") as tsvfile:
        # Set the delimiter to a tab character
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        next(tsvreader)  # skip header line

        for row in tsvreader:
            if row[1][-4:] == "0000":
                continue
            if row[2] == "x":
                (start, end) = row[3].split("-")
                for i in range(int(start), int(end) + 1):
                    gen_symbol(affiliation, row[1], f"1{i}")
            else:
                gen_symbol(affiliation, row[1], "00")

with open("output/train.json", "w", encoding="utf-8") as catalog_file:
    json.dump(catalog, catalog_file, indent=2, ensure_ascii=False)
