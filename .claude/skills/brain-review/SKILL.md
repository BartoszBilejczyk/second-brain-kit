---
name: brain-review
description: Content quality audit of a brain-ingest run. Run this after /brain-ingest — catches synthesis problems before they compound. Always run this after /brain-ingest — it catches synthesis problems, weak cross-linking, voice drift, coverage gaps, and contradictions before they compound across batches. Trigger aggressively whenever the user says "review the ingest", "check what brain-ingest did", "audit the wiki pages", "did the ingest look good", "quality check", or after any batch ingest even without an explicit ask. For structural checks (broken links, orphans, index drift), use brain-lint instead.
argument-hint: [optional batch name, date, or list of pages to review]
allowed-tools: Read, Glob, Grep, Edit, Bash
---

# Brain Review

Compact quality audit of a brain-ingest run. The goal is to catch problems early — before bad pages compound across batches — and to surface what the ingest missed or got wrong.

**Scope:** brain-review owns content quality, voice, contradictions, and whether `brain-ingest` actually did its job. For structural integrity (broken links, orphan pages, index drift), run `brain-lint` separately — they're complementary, not redundant.

## Setup

Read in this order before reviewing anything:
1. `AGENTS.md` — page conventions and domain context
2. `voice.md` — voice spine (register, vocabulary, metaphors, anti-voice). Skip if not yet built — run `/brain-voice` to create it.
3. `wiki/voice-profile/anti-voice.md` — the full drift-tell list with examples. Skip if not yet built.
4. `hot.md` — what was just ingested and current state
5. `index.md` — full page inventory

If the user specifies which pages or batch to review, focus there. Otherwise review all pages added or modified in the most recent ingest (visible from `hot.md` "Recently touched pages" or `log.md`).

For each page being reviewed, read it. Also spot-check 1-2 source files (from `raw/transcripts/` or `raw/sources/`) to compare against what made it into the wiki.

## What to check

### 1. Synthesis quality
- Is each page one idea, or a topic dump? A page titled "Beliefs" covering 8 unrelated things is a dump.
- Is the content distilled in the owner's words, or does it read like a transcript excerpt? Quotes are fine; paraphrased summaries of everything the source said are not.
- Are claims traceable to a source in the frontmatter?

### 2. Cross-linking (inline-first)
- Are links embedded inline at the sentence where the concept appears — or only in `_Related:_` at the bottom? Inline is the standard; bottom-only is thin linking.
- Do links go both ways? If page A links to page B, does page B link back to A where it makes sense?
- Are there isolated pages — pages with few or no outgoing links? Isolation is a smell; everything connects to something.
- Are any links to pages that clearly should exist but don't (i.e., obvious gaps in the wiki)?

### 3. Voice fidelity

You already read `voice.md` and `anti-voice.md` in Setup. Apply them here. If they don't exist yet, use the generic checks below.

**Anti-voice patterns — immediate FAIL if found:**
- Coach/therapist register: "Not a flaw — a fact to understand", "design your life", "something to work through", "space for growth", "build self-awareness"
- Invented aphorisms: `X = Y` formulas for personal beliefs (e.g. "Space = freedom of thought"), manufactured staccato punch ("I am ambitious. I fight for myself.")
- Analyst reframe: "This is the tension between X and Y"
- Growth-mindset uplift: "every day I become better", "I fall but I get back up"
- Third-person narration: "they are someone who...", "the user tends to..." (should be first-person throughout)

**If `voice.md` exists:** also check against their specific anti-voice list and vocabulary inventory.

**Register check:**
- First-person throughout? (Third-person = drift)
- Signature vocabulary present where relevant? (Check `wiki/voice-profile/vocabulary.md` if it exists)
- Metaphors preserved when the transcript used them? (Check `wiki/voice-profile/metaphors.md` if it exists)

**Structure check:**
- Does each page open with the most general statement (the principle/trait), then expand to specifics? Or does it open with a specific date/event?
- Do all dates include the year? ("March", "autumn" without a year = flag)

**Quote block check:**
- Is `## Quotes (verbatim)` present on full-voice pages?
- Are quotes clearly pulled from raw transcripts — not paraphrased, not invented?
- If the quotes sound more like the user than the body prose: the body drifted — fix the prose, not the quotes.

**Language:**
- Does the language match the user's preferred language from the `## User` section in `AGENTS.md`?
- Is the language consistent with what's expected for this page type?

### 4. Coverage gaps
- Read the source(s) and identify 2-3 ideas that were significant in the recording but have no wiki page. Note them — they're candidates for the next batch or a follow-up.
- Flag anything that was over-split (one idea fragmented into too many pages) or under-split (one page covering things that should be separate).

### 5. Tensions and contradictions
- Did the ingest produce any belief or identity claims that conflict with existing pages? Note them.
- Are there tensions in the new pages themselves that weren't flagged in `meta/tensions.md`? If so, add them.

## Output format

Produce a single compact report. No padding, no recapping what you read. Signal-only.

```
## Brain Review — [batch/date]

**Synthesis:** [1-2 sentences on quality. Flag any pages that are topic dumps or transcript copies.]

**Cross-linking:** [What links well. Any isolated pages or obvious missing links.]

**Voice:** [Pass / issues found. Specific examples if issues.]

**Coverage gaps:** [2-3 ideas from source that didn't make it. One line each.]

**Tensions found:** [Any new tensions not yet in meta/tensions.md. Add them there if found.]

**Overall:** [One line verdict: ready for next batch / needs fixes before proceeding. List specific fixes if needed.]
```

If everything looks good, say so briefly. Don't invent problems.

After the report, if you found new tensions, append them to `meta/tensions.md` using the same format as existing entries.
