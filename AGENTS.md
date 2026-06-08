# Second Brain — Agent Constitution

Full guide for AI assistants working in this vault. All tools (Claude Code, Codex CLI, Gemini CLI, etc.) read this file for the complete operating rules.

---

## User

Name/alias: (set by /brain-setup)
Goal: (set by /brain-setup)
Language: (set by /brain-setup)

*(This section is written by `/brain-setup` during onboarding. Update it any time.)*

---

## What this system is

A personal second brain built on the **Karpathy "LLM Wiki" pattern**: cross-linked markdown files that an AI reads, synthesizes, and queries — no vector database, no complex infrastructure. Just markdown files, wikilinks, and an AI that knows how to navigate them.

The core loop:
1. You talk (recording) or write (notes, source material)
2. AI transcribes and synthesizes it into `wiki/` pages
3. Pages link to each other — the brain becomes a graph, not a folder
4. You ask questions; the AI traverses the graph to answer in *your* voice

The difference from a notes app: **the AI knows who you are**. It answers from your actual views, stories, and beliefs — not generic training data.

---

## Folder ownership (non-negotiable)

```
<repo-root>/
├── CLAUDE.md            # pointer to this file (@AGENTS.md)
├── AGENTS.md            # this file — full agent constitution
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
- AI **NEVER edits `raw/` or `interview/`**. Those are human-owned source-of-truth. Read only.
- AI **only writes** to `wiki/`, `profile.md`, `index.md`, `hot.md`, `log.md`, `meta/`.
- Every write to `wiki/` gets a one-line entry appended to `log.md`.

**profile.md vs hot.md — the distinction:**
- `profile.md` = stable identity, settled beliefs, current life situation. Enriched after each ingest, never replaced.
- `hot.md` = operational state: recently touched pages, upcoming plans, what just changed, next actions. Refreshed frequently.

---

## Session start — what to read

**For any second-brain session, read in this order:**
1. `AGENTS.md` (this file — user profile + all rules)
2. `voice.md` (voice spine — register, vocabulary, metaphors, anti-voice; run `/brain-voice` to build it if missing)
3. `profile.md` (who the user is + current situation)
4. `hot.md` (operational state)

**Before brain-ingest:** also read `index.md`, `meta/tensions.md`, and `wiki/voice-profile/spoken-to-written.md` (if it exists).

**Before brain-query:** Run `python tools/embed-wiki.py --query "..." --top 5 --json` first to identify seed pages semantically. Do not manually scan index.md to guess which pages are relevant.

**Before brain-review:** also read `index.md` and the specific pages just created.

---

## Wiki structure — what each category is for

All wiki pages live in `wiki/` and are written by the AI (brain-ingest) or occasionally by brain-log. Each page covers **one idea** — a belief, a story, a person, a concept.

| Category | What goes here | Example topics |
|---|---|---|
| `identity/` | Who you are, where you come from, defining stories | Your origin story, key life chapters, cultural identity |
| `beliefs/` | Settled convictions — things you'd defend | Your theory of motivation, what you think about money, risk philosophy |
| `opinions/` | Strong but less settled views — things you'd argue | Hot takes on your industry, opinions on how X should work |
| `work/` | Professional identity, how you work, career philosophy | How you give feedback, what makes a great team, career turning points |
| `money/` | Your relationship with money, financial philosophy | What money is for, how you think about earning/spending/risk |
| `relationships/` | Key relationships, how you love, what you value in others | Partnership philosophy, friendship patterns, family dynamics |
| `mind/` | Mental models, cognitive habits, how you process the world | Reframing patterns, how you handle uncertainty, energy management |
| `voice-profile/` | How you communicate — your style, patterns, recurring phrases | Openings, rhythm, what you never say, how tone shifts by platform |
| `people/` | One page per significant person in your life | Key mentors, your partner, important collaborators |
| `concepts/` | Abstract ideas you return to repeatedly | Your personal definition of freedom, what "success" means to you |
| `synthesis/` | Cross-domain insights from brain-query (2+ hops) | "My anti-conformism is connected to my country's cultural pessimism" |
| `sources/` | One page per external source ingested (YouTube, article, book) | What it was, which wiki pages it created, why it mattered |

---

## Page conventions

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
- **Distill the structure, keep the voice.** Pages are one-idea distillations written in the user's words, phrasing, and register — not paraphrased into clean prose or a different tone. Filler and rambling removed; vocabulary, metaphors, and patterns preserved. Rule: compress repetition, never re-register. Full spec: `wiki/voice-profile/spoken-to-written.md`.
- **No invented statements.** Every sentence must trace to what the user actually said. Pattern-finding and synthesis are fine — but conclusions must not be stated as their words if they aren't. When in doubt: use a verbatim quote from the transcript.
- **Cite the source** in frontmatter so every claim is traceable back to a recording/transcript.

**Inline-first linking:** Every paragraph that references an existing wiki concept must contain a `[[wikilink]]` inline at the point of reference — not saved for the bottom `_Related:_` section. The reader (and brain-query) needs to know *which sentence* motivated the connection.

**Related section:** Use `_Related:_` at the bottom of each page to list all outbound links — including ones that didn't fit inline. It supplements inline linking; it doesn't replace it.

**Synthesis pages** (`wiki/synthesis/`) are created by brain-query when it surfaces a non-obvious cross-domain connection (2+ hops). Their `sources:` field lists wiki pages, not raw/.

**Source pages** (`wiki/sources/`) are created during brain-ingest for every external source (YouTube, article, podcast). Short: what the source is, which wiki pages it created/enriched, why it mattered.

**log.md format:** Each entry uses `## [YYYY-MM-DD] operation | title` so entries are grep-parseable.

