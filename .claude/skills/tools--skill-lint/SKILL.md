---
name: tools--skill-lint
description: Validates every SKILL.md in .claude/skills/ for a well-formed YAML frontmatter with a non-empty description field, and flags duplicate skill names. Use when the user says "lint skills", "check skills", "validate SKILL.md", "skill health check", after installing a new skill, or before committing changes to .claude/skills/.
disable-model-invocation: true
---

# Skill Lint

Catches broken skills before they sit invisible in the repo — the exact failure mode found in this repo's cleanup: `dev--security-auditor` had no `description:` field and Claude Code could never activate it.

## What it checks

For every `.claude/skills/*/SKILL.md`:
1. File starts with a YAML frontmatter block (`---` ... `---`)
2. Frontmatter has a `description:` field, non-empty
3. `name:` field (if present) matches the folder name
4. No two skills share the same `name:`

## Usage

```bash
python .claude/skills/tools--skill-lint/scripts/lint.py
```

Exit code 0 = all clean. Exit code 1 = at least one broken skill, printed with the specific problem (missing frontmatter / missing description / name mismatch / duplicate name).

## When something fails

- **Missing frontmatter / description:** open the file, add a `description:` that states when to use the skill (trigger phrases help). See any other `SKILL.md` in the repo for the format.
- **Duplicate name:** rename one of the two skills' `name:` field or folder.

Run this after adding any new skill, and before running `tools--skill-audit` (a skill audit is meaningless if some skills are silently broken).
