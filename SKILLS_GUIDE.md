# Guia de Skills Globais

> Arquivo de referência pessoal — **não é uma skill**, não interfere no Claude Code.
> Local: `~/.claude/SKILLS_GUIDE.md` · Pastas: `ls ~/.claude/skills/`
>
> **Histórico de limpeza:** 154 → 89 → 82 → 44 → **46 skills locais** (2026-09-15). Critério: qualidade sobre quantidade — só skills grandes, consolidadas, de framework/produto real ou de uso ativo confirmado. Cortados: 45 `marketing--*` (pack autoral fora de foco), 19 `composio--*` de nicho pessoal, `dev--security-auditor` (frontmatter inválido), 7 duplicatas de skills oficiais/mattpocock, 10 `frontend--threejs-*` (sem uso), 14 `arch--browserbase-*` (sem uso), + consolidação de redundâncias (`ai--`, `db--`, `dev--`, `frontend--`, `composio--`, `context7`). Adicionados `tools--skill-lint` + `tools--skill-audit` (+ agente `skill-reviewer`) pra não repetir esse trabalho manual. **Mesma data:** instalados 4 plugins oficiais (`claude-md-management`, `claude-security`, `hookify`, `commit-commands`) pra cobrir gaps reais sem duplicar skills locais — ver seção abaixo.

---

## Como funciona

**Ativação automática:** Claude Code lê o `description` do `SKILL.md` e ativa sozinho quando a situação encaixa.
**Ativação manual:** pedido natural ("usa a skill de X"), referência direta, ou slash command (`/nome-da-skill`).

**Dois mecanismos:**
| | Skills-pasta (`.claude/skills/`) | Plugin marketplace |
|---|---|---|
| Como carrega | Claude Code varre `SKILL.md` direto | `/plugin` — cache em `~/.claude/plugins/cache/` |
| Update | manual (reinstala) | `claude plugin update` |
| Usa aqui | as 46 abaixo | superpowers, mattpocock-skills, code-review, frontend-design, skill-creator, code-simplifier, claude-code-setup, claude-md-management, claude-security, hookify, commit-commands, caveman, genjutsu, gsap-skills |

### Setup em máquina nova
```bash
git clone https://github.com/LucasGS520/Claude-Skills.git && cd Claude-Skills && ./install.sh
```
Copia `.claude/skills/*` pra `~/.claude/skills/` + instala plugins de `plugins.json` (marketplaces de terceiros + oficiais Anthropic), idempotente.

---

## Skills oficiais / plugins (mantidas sempre — não editar)

Prefira estas antes de qualquer skill custom equivalente. Ficam em `~/.claude/plugins/cache/`, atualizadas pelo sistema.

| Fonte | Skills | Uso |
|---|---|---|
| **superpowers** (Anthropic) | brainstorming, writing-plans, executing-plans, systematic-debugging, test-driven-development, requesting/receiving-code-review, verification-before-completion, finishing-a-development-branch, dispatching-parallel-agents, subagent-driven-development, using-git-worktrees | Automáticas — processo de dev disciplinado |
| **code-review** (Anthropic) | `code-review:code-review` | Review de PR/diff, `--comment` posta inline, `--fix` aplica |
| **frontend-design** (Anthropic) | `frontend-design:frontend-design` | Direção visual/estética |
| **skill-creator** (Anthropic) | criar/testar/otimizar skills novas | Meta — criar skill nova |
| **code-simplifier** (Anthropic, agente) | simplifica código recém-modificado | Automático pós-edit |
| **mattpocock-skills** (25 skills) | diagnosing-bugs, tdd, code-review, codebase-design, improve-codebase-architecture, implement, to-spec, to-tickets, triage, wayfinder, teach, domain-modeling, prototype, research, resolving-merge-conflicts, grilling, grill-me, handoff, wizard, writing-for-agents, to-questionnaire, wait-what, ask-matt, grill-with-docs, setup | Pack de engenharia ativamente mantido (Matt Pocock). Prefira sobre skills custom de debugging/review/spec/arquitetura |
| **caveman** (marketplace) | modo de compressão de output | Ver bloco `tools--caveman-*` abaixo — versão pasta local |
| **genjutsu** | `cast` (micro-interação), `paint` (design system) | Motion/UI web |
| **gsap-skills** | gsap-core/frameworks/performance/plugins/react/scrolltrigger/timeline/utils | Animação GSAP |
| **claude-code-setup** (Anthropic) | `claude-automation-recommender` | Meta — recomenda hooks/skills/MCP pro codebase atual |
| **claude-md-management** (Anthropic, 2026-09-15) | audita/mantém `CLAUDE.md` | Repo não tinha `CLAUDE.md` — usar pra criar/manter um |
| **claude-security** (Anthropic, 2026-09-15) | scan de vulnerabilidade com effort tiers + challenge de findings | Prefira sobre skill custom de auditoria — usar junto com `dev--security-reviewer` (este cobre revisão de código geral; `claude-security` é scan dedicado) |
| **hookify** (Anthropic, 2026-09-15) | cria hooks a partir de padrões de conversa | Usar pra automatizar `tools--skill-lint` como PostToolUse, sem editar `settings.json` na mão |
| **commit-commands** (Anthropic, 2026-09-15) | comandos de commit/push/PR | Complementa `tools--caveman-commit` (aquele comprime a mensagem, este agiliza o fluxo) |
| **playwright** (Anthropic, 2026-09-15) | MCP oficial de browser automation | Overlap parcial com `composio--testing` (mecanismo diferente — MCP vs skill); prefira playwright pra e2e real, composio--testing pra teste local rápido |

