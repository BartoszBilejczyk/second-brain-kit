#!/usr/bin/env python3
"""
wiki-check.py — structural health-check for the second-brain wiki.

Reads all wiki pages, builds a link graph, and prints a structured report.
brain-lint reads this report instead of scanning individual files.

Usage:
  python tools/wiki-check.py
  python tools/wiki-check.py --json    output as JSON for programmatic use
  python tools/wiki-check.py --since 2025-01-01

Exit code 0 if no issues, 1 if any issues found.
"""

import sys
import re
import json
import argparse
from pathlib import Path
from datetime import date, timedelta

REPO_ROOT = Path(__file__).parent.parent
WIKI_ROOT = REPO_ROOT / "wiki"
INDEX_PATH = REPO_ROOT / "index.md"

REQUIRED_FIELDS = {"title", "type", "created", "updated", "confidence", "lang"}
SOURCE_REQUIRED_FIELDS = {"title", "type", "created", "updated"}
INLINE_DENSITY_THRESHOLD = 3
RELATED_THIN_THRESHOLD = 3

# Section marker — supports both English and Polish variants
RELATED_SECTION_RE = re.compile(r"^_(?:Related|Powiązane):_", re.MULTILINE)


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


def split_related(body: str) -> tuple[str, str]:
    match = RELATED_SECTION_RE.search(body)
    if match:
        return body[: match.start()], body[match.start():]
    return body, ""


def extract_link_titles(text: str) -> list[str]:
    return re.findall(r"\[\[([^\]|]+?)(?:\|[^\]]*?)?\]\]", text)


def load_wiki() -> dict:
    pages = {}
    for md_file in WIKI_ROOT.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        title = fm.get("title", "").strip()
        if not title:
            continue
        body = get_body(content)
        main_body, related_section = split_related(body)
        inline_links = extract_link_titles(main_body)
        related_links = extract_link_titles(related_section)
        pages[title] = {
            "file": str(md_file.relative_to(REPO_ROOT)),
            "type": fm.get("type", ""),
            "updated": fm.get("updated", ""),
            "frontmatter": fm,
            "inline_links": inline_links,
            "inline_link_count": len(inline_links),
            "related_links": related_links,
            "related_count": len(related_links),
            "inbound_links": [],
        }

    for title, data in pages.items():
        all_outbound = set(data["inline_links"] + data["related_links"])
        for target in all_outbound:
            if target in pages:
                pages[target]["inbound_links"].append(title)

    return pages


def load_index_files() -> set[str]:
    """Return set of repo-relative file paths declared in index.md."""
    if not INDEX_PATH.exists():
        return set()
    content = INDEX_PATH.read_text(encoding="utf-8")
    return set(re.findall(r"\((wiki/[^)]+\.md)\)", content))


def check_broken_links(pages: dict) -> list[dict]:
    known_titles = set(pages.keys())
    broken = []
    seen = {}
    for title, data in pages.items():
        all_links = set(data["inline_links"] + data["related_links"])
        for link in all_links:
            if link not in known_titles:
                if link not in seen:
                    seen[link] = []
                seen[link].append(data["file"])
    for link_title, sources in seen.items():
        broken.append({"link": link_title, "found_in": sources})
    return sorted(broken, key=lambda x: x["link"])


def check_orphans(pages: dict, index_files: set[str]) -> list[dict]:
    orphans = []
    for title, data in pages.items():
        if len(data["inbound_links"]) == 0:
            in_index = data["file"] in index_files
            orphans.append({
                "title": title,
                "file": data["file"],
                "type": data["type"],
                "in_index": in_index,
            })
    return sorted(orphans, key=lambda x: (x["type"], x["title"]))


def check_index_drift(pages: dict, index_files: set[str]) -> dict:
    disk_files = {data["file"] for data in pages.values()}
    missing_from_index = sorted(disk_files - index_files)
    missing_from_disk = sorted(index_files - disk_files)
    return {
        "missing_from_index": missing_from_index,
        "missing_from_disk": missing_from_disk,
    }


def check_thin_links(pages: dict) -> list[dict]:
    thin = []
    for title, data in pages.items():
        if data["related_count"] >= RELATED_THIN_THRESHOLD and data["inline_link_count"] == 0:
            thin.append({
                "title": title,
                "file": data["file"],
                "related_count": data["related_count"],
            })
    return sorted(thin, key=lambda x: -x["related_count"])


def check_inline_density(pages: dict, since: str) -> list[dict]:
    """Recently updated pages with fewer than 3 inline [[links]] in body.

    severity 'error'  — 0 inline links (brain-query has nothing to traverse)
    severity 'warn'   — 1-2 inline links (sparse but not empty)
    """
    low_density = []
    for title, data in pages.items():
        updated = data.get("updated", "")
        count = data["inline_link_count"]
        if updated >= since and count < INLINE_DENSITY_THRESHOLD:
            severity = "error" if count == 0 else "warn"
            low_density.append({
                "title": title,
                "file": data["file"],
                "inline_link_count": count,
                "updated": updated,
                "severity": severity,
            })
    return sorted(low_density, key=lambda x: (x["inline_link_count"], x["title"]))


