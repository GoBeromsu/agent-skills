# Obsidian CLI — Properties, Tags & Tasks

Commands for managing frontmatter properties, vault tags, and task items.

## properties

List properties in the vault.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | Show properties for file |
| path=\<path\> | Show properties for path |
| name=\<name\> | Get specific property count |
| total | Return property count |
| sort=count | Sort by count (default: name) |
| counts | Include occurrence counts |
| format=yaml\|json\|tsv | Output format (default: yaml) |
| active | Show properties for active file |

```bash
obsidian properties file="My Note"
obsidian properties sort=count counts
obsidian properties name="status" total
```

**Tip:** Without `file=` or `path=`, lists all properties across the entire vault. Use `sort=count counts` to find the most common properties.

## property:read

Read a property value from a file.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Property name (required) |
| file=\<name\> | File name |
| path=\<path\> | File path |

```bash
obsidian property:read name="status" file="My Note"
obsidian property:read name="tags" file="Project"
```

**Tip:** Returns the raw property value. For list properties (like tags), returns the full list.

## property:set

Set a property on a file.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Property name (required) |
| value=\<value\> | Property value (required) |
| type=text\|list\|number\|checkbox\|date\|datetime | Property type |
| file=\<name\> | File name |
| path=\<path\> | File path |

```bash
obsidian property:set name="status" value="done" file="My Note"
obsidian property:set name="priority" value="1" type=number file="Task"
obsidian property:set name="reviewed" value="true" type=checkbox file="Draft"
```

**Tip:** If the property doesn't exist, it's created. Use `type=` to ensure correct frontmatter typing. Without `type=`, the value is stored as text.

## property:remove

Remove a property from a file.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Property name (required) |
| file=\<name\> | File name |
| path=\<path\> | File path |

```bash
obsidian property:remove name="draft" file="Published Note"
```

## tags

List tags in the vault.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| total | Return tag count |
| counts | Include tag counts |
| sort=count | Sort by count (default: name) |
| format=json\|tsv\|csv | Output format (default: tsv) |
| active | Show tags for active file |

```bash
obsidian tags sort=count counts
obsidian tags file="My Note"
obsidian tags total
```

**Tip:** Without `file=`, lists all tags across the vault. `sort=count counts` gives a frequency-sorted tag overview — useful for vault auditing.

## tag

Get tag info for a specific tag.

| Parameter | Description |
|-----------|-------------|
| name=\<tag\> | Tag name (required) |
| total | Return occurrence count |
| verbose | Include file list and count |

```bash
obsidian tag name="project" verbose
obsidian tag name="review" total
```

**Tip:** Use `verbose` to get the full list of files using this tag.

## tasks

List tasks in the vault.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | Filter by file name |
| path=\<path\> | Filter by file path |
| total | Return task count |
| done | Show completed tasks |
| todo | Show incomplete tasks |
| status="\<char\>" | Filter by status character |
| verbose | Group by file with line numbers |
| format=json\|tsv\|csv | Output format (default: text) |
| active | Show tasks for active file |
| daily | Show tasks from daily note |

```bash
obsidian tasks todo
obsidian tasks todo verbose
obsidian tasks file="Project Plan" done
obsidian tasks daily todo
obsidian tasks status="/" verbose
```

**Tip:** `todo` and `done` filter by completion. `daily` scopes to the current daily note. Use `status="/"` for custom task statuses (e.g., in-progress). `verbose` groups output by file with line numbers — useful for locating specific tasks.

## task

Show or update a single task.

| Parameter | Description |
|-----------|-------------|
| ref=\<path:line\> | Task reference (path:line) |
| file=\<name\> | File name |
| path=\<path\> | File path |
| line=\<n\> | Line number |
| toggle | Toggle task status |
| done | Mark as done |
| todo | Mark as todo |
| daily | Use daily note |
| status="\<char\>" | Set status character |

```bash
obsidian task file="My Note" line=15 toggle
obsidian task ref="folder/note.md:42" done
obsidian task file="My Note" line=10 status="/"
```

**Tip:** Target a specific task by `file` + `line` or by `ref=path:line`. Use `toggle` to flip between done/todo, or use `done`/`todo`/`status=` for explicit control.
