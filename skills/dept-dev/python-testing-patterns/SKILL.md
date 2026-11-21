---
name: python-testing-patterns
description: Build fast, reliable Python test suites using pytest fixtures, parameterization, monkeypatch, and clean fakes without flaky I/O or SSD cache wear.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Python Testing Patterns (pytest)

## Use This Skill When
- Writing unit, integration, or regression tests for Python modules, CLIs, or FastAPI apps.
- Setting up isolated fixtures, mocks/fakes, and parameterized test cases.

## Core pytest Patterns
1. **Arrange-Act-Assert (AAA):** Keep each test focused on one behavior with descriptive names (`test_<unit>_<scenario>_<expected>`).
2. **Fixtures & `tmp_path`:** Use `tmp_path` for temporary files/SQLite DBs instead of writing inside the repo; scope fixtures cleanly (`function` by default).
3. **Prefer Fakes Over Over-Mocking:** Inject lightweight in-memory fakes for HTTP/RPC/DB ports so tests verify real behavior rather than fragile call-order internals.
4. **Parameterization:** Use `@pytest.mark.parametrize` to cover edge cases (empty inputs, boundary values, invalid payloads) concisely without copy-pasted tests.
5. **Environment Isolation:** Use `monkeypatch.setenv` / `monkeypatch.setattr` so tests never leak env vars or depend on host machine state.

## Low-Wear Execution Command
- Always run tests with RAM cache and no bytecode writes:
  `PYTHONDONTWRITEBYTECODE=1 pytest -q -o cache_dir=/tmp/.pytest_cache`
