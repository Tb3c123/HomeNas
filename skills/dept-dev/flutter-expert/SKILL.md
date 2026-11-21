---
name: flutter-expert
description: Build smooth, cross-platform Flutter/Dart apps with clean widget composition, predictable state management, and responsive layouts.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# Flutter Expert (Cross-Platform Mobile & Desktop)

## Use This Skill When
- Building iOS, Android, macOS, Windows, Linux, or Web apps with Flutter and Dart.

## Core Flutter Standards
1. **Small `const` Widgets:** Decompose large `build()` methods into focused `StatelessWidget` classes (`<= 150 lines/file`) and mark immutable widgets `const` to minimize rebuilds.
2. **Clean State Separation:** Keep business logic and async I/O out of UI widgets; use Riverpod / Bloc / ChangeNotifier with immutable state models (`freezed` or sealed classes).
3. **Lifecycle & Resource Cleanup:** Always dispose `TextEditingController`, `ScrollController`, `FocusNode`, and stream subscriptions inside `dispose()`.
4. **Responsive & Adaptive UI:** Handle safe areas, keyboard insets, and desktop/tablet breakpoints cleanly with `LayoutBuilder` and `MediaQuery`.
5. **Verification:** Run `dart analyze` (zero warnings) and write widget + unit tests for critical flows.