---

## Skills locais (44) — por categoria

### IA & Agentes (`ai--`, 2)
| Skill | Para que serve |
|---|---|
| `ai--agno` | Framework Agno — agentes/times/workflows de produção, MCP, AgentOS |
| `ai--agent-development` | Criar/editar subagentes Claude Code (frontmatter, description, tools, triggers) |

### Arquitetura & Infra (`arch--`, 4)
| Skill | Para que serve |
|---|---|
| `arch--api-designer` | REST/GraphQL, OpenAPI specs, versionamento, paginação |
| `arch--devops-engineer` | Dockerfiles, CI/CD, Kubernetes, Terraform/Pulumi |
| `arch--monitoring-expert` | Prometheus/Grafana, logging estruturado, alertas, load testing, profiling |
| `arch--senior-architect` | Arquitetura de sistema ampla (React/Next/Node/Express/RN/Swift/Kotlin/Flutter/Postgres/GraphQL/Go/Python) |

### Integrações & Utilitários (`composio--`, 3)
| Skill | Para que serve |
|---|---|
| `composio--apps` | Conectar Claude a apps externos (Gmail, Slack, GitHub, 1000+) |
| `composio--builder` | Artifacts HTML multi-componente (React/Tailwind/shadcn) |
| `composio--testing` | Testar apps web locais com Playwright |

### Dados & Banco (`data--`, `db--`, 3)
| Skill | Para que serve |
|---|---|
| `data--pandas-pro` | DataFrames — limpeza, agregação, transformação |
| `db--postgres-pro` | Postgres avançado — EXPLAIN, JSONB, replicação, extensões |
| `db--sql-pro` | Queries lentas, schema design, troubleshooting genérico |

### Desenvolvimento (`dev--`, 4)
| Skill | Para que serve |
|---|---|
| `dev--code-refactoring` | Clean code, SOLID, refatoração incremental sem quebrar comportamento |
| `dev--python-pro` | Python 3.11+ type-safe, async, error handling |
| `dev--security-reviewer` | Vulnerabilidades + relatório de auditoria com severidade |
| `dev--test-master` | Geração de testes, mocking, coverage, test plans |

### Frontend (`frontend--`, 2)
| Skill | Para que serve |
|---|---|
| `frontend--typescript-pro` | Type systems avançados, type guards, branded types, tRPC |
| `frontend--ui-ux-expert` | React acessível com shadcn/ui + Tailwind + TanStack Query (fluxo de 6 fases) |

### Aprendizado (`learn--`, 1)
| Skill | Para que serve |
|---|---|
| `learn--project-mentor` | Entender/explicar projeto ou codebase existente (visão macro) |

### n8n (`n8n--`, 14 — uso ativo confirmado)
Protocolo completo pra workflows n8n. `using-skills` é o roteador always-on; os demais cobrem uma fase/conceito cada.

