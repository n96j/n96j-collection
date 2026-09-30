#!/usr/bin/env python3
"""Turns the raw .txt lists ("Name: URL" lines, "## Section" headings) into data/builds.js,
with friendly names ("Windows XP Professional SP3 — English"), language, kind, 32/64-bit merged.
Usage: python tools/txt_para_js.py tools/sources/*.txt"""
import sys, json, re, os
SEC = {"Windows 1.x / 2.x / 3.x":"Windows 3.x and older","Windows 95 / Chicago":"Windows 95","Windows 98 / Memphis":"Windows 98",
 "Windows ME / Millennium":"Windows ME","Windows NT (3.x / 4.0 / Cairo)":"Windows NT","Windows 2000":"Windows 2000",
 "Windows Neptune / Odyssey":"Windows 2000","Windows XP / Whistler":"Windows XP","Windows Longhorn / Vista":"Windows Vista",
 "Windows 7":"Windows 7","Windows 8 / 8.1":"Windows 8 / 8.1","Windows 10":"Windows 10","Windows 11":"Windows 11","Windows Server (2003+)":"Windows Server","Outros SO (CE, Embedded, Thin PC, Fundamentals...)":"Other (CE, Thin PC...)"}
ORDER = list(dict.fromkeys(SEC.values()))
L = {"Portuguese (Brazil)":r"pt-?br|pt br|brazil|brasileiro","Portuguese":r"portugu[eê]s|portuguese|\bptg\b|\bptpt\b|pt-pt",
 "Spanish":r"espa[nñ]ol|spanish|actualizaci[oó]n|ayuda para","French":r"fran[cç]ais|french|professionnel","German":r"german|deutsch",
 "Italian":r"italian|\bita\b","Dutch":r"dutch|nederlands|\bnl\b|\bnld\b","Polish":r"polish|\bpl\b","Czech":r"czech|\bcz\b|\bcze\b",
 "Greek":r"greek","Danish":r"danish","Swedish":r"swedish","Hungarian":r"hungarian","Hebrew":r"hebrew","Russian":r"russian",
 "Vietnamese":r"b\u1ea3n","Korean":r"korean","Japanese":r"japanese|\bjpn\b|pc-?98","Chinese":r"chinese|\bchs\b|\bcht\b|taiwan",
 "Arabic":r"arabic","Bulgarian":r"bulgarian","Croatian":r"croatian","Estonian":r"estonian","Finnish":r"finnish","Latvian":r"latvian",
 "Lithuanian":r"lithuanian","Norwegian":r"norwegian","Slovak":r"slovak","Turkish":r"turkish","Slovenian":r"slovenian","Serbian (Latin)":r"serbian","Thai":r"\bthai\b","Ukrainian":r"ukrainian","Romanian":r"romanian|romana","English":r"english|en-us|\beng\b"}
CODES = {"ara":"Arabic","bul":"Bulgarian","cze":"Czech","dan":"Danish","deu":"German","engintl":"English (International)","esmx":"Spanish (Mexico)","esp":"Spanish","est":"Estonian",
 "fin":"Finnish","fra":"French","frca":"French (Canada)","gre":"Greek","heb":"Hebrew","hrv":"Croatian","hun":"Hungarian","ita":"Italian","jpn":"Japanese",
 "kor":"Korean","lav":"Latvian","lit":"Lithuanian","nld":"Dutch","nor":"Norwegian","pol":"Polish","ptbr":"Portuguese (Brazil)","ptpt":"Portuguese",
 "rom":"Romanian","rus":"Russian","slk":"Slovak","swe":"Swedish","slv":"Slovenian","srlat":"Serbian (Latin)","tha":"Thai","ukr":"Ukrainian","tur":"Turkish","zhcn":"Chinese (Simplified)","zhhk":"Chinese (Hong Kong)","zhtw":"Chinese (Traditional)","eng":"English",
 "esp":"Spanish","kor-k":"Korean (K)","kor-kn":"Korean (KN)"}
