---
name: brain-setup
description: Guided onboarding for second-brain-kit. Configures the user's name, goal, language, and privacy preferences; writes the ## User section to CLAUDE.md; installs Python dependencies; runs a test embed. Use when the user says "setup", "brain setup", "configure my brain", "get started", or opens Claude Code in a fresh kit. Trigger on first session automatically if the ## User section in CLAUDE.md still says "User" (the placeholder).
argument-hint: [--skip-install to skip pip install if already done]
allowed-tools: Read, Write, Edit, Bash
---

# Brain Setup

Welcome to second-brain-kit. This skill configures your brain in one go.

**Arguments:** `$ARGUMENTS`

---

## What this skill does

1. Welcome the user — explain what they're setting up and why (3 sentences max)
2. Collect 4 configuration answers conversationally
3. Write the `## User` section to `CLAUDE.md`
4. Write a starter `profile.md`
5. Update `.gitignore` for recordings based on their choice
6. Install Python dependencies (with download size warning)
7. Run a test embed to confirm tooling works
8. Show next steps and link to `interview/README.md`

You can either:
- **Run the CLI script** (recommended for a clean terminal experience): `python setup/setup.py`
- **Do it inline** (inside Claude Code): collect answers conversationally, then apply changes directly

If `$ARGUMENTS` contains `--skip-install`, skip steps 6 and 7.

---

## Step 1 — Welcome

Say something like:

> You're setting up your personal second brain. It's a vault of cross-linked markdown pages that an AI reads and uses to answer questions in your voice — not generic AI voice. You'll record yourself answering questions about your life, beliefs, and opinions. The AI transcribes them into linked pages. After a few sessions, it starts to actually know you.
>
> This will take about 5 minutes. Let's configure it.

---

## Step 2 — Collect answers

Ask these 4 questions conversationally (not all at once):

**Q1 — Name:**
> "What should I call you? This appears in your Claude sessions so the AI knows who you are. A nickname is totally fine — it doesn't have to be your real name. (Press Enter or type 'skip' to use 'User'.)"

**Q2 — Goal:**
> "What's the main thing you want to use this brain for? For example: 'Generate Instagram content in my voice', 'Think through career decisions', 'Write with my authentic perspective'."

**Q3 — Language:**
> "What language will you mainly use? The brain handles any language — English, Polish, Spanish, bilingual, etc."

**Q4 — Recordings privacy:**
> "Should your voice recordings be excluded from git? This means they stay on your machine and won't be pushed to GitHub even if you push the rest of your brain. Recordings can be personal and are often large. You can still keep everything locally — git doesn't mean push. [Y/n, default Y]"

---

## Step 3 — Apply configuration

After collecting answers, either:

**Option A** — Run the CLI script:
```bash
python setup/setup.py
```
(This will re-ask the questions. Tell the user to enter the same answers, or hand them off to the script directly.)

**Option B** — Apply directly from within Claude Code:

1. Read `CLAUDE.md` and replace the `## User` section:
   ```markdown
   ## User
   
   Name/alias: {name}
   Goal: {goal}
   Language: {language}
   
   *(This section is written by `/brain-setup` during onboarding. Update it any time.)*
   ```

2. Write `profile.md` with a starter template (name, goal, today's date, empty sections).

3. Update `.gitignore`:
   - If recordings should be excluded: uncomment or add `interview/recordings/`
   - If recordings should be committed: leave as-is (add a note)

---

## Step 4 — Install dependencies

Warn the user about download sizes first:

> Before installing, here's what will download on first use:
> - sentence-transformers model: ~420 MB (semantic search, downloaded once)
> - PyTorch: ~700 MB (required)
> - Whisper model: 75 MB (fast) to 1.5 GB (accurate), depending on what you choose
>
> Total: roughly 1.2–2.6 GB. This happens once and runs offline forever after.

Then run:
```bash
pip install -r tools/requirements.txt
```

If it fails: print the exact error and suggest checking Python version (`python --version`, need 3.13+).

---

## Step 5 — Test embed

Run a quick test to confirm sentence-transformers works:
```bash
python tools/embed-wiki.py --query "test" --top 1 --json
```

If `meta/embeddings.json` doesn't exist yet (wiki is empty), this will return an empty result — that's fine. The key is confirming the model loads without error.

If it fails: note the issue but don't block the user. Tell them to re-run `python tools/embed-wiki.py` after their first brain-ingest.

---

## Step 6 — Next steps

Tell the user:

> **You're set up. Here's what to do next:**
>
> 1. **Generate your interview questions** — open `interview/README.md`. It has a prompt template you paste into any LLM to generate questions personalized to you.
>
> 2. **Record your answers** — talk freely into your phone. Drop the file into `interview/recordings/`. Tangents are the best material.
>
> 3. **Transcribe:** `/brain-transcribe`
>
> 4. **Ingest:** `/brain-ingest` — this builds your wiki from the transcript.
>
> 5. **Query:** `/brain-query "what do I actually think about X?"`

Then ask: "Want me to show you the interview question prompt template now?"

If yes — show them the blank prompt template from `interview/README.md` (the one they paste into an LLM). Tell them to use a fresh chat to generate their questions, then save the output as `interview/01-identity.md` (or similar).
