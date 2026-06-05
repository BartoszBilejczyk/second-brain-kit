#!/usr/bin/env python3
"""
Graph traversal for the second-brain wiki.

Walks the [[link]] graph from a seed page title outward via BFS,
returning all reachable pages within N hops ordered by distance.

Usage:
    python tools/graph-traverse.py "My Core Belief" --hops 2 --max 15
    python tools/graph-traverse.py "Creativity" --hops 1 --max 8

Output (TSV): hop_distance<TAB>filepath
"""
import re
import sys
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
LINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]*?)?\]\]")
TITLE_RE = re.compile(r"^title:\s*(.+)$", re.MULTILINE)


def build_title_index(wiki_dir: Path) -> dict[str, Path]:
    """Map every wiki page to its file path by title (frontmatter) and filename stem."""
    index: dict[str, Path] = {}
    for md_file in sorted(wiki_dir.rglob("*.md")):
        stem_key = md_file.stem.lower()
        index[stem_key] = md_file

        try:
            content = md_file.read_text(encoding="utf-8")
        except OSError:
            continue

        m = TITLE_RE.search(content)
        if m:
            title_key = m.group(1).strip().lower()
            index[title_key] = md_file

    return index


def extract_links(path: Path) -> list[str]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return []
    return LINK_RE.findall(content)


def resolve(link: str, index: dict[str, Path]) -> Path | None:
    return index.get(link.strip().lower())


def traverse(
    seed_title: str,
    hops: int = 2,
    max_pages: int = 15,
) -> list[tuple[Path, int]]:
    """BFS from seed_title through [[link]] edges."""
    index = build_title_index(WIKI_DIR)

    seed_path = resolve(seed_title, index)
    if not seed_path:
        print(f"error: no page matched '{seed_title}'", file=sys.stderr)
        print("available titles (sample):", file=sys.stderr)
        for k in sorted(index.keys())[:20]:
            print(f"  {k}", file=sys.stderr)
        return []

    visited: dict[Path, int] = {}
    queue: list[tuple[Path, int]] = [(seed_path, 0)]

    while queue and len(visited) < max_pages:
        current, hop = queue.pop(0)
        if current in visited or hop > hops:
            continue
        visited[current] = hop

        for link_title in extract_links(current):
            linked = resolve(link_title, index)
            if linked and linked not in visited:
                queue.append((linked, hop + 1))

    return sorted(visited.items(), key=lambda x: x[1])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Walk the second-brain [[link]] graph from a seed page."
    )
    parser.add_argument("seed", help="Title (or filename stem) of the starting page")
    parser.add_argument("--hops", type=int, default=2, help="Max hop depth (default: 2)")
    parser.add_argument("--max", type=int, default=15, help="Max pages to return (default: 15)")
    parser.add_argument(
        "--repo-relative",
        action="store_true",
        help="Print paths relative to the repo root instead of absolute",
    )
    args = parser.parse_args()

    results = traverse(args.seed, hops=args.hops, max_pages=args.max)
    if not results:
        sys.exit(1)

    for path, hop in results:
        display = path
        if args.repo_relative:
            try:
                display = path.relative_to(REPO_ROOT)
            except ValueError:
                pass
        print(f"{hop}\t{display}")


if __name__ == "__main__":
    main()
