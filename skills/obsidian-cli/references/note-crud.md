# Obsidian CLI — Note CRUD

Commands for reading, creating, editing, and managing individual notes.

## read

Read file contents.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name (wikilink-style) |
| path=\<path\> | Exact file path from vault root |

```bash
obsidian read file="Meeting Notes"
obsidian read path="10. Zettel/My Note.md"
```

**Tip:** Returns resolved content including transclusions. Prefer this over the Read tool for vault notes.

## create

Create a new file.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | File name |
| path=\<path\> | File path (folder/name.md) |
| content=\<text\> | Initial content |
| template=\<name\> | Template to use |
| overwrite | Overwrite if file exists |
| open | Open file after creating |
| newtab | Open in new tab |

```bash
obsidian create name="New Note" content="# Hello World"
obsidian create path="10. Zettel/Concept.md" template="Zettel Template"
obsidian create name="Draft" content="Some text" overwrite
```

**Tip:** Use `template=` to apply a vault template on creation. Use `path=` to place the file in a specific folder. The `overwrite` flag replaces an existing file — use with caution.

## append

Append content to a file.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| content=\<text\> | Content to append (required) |
| inline | Append without newline |

```bash
obsidian append file="Daily Log" content="- [ ] New task"
obsidian append file="Running List" content=" (continued)" inline
```

**Tip:** By default adds a newline before the content. Use `inline` to append directly to the last line.

## prepend

Prepend content to a file.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| content=\<text\> | Content to prepend (required) |
| inline | Prepend without newline |

```bash
obsidian prepend file="My Note" content="**Updated 2026-04-15**"
```

**Tip:** Inserts content at the top of the file. Useful for adding status banners or update notices. Note: prepends before frontmatter — if the file has YAML frontmatter, consider using `append` or `property:set` instead.

## delete

Delete a file.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| permanent | Skip trash, delete permanently |

```bash
obsidian delete file="Old Draft"
obsidian delete path="archive/stale.md" permanent
```

**Tip:** By default sends to system trash (recoverable). Use `permanent` only when certain. There is no `trash` command — `delete` is the correct command.

## rename

Rename a file (stays in same folder).

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | Current file name |
| path=\<path\> | Current file path |
| name=\<name\> | New file name (required) |

```bash
obsidian rename file="Old Name" name="New Name"
obsidian rename path="folder/old.md" name="new"
```

**Tip:** Automatically updates all wikilinks across the vault. Always prefer this over Write+rm for renaming vault files. For batch renames, add `sleep 0.5` between operations and see `references/batch-operations.md`.

## move

Move or rename a file (can change folder).

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| to=\<path\> | Destination folder or full path (required) |

```bash
obsidian move file="My Note" to="20. Connect/"
obsidian move file="My Note" to="20. Connect/Renamed Note.md"
```

**Tip:** If `to=` is a folder path (ends with `/`), the file keeps its name. If `to=` includes a filename, the file is also renamed. Updates wikilinks vault-wide.

## open

Open a file in Obsidian.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| newtab | Open in new tab |

```bash
obsidian open file="My Note"
obsidian open file="Reference" newtab
```

## file

Show file info (metadata, not content).

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |

```bash
obsidian file file="My Note"
```

**Tip:** Returns file metadata (path, size, modification time, etc.), not the content. Use `read` for content.

## files

List files in the vault.

| Parameter | Description |
|-----------|-------------|
| folder=\<path\> | Filter by folder |
| ext=\<extension\> | Filter by extension |
| total | Return file count |

```bash
obsidian files folder="10. Zettel" ext=md
obsidian files total
```

**Tip:** Use `folder=` to scope to a specific directory. Combine with `total` for quick counts.
