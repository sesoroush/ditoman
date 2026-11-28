"""Shared helpers for the Ditoman book-summary scripts."""
import datetime, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "report"))
from jalali import g2j  # noqa: E402

DATA = ROOT / "scripts" / "books" / "data"
CATALOG = ROOT / "data" / "books" / "catalog.json"
STATE = ROOT / "data" / "books" / "state.json"
COVERS = ROOT / "data" / "books" / "covers.json"
FA_MONTHS = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def fa_num(x):
    return str(x).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))


def tehran_today():
    return (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3, minutes=30)).date()


def dates(d):
    """Date strings for a datetime.date: long/short, Persian (Jalali) and English."""
    jy, jm, jd = g2j(d.year, d.month, d.day)
    return {"iso": d.isoformat(), "fa_long": f"{fa_num(jd)} {FA_MONTHS[jm - 1]} {fa_num(jy)}", "fa_short": f"{fa_num(jd)} {FA_MONTHS[jm - 1]}",
            "en_long": f"{d.day} {EN_MONTHS[d.month - 1]} {d.year}", "en_short": f"{d.day} {EN_MONTHS[d.month - 1][:3]}"}


def load(path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def catalog():
    return load(CATALOG)


def book(slug):
    return next((b for b in catalog()["books"] if b["slug"] == slug), None)


def jacket_ok(slug):
    """A jacket exists and was not rejected at review."""
    return (ROOT / "assets" / "books" / f"{slug}.jpg").exists() and not (load(COVERS, {}).get(slug) or {}).get("rejected")


def telegram_text(slug, meta):
    """Full Telegram post: the book's own text plus the fixed footer (no image line)."""
    body = (DATA / slug / "telegram.md").read_text(encoding="utf-8").strip()
    return (f"{body}\n\n📖 نسخه‌ی کامل فارسی و انگلیسی:\n👈 https://ditoman.com/{slug}.html\n\n"
            "📚 کتابخانه‌ی کتاب‌های دیتومان:\n👈 https://ditoman.com/books.html\n\n"
            "ℹ️ این خلاصه نوشته‌ی دیتومان است و جایگزین کتاب نیست.\n\n"
            "📊 قیمت لحظه‌ای تتر، بیت‌کوین و طلا، هر وقت بخواهی:\n👈 https://ditoman.com/prices.html\n\n"
            f"Ditoman | Learn · Connect · Evolve\n{meta['hashtags']}\n")


def telegram_len(text):
    import re
    plain = re.sub(r"\*\*(.+?)\*\*", r"\1", text, flags=re.S)
    return len(plain.encode("utf-16-le")) // 2
