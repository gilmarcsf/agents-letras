---
name: codex-worktree-handoff
description: "Prepare and complete Codex App worktree handoffs from detached experiments back to the target branch without merge commits."
---

# Codex Worktree Handoff

Use this skill to bridge Codex App worktree experiments back into an existing branch.

## Mental Model

Codex App worktrees are often detached from the branch used as their base. Git does not allow the same branch to be checked out in two worktrees at once, so do not check out the original target branch inside the Codex worktree.

Instead:

1. Run `prepare` inside the Codex worktree.
2. Use the Codex App native **Handoff to branch** button.
3. Run `complete` after the thread is local on the handoff branch.

The final target branch receives committed handoff work as real cherry-picked commits, without a merge commit. Any staged, unstaged, or untracked dirty state is restored afterward as dirty state. The temporary handoff branch is only a transport branch.

## Commands

Use the bundled script. Resolve `scripts/codex_worktree_handoff.py` relative to this skill directory, then run it from the target repository checkout:

```bash
SCRIPT="/absolute/path/to/codex-worktree-handoff/scripts/codex_worktree_handoff.py"
python "$SCRIPT" diagnose
python "$SCRIPT" prepare --target <existing-branch>
python "$SCRIPT" complete
```

Run commands from the repository checkout involved in the handoff.

## Prepare Phase

Run this inside the detached Codex worktree after the experiment looks useful:

```bash
SCRIPT="/absolute/path/to/codex-worktree-handoff/scripts/codex_worktree_handoff.py"
python "$SCRIPT" prepare --target feature/remove-buildconfig
```

The script:

- confirms the target branch exists
- confirms the target branch still matches the worktree merge base
- creates a transport branch named `handoff/<target-slug>` or a unique variant
- records handoff metadata in the Git common directory under `codex-handoff/`
- leaves all worktree changes intact

After prepare succeeds, click **Handoff to branch** in Codex App and select the generated handoff branch.

Do not use this phase to commit, merge, push, rebase, or switch to the original target branch. If the target branch already moved away from the worktree base, refresh the worktree or use `--allow-diverged-base` only when that divergence is intentional.

## Complete Phase

Run this after Codex App handoff, when the thread is local and the current branch is the handoff branch:

```bash
SCRIPT="/absolute/path/to/codex-worktree-handoff/scripts/codex_worktree_handoff.py"
python "$SCRIPT" complete
```

The script:

- reads the target branch and base commit from metadata
- refuses unsafe repo states such as merge/rebase/cherry-pick in progress
- refuses likely secret or credential paths in dirty state and committed handoff changes
- stashes dirty state with untracked files before switching branches
- switches to the target branch
- applies the handoff branch commit sequence with `git cherry-pick`
- restores dirty state with `git stash apply --index`
- deletes the temporary handoff branch after a clean apply
- leaves restored dirty changes staged, unstaged, or untracked as Git can preserve them

This phase expects the Codex App handoff to have moved the local checkout onto the handoff branch. It then switches that same checkout back to the original target branch. If the target branch is still checked out in another worktree, Git cannot switch to it and the script stops.

If the target branch moved after prepare, the script stops by default. Re-run with `--allow-target-moved` only when applying the same change sequence onto the newer target is intentional.

If the handoff branch has commits and dirty changes, commits are preserved as commits on the target branch, then the dirty state is restored on top. If there are no handoff commits, `complete` only restores the dirty state.

## Diagnose Phase

Use diagnose when the app does not show the expected handoff action or the branch state is unclear:

```bash
SCRIPT="/absolute/path/to/codex-worktree-handoff/scripts/codex_worktree_handoff.py"
python "$SCRIPT" diagnose
```

Report the current checkout, branch state, known handoff metadata, and the relevant worktree list.

## Safety Rules

- Never use this skill to transport `.env*`, keys, certificates, credentials, or secret-looking paths.
- Do not merge or rebase as part of this workflow.
- Do not push branches from this skill.
- Do not delete non-handoff branches.
- Stop if the script reports a conflict or an in-progress Git operation.
- Review the final diff on the target branch before committing.
