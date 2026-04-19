---
name: deploy-quartz
description: Use when you need to publish Obsidian notes to the Quartz static site at berom.net, including pre-deploy markdown transformation, staging content, Eagle image processing, building, git push, and post-push live verification.
---

# Deploy Quartz

## Overview

This skill deploys Obsidian notes to the Quartz static site at `berom.net`. The Blog repository path is read from `QUARTZ_REPO_PATH` in the Ataraxia vault `.env` file. Articles go directly into `content/Articles/`. Eagle image processing runs only when `file:///` paths are detected.

The AI's role is to invoke `scripts/deploy.sh` and report results. All complex logic lives in the script.

Success is not declared until: (1) `npx quartz build` exits 0, (2) `git push` succeeds, (3) the GitHub Actions workflow exits 0, and (4) a `curl` to the live permalink returns HTTP 200 with a page-specific content marker.

## When to Use

- Use when the user says "배포", "배포해줘", "deploy", "publish", "/deploy-quartz", "/deploy", "사이트에 올려줘", "블로그에 발행", or wants to push content to `berom.net`.
- Use when the user provides a specific note path and asks to deploy it.
- Do not use for Tistory or Naver blog publishing.

## Process

### Configuration

All configuration is loaded from `.env` at the Ataraxia vault root.

| Variable | Description | Value |
|---|---|---|
| `QUARTZ_REPO_PATH` | Blog vault (Quartz repo) path | Set in `.env` |
| `EAGLE_LIBRARY_PATH` | Eagle library path | Set in `.env` |
| `DEPLOY_SITE_URL` | Site URL | `https://berom.net` |
| `DEPLOY_GIT_BRANCH` | Git branch | `v4` |
| `DEPLOY_GIT_REMOTE` | Git remote | `origin` |

Validate `QUARTZ_REPO_PATH` is set and the path exists before proceeding. It can go stale after directory reorganization.

Upstream reference: `jackyzha0/quartz` default branch `v4`. GitHub Pages environment `github-pages` on `GoBeromsu/Quartaz` enforces branch policy `v4` only. Workflow trigger must be on `v4`.

---

### Pre-Deploy Transformation

Apply all rules below to a **temporary copy** of the source note. The vault SSOT file is never modified. The transformed copy is what gets written to `content/Articles/`.

#### 1. Frontmatter Cleanup

**Fields to keep:** `aliases`, `date_created`, `date_modified`, `description`, `tags`, `type`, `permalink`, `title`.

**Fields to remove:** `moc`, `project`, and any field whose value is itself a wikilink (e.g., `project: "[[Some Note]]"`).

**Require `title`:** If the field is absent, set it to the filename minus the `.md` extension.

**Require `permalink`:** If the field is absent, derive it: lowercase the title, replace spaces with `-`, strip non-ASCII characters, collapse consecutive `-` into one. Example: `"My AI Post 2026"` → `my-ai-post-2026`. The `permalink` value is used throughout subsequent steps — capture it as `$PERMALINK`.

#### 2. Wikilink Transformation (body only)

Process every `[[...]]` occurrence after frontmatter has been extracted.

**Case A — External blog wikilinks** (links to articles that have a `source_url` in the References vault):

1. Parse the wikilink: `[[Note Title|display text]]` or `[[Note Title]]`.
2. Look up `Ataraxia/80. References/04 Articles/<Note Title>.md`.
3. Read its frontmatter. If a `source_url` field exists and is a non-empty URL:
   - Replace with `[display text](source_url)` (or `[Note Title](source_url)` when no alias).
4. If the file does not exist or has no `source_url`:
   - Replace with plain text: the display alias if present, otherwise the note title. Strip `[[ ]]` entirely.

**Case B — Internal terminology / concept wikilinks** (vault notes that are not external blog articles):

Applies to wikilinks pointing to notes under `50. AI/02 Terminologies/`, event notes (e.g., `2026 JNU x Upstage Skillthon`), and any other vault-internal note that is not an external article:

