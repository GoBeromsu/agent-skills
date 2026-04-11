---
name: brian-note-challenge
description: Fetch the daily Brian Note Challenge email via gws CLI and create a structured vault note using obsidian CLI. Use when the daily BNC email needs to be ingested into the vault as a note.
---

# BNC (Brian Note Challenge)

## Overview

Fetch today's Brian Note Challenge email from Gmail via `gws` CLI, extract the challenge topic (Q1 Korean + English), and create a vault note using `obsidian` CLI. The note follows the Template structure (공명 / 연관 노트 / 본문) for the user to fill in.

Detailed process reference: `[[Brian Note Challenge Daily (BNC)]]`

## When to Use
- The daily BNC email has arrived and needs to be ingested into the vault
- A past BNC email was missed and needs retroactive ingestion
- Do NOT use for general email triage or non-BNC emails
- Do NOT use for manual note creation without an email source

### Prerequisites
- `gws` CLI installed and authenticated (`gws auth login`)
- Obsidian running (required for `obsidian` CLI)

## Process

### Step 1 — Determine Target Date

Determine target date `D` in KST (format: `YYYY-MM-DD`). Default: today.

### Step 2 — Gmail Fetch & Parse

1. Search for the newest matching email:
   ```
   gws gmail users messages list --params '{"userId":"me","q":"newer_than:2d from:brian.brain.trinity@gmail.com (\"질문입니다\" OR \"1MNC\" OR \"Note Challenge\" OR \"Brian Note Challenge\")","maxResults":5}'
   ```
2. Pick the newest message id.
3. Fetch the full message:
   ```
   gws gmail users messages get --params '{"userId":"me","id":"<MESSAGE_ID>","format":"full"}'
   ```
4. Decode the first `text/plain` MIME part from `payload.parts` (base64url).
5. Parse the plain text body:
   - Find line `1.` (or `1`).
   - Q1 Korean = first line after that containing `?` and at least one Hangul character.
   - Q1 English = next line containing `?` and ASCII letters.
6. If no matching email found (query returns 0 results): stop and report "no BNC email found for date `D`".
7. If parsing fails (no Q1 Korean topic found): stop and report the error. Do NOT guess.

### Step 3 — Sanitize Topic for Filename

Remove `[?!:*"<>|/\\]`, collapse multiple spaces, trim leading/trailing spaces, limit to 100 characters. Result = `T`.

### Step 4 — Create Note

Target path: `15. Work/02 Area/Brian Note challenge/${D} ${T}.md`

1. **Duplicate check**: glob `${D} *.md` in `15. Work/02 Area/Brian Note challenge/`. If a same-date note exists, skip creation.
2. **Create note** via obsidian CLI:
   ```
   obsidian create path="15. Work/02 Area/Brian Note challenge/${D} ${T}.md" vault="Ataraxia" content="..."
   ```
3. **Note content**:
   ```markdown
   ---
   tags:
     - brian/notechallenge
   aliases: []
   date_created: ${D}
   type: article
   up: "[[Brian Note challenge]]"
   ---
   > [!note]
   > 오늘의 주제: ${Q1_KOREAN}
   > ${Q1_ENGLISH}

   ## 1. 공명
   > 의식의 흐름에 따라 마음 속의 울림을 먼저 적습니다.

   ## 2. 연관 노트

   ## 3. 본문
   ```
4. If `obsidian create` fails (e.g., Obsidian not running): log the error and stop. Do not attempt Dashboard update.

### Step 5 — Update Dashboard

Under `## Routine` in `10. Time/06 Dashboard/${D} Dashboard.md`, ensure exactly one bullet:
```
- [[${D} ${T}]]
```

If a legacy link (e.g. `[[YYYY-MM-DD Brian note challenge]]`) or another same-date Brian link already exists, replace it. Never create duplicates.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Extraction is simple, skip the parsing logic." | Email format varies between sends. Robust heuristic parsing prevents silent data corruption. |
| "Duplicate check is overkill for a daily skill." | Re-runs and retries happen. The check prevents double-creation. |
| "Dashboard update can wait." | Routine tracking breaks if the wikilink is missing from the daily dashboard. |
| "I can hardcode the email query." | The sender uses varying subject lines. The OR-based query handles all known variants. |

## Red Flags
- Note created without running a duplicate check first
- Hardcoded email queries missing the standard OR filter terms
- Missing Q1 English line in callout (only Korean topic shown)
- Wrong tag casing: `brian/noteChallenge` instead of `brian/notechallenge`
- Frontmatter uses array notation `[brian/notechallenge]` instead of indented YAML list
- use `date_created:` only

## Verification

	After completing the process, confirm:
- [ ] `gws` query returned a matching email
- [ ] Q1 Korean + Q1 English extracted correctly from email body
- [ ] Duplicate check ran before note creation
- [ ] Note exists at `15. Work/02 Area/Brian Note challenge/${D} ${T}.md`
- [ ] Frontmatter has `brian/notechallenge` (lowercase), `date_created:`, `type: article`, `up:`
- [ ] Note content has callout (Korean + English) → 공명 → 연관 노트 → 본문
- [ ] Dashboard `## Routine` updated with `[[${D} ${T}]]` wikilink
