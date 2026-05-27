---
summary: "Local Git and GitHub conventions for gh, commits, safety, and public body handling."
read_when:
    - Doing GitHub issue, PR, review, CI, release, comment, or commit work.
    - Writing public GitHub bodies with Markdown, shell snippets, env names, or user text.
---

# Git And GitHub

## GitHub

- Use `gh` for GitHub operations.
- Do not use curl against the GitHub API.

Before public GitHub writes with Markdown, shell snippets, env names, backticks, `$`, or user-provided text:

1. write the body to a temp file
2. inspect the file
3. pass it with `--body-file`

## Commits

- Format: `<type>: <message>`
- Types: `feat|fix|docs|style|refactor|test|chore|perf`
- One logical change per commit.
- Do not use vague subjects like `follow-up`, `cleanup`, or `address review` without naming the actual change.
- For multi-line commit bodies, use one contiguous message block. Do not use one `-m` flag per bullet.

## Safety

- Do not push, amend, force-push, rebase, merge, or switch branches unless requested or clearly required.
- Never use `--no-verify`.
- Prefer non-interactive commands.
- Use `GIT_EDITOR=true` when a command might open an editor.
- Do not create temporary refs that look like real branches.
