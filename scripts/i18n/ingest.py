#!/usr/bin/env python3
"""Merge numbered translations into data/i18n/src/<lang>-core.json (keys are the English strings).
Usage: ingest.py LANG strings.json part1.txt part2.txt ...
Each part file has lines 'id|translation'; '=' keeps the English text as it is."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
lang, src, parts = sys.argv[1], Path(sys.argv[2]), sys.argv[3:]
S = json.loads(src.read_text(encoding="utf-8"))
out_p = ROOT / "data" / "i18n" / "src" / f"{lang}-core.json"
D = json.loads(out_p.read_text(encoding="utf-8")) if out_p.exists() else {}
n = 0
for f in parts:
    for line in Path(f).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        i, _, t = line.partition("|")
        i = int(i)
        D[S[i]] = S[i] if t == "=" else t
        n += 1
out_p.write_text(json.dumps(D, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8")
print(lang, n, "lines;", len(D), "strings")
