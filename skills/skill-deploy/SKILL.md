---
name: skill-deploy
description: Sync vault skills to local .claude/skills/ and push publishable ones to GoBeromsu/agent-skills on GitHub. Use when the user says "/skill-deploy", "스킬 배포", "publish skills", "스킬 동기화", "sync skills", or wants to update deployed skills from the vault SSOT. Also triggers after skill improvements or batch skill edits.
---

# skill-deploy

## Overview

Full skill deployment pipeline: sync SSOT (`55. Tools/03 Skills/`) to local `.claude/skills/` directories, then push publishable skills to GitHub. Vault is the single source of truth — deployed copies are always overwritten from source.

## When to Use

- After improving or creating skills in `55. Tools/03 Skills/`
- After batch skill edits (guideline compliance, refactoring)
- When the user explicitly asks to deploy, sync, or publish skills
- Do NOT use for individual skill file edits — only for deployment sync

## Prerequisites

`gh` CLI authenticated (`gh auth status`), `rsync` available.

## Process

### Step 1 — Scan SSOT

Vault root: `/Users/beomsu/Documents/01. Obsidian/Ataraxia/55. Tools/03 Skills/`

For each subdirectory:
1. Verify `SKILL.md` exists (skip directories without it)
2. Check `{skill-name}/{skill-name}.md` for `publish: true` → mark as GitHub-publishable

### Step 2 — Local Sync (SSOT → .claude/skills/)

Sync source skills to the repo-scope deployment directory.

```bash
VAULT="/Users/beomsu/Documents/01. Obsidian/Ataraxia/55. Tools/03 Skills"
DEST="/Users/beomsu/Documents/01. Obsidian/Ataraxia/.claude/skills"

# Sync each skill that already has a deployed copy
for skill_dir in "$DEST"/*/; do
  skill=$(basename "$skill_dir")
  if [ -f "$VAULT/$skill/SKILL.md" ]; then
    cp "$VAULT/$skill/SKILL.md" "$DEST/$skill/"
    for dir in scripts references assets; do
      if [ -d "$VAULT/$skill/$dir" ]; then
        rsync -a --delete "$VAULT/$skill/$dir/" "$DEST/$skill/$dir/"
      fi
    done
  else
    echo "⚠ $skill — deployed but no SSOT source"
  fi
done
```

After sync, verify each updated skill:
```bash
for skill_dir in "$DEST"/*/; do
  skill=$(basename "$skill_dir")
  [ -f "$VAULT/$skill/SKILL.md" ] && diff -q "$VAULT/$skill/SKILL.md" "$DEST/$skill/SKILL.md"
done
```

Skills deployed without SSOT source are flagged — ask the user whether to remove or create source.

### Step 3 — Prepare GitHub Repo

```bash
REPO="${AGENT_SKILLS_REPO_PATH:-$HOME/dev/agent-skills}"

if [ ! -d "$REPO/.git" ]; then
  gh repo view GoBeromsu/agent-skills &>/dev/null || \
    gh repo create GoBeromsu/agent-skills --public --description "Personal Claude Code skill collection"
  gh repo clone GoBeromsu/agent-skills "$REPO"
fi

git -C "$REPO" pull --rebase
```

### Step 4 — Copy Publishable Skills to Repo

For each skill with `publish: true` in its metadata:

```bash
DEST="$REPO/skills/{skill-name}"
mkdir -p "$DEST"
cp "$VAULT/{skill-name}/SKILL.md" "$DEST/"
for dir in scripts references assets; do
  [ -d "$VAULT/{skill-name}/$dir" ] && rsync -a "$VAULT/{skill-name}/$dir/" "$DEST/$dir/"
done
```

Missing `SKILL.md` = error, skip that skill explicitly.

### Step 5 — Commit and Push

```bash
git -C "$REPO" add skills/
git -C "$REPO" diff --cached --quiet && echo "Already up to date." && exit 0
git -C "$REPO" commit -m "deploy: sync skills from vault ($(date +%Y-%m-%d))"
git -C "$REPO" push origin main
```

### Step 6 — Report

```
Local Sync:
  ✓ skill-name — synced
  ⚠ skill-name — no SSOT source (orphan)

GitHub Deployed (N):
  ✓ skill-name

GitHub Skipped (M):
  ⊘ skill-name — reason
```

Verify remote: `gh api repos/GoBeromsu/agent-skills/contents/skills --jq '.[].name'`

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The deployed copy is newer, I'll skip syncing from SSOT." | SSOT is always authoritative. If the deployed copy has useful changes, move them to SSOT first, then sync. |
| "I'll just edit .claude/skills/ directly, it's faster." | Direct edits to deployed copies are overwritten on next sync. Always edit in 55. Tools/03 Skills/. |
| "This skill doesn't need local sync, it's only for GitHub." | Local sync ensures the agent actually uses the latest version. GitHub push without local sync means your own environment is stale. |
| "I'll clean up orphan skills later." | Orphan deployed skills with no SSOT source cause confusion — flag and resolve immediately. |

## Red Flags

- `git push` without `git pull --rebase` first
- `git add .` instead of `git add skills/`
- Editing deployed copies (.claude/skills/) instead of SSOT (55. Tools/03 Skills/)
- No deployment summary at the end
- Skipping local sync and only pushing to GitHub

## Verification

After completing the workflow, confirm:

- [ ] All repo-scope deployed skills match SSOT: `diff` returns 0 for every synced SKILL.md
- [ ] Orphan skills (deployed without SSOT) flagged or resolved
- [ ] Each GitHub-deployed skill has `publish: true` in its `{skill-name}.md` metadata
- [ ] `git diff --cached --stat` shows only `skills/` paths
- [ ] Remote confirmed: `gh api repos/GoBeromsu/agent-skills/contents/skills --jq '.[].name'`
- [ ] Deployment report printed with sync/deployed/skipped counts
