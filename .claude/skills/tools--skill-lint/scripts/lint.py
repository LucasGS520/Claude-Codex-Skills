#!/usr/bin/env python3
"""Validate SKILL.md frontmatter across .claude/skills/. Exit 1 on any problem."""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[4]
SKILLS_DIR = ROOT / ".claude" / "skills"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm = {}
    lines = m.group(1).splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val in (">", "|", ">-", "|-", ">+", "|+") or val == "":
                # block scalar or continued value: non-empty if a following
                # indented (or quoted single-line) block exists
                j = i + 1
                has_content = False
                while j < len(lines) and (lines[j].startswith((" ", "\t")) or lines[j].strip() == ""):
                    if lines[j].strip():
                        has_content = True
                    j += 1
                val = "(block)" if (val and has_content) else val
                i = j - 1
            fm[key] = val
        i += 1
    return fm


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"ERROR: {SKILLS_DIR} not found")
        return 1

    problems = []
    seen_names = {}

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            problems.append(f"{skill_dir.name}: no SKILL.md file")
            continue

        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        if fm is None:
            problems.append(f"{skill_dir.name}: missing/malformed YAML frontmatter (no --- block)")
            continue

        desc = fm.get("description", "")
        if not desc:
            problems.append(f"{skill_dir.name}: missing or empty 'description:' field")

        # Folder-vs-name mismatches are common by convention here (folder is
        # "<category>--<short-name>", frontmatter name varies by author) and
        # aren't a functional problem — Claude Code loads by folder. Only
        # duplicate names across skills are worth flagging (real conflict risk).
        name = fm.get("name")
        if name:
            if name in seen_names:
                problems.append(f"{skill_dir.name}: duplicate name '{name}' (also used by {seen_names[name]})")
            else:
                seen_names[name] = skill_dir.name

    total = sum(1 for d in SKILLS_DIR.iterdir() if d.is_dir())
    if problems:
        print(f"skill-lint: {len(problems)} problem(s) across {total} skills\n")
        for p in problems:
            print(f"  ✗ {p}")
        return 1

    print(f"skill-lint: {total} skills OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
