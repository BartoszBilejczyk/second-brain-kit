---
name: brain-maintenance
description: Runs a scheduled health check on the user's second brain wiki. Invoke when the user says "maintain the brain", "run brain maintenance", "clean up the wiki", or on a scheduled basis. Checks for stale pages, weakly-linked content, resolved tensions, and outdated profile/hot.md. Outputs a prioritized action list and applies safe fixes automatically. Use this for recurring upkeep — it's the brain's sleep cycle equivalent.
argument-hint: [--level daily|weekly|monthly (default: weekly)]
allowed-tools: Read, Write, Glob, Grep, Edit, Bash
---

# Brain Maintenance

The second brain compounds only if it's pruned. This skill runs the recurring cleanup cycle — the equivalent of sleep consolidation for the brain. It doesn't replace `/brain-ingest` (which adds new material) or `/brain-lint` (deep structural check). It keeps what's already there healthy and actionable.

**Always read `CLAUDE.md` first**, then `log.md` (last 10 entries) to know what's changed since last maintenance.

---

## Maintenance levels

Run the appropriate level based on `$ARGUMENTS` or time since last maintenance (visible in `log.md`):

### Daily (< 2 min)
Triggered when: last entry in log.md was today or yesterday.

1. Read `hot.md` — is it still accurate? Update current situation if something shifted (new job, new project milestone, change in plans).
2. Check `profile.md` "current situation" — if it references something that's now past (e.g., "leaving job mid-July" after July), update it.
3. Done. Log: `## [date] maintenance | daily check`.

### Weekly (5–10 min)
Triggered when: last maintenance entry in log.md was 5–10 days ago.

1. Run structural check (same as `/brain-lint` but only critical checks):
   - Grep all `[[links]]` in wiki/, check each against page titles. Report mismatches.
   - Find pages with 0 inbound links from other wiki pages (not just index.md). Flag as candidates.
2. Check `meta/tensions.md` — are any marked tensions now resolved? If the user's situation has changed in a way that answers a tension (e.g., a decision was made, a situation resolved), note it and draft an answer under `_Answer:_` in the tension entry.
3. Update `hot.md` with any notable changes since last update.
4. Log: `## [date] maintenance | weekly`.

### Monthly (15–20 min)
Triggered when: last maintenance entry in log.md was 3+ weeks ago, OR user explicitly asks.

All weekly checks, plus:

1. **Staleness audit** — identify pages that meet ALL three criteria:
   - `updated` date 8+ weeks old
   - 0 inbound wiki-to-wiki links (not counting index.md)
   - Not cited in any tension in `meta/tensions.md`
   These are candidates for review: enrich, merge into another page, or delete.

2. **Weakly-linked pages review** — pages that only appear in `index.md` but nothing in the wiki links to them. For each one: should it exist as a standalone page, or should it be absorbed into a better-connected page?

3. **Profile.md current situation** — rewrite the "Current situation" section to reflect what's actually true now. This section decays fastest. Don't rewrite the whole file — just the situation block.

4. **Tension resolution check** — for each tension in `meta/tensions.md`, ask: has enough happened (new coaching, new wiki pages, life events) that an answer is now possible? If yes, write a draft answer under `_Answer:_` in the tension entry.

5. **Synthesis opportunity** — look at pages added since the last monthly maintenance. Are there 2-3 pages that connect across domains in a non-obvious way? If yes, create a synthesis page in `wiki/synthesis/`.

6. Log: `## [date] maintenance | monthly — [N pages reviewed, N tensions checked, N stale candidates]`.

---

## What to auto-fix vs. what to flag

**Auto-fix (safe, do immediately):**
- Broken link where the target page exists but the title doesn't match exactly (e.g., `[[Czas liminalny]]` → page title is `Czas liminalny - między jednym a drugim`): fix the title to match the short form used in links, not the other way around. Short = easier to link.
- `updated` date in frontmatter older than the actual last edit (when you can verify from log.md).
- `hot.md` references to events/pages that no longer exist.

**Flag only (require explicit user confirmation before changing):**
- Deleting any page (even if stale).
- Merging two pages.
- Updating `profile.md` current situation.
- Writing an answer to a tension.
- Creating synthesis pages.

---

## Staleness definition

A page is **stale** when:
- `updated` date is 8+ weeks ago, AND
- 0 inbound links from other wiki pages (only in index.md), AND
- Not referenced in `meta/tensions.md`

A page is **evergreen** (fine to not touch) when:
- It contains settled beliefs or identity facts (`type: belief`, `type: identity`, `confidence: high`)
- It's heavily linked from other pages
- It has no time-sensitive "current situation" language

Note: `profile.md` and `hot.md` are NOT wiki pages — they decay fastest and need review every 2-4 weeks regardless of links.

---

## The sleep-cycle analogy

Human brains consolidate during sleep: strengthen important connections, weaken unused ones, compress episodic memories into schemas. This skill does the same:

- **Strengthen**: add backlinks to weakly-connected but valuable pages
- **Weaken**: flag stale, 0-backlink pages for review  
- **Compress**: synthesis pages = schemas built from specific wiki pages

The goal is a **sharp brain, not a big one.** 62 high-quality linked pages > 200 disconnected notes.

---

## Output format

```
## Brain Maintenance — [date] | [level]

**Last maintenance:** [date from log.md]

**Hot/Profile:** [pass / what was updated]

**Broken links:** [count] — [list with proposed fixes]

**Weakly-linked candidates:** [list with recommended action per page]

**Stale candidates (monthly only):** [list]

**Tensions:** [any now answerable / any new]

**Synthesis opportunity (monthly only):** [if found]

**Actions taken:** [list of auto-fixes applied]

**Needs your decision:** [list of flagged items requiring confirmation]
```

Append to `log.md` after completing.
