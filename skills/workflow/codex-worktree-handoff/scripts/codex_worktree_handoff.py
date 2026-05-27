#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class HandoffError(RuntimeError):
    pass


@dataclass(frozen=True)
class Git:
    root: Path

    def run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["git", *args],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if check and result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise HandoffError(f"git {' '.join(args)} failed: {detail}")
        return result

    def out(self, *args: str, check: bool = True) -> str:
        return self.run(*args, check=check).stdout.strip()


def find_repo() -> Git:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise HandoffError("Run this command inside a Git repository.")
    return Git(Path(result.stdout.strip()).resolve())


def current_branch(git: Git) -> str | None:
    result = git.run("symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def short_head(git: Git) -> str:
    return git.out("rev-parse", "--short=8", "HEAD")


def full_head(git: Git) -> str:
    return git.out("rev-parse", "HEAD")


def ensure_valid_branch_name(git: Git, branch: str, label: str) -> None:
    if not branch or branch.startswith("-"):
        raise HandoffError(f"Invalid {label} branch name: {branch!r}")
    result = git.run("check-ref-format", "--branch", branch, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise HandoffError(f"Invalid {label} branch name: {branch!r}\n{detail}")


def branch_ref(branch: str) -> str:
    return f"refs/heads/{branch}"


def branch_exists(git: Git, branch: str) -> bool:
    ensure_valid_branch_name(git, branch, "local")
    return git.run("show-ref", "--verify", "--quiet", branch_ref(branch), check=False).returncode == 0


def ref_commit(git: Git, branch: str) -> str:
    ensure_valid_branch_name(git, branch, "local")
    return git.out("rev-parse", "--verify", f"{branch_ref(branch)}^{{commit}}")


def ensure_commit(git: Git, commit: str, label: str) -> None:
    result = git.run("cat-file", "-e", f"{commit}^{{commit}}", check=False)
    if result.returncode != 0:
        raise HandoffError(f"Invalid {label} commit in metadata: {commit}")


def merge_base(git: Git, branch: str) -> str:
    return git.out("merge-base", "HEAD", branch_ref(branch))


def git_common_dir(git: Git) -> Path:
    path = git.out("rev-parse", "--git-common-dir")
    common = Path(path)
    if not common.is_absolute():
        common = git.root / common
    return common.resolve()


def metadata_dir(git: Git) -> Path:
    return git_common_dir(git) / "codex-handoff"


def metadata_path(git: Git, handoff_branch: str) -> Path:
    digest = hashlib.sha256(handoff_branch.encode("utf-8")).hexdigest()[:12]
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "__", handoff_branch)
    return metadata_dir(git) / f"{safe}-{digest}.json"


def slug_branch(branch: str) -> str:
    slug = branch.strip().lower()
    slug = re.sub(r"[^a-z0-9._/-]+", "-", slug)
    slug = re.sub(r"/+", "/", slug).strip("/.-")
    slug = slug.replace("/", "-")
    return slug or "branch"


def unique_handoff_branch(git: Git, target: str, explicit: str | None) -> str:
    if explicit:
        ensure_valid_branch_name(git, explicit, "handoff")
        if not explicit.startswith("handoff/"):
            raise HandoffError("Explicit handoff branch must start with handoff/.")
        if branch_exists(git, explicit):
            raise HandoffError(f"Branch already exists: {explicit}")
        return explicit

    base = f"handoff/{slug_branch(target)}"
    ensure_valid_branch_name(git, base, "handoff")
    if not branch_exists(git, base):
        return base

    candidate = f"{base}-{short_head(git)}"
    ensure_valid_branch_name(git, candidate, "handoff")
    if not branch_exists(git, candidate):
        return candidate

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    candidate = f"{base}-{stamp}"
    ensure_valid_branch_name(git, candidate, "handoff")
    if branch_exists(git, candidate):
        raise HandoffError(f"Could not generate a unique handoff branch for {target}.")
    return candidate


def status_lines(git: Git) -> list[str]:
    output = git.out("status", "--porcelain=v1")
    return [line for line in output.splitlines() if line]


def changed_paths(git: Git) -> list[str]:
    output = git.run("status", "--porcelain=v1", "-z").stdout
    if not output:
        return []
    paths: list[str] = []
    entries = output.split("\0")
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if not entry:
            continue
        status = entry[:2]
        path = entry[3:]
        if path:
            paths.append(path)
        if "R" in status or "C" in status:
            if index < len(entries) and entries[index]:
                paths.append(entries[index])
            index += 1
    return paths


def range_paths(git: Git, base: str, branch: str) -> list[str]:
    output = git.run("diff", "--name-status", "-z", f"{base}..{branch_ref(branch)}").stdout
    if not output:
        return []
    paths: list[str] = []
    entries = output.split("\0")
    index = 0
    while index < len(entries):
        status = entries[index]
        index += 1
        if not status:
            continue
        if index < len(entries) and entries[index]:
            paths.append(entries[index])
        index += 1
        if status.startswith("R") or status.startswith("C"):
            if index < len(entries) and entries[index]:
                paths.append(entries[index])
            index += 1
    return paths


def forbidden_paths(paths: list[str]) -> list[str]:
    forbidden: list[str] = []
    sensitive_suffixes = (".env", ".pem", ".key", ".p12", ".pfx", ".crt", ".cer")
    sensitive_names = {
        ".env",
        ".netrc",
        "id_rsa",
        "id_dsa",
        "id_ecdsa",
        "id_ed25519",
        "known_hosts",
    }
    for path in paths:
        name = Path(path).name
        lower_name = name.lower()
        lower_path = path.lower()
        if (
            lower_name in sensitive_names
            or lower_name.startswith(".env.")
            or lower_name.endswith(sensitive_suffixes)
            or "secret" in lower_path
            or "credential" in lower_path
        ):
            forbidden.append(path)
    return forbidden


def ensure_no_forbidden_dirty_paths(git: Git) -> None:
    forbidden = forbidden_paths(changed_paths(git))
    if forbidden:
        raise HandoffError(
            "Refusing to stage likely secret or credential files:\n"
            + "\n".join(f"  {path}" for path in forbidden)
        )


def ensure_no_forbidden_range_paths(git: Git, base: str, branch: str) -> None:
    forbidden = forbidden_paths(range_paths(git, base, branch))
    if forbidden:
        raise HandoffError(
            "Refusing to apply likely secret or credential files from handoff commits:\n"
            + "\n".join(f"  {path}" for path in forbidden)
        )


def ensure_no_git_operation(git: Git) -> None:
    git_dir = Path(git.out("rev-parse", "--git-dir"))
    if not git_dir.is_absolute():
        git_dir = git.root / git_dir
    common = git_common_dir(git)
    markers = [
        git_dir / "MERGE_HEAD",
        git_dir / "CHERRY_PICK_HEAD",
        git_dir / "REVERT_HEAD",
        git_dir / "REBASE_HEAD",
        git_dir / "rebase-apply",
        git_dir / "rebase-merge",
        common / "MERGE_HEAD",
        common / "CHERRY_PICK_HEAD",
        common / "REVERT_HEAD",
        common / "REBASE_HEAD",
        common / "rebase-apply",
        common / "rebase-merge",
    ]
    active = [str(path) for path in markers if path.exists()]
    if active:
        raise HandoffError("Git operation in progress. Finish or abort it first:\n" + "\n".join(active))


def parse_worktrees(git: Git) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in git.out("worktree", "list", "--porcelain").splitlines():
        if not line:
            if current:
                entries.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    if current:
        entries.append(current)
    return entries


def branch_checked_elsewhere(git: Git, branch: str) -> str | None:
    current_root = git.root.resolve()
    expected_ref = branch_ref(branch)
    for entry in parse_worktrees(git):
        path = Path(entry.get("worktree", "")).resolve()
        if path == current_root:
            continue
        if entry.get("branch") == expected_ref:
            return str(path)
    return None


def write_metadata(
    git: Git,
    handoff_branch: str,
    target: str,
    base: str,
    target_commit_at_prepare: str,
) -> None:
    data = {
        "version": 1,
        "handoff_branch": handoff_branch,
        "target_branch": target,
        "base_commit": base,
        "target_commit_at_prepare": target_commit_at_prepare,
        "source_worktree": str(git.root),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    directory = metadata_dir(git)
    directory.mkdir(parents=True, exist_ok=True)
    metadata_path(git, handoff_branch).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise HandoffError(f"Invalid handoff metadata JSON at {path}: {error}") from error
    if not isinstance(data, dict):
        raise HandoffError(f"Invalid handoff metadata at {path}: expected object.")
    return data


def read_metadata(git: Git, handoff_branch: str) -> dict[str, str]:
    path = metadata_path(git, handoff_branch)
    if not path.exists():
        raise HandoffError(
            f"No handoff metadata found for {handoff_branch} at {path}. "
            "Run prepare first from the source worktree."
        )
    data = read_json_file(path)
    required = [
        "version",
        "handoff_branch",
        "target_branch",
        "base_commit",
        "target_commit_at_prepare",
    ]
    missing = [key for key in required if key not in data]
    if missing:
        raise HandoffError(f"Invalid handoff metadata at {path}: missing {', '.join(missing)}.")
    if data["version"] != 1:
        raise HandoffError(f"Unsupported handoff metadata version: {data['version']}")
    for key in required:
        if key != "version" and not isinstance(data[key], str):
            raise HandoffError(f"Invalid handoff metadata at {path}: {key} must be a string.")
    if data["handoff_branch"] != handoff_branch:
        raise HandoffError(
            f"Metadata branch mismatch: current={handoff_branch}, metadata={data['handoff_branch']}"
        )
    return {key: data[key] for key in required if key != "version"}


def remove_metadata(git: Git, handoff_branch: str) -> None:
    path = metadata_path(git, handoff_branch)
    if path.exists():
        path.unlink()


def diagnose(_: argparse.Namespace) -> None:
    git = find_repo()
    branch = current_branch(git)
    paths = changed_paths(git)
    print(f"Repo: {git.root}")
    print(f"HEAD: {full_head(git)}")
    print(f"Branch: {branch or '(detached HEAD)'}")
    print(f"Status entries: {len(paths)}")
    forbidden = forbidden_paths(paths)
    if forbidden:
        print("Forbidden dirty paths:")
        for path in forbidden:
            print(f"- {path}")
    print()
    print("Worktrees:")
    for entry in parse_worktrees(git):
        path = entry.get("worktree", "(unknown)")
        head = entry.get("HEAD", "")
        branch_ref_value = entry.get("branch", "(detached)")
        print(f"- {path} {head[:8]} {branch_ref_value}")
    print()
    meta = metadata_dir(git)
    if meta.exists():
        print("Handoff metadata:")
        for path in sorted(meta.glob("*.json")):
            print(f"- {path.name}")
    else:
        print("Handoff metadata: none")


def prepare(args: argparse.Namespace) -> None:
    git = find_repo()
    ensure_no_git_operation(git)
    ensure_valid_branch_name(git, args.target, "target")

    if not branch_exists(git, args.target):
        raise HandoffError(f"Target branch does not exist: {args.target}")

    branch = current_branch(git)
    if branch and not args.allow_attached:
        raise HandoffError(
            f"Current checkout is already on branch {branch}. "
            "Prepare is intended for detached Codex worktrees. Use --allow-attached to override."
        )

    target_commit = ref_commit(git, args.target)
    base = merge_base(git, args.target)
    handoff_branch = unique_handoff_branch(git, args.target, args.branch)

    print(f"Repo: {git.root}")
    print(f"Target branch: {args.target} ({target_commit[:8]})")
    print(f"Current HEAD: {full_head(git)[:8]}")
    print(f"Merge base: {base[:8]}")
    print(f"Handoff branch: {handoff_branch}")
    if target_commit != base:
        message = (
            "Target branch does not match this worktree merge base. "
            "Refresh the worktree or rerun with --allow-diverged-base if this is intentional."
        )
        if not args.allow_diverged_base:
            raise HandoffError(message)
        print(f"Warning: {message}")

    ensure_no_forbidden_dirty_paths(git)

    if args.dry_run:
        print("Dry run: no branch created.")
        return

    git.run("switch", "-c", handoff_branch)
    write_metadata(git, handoff_branch, args.target, base, target_commit)
    print()
    print("Prepared.")
    print(f"Now use Codex App: Handoff to branch -> {handoff_branch}")
    print("After the app handoff completes, run complete from the bundled skill script.")


def stash_dirty_state(git: Git, branch: str) -> str | None:
    if not status_lines(git):
        return None
    ensure_no_forbidden_dirty_paths(git)
    before = git.out("rev-parse", "--verify", "stash@{0}", check=False)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    message = f"codex-handoff-dirty:{branch}:{stamp}"
    git.run("stash", "push", "--include-untracked", "--message", message)
    after = git.out("rev-parse", "--verify", "stash@{0}", check=False)
    if not after or after == before:
        raise HandoffError("Expected git stash push to save dirty state, but no new stash was created.")
    return "stash@{0}"


def apply_dirty_stash(git: Git, stash_ref: str) -> None:
    git.run("stash", "apply", "--index", stash_ref)


def drop_dirty_stash(git: Git, stash_ref: str) -> None:
    result = git.run("stash", "drop", stash_ref, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        print()
        print(f"Applied dirty state, but failed to drop stash {stash_ref}: {detail}")


def commits_to_apply(git: Git, base: str, handoff_branch: str) -> list[str]:
    output = git.out("rev-list", "--reverse", f"{base}..{branch_ref(handoff_branch)}")
    return [line for line in output.splitlines() if line]


def ensure_no_merge_commits(git: Git, commits: list[str]) -> None:
    merge_commits: list[str] = []
    for commit in commits:
        parents = git.out("rev-list", "--parents", "-n", "1", commit).split()
        if len(parents) > 2:
            merge_commits.append(commit)
    if merge_commits:
        short = ", ".join(commit[:8] for commit in merge_commits)
        raise HandoffError(f"Cannot apply handoff range with merge commits: {short}")


def complete(args: argparse.Namespace) -> None:
    git = find_repo()
    ensure_no_git_operation(git)

    handoff_branch = current_branch(git)
    if not handoff_branch:
        raise HandoffError("Complete must run on a handoff branch, not detached HEAD.")
    if not handoff_branch.startswith("handoff/"):
        raise HandoffError(f"Current branch is {handoff_branch}. Expected a handoff/* branch.")

    data = read_metadata(git, handoff_branch)
    target = data["target_branch"]
    base = data["base_commit"]
    target_commit_at_prepare = data["target_commit_at_prepare"]

    ensure_valid_branch_name(git, target, "target")
    ensure_commit(git, base, "base")
    ensure_commit(git, target_commit_at_prepare, "target_at_prepare")
    if not branch_exists(git, target):
        raise HandoffError(f"Target branch no longer exists: {target}")
    if git.run("merge-base", "--is-ancestor", base, branch_ref(handoff_branch), check=False).returncode != 0:
        raise HandoffError("Base commit is not an ancestor of the handoff branch.")

    target_commit = ref_commit(git, target)
    target_moved = target_commit != target_commit_at_prepare
    if target_moved and not args.allow_target_moved:
        raise HandoffError(
            "Target branch moved since prepare.\n"
            f"  target:             {target} at {target_commit[:8]}\n"
            f"  target at prepare:  {target_commit_at_prepare[:8]}\n"
            "Re-run with --allow-target-moved only if applying onto the newer target is intentional."
        )

    checked_path = branch_checked_elsewhere(git, target)
    if checked_path:
        raise HandoffError(f"Target branch is checked out in another worktree: {checked_path}")

    dirty_paths = changed_paths(git)
    forbidden_dirty = forbidden_paths(dirty_paths)
    commits = commits_to_apply(git, base, handoff_branch)
    forbidden_committed = forbidden_paths(range_paths(git, base, handoff_branch))

    print(f"Repo: {git.root}")
    print(f"Handoff branch: {handoff_branch}")
    print(f"Target branch: {target}")
    print(f"Base commit: {base[:8]}")
    print(f"Target at prepare: {target_commit_at_prepare[:8]}")
    print(f"Target now: {target_commit[:8]}")

    if args.dry_run:
        print(f"Dry run: dirty entries={len(dirty_paths)}, commits ahead={len(commits)}")
        print(f"Dry run: target moved={'yes' if target_moved else 'no'}")
        print(f"Dry run: target checked elsewhere={checked_path or 'no'}")
        if forbidden_dirty:
            print("Dry run: forbidden dirty paths:")
            for path in forbidden_dirty:
                print(f"  {path}")
        if forbidden_committed:
            print("Dry run: forbidden committed paths:")
            for path in forbidden_committed:
                print(f"  {path}")
        return

    if not commits and not dirty_paths:
        raise HandoffError("No commits or dirty changes to apply from handoff branch.")
    if forbidden_dirty:
        ensure_no_forbidden_dirty_paths(git)
    ensure_no_forbidden_range_paths(git, base, handoff_branch)
    ensure_no_merge_commits(git, commits)

    stash_ref = stash_dirty_state(git, handoff_branch)
    pre_apply_target = ref_commit(git, target)
    git.run("switch", target)
    try:
        if commits:
            git.run("cherry-pick", *commits)
    except HandoffError:
        print()
        print("Cherry-pick failed. Resolve conflicts on the target branch.")
        print(f"Target was at {pre_apply_target[:8]} before apply.")
        print("Use `git cherry-pick --abort` if you want to abandon the apply.")
        print(f"The handoff branch was kept: {handoff_branch}")
        if stash_ref:
            print(f"Dirty state was kept in {stash_ref}.")
        raise

    try:
        if stash_ref:
            apply_dirty_stash(git, stash_ref)
    except HandoffError:
        print()
        print("Dirty state apply failed. Resolve conflicts on the target branch.")
        print(f"The handoff branch was kept: {handoff_branch}")
        print(f"Dirty state was kept in {stash_ref}.")
        raise

    if stash_ref:
        drop_dirty_stash(git, stash_ref)

    delete_result = git.run("branch", "-D", handoff_branch, check=False)
    if delete_result.returncode != 0:
        detail = delete_result.stderr.strip() or delete_result.stdout.strip()
        print()
        print(f"Applied changes, but failed to delete handoff branch: {detail}")
        print(f"Metadata kept at: {metadata_path(git, handoff_branch)}")
        return

    remove_metadata(git, handoff_branch)
    print()
    print("Completed.")
    print(f"Cherry-picked {len(commits)} commit(s) onto {target}.")
    if stash_ref:
        print("Restored dirty state with staged entries preserved where Git could preserve them.")
    print("Review the branch status before continuing.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare and complete Codex App worktree handoffs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    diagnose_parser = subparsers.add_parser("diagnose", help="Show current repo/worktree handoff state.")
    diagnose_parser.set_defaults(func=diagnose)

    prepare_parser = subparsers.add_parser("prepare", help="Create a temporary handoff branch.")
    prepare_parser.add_argument("--target", required=True, help="Existing branch that should receive the final changes.")
    prepare_parser.add_argument("--branch", help="Explicit handoff branch name. Must start with handoff/.")
    prepare_parser.add_argument("--allow-attached", action="store_true", help="Allow prepare when not detached.")
    prepare_parser.add_argument(
        "--allow-diverged-base",
        action="store_true",
        help="Allow prepare when target no longer matches the worktree merge base.",
    )
    prepare_parser.add_argument("--dry-run", action="store_true", help="Print the plan without creating a branch.")
    prepare_parser.set_defaults(func=prepare)

    complete_parser = subparsers.add_parser("complete", help="Apply a handoff branch back to its target branch.")
    complete_parser.add_argument("--allow-target-moved", action="store_true", help="Apply even if target advanced after prepare.")
    complete_parser.add_argument("--dry-run", action="store_true", help="Print the plan without changing branches.")
    complete_parser.set_defaults(func=complete)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except HandoffError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
