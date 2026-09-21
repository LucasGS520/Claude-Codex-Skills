# Codex Workflow Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `codex-plugin-cc` plugin entry and a single playbook skill so any Claude Code session on this machine knows how to delegate to Codex CLI as a secondary reviewer/test-validator, plus document both in `SKILLS_GUIDE.md`.

**Architecture:** Three independent, additive edits — no new subsystem, no runtime code. (1) a two-line data addition to `plugins.json` (no `install.sh` code change needed — it already loops generically over the manifest); (2) one new `SKILL.md` file at `.claude/skills/tools--codex-workflow/`, same flat shape as the existing `tools--cavecrew` skill; (3) two one-line table additions in `SKILLS_GUIDE.md`. There is no application code and no existing test suite in this repo — "testing" here means the repo's own validation scripts (`meta--skill-lint`) plus JSON/format checks.

**Tech Stack:** Plain JSON (`plugins.json`), Markdown + YAML frontmatter (`SKILL.md`, `SKILLS_GUIDE.md`), Python (existing `meta--skill-lint/scripts/lint.py`, unmodified).

**Spec:** `docs/superpowers/specs/2026-09-21-codex-workflow-integration-design.md`

## Global Constraints

- Manual invocation only for Codex — no hooks, no `--enable-review-gate`, anywhere in the new skill's text.
- No `templates/` directory, no scaffolding feature, no `AGENTS.md`/`CLAUDE.md` added anywhere (explicitly cut in the spec).
- New skill is a single file, no subfolder/assets — matches `tools--cavecrew`'s shape exactly.
- New skill's frontmatter `name:` must equal its folder name: `tools--codex-workflow`.
- `plugins.json` must remain valid JSON after edit.
- `meta--skill-lint/scripts/lint.py` must report all-clean (no missing description, no name/folder mismatch, no duplicate name) after the new skill is added.

---

### Task 1: Register the `codex-plugin-cc` plugin in the manifest

**Files:**
- Modify: `plugins.json` (repo root)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: nothing later tasks depend on programmatically — Task 3's `SKILLS_GUIDE.md` row references this plugin by name (`codex@openai-codex`) as prose, not as code.

Current file (already read this session):

```json
{
  "_comment": "Manifest of plugin-marketplace skills (not folder-copied). Used by install.sh to reproduce this setup on a new machine. Folder-based skills live in .claude/skills/ and are reproduced by plain copy.",
  "marketplaces": [
    {
      "name": "caveman",
      "url": "https://github.com/JuliusBrussee/caveman.git"
    },
    {
      "name": "mattpocock",
      "url": "https://github.com/mattpocock/skills.git"
    }
  ],
  "plugins": [
    "superpowers@claude-plugins-official",
    "frontend-design@claude-plugins-official",
    "skill-creator@claude-plugins-official",
    "code-simplifier@claude-plugins-official",
    "code-review@claude-plugins-official",
    "claude-code-setup@claude-plugins-official",
    "claude-md-management@claude-plugins-official",
    "claude-security@claude-plugins-official",
    "hookify@claude-plugins-official",
    "commit-commands@claude-plugins-official",
    "playwright@claude-plugins-official",
    "caveman@caveman",
    "mattpocock-skills@mattpocock"
  ]
}
```

- [ ] **Step 1: Add the marketplace and plugin entries**

Use Edit on `plugins.json`. Add `{"name": "openai-codex", "url": "https://github.com/openai/codex-plugin-cc"}` as the third entry in `marketplaces` (after `mattpocock`), and `"codex@openai-codex"` as the last entry in `plugins` (after `"mattpocock-skills@mattpocock"`). Resulting file:

```json
{
  "_comment": "Manifest of plugin-marketplace skills (not folder-copied). Used by install.sh to reproduce this setup on a new machine. Folder-based skills live in .claude/skills/ and are reproduced by plain copy.",
  "marketplaces": [
    {
      "name": "caveman",
      "url": "https://github.com/JuliusBrussee/caveman.git"
    },
    {
      "name": "mattpocock",
      "url": "https://github.com/mattpocock/skills.git"
    },
    {
      "name": "openai-codex",
      "url": "https://github.com/openai/codex-plugin-cc"
    }
  ],
  "plugins": [
    "superpowers@claude-plugins-official",
    "frontend-design@claude-plugins-official",
    "skill-creator@claude-plugins-official",
    "code-simplifier@claude-plugins-official",
    "code-review@claude-plugins-official",
    "claude-code-setup@claude-plugins-official",
    "claude-md-management@claude-plugins-official",
    "claude-security@claude-plugins-official",
    "hookify@claude-plugins-official",
    "commit-commands@claude-plugins-official",
    "playwright@claude-plugins-official",
    "caveman@caveman",
    "mattpocock-skills@mattpocock",
    "codex@openai-codex"
  ]
}
```

