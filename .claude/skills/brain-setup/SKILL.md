---
name: brain-setup
description: Guided onboarding for second-brain-kit. Configures the user's name, goal, language, and privacy preferences; writes the ## User section to AGENTS.md; installs Python dependencies; runs a test embed. Use when the user says "setup", "brain setup", "configure my brain", "get started", or opens Claude Code in a fresh kit. Trigger on first session automatically if the ## User section in AGENTS.md still says "User" (the placeholder).
argument-hint: [--skip-install to skip pip install if already done]
allowed-tools: Read, Write, Edit, Bash
---

# Brain Setup

Welcome to second-brain-kit. This skill configures your brain in one go.

**Arguments:** `$ARGUMENTS`

---

## Step 0 — Check for existing configuration

Before doing anything else, read `AGENTS.md` and check the `## User` section.

- If `Name/alias:` is anything other than `User`, the brain is already configured.
- In that case, say: "Your brain is already configured as [name]. Want to update your settings, or just re-install dependencies?" Then branch accordingly — don't re-run the full setup unless asked.

---

## Step 1 — Welcome

Say something like:

> You're setting up your personal second brain. It's a vault of cross-linked markdown pages that an AI reads and uses to answer questions in your voice — not generic AI voice. You'll record yourself answering questions about your life, beliefs, and opinions. The AI transcribes them into linked pages. After 3–5 sessions, it starts to actually know you.
>
> This will take about 5 minutes. Let's configure it.

---

## Step 2 — Collect answers

Ask all four questions as a single numbered list in plain text. Wait for the user to reply with their answers before proceeding.

> 1. What should I call you? (A nickname is fine — it appears in Claude sessions so the AI knows who you are.)
> 2. What's the main thing you want to use this brain for?
> 3. What language will you mainly use?
> 4. Should your voice recordings be excluded from git? They'll stay on your machine and won't be pushed to GitHub. Recommended if recordings are personal or large. (yes/no, default yes)

---

## Step 3 — Apply configuration directly

Apply the answers inline (do not delegate to `setup.py` — that would re-ask all questions):

1. Read `AGENTS.md` and replace the `## User` section:
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

Run directly:
```bash
pip install -r tools/requirements.txt
```

If it fails with `externally-managed-environment`: tell the user they need a venv because their Python is system-managed. Suggest:
```
python3 -m venv .venv && source .venv/bin/activate
```
Then re-run the install.

If it fails for any other reason: show the exact error and suggest checking Python version (`python --version`, need 3.10+).

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

Explain the full picture as plain text — the user must understand what to do next without reading any README:

> **Your brain is configured but empty. Here's how it comes alive.**
>
> The brain learns from *you* — your words, your stories, your way of thinking. The raw material is answers: to questions about your life, beliefs, decisions, opinions. Once you provide that material, `/brain-ingest` handles everything — transcribing, synthesizing, linking it all into a searchable wiki in your voice.
>
> **There are a few ways to get started:**
>
> **Let Claude generate your questions (recommended).** Tell me what you want this brain for — what's going on in your life, what you're trying to figure out, what you'd want to be able to ask in 6 months. The more context you give, the more tailored the questions. I'll generate a personalized list you can start answering right away. You can answer them by recording yourself (voice memo on your phone is perfect) or just by writing.
>
> **Start talking without questions.** You don't need a structured list first. Record yourself — stream of consciousness, whatever's on your mind. Drop the file into `interview/recordings/`, run `/brain-transcribe` then `/brain-ingest`. Done.
>
> **Write instead of record.** Prefer typing? Drop a text file into `raw/sources/` and run `/brain-ingest` directly.
>
> However you add material — once it's ingested, you can ask `/brain-query "what do I actually think about X?"` and get answers grounded in your own words.

Then ask as plain text:

> How do you want to start? I can generate a personalized question list right now if you tell me a bit about your goal — or if you already have recordings or written material ready, we can go straight to ingesting.

**If "Generate my questions now":**

Ask as plain text (not AskUserQuestion — needs a free-form response):

> "Tell me what you want this brain to do for you. What's going on in your life right now, what are you trying to figure out, what decisions are you facing? The more you share, the better the questions. Just write — there's no wrong answer."

Wait for their response. Generate a tailored list of 15–20 interview questions based on what they wrote. Questions should be open-ended and personal — designed to draw out beliefs, stories, patterns, and opinions, not facts. Save to `interview/01-questions.md` and tell the user: answer these by recording yourself (voice memo is fine) or writing — then drop the material into `interview/recordings/` or `raw/sources/` and run `/brain-ingest`.

**If "I already have recordings ready":**

Tell them to drop the files into `interview/recordings/` and run `/brain-transcribe` followed by `/brain-ingest`.

**If "I'll write my answers as text":**

Tell them to drop a text file into `raw/sources/` and run `/brain-ingest`.
