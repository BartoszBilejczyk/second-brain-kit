# second-brain-kit

Every time you ask an AI for help, it doesn't know who you are.

It doesn't know what you believe, how you think, what you've been through, or how you sound. So it gives you generic answers. Useful, maybe. But not *yours*.

This kit fixes that. It gives you a personal second brain — a vault of cross-linked markdown pages that captures who you actually are. Once it's built, your AI doesn't answer from training data anymore. It answers from *you*.

Built on the [Karpathy "LLM Wiki" pattern](https://x.com/karpathy/status/1816531576228053133): just markdown files, wikilinks, and Claude Code skills that do the heavy lifting.

---

## What you get

- **`/brain-transcribe`** — drop in a voice recording; get a clean transcript
- **`/brain-ingest`** — AI reads the transcript, writes synthesized wiki pages, links them to everything else you've told it
- **`/brain-query`** — ask anything; get an answer grounded in your actual views. Or: "write this LinkedIn post as me"
- **`/brain-lint`** — structural health check: broken links, orphan pages, weak connections
- **`/brain-log`** — capture a quick thought directly, no recording needed
- **`/brain-review`** — quality audit after an ingest
- **`/brain-maintenance`** — recurring upkeep, staleness check, tension resolution
- **`/brain-retrospective`** — system meta-audit, skill improvement proposals

---

## Prerequisites

This requires a terminal and a bit of comfort with it. If you're setting this up for someone else, you can do the install and hand them a working system.

| Tool | What it's for | Install |
|------|---------------|---------|
| [Git](https://git-scm.com) | Version control for your brain | Likely already installed |
| [Python 3.13+](https://python.org/downloads) | Runs the transcription and search tools | [python.org/downloads](https://python.org/downloads) |
| [Claude Code CLI](https://claude.ai/code) | The AI interface — runs the skills | Requires Anthropic Pro or API key |

---

## Getting started

### 1. Create your repo

On GitHub, click **"Use this template"** → **Create a new repository**. This gives you a fresh repo with no shared history — your brain, not a fork.

> If the "Use this template" button isn't visible, enable "Template repository" in your repo's Settings → General. Users who clone from you will see the button on your repo.

### 2. Clone and set up a Python environment

```bash
git clone https://github.com/you/your-brain-repo.git
cd your-brain-repo
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

The virtual environment keeps the AI model downloads isolated from your system Python.

### 3. Run setup

**Option A — via Claude Code (recommended):**

```bash
claude
```

Then run `/brain-setup`. The skill will walk you through everything interactively.

**Option B — via CLI only (no Claude Code needed):**

```bash
python setup/setup.py
```

Same questions, same result. Use this if you're setting up on behalf of someone else or don't have Claude Code yet.

The setup configures your profile, installs Python dependencies, and runs a test embed to confirm everything works.

---

## First-run downloads

The first time you run `/brain-ingest`, it will download the AI models locally:

| Component | Size | When |
|-----------|------|------|
| Sentence-transformers model | ~420 MB | First ingest (semantic search) |
| PyTorch | ~700 MB (GPU) / ~200 MB (CPU-only) | First ingest |
| Whisper tiny model | ~75 MB | First `/brain-transcribe` with "fast" |
| Whisper small model | ~460 MB | First `/brain-transcribe` with "balanced" |
| Whisper medium model | ~1.5 GB | First `/brain-transcribe` with "accurate" |

**Total first run: ~1.2 GB (tiny) to ~2.6 GB (medium).** This is a one-time download. After that, everything runs fully offline. No API calls, no data leaves your machine.

`/brain-setup` warns you about sizes and pre-downloads the sentence-transformers model (~420 MB + PyTorch). Whisper downloads separately the first time you run `/brain-transcribe` — expect a pause of 30 seconds to several minutes depending on which model you pick.

---

## Whisper model comparison

| Model | Size | Speed (10 min audio) | Best for |
|-------|------|----------------------|----------|
| tiny | 75 MB | ~30 sec | Clear speech, quick drafts |
| small | 460 MB | ~90 sec | Most recordings — recommended |
| medium | 1.5 GB | ~3–5 min | Accented speech, noisy environments |

The `/brain-transcribe` skill will ask which model you want each time.

---

## Privacy

Your data stays on your machine. The AI models run locally. Nothing is pushed anywhere unless you explicitly run `git push`.

By default, voice recordings are **not committed to git** — setup will ask about this. You can keep everything local, or push to a private GitHub repo for backup.

Your name (or nickname) appears in Claude Code sessions so the AI knows what to call you. A nickname is totally fine.

---

## Use cases

**Content creator:** Record what you think about a topic → transcribe → ingest → "write an Instagram caption about this in my voice"

**Journaler:** Write notes or record reflections → ingest → "what patterns do I see in how I handle stress?"

**Career / coaching:** Record coaching sessions → ingest → "what are my blind spots around leadership?"

---

## Skill quick reference

| Skill | What it does |
|-------|-------------|
| `/brain-setup` | One-time guided setup |
| `/brain-transcribe` | Transcribe audio → transcript |
| `/brain-ingest` | Process transcripts → wiki pages |
| `/brain-query` | Answer questions from your wiki |
| `/brain-log` | Capture a quick thought |
| `/brain-review` | Quality audit after ingest |
| `/brain-lint` | Structural health check |
| `/brain-maintenance` | Recurring upkeep |
| `/brain-retrospective` | System improvement audit |

---

## Multi-agent support

Skills follow the `.agents/skills/<name>/SKILL.md` convention supported by Codex CLI and Gemini CLI. The `.agents/skills/` directory contains symlinks to the same files in `.claude/skills/` — one SKILL.md, all agents. See each tool's docs for how to invoke skills.

---

## Fork and adapt

Open source (MIT). Clone it, change it, make it yours. The skills are in `.claude/skills/` — plain markdown files you can edit directly. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
