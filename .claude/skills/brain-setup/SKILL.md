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

## Step 0 — Check for existing configuration

Before doing anything else, read `CLAUDE.md` and check the `## User` section.

- If `Name/alias:` is anything other than `User`, the brain is already configured.
- In that case, say: "Your brain is already configured as [name]. Want to update your settings, or just re-install dependencies?" Then branch accordingly — don't re-run the full setup unless asked.

---

## Step 1 — Welcome

Say something like:

> You're setting up your personal second brain. It's a vault of cross-linked markdown pages that an AI reads and uses to answer questions in your voice — not generic AI voice. You'll record yourself answering questions about your life, beliefs, and opinions. The AI transcribes them into linked pages. After 3–5 sessions, it starts to actually know you.
>
> This will take about 5 minutes. Let's configure it.

---

## Step 2 — Collect answers conversationally

Ask these 4 questions one at a time:

**Q1 — Name:**
> "What should I call you? This appears in your Claude sessions so the AI knows who you are. A nickname is totally fine — it doesn't have to be your real name. (Press Enter to use 'User'.)"

**Q2 — Goal:**
> "What's the main thing you want to use this brain for? For example: 'Generate Instagram content in my voice', 'Think through career decisions', 'Write with my authentic perspective'."

**Q3 — Language:**
> "What language will you mainly use? The brain handles any language — English, Polish, Spanish, bilingual, etc."

**Q4 — Recordings privacy:**
> "Should your voice recordings be excluded from git? This means they stay on your machine and won't be pushed to GitHub even if you push the rest of your brain. Recordings can be personal and are often large. [Y/n, default Y]"

---

## Step 3 — Apply configuration directly

Apply the answers inline (do not delegate to `setup.py` — that would re-ask all questions):

1. Read `CLAUDE.md` and replace the `## User` section:
   ```markdown
   ## User

   Name/alias: {name}
   Goal: {goal}
   Language: {language}

   *(This section is written by `/brain-setup` during onboarding. Update it any time.)*
   ```

2. Write `profile.md` with a starter template — name, goal, today's date, empty section stubs.

3. Update `.gitignore`:
   - If recordings should be excluded: uncomment or add `interview/recordings/`
   - If committed: leave as-is and note it

> **Note for CLI-only setup (no Claude Code):** Users can run `python setup/setup.py` directly instead. It does the same thing and also handles the virtual environment automatically.

---

## Step 4 — Install dependencies

Warn the user about download sizes first:

> Before installing, here's what will download on first use:
> - sentence-transformers model: ~420 MB (semantic search, downloaded once)
> - PyTorch: ~700 MB (required)
> - Whisper model: 75 MB (fast) to 1.5 GB (accurate), depending on what you choose
>
> Total: roughly 1.2–2.6 GB. This happens once and runs offline forever after.

If `$ARGUMENTS` contains `--skip-install`, skip this step.

Before running pip, check whether a virtual environment is active:
```bash
python -c "import sys; print('venv active' if sys.prefix != sys.base_prefix else 'NO VENV')"
```

If the output is `NO VENV`, stop and tell the user:
> "You need to activate a virtual environment first. In your terminal, run:
> ```
> python3 -m venv .venv
> source .venv/bin/activate   # Windows: .venv\Scripts\activate
> ```
> Then restart Claude Code and run `/brain-setup` again."

Once confirmed active, run:
```bash
pip install -r tools/requirements.txt
```

If it fails for another reason: show the exact error and suggest checking Python version (`python --version`, need 3.13+).

---

## Step 5 — Test embed

Run a quick test to confirm sentence-transformers works:
```bash
python tools/embed-wiki.py --query "test" --top 1 --json
```

If `meta/embeddings.json` doesn't exist yet (wiki is empty), an empty result is fine — the key is confirming the model loads without error.

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

If yes — show them the blank prompt template from `interview/README.md` (the section with the code block to paste into an LLM). Tell them to save the generated questions as `interview/01-identity.md` (or similar).
