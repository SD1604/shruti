from pydantic import BaseModel
from typing import Optional


class Verse(BaseModel):
    text_name: str                          # e.g. "Bhagavad Gita"
    shruti_or_smriti: str                   # "shruti" | "smriti"
    edition: Optional[str] = None
    book_or_kanda: Optional[str] = None      # e.g. "Bhishma Parva"
    chapter: int
    verse_number: str
    sanskrit_devanagari: Optional[str] = None
    iast_transliteration: Optional[str] = None
    english_translation: Optional[str] = None
    translator: Optional[str] = None
    school_of_thought: Optional[str] = None  # for commentary, e.g. "Advaita"
    license: str                             # "public_domain" | "cc-by-4.0" | "mit"
    source_url: str
