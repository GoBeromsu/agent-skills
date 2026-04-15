# Obsidian CLI — Workspace & UI

Commands for managing workspaces, tabs, outlines, and UI navigation.

## workspace

Show workspace tree (current layout).

| Parameter | Description |
|-----------|-------------|
| ids | Include workspace item IDs |

```bash
obsidian workspace
obsidian workspace ids
```

**Tip:** Shows the current pane/tab layout as a tree structure. Use `ids` to get item identifiers for programmatic manipulation.

## workspaces

List saved workspaces.

| Parameter | Description |
|-----------|-------------|
| total | Return workspace count |

```bash
obsidian workspaces
obsidian workspaces total
```

## workspace:load

Load a saved workspace.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Workspace name (required) |

```bash
obsidian workspace:load name="Writing"
obsidian workspace:load name="Research"
```

**Tip:** Replaces the entire current layout with the saved workspace. Useful for switching between different task contexts (e.g., writing vs. research).

## workspace:save

Save current layout as workspace.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Workspace name |

```bash
obsidian workspace:save name="My Layout"
```

**Tip:** Saves the current pane arrangement, open files, and sidebar state. Overwrites if a workspace with the same name exists.

## workspace:delete

Delete a saved workspace.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Workspace name (required) |

```bash
obsidian workspace:delete name="Old Layout"
```

## tabs

List open tabs.

| Parameter | Description |
|-----------|-------------|
| ids | Include tab IDs |

```bash
obsidian tabs
obsidian tabs ids
```

## tab:open

Open a new tab.

| Parameter | Description |
|-----------|-------------|
| group=\<id\> | Tab group ID |
| file=\<path\> | File to open |
| view=\<type\> | View type to open |

```bash
obsidian tab:open file="My Note"
obsidian tab:open file="Project.md" group=1
```

## outline

Show headings for a file.

| Parameter | Description |
|-----------|-------------|
| file=\<name\> | File name |
| path=\<path\> | File path |
| format=tree\|md\|json | Output format (default: tree) |
| total | Return heading count |

```bash
obsidian outline file="Long Document"
obsidian outline file="My Note" format=md
obsidian outline file="My Note" total
```

**Tip:** `format=tree` shows an indented heading hierarchy. `format=md` outputs as a markdown list — useful for generating a table of contents.

## homepage

Open the homepage (requires Homepage plugin or configured homepage).

```bash
obsidian homepage
```

## homepage:read

Read homepage contents.

```bash
obsidian homepage:read
```

**Tip:** Returns the content of the configured homepage note.

## random

Open a random note.

| Parameter | Description |
|-----------|-------------|
| folder=\<path\> | Limit to folder |
| newtab | Open in new tab |

```bash
obsidian random
obsidian random folder="10. Zettel"
```

**Tip:** Opens a random note in the vault. Use `folder=` to limit randomness to a specific area. Useful for rediscovering forgotten notes.

## random:read

Read a random note (without opening it in UI).

| Parameter | Description |
|-----------|-------------|
| folder=\<path\> | Limit to folder |

```bash
obsidian random:read
obsidian random:read folder="10. Zettel"
```

**Tip:** Returns the content of a random note without navigating to it. Useful for programmatic "serendipity" workflows.

## web

Open URL in web viewer.

| Parameter | Description |
|-----------|-------------|
| url=\<url\> | URL to open (required) |
| newtab | Open in new tab |

```bash
obsidian web url="https://example.com"
obsidian web url="https://docs.obsidian.md" newtab
```

**Tip:** Opens a URL inside Obsidian's built-in web viewer pane, keeping the user in the app.
