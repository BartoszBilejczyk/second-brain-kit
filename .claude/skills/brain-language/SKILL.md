---
name: brain-language
description: Set the primary language for this second brain — updates the User profile and creates language.md with localized conventions (quote block heading, etc.). Run once during setup if your primary language is not English. Use when the user says "change language", "set language to Spanish", "I want to use the brain in French", "switch to German", or any similar request to localize the brain.
argument-hint: [optional language name, e.g. "Spanish"]
allowed-tools: Read, Write, Edit, AskUserQuestion
---

# Brain Language

Set the language this second brain operates in. The brain's infrastructure (skill instructions, AGENTS.md, wiki-check.py output) stays in English — the model reads those. What changes is the language of *your content*: wiki pages, voice profile, quote block headings, and synthesis outputs.

## What stays in English (always)

- Skill instructions (this file and all other SKILL.md files)
- AGENTS.md constitution and `_Related:_` link markers
- `wiki-check.py` output and frontmatter field names
- `index.md`, `log.md`, `hot.md` structural headers

These are machine-readable artifacts. Changing them would break tooling and make no practical difference — the model handles any content language.

## What this skill changes

1. **`AGENTS.md`** → `## User` → Language field (tells brain-ingest and brain-query what language to write in)
2. **`language.md`** → new config file at the repo root with:
   - Language name and code
   - Localized quote block heading (e.g. `## Citas (literal)` for Spanish)
3. **Reminder** → what to expect from brain-ingest and brain-voice going forward

## Steps

### Step 1 — Get the language

If `$ARGUMENTS` names a language, use it. Otherwise use AskUserQuestion:

Ask: "What language do you want to use for your second brain? (e.g. Spanish, French, German, Portuguese, Italian, Japanese...)"

### Step 2 — Generate localized conventions

For the chosen language, determine:

**Quote block heading** — the equivalent of `## Quotes (verbatim)` in the user's language. Examples:
- Spanish → `## Citas (literal)`
- French → `## Citations (verbatim)`
- German → `## Zitate (wörtlich)`
- Portuguese → `## Citações (literal)`
- Italian → `## Citazioni (letterale)`
- Japanese → `## 引用（逐語）`
- Polish → `## Cytaty (dosłownie)`

For any other language: derive the natural equivalent — "Quotes" → the common noun for quotation in that language, "(verbatim)" → the adjective for word-for-word/literal.

### Step 3 — Update AGENTS.md

Read `AGENTS.md` and update the `## User` section:

```markdown
## User

Name/alias: (set by /brain-setup)
Goal: (set by /brain-setup)
Language: [Language name] — wiki pages, voice profile, and synthesis outputs are written in this language
```

### Step 4 — Write language.md

Create `language.md` at the repo root:

```markdown
---
language: [Language name]
language_code: [ISO 639-1 code, e.g. es, fr, de]
quote_heading: "[localized heading]"
updated: YYYY-MM-DD
---

# Language Config

Primary language for this second brain: **[Language name]**

## Conventions

**Quote block heading** (used at the bottom of every full-voice wiki page):
```
[localized heading]
> Quote one
> Quote two
```

**What brain-ingest does:** Writes all wiki pages in [Language name]. Uses the quote heading above for the verbatim quotes section. The few-shot examples in brain-ingest are in English — they illustrate the *pattern* (don't re-register, don't invent), not the language.

**What brain-voice does:** Mines your transcripts and produces voice.md in [Language name]. Anti-voice phrases and vocabulary lists will be in your language.

**What stays in English:** Skill instructions, AGENTS.md structure, _Related:_ markers, wiki-check.py output.
```

### Step 5 — Confirm

Tell the user:
- Language set to [Language name]
- Quote heading for their wiki pages: `[localized heading]`
- brain-ingest and brain-voice will now produce content in their language
- Suggest running `/brain-voice` if they already have transcripts, to build the voice profile in their language

## Re-run behavior

If `language.md` already exists, read it first. Show the current language and ask if they want to change it. If yes, overwrite. If not, exit cleanly.