MULTI = r"multi-?language|multiple languages|all languages|\bmui\b|\b\d+ languages|international|pan european|intl"
STRIP = r"\b(english|en-us|eng|engintl|german|deu|japanese|jpn|korean|kor-kn|kor-k|kor|chinese|spanish|esp|esmx|french|frca|fra|italian|ita|dutch|nld|polish|pol|czech|cze|greek|gre|danish|dan|swedish|swe|hungarian|hun|hebrew|heb|russian|rus|portuguese|brazilian|brazil|ptbr|ptpt|pt-br|arabic|ara|slovenian|slv|serbian|srlat|thai|tha|ukrainian|ukr|romana|ia64|arm64|bulgarian|bul|croatian|hrv|estonian|est|finnish|fin|latvian|lav|lithuanian|lit|norwegian|nor|romanian|rom|slovak|slk|turkish|tur|zhcn|zhhk|zhtw)\b"
def lang(n, u):
    l = n.lower(); coded = re.match(r"^(xp|w\d|w2000|srv\d|fundamentals|thinpc|wce|nt|vista|longhorn|neptune|wxp|memphis|chicago)", l)
    if re.search(MULTI, l): return "Multilingual"
    hits = [k for k, rx in L.items() if re.search(rx, l)]
    if coded:
        for t in re.split(r"[\s_]+", l):
            if t in CODES and CODES[t] not in hits: hits.append(CODES[t])
    if "Portuguese (Brazil)" in hits and "Portuguese" in hits: hits.remove("Portuguese")
    if "English" in hits and len(hits) > 1 and coded: hits.remove("English")
    if len(hits) > 1: return "Multilingual"
    if hits: return hits[0]
    uu = u.lower().rstrip("/")
    for k, rx in [("German", r"[-_]de$|de-de"), ("Spanish", r"_es$"), ("Korean", r"[-_]ko$"), ("Japanese", r"ja-jp|-jpn"), ("Portuguese (Brazil)", r"ptbr|pt-br")]:
        if re.search(rx, uu): return k
    return "English"
def arch(n):
    l = n.lower()
    if "arm64" in l: return "ARM64"
    a = bool(re.search(r"x64|64[- ]?bit|64 bits|amd64|x-64", l)); b = bool(re.search(r"x86\b|x32|32[- ]?bit|32 bits|x/32|\bi386", l))
    return "32 & 64-bit" if a and b else "64-bit" if a else "32-bit" if b else ""
TOK = [(r"^w11\b", "Windows 11"), (r"^srv(\d{4})r2\b", r"Windows Server \1 R2"), (r"^srv(\d{4})\b", r"Windows Server \1"), (r"^fundamentals legacy pcs", "Windows Fundamentals for Legacy PCs"), (r"^thinpc", "Windows Thin PC"), (r"^wce 1-5", "Windows CE 1 to 5"), (r"\bltsc\b", "LTSC"), (r"\biot\b", "IoT"), (r"\beval\b", "Evaluation"), (r"\bstd\b", "Standard"), (r"\bcd(\d)\b", r"CD \1"), (r"\b(\d\d)h(\d)\b", lambda m: m.group(0).upper()), (r"^w(95|98)([abc]?)\b", r"Windows \1\2"), (r"^w2000\b", "Windows 2000"), (r"^srv2000\b", "Windows 2000 Server"), (r"^nt\b", "Windows NT"), (r"^chicago\b", "Windows Chicago (95)"), (r"^memphis\b", "Windows Memphis (98)"), (r"\bse\b", "Second Edition"), (r"\bfe\b", "First Edition"), (r"\bosr(\d)", r"OSR\1"), (r"\badv\b", "Advanced"), (r"\bsrv\b", "Server"), (r"\bwks\b", "Workstation"), (r"\boem\b", "OEM"), (r"^w3\.(\d\w?)\b", r"Windows 3.\1"), (r"^wxp/whistler\b", "Windows XP Whistler build"), (r"^wxp longhorn build", "Windows Longhorn (XP-based) build"),
 (r"^w8\.1\b", "Windows 8.1"), (r"^w8\b", "Windows 8"), (r"^w7\b", "Windows 7"), (r"^w10\b", "Windows 10"), (r"^xp\b", "Windows XP"),
 (r"^vista\b", "Windows Vista"), (r"^longhorn\b", "Windows Longhorn build"), (r"^neptune\b", "Windows Neptune build"),
 (r"\bmce2005\b", "Media Center Edition 2005"), (r"\bpro\b", "Professional"), (r"\bent\b", "Enterprise"), (r"\bult\b", "Ultimate"),
 (r"\bhomebasic\b", "Home Basic"), (r"\bhomeprem\b", "Home Premium"), (r"\btodas-edicoes\b", "All editions"), (r"\bsp(\d)\b", r"SP\1"),
 (r"\bu1\b", "Update 1"), (r"\brtm\b", "RTM"), (r"\btp\b", "Technical Preview"), (r"\bdevpreview\b", "Developer Preview"),
 (r"\bmais recente\b", "Latest"), (r"\batualizado-(\d+)", r"Updated to \1"), (r"\bpeixe\b", "Peixe edition (mod)"), (r"\bmulti\b", "Multi-language"),
 (r"\bn\b(?= *(ptpt|$))", "N"), (r"\bstarter\b", "Starter"), (r"\bembedded industry\b", "Embedded Industry"), (r"\bori?ginal-style iso\b", "(original ISO)")]
