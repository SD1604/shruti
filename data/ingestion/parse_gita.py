import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from schemas.verse import Verse

SANSKRIT_PATH = "data/raw/gita/gita_sanskrit_raw.json"
TRANSLATION_PATH = "data/raw/gita/gita_translation_raw.json"


def parse() -> list[Verse]:
    with open(SANSKRIT_PATH, encoding="utf-8") as f:
        sanskrit_data = json.load(f)
    with open(TRANSLATION_PATH, encoding="utf-8") as f:
        translation_data = json.load(f)

    verses = []
    missing = []
    for item in sanskrit_data:
        ch, v = item["chapter"], item["verse"]
        translation = translation_data.get(str(ch), {}).get(str(v))
        if translation is None:
            missing.append(f"{ch}.{v}")
            continue

        verses.append(Verse(
            text_name="Bhagavad Gita",
            shruti_or_smriti="smriti",
            edition="standard",
            book_or_kanda="Bhishma Parva",
            chapter=ch,
            verse_number=str(v),
            sanskrit_devanagari=item["slok"],
            iast_transliteration=item.get("transliteration"),
            english_translation=translation,
            translator="Swami Swarupananda (1909)",
            school_of_thought=None,
            license="public_domain",
            source_url="https://sacred-texts.com/hin/sbg/",
        ))

    if missing:
        print(f"WARNING: {len(missing)} verses had no matching translation: {missing[:10]}...")
    print(f"Successfully merged {len(verses)} verses")
    return verses


if __name__ == "__main__":
    parse()
