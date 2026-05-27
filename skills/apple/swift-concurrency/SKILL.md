---
name: swift-concurrency
description: "Use for Swift Concurrency work: async/await, actors, tasks, Swift 6 migration, data races, Sendable, @MainActor, isolation diagnostics, and concurrency performance."
---
# Swift Concurrency

## Overview

This skill provides expert guidance on Swift Concurrency, covering modern async/await patterns, actors, tasks, Sendable conformance, isolated conformances, and migration to Swift 6 and Swift 6.2. Use this skill to help developers write safe, performant concurrent code and navigate structured concurrency, including approachable concurrency / main-actor-by-default projects.

## Fast Path

Before proposing a fix:

1. Analyze `Package.swift` or `.pbxproj` to determine Swift language mode, strict concurrency level, default isolation, and upcoming features. Do this always when advice depends on build settings, not only for migration work.
2. Capture the exact diagnostic and offending symbol.
3. Determine the isolation boundary: `@MainActor`, custom actor, actor instance isolation, or `nonisolated`.
4. Confirm whether the code is UI-bound or intended to run off the main actor. For delayed retries, timers, and backoff tasks, separate waiting from UI mutation: the sleep often belongs off the main actor even when the final state update belongs on it.

Guardrails:

- Do not recommend `@MainActor` as a blanket fix. Justify why main-actor isolation is correct for the code.
- Prefer structured concurrency (child tasks, task groups) over unstructured tasks. Use `Task.detached` only with a clear reason.
- If recommending `@preconcurrency`, `@unchecked Sendable`, or `nonisolated(unsafe)`, require:
  - a documented safety invariant
  - a follow-up ticket to remove or migrate it
- Optimize for the smallest safe change. Do not refactor unrelated architecture during migration.
- Course references are for deeper learning only. Use them sparingly and only when they clearly help answer the developer's question.

## Recommended Tools for Analysis

When analyzing Swift projects for concurrency issues:

1. **Project Settings Discovery**
   - Use `Read` on `Package.swift` for SwiftPM settings (tools version, strict concurrency flags, upcoming features)
   - Use `Grep` for `SWIFT_STRICT_CONCURRENCY` or `SWIFT_DEFAULT_ACTOR_ISOLATION` in `.pbxproj` files
   - Use `Grep` for `SWIFT_UPCOMING_FEATURE_` to find enabled upcoming features

## Project Settings Intake (Evaluate Before Advising)

Concurrency behavior depends on build settings. Always try to determine:

- Default actor isolation (is the module default `@MainActor` or `nonisolated`?)
- Whether the project is effectively using approachable concurrency / main-actor-by-default
- Strict concurrency checking level (minimal/targeted/complete)
- Whether upcoming features are enabled (especially `NonisolatedNonsendingByDefault`)
- Swift language mode (Swift 5.x vs Swift 6)

### Manual checks (no scripts)

- SwiftPM:
  - Check `swiftLanguageVersions` or `-swift-version` for the language mode. `// swift-tools-version:` is useful context, but it is not a reliable proxy for Swift language mode.
  - Check `Package.swift` for `.defaultIsolation(MainActor.self)`.
  - Check `Package.swift` for `.enableUpcomingFeature("NonisolatedNonsendingByDefault")`.
  - Check for strict concurrency flags: `.enableExperimentalFeature("StrictConcurrency=targeted")` (or similar).
  - Check tools version at the top: `// swift-tools-version: ...`
- Xcode projects:
  - Search `project.pbxproj` for:
    - `SWIFT_DEFAULT_ACTOR_ISOLATION`
    - `SWIFT_STRICT_CONCURRENCY`
    - `SWIFT_UPCOMING_FEATURE_` (and/or `SWIFT_ENABLE_EXPERIMENTAL_FEATURES`)
  - Confirm whether the target is configured for main-actor-by-default / approachable concurrency in build settings

If any of these are unknown, ask the developer to confirm them before giving migration-sensitive guidance.

## Quick Fix Mode

Use Quick Fix Mode when all of these are true:

- The issue is localized to one file or one type.
- The isolation boundary is clear.
- The fix can be explained in 1-2 behavior-preserving steps.

Skip Quick Fix Mode when any of these are true:

- Build settings or default isolation are unknown.
- The issue crosses module boundaries or changes public API behavior.
- The likely fix depends on unsafe escape hatches.

## Swift 6.2 and Approachable Concurrency

Treat Swift 6.2 as a behavior change, not just a stricter compiler release.

- In approachable concurrency / main-actor-by-default projects, async functions often stay on the caller's actor unless code explicitly offloads work.
- Do not assume every `async` function hop leaves the current actor.
- Prefer minimal annotations when the module is already main-actor-by-default and the code is clearly UI-bound.
- Use isolated conformances such as `extension Foo: @MainActor SomeProtocol` instead of forcing `nonisolated` escape hatches.
- Watch for the opposite failure mode: CPU-heavy work silently staying on the main actor. Move real background work into an explicitly offloaded async boundary.

When diagnosing a Swift 6.2 issue, answer these first:

1. Is the module default actor-isolated?
2. Is this code intended to stay UI-bound or run concurrently?
3. Is the error about a real cross-actor send, or about an annotation that can now be simplified?

## Quick Decision Tree

When a developer needs concurrency guidance, follow this decision tree:

0. **Swift 6.2 / approachable concurrency issue?**
   - Check module settings first.
   - Read `references/swift-6-2-concurrency.md` and `references/approachable-concurrency.md`.

1. **Starting fresh with async code?**
   - Read `references/async-await-basics.md` for foundational patterns
   - For parallel operations → `references/tasks.md` (async let, task groups)

2. **Protecting shared mutable state?**
   - Need to protect class-based state → `references/actors.md` (actors, @MainActor)
   - Need thread-safe value passing → `references/sendable.md` (Sendable conformance)

3. **Managing async operations?**
   - Structured async work → `references/tasks.md` (Task, child tasks, cancellation)
   - Streaming data → `references/async-sequences.md` (AsyncSequence, AsyncStream)

4. **Working with legacy frameworks?**
   - Core Data integration → `references/core-data.md`
   - General migration → `references/migration.md`

5. **Performance or debugging issues?**
   - Slow async code → `references/performance.md` (profiling, suspension points)
   - Testing concerns → `references/testing.md` (XCTest, Swift Testing)

6. **Understanding threading behavior?**
   - Read `references/threading.md` for thread/task relationship and isolation

7. **Memory issues with tasks?**
   - Read `references/memory-management.md` for retain cycle prevention

## Common Diagnostics

| Diagnostic | First check | Smallest safe fix | Escalate to |
|---|---|---|---|
| `Main actor-isolated ... cannot be used from a nonisolated context` | Is this truly UI-bound? | Isolate the caller to `@MainActor` or use `await MainActor.run { ... }` only when main-actor ownership is correct. | `references/actors.md`, `references/threading.md` |
| `Actor-isolated type does not conform to protocol` | Must the requirement run on the actor? | Prefer isolated conformance such as `extension Foo: @MainActor SomeProtocol`; use `nonisolated` only for truly nonisolated requirements. | `references/actors.md`, `references/swift-6-2-concurrency.md` |
| `Sending value of non-Sendable type ... risks causing data races` | What isolation boundary is being crossed? | Keep access inside one actor, or convert the transferred value to an immutable/value type. | `references/sendable.md`, `references/threading.md` |
| SwiftLint `async_without_await` | Is `async` required by protocol, override, or `@concurrent`? | Remove `async`, or use a narrow suppression with rationale. Never add fake awaits. | `references/linting.md` |
| `wait(...) is unavailable from asynchronous contexts` | Is this legacy XCTest async waiting? | Replace with `await fulfillment(of:)` or Swift Testing equivalents. | `references/testing.md` |
| Core Data concurrency warnings | Are `NSManagedObject` instances crossing contexts or actors? | Pass `NSManagedObjectID` or map to a Sendable value type. | `references/core-data.md` |
| `Thread.current` unavailable from asynchronous contexts | Are you debugging by thread instead of isolation? | Reason in terms of isolation and use Instruments/debugger instead. | `references/threading.md` |
| SwiftLint concurrency-related warnings | Which lint rule triggered? | Use `references/linting.md` for rule intent and preferred fixes; avoid dummy awaits. | `references/linting.md` |

## When Quick Fixes Fail

1. Gather project settings if not already confirmed.
2. Re-evaluate which isolation boundaries the type crosses.
3. Route to the matching reference file for a deeper fix.
4. If the fix may change behavior, document the invariant and add verification steps.

## Smallest Safe Fixes

- **UI-bound state**: isolate the type or member to `@MainActor`.
- **Shared mutable state**: move it behind an `actor`, or use `@MainActor` only if the state is UI-owned.
- **Background work**: when work must hop off caller isolation, use an `async` API marked `@concurrent`; when work can safely inherit caller isolation, use `nonisolated` without `@concurrent`. If a task mostly waits or retries before one UI-bound mutation, keep the delay off `@MainActor` and hop back only for the final update.
- **Sendability issues**: prefer immutable values and explicit boundaries over `@unchecked Sendable`.

## Core Patterns Reference

### When to Use Each Concurrency Tool

**async/await** - Making existing synchronous code asynchronous
```swift
// Use for: Single asynchronous operations
func fetchUser() async throws -> User {
    try await networkClient.get("/user")
}
```

**async let** - Running multiple independent async operations in parallel
```swift
// Use for: Fixed number of parallel operations known at compile time
async let user = fetchUser()
async let posts = fetchPosts()
let profile = try await (user, posts)
```

**Task** - Starting unstructured asynchronous work
```swift
// Use for: Fire-and-forget operations, bridging sync to async contexts
Task {
    await updateUI()
}
```

**@concurrent** - Explicitly offloading Swift 6.2 async work
```swift
// Use for: Work that must leave the current actor and run on the concurrent pool
@concurrent
func buildThumbnail(from data: Data) async throws -> Thumbnail {
    try await imagePipeline.thumbnail(from: data)
}
```