- [ ] **Step 2: Verify the JSON is valid**

Run: `python -c "import json; json.load(open('plugins.json'))" && echo VALID`
Expected: `VALID` printed, no traceback.

- [ ] **Step 3: Verify `install.sh` needs no change**

Run: `grep -n "marketplaces\|plugins" install.sh`
Expected: only the generic `for mp in data.get("marketplaces", [])` / `for plugin in data.get("plugins", [])` loops shown earlier this session — confirms the script is manifest-driven and picks up the new entries with zero code change. If this grep instead shows hardcoded plugin names, stop and report back — the plan's assumption is wrong.

- [ ] **Step 4: Commit**

```bash
git add plugins.json
git commit -m "feat: register codex-plugin-cc marketplace and plugin

Adds openai/codex-plugin-cc so install.sh reproduces the Codex
integration alongside the existing Claude Code plugins.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 2: Add the `tools--codex-workflow` skill

**Files:**
- Create: `.claude/skills/tools--codex-workflow/SKILL.md`

**Interfaces:**
- Consumes: nothing from Task 1 programmatically (references the plugin's slash commands as prose, which are defined by the already-existing `codex-plugin-cc` plugin, not by this repo).
- Produces: the skill name `tools--codex-workflow` that Task 3 references in `SKILLS_GUIDE.md`.

- [ ] **Step 1: Create the skill directory and file**

Create `.claude/skills/tools--codex-workflow/SKILL.md` with exactly this content:

```markdown
---
name: tools--codex-workflow
description: >
  Playbook for delegating to Codex CLI (via the codex-plugin-cc Claude Code
  plugin) as a secondary reviewer and test validator. Claude Code stays
  primary: it plans, implements, and decides. Codex reviews diffs, runs
  adversarial review on risky changes, validates/executes tests, and takes
  small delimited fix/investigate tasks — always invoked manually, never
  automatically. Use when the user asks to review with Codex, validate
  tests via Codex, get a second opinion, run an adversarial review, or
  delegate a bounded bugfix/investigation to Codex.
---

# Codex Workflow

Claude Code coordinates. Codex is a secondary engineer: independent
reviewer, test validator, bounded executor. Never split a task evenly
between the two — each has one clear job, always triggered manually.

## Responsibility split

| Responsibility | Claude Code | Codex |
|---|---|---|
| Understand request, plan | Primary | Can question |
| Explore repo, implement | Primary | — |
| Code review | Optional | Primary |
| Adversarial review (architecture/security) | Optional | Primary |
| Run/validate tests | Optional | Primary |
| Diagnose failures | Primary | Second opinion |
| Small bounded fixes | Primary | Can execute |
| Final decision, commit | Always | Recommends only |

## Flow

1. **Plan in Claude Code.** Understand the request, explore the repo, find
   affected files, check conventions, propose a plan. No Codex yet.
2. **Implement incrementally in Claude Code.** One small unit at a time
   (model → service → endpoint → integration → tests → docs). Small
   increments make Codex's review easier later.
3. **Normal review — call manually, never automatically:**
   ```
   /codex:review --background
   /codex:status
   /codex:result
   ```
   Call after: a meaningful feature lands, before opening a PR, after a
   big refactor, or whenever a second opinion is wanted.
4. **Adversarial review for risky changes:**
   ```
   /codex:adversarial-review --background <question — e.g. "questione a
   estratégia de cache: invalidação, concorrência, consistência">
   ```
   Use for auth, payments, migrations, concurrency, queues, cache,
   uploads, data deletion, infra changes, public API changes, and any
   hard-to-reverse decision.
5. **Classify before applying anything.** Never auto-apply Codex's
   findings. Classify each one: bug real / accepted risk / false
   positive / future improvement. Decide what to fix, weighing business
   rules, compatibility, maintenance cost, and context Codex may be
   missing.
6. **Bounded execution via `/codex:rescue`:**
   ```
   /codex:rescue --background investigue <problema>. Não faça
   alterações; identifique a causa raiz e os arquivos envolvidos.
   /codex:rescue --resume aplique a solução aprovada e execute os testes
   ```
   Codex fixes small, well-delimited tasks; Claude Code integrates
   anything larger. Prefer investigate-first, apply-after-approval over a
   one-shot fix.
7. **Test validation report.** Codex should report: command run, tests
   passed, tests failed, likely cause, files changed, and anything it
   couldn't run.

## Operational rules

1. **One agent writes at a time.** Don't let Claude Code edit files while
   a Codex `rescue` with write access is still running.
2. **Review before fix.** `revisar → classificar → decidir → corrigir`,
   never auto-apply everything Codex reports.
