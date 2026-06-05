#!/usr/bin/env python3
"""
embed-wiki.py — generate or update semantic embeddings for the wiki.

Uses sentence-transformers (local, offline) to embed every wiki page.
Embeddings are stored in meta/embeddings.json and used by brain-query
to find semantically relevant pages without reading the full wiki.

Run modes:
  python tools/embed-wiki.py              # incremental — only embed changed pages
  python tools/embed-wiki.py --rebuild    # force re-embed all pages
  python tools/embed-wiki.py --query "what do I think about risk?"
  python tools/embed-wiki.py --query "..." --top 5

The model (paraphrase-multilingual-mpnet-base-v2) is ~420MB and downloads on
first run to ~/.cache/huggingface/. Subsequent runs are fully offline.
Works with any language — English, Polish, Spanish, etc.
"""

import json
import logging
import os
import re
import sys
import warnings
import argparse
import math
from pathlib import Path
from datetime import date

# Suppress noisy HuggingFace Hub warnings — model runs fully offline after first download
os.environ.setdefault("HF_HUB_VERBOSITY", "error")
warnings.filterwarnings("ignore", message=".*unauthenticated.*", category=UserWarning)
warnings.filterwarnings("ignore", message=".*HF_TOKEN.*", category=UserWarning)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

REPO_ROOT = Path(__file__).parent.parent
WIKI_ROOT = REPO_ROOT / "wiki"
EMBEDDINGS_PATH = REPO_ROOT / "meta" / "embeddings.json"
MODEL_NAME = "paraphrase-multilingual-mpnet-base-v2"
DEFAULT_TOP_K = 8


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


def clean_for_embedding(title: str, body: str) -> str:
    """Produce clean text for the embedding model: title + stripped body."""
    body = re.sub(r"\[\[(?:[^\]|]+\|)?([^\]]+)\]\]", r"\1", body)
    body = re.sub(r"[#*_`>]", " ", body)
    body = re.sub(r"^[-•]\s+", "", body, flags=re.MULTILINE)
    body = re.sub(r"\s+", " ", body).strip()
    return f"{title}\n\n{body}"


def load_wiki_pages() -> list[dict]:
    pages = []
    for md_file in WIKI_ROOT.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        title = fm.get("title", "").strip()
        if not title:
            continue
        body = get_body(content)
        pages.append({
            "title": title,
            "file": str(md_file.relative_to(REPO_ROOT)),
            "type": fm.get("type", ""),
            "updated": fm.get("updated", ""),
            "text": clean_for_embedding(title, body),
        })
    return pages


def load_embeddings() -> dict:
    if EMBEDDINGS_PATH.exists():
        return json.loads(EMBEDDINGS_PATH.read_text(encoding="utf-8"))
    return {"model": MODEL_NAME, "generated": date.today().isoformat(), "pages": {}}


def save_embeddings(store: dict):
    store["generated"] = date.today().isoformat()
    EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    EMBEDDINGS_PATH.write_text(
        json.dumps(store, separators=(",", ":"), ensure_ascii=False),
        encoding="utf-8",
    )


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def load_model():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("ERROR: sentence-transformers not installed.")
        print("Run: pip install -r tools/requirements.txt")
        sys.exit(1)
    print(f"Loading model {MODEL_NAME}…", flush=True)
    return SentenceTransformer(MODEL_NAME)


def embed_pages(rebuild: bool = False):
    pages = load_wiki_pages()
    store = load_embeddings()
    existing = store.get("pages", {})

    if rebuild:
        to_embed = pages
        print(f"Rebuild mode — embedding all {len(pages)} pages…")
    else:
        to_embed = [
            p for p in pages
            if p["title"] not in existing
            or existing[p["title"]].get("updated", "") != p["updated"]
        ]
        skipped = len(pages) - len(to_embed)
        if not to_embed:
            print(f"All {len(pages)} pages up-to-date, nothing to embed.")
            return
        print(f"Embedding {len(to_embed)} page(s) ({skipped} unchanged, skipping)…")

    model = load_model()
    texts = [p["text"] for p in to_embed]
    vectors = model.encode(texts, show_progress_bar=True, batch_size=32)

    for page, vector in zip(to_embed, vectors):
        existing[page["title"]] = {
            "file": page["file"],
            "type": page["type"],
            "updated": page["updated"],
            "vector": vector.tolist(),
        }

    current_titles = {p["title"] for p in pages}
    stale = [t for t in list(existing.keys()) if t not in current_titles]
    for t in stale:
        del existing[t]
        print(f"  Removed stale entry: {t}")

    store["pages"] = existing
    store["model"] = MODEL_NAME
    save_embeddings(store)

    size_kb = EMBEDDINGS_PATH.stat().st_size / 1024
    print(f"Done — {len(existing)} pages embedded, {size_kb:.0f} KB written to {EMBEDDINGS_PATH}")


def query(query_text: str, top_k: int = DEFAULT_TOP_K) -> list[dict]:
    """Return top_k most semantically similar wiki pages to query_text."""
    store = load_embeddings()
    if not store.get("pages"):
        print("No embeddings found. Run: python tools/embed-wiki.py")
        sys.exit(1)

    model = load_model()
    query_vector = model.encode([query_text])[0].tolist()

    scored = []
    for title, data in store["pages"].items():
        score = cosine_similarity(query_vector, data["vector"])
        scored.append({"title": title, "file": data["file"], "type": data["type"], "score": round(score, 4)})

    scored.sort(key=lambda x: -x["score"])
    return scored[:top_k]


def main():
    parser = argparse.ArgumentParser(description="Semantic embeddings for the second-brain wiki.")
    parser.add_argument("--rebuild", action="store_true", help="Force re-embed all pages")
    parser.add_argument("--query", "-q", metavar="TEXT", help="Find most relevant pages for a query")
    parser.add_argument("--top", "-k", type=int, default=DEFAULT_TOP_K, help=f"Number of results (default: {DEFAULT_TOP_K})")
    parser.add_argument("--json", action="store_true", help="Output query results as JSON")
    args = parser.parse_args()

    if args.query:
        results = query(args.query, top_k=args.top)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\nTop {args.top} pages for: \"{args.query}\"\n")
            for i, r in enumerate(results, 1):
                print(f"  {i:2}. [{r['score']:.3f}]  {r['title']}")
                print(f"       {r['file']}")
    else:
        embed_pages(rebuild=args.rebuild)


if __name__ == "__main__":
    main()