- Replace with plain text: the alias after `|` if present, otherwise the note title. Strip `[[ ]]` entirely.

**Decision order:** Check Case A first (lookup in `80. References/04 Articles/`). If the file exists there, apply Case A. Otherwise apply Case B.

#### 3. References Section Aggregation

After wikilink transformation:

1. Scan the full transformed body for all inline Markdown links: `[text](url)`.
2. Collect all unique URLs (deduplicate, order of first appearance).
3. If a `## References` section already exists:
   - Keep any list items that are standard Markdown links. Remove any remaining wikilink items (apply the same Case A / Case B rules to convert or strip them).
   - Append any new URLs not already listed.
4. If no `## References` section exists, append one at the end of the document:
   ```markdown
   ## References

   - [url](url)
   - ...
   ```
   Use the URL itself as the link text when no better label is available.

---

### Single File Deploy (most common)

When the user specifies a file to deploy:

```bash
# Load config
source "/Users/beomsu/Documents/01. Obsidian/Ataraxia/.env"

# Apply pre-deploy transformation to a temp copy, then copy to content directory
# (Transformation rules: see "Pre-Deploy Transformation" above)
cp "TRANSFORMED_TEMP_COPY.md" "$QUARTZ_REPO_PATH/content/Articles/"

# Process Eagle images if needed (only if file:/// paths present)
cd "$QUARTZ_REPO_PATH"
node "50. AI/04 Skills/deploy-quartz/scripts/process-eagle-images.mjs"

# Build
npx quartz build

# Stage ONLY content and attachments — NEVER git add .
git add content/
git add _attachments/

git commit -m "feat: add Article Name"
git push origin v4
```

After `git push`, proceed to **Post-Push Verification** before reporting success.

### Full Deploy (via script)

```bash
"50. AI/04 Skills/deploy-quartz/scripts/deploy.sh"
```

The `deploy.sh` script handles:
1. `.env` config loading
2. Pre-deploy transformation (wikilinks, frontmatter, References section)
3. Eagle image processing (skipped if no `file:///` paths found)
4. Quartz build via `npx quartz build`
5. Selective `git add content/` + `git add _attachments/`
6. Auto-generated commit message and push to `origin v4`
7. Post-push GitHub Actions watch and live URL verification

For staging-specific preparation, use `prepare-staging.sh` before `deploy.sh`.

### Eagle Image Processing

Only runs when markdown files contain Eagle `file:///` paths. The `process-eagle-images.mjs` script:
- Scans content for Eagle image references
- Copies images from the Eagle library to `_attachments/`
- Rewrites markdown paths to use relative `/_attachments/` paths

Plain markdown without Eagle paths skips this step entirely.

---

### Post-Push Verification

Do not report success until all three checks below pass.

#### Step 1 — Watch GitHub Actions

```bash
cd "$QUARTZ_REPO_PATH"
gh run watch --exit-status $(gh run list --branch v4 --limit 1 --json databaseId --jq '.[0].databaseId')
```

- If the workflow exits non-zero, treat it as a deployment failure (see **On Failure**). Do not auto-revert.
- Capture the run ID and the Actions URL (`https://github.com/<owner>/<repo>/actions/runs/<id>`) for the success report.

#### Step 2 — Verify Live URL (HTTP 200)

Construct the URL from `DEPLOY_SITE_URL` and the article's `$PERMALINK`:

```bash
URL="${DEPLOY_SITE_URL}/${PERMALINK}"
STATUS=$(curl -sS -o /dev/null -w '%{http_code}' "$URL")
```

Require `STATUS` to equal `200`. Retry up to **5 times** with **20-second backoff** to allow for CDN propagation. If all 5 attempts fail, surface the last HTTP status code and ask the user before proceeding.

#### Step 3 — Content Check (not a 404 fallback)

After a 200 response, confirm the body contains a page-specific marker:

