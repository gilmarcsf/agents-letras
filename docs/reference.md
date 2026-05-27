---
summary: "Full PT-BR reference for the agents-letras repo structure, files, configs, skills, and sync flow."
read_when:
  - Auditing the complete agents setup.
  - Updating broad repo documentation after structural changes.
---

# Referência Completa

Referência do repositório `agents-letras`.

## Visão geral

Este repo é a fonte versionada do setup de agentes. Ele centraliza:

- instruções em `AGENTS.md`
- skills source em `skills/`
- subagents em `agents/` e `codex/agents/`
- config de Claude em `claude/`
- config de Codex em `codex/`
- scripts de instalação e validação em `scripts/`

Estado local e sensível fica fora do Git.

## Estrutura

```text
AGENTS.md
README.md
install.sh
skills.toml
.githooks/
agents/
claude/
codex/
docs/
scripts/
skills/
```

## AGENTS.md

Regras globais para agentes. Deve conter só regras duráveis. Fluxos reutilizáveis vão para skills. Racional mais longo vai para docs.

## skills/

Árvore source categorizada. Cada skill tem `SKILL.md` no topo.

`skills-cli` gera `.runtime/skills`, que não é versionado. Esse runtime flat é o que Claude/Codex consomem quando instalados pelo `install.sh`.

## claude/

- `settings.json`: config do Claude.
- `mcp.json`: template de MCP servers com tokens via env vars.
- `statusline-command.py`: statusline custom.

`claude/claude.json` é uma base de config/estado do Claude. OAuth, IDs, projetos e histórico local não entram.

## codex/

- `config.toml`: config do Codex, usada diretamente como config final.
- `rules/default.rules`: regras de aprovação de comandos.
- `agents/`: custom agents do Codex.

Não versionar trusted projects, caches, marketplace state, tokens, desktop state ou paths pessoais.

## scripts/

Scripts de validação de docs, sync opcional de plugins Codex e sync auxiliar para Windows.

## install.sh

Cria symlinks em `~/.agents`, gera runtime de skills e conecta Claude/Codex ao hub.

O installer não instala pets e não copia caches de plugin.

## Segurança

Nunca versionar:

- `.env*`
- tokens e secrets
- dumps de ambiente
- trusted projects
- caches locais
- logs ou sessões
- OAuth e IDs de usuário de `claude/claude.json`
- trusted projects de `codex/config.toml`
- `.runtime/`

Valores sensíveis devem ser lidos por env vars fora do repo.
