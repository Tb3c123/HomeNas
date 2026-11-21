---
name: java-pro
description: Build clean, modern Java 21+ applications using records, sealed types, virtual threads, constructor injection, and fast JUnit 5 tests.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Java Pro (Modern Java 21+ & Spring)

## Use This Skill When
- Developing enterprise APIs, backend services, or JVM tools in modern Java 21+ / Spring Boot.

## Modern Java Standards
1. **Immutable Data Models:** Use `record` for DTOs/value objects, `sealed interface` + pattern matching `switch` for closed domain hierarchies, and `Optional` for nullable return types (never fields/params).
2. **Constructor Injection Only:** Inject dependencies via `final` fields and constructors (never field `@Autowired`) for immutability and easy unit testing.
3. **Clean Layering:** Keep controllers thin (validation + HTTP mapping), services transactional and framework-light, and repositories focused on persistence.
4. **Concurrency:** Leverage Java 21 Virtual Threads for blocking I/O workloads; avoid thread-local leaks and unbounded executor queues.
5. **Testing:** Write fast unit tests with JUnit 5 + AssertJ and targeted integration tests with Testcontainers when verifying real DB queries.
