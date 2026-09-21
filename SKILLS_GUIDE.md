# Guia de Skills Globais

> Arquivo de referência pessoal — **não é uma skill**, não interfere no Claude Code.
> Local: `~/.claude/SKILLS_GUIDE.md` · Pastas: `ls ~/.claude/skills/`

---

## Como funciona

**Ativação automática:** Claude Code lê o `description` do `SKILL.md` e ativa sozinho quando a situação encaixa (é por isso que boas descriptions importam — elas são o "gatilho" que o modelo lê antes de decidir usar a skill).
**Ativação manual:** pedido natural ("usa a skill de X"), referência direta, ou slash command (`/nome-da-skill`).

**Dois mecanismos:**
| | Skills-pasta (`.claude/skills/`) | Plugin marketplace |
|---|---|---|
| Como carrega | Claude Code varre `SKILL.md` direto | `/plugin` — cache em `~/.claude/plugins/cache/` |
| Update | manual (reinstala) | `claude plugin update` |
| Usa aqui | as 46 abaixo | superpowers, mattpocock-skills, code-review, frontend-design, code-simplifier, claude-md-management, claude-security, hookify, commit-commands, caveman |

---

## Skills oficiais / plugins (mantidas sempre — não editar)

Prefira estas antes de qualquer skill custom equivalente. Ficam em `~/.claude/plugins/cache/`, atualizadas pelo sistema.

| Fonte | Skills | O que faz |
|---|---|---|
| **superpowers** (Anthropic) | brainstorming, writing-plans, executing-plans, systematic-debugging, test-driven-development, requesting/receiving-code-review, verification-before-completion, finishing-a-development-branch, dispatching-parallel-agents, subagent-driven-development, using-git-worktrees | Pacote de processo de desenvolvimento disciplinado, always-on. `brainstorming` explora intenção antes de qualquer feature nova; `systematic-debugging` investiga causa raiz antes de propor fix; `writing-plans`/`executing-plans` transformam spec em plano executável e o executam; `test-driven-development` força red-green-refactor; `verification-before-completion` checa antes de declarar tarefa pronta; `using-git-worktrees` isola trabalho em branch própria |
| **code-review** (Anthropic) | `code-review:code-review` | Revisa o diff atual, PR ou branch por bugs de correção e oportunidades de simplificação. `--comment` posta os achados como comentários inline no PR; `--fix` aplica as correções direto na árvore de trabalho; `ultra` dispara review multi-agente na nuvem |
| **frontend-design** (Anthropic) | `frontend-design:frontend-design` | Direção visual e estética para telas/componentes novos — decide layout, hierarquia visual e estilo antes da implementação |
| **code-simplifier** (Anthropic, agente) | simplifica código recém-modificado | Roda automaticamente após edições — revisa por reuso, clareza e redundância sem mudar comportamento |
| **mattpocock-skills** (25 skills) | diagnosing-bugs, tdd, code-review, codebase-design, improve-codebase-architecture, implement, to-spec, to-tickets, triage, wayfinder, teach, domain-modeling, prototype, research, resolving-merge-conflicts, grilling, grill-me, handoff, wizard, writing-for-agents, to-questionnaire, wait-what, ask-matt, grill-with-docs, setup | Pacote de engenharia ativamente mantido (Matt Pocock). Cobre do fim ao fim: `to-spec`/`to-tickets` convertem ideia em spec e tickets, `domain-modeling`/`codebase-design` desenham a estrutura, `prototype`/`implement` constroem, `diagnosing-bugs` investiga falhas, `resolving-merge-conflicts` resolve conflitos, `grilling`/`grill-me` questionam premissas antes de aceitar um plano. Prefira sobre skills custom equivalentes de debugging/review/spec/arquitetura |
| **caveman** (marketplace) | modo de compressão de output | Ver bloco `tools--caveman-*` abaixo — versão pasta local faz o mesmo, mantida em paralelo |
| **claude-md-management** (Anthropic, 2026-09-15) | audita/mantém `CLAUDE.md` | Cria ou atualiza o `CLAUDE.md` do repo com os aprendizados da sessão — repo não tinha um antes disso |
| **claude-security** (Anthropic, 2026-09-15) | scan de vulnerabilidade com effort tiers + challenge de findings | Orquestra scan de segurança multi-agente ponta a ponta (inventário → pesquisa → verificação → patch). Prefira sobre skill custom de auditoria — usar junto com `dev--security-reviewer` (este cobre revisão de código geral pontual; `claude-security` é o scan dedicado e mais profundo) |
| **hookify** (Anthropic, 2026-09-15) | cria hooks a partir de padrões de conversa | Analisa a conversa em busca de comportamentos repetidos e gera hooks (PostToolUse, etc.) pra automatizar sem editar `settings.json` na mão — ex.: rodar `meta--skill-lint` sozinho após cada edição de skill |
| **commit-commands** (Anthropic, 2026-09-15) | comandos de commit/push/PR | Agiliza o fluxo git (commit → push → PR). Complementa `tools--caveman-commit` (aquele comprime a mensagem, este cuida do fluxo) |
| **playwright** (Anthropic, 2026-09-15) | MCP oficial de browser automation | Controla navegador real via protocolo MCP (não skill). Overlap parcial com `composio--testing`: prefira playwright pra e2e real e automação de browser, `composio--testing` pra checagem rápida de app local |
| **codex-plugin-cc** (openai-codex) | `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`, `/codex:transfer`, `/codex:status`, `/codex:result`, `/codex:setup` | Claude Code → Codex CLI local, uso 100% manual (sem hook automático). Codex atua como revisor independente, revisor adversarial (arquitetura/segurança) e validador/executor de teste em tarefas delimitadas — nunca implementação livre nem decisão final. Ver `tools--codex-workflow` pro playbook completo |

