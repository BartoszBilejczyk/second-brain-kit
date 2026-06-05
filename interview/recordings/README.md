# Recordings

Drop your voice recordings here: `.m4a`, `.mp3`, `.wav`.

**How to get the file path for transcription:**
- **Mac:** drag the file into the Terminal window to paste its path
- **Claude Code:** type `@` and start typing the filename to reference it
- **Or just type:** `interview/recordings/your-filename.m4a`

Then run:
```
/brain-transcribe
```

The skill will ask which model (fast/balanced/accurate) and which language, then save the transcript to `raw/transcripts/`.

---

Recordings are **not committed to git** by default (configured during setup). They stay local unless you explicitly push them. Your voice data is yours.
