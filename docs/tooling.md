---
summary: "Small catalog of local tools agents should know about without hardcoding broad tool preferences."
read_when:
    - Choosing a local helper for GitHub, skills, Codex plugins, Oracle review, docs, or Apple builds.
    - Updating AGENTS.md tool rules or deciding whether a workflow deserves a skill.
---

# Tooling

Use repo-local tooling first. This file is a catalog, not a global preference list.

## Core

- `rg`: default code search when available.
- `gh`: GitHub CLI for issues, PRs, checks, releases, comments, and repo metadata.
- `skills`: manages the categorized `.agents/skills` source tree and generated runtime symlinks.
- `uv`: preferred Python helper runner when the repo does not already define another Python workflow.

## Agents Repo

- `./install.sh`: applies the whole local setup.
- `skills validate --plain`: validates active skill frontmatter, metadata, duplicate names, and quality heuristics.
- `scripts/validate-docs.py`: validates docs frontmatter.
- `scripts/docs-list.py`: lists docs with `summary` and `read_when` hints.
- `scripts/sync-codex-plugins.py`: upgrades/checks declared Codex plugins.
- `scripts/sync-codex-plugins.py`: validates plugins declared in `codex/config.toml`.

## Review And Build Helpers

- `oracle`: second-model review through the local Oracle skill.
- `codex review`: built-in Codex review when a final review pass is useful.
- `xcodebuildmcp`: preferred Apple build/run/debug path when working on iOS/macOS projects.

Avoid adding tools here just because they are installed. Add only tools that agents should deliberately choose.