3. **Bounded tasks only.** Give Codex explicit scope limits (e.g. "only
   src/http and tests/http, don't touch the public API"), never "improve
   the whole project."
4. **Always check the diff after Codex touches files** —
   `git status --short`, `git diff --stat`, `git diff` — even if Codex
   claims it changed only one file.
5. **Don't mix objectives.** Don't ask Codex to fix tests, refactor
   architecture, and update docs in the same task unless truly necessary.
6. **Final decision stays with Claude Code / the user.** Codex
   recommends, reviews, and fixes — it doesn't decide scope or merge.

## Model/effort guidance

Fast model for simple diagnostics. More capable model plus higher
reasoning effort for architecture or security-critical reviews.
Background execution (`--background`) for large changes.

## Trigger phrases

"revisa com Codex", "valida com Codex", "segunda opinião", "review
adversarial", "usa Codex pra investigar/corrigir X", or wrapping up a
significant feature before commit/PR.
```

- [ ] **Step 2: Run the skill linter**

Run: `python .claude/skills/meta--skill-lint/scripts/lint.py`
Expected: `skill-lint: 47 skills OK` (46 existing + this new one). If it reports a problem, it will name the exact file and issue (missing frontmatter/description, name mismatch, or duplicate name) — fix and re-run before continuing.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/tools--codex-workflow/SKILL.md
git commit -m "feat: add tools--codex-workflow skill

Playbook for using the codex-plugin-cc plugin: Claude Code stays
primary (plan/implement/decide), Codex is manual-only secondary
reviewer, adversarial reviewer, and bounded test validator/executor.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

### Task 3: Document both additions in `SKILLS_GUIDE.md`

**Files:**
- Modify: `SKILLS_GUIDE.md` (repo root)

**Interfaces:**
- Consumes: plugin name `codex@openai-codex` / marketplace `openai-codex` from Task 1; skill name `tools--codex-workflow` from Task 2 — both referenced as prose text, not code.
- Produces: nothing further downstream.

The exact tables to edit were read earlier this session. The official-plugins table is a Markdown table with columns `Fonte | Skills | O que faz`, one row per plugin/pack, located under the `## Skills oficiais / plugins` heading. The local skills table for the `tools--` category is under `### ... (tools--, N)` — locate it by searching the file for `tools--cavecrew` (it is the current last-documented `tools--` entry before the caveman-family rows).

- [ ] **Step 1: Add a row to the official plugins table**

Use Edit on `SKILLS_GUIDE.md`. In the table under `## Skills oficiais / plugins`, add this row immediately after the `playwright` row (last row of that table):

```markdown
| **codex-plugin-cc** (openai-codex) | `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`, `/codex:transfer`, `/codex:status`, `/codex:result`, `/codex:setup` | Claude Code → Codex CLI local, uso 100% manual (sem hook automático). Codex atua como revisor independente, revisor adversarial (arquitetura/segurança) e validador/executor de teste em tarefas delimitadas — nunca implementação livre nem decisão final. Ver `tools--codex-workflow` pro playbook completo |
```

- [ ] **Step 2: Add a row to the local `tools--` skills table**

In the `tools--` category table (find it via the `tools--cavecrew` row), add this row right after the `tools--cavecrew` row:

```markdown
| `tools--codex-workflow` | Playbook de delegação Claude Code ↔ Codex: tabela de responsabilidade, fluxo de 7 passos (planejar → implementar incremental → `/codex:review` → `/codex:adversarial-review` em mudança de risco → classificar achado antes de aplicar → `/codex:rescue` delimitado → validar teste) e 6 regras operacionais (um agente escreve por vez, revisar antes de corrigir, tarefa delimitada, checar diff sempre, não misturar objetivo, decisão final é sua) |
```

- [ ] **Step 3: Verify both rows landed correctly**

Run: `grep -n "codex" SKILLS_GUIDE.md`
Expected: two matching lines (one per table), each starting with `|` and containing well-formed Markdown table syntax (matching pipe count of neighboring rows in the same table).

- [ ] **Step 4: Commit**

```bash
git add SKILLS_GUIDE.md
git commit -m "docs: document codex-plugin-cc and tools--codex-workflow in SKILLS_GUIDE

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

---

## Final Verification (after all 3 tasks)

- [ ] Run `python -c "import json; json.load(open('plugins.json'))" && echo VALID` — expect `VALID`.
- [ ] Run `python .claude/skills/meta--skill-lint/scripts/lint.py` — expect `skill-lint: 47 skills OK`.
- [ ] Run `git log --oneline -3` — expect the three commits from Tasks 1-3, newest last.
- [ ] Run `git status` — expect clean working tree.
