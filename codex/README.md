# codex

Config para Codex.

## Arquivos

- `config.toml`: config do Codex, pronta para ser usada como `~/.codex/config.toml`.
- `agents/`: custom agents do Codex em TOML.
- `rules/`: regras de aprovação de comandos.

## Como funciona

`codex/config.toml` é a única fonte versionada de config Codex neste repo. Ele é comentado e não depende da config pessoal de ninguém.

Ele não deve receber trusted projects, tokens, OAuth, histórico local, caches privados, paths absolutos, marketplace state ou preferências desktop específicas de uma máquina.

O installer cria:

```text
~/.agents/codex              -> <repo>/codex
~/.codex/config.toml         -> ~/.agents/codex/config.toml
~/.codex/rules/default.rules -> ~/.agents/codex/rules/default.rules
~/.codex/agents              -> ~/.agents/codex/agents
~/.codex/AGENTS.md           -> ~/.agents/AGENTS.md
```

## O que não entra

Não versionar plugin cache, plugin sources, trusted projects, tokens, OAuth, IDs de usuário, paths absolutos ou histórico local.
