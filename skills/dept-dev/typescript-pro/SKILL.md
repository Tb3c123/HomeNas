---
name: typescript-pro
description: Write strict, maintainable TypeScript using discriminated unions, generics, runtime schema validation, and zero-any contracts.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# TypeScript Pro (Strict Typing & Contracts)

## Use This Skill When
- Designing shared types, API contracts, frontend state models, or Node.js/Electron/Tauri backends in TypeScript.
- Tightening `tsconfig.json` strictness or eliminating unsafe `any` casts.

## Core Typing Discipline
1. **Strict Compiler Flags:** Enable `"strict": true`, `"noUncheckedIndexedAccess": true`, and `"exactOptionalPropertyTypes": true` where feasible; ban `any` (use `unknown` + type guards instead).
2. **Discriminated Unions Over Optional Bags:** Model state machines cleanly (`{ status: "idle" } | { status: "loading" } | { status: "error"; message: string } | { status: "ready"; data: T }`) and enforce exhaustiveness with `never`.
3. **Validate External Boundaries:** TypeScript types vanish at runtime — validate JSON from APIs, IPC, or config files with a schema validator (e.g., Zod) and infer TS types from schemas (`z.infer`).
4. **Prefer Composition & Utility Types:** Use `Pick`, `Omit`, `Readonly`, `Record`, and `satisfies` to keep types DRY and inference sharp.
5. **Clean Module Boundaries:** Keep barrel files minimal to avoid circular imports; split modules cleanly (`<= 150 lines/file`).

## Verification Checklist
- `tsc --noEmit` passes with zero errors and zero `@ts-ignore` suppressions.
