# AGENTS.md

## Scope

- Global defaults for P.'s agent work. Local repo instructions may override these, except safety, security, and destructive-action constraints.
- Keep this file for durable rules only. Put reusable workflows in skills and deeper rationale in docs.
- Before non-trivial work, read the closest local instructions and relevant docs for the touched area.

References:

- Instruction architecture: `docs/instruction-architecture.md`
- Engineering principles: `docs/engineering-principles.md`
- Git and GitHub workflow: `docs/git-github.md`
- Tooling catalog: `docs/tooling.md`

## Communication

- Match my language: EN-US for English prompts, PT-BR for Portuguese prompts.
- Code comments and PR text: PT-BR. Code identifiers: EN-US.
- Telegraph style. Drop filler. Simple language. Enough to be clear.
- Correct my English only when it is actually wrong or meaningfully awkward.
- If my idea is bad, say why directly.
- Voice-to-text noise is common. Infer intent before asking.

## Decision Rules

- `analyze only`, `analysis only`, `let's discuss`, or similar means do not edit.
- Ambiguous target means stop with `CLARIFICATION NEEDED` and numbered questions.
- Clear action verb means execute. If method is uncertain, figure it out.
- For non-trivial work, briefly state scope, assumptions, risk, and verification before editing.
- Re-anchor on `continue`, `update`, or `keep going`: current repo state, thread context, last agreed slice.
- If corrected, stop, quote back the requested direction, name the gap, then proceed with the corrected target.

## Tools

- Prefer `rg` for code search when available.
- Verify optional tools with `command -v tool &>/dev/null`.
- Use the repo's existing package manager and task wrappers. Do not switch package managers to match individual preference.
- For Python helper work without repo-specific tooling, prefer `uv` when available.
- Use `gh` for GitHub. Never use curl against the GitHub API.
- Use `gh` from `PATH`; do not call `/opt/homebrew/bin/gh` directly.
- GitHub remotes should use the normal `github.com` host unless the repo itself documents a different convention.

## Skills And Docs

- Skills are the routing layer for reusable workflows.
- Skill descriptions should be short trigger phrases with clear scope.
- Skill bodies should be operational: commands, source-of-truth paths, constraints, validation, and known traps.
- Do not copy local paths, machine names, secrets, tokens, or habits into skills.
- If an installed Codex plugin already provides the same skill, keep a local copy only when this repo intentionally adapts the behavior.
- Prefer helper scripts only when the workflow is repeated and testable.
- After editing skills, validate frontmatter, required `name` and `description`, duplicate names, metadata, and generated runtime links when tooling exists.

## Execution

- Read enough code before editing. Read the full file before changing it.
- Plan the whole change, then make one complete pass.
- Touch only files required by the task.
- Do not refactor adjacent code unless needed for the requested fix.
- Fix root causes when reasonably possible. Band-aids need explicit justification.
- Reuse existing helpers, patterns, and module boundaries.
- Keep implementation simple. No speculative flexibility, one-off abstractions, dead code, or compatibility breadcrumbs.
- Assume every project is greenfield with no users. Strive for a single source of truth: no fallbacks, no legacy code support, just one clean stream of information flow.
- If a change touches contracts, schemas, APIs, events, or config shape, identify consumers before implementation.

## Verification

- Never call work done without proof.
- Run relevant tests, checks, or the closest available validation.
- For docs-only changes, run at least `git diff --check`.
- Report what was checked and what was not.
- If validation fails, the task is not complete.

## Security

- No hardcoded secrets.
- Do not read `.env*`, environment dumps, local secrets, or broad env output unless explicitly asked.
- If env context is needed, read `.env.example` only.
- If a secret is exposed, stop and tell me so we can rotate.
- For public GitHub bodies with Markdown, shell snippets, backticks, `$`, env names, or user text, write a temp file, inspect it, and pass `--body-file`.

## Git

- Check `git status --short` before edits in dirty or multi-agent worktrees.
- Never revert user changes unless explicitly asked.
- Never commit or push without explicit approval for that specific action. One approval does not grant ongoing permission for future commits or pushes.
- Do not stage unrelated files.
- Do not push, amend, force-push, rebase, merge, or switch branches unless asked or clearly required by the requested command.
- Never squash. Merge commits are preferred to squashing.
- Never use `--no-verify`.
- Prefer non-interactive git commands. Set `GIT_EDITOR=true` when a git flow may open an editor.
- Commit format: `<type>: <message>` with `feat|fix|docs|style|refactor|test|chore|perf`.
- Git commits must always include an extended description.
- If asked for a commit message, provide both the subject and the extended description.
- Commit descriptions should be bullet lists with one point per line:
    ```text
    - line number 1
    - line number 2
    - line number 3
    (...)
    - line number n
    ```
- Commit message: use direct PT-BR imperative.
- One logical change per commit.

## Destructive Actions

- Do not edit files via shell scripts such as `perl`, `sed`, or Python rewrites. Use patch edits.
- Deleting files is allowed only when directly required by the task. Say what is being deleted and why.
- `git reset --hard`, `git clean -fd`, `rm -rf`, and destructive database commands require explicit approval.
- No backup/variant files like `_v2`, `_backup`, or `_new`.
