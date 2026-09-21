================================================================================
# CLAUDE_CODEX.md — Claude Code + Codex (plugin, mesma sessão)
================================================================================

O fluxo de trabalho onde utilizamos o Claude Code, como a ferramenta principal e podemos chamar o Codex (via pluguin) como ferramenta, na mesma sessão, sem trocar de terminal.
> Não cobre Codex standalone (terminal separado) — isso fica em `.codex/` + `AGENTS.md` - esse guia explica o uso; aquele arquivo é a instrução que eu executo. Se um mudar, o outro tem que refletir.

================================================================================
## 1. O QUE É
================================================================================

Plugin `openai-codex`. Não é uma segunda IA "dentro" de mim — é uma ponte: um script (`codex-companion.mjs`) que chama o binário real do Codex CLI e devolve o resultado pra minha sessão. Setup já feito, `/codex:setup` confirma:

Retorna `ready`, versão do `codex-cli`, status de auth, e se o stop-review-gate tá ligado (está).

================================================================================
## 2. PEÇAS DO PLUGIN
================================================================================

| Peça | Função |
|---|---|
| Comandos `/codex:*` | Interface digitável. Cada um é um arquivo de comando do plugin. |
| Subagente `codex:codex-rescue` | Forwarder puro — pega pedido, manda pro Codex via `task`, devolve saída sem interpretar. Claude pode despachar isso sozinho. |
| Skill `codex-cli-runtime` | Regra interna de como o rescue monta o comando `task`. Só usada dentro do subagente, não invoca direto. |
| Skill `codex-result-handling` | Regra de como apresentar o resultado — achado por severidade, nunca aplica fix sozinho sem perguntar. |
| Skill `gpt-5-4-prompting` | Usada internamente pra reescrever o pedido num prompt melhor antes de mandar pro Codex. |
| Hook `Stop` | Roda `stop-review-gate-hook.mjs` antes de encerrar sessão, se o gate estiver ligado. |

================================================================================
## 3. GUIA DE COMANDOS
================================================================================

Guia de uso e comandos do pluguin, quando executado em segundo plano, você pode usar:

* `/codex:status` para verificar o progresso.
* `/codex:cancel` para cancelar a tarefa em andamento.

---

### 3.1. `/codex:setup [--enable-review-gate|--disable-review-gate]`
**O quê:** confere Codex instalado/autenticado; liga ou desliga o stop-review-gate.
**Quando usar:** só precisa rodar de novo se Codex parar de autenticar, ou se quiser ligar/desligar o gate.

---

### 3.2. `/codex:review [--wait|--background] [--base <ref>] [--scope auto|working-tree|branch]`
**Disparo Manual:** comando tem `disable-model-invocation: true`, Claude não consegue rodar sozinho por nenhum caminho.

**O quê:** Executa uma revisão padrão do Codex sobre o seu trabalho atual (git state atual: working tree ou branch vs `--base`). Ela oferece a mesma qualidade de revisão de código que executar /review diretamente dentro do Codex, só acha problema, nunca corrige, nunca aplica patch.

**Quando usar:**
   * Uma revisão das suas alterações atuais ainda não commitadas.
   * Uma revisão da sua branch comparada a uma branch base, como main.

**Exemplo:** `/codex:review --scope branch --base main` — revisa a branch inteira contra `main`.

**Observação:** A revisão de código, especialmente para alterações que envolvem múltiplos arquivos, pode demorar. Em geral, recomenda-se executá-la em segundo plano.

Use `--base <ref>` para revisão de branch. Também suporta `--wait` e `--background`.

Este comando não é configurável (steerable) e não aceita texto personalizado para direcionar o foco da análise. Use `/codex:adversarial-review` quando quiser questionar uma decisão específica ou uma área de risco.

---

### 3.3. `/codex:adversarial-review [--wait|--background] [--base <ref>] [--scope ...] [foco]`
**Disparo Manual:** mesma trava do `review`.

**O quê:** Executa uma revisão direcionável (steerable) que questiona a implementação e o design escolhidos, pode ser usada para testar hipóteses, trade-offs, modos de falha e avaliar se outra abordagem teria sido mais segura ou simples.
Diferentemente de `/codex:review`, aceita texto adicional de foco após as flags.