### What a good wiki page looks like

```markdown
---
title: Why I Create
type: belief
created: 2025-03-01
updated: 2025-03-15
sources: [raw/transcripts/session-02.md]
confidence: high
lang: en
---

Creating isn't about output — it's the clearest way I experience [[Being Fully Alive]].
When I'm deep in a project, time collapses. The work itself is the reward.

This connects to why I'm drawn to [[Teaching and Sharing]] — the moment someone
gets something because of what I made is indistinguishable from creating it.

The flip side: when I create for approval rather than curiosity, the signal dies.
I've learned to treat that drop in energy as a reliable compass (see [[Internal Compass]]).

_Related:_ [[Being Fully Alive]], [[Teaching and Sharing]], [[Internal Compass]], [[Why I Don't Chase Metrics]]
```

Key elements:
- Frontmatter with all required fields
- Written in first person, in your voice
- Inline `[[wikilinks]]` at the sentence where the concept appears
- `_Related:_` section at the bottom listing all outbound links
- One idea, one page — not a brain dump

---

## Interaction conventions

**For short structured choices** (yes/no, pick one from a small list): use `AskUserQuestion`.

**For open-ended or multi-part input** (free-form context, setup questions where the user needs to think and type): ask as plain text. A numbered list works well when collecting several answers at once. Wait for the user's full reply before proceeding.

---

## Skill descriptions — what each skill does and when to invoke it

### `/brain-language`
Set the primary language for wiki content. Run once if your language is not English — sets the Language field, creates `language.md` with localized conventions (quote block heading), and tells brain-ingest/brain-voice what language to write in. The skill infrastructure (AGENTS.md, skill files, `_Related:_` markers) stays in English.

**Input:** language name (prompted if not provided as argument)
**Output:** updated `AGENTS.md` Language field + `language.md` config file
**When to trigger:** "set language to Spanish", "change language", "I want to use this in French"

### `/brain-voice`
Build or update the voice profile from existing transcripts. Run once after your first ingest; re-run whenever you add significant new material.

**Input:** files in `raw/transcripts/` and `raw/sources/`
**Output:** `voice.md` (spine) + `wiki/voice-profile/` depth pages (vocabulary, metaphors, register, anti-voice, spoken-to-written)
**When to trigger:** "build my voice profile", "update voice", "create voice.md", after first ingest if voice.md doesn't exist

