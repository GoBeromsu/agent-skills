# Obsidian CLI — Plugins, Themes & Snippets

Commands for managing plugins, themes, and CSS snippets.

## Plugins

### plugin

Get plugin info.

| Parameter | Description |
|-----------|-------------|
| id=\<plugin-id\> | Plugin ID (required) |

```bash
obsidian plugin id="dataview"
obsidian plugin id="templater-obsidian"
```

### plugins

List installed plugins.

| Parameter | Description |
|-----------|-------------|
| filter=core\|community | Filter by plugin type |
| versions | Include version numbers |
| format=json\|tsv\|csv | Output format (default: tsv) |

```bash
obsidian plugins
obsidian plugins filter=community versions
obsidian plugins format=json
```

### plugins:enabled

List enabled plugins.

| Parameter | Description |
|-----------|-------------|
| filter=core\|community | Filter by plugin type |
| versions | Include version numbers |
| format=json\|tsv\|csv | Output format (default: tsv) |

```bash
obsidian plugins:enabled filter=community
```

### plugins:restrict

Toggle or check restricted mode.

| Parameter | Description |
|-----------|-------------|
| on | Enable restricted mode |
| off | Disable restricted mode |

```bash
obsidian plugins:restrict on
obsidian plugins:restrict off
```

**Tip:** Restricted mode disables all community plugins. Useful for troubleshooting plugin conflicts.

### plugin:enable

Enable a plugin.

| Parameter | Description |
|-----------|-------------|
| id=\<id\> | Plugin ID (required) |
| filter=core\|community | Plugin type |

```bash
obsidian plugin:enable id="dataview"
```

### plugin:disable

Disable a plugin.

| Parameter | Description |
|-----------|-------------|
| id=\<id\> | Plugin ID (required) |
| filter=core\|community | Plugin type |

```bash
obsidian plugin:disable id="dataview"
```

### plugin:install

Install a community plugin.

| Parameter | Description |
|-----------|-------------|
| id=\<id\> | Plugin ID (required) |
| enable | Enable after install |

```bash
obsidian plugin:install id="calendar" enable
```

**Tip:** Use `enable` to activate the plugin immediately after installation.

### plugin:uninstall

Uninstall a community plugin.

| Parameter | Description |
|-----------|-------------|
| id=\<id\> | Plugin ID (required) |

```bash
obsidian plugin:uninstall id="unused-plugin"
```

### plugin:reload

Reload a plugin (for developers).

| Parameter | Description |
|-----------|-------------|
| id=\<id\> | Plugin ID (required) |

```bash
obsidian plugin:reload id="my-plugin"
```

**Tip:** Reloads the plugin code without restarting Obsidian. Essential for plugin development — run this after every code change.

---

## Themes

### theme

Show active theme or get info.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Theme name for details |

```bash
obsidian theme
obsidian theme name="Minimal"
```

### themes

List installed themes.

| Parameter | Description |
|-----------|-------------|
| versions | Include version numbers |

```bash
obsidian themes
obsidian themes versions
```

### theme:install

Install a community theme.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Theme name (required) |
| enable | Activate after install |

```bash
obsidian theme:install name="Minimal" enable
```

### theme:set

Set active theme.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Theme name (empty for default) (required) |

```bash
obsidian theme:set name="Minimal"
obsidian theme:set name=""
```

**Tip:** Pass an empty name to revert to the default theme.

### theme:uninstall

Uninstall a theme.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Theme name (required) |

```bash
obsidian theme:uninstall name="Old Theme"
```

---

## CSS Snippets

### snippet:enable

Enable a CSS snippet.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Snippet name (required) |

```bash
obsidian snippet:enable name="custom-headers"
```

### snippet:disable

Disable a CSS snippet.

| Parameter | Description |
|-----------|-------------|
| name=\<name\> | Snippet name (required) |

```bash
obsidian snippet:disable name="custom-headers"
```

### snippets

List installed CSS snippets. No parameters.

```bash
obsidian snippets
```

### snippets:enabled

List enabled CSS snippets. No parameters.

```bash
obsidian snippets:enabled
```

**Tip:** CSS snippets are `.css` files in the vault's `.obsidian/snippets/` folder. They allow custom styling without a full theme.
