---
name: verification-closeout
description: "Verify and close out a change: choose tests, run proof, inspect diff, and report what passed or remains unverified."
---

# Verification Closeout

Use when finishing a code, docs, config, or workflow change and the user expects proof.

## Pick Proof

Choose the smallest proof that actually covers the change:

- docs only: `git diff --check` and link/path sanity
- formatting-sensitive code: formatter or format check
- pure logic: focused unit tests
- shared behavior or contracts: broader test target or compile/typecheck
- UI: run the app when feasible and inspect the changed screen
- GitHub workflow: inspect workflow file plus `gh run` or `gh pr checks` when relevant

If no targeted tests exist, state that and run the closest available validation.

## Required Checks

Before final response:

1. Inspect `git diff --check` for touched files.
2. Run the selected proof.
3. Review the final diff for unrelated changes.
4. Confirm generated/runtime views are synced when the repo has such tooling.

## Report

Keep the closeout short:

- what changed
- proof run and result
- anything not run and why
- remaining risk, only if real

Do not call the task complete if proof failed.
