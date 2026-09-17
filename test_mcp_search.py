"""
Quick manual test — calls search_verses() directly as a normal Python
function, bypassing the MCP server layer entirely. This proves the actual
search logic works before we test it as a real MCP tool.
"""

from mcp_server.server import search_verses

results = search_verses("what happens to the soul after death", top_k=3)

for r in results:
    print(f"\nChapter {r['chapter']}, Verse {r['verse_number']} ({r['translator']}):")
    print(r['text'])