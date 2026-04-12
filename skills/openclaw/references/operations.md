# OpenClaw Operations Reference

Read this file when you need architecture context, agent composition details, troubleshooting tips, or session protocol beyond the core workflow in SKILL.md.

## Architecture Context

| Component | Role | Port | Process Manager |
|-----------|------|------|-----------------|
| OpenClaw Gateway | Messenger → agent routing | 18789 | launchd |
| clawhip daemon | Event routing + notification | 25294 | nohup (launchd pending) |
| OMX | Code execution in tmux | — | tmux session |

OpenClaw is the "지휘자" (conductor): receives Discord/Telegram/Slack messages → routes to the appropriate agent → returns responses. It does not execute code directly.

## Agent Composition

| Agent | Role | Notes |
|-------|------|-------|
| main | Default routing, general conversation | Orchestrator |
| xia-pkm | Vault knowledge work (GDR, BNC, QT) | |
| xia-researcher | External source collection (FYC, GPP) | |
| xia-calendar | Schedule management | |
| xia-pkm-roundup | PKM digest | |
| obsidian-maestro | Obsidian workspace orchestration | OMX dispatch via clawhip |

**Bootstrap files** (injected into context window on every turn, loaded from **workspace** directory):

| File | Role | Location |
|------|------|----------|
| SOUL.md | 말투, 톤, 스타일 ("voice, stance, and style") | workspace root |
| IDENTITY.md | 이름, 이모지, 아바타 (메타데이터) | workspace root |
| AGENTS.md | 운영 규칙 ("operating rules") | workspace root |
| TOOLS.md | 로컬 설정 (SSH hosts, API keys) | workspace root |
| USER.md | 사용자 선호/맥락 | workspace root |
| HEARTBEAT.md | 주기적 체크 항목 | workspace root |
| MEMORY.md | 장기 기억 (main session only) | workspace root |

- 개별 파일 최대 20KB (`agents.defaults.bootstrapMaxChars`)
- 전체 주입량 최대 150KB (`bootstrapTotalMaxChars`)
- Sub-agent 세션은 AGENTS.md + TOOLS.md만 수신 (경량화)
- **말투/성격 변경 = SOUL.md 수정** (매 턴 주입되므로 새 세션에서 즉시 반영, Gateway 재시작 불필요)
- **이름/정체성 = SOUL.md + IDENTITY.md 모두 설정** (SOUL.md에 "나는 X이다"를 명시해야 모델이 강하게 인식)
- Bootstrap 파일은 **workspace** 디렉토리에서 로딩됨 (agentDir 아님). 경로: `openclaw.json` → `agents.list[].workspace`
- 파일 누락 시 "missing file marker"가 세션에 주입되어 에이전트가 빈 상태로 동작

## Session Protocol

Every agent, every session:
1. Read SOUL.md (identity)
2. Read USER.md (preferences)
3. Read `memory/YYYY-MM-DD.md` (recent context, skip silently if missing)
4. Main session only: read MEMORY.md (security — not loaded in shared contexts)

## Heartbeat vs Cron

| Aspect | Heartbeat | Cron |
|--------|-----------|------|
| Timing | Conversational, can drift | Exact (e.g., "9:00 AM sharp") |
| Isolation | Within agent session | One-shot, isolated |
| Config | `agents.list[].heartbeat.every` | System `crontab -e` |
| State | `memory/heartbeat-state.json` | Stateless |
| Use for | Batch checks (email, calendar, mentions) | Scheduled tasks (FYC, reminders) |

## Troubleshooting (삽질 기록)

### IDENTITY.md vs SOUL.md
- IDENTITY.md = 이름, 이모지, 아바타 등 메타데이터. 없으면 기본 identity 사용 (e.g., "xia" instead of "maestro").
- SOUL.md = 말투, 톤, 성격. 없으면 기본 어조 사용. 고어체 등 말투 변경은 SOUL.md에서.
- 둘 다 workspace root에 위치해야 매 턴 주입됨.
- maestro가 xia로 응답했던 삽질: IDENTITY.md가 없어서 기본 identity 사용. agent dir에 IDENTITY.md 생성으로 해결.

