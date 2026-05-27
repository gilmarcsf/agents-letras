#!/usr/bin/env python3
"""Validate docs/*.md frontmatter used for agent retrieval hints."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def parse_frontmatter(path: Path) -> tuple[dict[str, object] | None, str | None]:
    text = path.read_text()
    if not text.startswith("---\n"):
        return None, "missing frontmatter"

    end = text.find("\n---\n", 4)
    if end == -1:
        return None, "unterminated frontmatter"

    data: dict[str, object] = {}
    current_list: str | None = None
    for line in text[4:end].splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            if current_list is None:
                return None, f"list item without key: {stripped}"
            data.setdefault(current_list, [])
            value = stripped[2:].strip()
            if value:
                assert isinstance(data[current_list], list)
                data[current_list].append(value)
            continue
        if ":" not in stripped:
            return None, f"invalid frontmatter line: {stripped}"
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value:
            data[key] = value
            current_list = None
        else:
            data[key] = []
            current_list = key

    return data, None


def main() -> int:
    errors: list[str] = []
    docs = sorted(path for path in DOCS.rglob("*.md") if "/archive/" not in path.as_posix())

    for path in docs:
        data, error = parse_frontmatter(path)
        rel = path.relative_to(ROOT)
        if error:
            errors.append(f"{rel}: {error}")
            continue
        assert data is not None
        summary = data.get("summary")
        read_when = data.get("read_when")
        if not isinstance(summary, str) or not summary.strip():
            errors.append(f"{rel}: missing non-empty summary")
        if not isinstance(read_when, list) or not any(str(item).strip() for item in read_when):
            errors.append(f"{rel}: missing non-empty read_when list")

    if errors:
        print("Docs validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(docs)} doc(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
