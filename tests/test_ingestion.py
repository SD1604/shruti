"""
Basic sanity tests for the Gita ingestion pipeline.
Run with: pytest tests/
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from schemas.verse import Verse


def test_verse_schema_minimal():
    v = Verse(
        text_name="Bhagavad Gita",
        shruti_or_smriti="smriti",
        chapter=2,
        verse_number="47",
        english_translation="Thy right is to work only...",
        license="public_domain",
        source_url="https://sacred-texts.com/hin/sbg/",
    )
    assert v.chapter == 2
    assert v.license == "public_domain"
