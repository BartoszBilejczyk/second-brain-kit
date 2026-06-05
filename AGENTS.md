# Second Brain — Agent Constitution

Full guide for AI assistants working in this vault. Claude Code reads `CLAUDE.md` for the user profile and folder rules, then this file for deeper context on wiki structure, skill operations, and daily use patterns.

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

## Skill descriptions — what each skill does and when to invoke it

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
One-time guided onboarding. Writes the `## User` section in CLAUDE.md.

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

## Health principles

**A brain that isn't pruned rots.** Quality > quantity.

- One idea per page — pages that cover multiple ideas become unmaintainable
- Inline links are the traversal layer — if a sentence mentions a concept, link it there
- Every ingest should leave the graph denser, not just bigger
- Stale pages are fine if they hold settled beliefs; stale pages about "current situation" are not
- `brain-lint` surfaces problems; `brain-retrospective` finds their root cause; fixing the skill prevents recurrence

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
