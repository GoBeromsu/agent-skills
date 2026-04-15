# Obsidian CLI — Search & Links

Commands for searching vault content and analyzing the link graph.

## search

Search vault for text.

| Parameter | Description |
|-----------|-------------|
| query=\<text\> | Search query (required) |
| path=\<folder\> | Limit to folder |
| limit=\<n\> | Max files |
| total | Return match count |
| case | Case sensitive |
| format=text\|json | Output format (default: text) |

```bash
obsidian search query="project plan" limit=5
obsidian search query="TODO" path="10. Zettel" case
```

**Known issue:** Currently returns empty results for all queries despite exit 0. See `references/known-limitations.md`. Use `search:open` or `qmd` as workarounds.

## search:context

Search with matching line context.

| Parameter | Description |
|-----------|-------------|
| query=\<text\> | Search query (required) |
| path=\<folder\> | Limit to folder |
| limit=\<n\> | Max files |
| case | Case sensitive |
| format=text\|json | Output format (default: text) |

```bash
obsidian search:context query="meeting" limit=10
```

**Known issue:** Same empty-result issue as `search`. Use `qmd` for CLI-based vault search.

## search:open

Open search view in Obsidian UI.

| Parameter | Description |
|-----------|-------------|
| query=\<text\> | Initial search query |

```bash
obsidian search:open query="project plan"
```

**Tip:** This is the recommended workaround for the search empty-result issue. Opens Obsidian's built-in search panel with the query pre-filled. The user sees results in the UI.

## backlinks

List backlinks to a file (files that link to this file).

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | Target file name |
| path=\<path\> | Target file path |
| counts | Include link counts |
| total | Return backlink count |
| format=json\|tsv\|csv | Output format (default: tsv) |

```bash
obsidian backlinks file="Concept Note"
obsidian backlinks file="Hub Note" counts format=json
obsidian backlinks file="My Note" total
```

**Tip:** Useful for verifying wikilinks after rename/move operations. Use `total` for a quick count.

## links

List outgoing links from a file.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| total | Return link count |

```bash
obsidian links file="Hub Note"
obsidian links file="My Note" total
```

**Tip:** Shows what a file links to. Pair with `backlinks` for a complete link analysis.

## orphans

List files with no incoming links (nothing links to them).

| Parameter | Description |
|-----------|-------------|
| total | Return orphan count |
| all | Include non-markdown files |

```bash
obsidian orphans total
obsidian orphans all
```

**Tip:** Useful for vault maintenance — orphan notes may need linking or cleanup.

## deadends

List files with no outgoing links (they don't link to anything).

| Parameter | Description |
|-----------|-------------|
| total | Return dead-end count |
| all | Include non-markdown files |

```bash
obsidian deadends total
```

**Tip:** Dead-end files are isolated — they exist but don't connect to the knowledge graph. Good candidates for adding links.

## unresolved

List unresolved links in vault (wikilinks pointing to non-existent files).

| Parameter | Description |
|-----------|-------------|
| total | Return unresolved link count |
| counts | Include link counts |
| verbose | Include source files |
| format=json\|tsv\|csv | Output format (default: tsv) |

```bash
obsidian unresolved
obsidian unresolved counts verbose
obsidian unresolved total
```

**Tip:** Critical for vault hygiene after batch renames. If old filenames appear here, the rename didn't update all links. See `references/batch-operations.md` for the round-trip rename fix.

## aliases

List aliases in the vault.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| total | Return alias count |
| verbose | Include file paths |
| active | Show aliases for active file |

```bash
obsidian aliases file="My Note"
obsidian aliases verbose
obsidian aliases total
```

**Tip:** Aliases are alternative names for notes defined in frontmatter. Useful for checking if a note can be found by a different name.
