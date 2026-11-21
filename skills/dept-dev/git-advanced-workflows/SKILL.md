---
name: git-advanced-workflows
description: Manage clean Git history, isolated git worktrees for parallel agents, safe rebasing, bisecting, and atomic pull requests.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Git Advanced Workflows

## Use This Skill When
- Coordinating parallel feature/agent branches with `git worktree`, cleaning commit history, or bisecting regressions.

## Pro Git Discipline
1. **Isolated Worktrees for Parallel Work:** Use `git worktree add ../wt-feature -b feat/xyz` so multiple agents/CLIs work on separate branches without colliding on the same working tree.
2. **Atomic Conventional Commits:** Each commit represents one coherent change (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`) with passing tests.
3. **Safe History Rewriting:** Rebase only local/unshared feature branches (`git pull --rebase`); never force-push `main` (use `--force-with-lease` on personal PR branches only).
4. **Fast Regression Hunting:** Use `git bisect start HEAD <good-tag>` + automated test script (`git bisect run ...`) to find breaking commits in O(log N) steps.
5. **Pre-Commit Hygiene:** Inspect `git status` and `git diff --staged` to ensure zero `.env`, cache files, or stray debug prints are ever committed.
