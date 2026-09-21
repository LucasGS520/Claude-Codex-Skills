# Fluxo de Trabalho: Claude Code + Codex

> Guia de referência pessoal — documento humano, não é uma skill (igual `SKILLS_GUIDE.md`). Descreve como Claude Code e Codex trabalham juntos no seu dia a dia. A versão que o Claude Code lê automaticamente é a skill [`tools--codex-workflow`](.claude/skills/tools--codex-workflow/SKILL.md); este arquivo é a versão completa, pra você consultar quando o fluxo parecer confuso.

## Princípio central

> **Claude Code coordena o trabalho e mantém o fluxo principal. Codex atua como revisor independente, executor secundário e responsável por validar testes.**

Você não divide cada tarefa igualmente entre os dois — isso gera duplicação, conflito e perda de contexto. Cada ferramenta tem uma função clara:

- **Claude Code** entende o pedido, planeja, explora o repositório, implementa e decide.
- **Codex** revisa de forma independente, questiona decisões arquiteturais quando acionado, roda e valida testes, e corrige tarefas pequenas e bem delimitadas.
- **Você** aprova o plano e a decisão final — nenhum dos dois decide por conta própria em pontos críticos.

Codex é sempre acionado manualmente. Não existe hook automático, não existe review-gate rodando sem você pedir.

---

## 1. Divisão de responsabilidades

| Responsabilidade | Claude Code | Codex |
|---|---:|---:|
| Entender o pedido do usuário | Principal | Secundário |
| Planejar a solução | Principal | Pode questionar |
| Explorar o repositório | Principal | Revisor independente |
| Implementação principal | Principal | Secundário |
| Revisão de código | Pode fazer | **Principal** |
| Revisão adversarial de arquitetura | Opcional | **Principal** |
| Execução dos testes | Pode executar | **Principal** |
| Diagnóstico de falhas | Principal | **Principal em segunda opinião** |
| Correções pontuais | Principal | Pode executar |
| Decisão final | **Claude Code / você** | Recomendação |
| Commit e organização do trabalho | Principal | Pode sugerir, mas não assume automaticamente |

---

## 2. O fluxo, fase por fase

### Fase 1 — Planejamento no Claude Code

Você começa normalmente no Claude Code. Ele deve:

1. entender o pedido;
2. investigar a estrutura do repositório;
3. identificar arquivos afetados;
4. verificar convenções existentes;
5. propor um plano;
6. levantar dúvidas importantes antes de codificar.

Codex não entra nessa fase.

### Fase 2 — Implementação incremental no Claude Code

Depois de aprovar o plano, implemente uma parte por vez — evite pedir uma implementação grande de uma vez só. Exemplo de sequência:

1. modelo ou estrutura de dados;
2. serviço de domínio;
3. endpoint;
4. integração;
5. testes;
6. documentação.

Incrementos pequenos facilitam a revisão do Codex depois.

### Fase 3 — Revisão normal pelo Codex

Depois de um bloco lógico de mudanças:

```bash
/codex:review --background
/codex:status
/codex:result
```

Use pra revisar: alterações não commitadas, bugs, erros de tratamento, testes ausentes, riscos de regressão, problemas de segurança evidentes.

**Chame o Codex quando:**
- terminar uma funcionalidade importante;
- estiver prestes a abrir um Pull Request;
- terminar uma refatoração grande;
- a implementação "parece correta" mas você quer uma segunda opinião.

### Fase 4 — Revisão adversarial em decisões importantes

```bash
/codex:adversarial-review --background
```

Use quando quiser **questionar a solução**, não só caçar erro de sintaxe. Exemplos:

```bash
/codex:adversarial-review --background questione a estratégia de cache, especialmente invalidação, concorrência e consistência
```

```bash
/codex:adversarial-review --background procure riscos de segurança, perda de dados e problemas de rollback
```

```bash
/codex:adversarial-review --base main --background avalie se esta arquitetura é adequada para produção e proponha alternativas caso necessário
```

Use principalmente pra: autenticação/autorização, pagamentos, migrações de banco, concorrência, filas, cache, uploads, exclusão de dados, mudanças de infraestrutura, alterações de API pública, e qualquer decisão difícil de reverter.

### Fase 5 — Claude Code interpreta e decide

Depois da revisão do Codex, **não peça pra aplicar tudo automaticamente**. Peça ao Claude Code:

```text
Leia o resultado da revisão do Codex.
Classifique cada ponto como:
1. bug real;
2. risco aceitável;
3. falso positivo;
4. melhoria futura.
Depois proponha quais correções devem ser aplicadas.
```

A decisão final considera: regras de negócio, compatibilidade, custo de manutenção, impacto operacional, prioridade da tarefa, e contexto que talvez não tenha sido transmitido perfeitamente ao Codex.

### Fase 6 — Codex como executor secundário

Use `/codex:rescue` só pra tarefa pequena e delimitada.

Investigação (sem alterar nada):

```bash
/codex:rescue --background investigue por que os testes de autenticação estão falhando. Não faça alterações; identifique a causa raiz e indique os arquivos envolvidos.
```

Correção controlada, depois de aprovar a proposta:

```bash
/codex:rescue --resume aplique a solução aprovada e execute os testes
```

