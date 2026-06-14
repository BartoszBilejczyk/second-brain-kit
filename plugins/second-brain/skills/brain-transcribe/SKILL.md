---
name: brain-transcribe
description: Transcribe voice recordings into text using mlx_whisper (GPU-accelerated, Apple Silicon). Handles single files and folders. Saves transcripts to raw/transcripts/YYYY-MM-DD/ ready for brain-ingest. Use when the user says "transcribe this recording", "process my audio", "transcribe my session", drops a file path, or says "I have a recording". Trigger aggressively on any audio file reference or recording mention.
argument-hint: [path to audio file or folder of recordings]
allowed-tools: Read, Write, Bash, Glob
---

# Brain Transcribe

Turn voice recordings into clean transcripts, ready for brain-ingest.

**Arguments:** `$ARGUMENTS`

> **Automated pipeline available (Mac + Apple Silicon):** The VoiceWatcher daemon transcribes iPhone recordings automatically on arrival — no manual step needed. See `setup/iphone-voice-pipeline.md`. This skill is for manually transcribing files you already have on disk.

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
> **fast** — tiny model (~30 sec per 10 min of audio) — good for clear speech
> **balanced** — small model (~60 sec per 10 min) — recommended for most recordings
> **accurate** — large-v3 model (~90 sec per 10 min, GPU) — best quality, default for Apple Silicon"

Map choices to mlx models:
- fast → `mlx-community/whisper-tiny-mlx`
- balanced → `mlx-community/whisper-small-mlx`
- accurate → `mlx-community/whisper-large-v3-mlx`

---

## Step 4 — Verify mlx_whisper is available

```bash
mlx_whisper --help > /dev/null 2>&1 && echo "ok" || echo "not found"
```

If not found:
```bash
pip install mlx-whisper
brew install ffmpeg
```

---

## Step 5 — Transcribe

Determine today's date for the output folder:
```bash
date '+%Y-%m-%d'
```

Set the output directory to `raw/transcripts/YYYY-MM-DD/` (create if needed):
```bash
mkdir -p raw/transcripts/YYYY-MM-DD
```

**Single file:**
```bash
mlx_whisper "<audio_path>" \
  --model <model> \
  --language <lang> \
  --output-format txt \
  --output-dir raw/transcripts/YYYY-MM-DD
```

The output filename will be `<stem-minus-last-extension>.txt` (mlx_whisper strips the last dotted segment via `.with_suffix()`).

**Folder (batch):** Run the command for each file. Print progress as each completes:
> "1/3 done — session-01-identity.txt saved"

---

## Step 6 — Confirm and offer ingest

After completion:
> "Transcripts saved to raw/transcripts/YYYY-MM-DD/. Created:
> - raw/transcripts/2026-06-14/session-01-identity.txt"

Then ask:
> "Want to ingest these into your brain now? Say 'yes' to run brain-ingest, or 'not yet' to do it later."

If yes — invoke brain-ingest.
