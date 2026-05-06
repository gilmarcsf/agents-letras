#!/usr/bin/env python3
"""Claude Code statusline — colorful, compact."""

import json
import os
import re
import subprocess
import sys

RESET = "\033[0m"
ANSI_CODE_RE = re.compile(r"^\d+(?:;\d+)*$")


def colors_enabled() -> bool:
    # https://no-color.org/ — any non-empty value disables
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("CLAUDE_STATUSLINE_NO_COLOR") == "1":
        return False
    return True


def c(code: str, text: object) -> str:
    plain_text = str(text)
    if not colors_enabled():
        return plain_text
    if not ANSI_CODE_RE.fullmatch(code):
        return plain_text
    return f"\033[{code}m{plain_text}{RESET}"


def to_float(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def main() -> None:
    data = json.load(sys.stdin)

    parts: list[str] = []
    sep = c("90", " · ")  # bright black — visible on light & dark terminals

    # Model — bold bright white
    model = (data.get("model") or {}).get("display_name", "")
    if model:
        parts.append(c("1;97", model))

    # Context remaining
    ctx = data.get("context_window") or {}
    used = to_float(ctx.get("used_percentage"))
    if used is not None:
        remaining = 100 - used
        label = f"{round(remaining)}% left"
        if remaining <= 20:
            parts.append(c("1;31", label))  # bold red
        elif remaining <= 50:
            parts.append(c("1;33", label))  # bold yellow
        else:
            parts.append(c("1;36", label))  # bold cyan

    # Cost — yellow
    cost = to_float((data.get("cost") or {}).get("total_cost_usd"))
    if cost is not None and cost > 0:
        parts.append(c("33", f"${cost:.2f}"))

    # Directory — bold blue
    workspace = data.get("workspace") or {}
    cwd = workspace.get("current_dir") or data.get("cwd", "")
    if cwd:
        home = os.path.expanduser("~")
        display = cwd.replace(home, "~", 1) if cwd.startswith(home) else cwd
        parts.append(c("1;34", display))

        # Git branch — bold magenta
        branch = git_branch(cwd)
        if branch:
            parts.append(c("1;35", branch))

    rate_limits = data.get("rate_limits") or {}

    # 5h rate limit
    five = to_float((rate_limits.get("five_hour") or {}).get("used_percentage"))
    if five is not None:
        parts.append(rate_pill(five, "5h"))

    # Weekly rate limit
    weekly = to_float((rate_limits.get("seven_day") or {}).get("used_percentage"))
    if weekly is not None:
        parts.append(rate_pill(weekly, "weekly"))

    print(sep.join(parts), end="")


def rate_pill(pct: float, label: str) -> str:
    s = f"{label} {pct:.0f}%"
    if pct >= 80:
        return c("1;31", s)  # bold red
    if pct >= 50:
        return c("1;33", s)  # bold yellow
    return c("90", s)        # bright black (gray)


def git_branch(cwd: str) -> str:
    try:
        env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
        r = subprocess.run(
            ["git", "-C", cwd, "symbolic-ref", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2,
            env=env,
        )
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


if __name__ == "__main__":
    main()
