# agents

Subagents para ferramentas que suportam agentes especializados.

Cada arquivo descreve um agente com escopo estreito, por exemplo uma revisão estrutural rigorosa. Evite colocar prompts soltos ou experimentos locais aqui.

## Como usar

O installer cria:

```text
~/.agents/agents  ->  <repo>/agents
~/.claude/agents  ->  ~/.agents/agents
```

Codex custom agents ficam em `codex/agents/`, porque usam outro formato.
