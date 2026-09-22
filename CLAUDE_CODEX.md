================================================================================
# CLAUDE_CODEX.md — Claude Code + Codex (plugin, mesma sessão)
================================================================================

O fluxo de trabalho onde utilizamos o Claude Code, como a ferramenta principal e podemos chamar o Codex (via pluguin) como ferramenta, na mesma sessão, sem trocar de terminal.
> Não cobre Codex standalone (terminal separado) — isso fica em `.codex/` + `AGENTS.md`.
> Guia explicativo sobre o uso — a política operacional que o Claude Code segue deve existir no respectivo projeto. Se não existir, necessário criar um arquivo contendo a **política de execução e regras do Claude Code**. 

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
| Subagente `/codex:codex-rescue` | Forwarder puro — pega pedido, manda pro Codex via `task`, devolve saída sem interpretar. Claude despacha diretamente (aviso + confirmação rápida) nos 3 gatilhos da seção 3.4 — ver §4. |
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

**O quê:** Executa uma revisão padrão do Codex sobre o seu trabalho atual (git state atual: working tree ou branch vs `--base`). Ela oferece a mesma qualidade de revisão de código que executar `/review` diretamente dentro do Codex, só acha problema, nunca corrige, nunca aplica patch.

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
**Disparo semi-autônomo, só nos 3 gatilhos abaixo:** Claude não só sugere — avisa em 1 linha o que vai mandar e por quê, espera uma confirmação rápida (não o comando digitado, só um sinal de "confirmação"), e despacha ele mesmo. Fora desses 3 gatilhos, volta a ser sugestão pura (comando pronto, você digita).

**O quê:** Encaminha uma tarefa ao Codex através do subagente `codex:codex-rescue` - delega investigação, diagnóstico, ou pedido explícito de fix. Roda write-capable por padrão (edita arquivo), a menos que o prompt peça leitura explicitamente.

**Quando Claude avisa e despacha (após sua confirmação rápida):**
   * Claude travou num bug depois de tentar `systematic-debugging`
   * Vale 2ª implementação independente antes de decidir caminho
   * Precisa validar um teste de verdade (modo leitura no prompt) — depois do implementador entregar comando+saída.

**Parâmetros que Claude escolhe ao despachar:**
   * `--background` se a investigação parecer grande, `--wait` se pequena
   * Continuar uma thread / tarefa anterior (`--resume`) ou começar do zero (`--fresh`) - se omitir os dois, o plugin pode oferecer continuar a thread de rescue mais recente do repositório
   * **`--effort`:** `none|minimal|low|medium|high|xhigh`, conforme o tamanho do pedido
   * **`--model spark`:** só se você pedir explicitamente (mapeia pra `gpt-5.3-codex-spark`)

**Exemplo:** `/codex:rescue --background "investigue por que o worker de admissão trava em X"`; Pode também pedir para uma tarefa ser delegada ao Codex, com linguagem natural: `"Peça ao Codex para redesenhar a conexão com o banco de dados para ser mais resiliente"`

**Observação:** Se não informado `--model` ou `--effort`, o Codex escolherá valores padrão; Se usar spark, o plugin o converte para `gpt-5.3-codex-spark`. 

Solicitações subsequentes de rescue podem continuar a tarefa mais recente do Codex no repositório.

---

### 3.5. `/codex:transfer [--source <claude-jsonl>]`
**Disparo Manual:** Claude não pode transferir, apenas usuário.

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

**Regra:** Claude executa comando de Codex quando necessário, a trava é por comando, não uma regra única pra todos. Três categorias:

| Categoria | Comandos | Regra |
|---|---|---|
| Trava técnica — só humano, sempre | `review`, `adversarial-review`, `transfer` | `disable-model-invocation: true` no próprio plugin. Nenhuma política do projeto muda isso — Claude não consegue rodar por nenhum caminho. |
| Trava de política — só humano, sempre | `setup` (com flag `--enable-review-gate`/`--disable-review-gate`), `cancel` | Tecnicamente Claude poderia, mas não roda. Ligar/desligar o gate especificamente — continua manual mesmo após a revisão desta regra. |
| Aviso + confirmação rápida, Claude despacha | `rescue`, nos 3 gatilhos da seção 3.4 | Claude avisa o que vai mandar e por quê, espera um sinal seu (não o comando digitado), despacha ele mesmo. Fora dos 3 gatilhos, volta a ser sugestão pura. |
| Leitura pura, Claude roda sem pedir | `status`, `result`, `setup` sem flag | Não mudam estado, não invocam o modelo Codex. Uso: conferir se um job em `--background` já terminou, ou responder "terminou?". Nunca em loop de polling — só quando o resultado muda a próxima ação. |

Hook `Stop`: dispara sozinho ao encerrar sessão — comportamento do plugin, não ação do Claude. Se travar (Codex indisponível/cota esgotada), Claude diagnostica e sugere o comando que resolve (ex. `/codex:setup --disable-review-gate`) — **nunca roda esse comando sozinho**, essa parte da regra antiga continua de pé.

