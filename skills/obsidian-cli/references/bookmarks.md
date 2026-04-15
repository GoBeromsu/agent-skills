# Obsidian CLI — Bookmarks

Commands for managing Obsidian bookmarks (pinned items for quick access).

## bookmark

Add a bookmark.

| Parameter | Description |
|-----------|-------------|
| file=\<path\> | File to bookmark |
| subpath=\<subpath\> | Subpath (heading or block) within file |
| folder=\<path\> | Folder to bookmark |
| search=\<query\> | Search query to bookmark |
| url=\<url\> | URL to bookmark |
| title=\<title\> | Bookmark title |

```bash
obsidian bookmark file="Important Note" title="Pinned"
obsidian bookmark file="Long Doc.md" subpath="#Section 3" title="Key Section"
obsidian bookmark search="TODO" title="All TODOs"
obsidian bookmark url="https://example.com" title="Reference"
```

**Tip:** Bookmarks can point to files, headings within files, folders, saved searches, or URLs. Use `subpath=` to bookmark a specific heading (`#heading`) or block (`^block-id`) within a file. The `title=` is optional but makes bookmarks easier to identify.

## bookmarks

List bookmarks.

| Parameter | Description |
|-----------|-------------|
| total | Return bookmark count |
| verbose | Include bookmark types |
| format=json\|tsv\|csv | Output format (default: tsv) |

```bash
obsidian bookmarks
obsidian bookmarks verbose format=json
obsidian bookmarks total
```

**Tip:** Use `verbose` to see what type each bookmark is (file, folder, search, URL). Useful for auditing saved bookmarks.
