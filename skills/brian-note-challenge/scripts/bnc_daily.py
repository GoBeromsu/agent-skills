#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import re
import shlex
import shutil
import subprocess
from pathlib import Path

VAULT = "Ataraxia"
BNC_DIR = "15. Work/02 Area/Brian Note challenge"
DASHBOARD_DIR = "10. Time/06 Dashboard"
VAULT_FS = Path.home() / "Documents/01. Obsidian" / VAULT
QUERY = (
    'newer_than:2d from:brian.brain.trinity@gmail.com '
    '("질문입니다" OR "1MNC" OR "Note Challenge" OR "Brian Note Challenge")'
)
os.environ.setdefault("GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND", "file")

KOREAN_RE = re.compile(r"[가-힣]")
INVALID_FILENAME_CHARS = re.compile(r'[?!:*"<>|/\\]+')
DATE_LINK_RE = re.compile(r"\[\[(\d{4}-\d{2}-\d{2})[^\]]*\]\]")


def run(cmd: list[str], check: bool = True) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd, proc.stdout, proc.stderr)
    return proc.stdout


def run_obsidian(args: list[str]) -> str:
    obsidian_bin = shutil.which("obsidian") or "obsidian"
    cmd = [obsidian_bin, *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or proc.stdout.startswith("Error:"):
        raise subprocess.CalledProcessError(proc.returncode or 1, cmd, proc.stdout, proc.stderr)
    return proc.stdout


def run_gws(args: list[str]) -> dict:
    gws_bin = shutil.which("gws") or "gws"
    proc = subprocess.run([gws_bin, *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, [gws_bin, *args], proc.stdout, proc.stderr)
    return json.loads(proc.stdout)


def decode_base64url(data: str) -> str:
    padded = data + "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8", errors="replace")


def extract_plain_text(payload: dict) -> str:
    mime_type = payload.get("mimeType") or ""
    body = payload.get("body") or {}
    data = body.get("data")
    if mime_type.startswith("text/plain") and data:
        return decode_base64url(data)

    for part in payload.get("parts") or []:
        text = extract_plain_text(part)
        if text:
            return text

    if data:
        return decode_base64url(data)
    return ""


def list_candidate_messages() -> list[dict]:
    params = json.dumps({"userId": "me", "q": QUERY, "maxResults": 5}, ensure_ascii=False)
    data = run_gws(["gmail", "users", "messages", "list", "--params", params])
    messages = data.get("messages") or data.get("result", {}).get("messages") or []
    if not isinstance(messages, list):
        return []
    return messages


def fetch_message(message_id: str) -> dict:
    params = json.dumps({"userId": "me", "id": message_id, "format": "full"}, ensure_ascii=False)
    data = run_gws(["gmail", "users", "messages", "get", "--params", params])
    if "payload" in data:
        return data
    return data.get("message") or data.get("result") or data


def strip_outer_quotes(text: str) -> str:
    stripped = text.strip()
    while stripped[:1] in {'"', "“", "”"}:
        stripped = stripped[1:].lstrip()
    while stripped[-1:] in {'"', "“", "”"}:
        stripped = stripped[:-1].rstrip()
    return stripped.strip()


def extract_english_prefix(text: str) -> str:
    if not re.search(r"[A-Za-z]", text):
        return ""
    match = KOREAN_RE.search(text)
    candidate = text[: match.start()] if match else text
    candidate = strip_outer_quotes(candidate).strip()
    return candidate if re.search(r"[A-Za-z]", candidate) else ""


def normalize_lines(body: str) -> list[str]:
    return [line.rstrip() for line in body.replace("\r", "").split("\n")]


def extract_questions(body: str) -> tuple[str, str]:
    q1_ko = ""
    q1_en = ""
    in_q1 = False

    for raw_line in normalize_lines(body):
        line = raw_line.strip()
        if not line:
            continue
        if line in {"1.", "1"}:
            in_q1 = True
            continue
        if in_q1 and line in {"2.", "2"}:
            break
        if not in_q1:
            continue

        cleaned = strip_outer_quotes(line)
        if not cleaned:
            continue
        if not q1_ko and "오늘의" in cleaned and "글귀" in cleaned:
            continue
        if not q1_ko and KOREAN_RE.search(cleaned):
            q1_ko = cleaned
            continue
        if q1_ko and not q1_en:
            candidate_en = extract_english_prefix(cleaned)
            if candidate_en:
                q1_en = candidate_en
                break

    if not q1_ko:
        raise SystemExit("Could not extract Q1 Korean line from BNC email")
    return q1_ko, q1_en


def sanitize_topic(topic: str) -> str:
    sanitized = INVALID_FILENAME_CHARS.sub("", topic).strip()
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized[:100]


def build_note(day: dt.date, q1_ko: str, q1_en: str) -> tuple[str, str]:
    title = f"{day.isoformat()} {sanitize_topic(q1_ko)}"
    lines = [
        "---",
        "tags:",
        "  - brian/notechallenge",
        "aliases: []",
        f"date_created: {day.isoformat()}",
        "type: article",
        'project: "[[Brian Note challenge]]"',
        "---",
        "> [!note]",
        f"> 오늘의 주제: {q1_ko}",
        f"> {q1_en}" if q1_en else ">",
        "",
        "## 1. 공명",
        "> 의식의 흐름에 따라 마음 속의 울림을 먼저 적습니다.",
        "",
        "## 2. 연관 노트",
        "",
        "## 3. 본문",
    ]
    return title, "\n".join(lines) + "\n"


def read_note(path: str) -> str:
    stem = Path(path).stem
    return run_obsidian(["read", f"vault={VAULT}", f"file={stem}"])


def write_note(path: str, content: str) -> None:
    run_obsidian(["create", f"vault={VAULT}", f"path={path}", f"content={content}", "overwrite"])


def existing_same_day_title(day: dt.date) -> str | None:
    pattern = f"{day.isoformat()} *.md"
    matches = sorted((VAULT_FS / BNC_DIR).glob(pattern))
    if matches:
        return matches[0].stem
    return None


def ensure_routine_link(content: str, target_title: str, day: dt.date) -> tuple[str, bool]:
    bullet = f"- [[{target_title}]]"
    lines = content.splitlines()

    routine_idx = next((i for i, line in enumerate(lines) if line.strip() == "## Routine"), None)
    if routine_idx is None:
        insert_idx = next((i for i, line in enumerate(lines) if line.strip().startswith("## ")), len(lines))
        block = ["## Routine", bullet, ""]
        lines[insert_idx:insert_idx] = block
        return "\n".join(lines).rstrip() + "\n", True

    end_idx = len(lines)
    for idx in range(routine_idx + 1, len(lines)):
        if lines[idx].startswith("## "):
            end_idx = idx
            break

    kept: list[str] = []
    changed = False
    day_str = day.isoformat()
    for line in lines[routine_idx + 1 : end_idx]:
        match = DATE_LINK_RE.search(line)
        if match and match.group(1) == day_str:
            changed = True
            continue
        kept.append(line)

    trimmed_kept = [line for line in kept if line.strip()]
    new_block = ["## Routine", bullet]
    if trimmed_kept:
        new_block.extend(trimmed_kept)
    new_block.append("")

    if lines[routine_idx:end_idx] != new_block:
        changed = True
        lines[routine_idx:end_idx] = new_block

    return "\n".join(lines).rstrip() + "\n", changed


def update_dashboard(day: dt.date, title: str) -> bool:
    dashboard_rel = f"{DASHBOARD_DIR}/{day.isoformat()} Dashboard.md"
    try:
        current = read_note(dashboard_rel)
    except subprocess.CalledProcessError:
        return False

    updated, changed = ensure_routine_link(current, title, day)
    if changed:
        write_note(dashboard_rel, updated)
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).date().isoformat())
    args = parser.parse_args()

    day = dt.date.fromisoformat(args.date)
    candidates = list_candidate_messages()
    if not candidates:
        raise SystemExit(f"No BNC email found for date {day.isoformat()}")

    chosen = candidates[0]
    message_id = chosen.get("id")
    if not message_id:
        raise SystemExit("BNC email result did not contain a message id")

    message = fetch_message(message_id)
    body = extract_plain_text(message.get("payload") or {})
    if not body:
        raise SystemExit("Could not decode plain text body from BNC email")

    q1_ko, q1_en = extract_questions(body)
    title, note_content = build_note(day, q1_ko, q1_en)

    existing_title = existing_same_day_title(day)
    if existing_title:
        title = existing_title
    else:
        write_note(f"{BNC_DIR}/{title}.md", note_content)

    dashboard_changed = update_dashboard(day, title)
    print(
        json.dumps(
            {
                "message_id": message_id,
                "title": title,
                "path": f"{BNC_DIR}/{title}.md",
                "dashboard_updated": dashboard_changed,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
