"""
Fetches Swami Swarupananda's 1909 English translation of the Gita from
sacred-texts.com. Confirmed public domain via the page's own metadata
(meta-copyright: Public Domain and Creative Commons).

Handles verse ranges (e.g. "4-6.") by expanding them so each individual
verse number maps to the same translated text block.

Also fixes mojibake: sacred-texts.com's older HTML pages don't declare
their encoding correctly, so special characters (em-dashes, etc.) get
garbled into sequences like "â" when decoded as UTF-8. ftfy detects and
repairs this automatically.
"""

import requests
import re
import json
import time
import os
import ftfy

BASE_URL = "https://sacred-texts.com/hin/sbg/sbg{:02d}.htm"
CHAPTER_START_PAGE = 6  # Chapter 1 lives at sbg06.htm
OUTPUT_PATH = "data/raw/gita/gita_translation_raw.json"

VERSE_PATTERN = re.compile(r'^(\d+)(?:-(\d+))?\.\s+(.*)', re.MULTILINE)


def fetch_chapter_text(chapter_num: int) -> str:
    page_num = CHAPTER_START_PAGE + (chapter_num - 1)
    url = BASE_URL.format(page_num)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def parse_chapter_verses(html: str) -> dict[int, str]:
    text = re.sub(r'<[^>]+>', '\n', html)
    verse_map = {}
    for match in VERSE_PATTERN.finditer(text):
        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else start
        verse_text = ftfy.fix_text(match.group(3).strip())  # repair mojibake
        for v in range(start, end + 1):
            verse_map[v] = verse_text
    return verse_map


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    all_translations = {}
    for ch in range(1, 19):
        html = fetch_chapter_text(ch)
        verse_map = parse_chapter_verses(html)
        all_translations[ch] = verse_map
        print(f"Chapter {ch}: parsed {len(verse_map)} verses")
        time.sleep(0.5)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_translations, f, ensure_ascii=False, indent=2)
    print(f"Saved to {OUTPUT_PATH}")