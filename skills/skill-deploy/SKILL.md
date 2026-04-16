---
name: skill-deploy
description: Push publishable skills from the vault SSOT to GoBeromsu/agent-skills on GitHub, then sync deployed mirrors. Use when the user says "/skill-deploy", "스킬 배포", "publish skills", or wants to update deployed skills from the vault SSOT after skill edits.
---

# skill-deploy

## Overview

Push publishable skills from the vault SSOT to GitHub, then pull those updates onto deployed machines. The vault copy under `50. AI/04 Skills/` is the source of truth; GitHub and local plugin installs are downstream mirrors.

## When to Use

Use this skill only after the SSOT changes are ready to be propagated beyond the vault.

- After improving or creating skills in `50. AI/04 Skills/`
- After batch skill edits such as guideline compliance or refactoring
- When the user explicitly asks to deploy, sync, or publish skills
- Do NOT use for individual skill file edits before the SSOT changes are ready

## Prerequisites

`gh` CLI authenticated (`gh auth status`).

## Private Skills Note

Skills without `publish: true` in their metadata are **vault-only** and are not pushed to GitHub. They are not delivered via `claude plugins update`. If needed on non-vault machines, copy them manually from the vault SSOT.

| Status | Skills |
|--------|--------|
| `publish: true` (via marketplace) | book, brian-note-challenge, clawhip, deploy-quartz, fyc, gws, obsidian-cli, obsidian-vault-doctor, openclaw, pdf2md, rize, skill-deploy, terminology, youtube-upload, zotero |
| Vault-only (not pushed) | channel-ingest, naver (directories not present in vault) |

## Process

### Step 1 — Scan SSOT

Vault root: `/Users/beomsu/Documents/01. Obsidian/Ataraxia/50. AI/04 Skills/`

For each subdirectory:
1. Verify `SKILL.md` exists (skip directories without it)
2. Check `{skill-name}/{skill-name}.md` for `publish: true` and mark it as GitHub-publishable

### Step 2 — Prepare GitHub Repo

```bash
REPO="${AGENT_SKILLS_REPO_PATH:-$HOME/dev/agent-skills}"

if [ ! -d "$REPO/.git" ]; then
  gh repo view GoBeromsu/agent-skills &>/dev/null || \
    gh repo create GoBeromsu/agent-skills --public --description "Personal Claude Code skill collection"
  gh repo clone GoBeromsu/agent-skills "$REPO"
fi

git -C "$REPO" pull --rebase
```

### Step 3 — Copy Publishable Skills to Repo

For each skill with `publish: true` in its metadata:

```bash
VAULT="/Users/beomsu/Documents/01. Obsidian/Ataraxia/50. AI/04 Skills"
DEST="$REPO/skills/{skill-name}"
mkdir -p "$DEST"
cp "$VAULT/{skill-name}/SKILL.md" "$DEST/"
for dir in scripts references assets; do
  [ -d "$VAULT/{skill-name}/$dir" ] && cp -r "$VAULT/{skill-name}/$dir/" "$DEST/$dir/"
done
```

Missing `SKILL.md` is an error. Skip that skill explicitly and report it.

### Step 4 — Version Bump

`claude plugins update` compares version strings, so the version must change when deployed content changes.

```bash
PLUGIN_JSON="$REPO/.claude-plugin/plugin.json"
CURRENT=$(grep -o '"version": "[^"]*"' "$PLUGIN_JSON" | grep -o '[0-9]*\.[0-9]*\.[0-9]*')
MAJOR=$(echo "$CURRENT" | cut -d. -f1)
MINOR=$(echo "$CURRENT" | cut -d. -f2)
PATCH=$(echo "$CURRENT" | cut -d. -f3)
NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
sed -i '' "s/\"version\": \"$CURRENT\"/\"version\": \"$NEW_VERSION\"/" "$PLUGIN_JSON"
echo "Version: $CURRENT → $NEW_VERSION"
```

### Step 5 — Commit and Push

```bash
git -C "$REPO" add skills/ .claude-plugin/plugin.json
git -C "$REPO" diff --cached --quiet && echo "Already up to date." && exit 0
git -C "$REPO" commit -m "deploy: sync skills from vault ($(date +%Y-%m-%d))"
git -C "$REPO" push origin main
```

### Step 6 — Sync Deployed Mirrors

```bash
claude plugins update agent-skills@beomsu-koh
ssh m1-pro claude plugins update agent-skills@beomsu-koh
```

Add more machines only when they actually consume the marketplace copy.

### Step 7 — Report

```text
GitHub Deployed (N):
  ✓ skill-name

GitHub Skipped (M):
  ⊘ skill-name — reason (e.g. publish: false)

Mirror Sync:
  ✓ local
  ✓ m1-pro
```

Verify remote: `gh api repos/GoBeromsu/agent-skills/contents/skills --jq '.[].name'`

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll just run plugins update later, it's fine." | Run it immediately after push. A stale machine is an invisible bug. |
| "The push succeeded so every machine is up to date." | Push updates GitHub only. Each machine must explicitly run `claude plugins update`. |
| "I'll edit the deployed plugin cache directly, it's faster." | Plugin cache is overwritten on the next update. Always edit the SSOT in `50. AI/04 Skills/`. |
| "I pushed to GitHub so `plugins update` will pick it up automatically." | `plugins update` compares version strings only. Same version means no download. Always bump `.claude-plugin/plugin.json` before pushing. |

## Red Flags

These patterns usually mean the deployment is drifting away from a clean SSOT-first sync.

- `git push` without `git pull --rebase` first
- `git add .` instead of `git add skills/ .claude-plugin/plugin.json`
- Pushing without bumping `.claude-plugin/plugin.json` version
- No deployment summary at the end
- Editing plugin cache copies instead of the SSOT under `50. AI/04 Skills/`

## Verification

After completing the workflow, confirm:

- [ ] Each GitHub-deployed skill has `publish: true` in its `{skill-name}.md` metadata
- [ ] `.claude-plugin/plugin.json` version was incremented
- [ ] `git diff --cached --stat` shows `skills/` and `.claude-plugin/plugin.json` paths only
- [ ] Remote confirmed: `gh api repos/GoBeromsu/agent-skills/contents/skills --jq '.[].name'`
- [ ] Deployment report printed with deployed/skipped counts
- [ ] `claude plugins update agent-skills@beomsu-koh` exits 0 on each intended mirror
- [ ] No direct writes to deployed plugin cache copies occurred during this run
