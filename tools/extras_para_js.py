#!/usr/bin/env python3
"""Turns the "not Windows builds" lists (Name: URL lines, ## Section headings) into data/extras.js
for programs.html. Usage: python tools/extras_para_js.py tools/sources_extras/*.txt"""
import sys, re, os, json, datetime
CAT = {"Steam BETA (arquivos de cliente p/ Win 7/8)": "Steam beta clients (Windows 7/8)",
       "MSDN / TechNet / documentos / conferências": "MSDN, TechNet and conference discs",
       "Livros, cursos e treinamento": "Books, courses and training",
       "Drivers, utilitários e mídias de fabricantes": "Drivers, utilities and vendor discs",
       "Softwares, jogos e outros (não são build de Windows)": "Software, games and other"}
ORDER = list(CAT.values()) + ["Videos, media and off-topic"]
# items that clearly have nothing to do with downloading Windows stuff: their own category
OFF = r"tiffany|shop windows|frank lloyd wright|illinois world labor|jerry joseph|thripsid|citro[eë]n|pipo's story|chinese phone crash|happy birthday to windows|virus warning|trying to get windows|can you install|will windows 2000 run|windows 2000 cyn|default beep|trap beat|demo videos|raw footage|frankenstein retro pc|deus ex|pubblicit|title\.wma|shanghai solitaire|windows longhorn 4029 in power point|what's new in windows xp/whistler|windows 2000 powered"
MON = {m: i + 1 for i, m in enumerate("january february march april may june july august september october november december".split())}
def steam_key(t):
    m = re.search(r"(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d+)\w*,?\s+(\d{4})", t, re.I)
    return datetime.date(int(m[3]), MON[m[1].lower()], int(m[2])) if m else datetime.date(1970, 1, 1)
items, seen, sec = [], set(), None
for f in sys.argv[1:]:
    for ln in open(f, encoding="utf-8"):
        ln = ln.strip()
        if ln.startswith("## "): sec = ln[3:].strip(); continue
        m = re.match(r"^(.*?):\s*(https?://\S+)$", ln)
        if not m or ln.startswith("#") or m[2] in seen: continue
        seen.add(m[2]); t, u = m[1].strip(), m[2]
        c = CAT.get(sec, sec)
        if c == CAT["Softwares, jogos e outros (não são build de Windows)"] and re.search(OFF, t.lower()): c = ORDER[-1]
        last = u.rstrip("/").split("/")[-1]
        folder = not re.search(r"\.(iso|rar|zip|7z|vhd|vmdk|img|exe|ova)$", last.lower()) or u.count("/") < 5
        href = u.replace("/download/", "/details/") if folder and "/download/" in u else u
        items.append({"t": t, "c": c, "u": href, "f": "FOLDER" if folder else last.rsplit(".", 1)[-1].upper()})
rank = {c: i for i, c in enumerate(ORDER)}
items.sort(key=lambda i: (rank.get(i["c"], 99), steam_key(i["t"]) if i["c"] == ORDER[0] else 0, i["t"].lower()))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "extras.js")
with open(out, "w", encoding="utf-8") as fh:
    fh.write("window.XORDER=" + json.dumps(ORDER) + ";\nwindow.EXTRAS=" + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";\n")
from collections import Counter
print(len(items), "items", dict(Counter(i["c"] for i in items)))
