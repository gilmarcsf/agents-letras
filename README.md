# agents-letras

Configuração compartilhada para agentes de código (Claude Code, Codex, OpenCode). Compartilhada como referência — pega o que faz sentido, ignora o resto.

## O que tem aqui

```
agents-letras/
├── AGENTS.md          # instruções compartilhadas entre os agentes
├── docs/              # documentações
├── claude/            # configs específicas do Claude Code
│   ├── statusline-command.py
│   ├── statusline.png
│   └── README.md
└── skills/            # skills agrupadas por categoria
    ├── gerais/        # uso amplo (browser, gh, bootstrap, code reading)
    ├── mobile/        # Android e iOS/Apple
    └── review/        # revisão de diff e simplificação
```

## AGENTS.md

É o "system prompt" que cada agente lê antes de trabalhar. Define como o agente deve se comunicar, executar, testar, commitar, etc. É opinativo e reflete um estilo pessoal de trabalho.

Funciona em qualquer ferramenta que respeite o padrão `AGENTS.md` (Codex, outras) ou via symlink pra `~/.claude/CLAUDE.md` no caso do Claude Code.

## claude/

Configs específicas do Claude Code.

- [`statusline-command.py`](claude/statusline-command.py) — statusline custom com modelo, contexto restante, custo, branch e rate limits
- [`README.md`](claude/README.md) — como instalar a statusline

## skills/

Skills são módulos de instrução que o agente carrega sob demanda quando o pedido casa com a `description` no `SKILL.md` da skill. Cada subpasta é uma categoria temática com seu próprio README detalhando o que tem dentro:

- [`gerais/`](skills/gerais/README.md) — automação de browser, `gh` CLI, bootstrap de AGENTS.md, exploração de código, stress-test de design
- [`mobile/`](skills/mobile/README.md) — Android (AGP 9, R8, Compose, KMP, Material 3, Navigation 3, Play Billing) e Apple (SwiftUI, Swift Concurrency, Xcode CLI)
- [`review/`](skills/review/README.md) — review em paralelo com subagentes e simplificação automática de diffs

Pra usar localmente, copia ou symlinka a pasta da skill pra `~/.claude/skills/<nome>/` (global) ou `.claude/skills/<nome>/` (no projeto).
