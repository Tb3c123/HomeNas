---
name: bash-pro
description: Write safe, defensive Bash/POSIX shell scripts with strict mode, proper quoting, trap cleanup, and zero word-splitting bugs.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Bash Pro (Defensive Shell Scripting)

## Use This Skill When
- Writing automation scripts, Docker entrypoints, deployment wrappers, or Linux/NAS ops scripts.

## Defensive Scripting Rules
1. **Strict Mode Always:** Start Bash scripts with `#!/usr/bin/env bash` and `set -euo pipefail` (`IFS=$'\n\t'` when splitting lines).
2. **Quote Every Variable:** Always write `"$var"`, `"${arr[@]}"`, and `"$(cmd)"` — unquoted variables break on spaces and globbing.
3. **Cleanup Traps:** Use `trap cleanup EXIT` to remove temporary files in `/tmp` or release locks even when a command fails.
4. **Safe Path & Arg Handling:** Use `--` before user paths (`rm -f -- "$file"`), validate required args early, and never `eval` untrusted input.
5. **Know When to Switch to Python:** If a script needs JSON parsing, complex data structures, or >80 lines of logic, write it in Python instead.
