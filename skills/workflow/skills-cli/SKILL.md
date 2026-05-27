---
name: skills-cli
description: "Use the local skills CLI to curate, import, categorize, archive, sync, validate, update, inspect, link, and diagnose agent skills and metadata."
---

# Skills CLI

Use `skills` as the source-of-truth manager for local agent skills. It owns the categorized source tree, archive tree, runtime symlink tree, import/update flow, and per-skill `skill.toml` metadata.

## Start Here

Always inspect the active config before changing anything:

```bash
skills
skills onboard
skills plan --plain
skills doctor --plain
skills link --plain
skills inspect https://github.com/org/repo/tree/main/skills/example --plain
skills categories --plain
```

Do not assume paths. The config decides:

- `source_dir`: editable categorized skill tree
- `archive_dir`: archived skills nested under the same category layout
- `runtime_dir`: generated flat symlink view
- `links`: direct install targets such as `agents`, `codex`, and `claude`

Edit source skills, not runtime symlinks or direct target copies, unless the user explicitly asks for a direct target import.

## Safety Rules

- Mutating commands are dry-run by default; use `--apply` only after reviewing the preview.
- Use `--plain` for stable readable output and `--json` when scriptable output is needed.
- Do not guess source URLs or licenses. If provenance is unclear, mark it unknown and ask.
- Keep archived skills under `archive/<category>/<skill>/`, not a separate top-level archive tree.
- If an installed Codex plugin already provides the skill, delete the local duplicate instead of archiving it.
- `import` is remote-only. Do not use it for local folders; categorize local skills with `move` or `suggest`.

## Common Workflows

Inspect catalog state:

```bash
skills list --plain
skills list --archived --plain
skills plan --plain
skills validate --plain
skills doctor --plain
skills improve handoff
skills metadata plan --plain
```

`doctor` is the quick health check before and after catalog work. It validates the same shape the `skill-cleaner` workflow cares about: path existence, configured global links, prompt-visible catalog budget, long descriptions, runtime sync drift, duplicate names, metadata, and native `SKILL.md` quality checks.

Import from GitHub:

```bash
skills inspect https://github.com/org/repo/tree/main/skills/example --plain
skills import https://github.com/org/repo/tree/main/skills/example --apply
skills import https://github.com/org/repo/tree/main/skills --skill example --apply
skills import https://github.com/org/repo/tree/main/skills --all --apply
```

Use `inspect` before importing broad URLs. A single skill URL lists only that skill; a folder URL lists discovered skills without installing anything.

In a terminal, `skills import <url>` is guided: select discovered skills, select destinations, choose categories, preview, then confirm apply. In non-interactive runs, folders with multiple skills require `--skill <name>` or `--all`.

Use `--category <slug>` when the category is already known. Without `--category`, non-interactive source imports use `codex exec --model gpt-5.4-mini` to propose a category. Use `--provider claude` to run the same prompt through `claude -p`. Use `--no-ai` only when the user wants to place a remote import in `uncategorized`.

Install directly into configured target folders:

```bash
skills import https://github.com/org/repo/tree/main/skills/example --target agents --apply
skills import https://github.com/org/repo/tree/main/skills/example --target codex --target claude --apply
skills import https://github.com/org/repo/tree/main/skills/example --target '*' --apply
```

`agents` means the general shared `~/.agents/skills` target; Codex, Cursor, Claude, and other tools can point at it. `codex` and `claude` are tool-specific direct targets.

Link configured global targets to the generated runtime view:

```bash
skills link --plain
skills link agents --apply
```

`link` is dry-run by default and refuses to replace an existing non-symlink path.

Move, archive, restore, or delete:

```bash
skills move oracle research --apply
skills archive xgh --apply
skills restore xgh --apply
```

Use archive for local skills that may be useful later. For plugin duplicates, remove the local directory and keep the plugin as the source of truth.

Sync runtime symlinks after source-tree changes:

```bash
skills sync --apply
```

Update imported skills:

```bash
skills update --apply
skills update azure-compliance --apply
```

Clean remote skills with `dirty = false` update by replacing from upstream. Dirty remote skills with `dirty = true` update through the selected AI provider using `gpt-5.5` so local edits are preserved deliberately. Codex is the default; use `--provider claude` for `claude -p`.

Export an improvement prompt when AI automation is not the right path:

```bash
skills improve handoff --export-prompt /tmp/skills-improve-handoff.md
skills improve handoff --provider claude
```

`--export-prompt` writes the exact prompt and exits without calling AI, so the person can refine or run it interactively if `claude -p` is not useful.

## Metadata

Each skill should have `skill.toml`:

```toml
version = 1
name = "example"
remote = true
dirty = false
license = "MIT"
status = "clean"

[[sources]]
url = "https://github.com/org/repo/tree/main/skills/example"
ref = "main"
path = "skills/example"
```

Use local metadata for user-authored skills:

```toml
version = 1
name = "example"
remote = false
dirty = false
license = "Unknown"
status = "local"
notes = "No remote source recorded."
```

Valid `status` values are `local`, `clean`, `adapted`, `unknown`, and `external`. Put explanatory prose in `notes`, not `status`.

Run these to find or generate missing metadata:

```bash
skills metadata plan --plain
skills metadata write
skills metadata write example --apply
```

`metadata write` creates generic local metadata. Replace it with evidence-backed remote metadata when a real source exists.

After metadata or organization changes, verify:

```bash
skills plan --plain
skills doctor --plain
skills sync --apply
```