---

## Skills locais (46) — por categoria

### IA & Agentes (`ai--`, 2)
| Skill | O que faz |
|---|---|
| `ai--agno` | Ensina a construir com o framework Agno: agentes de produção, times multi-agente, workflows e integrações MCP, e como fazer deploy via AgentOS |
| `ai--agent-development` | Guia pra criar ou editar subagentes do Claude Code — estrutura do frontmatter, como escrever a `description` que dispara o agente certo, quais `tools` conceder, exemplos de triggering |

### Arquitetura & Infra (`arch--`, 4)
| Skill | O que faz |
|---|---|
| `arch--api-designer` | Desenha APIs REST ou GraphQL: modelagem de recursos, especificação OpenAPI, estratégias de versionamento, paginação e padrões de tratamento de erro |
| `arch--devops-engineer` | Gera Dockerfiles, pipelines de CI/CD, manifests Kubernetes e templates Terraform/Pulumi. Cobre também automação de deploy, GitOps e runbooks de resposta a incidente |
| `arch--monitoring-expert` | Configura observabilidade: dashboards Prometheus/Grafana, logging estruturado, regras de alerta, tracing distribuído, load testing (k6/Artillery) e profiling de CPU/memória |
| `arch--senior-architect` | Arquitetura de sistema de ponta a ponta (React/Next/Node/Express/React Native/Swift/Kotlin/Flutter/Postgres/GraphQL/Go/Python) — gera diagramas, aplica padrões de design de sistema e avalia trade-offs de stack |

### Integrações & Utilitários (`composio--`, 3)
| Skill | O que faz |
|---|---|
| `composio--apps` | Conecta Claude a apps externos (Gmail, Slack, GitHub e outros) pra enviar email, abrir issue, postar mensagem ou executar ações reais fora do Claude Code |
| `composio--builder` | Constrói artifacts HTML multi-componente complexos usando React, Tailwind CSS e shadcn/ui — pra quando o artifact precisa de state management ou roteamento, não só um arquivo único |
| `composio--testing` | Testa aplicações web locais via Playwright: verifica comportamento de frontend, tira screenshot, lê console/logs do browser |

