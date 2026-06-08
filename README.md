# second-brain-kit

Every time you work with an AI, you have to be in the room.

You brief it, you correct it, you bring the judgment it's missing. It can execute — but it can't think like you, because it doesn't know how you think. So the ceiling on what you can delegate stays low.

This kit changes that. It gives Claude a persistent, growing model of how you reason — your frameworks, your voice, your priorities, the way you weigh tradeoffs. Once it's built, you can hand Claude work that previously needed you in the room: projects, decisions, automations, content. The output is yours — not because you wrote it, but because Claude knows how you would.

Built on the [Karpathy "LLM Wiki" pattern](https://x.com/karpathy/status/1816531576228053133): markdown files, wikilinks, and Claude Code skills that do the heavy lifting.

---

## How it works

You record yourself — voice memos answering questions about your life, work, beliefs, decisions. The AI transcribes and synthesizes those recordings into a cross-linked wiki of pages, each capturing a piece of how you think. The more sessions, the richer the model.

An alternative is writing the notes yourself rather than recording and then using them as as the brain good for /brain-ingest skill.

Once the wiki exists, every project you run through Claude can be grounded in your actual thinking.

---

## Skills

| Skill | What it does |
|-------|-------------|
| `/brain-setup` | One-time guided setup |
| `/brain-transcribe` | Transcribe a voice recording → clean transcript |
| `/brain-ingest` | Process transcripts or text → synthesized wiki pages |
| `/brain-query` | Answer a question or generate content grounded in your wiki |
| `/brain-log` | Log what was ingested and what changed |
| `/brain-review` | Quality audit after an ingest |
| `/brain-lint` | Structural health check: broken links, orphans, weak connections |
| `/brain-maintenance` | Recurring upkeep, staleness check, tension resolution |
| `/brain-retrospective` | System meta-audit, skill improvement proposals |

---

## Prerequisites

| Tool | What it's for | Install |
|------|---------------|---------|
| [Git](https://git-scm.com) | Version control for your brain | Likely already installed |
| [Python 3.10+](https://python.org/downloads) | Runs transcription (Whisper) and semantic search | [python.org/downloads](https://python.org/downloads) |
| [Claude Code](https://claude.ai/code) | Runs the skills — works in the desktop app, VS Code, or CLI | Requires Anthropic Pro or API key |

---

## Getting started

### 1. Create your repo

On GitHub, click **"Use this template"** → **Create a new repository**. This gives you a fresh repo with no shared history — your brain, not a fork.

> If the "Use this template" button isn't visible, enable "Template repository" in your repo's Settings → General.

### 2. Clone it

```bash
git clone https://github.com/you/your-brain-repo.git
cd your-brain-repo
```

### 3. Run setup

Open the repo in Claude Code (desktop app, VS Code, or `claude` in terminal) and run:

```
/brain-setup
```

The skill walks you through configuration, installs dependencies, and gets you to your first interview questions.

---

## First-run downloads

Two local tools download models on first use — these run on your machine, not in the cloud:

| Component | Size | When |
|-----------|------|------|
| Sentence-transformers model | ~420 MB | First ingest (semantic search) |
| PyTorch | ~200–700 MB | First ingest |
| Whisper tiny | ~75 MB | First `/brain-transcribe` (fast mode) |
| Whisper small | ~460 MB | First `/brain-transcribe` (balanced) |
| Whisper medium | ~1.5 GB | First `/brain-transcribe` (accurate) |

**Total first run: ~1.2–2.6 GB.** One-time download. After that, transcription and search run offline.

Claude itself runs via the cloud (Claude Code API) — your wiki pages are the context it reads, but the AI is not local.

---

## Whisper model comparison

| Model | Size | Speed (10 min audio) | Best for |
|-------|------|----------------------|----------|
| tiny | 75 MB | ~30 sec | Clear speech, quick drafts |
| small | 460 MB | ~90 sec | Most recordings — recommended |
| medium | 1.5 GB | ~3–5 min | Accented speech, noisy environments |

---

## Privacy

Voice recordings stay on your machine by default and are not committed to git. Your wiki pages can be kept fully local or backed up to a private GitHub repo — your call.

---

## Use cases

**Building products:** Run a project brief through Claude with your product instincts already loaded. Less back-and-forth, higher-quality output.

**Career decisions:** Record your thinking on a big decision → ingest → "given how I think about risk, what am I not seeing here?"

**Content creation:** Record what you actually think about a topic → "write a LinkedIn post on this in my voice"

**Automations:** Build Claude-powered workflows that act on your judgment, not generic defaults.

---

## Multi-agent support

Skills follow the `.agents/skills/<name>/SKILL.md` convention supported by Codex CLI and Gemini CLI. The `.agents/skills/` directory contains symlinks to `.claude/skills/` — one SKILL.md, all agents.

---

## Fork and adapt

Open source (MIT). Skills are plain markdown files in `.claude/skills/` — edit them directly. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
