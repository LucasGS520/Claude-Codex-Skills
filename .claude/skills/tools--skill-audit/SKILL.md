---
name: skill-audit
description: Scans .claude/skills/ for likely duplicate or overlapping skills (by keyword similarity in their descriptions) and lists installed official/marketplace skills (superpowers, mattpocock-skills, etc.) side by side, so overlap is visible before adding a new skill. Use when the user says "audit skills", "check for duplicate skills", "does a skill for X already exist", or before installing/creating a new skill.
disable-model-invocation: true
---

# Skill Audit

Applies the same criteria used in this repo's 154→44 cleanup (2026-09-15, see `SKILLS_GUIDE.md`) so it doesn't have to be redone by hand: prefer official/actively-maintained packs (superpowers, mattpocock-skills, official Anthropic plugins) over custom skills that duplicate them; flag niche one-off skills; flag near-duplicate descriptions.

## Usage

```bash
python .claude/skills/tools--skill-audit/scripts/audit.py
```

Run `tools--skill-lint` first — a broken (undescribed) skill can't be compared meaningfully.

## What it does

1. Reads every local skill's `description:` from `.claude/skills/*/SKILL.md`.
2. Reads the officially-tracked marketplace skill names from `plugins.json`'s referenced plugins (superpowers, mattpocock-skills, code-review, frontend-design, skill-creator) if their plugin cache is present.
3. Flags pairs of *local* skills whose descriptions share unusually high keyword overlap — candidates for merging or removing one.
4. Prints a plain list of every local skill name next to every known official/marketplace skill name, so a human can eyeball "does X already exist officially?" before writing a new one.

## Decision rule (matches this repo's cleanup criteria)

When a local skill overlaps an official/marketplace one:
- **Exact duplicate purpose** → remove the local skill, use the official one.
- **Partial overlap, official is actively maintained by a known author/org** → prefer official, remove local unless the local one covers something official genuinely lacks.
- **No overlap** → keep, no action.

When two *local* skills overlap each other: merge into one, or keep the more general one and cut the narrower/niche one — matches how `composio--connect` was cut in favor of `composio--apps`.
