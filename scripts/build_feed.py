"""Build telegram/feed.json from published Telegram posts (telegram/*.md, not drafts).

Each post file is named YYYY-MM-DD-NN-slug.md. Optional first line "image: file.png".
The site's posts.html renders this feed so every channel post is also on the website.
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TG = ROOT / "telegram"

def main():
    items = []
    for f in sorted(TG.glob("*.md")):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(\d+)-(.+)\.md$", f.name) or re.match(r"(\d{4}-\d{2}-\d{2})-()(.+)\.md$", f.name)
        if not m:
            continue
        lines = f.read_text(encoding="utf-8").splitlines()
        image = None
        if lines and lines[0].startswith("image:"):
            image = lines[0].split(":", 1)[1].strip()
            lines = lines[1:]
        text = "\n".join(lines).strip()
        items.append({"id": f.stem, "date": m.group(1), "order": int(m.group(2) or 0), "image": image, "text": text})
    items.sort(key=lambda x: (x["date"], x["order"]), reverse=True)
    (TG / "feed.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(items)} posts")

if __name__ == "__main__":
    main()
