---
name: brain-voice
description: Build or update the user's voice profile — mines all transcripts and source files to create voice.md (the spine) and the wiki/voice-profile/ depth pages. Run this after your first brain-ingest, and re-run whenever you add significant new material. Use when the user says "build my voice profile", "update voice", "mine voice", "create voice.md", "update my voice profile", or after a successful first brain-ingest when voice.md doesn't exist yet.
argument-hint: [--update to update existing voice.md without full rebuild]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Brain Voice

Build or update the voice profile — the anchor that keeps every wiki page, brain-query output, and synthesized content sounding like the user rather than a generic AI summary.

**Why this matters:** Without a voice profile, brain-ingest produces factually correct pages in the wrong register — coach prose, analyst framing, invented aphorisms. With voice.md, the model has a concrete anchor: specific vocabulary to keep, specific fillers to drop, specific metaphors that are meaningful, specific phrases that are red flags.

## Pre-reads

Before mining, read:
1. `AGENTS.md` — constitution and folder rules
2. `profile.md` — who the user is (sets context for what to look for)

## What to mine

Scan all files in `raw/transcripts/` and `raw/sources/`. If `$ARGUMENTS` is `--update`, also read the current `voice.md` to preserve and extend rather than rebuild.

Look for:

**Vocabulary — keep:**
- Signature phrases they use repeatedly and meaningfully (not filler)
- Specific words that carry distinct meaning for them
- Profanity or casual language that is deliberate emphasis, not just habit
- Domain-specific vocabulary (finance, tech, art — whatever their field)

**Vocabulary — remove (fillers):**
- Discourse fillers: sounds, tics, false starts, self-corrections
- Interview-apparatus meta: "next question", "let me think", "sorry, I forgot where I was"
- Thinking-out-loud repetition (keep repetition-for-emphasis; drop repetition-for-thinking)
- Softeners that weaken every sentence when used constantly

**Metaphors:**
- Any vivid comparison they use — especially recurring ones
- Note what concept each metaphor expresses (it's their thinking in image form)
- Note the source transcript so the quote can be verified

**Register:**
- What language(s) they speak and code-switch between
- Tone: direct/indirect, formal/casual, vulnerable/guarded, certain/exploratory
- What they never say (coach phrases, growth-mindset clichés, aphorisms they didn't coin)

**Anti-voice drift tells:**
- Phrases that would appear if an AI re-registered their words into "clean prose"
- Third-person narration about themselves ("they tend to...", "the user is someone who...")
- `X = Y` aphorism formula for personal beliefs
- Coach/therapist openers ("Not a flaw — a fact to understand", "space for growth", "design your life")

**Written/published voice** (if `raw/sources/` contains published content like LinkedIn posts, essays, newsletters):
- How their register shifts from spoken → written
- Structural patterns (how they open, close, build a point)
- What stays the same (vocabulary, stance) vs. what changes (rhythm, punctuation)

## What to write

### voice.md (spine — always read at session start)

Write at the repo root. Short and fast to read — it's loaded every session.

Structure:
```markdown
---
title: Voice — [User name/alias]
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: voice-spine
note: ALWAYS READ AT SESSION START before any synthesis or "as me" output.
---

# Voice — [User name/alias]

This file is the spine. Every session that writes in their voice reads this first,
then reads the full source transcripts for the relevant cluster. Anchor, not shortcut.

## The core distinction

**Spoken voice** (transcripts, recordings) → drives wiki page bodies.
**Written/published voice** (LinkedIn, email, essays) → drives published output.
[Note if these are very similar or very different for this user.]

## Register

[2-4 sentences: language(s), tone, how they handle uncertainty, what they never do.]

## Vocabulary quick-reference

### Keep — signature phrases
[List of meaningful phrases/words, one per bullet. Brief note on what each means/does.]

### Keep — domain vocabulary
[Domain-specific terms they use authentically.]

### Remove — fillers
[List of filler words/phrases to strip. One per bullet.]

## Key metaphors

| Metaphor | What it expresses | Source |
|---|---|---|
[Table of recurring metaphors. Source = transcript filename or quote.]

## Anti-voice drift tells

Phrases that signal the AI drifted into the wrong register — FAIL if found:
- [Coach phrase 1]
- [Invented aphorism pattern: X = Y formulas for personal beliefs]
- [Third-person narration: "they tend to...", "[alias] believes..."]
- [Growth-mindset uplift they never said]

## Spoken → written conversion rule

Strip: [their specific filler list]
Keep: vocabulary, metaphors, stance, profanity (if meaningful)
Structure: general → specific (open with the core principle, not the anecdote)
Quote block: every full-voice page ends with `## Quotes (verbatim)` — 3–5 raw transcript quotes

## Written/published voice

[Only if published sources exist. Note how register shifts, structural patterns, what stays vs. changes.]
```

### wiki/voice-profile/ pages

Create or update these depth pages (they supplement voice.md with full detail):

- **`vocabulary.md`** — complete vocabulary inventory: keep list (with meanings), filler removal list
- **`metaphors.md`** — all mined metaphors with source citations and what each expresses
- **`register.md`** — language mix, tone, uncertainty handling, what they never say
- **`anti-voice.md`** — drift tells with examples: coach-prose, invented aphorisms, third-person, staccato punch
- **`spoken-to-written.md`** — conversion spec: structure rule (general→specific), full filler list, self-check, quote block format
- **`written-voice.md`** — written/published register (only if published sources exist in raw/sources/)

Each page: standard frontmatter (`type: voice`, no `confidence:` needed), first-person perspective where relevant, `_Related:_` footer linking to the other voice pages.

## Gate — show before saving

Before writing `voice.md`, show the user:
1. The draft `voice.md` (full content)
2. A one-line summary of each voice-profile page being created/updated

Ask: "Does this capture your voice accurately? Anything wrong, missing, or that needs adjusting?"

Apply their feedback. Then save all files.

## After saving

1. Add all new voice-profile pages to `index.md` under the `voice-profile/` section
2. Append to `log.md`: `## [YYYY-MM-DD] brain-voice | voice profile built from [N] transcripts`
3. Tell the user: "voice.md is ready. From now on, brain-ingest and brain-query will read it before every synthesis. Run /brain-ingest next to reprocess any existing transcripts with the new voice anchor."

## Re-run behavior (`--update`)

When `voice.md` already exists:
- Read the current version first
- Mine only new transcripts (files added since `voice.md`'s `updated` date)
- Merge findings: extend vocabulary lists, add new metaphors, refine anti-voice list
- Don't discard existing content — add and refine
- Show the diff (what changed) to the user before saving
