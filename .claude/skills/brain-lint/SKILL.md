---
name: brain-lint
description: Structural health-check of the user's personal second brain — finds broken [[links]], orphan pages, index drift, thin-linked pages (declared connections without inline embeds), and stale or missing frontmatter. Use when the user says "lint the brain", "check my second brain", "is the wiki healthy", "clean up the brain", or after a large ingest. Reports findings by default; add --fix to apply repairs. Trigger when the brain's structural integrity is in question. For content quality, voice, and contradictions, use brain-review instead.
argument-hint: [--fix to apply repairs]
allowed-tools: Read, Glob, Grep, Edit, Bash
---

# Brain Lint

Keep the second brain structurally sound. This is a **structural** tool — it checks links, coverage, and formatting, not content quality or contradictions (that's `brain-review`'s job). Read-and-report by default; only change content when `$ARGUMENTS` contains `--fix`.

**Always read `AGENTS.md` first** for page conventions and structure.

## Step 1 — run the checker

```bash
python tools/wiki-check.py
```

This script reads all wiki pages, builds the link graph, and prints a structured report covering all 7 checks. Read the output — do not re-scan files manually. The script is the authoritative source; Claude's job is to interpret the findings and propose fixes.

## Step 2 — interpret the report

The 6 checks, in priority order:

1. **BROKEN_LINKS** — `[[Title]]` references with no matching page. Distinguish genuine breakage from intentional to-write markers (look for `_(to write)_` near the link).
2. **ORPHANS** — pages with 0 inbound links. Content orphans need something linking to them. Source orphans are systemic (wiki pages don't back-link to source pages) — flag as known pattern, not urgent.
3. **INDEX_DRIFT** — pages on disk missing from `index.md`, or `index.md` entries with no file. Both directions are errors.
4. **THIN_LINKS** — pages with 3+ `_Related:_` entries but 0 inline `[[links]]` in the body. The connections exist on paper but aren't wired into the text — `brain-query` can't traverse them. Flag as "inline enrichment candidates."
5. **LOW_INLINE_DENSITY** — recently updated pages with <3 inline links, split by severity:
   - `[ERROR]` — 0 inline links. `brain-query` has nothing to traverse from this page. Fix immediately.
   - `[WARN]` — 1–2 inline links. Sparse but not empty — informational, address in bulk enrichment passes, not urgently.
6. **FRONTMATTER_GAPS** — missing required frontmatter fields.
7. **VOICE_SMELLS** `[WARN]` — structural drift patterns detected in page bodies: coach-prose phrases, `X = Y` aphorism formulas, third-person narration about the user. These are warnings, not errors — investigate with `brain-review` to confirm and fix.

## Step 3 — output

Group findings by category, most important first. For each finding, state the file and a concrete proposed fix. Apply fixes only with `--fix`.

## Applying fixes (`--fix`)

**All link text changes must use `tools/wiki-rename.py`** — not Edit/sed. This ensures atomicity and logging.

```bash
# Fix a broken/mistyped link text across the vault:
python tools/wiki-rename.py fix-link "Wrong Link Text" "Correct Title"

# Rename a page and update all its links:
python tools/wiki-rename.py rename "Old Title" "New Title"

# Dry-run first to preview:
python tools/wiki-rename.py fix-link "Old" "New" --dry-run
```

For non-link fixes (missing frontmatter fields, index drift), use Edit/Write directly. After applying fixes, append a one-line summary to `log.md`.

## Scope boundary

Brain-lint does **not** check: synthesis quality, voice fidelity, coverage gaps, or contradictions between pages. Those require reading full content in context — that's `brain-review`. If a contradiction is obvious from metadata (e.g. two pages with the same title), flag it; otherwise defer to `brain-review`.

## Why it matters

Structural rot is silent. A broken link means `brain-query` silently drops a connection it would have followed. An orphan page means an insight exists but nothing leads to it. Thin links mean the graph exists on paper but not in practice — `brain-query` traverses inline links, not just `_Related:_` lists.