def clean(n, v):
    s = n
    if re.match(r"^(xp|w\d|w2000|srv\d|fundamentals|thinpc|wce|nt|vista|longhorn|neptune|wxp|memphis|chicago)", s) :
        for rx, rep in TOK: s = re.sub(rx, rep, s, flags=re.I)
    s = re.sub(r"^(MSDN - (BETA - )?Disc \d+ - |Microsoft TechNet( EN)?:? \d+ - )", "", s); s = re.sub(r"\s*\(Microsoft\)", "", s); s = re.sub(r"Microsoft (?=Windows)", "", s); s = re.sub(r"\blonghorn\b", "Longhorn", s); s = re.sub(r"\bwXP\b", "Windows XP", s); s = s.replace("''", " ")
    s = re.sub(r"\s*[\.\-]?\s*7z$", "", s); s = re.sub(r"\(?X\d\d[- ]\d{5}\)?", "", s); s = re.sub(r"\b(\d\d) H (\d)\b", r"\1H\2", s); s = re.sub(r"~[^~]*~", "", s); s = re.sub(r"\bX 64\b|\bEn US\b", "", s, flags=re.I); s = re.sub(r"\(([^)]*)$", r"\1", s); s = re.sub(r"\.iso$", "", s, flags=re.I)
    s = re.sub(r"\s*[\[\(]?\s*Windows Vintage Series - team derekab\s*[\]\)]?", "", s)
    s = re.sub(r"\b(x86/x64|x64/x86|x86,x64,IA64|x86|x64|x32|x32/x64|x-?64|x-?86)\b", "", s, flags=re.I)
    s = re.sub(r"\b(\d\d)[- ]?bits?\b", "", s, flags=re.I)
    s = re.sub(STRIP, "", s, flags=re.I)
    s = re.sub(r"[\(\[]\s*[,/&\-–]+\s*", "(", s); s = re.sub(r"\s*[,/&\-–]+\s*[\)\]]", ")", s)
    for _ in range(3): s = re.sub(r"[\(\[][\s,/&\-–:]*[\)\]]", "", s)
    s = re.sub(r"\(\s+", "(", s); s = re.sub(r"\s+\)", ")", s); s = re.sub(r"\s+", " ", s).strip(" -–:,/")
    if s == s.lower(): s = s.title().replace("Sp", "SP")
    if "windows" not in s.lower() and not re.search(r"vista|longhorn|neptune", s.lower()): s = v + " – " + s
    return s
