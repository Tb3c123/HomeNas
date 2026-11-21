---
name: golang-pro
description: Write idiomatic, concurrent Go code with small interfaces, explicit error wrapping, context propagation, and race-free goroutines.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Go Pro (Idiomatic & Concurrent Go)

## Use This Skill When
- Building CLIs, network daemons, proxies, microservices, or high-concurrency backend tools in Go.

## Idiomatic Go Rules
1. **Accept Interfaces, Return Structs:** Define tiny consumer-side interfaces (1-3 methods) for testability and decoupling.
2. **Explicit Error Wrapping:** Always check errors and add context with `fmt.Errorf("load config %s: %w", path, err)`; inspect via `errors.Is` / `errors.As`.
3. **Context Propagation:** Pass `ctx context.Context` as the first argument to every I/O or long-running function and respect `ctx.Done()` for clean cancellation.
4. **Safe Concurrency:** Every spawned goroutine must have a clear exit path (prevent leaks); prefer `errgroup.WithContext` and channels/mutexes verified with `go test -race ./...`.
5. **Clean Packaging:** Keep packages small and cohesive (`internal/` for non-exported code, `<= 150 lines/file`), zero `init()` side effects, and table-driven unit tests.
