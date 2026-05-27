# agents-letras

Setup versionado para agentes de código: instruções globais, skills, subagents, configs de Claude/Codex, scripts de instalação e docs operacionais.

Este repo versiona o que é útil reaproveitar. Ele não versiona runtime gerado, trusted projects, tokens, caches, logs, pets ou estado sensível específico de uma máquina.

## Modos de uso

### Simples

Use os arquivos diretamente:

- `AGENTS.md` como instrução base.
- `skills/<categoria>/<skill>/` como catálogo de skills source.
- `claude/statusline-command.py` se quiser a statusline custom do Claude.

Nesse modo não precisa rodar installer nem `skills-cli`.

### Completo

Use o installer:

```bash
./install.sh
```

Ele cria um hub em `~/.agents`, gera `.runtime/skills` com o `skills-cli`, aplica a config do Codex e cria symlinks para Claude e Codex.

## Layout

```text
AGENTS.md              # instruções base para agentes
agents/                # subagents
claude/                # settings, MCP template e statusline do Claude
codex/                 # config, regras e custom agents do Codex
docs/                  # docs de arquitetura, import, GitHub e tooling
scripts/               # helpers de sync, validação e config
skills/                # skills source, agrupadas por categoria
skills.toml            # config do skills-cli
install.sh             # installer idempotente por symlink
.githooks/             # hooks locais opcionais
```

## O que fica fora

- `.runtime/`: gerado pelo `skills-cli`.
- trusted projects, OAuth, IDs de usuário e histórico local.
- `codex/plugins-cache` e `codex/plugin-sources`: caches locais.
- `pets/`: não faz parte deste repo.
- secrets, tokens, `.env*`, trusted projects, logs e dumps de ambiente.

## Validação

```bash
skills --config skills.toml validate --plain
skills --config skills.toml plan --plain
python3 scripts/validate-docs.py
git diff --check
```

Quem não usa `skills-cli` pode ignorar os comandos de skills e copiar/symlinkar as pastas manualmente.
