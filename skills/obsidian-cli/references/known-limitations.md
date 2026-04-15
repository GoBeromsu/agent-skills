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

See `references/batch-operations.md` for the full pattern including round-trip rename.

## Obsidian.app must be running

All CLI commands require a running Obsidian instance. Commands fail silently or return errors without the app.

## Undocumented flags

Some flags work but are not listed in `obsidian help`:

- **`silent`** — confirmed working on `create` (suppresses UI navigation to the created file). May work on other commands that open files. Not in help output.

Previously documented flags that could not be verified:
- **`--copy`** — was documented as copying output to clipboard. Not present in help output, behavior unconfirmed. Removed from skill documentation.

## Fabricated commands (removed)

The following commands were previously documented in the skill but do not exist in the CLI:

- **`daily:read`** — `No commands matching "daily:read"`. No `daily` namespace exists.
- **`daily:append`** — `No commands matching "daily:append"`.
- **`trash`** — never existed. The correct command is `delete` (sends to system trash by default, use `permanent` flag for permanent deletion).

**Alternative for daily notes:** Use `obsidian command id="daily-notes"` to open/create the daily note, then `obsidian read`/`obsidian append` on the daily note file. Or use `obsidian tasks daily` to list tasks from the daily note.

## Resolved limitations

### `create path=` with `. ` in folder names — FIXED (confirmed 2026-04-15)

Previously, `create path=` failed on folder names containing `. ` (e.g., `00. Calendar/`). This has been fixed in the current version. No workaround needed.
