---
name: fixissue
description: "Fix a GitHub issue end to end with root cause, focused scope, regression coverage when useful, and proof."
---

# Fix Issue

Fix the issue properly, with proof.

## Flow

1. Read the issue with `gh issue view <issue> --comments`.
2. Reproduce the bug or identify the failing code path.
3. Fix the root cause at the right ownership boundary.
4. Add a regression test when the area already has tests.
5. Run focused validation first, then broader checks if the change warrants it.
6. Summarize changed behavior, proof, and remaining risk.

Use local repo instructions for branch, commit, test, and language rules.

## Guardrails

- Do not widen scope beyond the issue unless the root cause requires it.
- Do not push, close, comment, edit labels, or assign people unless explicitly asked.
- If the issue is already fixed on current `main`, report proof and stop.
- If reproduction is impossible, name the blocker and the evidence needed.
