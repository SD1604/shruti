"""
Fetches Sanskrit + transliteration (public domain) for all 700 Bhagavad Gita
verses from the vedicscriptures.github.io live API.

Deliberately does NOT save any of the author-attributed commentary fields
(Tejomayananda, Sivananda, Prabhupada, etc.) returned by this API, since those
are modern copyrighted translations, not the ancient verse text itself.
"""

import requests
import json
import time
import os

BASE_URL = "https://vedicscriptures.github.io"
OUTPUT_PATH = "data/raw/gita/gita_sanskrit_raw.json"


def fetch_chapter_verse_counts() -> dict[int, int]:
    counts = {}
    for ch in range(1, 19):
        resp = requests.get(f"{BASE_URL}/chapter/{ch}")
        resp.raise_for_status()
        data = resp.json()
        counts[ch] = data["verses_count"]
        time.sleep(0.2)
    return counts


def fetch_all_verses(counts: dict[int, int]) -> list[dict]:
    raw_verses = []
    for ch, verse_count in counts.items():
        for sl in range(1, verse_count + 1):
            resp = requests.get(f"{BASE_URL}/slok/{ch}/{sl}")
            resp.raise_for_status()
            data = resp.json()
            raw_verses.append({
                "chapter": data["chapter"],
                "verse": data["verse"],
                "slok": data["slok"],
                "transliteration": data.get("transliteration"),
            })
            time.sleep(0.15)
        print(f"Chapter {ch}: fetched {verse_count} verses")
    return raw_verses


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    counts = fetch_chapter_verse_counts()
    verses = fetch_all_verses(counts)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(verses)} verses to {OUTPUT_PATH}")