MOD = r"pre-?activated|preactivated|pr[eé] ativado|non tpm|no tpm|n[aã]o compat|debloat|retrophase|vienna|ninjutsu|gamer|10 to 7|win10to7|longhorn 19045|activated|\blite\b|lite\+\+|\bmod\b|carlos|virgilio|aero blue|skinpack|transformed|based win|xeondj|universal|kids|integral|nlite|peixe|hillel|super lite|kodiak"
BETA = r"insider|canary|dev channel|beta|preview|\brc ?\d|\btp\b|\bctp\b|milestone|whistler|longhorn|neptune|odyssey|chicago|memphis|georgia|cairo|checked|debug|pre-?release|technical|\bsdk\b|\bwdk\b|codename|leak|delta|debomb|\bbulid\b"
def kind(o, t):
    l = (o + " " + t).lower()
    if re.search(MOD, l): return "Modded / Lite (unofficial)"
    if re.search(BETA, l) and not re.search(r"\brtm\b(?!.*leak)", l) or re.search(r"build \d{4}|\bb[123]\b|\bm\d\b", l) and not re.search(r"\brtm\b|\bsp\d\b|service pack", l): return "Beta / Pre-release"
    return "Official release"
EXTRA_K = "Extras (Service Packs, DDK, symbols)"; REVIEW_K = "Unverified (check before using)"
KO = {"Official release": 0, "Beta / Pre-release": 1, "Modded / Lite (unofficial)": 2, EXTRA_K: 3, REVIEW_K: 4}
FORCE = {"02_": EXTRA_K, "03_": REVIEW_K}  # file-name prefix -> kind
raw, seen, sec, forced = [], set(), "Other", {}
for f in sys.argv[1:]:
    fk = FORCE.get(os.path.basename(f)[:3])
    for ln in open(f, encoding="utf-8"):
        ln = ln.strip()
        if ln.startswith("## "): sec = ln[3:].strip(); continue
        m = re.match(r"^(.*?):\s*(https?://\S+)$", ln)
        if not m or ln.startswith("#") or "jstor" in m.group(2) or m.group(2) in seen: continue
        seen.add(m.group(2)); raw.append((m.group(1).strip(), m.group(2), SEC.get(sec, sec))); forced[m.group(2)] = fk
groups = {}
for n, u, v in raw:
    p = u.rstrip("/").split("/"); e = re.search(r"\.(iso|rar|zip|7z|vhd|vmdk|img|exe|ova)$", p[-1].lower())
    fmt = e.group(1).upper() if e and len(p) >= 6 else "FOLDER"
    href = u.replace("/download/", "/details/") if fmt == "FOLDER" and "/download/" in u else u
    a, lg = arch(n), lang(n, u); k = forced.get(u); t = n if k else clean(n, v); k = k or kind(n, t)
    groups.setdefault((v, k, t, lg), []).append([a, href, fmt, n])
items = []
for (v, k, t, lg), ds in groups.items():
    arches = [d[0] for d in ds]
    parts = [ds] if len(set(arches)) == len(arches) else [[d] for d in ds]
    for ps in parts:
        one = len(ps) == 1
        title = f"{t} — {lg}" + (f", {ps[0][0]}" if one and ps[0][0] else "")
        items.append({"t": title, "v": v, "k": k, "l": lg, "o": ps[0][3], "d": [[d[0], d[1], d[2]] for d in sorted(ps, key=lambda d: d[0])]})
def bn(s):
    h = re.search(r"\b(\d\d)H([12])\b", s)
    if h: return int(h[1]) * 100 + (4 if h[2] == "1" else 10)
    return int((re.search(r"\b(\d{4,5})\b", s) or [0, 0])[1])
# extras/unverified keep their original names; disambiguate identical titles with the archive.org id
from collections import Counter
_c = Counter(i["t"] for i in items if i["k"] in (EXTRA_K, REVIEW_K))
for i in items:
    if i["k"] in (EXTRA_K, REVIEW_K) and _c[i["t"]] > 1:
        i["t"] += " [" + i["d"][0][1].rstrip("/").split("/")[-1] + "]"
items.sort(key=lambda i: (ORDER.index(i["v"]) if i["v"] in ORDER else 99, KO[i["k"]], bn(i["t"]), i["t"].lower()))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "builds.js")
with open(out, "w", encoding="utf-8") as fh:
    fh.write("window.ORDER=" + json.dumps(ORDER) + ";\nwindow.BUILDS=" + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(len(raw), "links ->", len(items), "entries")
