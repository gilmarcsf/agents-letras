---
name: landpr
description: "Land a GitHub PR only when explicitly requested, after checking review state, CI, validation, merge method, and final state."
---

# Land PR

Merge a PR only after it is correct, current, and verified.

## Guardrails

- Use `gh`, not browser URLs.
- Inspect local state with `git status --short --branch` first.
- Do not squash by default. Prefer merge commit unless repo instructions say otherwise.
- Do not force-push unless explicitly approved for that PR flow.
- Stop if the PR is draft, conflicted, untrusted in a risky area, or requires a product/policy choice.

## Flow

1. Read PR metadata, diff, comments, reviews, files, commits, and checks.
2. Resolve blocking review comments or CI failures in scope.
3. Run the relevant validation.
4. Merge only when checks and review state are acceptable.
5. Verify GitHub PR state is `MERGED`.
6. Return to the expected branch and show final status.

Use temp branches only when they reduce risk. If you create one, name it clearly under `temp/`, delete it after success, and do not push it unless needed.

## Final

Return a short recap with:

- PR number/URL
- merge method and final state
- validation run
- branch/status after landing
