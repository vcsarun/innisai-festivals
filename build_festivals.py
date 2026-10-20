#!/usr/bin/env python3
"""Builds festivals.json for the Innisai app from the open-source `holidays` package (no API key).

Run:  pip install -U holidays && python build_festivals.py
The GitHub Action in .github/workflows/update.yml does this every month.
"""
import datetime
import json
import sys

import holidays

TODAY = datetime.date.today()
YEARS = range(TODAY.year, TODAY.year + 4)  # this year + 3 more

# scope: "IN" = shown to users in India, "ALL" = shown everywhere
HARVEST_JAN_NAMES = {
    "default": "Happy Harvest Festival",
    "pongal": "Happy Pongal",
    "sankranti": "Happy Sankranti",
    "bihu": "Happy Magh Bihu",
}
HARVEST_APR_NAMES = {
    "default": "Happy Harvest Festival",
    "pongal": "Happy Puthandu",
    "bihu": "Happy Bohag Bihu",
    "baisakhi": "Happy Baisakhi",
}


def entry(fid, anim, date, scope, names, approx=False):
    return {
        "id": fid, "anim": anim, "date": date.isoformat(), "scope": scope,
        "names": names, "grace": 1 if approx else 0,
    }


def main():
    out = []
    for y in YEARS:
        h = holidays.India(years=y, categories=("public", "optional"))
        by_name = {}
        for d, n in h.items():
            for part in n.split("; "):
                by_name.setdefault(part.strip(), []).append(d)

        def first(pred):
            for name, ds in sorted(by_name.items(), key=lambda kv: kv[1][0]):
                if pred(name):
                    return name, ds[0]
            return None, None

        out.append(entry(f"newyear-{y}", "newyear", datetime.date(y, 1, 1), "ALL", {"default": "Happy New Year"}))
        out.append(entry(f"christmas-{y}", "christmas", datetime.date(y, 12, 25), "ALL", {"default": "Merry Christmas"}))

        _, d = first(lambda n: n == "Makar Sankranti")
        if d: out.append(entry(f"harvest-jan-{y}", "harvest", d, "IN", HARVEST_JAN_NAMES))
        _, d = first(lambda n: n.startswith("Meshadi") or n == "Vaisakhi")
        if d: out.append(entry(f"harvest-apr-{y}", "harvest", d, "IN", HARVEST_APR_NAMES))
        _, d = first(lambda n: n == "Holi")
        if d: out.append(entry(f"holi-{y}", "holi", d, "IN", {"default": "Happy Holi"}))
        _, d = first(lambda n: n.startswith("Ganesh Chaturthi"))
        if d: out.append(entry(f"ganesh-{y}", "ganesh", d, "IN", {"default": "Happy Vinayaka Chathurthi"}))
        n, d = first(lambda n: n.startswith("Id-ul-Fitr"))
        if d: out.append(entry(f"eid-{y}", "eid", d, "ALL", {"default": "Eid Mubarak"}, approx="estimated" in n))
        _, d = first(lambda n: n == "Good Friday")
        if d: out.append(entry(f"goodfriday-{y}", "goodfriday", d, "ALL", {"default": "Good Friday"}))
        _, d = first(lambda n: n == "Dussehra")
        if d: out.append(entry(f"dussehra-{y}", "navratri", d, "IN", {"default": "Happy Navarathiri \u00b7 Dussehra"}))
        _, d = first(lambda n: n.startswith("Diwali"))
        if d: out.append(entry(f"diwali-{y}", "diwali", d, "IN", {"default": "Happy Diwali"}))

    out.sort(key=lambda e: e["date"])
    doc = {"v": 1, "generated": TODAY.isoformat(), "festivals": out}
    with open("festivals.json", "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(out)} festivals", file=sys.stderr)


if __name__ == "__main__":
    main()
