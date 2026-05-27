# scripts

Helpers usados pelo installer, pelos hooks e pela manutenção do setup.

## Config Codex

- `sync-codex-plugins.py`: valida plugins declarados em `codex/config.toml`.
- `sync-codex-windows.py`: helper opcional para WSL/Windows.

## Docs

- `validate-docs.py`: valida frontmatter em `docs/*.md`.
- `docs-list.py`: lista docs e seus gatilhos.

Scripts não devem conter secrets, paths pessoais obrigatórios ou decisões específicas de uma máquina.