### Dados & Banco (`data--`, `db--`, 3)
| Skill | O que faz |
|---|---|
| `data--pandas-pro` | Operações de DataFrame pandas: limpeza de dados, merge/join com múltiplas chaves, pivot table, resample de série temporal, groupby, tratamento de NaN |
| `db--postgres-pro` | Postgres avançado: leitura de `EXPLAIN ANALYZE`, operações JSONB, extensões (PostGIS, pgvector), tuning de VACUUM, replicação streaming/lógica |
| `db--sql-pro` | Diagnostica query lenta, desenha ou migra schema, escreve joins/window functions/CTEs complexas, interpreta plano de execução — genérico entre PostgreSQL/MySQL/SQL Server/Oracle |

### Desenvolvimento (`dev--`, 4)
| Skill | O que faz |
|---|---|
| `dev--code-refactoring` | Refatora código aplicando clean code e princípios SOLID, sem alterar comportamento observável |
| `dev--python-pro` | Python 3.11+ com tipagem estrita: type hints, async/await, dataclasses, injeção de dependência, configura mypy strict e valida com black/ruff |
| `dev--security-reviewer` | Audita vulnerabilidades de código e infraestrutura, gera relatório estruturado com severidade e recomendação de correção. Cobre SAST, secrets scanning, auditoria de dependências e compliance |
| `dev--test-master` | Gera testes (unit/integration/E2E), estratégias de mock, analisa cobertura, monta test plans e relatórios de defeito. Cobre também performance testing e testes de segurança OWASP |

### Frontend (`frontend--`, 2)
| Skill | O que faz |
|---|---|
| `frontend--typescript-pro` | Type systems avançados: generics, conditional/mapped types, type guards custom, branded types, discriminated unions e tRPC pra type-safety end-to-end |
| `frontend--ui-ux-expert` | Implementa UI React acessível com shadcn/ui + Tailwind + TanStack Query, em fluxo de 6 fases com validação WCAG 2.1 AA e checagem visual no Chrome DevTools |

### Aprendizado (`learn--`, 1)
| Skill | O que faz |
|---|---|
| `learn--project-mentor` | Explica um projeto ou repositório existente de fora pra dentro — mapeia estrutura, decisões de arquitetura e fluxo principal, inclusive cruzando código com paper acadêmico quando fornecido |

### n8n (`n8n--`)
Protocolo completo pra workflows n8n. `using-skills` é o roteador always-on carregado no SessionStart; os demais cobrem uma fase ou conceito específico cada.

| Skill | O que faz |
|---|---|
| `n8n--using-skills` | Roteador always-on: identifica qual skill n8n usar pra cada situação e resume as ferramentas MCP disponíveis |
| `n8n--workflow-lifecycle` | Cobre o ciclo completo de um workflow: design, sticky notes, nomes de node, validação, teste, organização em pastas/projetos e publicação |
| `n8n--agents` | AI Agents, Text Classifier, Information Extractor, Sentiment Analysis, Summarization/LLM Chain e geração de mídia via nodes LangChain nativos do n8n |
| `n8n--node-configuration` | Configura qualquer node (HTTP, webhook, banco, Slack/Gmail/Discord, IA, triggers, Merge) — inclusive parâmetros específicos como fan-in e `numberOfInputs` |
| `n8n--expressions` | Sintaxe `{{...}}`, referências `$json`/`$node`/`$input`, manipulação de data com Luxon, debug de erro de expressão |
| `n8n--code-nodes` | Escreve lógica custom em JavaScript/Python dentro do Code node quando um node nativo não resolve |
| `n8n--data-tables` | Data Tables nativas do n8n: design de schema, insert/update/upsert, dedup, idempotência e query |
| `n8n--binary-and-data` | Lida com arquivo, imagem, anexo e dado binário — inclusive quando um AI agent precisa receber ou devolver um arquivo |
| `n8n--loops` | Processamento multi-item: batch, paginação de API, rate limit, fan-out entre branches paralelas |
| `n8n--subworkflows` | Extrai lógica repetida em subworkflow reutilizável — pra workflows com mais de ~10 nodes ou lógica compartilhada |
| `n8n--error-handling` | Evita falha silenciosa em workflow de webhook/produção — branch de erro por node, `continueErrorOutput`, retorno de status |
| `n8n--credentials-and-security` | Trata autenticação: API keys, tokens, OAuth, bearer/basic auth e onde guardar segredo com segurança |
| `n8n--debugging` | Investiga workflow quebrado ou resultado inesperado — ponto de entrada pra qualquer "não está funcionando" |
| `n8n--extending-mcp` | Expõe um workflow n8n como tool MCP chamável pelo agente — tanto pra cobrir gap da API do n8n quanto pra virar tool de propósito geral |

