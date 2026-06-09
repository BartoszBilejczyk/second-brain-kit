---
name: brain-log
description: Capture a quick thought, idea, opinion, or takeaway straight into the user's personal second brain without needing a raw source file. Use when the user says "log this", "note to my brain", "remember this in my second brain", "add this thought", or dumps a standalone idea they want saved and cross-linked for later. Trigger when a fleeting thought should become durable, linked knowledge.
argument-hint: <the thought to capture>
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Brain Log

Append a quick thought into the second brain — the low-friction path for ideas that arrive without a recording.

**Always read `AGENTS.md` first** for page conventions.

Thought: `$ARGUMENTS`

## Steps

1. **Place it.** Read `index.md`/`hot-system.md` and decide whether this extends an existing `wiki/` page or warrants a new one. Prefer extending when it genuinely belongs together.
2. **Write it** per the page conventions: frontmatter, one idea per page, in the user's own words. Set `sources: [brain-log <today>]` and an honest `confidence` (quick thoughts are often `low`/`medium`).
3. **Link it** with `[[Title]]` to related pages so it joins the graph rather than floating alone.
4. **Update the spine.** Add to `index.md` if new, refresh `hot-system.md` (add to recently changed), append a one-line entry to `log.md`.
5. **Report** what you captured and where.

## Why it matters

The best raw material is often a passing thought. Making capture frictionless — and immediately linked — is how the brain grows between recording sessions instead of only during them.