> **Regra:** Codex corrige tarefas pequenas e bem delimitadas. Claude Code continua responsável por integrar mudanças maiores.

Pra tarefas complexas, sempre investigue antes de aplicar — nunca peça `/codex:rescue` pra investigar e corrigir de uma vez quando o problema não é trivial.

---

## 3. Codex como validador de testes

Ao rodar/validar teste, Codex deve retornar:

- comando executado;
- testes aprovados;
- testes falhos;
- causa provável;
- arquivos alterados;
- limitações ou testes que não puderam ser executados.

---

## 4. Regras operacionais (pra evitar conflito)

1. **Um agente escreve por vez.** Não deixe Claude Code editar enquanto um `/codex:rescue` com permissão de escrita ainda está rodando.
2. **Revisão antes de correção.** `revisar → classificar → decidir → corrigir`, nunca `revisar → aplicar tudo automaticamente`.
3. **Codex recebe tarefa delimitada.** Evite "melhore o projeto inteiro". Prefira algo como "corrija a falha de timeout no cliente HTTP, sem alterar a API pública e sem modificar arquivos fora de `src/http` e `tests/http`".
4. **Sempre verifique o diff** depois que o Codex alterar algo, mesmo que ele diga que só tocou um arquivo:
   ```bash
   git status --short
   git diff --stat
   git diff
   ```
5. **Não misture objetivos.** Não peça pra corrigir teste, refatorar arquitetura e atualizar documentação na mesma tarefa, salvo necessidade real.
6. **A decisão final é sua** (via Claude Code). Codex recomenda, revisa, corrige — não consolida, não decide escopo, não commita por conta própria.

---

## 5. Configuração de modelo e esforço

- Modelo mais rápido pra diagnóstico simples.
- Modelo mais capaz + esforço alto pra arquitetura e segurança.
- Execução em `--background` pra alterações grandes, pra não bloquear o Claude Code enquanto o Codex trabalha.

---

## 6. Ciclo diário resumido

```text
1. Você descreve a tarefa
2. Claude Code analisa e planeja
3. Claude Code implementa um incremento
4. Claude Code executa testes básicos
5. Codex faz revisão normal          → /codex:review --background
6. Claude Code avalia os achados      → classifica cada ponto
7. Codex executa/valida testes
8. Claude Code aplica ajustes necessários
9. Codex faz revisão final/adversarial (mudanças críticas)
10. Claude Code organiza o resultado final
```

Pra mudança crítica, o ciclo curto é:

```text
Claude planeja → Codex questiona a arquitetura → Claude implementa
→ Codex testa → Claude corrige → Codex revisa novamente
```

---

## 7. Referência rápida de comandos

| Comando | Uso |
|---|---|
| `/codex:review --background` | Revisão normal de diff não commitado |
| `/codex:status` | Consulta progresso de uma revisão/tarefa em background |
| `/codex:result` | Lê o resultado final |
| `/codex:adversarial-review --background <pergunta>` | Questiona a solução/arquitetura, não só sintaxe |
| `/codex:rescue --background <instrução>` | Investigação ou correção delimitada |
| `/codex:rescue --resume <instrução>` | Continua/aplica depois de aprovar uma proposta |
| `/codex:transfer` | Cria thread persistente no Codex a partir da sessão atual (uso raro nesse fluxo — ver §8) |
| `/codex:cancel` | Cancela tarefa em background |
| `/codex:setup` | Configura/reconfigura o plugin e o binário `codex` local |

---

## 8. O que fica de fora, de propósito

- **Sem hook automático.** Nada de `Stop` hook, nada de `--enable-review-gate`. Toda chamada ao Codex é manual, iniciada por você.
- **Sem skills portadas pro Codex.** Suas skills continuam formato Claude Code (`SKILL.md`, em `~/.claude/skills/`). Codex tem o próprio mecanismo (`AGENTS.md`, `~/.agents/skills/`) e não lê essa pasta — a integração é só via plugin/slash commands, não duplicação de conteúdo.
- **Sem `/codex:transfer` como padrão.** Esse comando cria uma thread persistente no Codex fora da sessão do Claude Code — útil se um dia você quiser Codex trabalhando em paralelo por conta própria, mas não faz parte do ciclo diário acima (que é sempre `review` → classificar → `rescue` delimitado).
- **Sem scaffolding automático de `AGENTS.md`/`CLAUDE.md`.** Se algum dia você tiver um projeto de código real (não este repo de skills) e quiser que Claude Code e Codex compartilhem um contrato de instruções (stack, comandos de build/test/lint, convenções, diretórios protegidos), isso é uma tarefa separada, decidida caso a caso — não uma feature automática deste repo.

---

## 9. Onde isso vive no seu setup

- Plugin instalado via `plugins.json` (marketplace `openai-codex`, plugin `codex@openai-codex`) — ver [SKILLS_GUIDE.md](SKILLS_GUIDE.md).
- Skill que o Claude Code carrega automaticamente: [`tools--codex-workflow`](.claude/skills/tools--codex-workflow/SKILL.md) — versão condensada deste guia, pra ativação automática por trigger phrase.
- Setup do Codex CLI em si (`npm install -g @openai/codex`, `codex login`) é manual/interativo, feito por você fora deste repo — não é scriptado no `install.sh`.