### Produto (`product--`, 2)
| Skill | O que faz |
|---|---|
| `product--product-discovery` | Valida oportunidade de produto antes de construir: mapeia hipóteses, planeja sprint de discovery, testa problem-solution fit |
| `product--project-planner` | Planejamento não-técnico de qualquer domínio (negócio, evento, pessoal, acadêmico): metas, milestones, timeline, alocação de recurso, avaliação de risco |

### Ferramentas (`tools--`, 9)
| Skill | O que faz |
|---|---|
| `tools--caveman` | Ativa o modo de compressão de output (~65% menos tokens medido), com 6 níveis de intensidade (lite/full/ultra/wenyan-*) mantendo exatidão técnica |
| `tools--caveman-commit` | Gera mensagem de commit comprimida em Conventional Commits — assunto ≤50 char, corpo só quando o "porquê" não é óbvio |
| `tools--caveman-compress` | Comprime arquivo de memória em linguagem natural (CLAUDE.md, todos, preferências) pra formato caveman, economizando tokens de input; guarda backup legível em `.original.md` |
| `tools--caveman-help` | Cartão de referência rápida de todos os modos, skills e comandos caveman disponíveis |
| `tools--caveman-review` | Gera comentário de PR comprimido: uma linha por achado, local + problema + fix, sem elogio nem scope creep |
| `tools--caveman-stats` | Mostra uso real de token da sessão atual, lido direto do log de sessão (sem estimativa do modelo) |
| `tools--cavecrew` | Decide quando vale delegar a um subagente estilo-caveman em vez de fazer inline: `cavecrew-investigator` pra localizar código, `cavecrew-builder` pra edição de 1-2 arquivos, `cavecrew-reviewer` pra revisar diff — reduz ~60% do tamanho do resultado injetado de volta no contexto principal |
| `tools--codex-workflow` | Playbook de delegação Claude Code ↔ Codex: tabela de responsabilidade, fluxo de 7 passos (planejar → implementar incremental → `/codex:review` → `/codex:adversarial-review` em mudança de risco → classificar achado antes de aplicar → `/codex:rescue` delimitado → validar teste) e 6 regras operacionais (um agente escreve por vez, revisar antes de corrigir, tarefa delimitada, checar diff sempre, não misturar objetivo, decisão final é sua) |
| `tools--context7-mcp` | Busca documentação atualizada de biblioteca/framework (React, Vue, Next.js, Prisma, Supabase etc.) via Context7, evitando resposta desatualizada de memória |
| `tools--graphify` | Transforma qualquer entrada (código, docs, papers, imagem, vídeo) num knowledge graph persistente com detecção de comunidade e ferramentas de query/path/explain — trata perguntas sobre arquitetura do codebase como query nesse grafo |

### Meta — skills sobre skills (`meta--`, 2)
| Skill | O que faz |
|---|---|
| `meta--skill-lint` | Valida o frontmatter YAML de todo `SKILL.md` do repo, confere se `description` está presente e não-vazia, e sinaliza nomes de skill duplicados — pega skill quebrada antes que fique invisível pro Claude Code |
| `meta--skill-audit` | Compara skills locais entre si e contra as oficiais/marketplace instaladas, por similaridade de palavra-chave na `description`, apontando duplicata ou sobreposição antes de adicionar skill nova |

---

## Sinergia / fluxo de trabalho

Como as skills se encadeiam na prática — cada bloco é uma cadeia real, não uma lista solta.

### Bug em produção ou teste falhando
```
systematic-debugging (superpowers)
  → mattpocock:diagnosing-bugs        — isola causa raiz
  → dev--code-refactoring             — se o fix pede limpeza estrutural
  → dev--test-master                  — cobre o caso com teste de regressão
  → verification-before-completion (superpowers)
```

