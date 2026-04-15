# Obsidian CLI — Known Limitations

## Search returns empty results (confirmed 2026-04-15)

`obsidian search query="..."` and `search:context` return exit 0 but no output for any query. Search operators (`tag:`, `path:`, `file:`) are recognized without error; `type:` gives "Operator not recognized". Despite operator parsing, no results are returned regardless of query.

**Workaround:** Use `search:open query="term"` to open Obsidian's built-in search UI, or use `qmd` for CLI-based vault search.

**Status:** Unresolved. May be an indexing or IPC issue.

## Batch operations freeze (~400 ops)

Sequential rename/move operations cause Obsidian to freeze after approximately 400 operations. The app becomes unresponsive to CLI commands.

**Workaround:** Health check every 40 operations:
```bash
obsidian vault=Ataraxia eval code="'ping'"
# empty response = frozen — restart:
pkill -f Obsidian && sleep 3 && open -a Obsidian && sleep 6
```

## Obsidian.app must be running

All CLI commands require a running Obsidian instance. Commands fail silently or return errors without the app.

## Resolved limitations

### `create path=` with `. ` in folder names — FIXED (confirmed 2026-04-15)

Previously, `create path=` failed on folder names containing `. ` (e.g., `00. Calendar/`). This has been fixed in the current version. No workaround needed.

### `trash` command — never existed

The `trash` command was incorrectly documented. The correct command is `delete`:
```bash
obsidian delete file="Note"           # sends to system trash
obsidian delete file="Note" permanent # permanently deletes
```
