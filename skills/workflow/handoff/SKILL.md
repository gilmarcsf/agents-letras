---
name: handoff
description: "Capture a compact handoff for another agent or future continuation, including current slice, dirty state, proof, blockers, and next step."
---

# Handoff

Create a short handoff that lets the next agent continue safely without reading the whole chat.

## Sources

Prefer local state over memory:

- repo/path: `pwd`
- branch and dirty state: `git status --short --branch`
- recent commits, only when useful: `git log --oneline -5`
- PR state, when relevant: `gh pr status` or `gh pr view`
- validation proof: exact commands already run and their pass/fail result

## Capture

Include:

- current repo/path/branch
- user's latest goal and constraints
- what is done
- what is dirty or uncommitted
- relevant PR, issue, or CI state
- commands/tests already run and results
- next safe step
- blockers or assumptions

## Constraints

Keep it short. Do not turn it into a project TODO list.

Do not invent validation. Mark unrun checks as not run.
Do not hide dirty files; list them or say the tree is clean.
If the user corrected direction mid-task, hand off the corrected target.

## Validation

Before finishing, check that the handoff has:

- latest user request, not an older goal
- dirty state or `clean`
- proof commands with status
- one next safe step
- blockers or `none known`

## Temporary File

If writing a file is requested, create or refresh temporary repo-root `handoff.md`. It is a bridge for re-entry, not durable project docs. Do not delete an existing handoff unless the user asks or the re-entry workflow consumes it.
