"""
parse_articles.py
-----------------
Parses a ProQuest-style flat-text export (Articles.txt) into a CSV file
with one row per article, including all available metadata and full text.

Format detected in this file:
  <Title>
  <Author>          (may be absent)
  <Publication>

  <Body paragraph 1>

  <Body paragraph 2>
  ...
  <Title of next article>
  ...

Articles are separated from each other by blank lines. A "header block"
is identified as a block of ≤3 short lines (no line > 200 chars).
"""

import re
import csv
import sys

INPUT_FILE  = "Articles.txt"
OUTPUT_FILE = "articles.csv"


def is_header_block(block: str) -> bool:
    """Return True if block looks like an article header (title/author/pub).

    Rules:
      - 2 or 3 lines exactly (single-line subheadings inside articles are
        excluded; 4+ line blocks are body text with internal line breaks)
      - The first line (title) may be up to 200 chars
      - Lines 2 and 3 (author / publication) must be ≤ 70 chars each;
        longer values indicate body text or channel descriptions, not metadata
    """
    lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
    if len(lines) < 2 or len(lines) > 3:
        return False
    # Title line: reasonable headline length
    if len(lines[0]) > 200:
        return False
    # Author / publication lines must be short (names, not sentences)
    if any(len(l) > 70 for l in lines[1:]):
        return False
    return True


def clean(text: str) -> str:
    """Normalise whitespace and strip stray Windows smart-chars."""
    # Replace common Windows-1252 / Latin-1 artifacts that survived UTF-8 decode
    replacements = {
        "’": "'",   # right single quotation mark
        "‘": "'",   # left  single quotation mark
        "“": '"',   # left  double quotation mark
        "”": '"',   # right double quotation mark
        "–": "-",   # en dash
        "—": "--",  # em dash
        " ": " ",   # non-breaking space
        "�": "",    # replacement character (encoding error residue)
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text.strip()


def parse(path: str) -> list[dict]:
    raw = open(path, "rb").read().decode("utf-8", errors="replace")
    # Normalise line endings
    raw = raw.replace("\r\n", "\n").replace("\r", "\n").strip()

    # Split into paragraphs / blocks on blank lines
    blocks = re.split(r"\n\n", raw)

    articles: list[dict] = []
    current_header: dict | None = None
    body_parts: list[str] = []

    def flush():
        """Commit the current article to the list."""
        if current_header is None:
            return
        full_text = "\n\n".join(clean(p) for p in body_parts if p.strip())
        articles.append({
            "title":       current_header.get("title", ""),
            "author":      current_header.get("author", ""),
            "publication": current_header.get("publication", ""),
            "full_text":   full_text,
        })

    for block in blocks:
        block_stripped = block.strip()
        if not block_stripped:
            continue

        if is_header_block(block_stripped):
            # Save the previous article before starting a new one
            flush()
            body_parts = []

            lines = [l.strip() for l in block_stripped.splitlines() if l.strip()]
            if len(lines) == 3:
                current_header = {
                    "title":       clean(lines[0]),
                    "author":      clean(lines[1]),
                    "publication": clean(lines[2]),
                }
            elif len(lines) == 2:
                # Could be title + publication (no author) or title + author
                # Heuristic: if second line contains spaces it's likely a full name
                current_header = {
                    "title":       clean(lines[0]),
                    "author":      "",
                    "publication": clean(lines[1]),
                }
            else:  # 1 line — just a title
                current_header = {
                    "title":       clean(lines[0]),
                    "author":      "",
                    "publication": "",
                }
        else:
            # Body paragraph — accumulate
            if current_header is not None:
                body_parts.append(block_stripped)

    # Don't forget the last article
    flush()
    return articles


def write_csv(articles: list[dict], path: str) -> None:
    fieldnames = ["title", "author", "publication", "full_text"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(articles)


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print(f"Parsing {INPUT_FILE} ...")
    articles = parse(INPUT_FILE)
    print(f"  → {len(articles)} articles found")

    write_csv(articles, OUTPUT_FILE)
    print(f"  → Saved to {OUTPUT_FILE}")

    # Quick sanity check
    for a in articles[:3]:
        print(f"\n  Title : {a['title'][:70]}")
        print(f"  Author: {a['author']}")
        print(f"  Pub   : {a['publication']}")
        print(f"  Text  : {a['full_text'][:120]}...")
