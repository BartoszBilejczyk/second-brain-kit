@AGENTS.md

## AI Toolkit

Universal tools and skills available from `~/ai-toolkit`. Plugins `core@ai-toolkit` and
`experts@ai-toolkit` are installed - skills are auto-surfaced by the plugin system.

### Tools (must be invoked manually)

| Tool | Purpose | How to run |
|------|---------|------------|
| `~/ai-toolkit/tools/audio-intelligence/transcribe_audio.py` | Transcribe audio (m4a, mp3, wav) using Whisper large-v3 on Apple Silicon GPU | `python ~/ai-toolkit/tools/audio-intelligence/transcribe_audio.py <file> --language pl` |
| `~/ai-toolkit/tools/voice-watcher/` | launchd daemon: auto-transcribes Voice Memos from iCloud Drive on arrival. Full pipeline: `setup/iphone-voice-pipeline.md` | See README — daemon, not a script to run manually |
| `~/ai-toolkit/tools/video-intelligence/` | Analyze YouTube videos via Gemini API | See README in that directory |
| `~/ai-toolkit/tools/md-to-pdf/convert_md_to_pdf.py` | Convert Markdown to PDF | `python ~/ai-toolkit/tools/md-to-pdf/convert_md_to_pdf.py <file>` |
| `~/ai-toolkit/tools/mobi-converter/mobi_converter.py` | Convert ebooks to MOBI format | `python ~/ai-toolkit/tools/mobi-converter/mobi_converter.py <file>` |

---

## Behavioral rules

**Think holistically about the whole repo before making changes.** Before implementing anything — a new skill, a tooling change, a constitution update — ask: what else in this repo is affected? Skills reference each other, AGENTS.md references skills, wiki-check.py is referenced by brain-lint, brain-setup feeds into brain-language, etc. A change to one file often has a correct corresponding change in 2-3 others. Silently touching one file while leaving related files inconsistent is the failure mode to avoid.

---

## Cross-repo Claude memory

Claude keeps a cross-repo working memory at `~/claude-memory/` (`short-term.md` + `long-term.md`), via the `memory@ai-toolkit` plugin — session digests and distilled facts spanning all repos. **This is Claude's own working memory, distinct from any second brain this kit builds** (a second brain is the *user*; this memory is *Claude*). Never mix them.

- Recall recent work → `short-term-memory` (filtered to current repo; ask to widen).
- Save the session → `short-term-memory` (write mode).
- Distill into durable facts → `memory-consolidate`.

Read is manual (no auto-injection at session start).
