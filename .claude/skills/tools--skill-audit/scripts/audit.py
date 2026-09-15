#!/usr/bin/env python3
"""Flag likely-duplicate local skills and list them next to installed
marketplace/official skills, so overlap is visible before adding a new one."""
import json
import os
import re
import sys
from itertools import combinations
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[4]
SKILLS_DIR = ROOT / ".claude" / "skills"
PLUGINS_JSON = ROOT / "plugins.json"
PLUGIN_CACHE = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".claude" / "plugins" / "cache"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "when", "use", "used", "using",
    "skill", "should", "user", "wants", "needs", "or", "a", "an", "to", "of",
    "in", "on", "any", "also", "any", "from", "into", "your", "you", "is", "are",
    "be", "it", "its", "as", "e.g", "like", "asks", "want", "help", "based",
}


def get_description(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return ""
    body = m.group(1)
    dm = re.search(r"^description:\s*(.*?)(?=^\w+:|\Z)", body, re.DOTALL | re.MULTILINE)
    return dm.group(1) if dm else ""


def keywords(desc: str) -> set:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{3,}", desc.lower())
    return {w for w in words if w not in STOPWORDS}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def local_skills():
    result = {}
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        f = d / "SKILL.md"
        if f.is_file():
            result[d.name] = keywords(get_description(f))
    return result


def marketplace_skills():
    names = []
    if not PLUGINS_JSON.is_file():
        return names
    manifest = json.loads(PLUGINS_JSON.read_text(encoding="utf-8"))
    for plugin_ref in manifest.get("plugins", []):
        plugin_name = plugin_ref.split("@")[0]
        # search plugin cache for this plugin's skills/ dir, any version
        for hit in PLUGIN_CACHE.glob(f"*/{plugin_name}/*/skills/**/SKILL.md"):
            names.append(f"{plugin_name}:{hit.parent.name}")
        for hit in PLUGIN_CACHE.glob(f"*/{plugin_name}/*/*/SKILL.md"):
            # plugins with a flat skills layout (single-skill plugins)
            rel = hit.relative_to(PLUGIN_CACHE)
            names.append(f"{plugin_name}:{rel.parts[-2]}")
    return sorted(set(names))


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"ERROR: {SKILLS_DIR} not found")
        return 1

    locals_ = local_skills()
    market = marketplace_skills()

    print(f"=== {len(locals_)} local skills vs {len(market)} known marketplace skills ===\n")

    print("-- Marketplace/official skills found in plugin cache --")
    if market:
        for m in market:
            print(f"  {m}")
    else:
        print("  (none found — plugin cache not populated locally, or plugins.json missing)")

    print(f"\n-- Local skills ({len(locals_)}) --")
    for name in locals_:
        print(f"  {name}")

    print("\n-- Likely-duplicate LOCAL pairs (keyword overlap >= 0.35) --")
    threshold = 0.35
    found = False
    for a, b in combinations(locals_.items(), 2):
        (name_a, kw_a), (name_b, kw_b) = a, b
        score = jaccard(kw_a, kw_b)
        if score >= threshold:
            found = True
            print(f"  {score:.2f}  {name_a}  <->  {name_b}")
    if not found:
        print("  (none above threshold)")

    print(
        "\nReminder: for any overlap against an official/marketplace skill, prefer the "
        "official one unless the local skill covers something it genuinely lacks. "
        "See SKILLS_GUIDE.md 'Histórico de limpeza' for the precedent."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
