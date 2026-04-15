# Obsidian CLI — Developer

Commands for plugin/theme development, JavaScript execution, DOM inspection, and debugging.

## eval

Execute JavaScript and return result.

| Parameter | Description |
|-----------|-------------|
| code=\<javascript\> | JavaScript code to execute (required) |

```bash
obsidian eval code="app.vault.getFiles().length"
obsidian eval code="app.workspace.getActiveFile()?.basename"
obsidian eval code="app.plugins.enabledPlugins.size"
obsidian eval code="'ping'"
```

**Tip:** Runs JavaScript in the Obsidian app context with full access to the Obsidian API (`app`, `app.vault`, `app.workspace`, `app.plugins`, etc.). Extremely powerful for:
- Querying vault state beyond what other CLI commands expose
- Automating complex operations that combine multiple API calls
- Health-checking Obsidian during batch operations (`code="'ping'"` — empty response means frozen)
- Accessing plugin APIs (e.g., `app.plugins.plugins["dataview"]?.api`)

The return value is serialized and printed to stdout. Complex objects may need `.toString()` or `JSON.stringify()`.

**Getting return values:** `eval` prints the result of the evaluated expression. Single expressions work directly (`code="app.vault.getFiles().length"`), but multi-statement code needs an IIFE — top-level `return` is illegal, and a bare trailing expression produces no output.

```bash
# Single expression — works directly
obsidian eval code="app.vault.getFiles().length"

# Multi-statement — MUST use IIFE
obsidian eval code="(()=>{const files=app.vault.getMarkdownFiles();const count=files.filter(f=>f.path.startsWith('15.')).length;return count;})()"

# Top-level return — ERROR: Illegal return statement
obsidian eval code="const x=1; return x;"

# Bare trailing expression — SILENT (no output)
obsidian eval code="const x=1; x;"
```

## dev:errors

Show captured errors.

| Parameter | Description |
|-----------|-------------|
| clear | Clear the error buffer |

```bash
obsidian dev:errors
obsidian dev:errors clear
```

**Tip:** Shows JavaScript errors captured since the last check. Essential after `plugin:reload` — check this to see if reloaded code has errors.

## dev:console

Show captured console messages.

| Parameter | Description |
|-----------|-------------|
| clear | Clear the console buffer |
| limit=\<n\> | Max messages to show (default 50) |
| level=log\|warn\|error\|info\|debug | Filter by log level |

```bash
obsidian dev:console
obsidian dev:console level=error
obsidian dev:console level=warn limit=10
obsidian dev:console clear
```

**Tip:** Captures `console.log()`, `console.warn()`, etc. from the app. Use `level=error` to focus on problems. Use `clear` to reset the buffer before testing so you only see fresh messages.

## dev:dom

Query DOM elements.

| Parameter | Description |
|-----------|-------------|
| selector=\<css\> | CSS selector (required) |
| total | Return element count |
| text | Return text content |
| inner | Return innerHTML instead of outerHTML |
| all | Return all matches instead of first |
| attr=\<name\> | Get attribute value |
| css=\<prop\> | Get CSS property value |

```bash
obsidian dev:dom selector=".workspace-leaf" total
obsidian dev:dom selector=".workspace-leaf-content" text
obsidian dev:dom selector=".nav-file-title" all text
obsidian dev:dom selector=".cm-editor" attr=class
obsidian dev:dom selector=".workspace" css=background-color
```

**Tip:** Query Obsidian's UI DOM for inspection and testing. By default returns the first match's outerHTML. Use `text` for readable content, `all` for multiple elements, `attr=` for attribute values, `css=` for computed CSS properties.

## dev:css

Inspect CSS with source locations.

| Parameter | Description |
|-----------|-------------|
| selector=\<css\> | CSS selector (required) |
| prop=\<name\> | Filter by property name |

```bash
obsidian dev:css selector=".workspace-leaf"
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

**Tip:** Shows CSS rules applied to matching elements, including source file locations. More detailed than `dev:dom css=` — shows all rules, not just the computed value.

## dev:screenshot

Take a screenshot.

| Parameter | Description |
|-----------|-------------|
| path=\<filename\> | Output file path |

```bash
obsidian dev:screenshot path=screenshot.png
obsidian dev:screenshot path=/tmp/obsidian-ui.png
```

**Tip:** Captures the current Obsidian window. Useful for visual regression testing during plugin/theme development. If `path=` is relative, it's relative to the current working directory.

## dev:debug

Attach/detach Chrome DevTools Protocol debugger.

| Parameter | Description |
|-----------|-------------|
| on | Attach debugger |
| off | Detach debugger |

```bash
obsidian dev:debug on
obsidian dev:debug off
```

**Tip:** Attaches the CDP debugger for advanced debugging. Use with `dev:cdp` for protocol-level inspection.

## dev:cdp

Run a Chrome DevTools Protocol command.

| Parameter | Description |
|-----------|-------------|
| method=\<CDP.method\> | CDP method to call (required) |
| params=\<json\> | Method parameters as JSON |

```bash
obsidian dev:cdp method="Runtime.evaluate" params='{"expression":"1+1"}'
obsidian dev:cdp method="Page.captureScreenshot"
```

**Tip:** Direct access to Chrome DevTools Protocol. Requires the debugger to be attached (`dev:debug on`). See the [CDP documentation](https://chromedevtools.github.io/devtools-protocol/) for available methods. This is the most low-level debugging tool — use `eval` and `dev:dom` first for most tasks.

## dev:mobile

Toggle mobile emulation.

| Parameter | Description |
|-----------|-------------|
| on | Enable mobile emulation |
| off | Disable mobile emulation |

```bash
obsidian dev:mobile on
obsidian dev:mobile off
```

**Tip:** Emulates mobile viewport for testing responsive layouts in plugins/themes. Toggle off to return to desktop view.

## devtools

Toggle Electron dev tools. No parameters.

```bash
obsidian devtools
```

**Tip:** Opens/closes the built-in Electron developer tools panel (equivalent to Cmd+Option+I). Provides a full Chrome DevTools interface within Obsidian.

---

## Plugin Development Workflow

Recommended cycle after making code changes:

1. **Reload** the plugin: `obsidian plugin:reload id=my-plugin`
2. **Check for errors**: `obsidian dev:errors`
3. **Verify visually**: `obsidian dev:screenshot path=screenshot.png` or `obsidian dev:dom selector=".my-element" text`
4. **Check console**: `obsidian dev:console level=error`
5. **Run custom checks**: `obsidian eval code="app.plugins.plugins['my-plugin'].someMethod()"`
