"""
parse_articles.py
-----------------
Parses Articles.txt into a CSV (articles.csv) with one row per article,
including full text and all available metadata.

The Articles.txt format uses a simple structure (not standard ProQuest format):
  Title\r\n
  Author\r\n
  Publication\r\n
  \r\n
  Content line 1\r\n
  Content line 2\r\n
  ...
  \r\n             <- blank line separates articles
  Next title\r\n
  ...

This parser is inspired by the pq_parser approach from:
  https://github.com/chennesy/pq_parser

Key difference: the input file uses a three-line header (Title / Author / Publication)
rather than the ProQuest "Field: Value" metadata format.
"""

import csv
import re
import sys


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def decode(raw: bytes) -> str:
    """Decode bytes using Windows-1252 (superset of latin-1, common in
    ProQuest / news-database downloads), then strip surrounding whitespace."""
    return raw.decode("cp1252", errors="replace").strip()


def is_header_section(lines: list[bytes]) -> bool:
    """Return True when *lines* looks like an article header block.

    A header has exactly three non-empty lines:
      lines[0] – article title   (can be long)
      lines[1] – author name(s)  (always short: a name, not a sentence)
      lines[2] – publication     (short: publication title)

    False positives (content paragraphs that happen to span three lines when
    split on blank lines) are rejected because their "author" line is a full
    sentence, typically > 80 characters.
    """
    if len(lines) != 3:
        return False
    author_line = decode(lines[1])
    # A real author field is a name or short organisation, never a sentence.
    return len(author_line) <= 80


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

def parse_articles(filepath: str) -> list[dict]:
    """Parse *filepath* and return a list of article dicts."""
    with open(filepath, "rb") as fh:
        raw = fh.read()

    # Split on CRLF blank lines (the blank-line separator in the file).
    # This gives alternating header/content sections, with a small number of
    # content sections that contain internal blank lines (those produce extra
    # intermediate sections that are treated as additional content paragraphs).
    sections = raw.split(b"\r\n\r\n")

    articles: list[dict] = []
    current_title = ""
    current_author = ""
    current_publication = ""
    content_paragraphs: list[str] = []  # one entry per inter-blank-line chunk
    in_article = False

    def _save_current():
        if in_article:
            full_text = "\n\n".join(content_paragraphs)
            articles.append(
                {
                    "Title": current_title,
                    "Author": current_author,
                    "Publication": current_publication,
                    "Full Text": full_text,
                }
            )

    for section in sections:
        # Split on any remaining bare newlines within the section.
        lines = [l for l in section.split(b"\r\n") if l.strip()]

        if not lines:
            continue

        if is_header_section(lines):
            # Flush the previous article (if any) before starting the new one.
            _save_current()
            current_title = decode(lines[0])
            current_author = decode(lines[1])
            current_publication = decode(lines[2])
            content_paragraphs = []
            in_article = True
        else:
            # Content section: join its lines into a paragraph and accumulate.
            if in_article:
                paragraph = "\n".join(decode(l) for l in lines if l.strip())
                if paragraph:
                    content_paragraphs.append(paragraph)

    # Don't forget the final article.
    _save_current()

    return articles


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    input_file = "Articles.txt"
    output_file = "articles.csv"

    print(f"Parsing {input_file} …")
    articles = parse_articles(input_file)
    print(f"Found {len(articles)} articles.")

    fieldnames = ["Title", "Author", "Publication", "Full Text"]
    with open(output_file, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(articles)

    print(f"Saved to {output_file}.")

    # Quick sanity-check summary
    print("\nSample rows:")
    for art in articles[:3]:
        text_preview = art["Full Text"][:80].replace("\n", " ")
        print(f"  [{art['Publication']}] {art['Title'][:50]!r} by {art['Author']!r}")
        print(f"    Text preview: {text_preview!r}")
    print(f"\nTotal rows in CSV (excl. header): {len(articles)}")


if __name__ == "__main__":
    main()
