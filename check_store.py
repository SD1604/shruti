import sys
sys.path.append(".")

from agent.search_core import search_verses

results = search_verses("duty without attachment to results", top_k=3)

for r in results:
    print(f"\nChapter {r['chapter']}, Verse {r['verse_number']}:")
    print(r['text'])