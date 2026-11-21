---
name: csharp-pro
description: Build clean .NET 8+ / C# applications with nullable reference types, async CancellationToken flows, minimal APIs, and xUnit tests.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# C# / .NET Pro (Modern .NET 8+)

## Use This Skill When
- Building ASP.NET Core APIs, desktop apps, background workers, or libraries in C# / .NET 8+.

## Modern .NET Discipline
1. **Nullable Safety:** Enable `<Nullable>enable</Nullable>` and `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`; use `record` types for immutable DTOs and `required` properties.
2. **Async All the Way:** Pass `CancellationToken` through every async call; never block on async code (`.Result` / `.Wait()`) to prevent thread-pool starvation and deadlocks.
3. **Dependency Injection & Options:** Register services with explicit lifetimes (`Scoped`, `Transient`, `Singleton`) and bind validated configuration via `IOptions<T>`.
4. **Data Access Hygiene:** Use EF Core `AsNoTracking()` for read-only queries, project directly to DTOs (`Select`), and avoid client-side evaluation of large tables.
5. **Testing:** Cover domain logic with fast xUnit tests and verify HTTP endpoints with `WebApplicationFactory`.
