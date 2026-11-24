"""Verify the curated 76-skill Dev Team library (frontmatter, line cap, catalog sync)."""

import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills" / "dept-dev"

EXPECTED_SKILLS = {
    # 1. Process, Product & Systems Architecture (9)
    "micro-agent-swarm", "context-driven-development", "architecture-patterns",
    "api-design-principles", "microservices-patterns", "event-sourcing-architect",
    "performance-engineer", "monorepo-architect", "docs-architect",
    # 2. UI/UX Pro & Interaction Design (15)
    "ui-ux-designer", "frontend-aesthetic-design", "design-tokens-oklch",
    "typography-and-hierarchy", "tailwind-design-system", "web-interaction-motion",
    "ui-critique-and-polish", "ux-copywriting-microcopy", "forms-and-validation-ux",
    "responsive-layout-architecture", "react-composition-patterns",
    "data-visualization-ux", "interactive-canvas-svg-ui",
    "web-performance-core-vitals", "accessibility-compliance-accessibility-audit",
    # 3. Scientific Research, Math & Algorithms (9)
    "scientific-research-synthesis", "research-ideation-methodology",
    "academic-paper-writing", "autoresearch-experiment-loop",
    "algorithm-design-complexity", "combinatorial-optimization",
    "mathematical-stochastic-modeling", "numerical-computing-vectorization",
    "time-series-forecasting",
    # 4. AI, Machine Learning & LLM Engineering (12)
    "ml-modeling-classical", "deep-learning-pytorch", "llm-finetuning-post-training",
    "ai-inference-optimization", "multimodal-vision-audio-ai",
    "ai-safety-guardrails-alignment", "vector-hybrid-search-engineering",
    "ai-engineer", "prompt-engineering-patterns", "rag-implementation",
    "llm-evaluation", "agent-orchestration-multi-agent-optimize",
    # 5. Data & Databases (5)
    "database-architect", "postgresql", "sql-optimization-patterns",
    "database-migration", "data-engineer",
    # 6. Languages, Web & Mobile (12)
    "python-pro", "fastapi-pro", "typescript-pro", "frontend-developer",
    "nodejs-backend-patterns", "golang-pro", "rust-pro", "java-pro", "csharp-pro",
    "flutter-expert", "react-native-architecture", "bash-pro",
    # 7. Quality, Testing, Debugging & Security (9)
    "code-review-excellence", "tdd-orchestrator", "python-testing-patterns",
    "e2e-testing-patterns", "debugging-strategies", "error-handling-patterns",
    "security-auditor", "auth-implementation-patterns", "threat-modeling-expert",
    # 8. DevOps, Cloud, Git & Observability (5)
    "deployment-engineer", "git-advanced-workflows", "github-actions-templates",
    "kubernetes-architect", "observability-engineer",
}


def test_dev_skills_pack_completeness_and_frontmatter():
    assert len(EXPECTED_SKILLS) == 76
    found = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}
    assert EXPECTED_SKILLS.issubset(found), f"Missing skills: {EXPECTED_SKILLS - found}"

    catalog_text = (SKILLS_DIR / "CATALOG.md").read_text(encoding="utf-8")
    assert len(catalog_text.splitlines()) <= 150, "CATALOG.md exceeds 150 lines"
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
        assert catalog_text.count(f"`{skill}`") == 1, f"{skill} missing or duplicated in CATALOG.md"
