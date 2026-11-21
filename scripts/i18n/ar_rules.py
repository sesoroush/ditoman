"""Shared Arabic rules: Persian digits to Western digits, Iranian-calendar dates to Gregorian, reading times, steps."""
import re

FA_DIG = str.maketrans("۰۱۲۳۴۵۶۷۸۹٬٫", "0123456789,.")
# first day of each Iranian month in 1405 as (Gregorian month, day); the year rolls over in Dey
MONTH_START = {"فروردین": (3, 21), "اردیبهشت": (4, 21), "خرداد": (5, 22), "تیر": (6, 22), "مرداد": (7, 23), "شهریور": (8, 23),
               "مهر": (9, 23), "آبان": (10, 23), "آذر": (11, 22), "دی": (12, 22), "بهمن": (1, 21), "اسفند": (2, 20)}
G_MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
DAYS_IN = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def greg(day, month):
    gm, gd = MONTH_START[month]
    gd += int(day) - 1
    while gd > DAYS_IN[gm - 1]:
        gd -= DAYS_IN[gm - 1]
        gm = gm % 12 + 1
    return f"{gd} {G_MONTHS[gm - 1]}"


def minutes(n):
    n = int(n)
    if n == 1: return "دقيقة واحدة"
    if n == 2: return "دقيقتان"
    if 3 <= n <= 10: return f"{n} دقائق"
    return f"{n} دقيقة"


MONTHS_RE = "|".join(MONTH_START)
PATTERNS = [
    (re.compile(rf"^(\d+) ({MONTHS_RE}) · (\d+) دقیقه مطالعه$"), lambda m: f"{greg(m[1], m[2])} · قراءة {minutes(m[3])}"),
    (re.compile(r"^(\d+) دقیقه مطالعه$"), lambda m: f"قراءة {minutes(m[1])}"),
    (re.compile(r"^(\d+) دقیقه$"), lambda m: minutes(m[1])),
    (re.compile(r"^قدم (\d+)$"), lambda m: f"الخطوة {m[1]}"),
    (re.compile(rf"^(\d+) ({MONTHS_RE})$"), lambda m: greg(m[1], m[2])),
    (re.compile(rf"^(\d+) ({MONTHS_RE}) (\d{{4}})$"), lambda m: f"{greg(m[1], m[2])} {int(m[3]) + 621}"),
]


def apply(t):
    """Arabic for one normalised Persian string from the rules, or None."""
    d = t.translate(FA_DIG)
    for rx, fn in PATTERNS:
        m = rx.match(d)
        if m:
            return fn(m)
    return None
