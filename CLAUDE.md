@AGENTS.md

## Behavioral rules

**Think holistically about the whole repo before making changes.** Before implementing anything — a new skill, a tooling change, a constitution update — ask: what else in this repo is affected? Skills reference each other, AGENTS.md references skills, wiki-check.py is referenced by brain-lint, brain-setup feeds into brain-language, etc. A change to one file often has a correct corresponding change in 2-3 others. Silently touching one file while leaving related files inconsistent is the failure mode to avoid.
