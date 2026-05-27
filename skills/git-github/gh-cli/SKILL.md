---
name: gh-cli
description: "GitHub and git workflow with gh: issues, PRs, checks, comments, safe bodies, commits, and branch guardrails."
---

# GitHub CLI Workflow

Use `gh` for all GitHub operations. Do not use curl against the GitHub API.

## Start

In a repo, inspect state before writes:

```bash
git status --short --branch
git remote -v
gh auth status
```

Use `gh` from `PATH`; do not call `/opt/homebrew/bin/gh` directly. GitHub remotes should use the normal `github.com` host unless the repo itself documents a different convention.

## Public Body Safety

For PR comments, issue comments, release notes, review bodies, or any public GitHub text containing Markdown, shell snippets, backticks, `$`, env names, or user-provided text:

1. Write the body to a temp file.
2. Inspect the file.
3. Use `--body-file`.

Example:

```bash
tmp="$(mktemp)"
cat >"$tmp" <<'EOF'
Message body here.
EOF
sed -n '1,220p' "$tmp"
gh issue comment 123 --body-file "$tmp"
```

Do not inline complex bodies in shell arguments.

## Read Commands

Prefer structured reads:

```bash
gh issue view <n> --json number,title,state,author,body,comments,labels,updatedAt,url
gh pr view <n> --json number,title,state,author,body,comments,reviews,files,commits,statusCheckRollup,mergeStateStatus,headRefName,baseRefName,url
gh pr diff <n> --patch
gh run list --limit 20
gh run view <id> --log-failed
```

For search endpoints through `gh api search/*`, use `--method GET`.

## Write Guardrails

- Do not push, merge, close, reopen, edit labels, create releases, or change secrets unless asked.
- Never use `--no-verify`.
- Prefer non-interactive commands.
- Use `GIT_EDITOR=true` when a git flow may open an editor.
- Do not create temp local refs that look like real remote branches.
- If the tree is dirty, stage only explicit files.

## Commits

Commit format:

```text
<type>: <message>
```

Types: `feat|fix|docs|style|refactor|test|chore|perf`.

Rules:

- English by default.
- Letras projects use direct PT-BR imperative.
- One logical change per commit.
- Message must name the actual change, not `follow-up`, `cleanup`, or `address review`.
- Multi-line bodies should be one contiguous message block.
- Leave one blank line before trailers.

## PR And Issue Review

When reviewing a PR or issue, answer:

- ref and surface
- bug or behavior being changed
- root cause, with code path when known
- whether the proposed fix is the right ownership boundary
- whether a larger refactor is worth it
- proof checked
- remaining risk

Lead PR reviews with findings. If no blocking issues exist, say that directly and list proof plus residual risk.

## Reference

Read `docs/git-github.md` in the agents repo for the durable local convention. Use `gh <command> --help` for command syntax instead of copying a full manual into this skill.
