---
name: python-pro
description: Write idiomatic, type-safe Python 3.12+ code using modern typing, dataclasses, pathlib, async I/O, and clean modular packaging.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Python Pro (Modern Python 3.12+)

## Use This Skill When
- Implementing Python services, CLIs, automation scripts, or shared libraries.
- Modernizing legacy Python code for type safety, performance, and maintainability.

## Idiomatic Standards
1. **Strict Type Hints:** Use built-in generics (`list[str]`, `dict[str, Any]`, `X | None`), `Protocol` for interfaces, and `@dataclass(frozen=True, slots=True)` for immutable value objects.
2. **Stdlib First:** Prefer `pathlib.Path`, `subprocess.run(..., check=True, shell=False)`, `urllib`/`json`, and `logging` over heavy third-party dependencies when stdlib suffices.
3. **Explicit Error Handling:** Catch specific exception types, attach actionable context, and never use bare `except:`. Use context managers (`with`) for files, locks, and DB connections.
4. **Async & Concurrency:** Never block an `asyncio` event loop with sync I/O (`time.sleep`, sync HTTP); offload blocking calls via `asyncio.to_thread` or keep services cleanly synchronous when single-worker suffices.
5. **Module Hygiene:** Keep modules cohesive and `<= 150 lines/file`; run with `PYTHONDONTWRITEBYTECODE=1` and `/tmp` caches on low-wear SSD environments.

## Verification Checklist
- Functions are small, pure where possible, and have clear input/output types.
- No mutable default arguments (`def f(x=[])`) or hidden global state.
