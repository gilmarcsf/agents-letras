#!/usr/bin/env python3
"""Sync and validate Codex plugin state declared in codex/config.toml."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CODEX_HOME = Path.home() / ".codex"
CONFIG = REPO_ROOT / "codex" / "config.toml"


def enabled_plugins() -> list[str]:
    data = tomllib.loads(CONFIG.read_text())
    plugins = data.get("plugins", {})
    return sorted(
        plugin_id
        for plugin_id, settings in plugins.items()
        if isinstance(settings, dict) and settings.get("enabled") is True
    )


def split_plugin_id(plugin_id: str) -> tuple[str, str]:
    if "@" not in plugin_id:
        raise ValueError(f"invalid plugin id {plugin_id!r}; expected name@marketplace")
    name, marketplace = plugin_id.rsplit("@", 1)
    return name, marketplace


def plugin_source_exists(name: str, marketplace: str) -> bool:
    if marketplace == "openai-curated":
        return (CODEX_HOME / ".tmp" / "plugins" / "plugins" / name / ".codex-plugin" / "plugin.json").exists()
    if marketplace == "openai-bundled":
        return (CODEX_HOME / ".tmp" / "bundled-marketplaces" / "openai-bundled" / "plugins" / name).exists()
    if marketplace == "openai-primary-runtime":
        return True
    return True


def plugin_cache_exists(name: str, marketplace: str) -> bool:
    cache_root = CODEX_HOME / "plugins" / "cache" / marketplace / name
    if not cache_root.exists():
        return False
    return any(cache_root.glob("*/.codex-plugin/plugin.json"))


def run_marketplace_sync() -> None:
    if not shutil_which("codex"):
        print("  [warn] codex CLI not found; skipped marketplace upgrade")
        return

    marketplace_source = CODEX_HOME / ".tmp" / "plugins" / "plugins"
    if not marketplace_source.exists():
        add_result = subprocess.run(
            ["codex", "plugin", "marketplace", "add", "openai/plugins"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if add_result.returncode == 0:
            print("  [ok] codex plugin marketplace add openai/plugins")
        else:
            message = add_result.stdout.strip().splitlines()
            detail = message[-1] if message else "unknown error"
            print(f"  [warn] codex plugin marketplace add openai/plugins failed: {detail}")

    result = subprocess.run(
        ["codex", "plugin", "marketplace", "upgrade"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode == 0:
        print("  [ok] codex plugin marketplace upgrade")
        return

    message = result.stdout.strip().splitlines()
    detail = message[-1] if message else "unknown error"
    print(f"  [warn] codex plugin marketplace upgrade failed: {detail}")


def shutil_which(command: str) -> str | None:
    from shutil import which

    return which(command)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="upgrade configured Codex marketplaces before checking")
    parser.add_argument("--strict-cache", action="store_true", help="fail when enabled plugins are missing from local cache")
    args = parser.parse_args()

    if args.apply:
        run_marketplace_sync()

    plugins = enabled_plugins()
    errors: list[str] = []
    warnings: list[str] = []

    for plugin_id in plugins:
        name, marketplace = split_plugin_id(plugin_id)
        if not plugin_source_exists(name, marketplace):
            errors.append(f"{plugin_id}: source missing")
        if not plugin_cache_exists(name, marketplace):
            message = f"{plugin_id}: cache missing; Codex may fetch it lazily on first use"
            if args.strict_cache:
                errors.append(message)
            else:
                warnings.append(message)

    for warning in warnings:
        print(f"  [warn] {warning}")

    if errors:
        print("Codex plugin sync failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"  [ok] {len(plugins)} Codex plugin(s) declared in codex/config.toml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
