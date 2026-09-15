from schemas.verse import Verse


def validate_all(items: list) -> tuple[list[Verse], list[tuple[dict, str]]]:
    """Accepts a list of dicts or Verse objects. Returns (valid, failed)."""
    valid, failed = [], []
    for item in items:
        try:
            valid.append(item if isinstance(item, Verse) else Verse(**item))
        except Exception as e:
            failed.append((item, str(e)))
    print(f"Validated: {len(valid)} passed, {len(failed)} failed")
    return valid, failed
