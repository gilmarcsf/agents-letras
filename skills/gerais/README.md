# Skills — Gerais

Ferramentas de uso amplo, sem amarração a stack específica. Servem para automação de browser, operações no GitHub, bootstrap de instruções de agente, exploração de código e estresse de design.

## Skills

### [`agent-browser`](agent-browser/SKILL.md)
CLI de automação de browser para agentes. Usa Chrome/Chromium via CDP direto.

- **Quando dispara:** pedidos como "abra o site X", "preencha esse form", "tira print da página", "extrai dados desta tabela", "testa o fluxo de login".
- **Como usar:** instale com `npm i -g agent-browser` (ou `brew`/`cargo`). Fluxo padrão: `agent-browser open <url>` → `agent-browser snapshot -i` (pega refs `@e1`, `@e2`...) → interage por ref → re-snapshot quando o DOM muda.
- **Útil para:** scraping leve, QA de fluxos web, validação de UI antes de marcar tarefa como pronta.

### [`agents-bootstrap`](agents-bootstrap/SKILL.md)
Cria ou atualiza um `AGENTS.md` local do repositório a partir de um template enxuto, e adiciona um symlink `CLAUDE.md` apontando para ele.

- **Quando dispara:** ao iniciar um repo novo ou quando o repositório precisa de instruções específicas (workflow, source-of-truth, fronteiras de arquitetura, comandos de validação, regras de naming, defaults de teste) que não cabem no `~/.agents/AGENTS.md` global.
- **Como usar:** invoca a skill e ela gera um `AGENTS.md` curto e operacional, focado em prevenir decisões erradas de agente nesse repo. É a dona desse bootstrap — outras skills (como `android-bootstrap`, `kmp-bootstrap`) delegam para ela.

### [`gh-cli`](gh-cli/SKILL.md)
Referência completa do GitHub CLI (`gh`) — versão 2.85.0+. Cobre repositórios, issues, PRs, Actions, projects, releases, gists, codespaces, organizações e extensões.

- **Quando dispara:** qualquer operação no GitHub via terminal. Por regra do `AGENTS.md`, sempre use `gh` em vez de `curl` direto na API ou navegação web.
- **Como usar:** consulte para sintaxe correta de comandos `gh` antes de executar, principalmente em fluxos de PR, release e Actions.

### [`grill-me`](grill-me/SKILL.md)
Modo entrevista: o Claude faz perguntas implacáveis até atingir entendimento compartilhado sobre um plano ou design.

- **Quando dispara:** o usuário diz "grill me", "me entrevista", "estressa esse plano", "quero que você desafie esse design".
- **Como usa:** uma pergunta por vez, percorrendo cada ramo da árvore de decisão. Para cada pergunta, oferece a resposta recomendada. Se a pergunta puder ser respondida lendo o código, ele lê em vez de perguntar.
- **Útil para:** validar plano antes de implementação, achar buracos em especs, alinhar tradeoffs.

### [`how`](how/SKILL.md)
Explica como algo funciona neste codebase, no nível de um sênior fazendo onboarding em um subsistema. Tem dois modos:

- **Explain (padrão):** explora o código e produz uma explicação arquitetural clara — suficiente para um modelo mental funcional, sem virar leitura linha-a-linha do código.
- **Critique:** explica primeiro, depois aciona múltiplos modelos em paralelo para apontar problemas arquiteturais de forma independente.
- **Quando dispara:** "como funciona X aqui?", "me explica a arquitetura desse fluxo", "critica esse subsistema".