**Task Group** - Dynamic parallel operations with structured concurrency
```swift
// Use for: Unknown number of parallel operations at compile time
await withTaskGroup(of: Result.self) { group in
    for item in items {
        group.addTask { await process(item) }
    }
}
```

**Actor** - Protecting mutable state from data races
```swift
// Use for: Shared mutable state accessed from multiple contexts
actor DataCache {
    private var cache: [String: Data] = [:]
    func get(_ key: String) -> Data? { cache[key] }
}
```

**@MainActor** - Ensuring UI updates on main thread
```swift
// Use for: View models, UI-related classes
@MainActor
class ViewModel: ObservableObject {
    @Published var data: String = ""
}
```

### Common Scenarios

**Scenario: Network request with UI update**
```swift
Task { @concurrent in
    let data = try await fetchData() // Background
    await MainActor.run {
        self.updateUI(with: data) // Main thread
    }
}
```

**Scenario: Multiple parallel network requests**
```swift
async let users = fetchUsers()
async let posts = fetchPosts()
async let comments = fetchComments()
let (u, p, c) = try await (users, posts, comments)
```

**Scenario: Processing array items in parallel**
```swift
await withTaskGroup(of: ProcessedItem.self) { group in
    for item in items {
        group.addTask { await process(item) }
    }
    for await result in group {
        results.append(result)
    }
}
```

## Swift 6 Migration Quick Guide

Key changes in Swift 6:
- **Strict concurrency checking** enabled by default
- **Complete data-race safety** at compile time
- **Sendable requirements** enforced on boundaries
- **Isolation checking** for all async boundaries

Key shifts to account for in Swift 6.2:
- **Approachable concurrency** can keep async code on the caller's actor by default
- **Main-actor-by-default** is a practical mode for many app targets
- **Isolated conformances** reduce friction on UI-bound protocol implementations
- **Explicit offloading matters more** because "async" alone does not imply background work

For detailed migration steps, see `references/migration.md`, `references/swift-6-2-concurrency.md`, and `references/approachable-concurrency.md`.

## Reference Files

Load these files as needed for specific topics:

- **`async-await-basics.md`** - async/await syntax, execution order, async let, URLSession patterns
- **`tasks.md`** - Task lifecycle, cancellation, priorities, task groups, structured vs unstructured
- **`threading.md`** - Thread/task relationship, suspension points, isolation domains, nonisolated
- **`memory-management.md`** - Retain cycles in tasks, memory safety patterns
- **`actors.md`** - Actor isolation, @MainActor, global actors, reentrancy, custom executors, Mutex
- **`sendable.md`** - Sendable conformance, value/reference types, @unchecked, region isolation
- **`linting.md`** - Concurrency-focused lint rules and SwiftLint `async_without_await`
- **`async-sequences.md`** - AsyncSequence, AsyncStream, when to use vs regular async methods
- **`core-data.md`** - NSManagedObject sendability, custom executors, isolation conflicts
- **`performance.md`** - Profiling with Instruments, reducing suspension points, execution strategies
- **`testing.md`** - XCTest async patterns, Swift Testing, concurrency testing utilities
- **`migration.md`** - Swift 6 migration strategy, closure-to-async conversion, @preconcurrency, FRP migration
- **`swift-6-2-concurrency.md`** - Swift 6.2 behavior changes, isolated conformances, explicit offloading
- **`approachable-concurrency.md`** - quick guide for main-actor-by-default / approachable concurrency mode
- **`swiftui-concurrency-tour-wwdc.md`** - SwiftUI-specific concurrency notes for Sendable closures and off-main evaluation

## Best Practices Summary

1. **Prefer structured concurrency** - Use task groups over unstructured tasks when possible
2. **Minimize suspension points** - Keep actor-isolated sections small to reduce context switches
3. **Use @MainActor judiciously** - Only for truly UI-related code
4. **Make types Sendable** - Enable safe concurrent access by conforming to Sendable
5. **Handle cancellation** - Check Task.isCancelled in long-running operations
6. **Avoid blocking** - Never use semaphores or locks in async contexts
7. **Treat Swift 6.2 settings as part of the bug** - Default actor isolation changes the meaning of many diagnostics
8. **Test concurrent code** - Use proper async test methods and consider timing issues

## Verification Checklist (When You Change Concurrency Code)

- Confirm build settings (default isolation, strict concurrency, upcoming features) before interpreting diagnostics.
- After refactors:
  - Run tests, especially concurrency-sensitive ones (see `references/testing.md`).
  - If performance-related, verify with Instruments (see `references/performance.md`).
  - If lifetime-related, verify deinit/cancellation behavior (see `references/memory-management.md`).

## Glossary

See `references/glossary.md` for quick definitions of core concurrency terms used across this skill.

---

**Note**: This skill is based on the comprehensive [Swift Concurrency Course](https://www.swiftconcurrencycourse.com?utm_source=github&utm_medium=agent-skill&utm_campaign=skill-footer) by Antoine van der Lee.