def check_frontmatter_gaps(pages: dict) -> list[dict]:
    gaps = []
    for title, data in pages.items():
        fm = data["frontmatter"]
        required = SOURCE_REQUIRED_FIELDS if fm.get("type") == "source" else REQUIRED_FIELDS
        missing = sorted(required - set(fm.keys()))
        if missing:
            gaps.append({
                "title": title,
                "file": data["file"],
                "missing_fields": missing,
            })
    return sorted(gaps, key=lambda x: x["title"])


def print_report(results: dict):
    inline_errors = [i for i in results["low_inline_density"] if i["severity"] == "error"]
    inline_warns  = [i for i in results["low_inline_density"] if i["severity"] == "warn"]

    total_errors = (
        len(results["broken_links"])
        + len(results["orphans"])
        + len(results["index_drift"]["missing_from_index"])
        + len(results["index_drift"]["missing_from_disk"])
        + len(results["thin_links"])
        + len(inline_errors)
        + len(results["frontmatter_gaps"])
    )
    total_warnings = len(inline_warns)

    today = date.today().isoformat()
    print(f"# wiki-check report — {today}")
    print(f"Pages scanned: {results['page_count']}  |  Errors: {total_errors}  |  Warnings: {total_warnings}\n")

    print("## 1. BROKEN_LINKS")
    if results["broken_links"]:
        for item in results["broken_links"]:
            sources = ", ".join(item["found_in"])
            print(f"  [[{item['link']}]]")
            print(f"    found in: {sources}")
    else:
        print("  (none)")
    print()

    print("## 2. ORPHANS  (0 inbound links)")
    if results["orphans"]:
        content_orphans = [o for o in results["orphans"] if o["type"] != "source"]
        source_orphans = [o for o in results["orphans"] if o["type"] == "source"]
        if content_orphans:
            print("  Content pages:")
            for o in content_orphans:
                idx = "in index" if o["in_index"] else "NOT in index"
                print(f"    {o['title']}  [{o['type']}]  ({idx})")
        if source_orphans:
            print("  Source pages (systemic — wiki pages don't back-link to sources):")
            for o in source_orphans:
                print(f"    {o['title']}")
    else:
        print("  (none)")
    print()

    print("## 3. INDEX_DRIFT")
    drift = results["index_drift"]
    if drift["missing_from_index"] or drift["missing_from_disk"]:
        if drift["missing_from_index"]:
            print("  On disk but missing from index.md:")
            for f in drift["missing_from_index"]:
                print(f"    {f}")
        if drift["missing_from_disk"]:
            print("  In index.md but no file on disk:")
            for f in drift["missing_from_disk"]:
                print(f"    {f}")
    else:
        print("  (none)")
    print()

    print(f"## 4. THIN_LINKS  (3+ _Related:_ entries, 0 inline [[links]])")
    if results["thin_links"]:
        for item in results["thin_links"]:
            print(f"  {item['title']}  (related: {item['related_count']})")
    else:
        print("  (none)")
    print()

    print(f"## 5. LOW_INLINE_DENSITY  (updated since {results['since']}, <{INLINE_DENSITY_THRESHOLD} inline links)")
    if inline_errors:
        print("  [ERROR] 0 inline links — brain-query has nothing to traverse:")
        for item in inline_errors:
            print(f"    {item['title']}  (inline: {item['inline_link_count']}, updated: {item['updated']})")
    if inline_warns:
        print("  [WARN] 1-2 inline links — sparse but not empty:")
        for item in inline_warns:
            print(f"    {item['title']}  (inline: {item['inline_link_count']}, updated: {item['updated']})")
    if not results["low_inline_density"]:
        print("  (none)")
    print()

    print("## 6. FRONTMATTER_GAPS")
    if results["frontmatter_gaps"]:
        for item in results["frontmatter_gaps"]:
            print(f"  {item['title']}  missing: {', '.join(item['missing_fields'])}")
    else:
        print("  (none)")
    print()

    return total_errors > 0


def main():
    # Default: check pages updated in the last year
    one_year_ago = (date.today() - timedelta(days=365)).isoformat()

    parser = argparse.ArgumentParser(description="Structural health-check for the second-brain wiki.")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of human-readable text")
    parser.add_argument("--since", default=one_year_ago, help="Check inline density for pages updated since this date (YYYY-MM-DD)")
    args = parser.parse_args()

    pages = load_wiki()
    index_files = load_index_files()

    results = {
        "page_count": len(pages),
        "generated": date.today().isoformat(),
        "since": args.since,
        "broken_links": check_broken_links(pages),
        "orphans": check_orphans(pages, index_files),
        "index_drift": check_index_drift(pages, index_files),
        "thin_links": check_thin_links(pages),
        "low_inline_density": check_inline_density(pages, since=args.since),
        "frontmatter_gaps": check_frontmatter_gaps(pages),
    }

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        sys.exit(0)

    has_errors = print_report(results)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
