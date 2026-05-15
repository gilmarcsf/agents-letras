# Skills

Skills são instruções especializadas que o agente carrega sob demanda quando o pedido casa com a `description` no frontmatter de cada `SKILL.md`. Funcionam em qualquer agente que respeite o padrão (Claude Code, Codex, OpenCode, etc).

## Como funciona

- Cada skill é uma pasta com um `SKILL.md` no nível superior — esse é o ponto de entrada que o agente lê.
- A skill dispara automaticamente quando o pedido casa com os gatilhos descritos. Algumas também aceitam invocação explícita via `/<nome>`.

## Aviso sobre o aninhamento

**Claude Code e Codex não suportam skills em pastas aninhadas.** A skill tem que ficar direto no diretório varrido — sem categoria no caminho:

- **Codex:** `~/.agents/skills/<nome>/SKILL.md` (path oficial)
- **Claude Code:** `~/.claude/skills/<nome>/SKILL.md` — não lê de `~/.agents/` nativamente; pra reaproveitar a mesma pasta, faz `ln -s ~/.agents/skills ~/.claude/skills`

As subpastas `gerais/`, `mobile/` e `review/` aqui no repo são **só pra organização visual**. Pra usar localmente, copia ou symlinka **a pasta da skill em si** (não a categoria):

```bash
# Exemplo: skill "how" da categoria "gerais"
# Codex
ln -sf "$(pwd)/skills/gerais/how" ~/.agents/skills/how
# Claude Code
ln -sf "$(pwd)/skills/gerais/how" ~/.claude/skills/how
```

## Categorias

| Categoria | O que tem | Link |
|---|---|---|
| **Gerais** | Ferramentas de uso amplo: automação de browser, CLI do GitHub, bootstrap de `AGENTS.md`, exploração de código e entrevista de design | [`gerais/`](gerais/README.md) |
| **Mobile** | Android (AGP, R8, Compose, KMP, Play Billing, Navigation 3, edge-to-edge) e Apple (SwiftUI, Swift Concurrency, XcodeBuildMCP) | [`mobile/`](mobile/README.md) |
| **Review** | Revisão de diffs em paralelo com subagentes e simplificação automática de mudanças | [`review/`](review/README.md) |
