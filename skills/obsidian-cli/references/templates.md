# Obsidian CLI — Templates

Commands for managing and using core templates and Templater plugin templates.

## templates

List available templates. No parameters.

```bash
obsidian templates
obsidian templates total
```

| Parameter | Description |
|-----------|-------------|
| total | Return template count |

**Tip:** Lists templates from the configured templates folder.

## template:insert

Insert template into active file.

| Parameter | Description |
|-----------|-------------|
| name=\<template\> | Template name (required) |

```bash
obsidian template:insert name="Daily Template"
```

**Tip:** Inserts the template content into the currently active file. The file must be open in Obsidian. Uses Obsidian's core Templates plugin.

## template:read

Read template content.

| Parameter | Description |
|-----------|-------------|
| name=\<template\> | Template name (required) |
| resolve | Resolve template variables |
| title=\<title\> | Title for variable resolution |

```bash
obsidian template:read name="Meeting Notes"
obsidian template:read name="Zettel" resolve title="My New Note"
```

**Tip:** Use `resolve` to see what the template would look like with variables filled in (e.g., `{{date}}`, `{{title}}`). Pass `title=` to set the title variable during resolution.

## templater:create-from-template

Create a new note from a Templater template. Requires the Templater community plugin.

| Parameter | Description |
|-----------|-------------|
| template=\<path\> | Template file path, relative to vault root or templates folder (required) |
| file=\<path\> | Output file path, relative to vault root (required) |
| open | Open the created file in the UI |

```bash
obsidian templater:create-from-template template="Templates/Zettel.md" file="10. Zettel/New Concept.md"
obsidian templater:create-from-template template="Templates/Project.md" file="30. Projects/New Project.md" open
```

**Tip:** This runs Templater's full template engine, which supports JavaScript execution, dynamic prompts, and advanced variable resolution beyond what core Templates offers. The `template=` path can be relative to the vault root or the templates folder. Use `open` to immediately view the created note.
