---
name: brain-query
description: Answer from — or write in the authentic voice of — the user's personal second brain in the wiki vault. Synthesizes the user's real views, stories, and tone from the wiki, with citations. Use whenever the user asks "what's my take on X", "what do I actually think about…", "write this LinkedIn post / Instagram reel / email / message in my voice", "how would I say this", "draft this as me", or wants any content produced as themselves. Trigger aggressively on any "in my voice", "as me", "my opinion/view", or personal-content-drafting request — this is the payoff of the whole second brain.
argument-hint: <question, or content brief to write in the user's voice>
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Brain Query

Answer questions, or generate content in the user's voice, grounded in what the second brain actually contains.

**Always read these files first:**
1. `AGENTS.md` — constitution and domain context
2. `voice.md` — voice spine (register, vocabulary, metaphors, anti-voice). **Required before any "as me" output — no exceptions.** If voice.md doesn't exist yet, run `/brain-voice` to build it from existing transcripts.

For any "in my voice" or "as me" request: after reading voice.md, also pull the relevant `wiki/voice-profile/` depth pages (e.g. `written-voice.md` for published content, `spoken-to-written.md` for conversion rules, `anti-voice.md` for drift check).

Request: `$ARGUMENTS`

## Steps

1. **Find seed pages with semantic search.** Run:
   ```bash
   python tools/embed-wiki.py --query "<the query or topic>" --top 5 --json
   ```
   This returns the 5 most semantically relevant pages in JSON with title, file path, and similarity score. These are your seeds — no need to manually read `index.md` to guess. Read `hot-personal.md` if the query is about the user's current life/emotional state. Read `hot-system.md` if the query is about recent wiki changes or what was ingested.

2. **Traverse the link graph from each seed.** Run the traversal script for the top 2-3 seeds:
   ```bash
   python tools/graph-traverse.py "<seed-title>" --hops 2 --max 15 --repo-relative
   ```
   This returns pages ordered by hop distance (0 = seed, 1 = direct links, 2 = two hops away). Read all hop-0 and hop-1 pages; read hop-2 pages selectively if they look relevant. Cross-domain connections at hop-2 are often where the non-obvious insight lives — a belief page that reaches a core identity page in two hops carries real signal.

3. **Stay grounded.** Synthesize only from what the wiki actually says. Do not invent views the user hasn't expressed. Where the wiki is silent or thin, say so plainly rather than filling the gap with a generic guess.

4. **Cite.** Attribute every substantive claim to its page, e.g. "(from [[Polska kultura "uważaj"]])". This keeps the output traceable and trustworthy.

5. **If writing content as the user:** pull the relevant `wiki/voice-profile/` pages plus the topical pages, and match their tone profile from the wiki (voice-profile/ pages define style, rhythm, patterns, and what they never say). Output the *finished* piece, not an outline or a list of options.

6. **Save valuable synthesis.** If the query surfaces a non-obvious cross-domain connection (something that required following 2+ hops to find), offer to save it as a `wiki/synthesis/` page. These compound — future queries can build on saved insights rather than rediscovering them. See synthesis page format in the constitution.

7. **Close honestly.** Note any gap where a recorded answer would make the output meaningfully stronger — that feeds the next `brain-ingest`.

## Scaling past ~100 pages

Semantic seed discovery (`embed-wiki.py`) + graph traversal (`graph-traverse.py`) is already in place. At ~150 pages, if queries feel expensive, decrease `--top` from 5 to 3 and `--hops` from 2 to 1 to stay within context budget.

## Why it matters

The value of the link graph is that it encodes *intentional* connections a human built with meaning — not cosine similarity. Keyword search finds pages that mention a topic. Graph traversal finds that one belief connects to a life story that connects to a core value — meaning two apparently unrelated ideas share a common root. That non-obvious connection is what makes the brain compound.
