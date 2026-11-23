"""Unit Tests for v2.0.1 CasaOS Native App Validator & Safe Host-Keeper Bridge."""

import json
import pathlib
import tempfile
import unittest

from shared.tools.project_loader.casaos_apply import request_casaos_apply, validate_casaos_compose


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

    def test_valid_casaos_compose_queues_safe_request_for_host_keeper(self) -> None:
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
            self.assertTrue(req_data["file"].endswith("casaos-compose.yml"))


if __name__ == "__main__":
    unittest.main()
