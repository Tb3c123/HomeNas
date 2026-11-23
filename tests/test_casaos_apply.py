"""Unit Tests for v2.0.2 CasaOS Native App Validator, Apply->Install 404 Fallback & Memory CLI."""

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

from shared.tools.project_loader.casaos_apply import (
    request_casaos_apply,
    run_apply_with_install_fallback,
    validate_casaos_compose,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class CasaosApplyTests(unittest.TestCase):
    def test_rejects_build_directive_missing_xcasaos_and_path_escape(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            ws = pathlib.Path(tmp) / "Workspace"
            app_dir = ws / "demo-app"
            app_dir.mkdir(parents=True)

            bad_build = app_dir / "casaos-compose.yml"
            bad_build.write_text(
                "name: demo-app\nservices:\n  web:\n    build: .\n    image: demo-app-web:latest\nx-casaos:\n  main: web\n",
                encoding="utf-8",
            )
            errs = validate_casaos_compose("demo-app", bad_build, workspace_root=ws)
            self.assertTrue(any("build:" in e for e in errs))

            outside = pathlib.Path(tmp) / "casaos-compose.yml"
            outside.write_text("services:\n  web:\n    image: nginx:latest\nx-casaos:\n  main: web\n", encoding="utf-8")
            errs_out = validate_casaos_compose("demo-app", outside, workspace_root=ws)
            self.assertTrue(any("must reside inside" in e for e in errs_out))

            errs_slug = validate_casaos_compose("bad;rm -rf /", bad_build, workspace_root=ws)
            self.assertTrue(any("Invalid app slug" in e for e in errs_slug))

    def test_apply_success_and_404_fallback_to_install(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            fpath = pathlib.Path(tmp) / "casaos-compose.yml"
            fpath.write_text("services:\n  web:\n    image: demo:latest\nx-casaos:\n  main: web\n", encoding="utf-8")

            # Branch 1: existing app -> apply succeeds directly
            cmds_apply: list[list[str]] = []
            res_apply = run_apply_with_install_fallback(
                "demo-app", fpath, cmd_runner=lambda c: (cmds_apply.append(c) or (0, "applied ok")),
            )
            self.assertTrue(res_apply["ok"])
            self.assertEqual(res_apply["action"], "APPLIED")
            self.assertEqual(len(cmds_apply), 1)
            self.assertEqual(cmds_apply[0][2], "apply")

            # Branch 2: first-time app -> apply returns 404 Not Found -> auto-fallback to install -f
            cmds_inst: list[list[str]] = []

            def fake_404_runner(cmd: list[str]) -> tuple[int, str]:
                cmds_inst.append(cmd)
                if cmd[2] == "apply":
                    return 1, "Error: 404 Not Found"
                return 0, "installed ok"

            res_inst = run_apply_with_install_fallback("new-app", fpath, cmd_runner=fake_404_runner)
            self.assertTrue(res_inst["ok"])
            self.assertEqual(res_inst["action"], "INSTALLED")
            self.assertEqual(len(cmds_inst), 2)
            self.assertEqual(cmds_inst[1][:4], ["casaos-cli", "app-management", "install", "-f"])

    def test_valid_casaos_compose_queues_safe_request_and_memory_cli_works_without_pythonpath(self) -> None:
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            ws = pathlib.Path(tmp) / "Workspace"
            app_dir = ws / "stochastic-matrix-lab"
            state_dir = ws / "HomeNas" / ".state"
            app_dir.mkdir(parents=True)

            good = app_dir / "casaos-compose.yml"
            good.write_text(
                "name: stochastic-matrix-lab\nservices:\n  backend:\n    image: stochastic-matrix-lab-backend:latest\n"
                "x-casaos:\n  main: backend\n  port_map: '3080'\n",
                encoding="utf-8",
            )
            res = request_casaos_apply(
                "stochastic-matrix-lab", good, workspace_root=ws, state_dir=state_dir, wait_sec=0.0,
            )
            self.assertTrue(res["ok"])
            self.assertEqual(res["status"], "QUEUED_FOR_HOST_KEEPER")
            req_data = json.loads((state_dir / "casaos_apply_req.json").read_text(encoding="utf-8"))
            self.assertEqual(req_data["app"], "stochastic-matrix-lab")

            # Verify memory_manager/cli.py runs directly from another cwd WITHOUT PYTHONPATH
            clean_env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
            clean_env["PYTHONDONTWRITEBYTECODE"] = "1"
            cli_script = str(REPO_ROOT / "shared" / "tools" / "memory_manager" / "cli.py")
            proc = subprocess.run(
                [sys.executable, cli_script, "list", "--dept", "demo"],
                cwd=str(app_dir), env=clean_env, capture_output=True, text=True, check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
