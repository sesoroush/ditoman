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
    "pt": dict(date=lambda d, m: f"{d} " + ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"][_m(m) - 1],
               read=lambda n: f"{n} min de leitura", mins=lambda n: f"{n} min", step=lambda n: f"Passo {n}"),
    "es": dict(date=lambda d, m: f"{d} " + ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sept", "oct", "nov", "dic"][_m(m) - 1],
               read=lambda n: f"{n} min de lectura", mins=lambda n: f"{n} min", step=lambda n: f"Paso {n}"),
    "fr": dict(date=lambda d, m: f"{d} " + ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."][_m(m) - 1],
               read=lambda n: f"{n} min de lecture", mins=lambda n: f"{n} min", step=lambda n: f"Étape {n}"),
    "de": dict(date=lambda d, m: f"{d}. " + ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."][_m(m) - 1],
               read=lambda n: f"{n} Min. Lesezeit", mins=lambda n: f"{n} Min.", step=lambda n: f"Schritt {n}"),
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
