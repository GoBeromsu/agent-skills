---
name: skill-deploy
description: Scan Obsidian vault skills for `publish: true` and sync them to GoBeromsu/agent-skills on GitHub. Use when the user says "/skill-deploy", "스킬 배포", "publish skills", "vault 스킬 GitHub에 올려", or wants to push their publishable vault skills to their personal agent-skills repo.
---

# skill-deploy

## Overview

Scan `Ataraxia/55. Tools/03 Skills/` for skills flagged `publish: true` in their metadata `.md` file, and sync them to the `GoBeromsu/agent-skills` GitHub repository. Skills without a metadata file or with `publish: false` are skipped. Vault is the single source of truth.

## When to Use

- User invokes `/skill-deploy` or says "스킬 배포", "publish skills", "vault 스킬 GitHub에 올려"
- A skill was newly marked `publish: true` and needs to be pushed
- Multiple skills need to be synced in one batch

**Not for:**
- Deploying non-skill vault content
- Pushing to marketplace repos (addyosmani/agent-skills) — that is a separate manual step

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`)
- `rsync` available (macOS built-in)

## Process

### Step 1 — Scan for Publishable Skills

Vault skills root: `/Users/beomsu/Documents/01. Obsidian/Ataraxia/55. Tools/03 Skills/`

For each subdirectory `{skill-name}`:
1. Check if `{skill-name}/{skill-name}.md` exists
2. Read its frontmatter: `grep "^publish:" {skill-name}.md`
3. `publish: true` → add to **publishable** list
4. Missing file, `publish: false`, or no `publish:` key → add to **skipped** list with reason

### Step 2 — Prepare Local Repo

**Default repo path**: `~/dev/agent-skills`
Override with env var: `$AGENT_SKILLS_REPO_PATH`

```bash
REPO="${AGENT_SKILLS_REPO_PATH:-$HOME/dev/agent-skills}"

if [ ! -d "$REPO/.git" ]; then
  # Create on GitHub if it does not exist yet
  gh repo view GoBeromsu/agent-skills &>/dev/null || \
    gh repo create GoBeromsu/agent-skills --public \
      --description "Personal Claude Code skill collection"

  # Clone locally
  gh repo clone GoBeromsu/agent-skills "$REPO"

  # Seed README on first run
  if [ ! -f "$REPO/README.md" ]; then
    printf "# agent-skills\n\nPersonal Claude Code skill collection.\n" \
      > "$REPO/README.md"
    git -C "$REPO" add README.md
    git -C "$REPO" commit -m "init: initial repo setup"
    git -C "$REPO" push origin main
  fi
fi

# Sync remote changes before writing
git -C "$REPO" pull origin main --rebase
```

### Step 3 — Copy Skill Files

For each skill in the publishable list:

```bash
VAULT_SKILL="/Users/beomsu/Documents/01. Obsidian/Ataraxia/55. Tools/03 Skills/{skill-name}"
REPO_SKILL="$REPO/skills/{skill-name}"

mkdir -p "$REPO_SKILL"

# Required files
cp "$VAULT_SKILL/SKILL.md"          "$REPO_SKILL/SKILL.md"
cp "$VAULT_SKILL/{skill-name}.md"   "$REPO_SKILL/{skill-name}.md"

# Optional nested folders — copy as-is
for dir in scripts references assets; do
  [ -d "$VAULT_SKILL/$dir" ] && rsync -a "$VAULT_SKILL/$dir/" "$REPO_SKILL/$dir/"
done
```

Wikilinks (`[[...]]`) inside SKILL.md are left as-is — no transformation.

If `SKILL.md` is missing for a publishable skill, report it as an error and skip that skill rather than silently continuing.

### Step 4 — Commit and Push

```bash
git -C "$REPO" add skills/
```

If `git diff --cached --stat` shows no changes: print "Already up to date." and stop.

Otherwise:

```bash
SKILL_COUNT=$(git -C "$REPO" diff --cached --name-only | grep -c "^skills/")
git -C "$REPO" commit -m "deploy: sync skills from vault ($(date +%Y-%m-%d))"
git -C "$REPO" push origin main
```

### Step 5 — Report

Always end with a deployment summary:

```
Deployed (N):
  ✓ brian-note-challenge
  ✓ skill-deploy

Skipped (M):
  ⊘ book          — no metadata file
  ⊘ deploy-quartz — publish: false
  ⊘ youtube       — no metadata file
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The repo probably hasn't changed, skip git pull" | Remote edits (README, manual fixes) cause push conflicts. Always pull first. |
| "Use `git add .` for simplicity" | Stages README, .gitignore, and unrelated files. Only `git add skills/` is safe. |
| "If SKILL.md is missing, skip silently" | A missing SKILL.md is a data integrity error — surface it explicitly. |
| "rsync might overwrite important repo files" | rsync only touches files within `$REPO_SKILL/`. Unrelated repo files are untouched. |

## Red Flags

- Running `git push` without `git pull --rebase` first
- Using `git add .` instead of `git add skills/`
- Deploying a skill without verifying `publish: true` in its metadata `.md`
- No summary at the end (user cannot tell what was deployed vs. skipped)

## Verification

- [ ] Every skill in "Deployed" list has `publish: true` in its `{skill-name}.md`
- [ ] `git diff --cached --stat` shows only paths under `skills/`
- [ ] `git push` completed without errors
- [ ] Skipped skills are listed with their reason
