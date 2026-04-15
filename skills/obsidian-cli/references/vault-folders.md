# Obsidian CLI — Vault & Folders

Commands for vault information, folder management, and general utilities.

## vault

Show vault info.

| Parameter | Description |
|-----------|-------------|
| info=name\|path\|files\|folders\|size | Return specific info only |

```bash
obsidian vault
obsidian vault info=path
obsidian vault info=files
```

**Tip:** Without `info=`, returns all vault metadata. Use `info=path` to get the vault root path, `info=files` for file count.

## vaults

List known vaults.

| Parameter | Description |
|-----------|-------------|
| total | Return vault count |
| verbose | Include vault paths |

```bash
obsidian vaults verbose
obsidian vaults total
```

**Tip:** Shows all vaults Obsidian knows about. Use `verbose` to see filesystem paths.

## folder

Show folder info.

| Parameter | Description |
|-----------|-------------|
| path=\<path\> | Folder path (required) |
| info=files\|folders\|size | Return specific info only |

```bash
obsidian folder path="10. Zettel"
obsidian folder path="20. Connect" info=files
```

## folders

List folders in the vault.

| Parameter | Description |
|-----------|-------------|
| folder=\<path\> | Filter by parent folder |
| total | Return folder count |

```bash
obsidian folders
obsidian folders folder="10. Zettel"
obsidian folders total
```

## reload

Reload the vault. No parameters.

```bash
obsidian reload
```

**Tip:** Forces Obsidian to re-index the vault. Useful after bulk file operations outside Obsidian, or when the file explorer seems stale.

## restart

Restart the app. No parameters.

```bash
obsidian restart
```

**Tip:** Full app restart. More aggressive than `reload` — use when plugins misbehave or the UI is stuck.

## version

Show Obsidian version. No parameters.

```bash
obsidian version
```

## wordcount

Count words and characters.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| words | Return word count only |
| characters | Return character count only |

```bash
obsidian wordcount file="Essay Draft"
obsidian wordcount file="Essay Draft" words
```

**Tip:** Without flags, returns both word and character counts. Use `words` or `characters` for a single number.

## recents

List recently opened files.

| Parameter | Description |
|-----------|-------------|
| total | Return recent file count |

```bash
obsidian recents
obsidian recents total
```

**Tip:** Shows files in order of most recently opened. Useful for finding what the user was working on.
