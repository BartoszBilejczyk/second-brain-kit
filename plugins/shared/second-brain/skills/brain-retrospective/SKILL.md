---
name: brain-retrospective
description: Post-session retrospective for the user's second-brain system. Runs after brain-ingest + brain-lint to surface patterns across what was done, what was flagged, and what skills or strategy could be improved. Produces a compact report with concrete proposals for skill changes. Trigger whenever the user says "retrospective", "what went wrong this session", "how can we improve the brain system", "review the session", "what should we fix in the skills", "how did the session go", "what patterns did you find", "anything to improve in the skills", "review what we did", or after noticing repeated problems across sessions. Also trigger when the user asks "how is the skill quality" or "are the brain skills working well". NOT for reviewing content quality (that's brain-review) or structural integrity (that's brain-lint). This is about the *system itself*.
allowed-tools: Read, Glob, Grep, Bash
---

# Brain Retrospective

A fast meta-layer audit: not of the wiki content, but of the *process* — the skills, the standards, the patterns of what went wrong and right. Runs after a session, reads evidence, proposes changes.

**This skill does NOT auto-apply changes.** It produces proposals. The user reviews and confirms before anything is edited.

---

## What to read

1. `log.md` — last 20 entries (grep `"^## \[" log.md | tail -20`) to understand what was done
2. `hot.md` — current operational state and what just changed
3. Any `meta/brain-lint-report-*.md` files from the current date — these are the ground truth for what failed
4. The specific skill files that were invoked this session (read their `SKILL.md` to compare intent vs. outcome)

Do NOT read all wiki pages — the retrospective is about process, not content.

---

## What to analyse

### 1. Pattern recognition across lint findings
- What categories of problems appeared? (broken links, orphans, thin links, low inline count?)
- Are these one-off issues or systemic? A single broken link is noise; 28 thin pages is a pattern.
- Which checks fired most — that's where the friction lives.

### 2. Skill performance vs. stated intent
For each skill that ran this session, ask: did it do what its SKILL.md says it should?
- `brain-ingest`: did pages it created/enriched have inline links? Were backlinks added?
- `brain-lint`: did it catch what it should have? Any false positives?
- `brain-review`: (if run) did it catch content issues early?
- Any skill where the outcome diverged from the stated standard is a candidate for improvement.

### 3. Root cause, not symptom
Don't just say "28 pages are thin." Ask *why*: Was the inline-linking rule absent when these pages were created? Was it unclear? Was the rule present but not enforced (LLM ignored it)? Each root cause implies a different fix.

Root causes to consider:
- Rule missing from skill entirely
- Rule present but too vague (no examples, no sub-rules)
- Rule present and clear, but the LLM skipped it under token/context pressure
- Rule present, but the skill didn't read enough context to apply it (e.g. didn't read existing pages to know what to link)
- External factor (e.g. handoff brief too narrow in scope)

### 4. Strategic observations
Step back from individual findings. What does this session reveal about the system overall?
- Is the wiki growing faster than quality can keep up?
- Are certain domains (work, mind, money) better maintained than others?
- Is there a mismatch between what brain-query needs and what brain-ingest produces?
- Is token cost a problem — are skill runs getting too expensive as the wiki grows?

---

## Output format

```
## Brain Retrospective — [date]

**Session summary:** [1-2 sentences: what happened, what skills ran]

**Patterns found:**
- [Pattern 1: what, how many occurrences, estimated root cause]
- [Pattern 2: ...]

**Skill improvement proposals:**
- Skill: brain-ingest | Change: [specific addition/edit to SKILL.md] | Reason: [root cause it addresses]
- Skill: brain-lint   | Change: [...] | Reason: [...]
- (list only skills that need changes — don't pad)

**Strategic observations:**
[1-3 sentences on bigger picture. What does this session reveal about the system? What's the right next investment?]

**Proposed actions (prioritised):**
1. [Immediate — do now]
2. [Soon — next session]
3. [Backlog — track in meta/]
```

Keep it compact. If everything went well, say so briefly. Don't invent problems to look thorough.

---

## After the report

If the user approves any skill proposals, edit the relevant SKILL.md files directly. Append a one-line note to `log.md`: `## [date] retrospective | proposals: N skills updated`.

If any finding warrants a new tension entry in `meta/tensions.md`, add it there.
