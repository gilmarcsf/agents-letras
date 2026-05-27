---
summary: "Index of durable docs for the agents setup."
read_when:
  - Looking for setup documentation.
  - Updating docs organization.
---

# docs

Documentação operacional do setup.

- `instruction-architecture.md`: como dividir instruções entre `AGENTS.md`, docs e skills.
- `engineering-principles.md`: princípios de implementação.
- `git-github.md`: fluxo de Git e GitHub.
- `tooling.md`: catálogo de ferramentas.
- `import.md`: mapa de instalação e symlinks.
- `path-layout.md`: como as pastas locais se conectam.
- `reference.md`: referência completa do repo.

Arquivos em `docs/` usam frontmatter para facilitar busca por agentes. Depois de editar, rode:

```bash
python3 scripts/validate-docs.py
```