```bash
curl -sS "$URL" | grep -q "${PERMALINK}" && echo OK
```

If `grep` fails (the page is a generic Quartz 404 fallback that returns 200), report the failure with the raw HTML excerpt and ask the user.

---

### On Success

Report to user:
- Commit hash and message
- GitHub Actions workflow run ID and URL
- HTTP 200 confirmation for `${DEPLOY_SITE_URL}/${PERMALINK}`
- Live-check timestamp (UTC)
- "배포 완료!" confirmation
- Site URL: `https://berom.net`

### On Failure

Distinguish failure type before acting:

| Failure point | Action |
|---|---|
| Pre-deploy transformation error | Fix in temp copy, do not touch vault SSOT. Retry. |
| `npx quartz build` exits non-zero | Auto-revert: `git revert HEAD --no-edit && git push origin v4`. Report build log. |
| `git push` fails | Auto-revert if a commit was made. Report push error. |
| **GitHub Actions workflow fails** | **Do NOT auto-revert.** Surface the Actions log excerpt below and ask user how to proceed. |
| Live URL returns non-200 after 5 retries | Report last HTTP status and ask user. Do not auto-revert. |
| Content check fails (404 fallback body) | Report raw HTML excerpt and ask user. Do not auto-revert. |

Auto-revert command (local build / push failures only):

```bash
cd "$QUARTZ_REPO_PATH" && git revert HEAD --no-edit && git push origin v4
```

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "`git add .` is faster and I know what I'm committing." | Broad staging sweeps in `.omc/`, `AGENTS.md`, build artifacts, and other local noise into the deploy commit. |
| "Asset processing can always run — it won't hurt if there are no Eagle paths." | Conditional processing is explicit. Unconditional processing masks errors when the Eagle library path is stale. |
| "The branch is probably still v4, no need to check." | `DEPLOY_GIT_BRANCH` is the source of truth. Hardcoding the branch causes silent pushes to the wrong branch after config changes. |
| "Push succeeded, so the site must be updated." | GitHub Actions may still be running or may fail silently. Always watch the run until it exits 0 before reporting live. |
| "A 200 response means my page is live." | Quartz can return 200 for a generic fallback. Always grep the body for a page-specific marker. |

## Red Flags

- `git add .` anywhere in the deploy workflow — only `git add content/` and `git add _attachments/` are allowed.
- Pushing without running `npx quartz build` first — build errors must block the push.
- Not loading `.env` before accessing `QUARTZ_REPO_PATH` — the path will be empty and the deploy will silently fail or corrupt the wrong directory.
- Skipping the empty-diff check — committing with nothing staged creates an empty commit.
- Modifying the vault SSOT file during transformation — always work on a temp copy.
- Reporting "배포 완료!" before `gh run watch` exits 0 and the live URL check passes.

## Verification

- [ ] `.env` loaded and `QUARTZ_REPO_PATH` resolves to an existing directory.
- [ ] Wikilinks transformed per rules before copying to `content/Articles/` (temp copy used; vault SSOT unchanged).
- [ ] `permalink` and `title` present in frontmatter of the deployed copy.
- [ ] `moc`, `project`, and wikilink-valued frontmatter fields removed from deployed copy.
- [ ] References section contains all body URLs, deduped, with no remaining unresolved wikilinks.
- [ ] Only `content/` and `_attachments/` staged — confirmed with `git diff --cached --name-only`.
- [ ] `npx quartz build` exits 0 before `git push`.
- [ ] `gh run watch` exited 0 (GitHub Actions workflow succeeded).
- [ ] `curl` on `${DEPLOY_SITE_URL}/<permalink>` returned 200.
- [ ] Response body contains permalink/title marker (not a 404 fallback page).
- [ ] Commit hash, Actions run URL, HTTP 200 confirmation, live-check timestamp, and site URL (`https://berom.net`) reported to user.
- [ ] If `git diff --cached` is empty after staging, inform user the site is already up to date instead of creating an empty commit.
