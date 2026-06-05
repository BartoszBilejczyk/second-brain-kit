#!/usr/bin/env python3
"""
build-graph.py — generate wiki-graph.json for the second-brain wiki.

Reads all wiki/ pages and writes meta/wiki-graph.json.
brain-query reads this file instead of opening every individual page,
so it can navigate the full link structure in one shot.

Usage:
  python tools/build-graph.py
  python tools/build-graph.py --pretty    # formatted JSON (larger, human-readable)
"""

import json
import re
import argparse
from pathlib import Path
from datetime import date

REPO_ROOT = Path(__file__).parent.parent
WIKI_ROOT = REPO_ROOT / "wiki"
OUTPUT_PATH = REPO_ROOT / "meta" / "wiki-graph.json"
EXCERPT_CHARS = 200


def parse_frontmatter(content: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm


def get_body(content: str) -> str:
    match = re.match(r"^---\n.*?\n---\n(.*)$", content, re.DOTALL)
    return match.group(1) if match else content


def extract_link_titles(text: str) -> list[str]:
    """Extract target titles from [[Title]] and [[Title|Display]] patterns."""
    return re.findall(r"\[\[([^\]|]+?)(?:\|[^\]]*?)?\]\]", text)


def make_excerpt(body: str) -> str:
    """First EXCERPT_CHARS chars of body text, stripped of markdown syntax."""
    body = re.sub(r"\n_Related:_.*$", "", body, flags=re.DOTALL)
    body = re.sub(r"\n_Powiązane:_.*$", "", body, flags=re.DOTALL)
    body = re.sub(r"\[\[(?:[^\]|]+\|)?([^\]]+)\]\]", r"\1", body)
    body = re.sub(r"[#*_`>-]", " ", body)
    body = re.sub(r"\s+", " ", body).strip()
    return body[:EXCERPT_CHARS]


def load_wiki() -> dict:
    pages = {}
    for md_file in WIKI_ROOT.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        title = fm.get("title", "").strip()
        if not title:
            continue
        body = get_body(content)

        related_match = re.search(r"^_(?:Related|Powiązane):_", body, re.MULTILINE)
        if related_match:
            main_body = body[: related_match.start()]
            related_text = body[related_match.start():]
        else:
            main_body = body
            related_text = ""

        inline_links = extract_link_titles(main_body)
        related_links = extract_link_titles(related_text)
        all_links = list(dict.fromkeys(inline_links + related_links))

        pages[title] = {
            "file": str(md_file.relative_to(REPO_ROOT)),
            "type": fm.get("type", ""),
            "updated": fm.get("updated", ""),
            "confidence": fm.get("confidence", ""),
            "lang": fm.get("lang", ""),
            "inline_links": inline_links,
            "all_links": all_links,
            "inbound_links": [],
            "excerpt": make_excerpt(body),
        }

    for title, data in pages.items():
        for target in data["all_links"]:
            if target in pages:
                if title not in pages[target]["inbound_links"]:
                    pages[target]["inbound_links"].append(title)

    return pages


def main():
    parser = argparse.ArgumentParser(description="Generate wiki-graph.json for navigation.")
    parser.add_argument("--pretty", action="store_true", help="Output formatted JSON (larger, human-readable)")
    args = parser.parse_args()

    pages = load_wiki()
    output = {
        "generated": date.today().isoformat(),
        "page_count": len(pages),
        "pages": pages,
    }

    indent = 2 if args.pretty else None
    separators = None if args.pretty else (",", ":")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(output, indent=indent, separators=separators, ensure_ascii=False),
        encoding="utf-8",
    )

    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"wiki-graph.json written — {len(pages)} pages, {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
