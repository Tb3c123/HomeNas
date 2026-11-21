"""Verify the curated 18-skill Dev Team library (frontmatter, line cap, catalog sync)."""

import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills" / "dept-dev"

EXPECTED_SKILLS = {
    # Tier 1: Mindset & Engineering Discipline (10)
    "micro-agent-swarm",
    "context-driven-development",
    "ui-ux-designer",
    "architecture-patterns",
    "api-design-principles",
    "code-review-excellence",
    "tdd-orchestrator",
    "security-auditor",
    "deployment-engineer",
    "docs-architect",
    # Tier 2: Language & Stack Packs (8)
    "python-pro",
    "fastapi-pro",
    "python-testing-patterns",
    "typescript-pro",
    "frontend-developer",
    "tailwind-design-system",
    "nodejs-backend-patterns",
    "e2e-testing-patterns",
}


def test_dev_skills_pack_completeness_and_frontmatter():
    found = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}
    assert EXPECTED_SKILLS.issubset(found), f"Missing skills: {EXPECTED_SKILLS - found}"

    catalog_text = (SKILLS_DIR / "CATALOG.md").read_text(encoding="utf-8")
    for skill in sorted(EXPECTED_SKILLS):
        skill_md = SKILLS_DIR / skill / "SKILL.md"
        assert skill_md.is_file(), f"Missing SKILL.md for {skill}"
        content = skill_md.read_text(encoding="utf-8")
        lines = content.splitlines()
        assert len(lines) <= 120, f"{skill}/SKILL.md exceeds 120 lines ({len(lines)})"
        assert lines[0].strip() == "---", f"{skill}/SKILL.md missing YAML frontmatter start"
        assert f"name: {skill}" in content, f"{skill}/SKILL.md missing matching name"
        assert "description:" in content, f"{skill}/SKILL.md missing description"
        assert "model: sonnet" not in content and "model: opus" not in content
        assert f"`{skill}`" in catalog_text, f"{skill} missing from CATALOG.md"