================================================================================
## 5. FLUXO DE TRABALHO IDEAL
================================================================================

* **Task mecânica/simples (typo, rename, config, cache):** nada de Codex. Eu edito ou uso `cavecrew`, sem custo extra.

* **Task de julgamento normal (endpoint novo, tela, lógica sem PII/transação):** `sira-implementador` implementa, `sira-revisor` ou `cavecrew` revisa. Codex não entra — reservado pra risco.

* **Task de risco (acesso, transação, PII, migration):**
  1. `sira-implementador` entrega com evidência (comando + saída real).
  2. Claude avisa: "task de risco, roda `/codex:review` ou `/codex:adversarial-review`" — comando pronto, copiável (trava técnica, só disparo manual). Se for caso de investigação/diagnóstico/fix explícito, avisa o que será mandado, espera confirmação rápida, e próprio Claude despacha `codex:rescue`.
  3. Acompanha sozinho com `/codex:status`/`/codex:result` (leitura pura, sem permissão) quando precisar do resultado pra continuar.
  4. Claude le o achado, apresenta por severidade, **para e pergunta** o que você quer corrigido antes de tocar em qualquer arquivo.

* **Dentro de `subagent-driven-development` (execução por subagentes, plano com várias tasks):** Codex é a **primeira opção**, não uma alternativa — pra toda task de risco E pra revisão final de branch. Antes de despachar qualquer revisor Claude, para e da o comando Codex daquela task específica; só cai para o revisor Claude se você pedir pra pular ou Codex estiver indisponível. Isso vale **por ocorrência** — um plano com 4 tasks de risco pausa 4 vezes, não uma.

* **Brief com critério de teste (qualquer task):** Depois que o implementador entrega comando+saída, avisa e despacha `codex:rescue` em modo leitura, após sua confirmação rápida, pra confirmar de forma independente. Se você disser pra pular, segue com o que o implementador reportou.

* **Claude travou num bug, ou quer 2ª opinião antes de decidir caminho:** avisa o que será mandado, espera confirmação rápida e assim, Claude despacha `/codex:rescue` (`--wait` se parecer rápido, `--background` se parecer longo). Ler a saída do Codex e devolver verbatim, sem reescrever.

* **Revisão de branch inteira:** é o padrão da revisão final de `subagent-driven-development` agora, não só uma opção avulsa — Claude entrega o comando `/codex:review --scope branch --base <base>` sozinho nesse ponto do fluxo. Fora desse contexto, mesma coisa por sua iniciativa a qualquer momento (ou `adversarial-review` pra desafiar decisão de design) — sempre `disable-model-invocation` do lado do Claude.

* **Fim de sessão:** Stop-review-gate roda sozinho, sem ação sua — isso é o hook do plugin. Isso NÃO substitui a revisão de risco do passo acima — é a rede de segurança final, não a revisão principal. Se o gate travar (Codex indisponível/cota esgotada), avisa e sugere o comando pra desligar — nunca desliga sozinho.

* **Movendo o trabalho para Codex:** Tarefas delegadas e execuções do stop gate também podem ser retomadas diretamente dentro do Codex usando `codex resume`, podedo informar explicitamente o ID da sessão obtido por `/codex:result` ou `/codex:status`

================================================================================
## 6. EQUIVALÊNCIA DE MODELO — CLAUDE ↔ CODEX
================================================================================

Modelo do Codex CLI é o que estiver configurado no ambiente local (`.codex/config.toml`
ou variável de ambiente) — família GPT-5.x da OpenAI. Três níveis, espelhando os três
modelos que já uso pros meus próprios subagentes (`sira-claude-workflow/SKILL.md`, seção 2):

| Claude Code | Codex — `--model` | Codex — `--effort` | Papel |
|---|---|---|---|
| `haiku` | `gpt-5.6-luna` (ou `spark`) | `low` | Mecânico, barato: diff pequeno, validação de teste read-only, achado simples de confirmar |
| `sonnet` | `gpt-5.6-terra` (padrão, sem `--model`) | `medium` | Julgamento normal: `/codex:review` de task de risco comum, `codex:rescue` investigando bug |
| `opus` | `gpt-5.6-sol` | `high` (`xhigh` em achado difícil) | Mais capaz: revisão final de branch inteira, `/codex:adversarial-review` questionando design |

**Isso é exemplo de equivalência, não regra rígida.** Nem toda task de risco precisa do
tier `gpt-5.6-sol` — uso `gpt-5.6-terra` como padrão e só subo pra `gpt-5.6-sol` quando 
o achado ou o escopo pedir (mesmo critério de "modelo proporcional ao risco" que já uso 
pros meus próprios subagentes). `spark`/`luna` é o único alias de modelo confirmado rodando 
neste projeto.

Ao montar o comando `/codex:review`, `/codex:adversarial-review` ou `/codex:rescue`, use
esta tabela pra sugerir (ou, no caso do `rescue` nos 3 gatilhos da seção 3.4, montar
sozinho após sua confirmação) o `--model`/`--effort` proporcional ao tier — nunca deixar
os dois implícitos sem pensar no equivalente certo.

