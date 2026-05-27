#!/usr/bin/env python3
"""Sincroniza AGENTS.md e codex/config.toml pro Codex do Windows.

Transformações no config.toml:
- Copia o config do repo
- Preserva blocos `[projects.*]` existentes (trust_level local)

Roda no WSL, escreve em /mnt/c/Users/$WIN_USER/.codex.
Defina WIN_USER explicitamente para evitar gravar no usuário errado.
"""
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WIN_USER = os.environ.get("WIN_USER")

if not WIN_USER:
    sys.exit("WIN_USER is required, for example: WIN_USER=alice scripts/sync-codex-windows.py")

WIN_CODEX = Path(f"/mnt/c/Users/{WIN_USER}/.codex")

if not WIN_CODEX.is_dir():
    sys.exit(f"not found: {WIN_CODEX}")

shutil.copy(REPO / "AGENTS.md", WIN_CODEX / "AGENTS.md")
print(f"  synced: {WIN_CODEX / 'AGENTS.md'}")

dest = WIN_CODEX / "config.toml"

preserved_projects = ""
if dest.exists():
    keep = False
    buf = []
    for line in dest.read_text().splitlines(keepends=True):
        if line.startswith("[projects."):
            keep = True
        elif line.startswith("[") and keep:
            keep = False
        if keep:
            buf.append(line)
    preserved_projects = "".join(buf)

out = []
for line in (REPO / "codex" / "config.toml").read_text().splitlines(keepends=True):
    out.append(line)

separator = "\n" if preserved_projects else ""
dest.write_text("".join(out) + separator + preserved_projects)
print(f"  synced: {dest}")
