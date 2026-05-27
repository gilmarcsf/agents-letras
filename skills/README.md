# skills

Skills source.

Cada skill é uma pasta com `SKILL.md` no topo. O repo organiza essas pastas por categoria para leitura humana. Ferramentas como Claude e Codex geralmente esperam um runtime flat, por isso quem usa `skills-cli` roda sync para gerar `.runtime/skills`.

## Dois jeitos de usar

### Manual

Copie ou symlinke uma skill específica:

```bash
ln -sf "$(pwd)/skills/mobile/android-cli" "$HOME/.claude/skills/android-cli"
```

### Com skills-cli

```bash
skills --config skills.toml plan --plain
skills --config skills.toml sync --apply
```

O runtime gerado em `.runtime/skills` não é versionado.

## Categorias

| Categoria | Uso |
|---|---|
| `apple/` | Swift, SwiftUI, Xcode e plataformas Apple |
| `automation/` | Reservado para automações genéricas |
| `cloud/` | Reservado para cloud e infra |
| `fun/` | Fluxos experimentais ou criativos |
| `gerais/` | Compatibilidade com a organização antiga |
| `git-github/` | GitHub, PRs, issues e branches |
| `mobile/` | Android, KMP, Gradle, emulator e mobile UI |
| `product-growth/` | Produto, copy, pricing e direção |
| `research/` | Exploração e explicação de codebase |
| `review/` | Revisão de diff e qualidade |
| `web/` | Frontend, React, Next.js, UI e performance |
| `workflow/` | Handoff, pickup, skills-cli e coordenação |

Depois de editar skills:

```bash
skills --config skills.toml validate --plain
skills --config skills.toml plan --plain
```