### Feature nova, do zero
```
brainstorming (auto, superpowers)      — alinha intenção antes de codar
  → mattpocock:to-spec                 — vira spec 
  → arch--senior-architect             — se a feature mexe em arquitetura
  → mattpocock:to-tickets              — tickets executáveis
  → writing-plans (auto, superpowers)  — plano passo a passo
  
  → dev--python-pro | frontend--typescript-pro  — implementação tipada
  → dev--test-master                   — testes
  → executing-plans (auto, superpowers)
```

### Review de código
```
code-review:code-review --comment (GitHub, remoto)
  | mattpocock:code-review (local, sem PR)
  → code-simplifier (auto, pós-edit)   — limpa o que sobrou
  → tools--caveman-review              — se quiser o feedback comprimido, 1 linha por achado
```

### Refatoração estrutural
```
learn--project-mentor
  → tools--graphify
  → mattpocock:wayfinder

  → dev--code-refactoring
  → mattpocock:improve-codebase-architecture
  → code-simplifier                             — simplifica código recém-modificado

  → dev--test-master                            — validação
  → code-review                                 — Revisão completa, código refatorado

  → verification-before-completion              — checklist final
```

### Segurança pré-deploy
```
dev--security-reviewer                 — varredura pontual, relatório com severidade
  → claude-security (plugin)           — scan multi-agente mais profundo, se o pontual achar algo sério
  → correções manuais
  → dev--test-master                   — teste de segurança OWASP no que foi corrigido
```

### Tela de UI nova
```
frontend-design:frontend-design        — direção visual antes de codar
  → frontend--ui-ux-expert             — implementação React acessível (fluxo de 6 fases)
  → frontend--typescript-pro           — tipagem forte na camada de dados/props
  → genjutsu:paint | genjutsu:cast     — design system ou micro-interação pontual
  → gsap-skills:gsap-react             — se precisar de animação além de CSS
```



### Novo Agente de IA (agno)
```
brainstorming (auto, superpowers)      — entendimento do objetivo
  → mattpocock:to-spec                 — especificação do agente
  → ai--agno                           — definição da persona, tools e workflow
  → mattpocock:domain-modeling          — se houver memória, conhecimento ou múltiplas entidades
  → dev--python-pro                     — implementação
  → composio--apps                      — integrações necessárias
  → dev--test-master                    — validação
  → verification-before-completion      — checklist final
```

### Novo Time de Agentes de IA - (agno)
```
brainstorming                               — explora objetivo, casos de uso e limites do agente
  → product--product-discovery              — valida problema, usuário e ROI da automação
  → mattpocock:grilling                     — desafia premissas e encontra gaps cedo
  → mattpocock:to-spec                      — transforma ideia em especificação executável
  
  → ai--agno                               — define agentes, team, workflow, tools e MCPs
  → mattpocock:domain-modeling             — modela entidades, memória e contratos
  → arch--senior-architect                 — arquitetura de ponta a ponta
  → arch--api-designer                     — APIs, webhooks e contratos externos
  → mattpocock:to-tickets                  — decomposição em tickets
  → writing-plans (auto, superpowers)      — plano de execução detalhado
  → dev--python-pro                        — implementação dos agentes e workflows
  → db--postgres-pro                       — memória persistente, pgvector e banco
  → composio--apps                         — integrações externas
  
  → dev--test-master                       — testes unitários, integração e avaliação
  → composio--testing | playwright         — validação de fluxos completos
  → arch--monitoring-expert                — observabilidade, tracing e métricas

  → dev--security-reviewer                 — revisão de segurança
  → claude-security                        — auditoria profunda multi-agente

  → verification-before-completion        — validação final
  → code-review:code-review               — revisão final do código
```

### Workflows (n8n)
```
n8n--using-skills (auto, SessionStart)
  → n8n--workflow-lifecycle            — design → organização → publicação
  → skill da fase específica (agents / node-configuration / expressions / code-nodes /
     data-tables / binary-and-data / loops / subworkflows / error-handling /
     credentials-and-security / extending-mcp)
  → n8n--debugging                     — se algo quebrar no meio do processo
```

