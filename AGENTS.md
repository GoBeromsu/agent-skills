# agent-skills

This repository is a starter workspace for future agent-skill publication.

## Current structure
- `skills/` — reserved for future skill directories; currently intentionally empty except for the placeholder needed to keep the directory in Git
- `.claude-plugin/marketplace.json` — starter marketplace manifest
- `.github/workflows/` — starter validation workflow
- `README.md` — public starter copy

## Conventions
- Future skills should live at `skills/<name>/SKILL.md`
- Keep the marketplace manifest aligned with any newly published skills
- Keep public-facing copy truthful about the current published state
- Prefer minimal starter-safe metadata until real skills are reintroduced

## Validation
- `claude plugin validate .`
