---
name: brain-ingest
description: Ingest new raw material into the wiki vault — transcribes interview audio via Whisper, synthesizes it into cross-linked markdown pages, and updates the index, hot cache, and log. Use whenever the user drops a new .m4a answer in interview/recordings/, adds a file to raw/, or says things like "ingest", "process my recording", "add this to my second brain", "update the brain", or "I recorded another theme". Trigger aggressively on any new personal source material destined for the vault.
argument-hint: [optional path to a specific file/folder to ingest]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Brain Ingest

Turn new human-owned raw material into clean, cross-linked `wiki/` pages in the second brain. This is the step that makes the brain compound — every recording becomes durable, linked, reusable knowledge.

**Always read `CLAUDE.md` first.** It is the constitution: folder ownership, page conventions, the voice profile, and the user's domain context. Everything below assumes its rules (especially: never edit `raw/` or `interview/`; only write to `wiki/`, `profile.md`, `index.md`, `hot.md`, `log.md`).

## Steps

1. **Orient.** Read `profile.md` (who the user is + current situation), then `hot.md` (operational state), then `index.md` (existing pages) and `meta/tensions.md` (open questions). Build on what's there — don't duplicate.
2. **Surface state before proceeding.** After reading the spine files, briefly tell the user: what batches/pages already exist, which wiki sections are populated vs empty, any open tensions worth carrying into this batch. This gives them a chance to course-correct before new pages get written. Keep it to 5–8 lines — signal only, no padding.
3. **Find new material.** Look in `raw/` and `interview/recordings/`. If `$ARGUMENTS` names a specific file or folder, ingest only that; otherwise process everything not yet reflected in the wiki/log.
4. **Transcribe audio if needed.** For any `.m4a` without a matching transcript, prefer running `/brain-transcribe` first — it handles model selection and UX. Alternatively, run directly: `python tools/transcribe_audio.py <file> --language <lang> --output raw/transcripts/<stem>.md`. The raw transcript is a source — never hand-edit it afterwards.
5. **Synthesize, don't transcribe.** For each source, distill it into `wiki/` pages following the page conventions in the constitution: one idea per page (a belief, a story, a person, an opinion, a concept), written in the user's own words and meaning. Full frontmatter (title, type, created/updated, sources, confidence, lang). File into the correct `wiki/` subfolder. Note: `wiki/synthesis/` is reserved for cross-domain insights surfaced by `brain-query` — don't file ingest pages there.

   **For external sources** (YouTube, articles, podcasts — anything in `raw/sources/`): also create a `wiki/sources/<slug>.md` page. Keep it short: what the source is (1 sentence), which wiki pages it created/enriched (link list), and why it mattered to the user. Use `type: source`, `source_url:`, `source_type: youtube|article|podcast|book` in frontmatter — no `confidence:` field needed. Personal interview transcripts don't get source pages; those flow directly into identity/belief/etc. pages.
6. **Link aggressively.** Connect pages with `[[Title]]` links, *especially across domains* — this is where the brain's value lives (e.g. a money belief that connects to the no-kids choice that connects to a definition of freedom). Links to not-yet-written pages are valid to-write markers; leave them.

   **Inline-first:** Every paragraph that references an existing wiki concept must contain a `[[wikilink]]` inline at the point of reference — not saved for the bottom. If a sentence says "this is the same fear of rejection", link `[[Strach przed odmową]]` right there in that sentence. The reader (and `brain-query`) needs to know *which sentence* motivated the connection, not just that a connection exists.

   **Backlink obligation:** When a new page is created OR an existing page is enriched with new content, identify which *other* pages discuss the same concept and add the link there too (bidirectional). A page with 0 inbound wiki links is a smell — something is missing. Actively scan the surrounding wiki for pages where a sentence now deserves a link to the new content.

   The `_Related:_` section at the bottom of each page is a *complete-list supplement* — it lists every outbound link, including ones that didn't fit naturally inline. It does not substitute for inline linking; it follows it.
7. **Respect tension.** If a source contradicts an existing page, do not silently overwrite. Note the tension on the page and surface it in your report — contradictions are signal, not error.
8. **Update the spine.** Add new pages to `index.md` under their section, refresh `hot.md` (~500 words: current state, recently touched pages, anything notable), append a one-line entry per source to `log.md`, and enrich `profile.md` with anything new about the user's identity, situation, or beliefs that emerged from this batch. Profile.md is enriched, never replaced — add and refine, don't rewrite.
9. **Report back.** List pages created/updated, notable new cross-links, contradictions found, and any gap where a follow-up question or recording would meaningfully enrich the brain.

10. **Regenerate navigation artefacts.** After all wiki writes are done, run:
    ```bash
    python tools/build-graph.py          # rebuild wiki-graph.json (navigation layer)
    python tools/embed-wiki.py           # incremental — only re-embeds changed pages
    ```
    These are fast (< 5s for incremental runs). They keep `brain-query` accurate without manual maintenance. If any step fails, report the error but do not block the ingest — the wiki content is the primary output.

## Why it matters

A folder of transcripts is dead storage. The wiki is alive because it is synthesized and linked — that is what lets `brain-query` later write in the user's voice and reason across their whole life at once. Quality of synthesis here determines quality of every future output.
