#!/usr/bin/env python3
"""
wiki-rename.py — rename a wiki page title and update all [[wikilinks]] across the vault.

Two modes:

  rename   — change a page's canonical title and update every [[link]] that references it.
             Also updates the title: field in the page's own frontmatter and index.md.

  fix-link — replace a broken/mistyped link text with the correct title, across all wiki files.
             Does NOT change any page's own frontmatter. Use when a link was written wrong,
             not when the page itself is being renamed.

Usage:
  python tools/wiki-rename.py rename   "Old Title" "New Title"  [--dry-run]
  python tools/wiki-rename.py fix-link "Wrong Link Text" "Correct Title"  [--dry-run]

  --dry-run  prints what would change without writing anything.
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import date


def title_to_slug(title: str) -> str:
    """Convert a page title to a safe filename stem."""
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug.strip("-")

REPO_ROOT = Path(__file__).parent.parent
WIKI_ROOT = REPO_ROOT / "wiki"
INDEX_PATH = REPO_ROOT / "index.md"
LOG_PATH = REPO_ROOT / "log.md"


def find_page_file(title: str) -> Path | None:
    """Find the wiki file whose frontmatter title: matches exactly."""
    for md_file in WIKI_ROOT.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        if re.search(rf"^title: {re.escape(title)}\s*$", content, re.MULTILINE):
            return md_file
    return None


def replace_links_in_file(path: Path, old_title: str, new_title: str, dry_run: bool) -> int:
    content = path.read_text(encoding="utf-8")
    pattern = r"\[\[" + re.escape(old_title) + r"\]\]"
    new_content, count = re.subn(pattern, f"[[{new_title}]]", content)
    if count > 0:
        if not dry_run:
            path.write_text(new_content, encoding="utf-8")
        print(f"  {'[dry-run] ' if dry_run else ''}Updated {path.relative_to(REPO_ROOT)} ({count} occurrence{'s' if count != 1 else ''})")
    return count


def replace_links_across_vault(old_title: str, new_title: str, dry_run: bool) -> int:
    total = 0
    for md_file in WIKI_ROOT.rglob("*.md"):
        total += replace_links_in_file(md_file, old_title, new_title, dry_run)
    if INDEX_PATH.exists():
        total += replace_links_in_file(INDEX_PATH, old_title, new_title, dry_run)
    return total


def update_frontmatter_title(page_file: Path, old_title: str, new_title: str, dry_run: bool):
    content = page_file.read_text(encoding="utf-8")
    today = date.today().isoformat()
    content = re.sub(
        rf"^title: {re.escape(old_title)}\s*$",
        f"title: {new_title}",
        content,
        flags=re.MULTILINE
    )
    content = re.sub(
        r"^updated: \d{4}-\d{2}-\d{2}\s*$",
        f"updated: {today}",
        content,
        flags=re.MULTILINE
    )
    if not dry_run:
        page_file.write_text(content, encoding="utf-8")
    print(f"  {'[dry-run] ' if dry_run else ''}Updated frontmatter in {page_file.name}")


def update_index(old_title: str, new_title: str, dry_run: bool):
    if not INDEX_PATH.exists():
        return
    content = INDEX_PATH.read_text(encoding="utf-8")
    new_content = content.replace(f"[{old_title}]", f"[{new_title}]")
    if new_content != content:
        if not dry_run:
            INDEX_PATH.write_text(new_content, encoding="utf-8")
        print(f"  {'[dry-run] ' if dry_run else ''}Updated index.md display text")


def append_log(operation: str, old_title: str, new_title: str, replacements: int, dry_run: bool):
    if dry_run:
        return
    today = date.today().isoformat()
    entry = f"\n## [{today}] wiki-rename | {operation}: \"{old_title}\" → \"{new_title}\" ({replacements} link{'s' if replacements != 1 else ''} updated)\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)


def cmd_rename(old_title: str, new_title: str, dry_run: bool):
    print(f"\nRename: \"{old_title}\" → \"{new_title}\"")
    if dry_run:
        print("(dry-run — no files will be written)\n")

    page_file = find_page_file(old_title)
    if page_file is None:
        print(f"ERROR: No wiki page found with title: {old_title}")
        print("Hint: check that the title matches the frontmatter exactly (case-sensitive).")
        sys.exit(1)

    print(f"Found page: {page_file.relative_to(REPO_ROOT)}")
    update_frontmatter_title(page_file, old_title, new_title, dry_run)
    total = replace_links_across_vault(old_title, new_title, dry_run)
    update_index(old_title, new_title, dry_run)

    # Rename the physical file to match the new title
    new_slug = title_to_slug(new_title)
    new_file = page_file.parent / f"{new_slug}.md"
    if new_file != page_file:
        if dry_run:
            print(f"  [dry-run] Would rename {page_file.name} → {new_file.name}")
        else:
            page_file.rename(new_file)
            print(f"  Renamed file: {page_file.name} → {new_file.name}")

    append_log("rename", old_title, new_title, total, dry_run)
    print(f"\nDone. {total} link{'s' if total != 1 else ''} updated across the vault.")


def cmd_fix_link(wrong_text: str, correct_title: str, dry_run: bool):
    print(f"\nFix-link: [[{wrong_text}]] → [[{correct_title}]]")
    if dry_run:
        print("(dry-run — no files will be written)\n")

    target_file = find_page_file(correct_title)
    if target_file is None:
        print(f"WARNING: No wiki page found with title: {correct_title}")
        print("Proceeding anyway — you may be fixing a link to a to-write marker.")

    total = replace_links_across_vault(wrong_text, correct_title, dry_run)
    append_log("fix-link", wrong_text, correct_title, total, dry_run)

    if total == 0:
        print(f"No occurrences of [[{wrong_text}]] found — nothing to fix.")
    else:
        print(f"\nDone. {total} link{'s' if total != 1 else ''} corrected.")


def main():
    parser = argparse.ArgumentParser(
        description="Rename a wiki page title and update all [[wikilinks]] atomically.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("mode", choices=["rename", "fix-link"], help="Operation mode")
    parser.add_argument("old_title", help="Current title (or broken link text for fix-link)")
    parser.add_argument("new_title", help="New title (or correct title for fix-link)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")

    args = parser.parse_args()

    if args.mode == "rename":
        cmd_rename(args.old_title, args.new_title, args.dry_run)
    elif args.mode == "fix-link":
        cmd_fix_link(args.old_title, args.new_title, args.dry_run)


if __name__ == "__main__":
    main()
