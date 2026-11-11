"""Turn **bold** markers into Telegram bold entities (UTF-16 offsets).
Usage: python3 tg_bold.py <text-file>  -> prints JSON {"text":..., "entities":[...]}"""
import json, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
out, ents, pos = "", [], 0
u16 = lambda s: len(s.encode("utf-16-le")) // 2
for m in re.finditer(r"\*\*(.+?)\*\*", src, re.S):
    out += src[pos:m.start()]
    ents.append({"type": "bold", "offset": u16(out), "length": u16(m.group(1))})
    out += m.group(1)
    pos = m.end()
out += src[pos:]
print(json.dumps({"text": out, "entities": ents}, ensure_ascii=False))
