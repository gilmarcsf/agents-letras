---
name: pickup
description: "Rehydrate current task context before continuing work from repo state, diffs, handoff notes, local docs, PR or issue state, and thread constraints."
---

# Pickup

Rebuild enough context to act without relying on stale chat memory.

## Gather

Start from the smallest reliable sources:

- current `cwd`, branch, and `git status --short --branch`
- root-level `handoff.md`, if present
- unstaged and staged diffs
- recent commits only when there is no useful handoff or worktree diff
- local instructions and docs near the touched area
- current thread's last agreed slice, constraints, and blockers
- open PR, issue, or failing checks when relevant
- running processes only when the repo already depends on them or the user mentions them

Do not trawl broad history if repo state, `handoff.md`, and local diffs already narrow the task.

Treat `handoff.md` as a temporary bridge, not a project TODO. If it is consumed, remove it after the brief is captured unless the user explicitly asks to keep it.

## Infer

Turn the evidence into one compact working brief:

- current slice
- what should stay out of scope
- what is already done
- next safe step
- files carrying the current state

If there are multiple plausible slices, present the 2-3 most likely options and stop.

## Act

If the user asked to resume or continue:

- state the inferred scope in one sentence
- list the next 2-3 concrete actions when useful
- continue from that slice

If the user asked what they were working on:

- return the brief without editing
- mention whether a `handoff.md` exists
- summarize the local state that shaped the brief

## Output

Keep it short:

- `Current slice`
- `Constraints`
- `Evidence`
- `Next safe step`
- `Open question`, only if one blocks confident action
