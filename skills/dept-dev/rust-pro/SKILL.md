---
name: rust-pro
description: Write safe, idiomatic Rust using clean ownership/borrowing, typed Result errors, async Tokio hygiene, and clippy-clean modules.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Rust Pro (Systems, CLI & Tauri Backends)

## Use This Skill When
- Building high-performance CLIs, Tauri desktop backends, system daemons, or memory-safe libraries in Rust.

## Core Rust Discipline
1. **Ownership & Borrowing First:** Prefer borrowing (`&T`, `&mut T`, `&str`, `&[T]`) over unnecessary `.clone()`; use smart pointers (`Arc`, `RwLock`) only when shared ownership is truly required.
2. **Zero `unwrap()` in Production Paths:** Propagate errors with `?`, define typed domain errors with `thiserror` (libraries) or rich context with `anyhow` (binaries).
3. **Make Illegal States Unrepresentable:** Model domain variants with `enum` and newtype wrappers (`struct UserId(u64)`) so the compiler enforces invariants.
4. **Async Tokio Hygiene:** Never hold a `std::sync::Mutex` across `.await` or run blocking CPU/file I/O on async worker threads (use `tokio::task::spawn_blocking`).
5. **Quality Gate:** Run `cargo fmt --check`, `cargo clippy -- -D warnings`, and `cargo test` (with `CARGO_TARGET_DIR=/tmp/cargo-target` on low-wear SSDs).
