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
