"""Verify the curated 79-skill Dev Team library (frontmatter, line cap, catalog sync & scripts)."""

import importlib.util
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills" / "dept-dev"

EXPECTED_SKILLS = {
    # 1. Process, Product & Systems Architecture (10)
    "micro-agent-swarm", "context-driven-development", "architecture-patterns",
    "api-design-principles", "microservices-patterns", "event-sourcing-architect",
    "performance-engineer", "monorepo-architect", "docs-architect", "viet-nhu-nguoi",
    # 2. UI/UX Pro & Interaction Design (16)
    "ui-ux-designer", "design-md-system", "frontend-aesthetic-design", "design-tokens-oklch",
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
    # 7. Quality, Testing, Debugging & Security (10)
    "code-review-excellence", "code-graph-rag", "tdd-orchestrator", "python-testing-patterns",
    "e2e-testing-patterns", "debugging-strategies", "error-handling-patterns",
    "security-auditor", "auth-implementation-patterns", "threat-modeling-expert",
    # 8. DevOps, Cloud, Git & Observability (5)
    "deployment-engineer", "git-advanced-workflows", "github-actions-templates",
    "kubernetes-architect", "observability-engineer",
}


def test_dev_skills_pack_completeness_and_frontmatter():
    assert len(EXPECTED_SKILLS) == 79
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


def test_viet_nhu_nguoi_scan_and_check_facts():
    scripts = SKILLS_DIR / "viet-nhu-nguoi" / "scripts"
    scan_spec = importlib.util.spec_from_file_location("vnn_scan", scripts / "scan.py")
    facts_spec = importlib.util.spec_from_file_location("vnn_facts", scripts / "check_facts.py")
    assert scan_spec and scan_spec.loader and facts_spec and facts_spec.loader
    scan_mod = importlib.util.module_from_spec(scan_spec)
    facts_mod = importlib.util.module_from_spec(facts_spec)
    scan_spec.loader.exec_module(scan_mod)
    facts_spec.loader.exec_module(facts_mod)

    ai_res = scan_mod.scan_text("Tất nhiên rồi! Trong bối cảnh hiện nay, công cụ này không chỉ nhanh mà còn nâng tầm giá trị.")
    assert ai_res["score"] > 20
    clean_res = scan_mod.scan_text("Hệ thống đã chạy ổn định từ 08:00 sáng nay, nhiệt độ ổ cứng giữ ở 55 độ.")
    assert clean_res["score"] == 0

    ok_res = facts_mod.compare_facts("Bản v2.2.0 có 78 skills, không dùng Memgraph.", "Bản v2.2.0 gồm 78 skills và không chạy Memgraph.")
    assert ok_res["ok"] is True
    bad_res = facts_mod.compare_facts("Tốc độ đạt 2.5 MB/s tại https://example.com", "Tốc độ rất nhanh.")
    assert bad_res["ok"] is False and "numbers" in bad_res["missing_facts"]
