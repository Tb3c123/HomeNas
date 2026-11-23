#!/usr/bin/env python3
"""Validate CasaOS Native Compose (Zero `build:`) & Trigger Safe Host-Keeper Apply/Install."""

import argparse
import json
import pathlib
import re
import subprocess
import sys
import time
from typing import Any, Callable

DEFAULT_STATE_DIR = pathlib.Path("/mnt/disk1/Workspace/HomeNas/.state")
DEFAULT_WORKSPACE_ROOT = pathlib.Path("/mnt/disk1/Workspace")
APP_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}$")


def validate_casaos_compose(
    app_slug: str,
    compose_path: pathlib.Path,
    workspace_root: pathlib.Path = DEFAULT_WORKSPACE_ROOT,
) -> list[str]:
    errors: list[str] = []
    if not APP_SLUG_RE.match(app_slug):
        errors.append(f"Invalid app slug '{app_slug}' (use lowercase a-z, 0-9, '-').")
    resolved = compose_path.resolve()
    ws_resolved = workspace_root.resolve()
    try:
        resolved.relative_to(ws_resolved)
    except ValueError:
        errors.append(f"Compose file must reside inside {ws_resolved}.")
    if resolved.name != "casaos-compose.yml":
        errors.append("CasaOS native manifest must be named 'casaos-compose.yml'.")
    if not resolved.is_file():
        errors.append(f"File not found: {resolved}")
        return errors

    text = resolved.read_text(encoding="utf-8")
    if re.search(r"^\s*build\s*:", text, flags=re.MULTILINE):
        errors.append("CasaOS parser rejects 'build:'. Pre-build local images via docker-compose.yml and use 'image:' only.")
    if "x-casaos:" not in text:
        errors.append("Missing 'x-casaos:' metadata block required for CasaOS Native App registration.")
    if not re.search(r"^\s*image\s*:", text, flags=re.MULTILINE):
        errors.append("Missing 'image:' directive in casaos-compose.yml.")
    return errors


def run_apply_with_install_fallback(
    app_slug: str,
    compose_path: pathlib.Path,
    cmd_runner: Callable[[list[str]], tuple[int, str]] | None = None,
) -> dict[str, Any]:
    def _default_run(cmd: list[str]) -> tuple[int, str]:
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return p.returncode, (p.stdout + p.stderr).strip()

    runner = cmd_runner or _default_run
    fpath = str(compose_path.resolve())
    rc, out = runner(["casaos-cli", "app-management", "apply", app_slug, f"--file={fpath}"])
    if rc == 0:
        return {"ok": True, "action": "APPLIED", "output": out}
    if re.search(r"404|not\s+found", out, flags=re.IGNORECASE):
        irc, iout = runner(["casaos-cli", "app-management", "install", "-f", fpath])
        return {"ok": irc == 0, "action": "INSTALLED" if irc == 0 else "FAILED_INSTALL", "output": iout}
    return {"ok": False, "action": "FAILED_APPLY", "output": out}


def request_casaos_apply(
    app_slug: str,
    compose_path: pathlib.Path,
    workspace_root: pathlib.Path = DEFAULT_WORKSPACE_ROOT,
    state_dir: pathlib.Path = DEFAULT_STATE_DIR,
    wait_sec: float = 0.0,
) -> dict[str, Any]:
    errors = validate_casaos_compose(app_slug, compose_path, workspace_root=workspace_root)
    if errors:
        return {"ok": False, "status": "INVALID_COMPOSE", "errors": errors}

    state_dir.mkdir(parents=True, exist_ok=True)
    req_file = state_dir / "casaos_apply_req.json"
    res_file = state_dir / "casaos_apply_result.txt"
    if res_file.exists():
        res_file.unlink()

    payload = {"app": app_slug, "file": str(compose_path.resolve()), "ts": int(time.time())}
    req_file.write_text(json.dumps(payload), encoding="utf-8")

    deadline = time.time() + max(0.0, wait_sec)
    while time.time() < deadline:
        if res_file.exists() and res_file.read_text(encoding="utf-8").strip():
            txt = res_file.read_text(encoding="utf-8").strip()
            ok = "APPLIED " in txt or "INSTALLED " in txt or "OK " in txt
            action = "INSTALLED" if "INSTALLED " in txt else ("APPLIED" if "APPLIED " in txt else "ERROR")
            return {"ok": ok, "status": action, "result": txt}
        time.sleep(0.5)

    return {
        "ok": True,
        "status": "QUEUED_FOR_HOST_KEEPER",
        "req_file": str(req_file),
        "fallback_web": "CasaOS Web UI -> '+' -> Install a customized app -> Import -> dán casaos-compose.yml -> Submit -> Install",
        "fallback_ssh": f"casaos-cli app-management install -f {compose_path.resolve()}",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="casaos-apply", description="Validate & register CasaOS Native App")
    parser.add_argument("--app", required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE_ROOT))
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR))
    parser.add_argument("--wait", type=float, default=8.0)
    args = parser.parse_args(argv)
    out = request_casaos_apply(
        app_slug=args.app,
        compose_path=pathlib.Path(args.file),
        workspace_root=pathlib.Path(args.workspace_root),
        state_dir=pathlib.Path(args.state_dir),
        wait_sec=args.wait,
    )
    print(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
