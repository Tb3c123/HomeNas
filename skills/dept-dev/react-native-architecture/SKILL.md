---
name: react-native-architecture
description: Architect cross-platform React Native / Expo apps with typed navigation, offline-friendly state, native performance, and secure storage.
metadata:
  model: inherit
  source: rmyndharis/antigravity-skills (MIT)
---

# React Native Architecture

## Use This Skill When
- Building iOS and Android apps with React Native / Expo and TypeScript.

## Core Mobile Patterns
1. **Typed Navigation & Feature Modules:** Organize code by feature (`features/auth`, `features/tasks`) with strictly typed navigation params (Expo Router / React Navigation).
2. **List & Rendering Performance:** Use `FlashList` / `FlatList` with stable `keyExtractor` and memoized row items; offload heavy animations to Reanimated UI thread.
3. **Offline-First & Network Resilience:** Cache server state (TanStack Query + persistence), handle flaky mobile connectivity gracefully, and show clear sync/retry indicators.
4. **Secure Storage:** Store auth tokens only in OS Keychain/Keystore (`expo-secure-store`), never in plain `AsyncStorage`.
5. **Platform Polish:** Respect safe areas, keyboard avoidance, platform-specific haptics/gestures, and test on both iOS and Android layouts.
