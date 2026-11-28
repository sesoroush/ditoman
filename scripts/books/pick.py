#!/usr/bin/env python3
"""Pick books at random.

  python3 scripts/books/pick.py post          one prepared book that has not gone to Telegram yet
  python3 scripts/books/pick.py prepare [N]   N books (default 3) that have a reviewed jacket but no summary yet
  python3 scripts/books/pick.py status        counts, and the books still waiting for a jacket
Prints one slug per line (nothing if none is left).
"""
import random, sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import DATA, ROOT, STATE, catalog, jacket_ok, load  # noqa: E402

state = load(STATE, {})
books = catalog()["books"]
prepared = [b for b in books if state.get(b["slug"], {}).get("prepared") and (ROOT / f"{b['slug']}.html").exists()]
mode = sys.argv[1] if len(sys.argv) > 1 else "status"
if mode == "post":
    pool = [b["slug"] for b in prepared if not state[b["slug"]].get("posted")]
    if pool:
        print(random.choice(pool))
elif mode == "prepare":
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    done = {b["slug"] for b in prepared}
    pool = [b["slug"] for b in books if b["slug"] not in done and jacket_ok(b["slug"])]
    print("\n".join(random.sample(pool, min(n, len(pool)))))
else:
    posted = [b for b in prepared if state[b["slug"]].get("posted")]
    print(f"{len(books)} books in the catalog; {len(prepared)} summaries prepared; {len(posted)} posted to Telegram; "
          f"{len(prepared) - len(posted)} ready and waiting")
    missing = [b for b in books if not jacket_ok(b["slug"])]
    if missing:
        print("No usable jacket yet (put the image at assets/books/<slug>.jpg):")
        for b in missing:
            print(f"  {b['n']:>3}  {b['slug']}  |  {b['en']} ({b['authors_en']}, {b['year']})")
