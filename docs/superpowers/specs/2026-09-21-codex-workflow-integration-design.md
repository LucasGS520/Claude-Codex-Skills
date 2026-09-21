# Codex Workflow Integration — Design

**Date:** 2026-09-21
**Status:** Approved by user, ready for implementation plan.

## Context

This repo is a personal manifest/library of Claude Code skills and plugins
(`.claude/skills/` copied to `~/.claude/skills/` via `install.sh`; plugin
marketplaces/plugins tracked in `plugins.json`). Until now it targeted
Claude Code only.

Goal: add OpenAI's `codex-plugin-cc` (a Claude Code plugin that lets a
Claude Code session invoke the local Codex CLI) and document the workflow
rules for using it, so Claude Code sessions anywhere on this machine know
how to work with Codex as a secondary engineer.

## What `codex-plugin-cc` actually is

Confirmed by reading its README: a **Claude Code plugin**, not a Codex-side
extension and not a way to make `SKILL.md` files readable by Codex CLI. It
is one-directional (Claude Code → Codex). It adds slash commands to Claude
Code: `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`,
`/codex:transfer`, `/codex:status`, `/codex:result`, `/codex:cancel`,
`/codex:setup`. It wraps the user's local `codex` binary and reuses its
existing config/auth — no separate runtime.

Install commands (documented, run by the user interactively — `codex
login` is interactive and out of scope for scripting):
```
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```

## Decisions (from user Q&A)

- **Skill portability**: skills stay Claude-Code-only (`SKILL.md` format).
  No duplication into Codex's own `AGENTS.md`/`~/.agents/skills` format.
  Codex is reached only through the plugin's slash commands.
- **Trigger model**: manual only. No `Stop` hook, no automatic
  `--enable-review-gate`. The user invokes `/codex:*` explicitly.
- **Codex's role**: code review + test validation, primary. Adversarial
  review for high-risk changes. Bounded execution/investigation via
  `/codex:rescue`. Never unbounded implementation, never automatic merge
  or commit decisions.
- **Explicitly out of scope** (cut after the design was found overbuilt):
  no `templates/` directory or asset files inside the new skill, no
  scaffolding feature that writes `AGENTS.md`/`CLAUDE.md` into *other*
  projects, no `AGENTS.md`/`CLAUDE.md` added to this repo itself (it has
  no build/test to describe). If project-scaffolding is wanted later,
  it's a separate task.

## Final design — 3 changes

### 1. `plugins.json` / `install.sh`

Add to `plugins.json`:
- `marketplaces[]`: `{"name": "openai-codex", "url": "https://github.com/openai/codex-plugin-cc"}`
- `plugins[]`: `"codex@openai-codex"`

`install.sh` needs no code change — it already loops generically over
`marketplaces` and `plugins` from the manifest.

### 2. New skill: `.claude/skills/tools--codex-workflow/SKILL.md`

Single file, no subfolder, following the exact shape of the existing
`tools--cavecrew` skill (YAML frontmatter + markdown body, no assets).
Content (condensed from the user-approved playbook):

- Responsibility table (Claude Code primary on plan/implement/decide;
  Codex primary on review/adversarial-review/test validation).
- 7-step flow: plan → implement incrementally → `/codex:review` (manual,
  after a meaningful feature / before a PR / after a big refactor / on
  request) → `/codex:adversarial-review` for high-risk changes (auth,
  payments, migrations, concurrency, cache, public API, hard-to-revert
  decisions) → classify findings before applying anything (bug real /
  accepted risk / false positive / future improvement) → bounded
  `/codex:rescue` (investigate-first, apply-after-approval) → test
  validation report format.
- 6 operational rules: one agent writes at a time; review before fix;
  bounded tasks only; always re-check `git diff` after Codex touches
  files; don't mix objectives in one Codex task; final decision stays
  with Claude Code/the user.
- Short model/effort note: fast model for simple diagnostics, more
  capable model + higher effort for architecture/security review,
  background execution for large changes.
- Trigger phrases so Claude Code activates it: "revisa com Codex",
  "valida com Codex", "segunda opinião", "review adversarial", "usa
  Codex pra investigar/corrigir X", or before commit/PR on a
  significant feature.

### 3. `SKILLS_GUIDE.md`

Two one-line additions to existing tables (no new section):
- Row in the official plugins table for `codex-plugin-cc` (marketplace
  `openai-codex`): Claude Code → Codex, manual only, review + test
  validation role.
- Row in the local `tools--` skills table for `tools--codex-workflow`:
  points to the playbook above.

## Verification plan

- `plugins.json` stays valid JSON (parse check).
- `python .claude/skills/meta--skill-lint/scripts/lint.py` passes (46 → 47
  skills OK, no missing description, no name collision).
- New `SKILL.md` frontmatter `name:` matches folder name
  (`tools--codex-workflow`), matching the convention every other skill in
  this repo follows.
- Manual read-through of `SKILLS_GUIDE.md` diff for table formatting.

## Explicitly not done here

- Not installing/authenticating the Codex CLI itself (interactive, user's
  own machine action).
- Not writing `AGENTS.md`/`CLAUDE.md` anywhere.
- Not adding hooks of any kind.
