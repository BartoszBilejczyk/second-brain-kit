---
name: brain-sleep
description: Deep, infrequent memory-consolidation pass over the user's second-brain wiki — compresses pages bloated by repeated brain-ingest enrichment, sharpens near-duplicate pages, and proposes synthesis pages. Invoke when the user says "let the brain sleep on this", "compress the wiki", "run brain sleep", or "deep consolidation". Not for routine upkeep (use brain-consolidate) and not for voice/contradiction checks (use brain-review) — this is the slow, judgment-heavy pass, not the nightly one. Report-only: every proposal needs explicit confirmation before anything is written.
argument-hint: [optional page or folder to focus the pass on]
allowed-tools: Read, Glob, Grep, Edit, Bash
---

# Brain Sleep

`brain-consolidate` is the nightly pass: cheap, mechanical, link- and frontmatter-level, runs in minutes. This skill is the other kind of sleep — the slow one that actually reorganizes what's stored. It requires reading full page bodies, so it's expensive and infrequent (monthly or on-demand), not part of the routine cycle.

**Loosely modeled on two real sleep mechanisms** (analogy, not literal mechanism — every step below still ends in a proposal the user confirms, nothing here is autonomous):
- **Synaptic downscaling** — sleep proportionally weakens over-potentiated connections built up during the day, keeping the signal but shrinking the footprint. Maps to: a page enriched across many `brain-ingest` sessions often ends up saying the same thing three times in three sessions' worth of paragraphs. Compress to the strongest version once.
- **Pattern separation** — sleep sharpens the boundary between similar-but-distinct memories so they stop blurring together. Maps to: two wiki pages that have semantically drifted toward saying the same thing need either a sharper distinguishing sentence or a merge.

**Explicitly not this skill's job:** voice/anti-voice drift, contradiction-finding (`brain-review`), broken links/orphans/frontmatter/staleness (`brain-consolidate`, `brain-lint`). If you find one of those in passing, note it in the report but don't act on it here — keeps the skills from overlapping.

**Hard rule:** never touch the verbatim quotes block (`## Quotes (verbatim)`, or the localized heading from `language.md`). Never merge two distinct quotes into one paraphrase. If in doubt about whether two sentences are "the same point twice" or "two related but distinct points," leave them — false negatives are cheap, false positives (deleting real signal) are not.

## Step 1 — Read

`AGENTS.md`, `voice.md`, `index.md`, and `language.md` if it exists (for the localized quote-heading value). If `$ARGUMENTS` names a page or folder, scope everything below to that; otherwise scan the whole wiki.

## Step 2 — Find compression candidates

A page is a candidate if it's been touched by 3+ separate `brain-ingest` sessions (check `grep "ENRICHED.*<page>" log.md`) or its body has grown past ~60 lines.

**Pre-filter with paragraph diffing before reading the whole page:** `python tools/embed-wiki.py --paragraph-diff <file> --json` embeds each paragraph in the page (excluding the verbatim quotes block — never touched, never diffed) and reports pairs scoring ≥0.80 (default; pass `--threshold` to adjust). This tells you *where* to look — it does not replace reading. Read the flagged paragraph pair(s) in context; if nothing clears the threshold but the page is still a candidate by the length/touch-count rule, read the full page (the tool only catches near-identical phrasing, not conceptually-same-point-different-words).

Look for: the same conclusion or fact restated in near-identical words across two different enrichment paragraphs (each one traceable to a different ingest date); redundant bullets covering the same ground; a quote that's now fully subsumed by a later, clearer quote saying the same thing (rare — flag, don't auto-drop).

For each finding, draft a before/after: what would be removed, what single strong version would remain, and confirm every remaining claim still traces to a source. Do not touch the verbatim quotes block.

**Scope discipline:** this read is for redundancy-detection only. Do not also audit voice fidelity, tone, or contradictions while the page happens to be open — that's `brain-review`'s job, not a bonus you do here because the file is already in context. If something voice- or contradiction-shaped catches your eye, note it in the report as an aside (like any other out-of-scope finding) and leave it for `brain-review`.

## Step 3 — Find pattern-separation candidates

Run `python tools/embed-wiki.py --query "<candidate page title/topic>" --top 5 --json` for each compression candidate (reuse the same call, no extra cost). If another page scores unusually high (rule of thumb: notably higher than the typical 0.4–0.55 range seen for legitimately related-but-distinct pages), read both pages and decide:
- **Genuinely distinct** — propose one sentence for each page making explicit what's unique to it.
- **True duplication** — propose a merge (via `tools/wiki-rename.py`, never manual find-and-replace), flagged for confirmation like any page deletion.

## Step 4 — Synthesis candidates

Look at pages added or enriched since the last `brain-sleep` run (`log.md`).

**Rank before reading, don't rely on chronological skim alone:** `python tools/embed-wiki.py --cluster-recent --since <last-sleep-date> --top-pairs 8 --json` computes pairwise similarity across every page touched since then and ranks the pairs — surfacing candidates a chronological log read could miss (e.g. pages from batches weeks apart that never appeared in the same session). Prioritize reading pairs where `type_a != type_b` (cross-domain) — same-type high-similarity pairs are usually restating one topic (a compression/pattern-separation signal, back to Step 2/3) rather than a novel cross-domain connection.

If 2-3 pages connect across domains in a way not yet captured by an existing `wiki/synthesis/` page, draft a proposed synthesis page (title, sources, core insight) for confirmation — don't create it yet.

## Step 5 — Report, then wait

```
## Brain Sleep — [date]

**Scope:** [whole wiki / page or folder from $ARGUMENTS]

**Compression candidates:** [page — what's redundant — proposed before/after, or "none"]

**Pattern-separation candidates:** [page pair — similarity signal — distinct/merge recommendation, or "none"]

**Synthesis candidates:** [proposed title + the 2-3 source pages + core insight, or "none"]

**Needs your decision:** [everything above — nothing is applied yet]
```

Nothing gets written in this pass without explicit confirmation — not even the most trivial exact-duplicate-sentence case. This is the highest-risk skill in the system (it edits the user's actual words), so it stays conservative by design.

## After confirmation

Apply only what was confirmed. Merges go through `tools/wiki-rename.py`. Update `updated:` frontmatter on any touched page. Append one line per page to `log.md`. Rebuild navigation artefacts (`python tools/build-graph.py`, `python tools/embed-wiki.py`).
