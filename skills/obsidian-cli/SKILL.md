---
name: obsidian-cli
description: Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.
---

# Obsidian CLI

Use the `obsidian` CLI to interact with a running Obsidian instance. Requires Obsidian to be open.

## Command reference

Run `obsidian help` to see all available commands. This is always up to date. Full docs: https://help.obsidian.md/cli

## Syntax

**Parameters** take a value with `=`. Quote values with spaces:

```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are boolean switches with no value:

```bash
obsidian create name="My Note" silent overwrite
```

For multiline content use `\n` for newline and `\t` for tab.

## File targeting

Many commands accept `file` or `path` to target a file. Without either, the active file is used.

- `file=<name>` — resolves like a wikilink (name only, no path or extension needed)
- `path=<path>` — exact path from vault root, e.g. `folder/note.md`

## Vault targeting

Commands target the most recently focused vault by default. Use `vault=<name>` as the first parameter to target a specific vault:

```bash
obsidian vault="My Vault" search query="test"
```

## When to Use

- User asks to read, create, append, rename, move, or delete vault notes
- User wants to search vault content or list files/tags/tasks
- User needs to update frontmatter properties
- User references a note by name or asks about backlinks/outgoing links
- Renaming or moving a vault file — **always prefer `obsidian rename` / `obsidian move` over Write+Bash rm**

**NOT for:**
- Reading files outside the vault (use Read tool)
- Batch file operations on non-markdown assets (use Bash)
- Plugin/theme development (see Plugin Development section below)

## Common patterns

```bash
# Read / create / edit
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"

# Rename in place (same folder, new name)
obsidian rename file="구글폼 만드는 팁" name="Google Form 설계 체크리스트"

# Move to a different folder (can also rename simultaneously)
obsidian move file="My Note" to="20. Connect/My Note.md"

# Delete (sends to trash by default)
obsidian delete file="My Note"

# Search & discover
obsidian search query="search term" limit=10
obsidian tags sort=count counts
obsidian backlinks file="My Note"

# Daily note
obsidian daily:read
obsidian daily:append content="- [ ] New task"

# Properties & tasks
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
```

Use `--copy` on any command to copy output to clipboard. Use `silent` to prevent files from opening. Use `total` on list commands to get a count.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll use Write + Bash rm to rename — it's simpler" | `obsidian rename` preserves backlinks and sync history. Write+rm breaks wikilinks across the vault. |
| "I'll use Read tool to read the note" | `obsidian read` returns resolved content including transclusions. Use it for vault notes. |
| "I need the exact path so I'll use `path=`" | `file=` resolves like a wikilink — name only works fine and is less fragile when notes move. |

## Red Flags

- Using `Write` + `Bash rm` to rename vault notes instead of `obsidian rename`
- Using `Bash mv` to move vault files instead of `obsidian move`
- Hardcoding full paths with `path=` when `file=` (name-based) would work

## Verification

After vault file operations:
- [ ] `obsidian read file="<new-name>"` returns content without error
- [ ] Old filename no longer resolves (`obsidian file file="<old-name>"` returns not found)
- [ ] Backlinks still resolve (`obsidian backlinks file="<new-name>"`)

## Known Limitations

- **`search` / `search:context` returns empty results via CLI** — operators (`tag:`, `path:`, `file:`) are recognized but produce no output. Use `search:open` to delegate to Obsidian's UI, or use `qmd` for vault search instead.
- **Batch operations freeze after ~400 ops** — health check every 40 operations with `obsidian eval code="'ping'"`. See `references/batch-operations.md` for the full pattern.
- **Requires Obsidian.app to be running** — all commands fail silently or error without the app.

For detailed workarounds and history, see `references/known-limitations.md`.

## Plugin development

### Develop/test cycle

After making code changes to a plugin or theme, follow this workflow:

1. **Reload** the plugin to pick up changes:
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **Check for errors** — if errors appear, fix and repeat from step 1:
   ```bash
   obsidian dev:errors
   ```
3. **Verify visually** with a screenshot or DOM inspection:
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **Check console output** for warnings or unexpected logs:
   ```bash
   obsidian dev:console level=error
   ```

### Additional developer commands

Run JavaScript in the app context:

```bash
obsidian eval code="app.vault.getFiles().length"
```

Inspect CSS values:

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

Toggle mobile emulation:

```bash
obsidian dev:mobile on
```

Run `obsidian help` to see additional developer commands including CDP and debugger controls.
