---
name: brain-ingest
description: Ingest new raw material into the wiki vault — transcribes interview audio via Whisper, synthesizes it into cross-linked markdown pages, and updates the index, hot cache, and log. Use whenever the user drops a new .m4a answer in interview/recordings/, adds a file to raw/, or says things like "ingest", "process my recording", "add this to my second brain", "update the brain", or "I recorded another theme". Trigger aggressively on any new personal source material destined for the vault.
argument-hint: [optional path to a specific file/folder to ingest]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Brain Ingest

Turn new human-owned raw material into clean, cross-linked `wiki/` pages in the second brain. This is the step that makes the brain compound — every recording becomes durable, linked, reusable knowledge.

**Always read these files first, in order:**
1. `AGENTS.md` — the constitution: folder ownership, page conventions, the user's domain context
2. `voice.md` — voice spine: register, vocabulary, metaphors, anti-voice, conversion rule. **If voice.md doesn't exist yet:** note this after orientation and suggest running `/brain-voice` after this ingest to build it from the transcripts.
3. `wiki/voice-profile/spoken-to-written.md` — full conversion spec: structure rule (general→specific), filler list, quote block format, self-check. Skip if not yet created.
4. `language.md` — localized conventions (quote block heading, language code). If it exists, use its `quote_heading` value for the verbatim quotes section instead of the English default. If it doesn't exist, use `## Quotes (verbatim)`.

Everything below assumes these rules (especially: never edit `raw/` or `interview/`; only write to `wiki/`, `profile.md`, `index.md`, `hot-personal.md`, `hot-system.md`, `log.md`).

## Steps

1. **Orient.** Read `profile.md` (who the user is + current situation), then `hot-personal.md` (current human state) and `hot-system.md` (wiki state), then `index.md` (existing pages) and `meta/tensions.md` (open questions). Build on what's there — don't duplicate.
2. **Surface state before proceeding.** After reading the spine files, briefly tell the user: what batches/pages already exist, which wiki sections are populated vs empty, any open tensions worth carrying into this batch. This gives them a chance to course-correct before new pages get written. Keep it to 5–8 lines — signal only, no padding.
3. **Find new material.** Look in `raw/` and `interview/recordings/`. If `$ARGUMENTS` names a specific file or folder, ingest only that; otherwise process everything not yet reflected in the wiki/log.
4. **Transcribe audio if needed.** For any `.m4a` without a matching transcript, prefer running `/brain-transcribe` first — it handles model selection and UX. Alternatively, run directly: `python tools/transcribe_audio.py <file> --language <lang> --output raw/transcripts/<stem>.md`. The raw transcript is a source — never hand-edit it afterwards.
5. **Distill the structure, keep the voice.** For each source, distill it into `wiki/` pages following the page conventions in the constitution: one idea per page (a belief, a story, a person, an opinion, a concept), written in the user's own words, phrasing, and register. Full frontmatter (title, type, created/updated, sources, confidence, lang). File into the correct `wiki/` subfolder. Note: `wiki/synthesis/` is reserved for cross-domain insights surfaced by `brain-query` — don't file ingest pages there.

   **Structure: general → specific.** Each page must open with the most general statement (the core trait, belief, or principle), then context and tensions, then concrete examples, then anecdotes/illustrations last. The most recent event is not automatically the lead. Dates go deeper in the page, not in the opening paragraph.

   **All dates must include the year.** "March", "autumn", "last year" are meaningless in 5 years. Always write "March 2026", "autumn 2025", etc.

   **Self-check before saving any page:** Would the user read this and say "yes, that's me"? Does every claim trace to the cited source? Are any phrases from the anti-voice list (coach-prose, invented aphorisms, "X = Y" formulas)?

   **No invented statements:** Every sentence must trace to what the user actually said. Do NOT write: conclusions they didn't draw, literary flourishes they never said, vocabulary they don't use. Pattern-finding and synthesis are fine — but do not state a conclusion *as their words* if it isn't. When in doubt: replace the invented sentence with a verbatim quote from the transcript.

   **Third-person source rule:** Some transcripts are narrated externally — by a coach, therapist, interviewer, or another person — in third person ("they said X", "we see in them Y", "the client tends to..."). Flip ALL such content to first person before writing. The user's name/alias must never appear in a wiki page body — only in frontmatter `sources:` or log entries.

   **Quote block required:** Every full-voice page must include `## Quotes (verbatim)` near the bottom — 3–5 `>` quotes pulled verbatim from the raw transcript. Use `[...]` only to trim filler mid-quote. Never quote from a summary or a drifted wiki page. A page without a Quotes section is incomplete.

   **Few-shot examples — the voice drift pattern to avoid:**
   ```
   ❌ BAD: source said "I don't want to do things half-assed, I want quality"
   Wiki wrote: "This is the tension between perfectionism and pragmatism. Standards must be upheld."
   Why wrong: re-registered into analyst prose; user's actual words gone; "X and Y tension" is a phrase they never said.
   ✅ GOOD: "I don't want to do things half-assed. That's my standard and I'm not walking away from it."

   ❌ BAD: source used a vivid metaphor ("running a marathon at pace I'm not built for — no water, no gel — and the blisters are forming")
   Wiki wrote: "Delivered. At the cost of health."
   Why wrong: all texture of the metaphor dropped; manufactured staccato punch they never said.
   ✅ GOOD: "I started treating this like a marathon I'm running at pace I'm not built for — no water, no gel — and the blisters are forming."

   ❌ BAD: source described needing alone time and personal space
   Wiki wrote: "Not a flaw — a fact to understand." / "Space = freedom of thought." / "design life around yourself"
   Why wrong: none of these phrases appear in the transcript; coach/therapist register; "X = Y" formula they don't use for self-description.
   ✅ GOOD: "I need my own time and my own space. When I had my own room for the first time, I understood what it meant to have a place that's mine."
   ```

   **For external sources** (YouTube, articles, podcasts — anything in `raw/sources/`): also create a `wiki/sources/<slug>.md` page. Keep it short: what the source is (1 sentence), which wiki pages it created/enriched (link list), and why it mattered to the user. Use `type: source`, `source_url:`, `source_type: youtube|article|podcast|book` in frontmatter — no `confidence:` field needed. Personal interview transcripts don't get source pages; those flow directly into identity/belief/etc. pages.
