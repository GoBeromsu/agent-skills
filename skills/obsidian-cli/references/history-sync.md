# Obsidian CLI — History & Sync

Commands for local file history, Obsidian Sync version management, and diffing.

## history

List file history versions (local).

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |

```bash
obsidian history file="My Note"
```

**Tip:** Shows locally stored version snapshots. Obsidian periodically saves file versions.

## history:list

List files with history. No file-specific parameters.

```bash
obsidian history:list
```

**Tip:** Shows which files have local history snapshots available.

## history:open

Open file recovery UI.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |

```bash
obsidian history:open file="My Note"
```

**Tip:** Opens Obsidian's file recovery interface for visual version comparison.

## history:read

Read a specific file history version.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| version=\<n\> | Version number (default: 1) |

```bash
obsidian history:read file="My Note" version=1
obsidian history:read file="My Note" version=3
```

**Tip:** Version 1 is the most recent snapshot. Higher numbers go further back.

## history:restore

Restore a file history version.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| version=\<n\> | Version number (required) |

```bash
obsidian history:restore file="My Note" version=2
```

**Tip:** Overwrites the current file with the specified version. Consider reading the version first with `history:read` to verify.

## diff

List or diff local/sync versions.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| from=\<n\> | Version number to diff from |
| to=\<n\> | Version number to diff to |
| filter=local\|sync | Filter by version source |

```bash
obsidian diff file="My Note"
obsidian diff file="My Note" from=1 to=3
obsidian diff file="My Note" filter=sync
```

**Tip:** Without `from`/`to`, lists available versions. With both, shows a diff between the two versions. Use `filter=` to see only local or sync versions.

---

## Sync Commands

Requires Obsidian Sync to be configured.

## sync

Pause or resume sync.

| Parameter | Description |
|-----------|-------------|
| on | Resume sync |
| off | Pause sync |

```bash
obsidian sync on
obsidian sync off
```

## sync:status

Show sync status. No parameters.

```bash
obsidian sync:status
```

## sync:history

List sync version history for a file.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| total | Return version count |

```bash
obsidian sync:history file="My Note"
obsidian sync:history file="My Note" total
```

## sync:read

Read a sync version.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| version=\<n\> | Version number (required) |

```bash
obsidian sync:read file="My Note" version=1
```

## sync:restore

Restore a sync version.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| version=\<n\> | Version number (required) |

```bash
obsidian sync:restore file="My Note" version=2
```

**Tip:** Restores the file to the specified sync version. Verify with `sync:read` first.

## sync:deleted

List deleted files in sync.

| Parameter | Description |
|-----------|-------------|
| total | Return deleted file count |

```bash
obsidian sync:deleted
obsidian sync:deleted total
```

**Tip:** Shows files that were deleted but are still in sync history. Can be used to identify accidentally deleted files.

## sync:open

Open sync history UI.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |

```bash
obsidian sync:open file="My Note"
```