**Quando usar:** 
  * Uma revisão antes do deploy que questione a direção adotada, não apenas os detalhes do código.
  * Uma revisão focada em decisões de design, trade-offs, premissas ocultas e abordagens alternativas.
  * Testar a robustez de áreas específicas de risco, como autenticação, perda de dados, rollback, condições de corrida (race conditions) ou confiabilidade.

**Exemplo:** `/codex:adversarial-review --scope working-tree "questione se essa transação precisa de lock explícito"`.

**Observação:** Este comando é somente leitura. Ele não corrige código.

---

### 3.4. `/codex:rescue [--background|--wait] [--resume|--fresh] [--model <modelo|spark>] [--effort <nível>] [pedido]`
**Disparo Hibrido:** este comando não tem a trava dos outros; o plugin autoriza o claude a usar de forma proativa.

**O quê:** Encaminha uma tarefa ao Codex através do subagente `codex:codex-rescue` - delega investigação, diagnóstico, ou pedido explícito de fix. Roda write-capable por padrão (edita arquivo), a menos que o prompt peça leitura explicitamente.

**Uso Claude (automático):** 
   * Claude travou num bug depois de tentar `systematic-debugging`
   * Realiza 2ª implementação independente antes de decidir caminho
   * Precisa validar um teste de verdade (modo leitura no prompt).

**Quando usar (manual):** 
   * Mandar uma investigação ou fix específico pro Codex
   * Continuar uma thread / tarefa anterior (`--resume`) ou começar do zero (`--fresh`) - se omitir `--resume` e `--fresh`, o plugin pode oferecer continuar a thread de rescue mais recente do repositório..
   * **`--effort`:** `none|minimal|low|medium|high|xhigh`.
   * **`--model spark`:** mapeia pra `gpt-5.3-codex-spark`.

**Exemplo:** `/codex:rescue --background "investigue por que o worker de admissão trava em X"`; Pode também pedir para uma tarefa ser delegada ao Codex, com linguagem natural: `"Peça ao Codex para redesenhar a conexão com o banco de dados para ser mais resiliente"`

**Observação:** Se não informado `--model` ou `--effort`, o Codex escolherá valores padrão; Se usar spark, o plugin o converte para `gpt-5.3-codex-spark`. 

Solicitações subsequentes de rescue podem continuar a tarefa mais recente do Codex no repositório.

---

### 3.5. `/codex:transfer [--source <claude-jsonl>]`
**Disparo Manual:** Claude não pode/consegue transferir, apenas usuário.

**O quê:** empacota a sessão atual do Claude Code numa thread Codex retomável — devolve `codex resume <session-id>` pra você continuar num terminal Codex separado, com o contexto desta conversa.

**Quando usar:** 
   * Levar uma investigação começada no Claude, pra uma sessão Codex standalone
   * Iniciou uma conversa de depuração ou implementação, e quer ser executado em outra sessão.

**Exemplo:** `/codex:transfer` ou `/codex:transfer --source ~/.claude/projects/-Users-me-repo/<session-id>.jsonl`

**Observação:** O hook SessionStart do plugin já fornece automaticamente o caminho da transcrição atual, a opção `--source` está disponível como substituição manual.

---

### 3.6. `/codex:status [job-id] [--all]`
**Disparo Manual:** Verificar status das tarefas Codex.

**O quê:** Mostra tarefas do Codex em execução e tarefas recentes para o repositório atual, progresso de job em background (review, adversarial-review ou rescue). Sem job-id, lista tudo da sessão.

**Quando usar:** 
   * Rodou algo com `--background` e quer saber se terminou.
   * Verificar progresso de trabalho em segundo plano.
   * Ver a tarefa concluída mais recentemente.
   * Confirmar tarefas se/ainda estão em execução

---

### 3.7. `/codex:result [job-id]`
**Disparo Manual:** Resultado final.

**O quê:** Mostra a saída final armazenada de uma tarefa concluída, resultado final guardado de job já concluído — verdict, achado, próximos passos, arquivo tocado.

**Quando usar:**
   * `/codex:status` mostrou "concluído" e você quer o payload completo.
   * `/codex:result task-abc123` quando quiser o resultado de uma tarefa especifica.

**Observação:** Quando disponível, também exibe o ID da sessão do Codex para que você possa reabri-la diretamente usando `codex resume <session-id>`

---

### 3.8. `/codex:cancel [job-id]`
**Disparo Manual:** Cancelamento.

