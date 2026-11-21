---
name: auth-implementation-patterns
description: Implement secure authentication and authorization using OAuth2/OIDC, short-lived tokens, RBAC/ABAC, and hardened session cookies.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Auth Implementation Patterns (OAuth2, JWT & RBAC)

## Use This Skill When
- Implementing login, session management, OAuth2/OIDC flows, API tokens, or role/permission checks.

## Security Standards
1. **Sessions vs. JWT:** Prefer opaque server-side sessions (`HttpOnly`, `Secure`, `SameSite=Lax`) for web apps; if using JWTs, keep access tokens short-lived (5-15m), verify `alg`/`iss`/`aud`/`exp`, and rotate refresh tokens.
2. **Password & Secret Hashing:** Hash passwords with Argon2id or bcrypt (cost >= 12); compare API keys/HMACs with constant-time functions (`hmac.compare_digest`).
3. **Enforce AuthZ at Every Boundary:** Check both authentication (who) and authorization (can access this specific resource ID) in the service layer — never trust client-supplied roles or IDs.
4. **OAuth2 / OIDC Hygiene:** Always use Authorization Code Flow + PKCE + `state` nonce; validate exact redirect URIs.
5. **Brute-Force & Lockout Defense:** Rate-limit login/token endpoints and return uniform error messages so attackers cannot enumerate valid accounts.