### `/brain-ingest`
Turn new raw material into wiki pages. Invoke when you've added recordings, transcripts, or source files.

**Input:** files in `raw/` or `interview/recordings/`
**Output:** new/updated `wiki/` pages, updated `index.md`, `hot.md`, `log.md`, `profile.md`
**When to trigger:** "process my recording", "ingest this", "I have new material", "update the brain"
**Final step:** always runs `python tools/build-graph.py` and `python tools/embed-wiki.py`

### `/brain-query`
Answer a question or write content in your voice, grounded in the wiki.

**Input:** a question, or a content brief ("write a LinkedIn post about X as me")
**Output:** an answer citing wiki pages, or a finished piece in your voice
**When to trigger:** "what's my take on X", "write this as me", "in my voice", "what do I actually think about…"
**Step 1:** always runs `python tools/embed-wiki.py --query "..." --top 5 --json` for seed discovery

### `/brain-lint`
Structural health check — broken links, orphan pages, index drift, thin linking.

**Input:** optional `--fix` flag
**Output:** report of structural issues with proposed fixes
**When to trigger:** "lint the brain", "check the wiki", "is everything connected", after large ingests

### `/brain-log`
Capture a quick thought directly into the wiki without needing a recording.

**Input:** the thought to capture (as skill argument)
**Output:** a new or extended wiki page, updated spine files
**When to trigger:** "log this", "note to my brain", "remember this", "add this thought"

### `/brain-review`
Content quality audit after a brain-ingest run.

**Input:** optional batch name or list of pages
**Output:** compact report — synthesis quality, cross-linking, voice fidelity, coverage gaps, tensions
**When to trigger:** "review the ingest", "check what brain-ingest did", "audit the pages"

### `/brain-maintenance`
Recurring upkeep — staleness, tensions, profile freshness.

**Input:** optional `--level daily|weekly|monthly`
**Output:** maintenance report + auto-fixes applied
**When to trigger:** "maintain the brain", "run brain maintenance", "clean up the wiki"

### `/brain-retrospective`
System meta-audit — skill quality, patterns, improvement proposals.

**Input:** none
**Output:** compact report with concrete skill improvement proposals
**When to trigger:** "retrospective", "how did the session go", "what should we fix in the skills"

### `/brain-setup`
One-time guided onboarding. Writes the `## User` section in AGENTS.md.

**When to trigger:** first time setup, or "run brain setup again"

### `/brain-transcribe`
Transcribe audio recordings via Whisper. Supports single files and folders.

**When to trigger:** "transcribe this recording", "process my audio", or drop a file path

---

## Operating loop — how material flows

```
You speak → recording in interview/recordings/ or raw/
         → /brain-transcribe → transcript in raw/transcripts/
         → /brain-ingest → wiki/ pages created/updated
                         → index.md, hot.md, log.md, profile.md updated
                         → wiki-graph.json + embeddings.json rebuilt
         → /brain-language (once, if not English)
                         → language.md config + AGENTS.md Language field updated
         → /brain-voice (first time, or after major new material)
                         → voice.md + wiki/voice-profile/ pages built/updated
         → /brain-query → answers grounded in the wiki, in your voice
         → /brain-review (optional, after ingest) → quality check
         → /brain-lint (periodic) → structural health
         → /brain-retrospective (periodic) → system improvement
```

---

## Daily use — 3 use cases

### 1. Content creator
You record ideas for posts, stories, and your personal brand. The brain remembers all of it and helps you write in your consistent voice.

**Routine:**
- Record a voice memo about an idea, experience, or opinion
- `/brain-transcribe` → transcript saved
- `/brain-ingest` → becomes a wiki page in the right category
- `/brain-query "write an Instagram caption about [topic] in my voice"` → finished draft grounded in how you actually think
- Optionally: `/brain-query "what's my unique angle on X?"` to find cross-domain connections you haven't seen