6. **Link aggressively.** Connect pages with `[[Title]]` links, *especially across domains* — this is where the brain's value lives (e.g. a money belief that connects to the no-kids choice that connects to a definition of freedom). Links to not-yet-written pages are valid to-write markers; leave them.

   **Inline-first:** Every paragraph that references an existing wiki concept must contain a `[[wikilink]]` inline at the point of reference — not saved for the bottom. If a sentence says "this is the same fear of rejection", link `[[Fear of Rejection]]` right there in that sentence. The reader (and `brain-query`) needs to know *which sentence* motivated the connection, not just that a connection exists.

   **Backlink obligation:** When a new page is created OR an existing page is enriched with new content, identify which *other* pages discuss the same concept and add the link there too (bidirectional). A page with 0 inbound wiki links is a smell — something is missing. Actively scan the surrounding wiki for pages where a sentence now deserves a link to the new content.

   The `_Related:_` section at the bottom of each page is a *complete-list supplement* — it lists every outbound link, including ones that didn't fit naturally inline. It does not substitute for inline linking; it follows it.
7. **Respect tension.** If a source contradicts an existing page, do not silently overwrite. Note the tension on the page and surface it in your report — contradictions are signal, not error.
8. **Update the spine.** Add new pages to `index.md` under their section. Update `hot-system.md`: page count, last ingest date, recently changed pages, next recommended actions. Update `hot-personal.md` only if the material revealed a meaningful shift in the user's current state, emotional register, or active tensions — don't rewrite it on every ingest, only when something actually changed. Append a one-line entry per source to `log.md`. Enrich `profile.md` with anything new about the user's identity, situation, or beliefs — enriched, never replaced.
9. **Language check.** Before reporting back, proofread every page written in this session for the user's primary language (set in `AGENTS.md` → `## User` → Language): spelling, grammar, punctuation, word meaning. AI is not a native speaker in most languages — this step is mandatory, not optional. Fix issues directly in the files.
10. **Report back.** List pages created/updated, notable new cross-links, contradictions found, and any gap where a follow-up question or recording would meaningfully enrich the brain. If `voice.md` didn't exist at the start of this session, remind the user to run `/brain-voice` to build their voice profile from the material just ingested.

11. **Regenerate navigation artefacts.** After all wiki writes are done, run:
    ```bash
    python tools/build-graph.py          # rebuild wiki-graph.json (navigation layer)
    python tools/embed-wiki.py           # incremental — only re-embeds changed pages
    ```
    These are fast (< 5s for incremental runs). They keep `brain-query` accurate without manual maintenance. If any step fails, report the error but do not block the ingest — the wiki content is the primary output.

## Why it matters

A folder of transcripts is dead storage. The wiki is alive because it is synthesized and linked — that is what lets `brain-query` later write in the user's voice and reason across their whole life at once. Quality of synthesis here determines quality of every future output.
