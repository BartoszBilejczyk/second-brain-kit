@AGENTS.md

## AI Toolkit

Universal tools and skills available from `~/ai-toolkit`. Plugins `core@ai-toolkit` and
`experts@ai-toolkit` are installed - skills are auto-surfaced by the plugin system.

### Tools (must be invoked manually)

| Tool | Purpose | How to run |
|------|---------|------------|
| `~/ai-toolkit/tools/audio-intelligence/transcribe_audio.py` | Transcribe audio (m4a, mp3, wav) using Whisper large-v3 on Apple Silicon GPU | `python ~/ai-toolkit/tools/audio-intelligence/transcribe_audio.py <file> --language pl` |
<<<<<<< Updated upstream
=======
| `~/ai-toolkit/tools/voice-watcher/` | launchd daemon: auto-transcribes Voice Memos from iCloud Drive on arrival. Full pipeline: `setup/iphone-voice-pipeline.md` | See README — daemon, not a script to run manually |
>>>>>>> Stashed changes
| `~/ai-toolkit/tools/video-intelligence/` | Analyze YouTube videos via Gemini API | See README in that directory |
| `~/ai-toolkit/tools/md-to-pdf/convert_md_to_pdf.py` | Convert Markdown to PDF | `python ~/ai-toolkit/tools/md-to-pdf/convert_md_to_pdf.py <file>` |
| `~/ai-toolkit/tools/mobi-converter/mobi_converter.py` | Convert ebooks to MOBI format | `python ~/ai-toolkit/tools/mobi-converter/mobi_converter.py <file>` |

---

## Behavioral rules

**Think holistically about the whole repo before making changes.** Before implementing anything — a new skill, a tooling change, a constitution update — ask: what else in this repo is affected? Skills reference each other, AGENTS.md references skills, wiki-check.py is referenced by brain-lint, brain-setup feeds into brain-language, etc. A change to one file often has a correct corresponding change in 2-3 others. Silently touching one file while leaving related files inconsistent is the failure mode to avoid.
