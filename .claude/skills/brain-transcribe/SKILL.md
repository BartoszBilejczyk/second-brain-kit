---
name: brain-transcribe
description: Transcribe voice recordings into text using Whisper (local, offline). Handles single files and folders. Saves transcripts to raw/transcripts/ ready for brain-ingest. Use when the user says "transcribe this recording", "process my audio", "transcribe my session", drops a file path, or says "I have a recording". Trigger aggressively on any audio file reference or recording mention.
argument-hint: [path to audio file or folder of recordings]
allowed-tools: Read, Write, Bash, Glob
---

# Brain Transcribe

Turn voice recordings into clean transcripts, ready for brain-ingest.

**Arguments:** `$ARGUMENTS`

---

## Step 1 — Find the recording(s)

If `$ARGUMENTS` contains a file or folder path, use it directly.

Otherwise ask:
> "What's the path to your recording(s)? You can drag a file into the terminal to get its path, or use @ in Claude Code to browse. A single file or a whole folder both work."

**Single file:** `.m4a`, `.mp3`, `.wav`, or similar audio format.

**Folder:** Scan for all audio files (`.m4a`, `.mp3`, `.wav`) and list what was found:
> "Found 3 recordings in that folder:
> - session-01-identity.m4a
> - session-02-work.m4a
> - voice-memo-2025-03-15.m4a"

---

## Step 2 — Choose language

Always ask — don't try to auto-detect:
> "What language did you speak? (e.g. English, Polish, Spanish — or 'en', 'pl', 'es')"

---

## Step 3 — Choose model

Show the options with timing estimates:
> "How much accuracy do you need?
>
> **fast** — tiny model (~75 MB, ~30 sec per 10 min of audio) — good for clear speech
> **balanced** — small model (~460 MB, ~90 sec per 10 min) — recommended for most recordings
> **accurate** — medium model (~1.5 GB, ~3–5 min per 10 min) — best for accented speech, noisy audio"

For batch folders, also show the total time estimate:
> "You have 3 recordings totaling ~45 minutes. At balanced speed, that's about ~7 minutes of transcription."

Map choices to Whisper models:
- fast → `tiny`
- balanced → `small`
- accurate → `medium`

---

## Step 4 — Transcribe

**Single file:**
```bash
python tools/transcribe_audio.py "<audio_path>" --model <model> --language <lang> --output "raw/transcripts/<stem>.md"
```

**Folder (batch):**
Print progress as each file completes:
> "1/3 done — session-01-identity.md saved"
> "2/3 done — session-02-work.md saved"
> "3/3 done — voice-memo-2025-03-15.md saved"

All transcripts save to `raw/transcripts/` with `.md` extension.

---

## Step 5 — Confirm and offer ingest

After completion:
> "All transcripts saved to raw/transcripts/. Here's what was created:
> - raw/transcripts/session-01-identity.md
> - raw/transcripts/session-02-work.md"

Then ask:
> "Want to ingest these into your brain now? Once ingested, you'll be able to ask things like:
> - 'What's my genuine take on why I create content?'
> - 'Write a post about [topic] in my voice.'
>
> Say 'yes' to run brain-ingest, or 'not yet' to do it later."

If they say yes — hand off to brain-ingest (or invoke it directly if the skill system supports chaining).
