#!/usr/bin/env python3
"""List docs with summary/read_when hints for quick agent re-entry."""

from __future__ import annotations

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
        if stripped.startswith("- ") and current_list:
            assert isinstance(data[current_list], list)
            data[current_list].append(stripped[2:].strip())
            continue
        if ":" not in stripped:
            return None, f"invalid frontmatter line: {stripped}"
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        data[key] = value if value else []
        current_list = key if not value else None
    return data, None


def main() -> int:
    for path in sorted(DOCS.rglob("*.md")):
        data, error = parse_frontmatter(path)
        rel = path.relative_to(DOCS)
        if error or data is None:
            print(f"{rel} - [{error or 'invalid frontmatter'}]")
            continue
        print(f"{rel} - {data.get('summary', '')}")
        read_when = data.get("read_when", [])
        if isinstance(read_when, list):
            for item in read_when:
                print(f"  Read when: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
