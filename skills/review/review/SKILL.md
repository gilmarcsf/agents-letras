---
name: review
description: "Review diffs, PRs, issues, CI failures, comments, simplification, regression risk, root cause, proof, and safe fixes."
---

# Review

Use this as the single review entrypoint. Pick the workflow from the user's wording and keep the output high-signal.

## Routing

- "review", "audit", "check this PR", "is this fix good": review PR, issue, branch, commit, or diff with cause, best fix, proof, and risk.
- "address comments", "requested changes": inspect unresolved PR review comments or inline feedback.
- "simplify", "clean up", "refactor changes": review local changes for reuse, clarity, efficiency, and safe simplification.
- "fix CI", "why checks fail": review failing GitHub Actions checks and identify root cause.
- "review swarm", "parallel review": use read-only sub-agents for broad or risky diffs.
- "codex review", "autoreview", "review closeout": run Codex's built-in review as an advisory closeout check.

## Scope

Prefer the smallest correct scope:

1. Explicit paths, PR, issue, branch, commit, or URL from the user
2. Current git changes
3. Current branch PR
4. Files edited earlier in the current turn

Use the smallest diff command that matches the scope:

```bash
git diff
git diff --cached
gh pr view <ref> --json number,title,state,author,body,comments,reviews,files,commits,statusCheckRollup,mergeStateStatus,headRefName,baseRefName,url
gh pr diff <ref> --patch
gh issue view <ref> --json number,title,state,author,body,comments,labels,updatedAt,url
```

Read local instructions and relevant docs before judging the change.

## Deep Review Contract

Always answer:

- Ref: issue, PR, branch, commit, or file scope.
- Surface: runtime, CLI, UI, API, data, build, docs, infra, or workflow.
- Bug or behavior: what changed or what is broken.
- Cause: code path and confidence. If not proven, say what evidence is missing.
- Best fix: whether the fix lands at the right ownership boundary.
- Refactor: whether a larger refactor improves correctness or clarity enough to justify risk.
- Proof: tests, CI, repro, logs, source docs, dependency docs, or live behavior checked.
- Risk: what remains unverified.

When the user says `/review`, treat it as this skill. Produce high-signal findings, not a generic summary:

1. Use the smallest correct scope.
2. Read local instructions and relevant docs.
3. Follow the real code path past the first touched file.
4. For each finding, include file/line or symbol, failure mode, why it matters, and concrete fix.
5. Separate real issues from open questions.

For PRs from an unknown external contributor, collect only public GitHub context when it changes review risk:

```bash
gh pr view <pr> --json author,commits,files,reviews,comments
gh api "users/<login>"
gh api "repos/<owner>/<repo>/contributors" --paginate
gh search prs --author "<login>" --repo "<owner>/<repo>" --json number,state,title,createdAt,mergedAt,url
```

Use it to calibrate review depth, not to judge the person. Report only relevant signals:

- prior activity in the repo
- size and focus of the current PR
- whether changes touch sensitive areas
- whether the author appears new to the project

Skip this for local work, trusted internal contributors, tiny docs-only changes, or when the user only wants code findings.

## PR Comments

For PR comments and requested changes:

1. Resolve the PR with `gh pr view`.
2. Fetch thread-aware review state when needed with `gh api graphql`; flat comments are not enough for unresolved inline review threads.
3. Group actionable feedback by behavior or file.
4. Separate real requested changes from informational comments, stale threads, duplicates, and conflicts.
5. If the user asked to fix comments, implement only actionable items in scope.
6. Do not reply, resolve threads, submit reviews, push, or merge unless explicitly asked.

If comments conflict or would cause a regression, stop and explain the tradeoff.

## Simplification

Review for:

- existing helpers or utilities that should be reused
- duplicated or near-duplicated logic
- redundant state, cached derived values, dead code, or needless indirection
- unnecessary recomputation, broad reads, repeated I/O, leaks, or missing cleanup
- unclear names, cleverness, or local convention drift

If the user asked only for review, report findings. If they asked to simplify or clean up, apply only high-confidence, behavior-preserving fixes and run focused validation.

## CI Review

For GitHub Actions failures:

```bash
gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow
gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha
gh run view <run_id> --log-failed
```

Inspect only failing or relevant jobs. Avoid broad log dumps. Identify the root cause before editing. If fixing CI requires product or workflow tradeoffs, explain before changing.

## Codex Closeout

Use Codex's built-in review only as advisory proof. Verify every accepted finding by reading the real code path before changing code.

Pick the target:

```bash
codex review --uncommitted
codex review --base origin/main
codex review --commit HEAD
```

For PR branches, prefer the actual PR base:

```bash
base=$(gh pr view --json baseRefName --jq .baseRefName)
codex review --base "origin/$base"
```

Rules:

- Do not switch review models.
- Do not push just to review.
- Reject speculative findings, broad rewrites, and fixes that over-complicate the codebase.
- If a review-triggered fix changes code, rerun focused tests and rerun review when it is worth the cost.
- Report accepted findings, rejected findings with reason, proof run, and remaining risk.

## Parallel Review

Use sub-agents only for broad or risky scopes. Keep them read-only.

Roles:

- intent and regression
- security and privacy
- performance and reliability
- contracts and coverage

Give each reviewer the same scope and intent packet. Ask for file/line or symbol, issue, impact, recommended fix, and confidence. The parent agent filters duplicates, drops weak findings, and owns final synthesis.

## Output

Lead with findings ordered by severity. Each finding needs file/line or symbol, concrete failure mode, and fix.

If no blocking issue exists, say that directly and list proof plus residual risk.

Compact shape:

```text
Ref:
Surface:
Findings:
Proof:
Risk:
Next:
```
