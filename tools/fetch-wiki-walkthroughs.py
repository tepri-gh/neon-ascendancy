#!/usr/bin/env python3
"""Fetch Cyberpunk 2077 quest and location pages from the Cyberpunk wiki.

Local research input for venue work (docs/venue-playbook.md). Downloads the
raw wikitext of every page in the quest and location categories through the
MediaWiki API, plus an index. Output is never committed; AGENTS-LOCAL.md
records where it lives.

Usage:
  tools/fetch-wiki-walkthroughs.py [--out DIR]

Idempotent: re-running refetches the category lists and rewrites every page
and the index. Requests are rate-limited to one per second. Stdlib only.
Wiki content is CC BY-SA (https://cyberpunk.fandom.com).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://cyberpunk.fandom.com/api.php"
USER_AGENT = "neon-research-client/0.1 (offline mod research)"
DEFAULT_OUT = Path.home() / "Work" / "Cyberpunk" / "Walkthroughs" / "cyberpunk-fandom"

# Category -> kind. Subcategories are not followed; every district category is
# listed explicitly so unrelated subcategories (cities, countries) stay out.
CATEGORIES = {
    "Cyberpunk 2077 Main Jobs": "main_job",
    "Cyberpunk 2077 Side Jobs": "side_job",
    "Cyberpunk 2077 Gigs": "gig",
    "Cyberpunk 2077 Minor Jobs": "minor_job",
    "Cyberpunk 2077 Minor Activities": "minor_activity",
    "Cyberpunk 2077 Locations": "location",
    "Cyberpunk 2077 Locations - Badlands": "location",
    "Cyberpunk 2077 Locations - City Center": "location",
    "Cyberpunk 2077 Locations - Heywood": "location",
    "Cyberpunk 2077 Locations - Pacifica": "location",
    "Cyberpunk 2077 Locations - Santo Domingo": "location",
    "Cyberpunk 2077 Locations - Watson": "location",
    "Cyberpunk 2077 Locations - Westbrook": "location",
    "Cyberpunk 2077 Districts": "district",
    "Cyberpunk 2077 Sub-districts": "sub_district",
    "Cyberpunk 2077 Apartments": "apartment",
    "Cyberpunk 2077 Stores": "store",
    "Cyberpunk 2077 Vendor Hubs": "vendor_hub",
    "Cyberpunk 2077 Vendors": "vendor",
    "Cyberpunk 2077 Fixers": "fixer",
    "Cyberpunk 2077 Gangs": "gang",
}

_last_request = 0.0


def api(params: dict[str, str]) -> dict:
    global _last_request
    wait = 1.0 - (time.monotonic() - _last_request)
    if wait > 0:
        time.sleep(wait)
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"})
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                _last_request = time.monotonic()
                return json.load(resp)
        except OSError as exc:  # network hiccup: back off and retry
            if attempt == 3:
                raise
            print(f"  retry after {exc}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    raise AssertionError("unreachable")


def category_members(category: str) -> list[str]:
    titles: list[str] = []
    params = {"action": "query", "list": "categorymembers", "cmtitle": f"Category:{category}",
              "cmtype": "page", "cmnamespace": "0", "cmlimit": "500"}
    while True:
        data = api(params)
        titles += [m["title"] for m in data["query"]["categorymembers"]]
        cont = data.get("continue")
        if not cont:
            return titles
        params = {**params, **cont}


def fetch_pages(titles: list[str]) -> list[dict]:
    pages: list[dict] = []
    for i in range(0, len(titles), 50):
        batch = titles[i:i + 50]
        data = api({"action": "query", "prop": "revisions", "rvprop": "content|ids|timestamp",
                    "rvslots": "main", "redirects": "1", "titles": "|".join(batch)})
        pages += data["query"]["pages"]
        print(f"  pages {i + len(batch)}/{len(titles)}")
    return pages


def safe_name(title: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", title).strip("_") + ".wiki"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    pages_dir = args.out / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    kinds: dict[str, set[str]] = {}
    cats: dict[str, set[str]] = {}
    for category, kind in CATEGORIES.items():
        members = category_members(category)
        print(f"{category}: {len(members)}")
        for t in members:
            kinds.setdefault(t, set()).add(kind)
            cats.setdefault(t, set()).add(category)

    index = []
    for page in fetch_pages(sorted(kinds)):
        if page.get("missing") or "revisions" not in page:
            continue
        title = page["title"]
        rev = page["revisions"][0]
        fname = safe_name(title)
        (pages_dir / fname).write_text(rev["slots"]["main"]["content"], encoding="utf-8")
        index.append({
            "title": title,
            "file": f"pages/{fname}",
            "kinds": sorted(kinds.get(title, set())),
            "categories": sorted(cats.get(title, set())),
            "pageid": page["pageid"],
            "revid": rev["revid"],
            "timestamp": rev["timestamp"],
            "url": "https://cyberpunk.fandom.com/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
        })
    index.sort(key=lambda r: r["title"])
    (args.out / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(index)} pages to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
