# Obsidian CLI — Batch Operations

## Round-trip Rename

When `obsidian rename` fails to update wikilinks during batch execution (async failure or freeze), use a round-trip rename to force wikilink resolution:

```bash
# Step 1: restore original name
obsidian vault=Ataraxia rename path="folder/New Name.md" name="Old Name"
sleep 0.5

# Step 2: rename again (triggers wikilink update)
obsidian vault=Ataraxia rename path="folder/Old Name.md" name="New Name"
sleep 0.5
```

Step 2 triggers Obsidian's vault-wide `[[Old Name]]` → `[[New Name]]` wikilink replacement.

## Health Check Pattern (every 40 operations)

```bash
obsidian vault=Ataraxia eval code="'ping'"
# empty response = frozen — restart:
pkill -f Obsidian && sleep 3 && open -a Obsidian && sleep 6
```

## Verification

```bash
obsidian vault=Ataraxia unresolved  # old filename absent = success
```

## Caveats

- Do not add parentheses-containing old filenames to aliases. Round-trip rename is the correct approach for wikilink updates.
- Expect freeze around ~400 consecutive operations. The 40-operation health check interval prevents data loss.
- Always add `sleep 0.5` between rename operations to allow Obsidian's indexer to process changes.
