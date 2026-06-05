# Contributing

second-brain-kit is intentionally minimal — that's a feature, not a gap. Before opening a PR, read this.

---

## What belongs here

- Bug fixes in the Python tools (`tools/`)
- Improvements to the setup experience (`setup/setup.py`)
- Skill improvements that make the core loop more reliable
- Documentation fixes

## What doesn't belong here

- New wiki categories (the existing ones cover most personal domains)
- Personal or domain-specific skill additions (fork the repo instead)
- New dependencies — the tool count is kept small deliberately

---

## How to contribute

1. Fork the repo
2. Create a branch: `git checkout -b fix/short-description`
3. Make your change — keep it focused
4. Test the flow end-to-end if you changed a skill or setup script
5. Open a PR with a clear description of what changed and why

---

## Skill changes

Skills are plain markdown in `.claude/skills/<name>/SKILL.md`. If you change a skill:
- Test it with a real Claude Code session
- Check that `.agents/skills/<name>` symlink still resolves correctly
- Make sure the description frontmatter still accurately triggers the skill

---

## Bug reports

Open a GitHub issue. Include:
- Your OS and Python version (`python --version`)
- Which skill or tool failed
- The exact error message
