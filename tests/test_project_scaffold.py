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

            self.assertIn("🚀 Dán vào khung chat mới", res["kickoff_prompt"])
            self.assertIn("Kanboard Project #2", res["kickoff_prompt"])
            self.assertIn("Web bán hàng cá nhân", res["kickoff_prompt"])
            self.assertEqual(audit_repository(proj_dir), [])


if __name__ == "__main__":
    unittest.main()