**O quê:** Cancela uma tarefa ativa do Codex executada em segundo plano, mata job em background.

**Quando usar:** 
   * pediu revisão/rescue grande demais, mudou de ideia, ou o escopo mudou no meio.

================================================================================
## 4. AUTOMÁTICO VS MANUAL
================================================================================

| Categoria | Comandos | Regra |
|---|---|---|
| Hook, ninguém decide | Stop-review-gate | Sempre roda ao encerrar sessão. |
| Decisão Claude | `codex:rescue` (via Agent, subagente `codex:codex-rescue`) | Travei, quero 2ª opinião, ou validando teste. |
| Decisão Usuário | `review`, `adversarial-review`, `status`, `result`, `cancel`, `transfer` | `disable-model-invocation: true` — trava técnica, eu literalmente não consigo. |

================================================================================
## 5. FLUXO DE TRABALHO IDEAL
================================================================================

* **Task mecânica/simples (typo, rename, config, cache):** nada de Codex. Eu edito ou uso `cavecrew`, sem custo extra.

* **Task de julgamento normal (endpoint novo, tela, lógica sem PII/transação):** `sira-implementador` implementa, `sira-revisor` ou `cavecrew` revisa. Codex não entra — reservado pra risco.

* **Task de risco (acesso, transação, PII, migration):**
  1. `sira-implementador` entrega com evidência (comando + saída real).
  2. Eu aviso: "task de risco, roda `/codex:review` ou `/codex:adversarial-review`"; Se necessário delegar investigação, diagnóstico, ou pedido explícito de fix, usar `codex:codex-rescue` (roda — `--wait` se pequeno, `--background` se grande).
  3. Depois, acompanhar com `/codex:status`/`/codex:result`.
  4. Eu leio o achado, apresento por severidade, **paro e pergunto** o que você quer corrigido antes de tocar em qualquer arquivo.

* **Brief com critério de teste (qualquer task):** Depois que o implementador entrega comando+saída, eu despacho `codex:rescue` em modo leitura pra rodar o mesmo comando de verdade e confirmar — você não precisa fazer nada, só vê o resultado antes de eu fechar a task.

* **Claude travou num bug, ou quer 2ª opinião antes de decidir caminho:** despacha `codex:rescue` (foreground se parecer rápido, `--background` se parecer longo). Avisa e devolvo a saída do Codex verbatim, sem reescrever.

* **Quer revisão de branch inteira antes de abrir PR, fora do fluxo automático de task:** roda `/codex:review --scope branch --base main` (ou `adversarial-review` se quiser desafiar decisão de design) quando achar que vale.

* **Fim de sessão:** Stop-review-gate roda sozinho, sem ação sua. Isso NÃO substitui a revisão de risco do passo acima — é a rede de segurança final, não a revisão principal.

* **Movendo o trabalho para Codex:** Tarefas delegadas e execuções do stop gate também podem ser retomadas diretamente dentro do Codex usando `codex resume`, podedo informar explicitamente o ID da sessão obtido por `/codex:result` ou `/codex:status`

================================================================================
## 6. BOAS PRÁTICAS
================================================================================

- **Prompt pro Codex é autocontido.** Ele não vê o raciocínio de sessão do Claude — só git state + o texto que o Claude (ou você) mandar. Pedido vago = Codex reexplora do zero, gasta tempo e custo à toa.
- **Nunca aceite fix automático de review.** Achado de `/codex:review`/`/codex:adversarial-review` para na apresentação — você (ou eu, depois que você aprovar) decide o que corrigir. Isso é regra do próprio plugin (`codex-result-handling`), não vale pular.
- **Não mande Codex pra task que `cavecrew`/`sira-revisor` já resolve.** Diff mecânico trivial não precisa de revisor independente — é exatamente a duplicação que este fluxo existe pra evitar.
- **`--resume` só quando é continuação de verdade.** Caso contrário `--fresh` — herdar contexto errado do Codex confunde mais do que ajuda.
- **Background por padrão pra qualquer coisa maior que 1-2 arquivo.** Não trava a sessão, e review grande em foreground é a forma mais comum de perder tempo esperando à toa.

================================================================================
## 7. REFERÊNCIAS
================================================================================

> Regras arquiteturais do projeto (o que Codex/Claude não podem violar mesmo revisando ou corrigindo): `CLAUDE.md` e `AGENTS.md`.
