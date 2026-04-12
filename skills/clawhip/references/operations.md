# clawhip Operations Reference

Read this file when you need architecture context, troubleshooting tips, or daemon lifecycle details beyond the core workflow in SKILL.md.

## Architecture Context

```
[Discord (사용자)] → [OpenClaw maestro] → [clawhip deliver] → [OMX (tmux)]
                                                                    ↓
                                              [clawhip daemon 감시] → [Discord 알림]
```

| Component        | Role                         | Port  | Process Manager         |
| ---------------- | ---------------------------- | ----- | ----------------------- |
| clawhip daemon   | Event routing + notification | 25294 | nohup (launchd pending) |
| OpenClaw Gateway | Messenger → agent routing    | 18789 | launchd                 |
| OMX              | Code execution in tmux       | —     | tmux session            |

clawhip and OpenClaw use **separate Discord bots**. This separation prevents high-frequency notifications (commits, keywords, stale alerts) from polluting the conversational bot's context.

## Troubleshooting (삽질 기록)

### TOML config pitfalls
- `[[monitors.git]]` is wrong — clawhip uses event-based git monitoring, not polling. This TOML key causes silent parse errors.
- Route `event` fields use dot notation with glob: `github.*`, `tmux.*`, `agent.*`, `session.*`.
- Legacy `[discord]` config is still accepted but prefer `[providers.discord]`.

### Channel binding silent failure
When adding a new channel for routing, the channel must also be registered in the guild channel allowlist on the Discord bot side. Missing this causes silent delivery failure — the daemon reports success but no message appears.

### Daemon lifecycle
- Currently runs via `nohup clawhip &`. Survives terminal close but not reboot.
- Pending migration: register as launchd service for auto-start on boot.
- After m1-pro reboot, manually restart: `nohup clawhip > /tmp/clawhip.log 2>&1 &`

### Session naming
- Session names are operator labels, not routing authority. Route filtering should use project metadata (`filter = { repo = "..." }`) not session names.
- Broad prefix monitors like `clawhip*` overlap with launcher-registered watches and create stale/keyword noise.

### deliver safety
- `clawhip deliver` refuses arbitrary shells — it requires repo-local prompt-submit-aware hook setup.
- Install hooks first: `clawhip hooks install --all --scope project`
- deliver retries Enter keypresses (bounded by `--max-enters`) until `.clawhip/state/prompt-submit.json` changes.

### Keyword matching is case-insensitive
clawhip keyword matching ignores case. `Error:` also matches `error`, `ERROR`, etc. This causes massive false positives when code analysis text contains the word "error". Recommended keyword set: `FAILED,panic,BLOCKED,PR created,PR merged`. Avoid: `error`, `Error:`, `complete`, `done`.

### Watch process stacking
`clawhip tmux watch` spawns a **new background process** per registration. It does NOT replace or kill previous watches for the same session. If you re-register a watch, old processes continue firing with their original keywords. Always kill old PIDs before re-registering:
```bash
ps aux | grep 'clawhip.*tmux.*watch.*<session-name>' | grep -v grep | awk '{print $2}' | xargs kill
clawhip tmux watch -s <session-name> --keywords '...' --stale-minutes 30
```

### OMX process tree cleanup
Sending `exit` to a tmux pane may not kill the full OMX process tree (codex binary, MCP servers, explore harnesses, notify watchers). To cleanly restart OMX:
```bash
# Find all OMX-related processes
ps aux | grep -E 'omx|oh-my-codex' | grep -v grep
# Kill the main omx process and its children
kill <omx-pid> <codex-pid> <mcp-pids...>
# Then start fresh in the tmux pane
tmux send-keys -t <session-name> 'omx --madmax --high' Enter
```

### Recommended stale interval
Default stale is 10 minutes — too noisy for long-running OMX sessions. Use 30 minutes for active work sessions. Use `--stale-minutes 0` to disable stale alerts entirely for monitoring-only watches.