### Workflows Multi-Agente (n8n + agno)
```
brainstorming (superpowers)                 — explora objetivo, casos de uso e limites do agente
  → product--product-discovery              — valida problema, usuário e ROI da automação
  → mattpocock:grilling                     — desafia premissas e encontra gaps cedo
  → mattpocock:to-spec                      — transforma ideia em especificação executável

  → ai--agno                               — define agentes, team, workflow, tools e MCPs
  → mattpocock:domain-modeling             — modela entidades, memória e contratos
  → arch--senior-architect                 — arquitetura de ponta a ponta
  → arch--api-designer                     — APIs, webhooks e contratos externos

  → mattpocock:to-tickets                  — decomposição em tickets
  → writing-plans (auto, superpowers)      — plano de execução detalhado

  → dev--python-pro                        — implementação dos agentes e workflows
  → db--postgres-pro                       — memória persistente, pgvector e banco
  → composio--apps                         — integrações externas
  → n8n--workflow-lifecycle                — ciclo de vida do workflow
  → n8n--subworkflows                      — se necessário desenho de subworkflows
  → n8n--extending-mcp                     — criação de ferramentas MCP via n8n

  → dev--test-master                       — testes unitários, integração e avaliação
  → composio--testing | playwright         — validação de fluxos completos
  → arch--monitoring-expert                — observabilidade, tracing e métricas

  → dev--security-reviewer                 — revisão de segurança
  → claude-security                        — auditoria profunda multi-agente

  → verification-before-completion        — validação final
  → code-review:code-review               — revisão final do código
  → executing-plans (superpowers)
```

### API + banco de dados
```
arch--api-designer                     — modela recursos e contrato OpenAPI
  → db--sql-pro | db--postgres-pro     — desenha schema por trás do contrato
  → arch--devops-engineer              — containeriza e sobe pipeline de deploy
  → arch--monitoring-expert            — observabilidade e alerta no serviço no ar
```

### Deploy e infraestrutura
```
arch--devops-engineer                  — Dockerfile, CI/CD, Kubernetes, Terraform
  → dev--security-reviewer             — auditoria antes da infra validada
  → arch--monitoring-expert            — dashboards, alertas, tracing no que subiu
  → dev--security-reviewer             — auditoria para validação pós infra, antes de ir pra produção
  → commit-commands (plugin)           — commit/push/PR do que foi gerado
```

### Entender codebase existente
```
learn--project-mentor                  — visão macro, explica de fora pra dentro
  | tools--graphify                    — quando precisa de grafo navegável (graphify-out/)
  | mattpocock:wayfinder                — navegação pontual dentro do código
```

### Dados / análise
```
data--pandas-pro                       — limpeza, merge, agregação de DataFrame
  → dataviz (skill de visualização)    — transforma resultado em gráfico/dashboard
```

### Produto / planejamento
```
product--product-discovery             — valida hipótese antes de comprometer time
  → mattpocock:to-spec → to-tickets    — vira spec técnica e tickets
  → product--project-planner           — planeja a parte não-técnica (timeline, recurso, evento)
```

### Arquitetura de sistema
```
brainstorming
  → product--product-discovery       - se necessário descobrir e definir produto
  → mattpocock:domain-modeling
  → arch--senior-architect
  → arch--api-designer
  → mattpocock:grilling
  → mattpocock:to-spec
  → mattpocock:to-tickets
```

### Evoluir/Ajustar Arquitetura Existente
```
learn--project-mentor
  → tools--graphify
  → mattpocock:wayfinder

  → mattpocock:improve-codebase-architecture
  → arch--senior-architect

  → mattpocock:to-tickets
  → writing-plans
```

### Compressão de output (caveman)
```
tools--caveman                         — ativa modo comprimido na conversa
  → tools--caveman-commit              — comprime mensagem de commit
  → tools--caveman-review              — comprime comentário de PR
  → tools--caveman-compress            — comprime memory file (CLAUDE.md, todos)
  → tools--cavecrew                    — decide quando delegar pra subagente caveman em vez de inline
  → tools--caveman-stats               — confere economia real de token da sessão
```
