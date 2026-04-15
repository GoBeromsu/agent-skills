# Obsidian CLI — Commands & Hotkeys

Commands for executing Obsidian commands and managing hotkeys.

## command

Execute an Obsidian command.

| Parameter | Description |
|-----------|-------------|
| id=\<command-id\> | Command ID to execute (required) |

```bash
obsidian command id="editor:toggle-bold"
obsidian command id="app:toggle-left-sidebar"
obsidian command id="daily-notes"
```

**Tip:** This is extremely powerful — it can trigger any registered command in Obsidian, including those from plugins. Use `commands` to discover available command IDs. This enables automation of any action that has a command palette entry.

## commands

List available commands.

| Parameter | Description |
|-----------|-------------|
| filter=\<prefix\> | Filter by ID prefix |

```bash
obsidian commands
obsidian commands filter=editor
obsidian commands filter=app
obsidian commands filter=daily
```

**Tip:** Use `filter=` to narrow results by command namespace. Common prefixes: `editor:` (editing), `app:` (application), `workspace:` (layout), `file-explorer:` (sidebar). Plugin commands use the plugin ID as prefix (e.g., `dataview:`, `templater-obsidian:`).

## hotkey

Get hotkey for a command.

| Parameter | Description |
|-----------|-------------|
| id=\<command-id\> | Command ID (required) |
| verbose | Show if custom or default |

```bash
obsidian hotkey id="editor:toggle-bold"
obsidian hotkey id="app:toggle-left-sidebar" verbose
```

**Tip:** Use `verbose` to see whether the hotkey is a custom user binding or the default.

## hotkeys

List hotkeys.

| Parameter | Description |
|-----------|-------------|
| total | Return hotkey count |
| verbose | Show if hotkey is custom |
| format=json\|tsv\|csv | Output format (default: tsv) |
| all | Include commands without hotkeys |

```bash
obsidian hotkeys
obsidian hotkeys verbose format=json
obsidian hotkeys all total
```

**Tip:** By default only shows commands that have hotkeys assigned. Use `all` to include commands without hotkeys — useful for finding unbound commands you might want to assign shortcuts to.