| Skill | Para que serve |
|---|---|
| `n8n--using-skills` | Roteador always-on, carregado no SessionStart |
| `n8n--workflow-lifecycle` | Design → organização → finalização de um workflow |
| `n8n--agents` | AI Agents, Text Classifier, Information Extractor, LLM Chain |
| `n8n--node-configuration` | Configurar qualquer node (HTTP, webhook, DB, comms, triggers, Merge) |
| `n8n--expressions` | Sintaxe `{{...}}`, `$json`/`$node`, Luxon dates |
| `n8n--code-nodes` | Code node — JS/Python custom logic |
| `n8n--data-tables` | Data Tables — schema, insert/update/upsert, query |
| `n8n--binary-and-data` | Arquivos, imagens, anexos, binary data |
| `n8n--loops` | Multi-item, batches, paginação, rate limits, fan-out |
| `n8n--subworkflows` | Workflows multi-step ou reutilizáveis (>10 nodes) |
| `n8n--error-handling` | Webhook/produção — evitar falha silenciosa |
| `n8n--credentials-and-security` | Auth, API keys, tokens, OAuth, secrets |
| `n8n--debugging` | Workflow quebrado / resultado inesperado |
| `n8n--extending-mcp` | Expor workflow n8n como tool MCP |

### Produto (`product--`, 2)
| Skill | Para que serve |
|---|---|
| `product--product-discovery` | Validar oportunidades, discovery sprints, problem-solution fit |
| `product--project-planner` | Planejamento não-técnico — negócios, eventos, pessoal |

### Ferramentas (`tools--`, 11)
| Skill | Para que serve |
|---|---|
| `tools--caveman` | Modo de compressão de output (~65%), 6 níveis de intensidade |
| `tools--caveman-commit` | Commit messages comprimidas, Conventional Commits |
| `tools--caveman-compress` | Comprime memory files (CLAUDE.md, todos) pra economizar tokens |
| `tools--caveman-help` | Cartão de referência dos modos/comandos caveman |
| `tools--caveman-review` | Comentários de PR comprimidos, um por linha |
| `tools--caveman-stats` | Uso real de tokens da sessão atual |
| `tools--cavecrew` | Decide quando delegar a subagentes estilo-caveman |
| `tools--context7-mcp` | Docs de libraries/frameworks via Context7 |
| `tools--graphify` | Perguntas sobre arquitetura/relações de arquivos do codebase |
| `tools--skill-lint` | Valida frontmatter de todo `SKILL.md` — pega skills quebradas (sem `description`) antes que fiquem invisíveis |
| `tools--skill-audit` | Compara skills locais entre si e contra as oficiais/marketplace instaladas, aponta duplicatas |

**Meta:** agente `.claude/agents/skill-reviewer.md` — roda antes de instalar/criar skill nova, aplica o critério dessa limpeza (154→46) automaticamente.

---

## Fluxos comuns

```
Bug                 → systematic-debugging (auto) → mattpocock:diagnosing-bugs → fix na camada certa → verification-before-completion (auto)
Feature nova         → brainstorming (auto) → mattpocock:to-spec → to-tickets → writing-plans (auto)
Review de PR         → code-review:code-review --comment (GitHub) | mattpocock:code-review (local)
Segurança pré-deploy  → dev--security-reviewer → correções manuais
Nova tela UI          → frontend-design:frontend-design → frontend--ui-ux-expert → frontend--typescript-pro
n8n workflow          → n8n--using-skills (auto) → n8n--workflow-lifecycle → skill da fase específica
Entender codebase     → learn--project-mentor | tools--graphify | mattpocock:wayfinder
```

## Referência rápida

| Preciso de... | Skill |
|---|---|
| API design | `arch--api-designer` |
| Deploy/infra | `arch--devops-engineer` |
| Observabilidade | `arch--monitoring-expert` |
| Query SQL lenta | `db--sql-pro` / `db--postgres-pro` |
| Refatorar código | `dev--code-refactoring` |
| Gerar testes | `dev--test-master` |
| Auditoria de segurança | `dev--security-reviewer` |
| Tela React acessível | `frontend--ui-ux-expert` |
| Tipos TS avançados | `frontend--typescript-pro` |
| Conectar app externo | `composio--apps` |
| Testar app web local | `composio--testing` |
| pandas/dados | `data--pandas-pro` |
| Workflow n8n | `n8n--using-skills` |
| Validar ideia de produto | `product--product-discovery` |
| Planejar projeto não-técnico | `product--project-planner` |
| Entender projeto/codebase | `learn--project-mentor` |
| Docs de lib/framework | `tools--context7-mcp` |
| Modo comprimido | `tools--caveman` |
