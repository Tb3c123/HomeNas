"""Verify the curated 48-skill Dev Team library (frontmatter, line cap, catalog sync)."""

import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills" / "dept-dev"

EXPECTED_SKILLS = {
    # 1. Process, Product & Systems Architecture (10)
    "micro-agent-swarm", "context-driven-development", "ui-ux-designer",
    "architecture-patterns", "api-design-principles", "microservices-patterns",
    "event-sourcing-architect", "performance-engineer", "monorepo-architect",
    "docs-architect",
    # 2. Data & Databases (5)
    "database-architect", "postgresql", "sql-optimization-patterns",
    "database-migration", "data-engineer",
    # 3. AI / LLM & Multi-Agent Engineering (5)
    "ai-engineer", "prompt-engineering-patterns", "rag-implementation",
    "llm-evaluation", "agent-orchestration-multi-agent-optimize",
    # 4. Languages, Web & Mobile (13)
    "python-pro", "fastapi-pro", "typescript-pro", "frontend-developer",
    "tailwind-design-system", "nodejs-backend-patterns", "golang-pro",
    "rust-pro", "java-pro", "csharp-pro", "flutter-expert",
    "react-native-architecture", "bash-pro",
    # 5. Quality, Testing, Debugging & Security (10)
    "code-review-excellence", "tdd-orchestrator", "python-testing-patterns",
    "e2e-testing-patterns", "debugging-strategies", "error-handling-patterns",
    "security-auditor", "auth-implementation-patterns", "threat-modeling-expert",
    "accessibility-compliance-accessibility-audit",
    # 6. DevOps, Cloud, Git & Observability (5)
    "deployment-engineer", "git-advanced-workflows", "github-actions-templates",
    "kubernetes-architect", "observability-engineer",
}


def test_dev_skills_pack_completeness_and_frontmatter():
    assert len(EXPECTED_SKILLS) == 48
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
