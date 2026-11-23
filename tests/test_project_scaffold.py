"""Unit Tests for Standalone Project Factory Scaffolder & Kickoff Prompt Generator."""

import pathlib
import tempfile
import unittest
from typing import Any

from shared.tools.guardrails.pre_tool_guard import audit_repository
from shared.tools.kanboard_client.rpc_client import KanboardClient
from shared.tools.project_loader.loader import load_project_manifest
from shared.tools.project_loader.scaffold import scaffold_project


class FakeScaffoldKanboardClient(KanboardClient):
    def __init__(self) -> None:
        super().__init__(url="http://mock/jsonrpc.php", token="tok")
        self.calls: list[str] = []

    def call(self, method: str, params: dict[str, Any] | None = None) -> Any:
        self.calls.append(method)
        if method == "getAllProjects":
            return []
        if method == "createProject":
            return 2
        if method == "getUserByName":
            return {"id": 5, "username": "dept-dev"}
        if method == "getColumns":
            return [{"id": 1, "title": "Backlog"}, {"id": 2, "title": "Work in progress"}]
        if method == "getAllSwimlanes":
            return [{"id": 1, "name": "Default swimlane"}]
        return True


class ProjectScaffoldTests(unittest.TestCase):
    def test_scaffold_creates_isolated_project_and_kickoff_prompt(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            tpath = pathlib.Path(tmp)
            kb = FakeScaffoldKanboardClient()
            res = scaffold_project(
                name="MyShop App",
                summary="Web bán hàng cá nhân",
                workspace_root=tpath,
                kb_client=kb,
            )
            proj_dir = pathlib.Path(res["project_dir"])
            self.assertEqual(proj_dir.name, "MyShop-App")
            self.assertEqual(res["kanboard_project_id"], 2)
            self.assertTrue((proj_dir / "project.yaml").exists())
            self.assertTrue((proj_dir / "AGENTS.md").exists())
            self.assertTrue((proj_dir / "memory" / "MEMORY.md").exists())

            manifest = load_project_manifest(proj_dir / "project.yaml")
            self.assertEqual(manifest["kanboard_project_id"], 2)
            self.assertEqual(manifest["max_lines_per_file"], 150)

            self.assertIn("Hướng dẫn 2 bước bắt đầu", res["kickoff_prompt"])
            self.assertIn("Kanboard Project #2", res["kickoff_prompt"])
            self.assertIn("Web bán hàng cá nhân", res["kickoff_prompt"])
            agents_txt = (proj_dir / "AGENTS.md").read_text(encoding="utf-8")
            yaml_txt = (proj_dir / "project.yaml").read_text(encoding="utf-8")
            gemini_txt = (proj_dir / "GEMINI.md").read_text(encoding="utf-8")
            self.assertIn("/mnt/disk1/Workspace/shared/templates/DEV_TEAM_RULES.md", agents_txt)
            self.assertIn("/mnt/disk1/Workspace/shared/skills/dept-dev", yaml_txt)
            self.assertIn("@[AGENTS.md](AGENTS.md)", gemini_txt)
            self.assertNotIn("/Workspace/HomeNas/", agents_txt)
            self.assertNotIn("/Workspace/HomeNas/", yaml_txt)
            self.assertEqual(audit_repository(proj_dir), [])

    def test_bootstrap_workspace_shared_symlinks_and_legacy_child_migration(self) -> None:
        from shared.tools.project_loader.bootstrap_workspace import bootstrap_workspace_shared

        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            ws = pathlib.Path(tmp)
            (ws / "HomeNas" / "shared" / "templates").mkdir(parents=True)
            (ws / "HomeNas" / "skills" / "dept-dev").mkdir(parents=True)
            (ws / "HomeNas" / "shared" / "templates" / "DEV_TEAM_RULES.md").write_text("# Rules\n", encoding="utf-8")
            (ws / "HomeNas" / "skills" / "dept-dev" / "CATALOG.md").write_text("# Catalog\n", encoding="utf-8")

            child = ws / "stochastic-matrix-lab"
            child.mkdir()
            (child / "AGENTS.md").write_text(
                "Đọc /mnt/disk1/Workspace/HomeNas/shared/templates/DEV_TEAM_RULES.md và /mnt/disk1/Workspace/HomeNas/skills/dept-dev/CATALOG.md\n",
                encoding="utf-8",
            )
            (child / "project.yaml").write_text(
                "shared_dev_skills: \"/mnt/disk1/Workspace/HomeNas/skills/dept-dev\"\n",
                encoding="utf-8",
            )
            (child / "GEMINI.md").write_text("Rule: @[AGENTS.md](.agent/rules/AGENTS.md)\n", encoding="utf-8")

            res = bootstrap_workspace_shared(workspace_root=ws)
            self.assertEqual(res["top_symlink"], "linked")
            self.assertEqual(res["skills_bridge"], "linked")
            self.assertEqual(res["migrated_projects"], ["stochastic-matrix-lab"])
            self.assertTrue((ws / "shared" / "templates" / "DEV_TEAM_RULES.md").is_file())
            self.assertTrue((ws / "shared" / "skills" / "dept-dev" / "CATALOG.md").is_file())
            self.assertNotIn("/Workspace/HomeNas/", (child / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertIn("/mnt/disk1/Workspace/shared/skills/dept-dev", (child / "project.yaml").read_text(encoding="utf-8"))
            self.assertIn("@[AGENTS.md](AGENTS.md)", (child / "GEMINI.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
