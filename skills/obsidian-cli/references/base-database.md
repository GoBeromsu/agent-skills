# Obsidian CLI — Base (Database)

Commands for querying and managing Obsidian Bases (database views built on top of vault notes).

## bases

List all base files in vault. No parameters.

```bash
obsidian bases
```

**Tip:** Bases are Obsidian's structured data views (like Notion databases). Each base is a file in the vault that defines views over notes.

## base:create

Create a new item in a base.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | Base file name |
| path=\<path\> | Base file path |
| view=\<name\> | View name |
| name=\<name\> | New file name |
| content=\<text\> | Initial content |
| open | Open file after creating |
| newtab | Open in new tab |

```bash
obsidian base:create file="Projects" name="New Project" content="# New Project"
obsidian base:create file="Tasks" view="Active" name="Fix Bug" open
```

**Tip:** Creates a new note that appears in the specified base view. Use `view=` to target a specific view within the base.

## base:query

Query a base and return results.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | Base file name |
| path=\<path\> | Base file path |
| view=\<name\> | View name to query |
| format=json\|csv\|tsv\|md\|paths | Output format (default: json) |

```bash
obsidian base:query file="Projects" format=json
obsidian base:query file="Tasks" view="Active" format=md
obsidian base:query file="Reading List" format=paths
```

**Tip:** `format=md` returns a markdown table — useful for embedding results. `format=paths` returns just file paths — useful for piping to other commands. `format=json` gives full structured data for programmatic use. Use `view=` to query a specific view (filtered/sorted subset).

## base:views

List views in a base file. Defaults to active file if no file specified.

```bash
obsidian base:views
obsidian base:views file="Projects"
```

**Tip:** Use this to discover available views before querying with `base:query view=`.