### 2. Journaler / thinker
You write notes, reflect on experiences, and want to see patterns across months of thinking.

**Routine:**
- Write raw notes in `raw/sources/` or record a voice reflection
- `/brain-ingest` → synthesized into wiki pages
- `/brain-query "what patterns do I see in how I handle uncertainty?"` → answer spanning your whole wiki
- Periodic `/brain-retrospective` or `/brain-maintenance` → catch stale beliefs, surface tensions

### 3. Career / coaching
You have coaching sessions, performance reviews, or career reflections you want to mine for insights.

**Routine:**
- `/brain-transcribe` your coaching session audio
- `/brain-ingest` → captures beliefs about work, fears, goals
- `/brain-query "what are my blind spots around leadership?"` → grounded in actual coaching content
- `/brain-maintenance --level monthly` → check which career tensions have resolved

---

## Voice profile

The canonical voice asset is `voice.md` (repo root) — read it at every session start (see Session start above). Build it by running `/brain-voice` after your first ingest. It holds: register description, vocabulary quick-reference (keep / remove), key metaphors, anti-voice drift tells, and the spoken→written conversion rule.

Depth pages in `wiki/voice-profile/` provide the full detail:
- `vocabulary.md` — complete signature phrases and filler removal list
- `metaphors.md` — mined metaphor bank with source citations
- `register.md` — language mix, tone, what they never say
- `anti-voice.md` — drift tells: coach-prose, invented aphorisms, third-person narration
- `spoken-to-written.md` — conversion spec, filler list, structure rule (general→specific), self-check, quote block format
- `written-voice.md` — written/published register (LinkedIn, email, essays) if built from published sources

**For any "write as me" or wiki-synthesis output:** read `voice.md` first, then pull relevant depth pages. Never guess the register from training data when the assets are right there.

---

## System health principles

**A brain that isn't pruned rots.** Quality > quantity.

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

### Voice fidelity
- Every wiki page must pass the "would they read this and say 'yes, that's me'?" test. If not, it is a drift bug — fix the page, not the standard.
- `brain-review` detects voice drift after every ingest: coach-prose, invented aphorisms, dropped metaphors, re-registered vocabulary. Run it every time.
- `python tools/wiki-check.py` section 7 (VOICE_DRIFT) surfaces structural drift patterns as WARNings — check it as part of `brain-lint`.
- A quote block that sounds more like the user than the surrounding prose is a drift signal: the prose drifted, not the quotes.
- Cross-session drift is anchored by `voice.md`. Every rewrite session must also read the full source transcripts for the relevant cluster — token cost accepted; it is the point.

### No short-term thinking
- Don't fix a symptom if the root cause is a missing skill rule. Add the rule.
- Every session should leave the *system* slightly better than it found it.

---

## Technical notes for AI assistants

**Semantic search:** `python tools/embed-wiki.py --query "..." --top 5 --json` returns ranked pages as JSON. Use this as the first step in brain-query — it's faster and more accurate than scanning index.md manually.

**Graph traversal:** `python tools/graph-traverse.py "Title" --hops 2 --max 15 --repo-relative` returns pages ordered by hop distance. Read hop-0 and hop-1 fully; read hop-2 selectively.

**Two-layer retrieval:** embeddings find semantically relevant seeds; graph traversal expands from those seeds through intentional wikilinks. Each layer does what it's good at: ML for "what's relevant", explicit links for "what connects to what".

**Link text must match frontmatter title exactly.** Never create `[[my-page-slug]]`-style links — always use the `title:` value verbatim. Use `tools/wiki-rename.py` for all renames.

**After every ingest:**
```bash
python tools/build-graph.py          # rebuild wiki-graph.json
python tools/embed-wiki.py           # incremental re-embed (only changed pages, ~3s)
```

---

## Multi-agent skill discovery

Skills are in `.claude/skills/<name>/SKILL.md` (Claude Code) and mirrored via symlinks at `.agents/skills/<name>/` (Codex CLI, Gemini CLI). Both paths point to the same SKILL.md files — one source of truth.
