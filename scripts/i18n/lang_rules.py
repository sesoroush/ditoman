"""Patterns that need no dictionary entry: dates, reading times and step numbers, per language."""
import re

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONRE = "|".join(MON)

def _m(s):
    return MON.index(s) + 1

R = {
    "zh": dict(date=lambda d, m: f"{_m(m)}月{d}日", read=lambda n: f"阅读{n}分钟", mins=lambda n: f"{n}分钟", step=lambda n: f"第{n}步"),
    "tr": dict(date=lambda d, m: f"{d} " + ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"][_m(m) - 1],
               read=lambda n: f"{n} dk okuma", mins=lambda n: f"{n} dk", step=lambda n: f"Adım {n}"),
    "ru": dict(date=lambda d, m: f"{d} " + ["янв.", "февр.", "мар.", "апр.", "мая", "июн.", "июл.", "авг.", "сент.", "окт.", "нояб.", "дек."][_m(m) - 1],
               read=lambda n: f"{n} мин чтения", mins=lambda n: f"{n} мин", step=lambda n: f"Шаг {n}"),
}


def apply(lang, t):
    r = R[lang]
    m = re.match(rf"^(\d+) ({MONRE}) · (\d+) min read$", t)
    if m:
        return r["date"](m[1], m[2]) + " · " + r["read"](m[3])
    m = re.match(r"^(\d+) min read$", t)
    if m:
        return r["read"](m[1])
    m = re.match(r"^(\d+) min$", t)
    if m:
        return r["mins"](m[1])
    m = re.match(r"^Step (\d+)$", t)
    if m:
        return r["step"](m[1])
    m = re.match(rf"^(\d+) ({MONRE})$", t)
    if m:
        return r["date"](m[1], m[2])
    return None
