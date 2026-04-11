---
name: skill-deploy
description: Scan Obsidian vault skills for publish true and sync them to GoBeromsu/agent-skills on GitHub. Use when the user says "/skill-deploy", "스킬 배포", "publish skills", "vault 스킬 GitHub에 올려", or wants to push their publishable vault skills to their personal agent-skills repo.
---

# skill-deploy

## Overview

Scan `Ataraxia/55. Tools/03 Skills/` for skills with `publish: true` in their `{skill-name}.md` metadata, and sync them to `GoBeromsu/agent-skills`. Vault is the single source of truth.

## Prerequisites

`gh` CLI authenticated (`gh auth status`), `rsync` available.

## Process

### Step 1 — Scan

Vault root: `/Users/beomsu/Documents/01. Obsidian/Ataraxia/55. Tools/03 Skills/`

For each subdirectory:
1. Check `{skill-name}/{skill-name}.md` exists
2. `grep "^publish:" {skill-name}.md` → `true` = publishable, else skip (record reason)

### Step 2 — Prepare Repo

```bash
REPO="${AGENT_SKILLS_REPO_PATH:-$HOME/dev/agent-skills}"

if [ ! -d "$REPO/.git" ]; then
  gh repo view GoBeromsu/agent-skills &>/dev/null || \
    gh repo create GoBeromsu/agent-skills --public --description "Personal Claude Code skill collection"
  gh repo clone GoBeromsu/agent-skills "$REPO"
fi

git -C "$REPO" pull --rebase
```

### Step 3 — Copy Files

For each publishable skill:

```bash
VAULT="/Users/beomsu/Documents/01. Obsidian/Ataraxia/55. Tools/03 Skills/{skill-name}"
DEST="$REPO/skills/{skill-name}"
mkdir -p "$DEST"
cp "$VAULT/SKILL.md" "$DEST/"
for dir in scripts references assets; do
  [ -d "$VAULT/$dir" ] && rsync -a "$VAULT/$dir/" "$DEST/$dir/"
done
```

Missing `SKILL.md` = error, skip that skill explicitly.

### Step 4 — Commit and Push

```bash
git -C "$REPO" add skills/
git -C "$REPO" diff --cached --quiet && echo "Already up to date." && exit 0
git -C "$REPO" commit -m "deploy: sync skills from vault ($(date +%Y-%m-%d))"
git -C "$REPO" push origin main
```

### Step 5 — Report

```
Deployed (N):
  ✓ skill-name

Skipped (M):
  ⊘ skill-name — reason
```

Verify remote: `gh api repos/GoBeromsu/agent-skills/contents/skills --jq '.[].name'`

## Red Flags

- `git push` without `git pull --rebase` first
- `git add .` instead of `git add skills/`
- No deployment summary at the end

## Verification

- [ ] Each deployed skill has `publish: true` in its metadata `.md`
- [ ] `git diff --cached --stat` shows only `skills/` paths
- [ ] Remote confirmed: `gh api repos/GoBeromsu/agent-skills/contents/skills --jq '.[].name'`