### Workspace vs AgentDir — bootstrap 파일 위치
Bootstrap 파일(SOUL.md, IDENTITY.md, USER.md 등)은 **workspace** 디렉토리에서 로딩된다. agentDir(`~/.openclaw/agents/<id>/agent/`)에 넣으면 로딩되지 않는다. 삽질: agentDir에만 IDENTITY.md를 넣고 "왜 에이전트가 이름을 모르지?"로 몇 시간 소모. workspace 경로 확인: `openclaw.json` → `agents.list[].workspace`.

### Guild channel allowlist
Binding a channel to an agent is necessary but not sufficient. The channel must also appear in the guild's channel allowlist on the Discord bot configuration. Missing this causes a silent failure pattern: gateway receives the message, routes to agent, agent responds, but the response never appears in Discord.

### Obsidian CLI in cron
Cron jobs that use obsidian CLI must export the correct PATH:
```bash
export PATH="/opt/homebrew/bin:$PATH"
```
The obsidian CLI binary locations on m1-pro:
- `/opt/homebrew/bin/ob` — obsidian-headless
- `/opt/homebrew/bin/obsidian` — obsidian CLI symlink

### Context window safety
- At 70% context usage: agent auto-saves critical context to memory
- At 85%: flush and recommend session reset
- Previous issue: timeout loops caused context exhaustion. Avoid retry loops without bounded limits.

### Gateway is launchd-managed
Unlike clawhip (nohup, pending migration), OpenClaw Gateway runs under launchd and auto-restarts on crash or reboot. Do not manage it with nohup or manual process control.

### BOOTSTRAP.md vs AGENTS.md
- **BOOTSTRAP.md** = one-time file. Deleted after initial bootstrapping. Do NOT put persistent operational rules here.
- **AGENTS.md** = loaded every session. All persistent rules (dispatch logic, session naming, mandatory flags) go here.
- Putting rules in BOOTSTRAP.md causes them to disappear after the first session. This was a common early mistake.

### Maestro OMX Dispatch — 지능형 릴레이 패턴
OpenClaw maestro acts as an intelligent relay: Discord message → maestro (LLM) judges intent → selects OMX skill → executes `clawhip deliver --session maestro-work --prompt '$skill "..."'` → clawhip injects into tmux → OMX runs.

AGENTS.md must contain explicit dispatch rules:
- **Session name**: Fixed to `maestro-work` (prevents maestro from inventing names like `maestro-globalcheck`)
- **Mandatory flags**: `omx --madmax --high` (without `--madmax`, all MCP tool calls fail with "user cancelled" in headless mode)
- **Skill selection**: Table mapping request types to skills (`$ralph` for implementation, `$deep-interview` for exploration, `$ralplan` for planning, `$team N:executor` for parallel work)
- **Forbidden patterns**: `$executor` and `$architect` are agent roles, not standalone skills

### Session reset after AGENTS.md changes
Modifying AGENTS.md requires both Gateway restart and session clearing:
1. Gateway restart: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`
2. Session clear: `rm ~/.openclaw/agents/<name>/sessions/*.jsonl`
3. Session cleanup: `openclaw sessions cleanup --agent <name> --fix-missing --enforce`
Without this, existing sessions continue using the cached old AGENTS.md.

### Workspace directory structure
workspace and code repo must be separate. If workspace points directly at the code repo, bootstrap files mix into the repo.
```
~/.openclaw/workspace/obsidian-maestro/       ← workspace (bootstrap files)
├── AGENTS.md, IDENTITY.md, SOUL.md, TOOLS.md, USER.md
└── obsidian-workspace/                       ← code repo (submodule monorepo)

~/.openclaw/agents/obsidian-maestro/agent/    ← runtime only (auth, sessions)
```
The workspace path is set in `openclaw.json` → `agents.list[].workspace`.
