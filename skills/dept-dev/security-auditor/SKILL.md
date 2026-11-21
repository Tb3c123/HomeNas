---
name: security-auditor
description: Audit applications, APIs, auth flows, and infrastructure for OWASP Top 10 vulnerabilities, secret leaks, injection risks, and least-privilege compliance.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Security Auditor & Secure Coding

## Use This Skill When
- Reviewing auth/session flows, API endpoints, subprocess/shell calls, file I/O, or Docker/infra configs.
- Performing pre-release security checks and dependency/secret hygiene audits.

## High-Priority Audit Checklist
1. **Injection Prevention:** Parameterized SQL only; avoid `shell=True` with untrusted input; validate/sanitize file paths against path traversal (`..`).
2. **Authentication & Authorization:** Verify authz on every object/endpoint (prevent IDOR/BOLA); use constant-time secret comparison and strong password hashing (Argon2/bcrypt).
3. **Secrets Hygiene:** Zero hardcoded tokens, API keys, or passwords in code, tests, logs, or Git history; load secrets via environment variables or mounted secret files (`.env` gitignored).
4. **Web & Client Safety:** Escape untrusted HTML (prevent XSS), enforce strict CORS, set secure cookie flags (`HttpOnly`, `Secure`, `SameSite`), and avoid `dangerouslySetInnerHTML`.
5. **Least Privilege & Supply Chain:** Run containers non-root when feasible, mount sensitive host volumes read-only (`:ro`), pin/audit dependencies, and restrict network exposure (`127.0.0.1` for internal services).

## Reporting Format
- Classify findings by severity (`Critical / High / Medium / Low`), cite exact file & line, explain exploit path, and provide minimal safe remediation.
- Never run destructive exploits or leak real credentials in output.
