# Second Brain — Constitution

This file is read by Claude Code (and other AI assistants via AGENTS.md) at the start of every session. It defines who the user is and how this vault is structured.

> Full system documentation — wiki structure, skill descriptions, operating loop, and daily use guide — lives in `AGENTS.md`. Skills reference it for deep context.

---

## User

Name/alias: (set by /brain-setup)
Goal: (set by /brain-setup)
Language: (set by /brain-setup)

*(This section is written by `/brain-setup` during onboarding. Update it any time.)*

---

## 1. Folder ownership (non-negotiable)

```
<repo-root>/
├── CLAUDE.md            # this file — constitution + user profile
├── AGENTS.md            # full agent constitution (wiki structure, skills, workflows)
├── profile.md           # stable identity + current situation (AI maintains)
├── index.md             # table of contents of every wiki page (AI maintains)
├── hot.md               # ~500-word recency cache: recent changes, upcoming plans
├── log.md               # append-only audit trail of every operation
├── meta/
│   ├── tensions.md      # open contradictions and unresolved questions
│   ├── wiki-graph.json  # pre-built link map — rebuilt on every ingest
│   └── embeddings.json  # semantic vectors (gitignored, rebuilt incrementally)
├── interview/           # HUMAN-OWNED — questions + recordings
├── raw/                 # HUMAN-OWNED — inputs Claude reads but NEVER edits
│   ├── transcripts/     # Whisper output from recordings
│   └── sources/         # pasted text, web clippings, PDFs, etc.
└── wiki/                # AI-OWNED — synthesized, cross-linked pages
    ├── identity/         beliefs/         opinions/
    ├── work/             money/           relationships/
    ├── mind/             voice-profile/   people/
    ├── concepts/         synthesis/       sources/
```

**Rules:**
- Claude **NEVER edits `raw/` or `interview/`**. Those are human-owned source-of-truth. Read only.
- Claude **only writes** to `wiki/`, `profile.md`, `index.md`, `hot.md`, `log.md`, `meta/`.
- Every write to `wiki/` gets a one-line entry appended to `log.md`.

**profile.md vs hot.md — the distinction:**
- `profile.md` = stable identity, settled beliefs, current life situation. Enriched after each ingest, never replaced.
- `hot.md` = operational state: recently touched pages, upcoming plans, what just changed, next actions. Refreshed frequently.

---

## 1b. Session start — what to read

**For any second-brain session, read in this order:**
1. `CLAUDE.md` (this file — user profile + folder rules)
2. `profile.md` (who the user is + current situation)
3. `hot.md` (operational state)

**Before brain-ingest:** also read `index.md` and `meta/tensions.md`.

**Before brain-query:** Run `python tools/embed-wiki.py --query "..." --top 5 --json` first to identify seed pages semantically. Do not manually scan index.md to guess which pages are relevant.

**Before brain-review:** also read `index.md` and the specific pages just created.

---

## 2. Page conventions

Every wiki page is a markdown file with frontmatter:

```yaml
---
title: <Human readable title>
type: identity | belief | opinion | work | venture | money | relationship | mind | voice | person | concept | synthesis | source
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [raw/transcripts/session-01.md]
confidence: high | medium | low
lang: en | pl | mixed | <your language code>
---
```

- **One idea per page.** A page is a belief, a story, a person, a concept — not a dump.
- **Title is the link target.** Pages reference each other with `[[Title]]`. Link liberally.
- **Synthesize, don't transcribe.** Pages are distilled in the user's own words and meaning.
- **Cite the source** in frontmatter so every claim is traceable back to a recording/transcript.

**Inline-first linking:** Every paragraph that references an existing wiki concept must contain a `[[wikilink]]` inline at the point of reference — not saved for the bottom `_Related:_` section. The reader (and brain-query) needs to know *which sentence* motivated the connection.

**Related section:** Use `_Related:_` at the bottom of each page to list all outbound links — including ones that didn't fit inline. It supplements inline linking; it doesn't replace it.

**Synthesis pages** (`wiki/synthesis/`) are created by brain-query when it surfaces a non-obvious cross-domain connection (2+ hops). Their `sources:` field lists wiki pages, not raw/.

**Source pages** (`wiki/sources/`) are created during brain-ingest for every external source (YouTube, article, podcast). Short: what the source is, which wiki pages it created/enriched, why it mattered.

**log.md format:** Each entry uses `## [YYYY-MM-DD] operation | title` so entries are grep-parseable.

---

## 3. Interaction conventions

**For short structured choices** (yes/no, pick one from a small list): use `AskUserQuestion`.

**For open-ended or multi-part input** (free-form context, setup questions where the user needs to think and type): ask as plain text. A numbered list works well when collecting several answers at once. Wait for the user's full reply before proceeding.

---

## 4. The operating loop (skills)

- **brain-ingest** — turn new `raw/` files or interview transcripts into `wiki/` pages
- **brain-query** — answer a question or generate content in the user's voice, grounded in the wiki
- **brain-lint** — structural health check: broken links, orphans, index drift, thin pages
- **brain-log** — capture a quick thought directly into the wiki without a raw source
- **brain-review** — content quality audit after a brain-ingest run
- **brain-maintenance** — recurring upkeep: staleness, tensions, profile refresh
- **brain-retrospective** — system meta-audit: skill quality, patterns, proposals for improvement
- **brain-setup** — one-time guided onboarding (writes this `## User` section)
- **brain-transcribe** — transcribe audio recordings via Whisper with good UX

---

## 5. Voice profile

*(This section is populated by brain-ingest after interview answers are processed. The voice profile grows from wiki/voice-profile/ pages. The AI should read those pages rather than relying on a static block here.)*

When writing content in the user's voice, always read:
1. `wiki/voice-profile/` — all pages in this folder define tone, style, and patterns
2. The relevant topical pages for the content being written

---

## 6. System health principles

### Reliability
- A `[[link]]` must always resolve. Broken link = silent data loss for brain-query.
- **Renames always use `tools/wiki-rename.py`** — never manual find-and-replace.
- Structural checks run via `brain-lint` after every non-trivial ingest.

### Efficiency
- Don't read 75+ files to answer a structural or semantic question. Use pre-computed tooling:
  - **Structural checks** → `python tools/wiki-check.py`
  - **Navigation map** → `meta/wiki-graph.json` (rebuilt after each ingest via `python tools/build-graph.py`)
  - **Semantic search** → `python tools/embed-wiki.py --query "..." --top N`
- Read only what's needed: frontmatter + `_Related:_` lines for structure; full pages for content reasoning.

### Maintainability
- When a skill rule is added, the backlog of existing pages not meeting the standard is expected. Surface via brain-lint, address incrementally.
- Every skill change should ask: "what does this break in the existing wiki?"

### Consistency
- The same standard applies every run.
- `brain-lint` is the truth-teller. `brain-retrospective` closes the loop.

### Scalability
- One idea per page is the scalability invariant.
- The link graph is the index. Don't rely on folder structure for navigation.
- At ~150 pages, revisit embedding tuning: consider increasing `--top` in brain-query.

### No short-term thinking
- Don't fix a symptom if the root cause is a missing skill rule. Add the rule.
- Every session should leave the *system* slightly better than it found it.
