---
name: swiftui-expert-skill
description: "Use for SwiftUI implementation, review, refactors, state management, view composition, accessibility, performance traces, macOS SwiftUI, and optional Liquid Glass adoption."
---

# SwiftUI Expert Skill

## Overview
Use this skill to build, review, or improve SwiftUI features with correct state management, optimal view composition, Observation-first data flow, current SwiftUI APIs, accessibility, and iOS 26+ Liquid Glass styling when requested. Prioritize native APIs, Apple design guidance, and performance-conscious patterns. Architecture should stay simple: prefer MV and Apple-native SwiftUI patterns, not MVVM by default.

## Workflow Decision Tree

### 1) Review existing SwiftUI code
- Check deprecated APIs and modern replacements first (see `references/latest-apis.md`)
- Check property wrapper usage against the selection guide (see `references/state-management.md`)
- Verify view composition follows extraction rules (see `references/view-structure.md`)
- Check performance patterns are applied (see `references/performance-patterns.md`)
- Verify list patterns use stable identity (see `references/list-patterns.md`)
- Check animation patterns for correctness (see `references/animation-basics.md`, `references/animation-transitions.md`)
- Check accessibility basics for tappable controls, Dynamic Type, labels, and grouping (see `references/accessibility-patterns.md`)
- Check focus, text, chart, and macOS topics when relevant (see `references/focus-patterns.md`, `references/text-patterns.md`, `references/charts.md`, `references/charts-accessibility.md`, `references/macos-scenes.md`, `references/macos-window-styling.md`, `references/macos-views.md`)
- Inspect Liquid Glass usage for correctness and consistency (see `references/liquid-glass.md`)
- Validate iOS 26+ availability handling with sensible fallbacks

### 2) Improve existing SwiftUI code
- Replace deprecated APIs with modern equivalents where the deployment target allows it (see `references/latest-apis.md`)
- Audit state management for correct wrapper selection (see `references/state-management.md`)
- Extract complex views into separate subviews (see `references/view-structure.md`)
- Refactor hot paths to minimize redundant state updates (see `references/performance-patterns.md`)
- Ensure ForEach uses stable identity (see `references/list-patterns.md`)
- Improve animation patterns (use value parameter, proper transitions, see `references/animation-basics.md`, `references/animation-transitions.md`)
- Prefer `Button` and accessibility modifiers over gesture-only controls when possible (see `references/accessibility-patterns.md`)
- Suggest image downsampling when `UIImage(data:)` is used (as optional optimization, see `references/image-optimization.md`)
- Adopt Liquid Glass only when explicitly requested by the user

### 3) Implement new SwiftUI feature
- Start from current SwiftUI APIs and avoid deprecated forms (see `references/latest-apis.md`)
- Design data flow first: identify owned vs injected state (see `references/state-management.md`)
- Structure views for optimal diffing (extract subviews early, see `references/view-structure.md`)
- Keep business logic in services and models for testability (see `references/layout-best-practices.md`)
- Apply MV-first defaults before introducing a view model layer (see `references/mv-patterns.md`)
- Use correct animation patterns (implicit vs explicit, transitions, see `references/animation-basics.md`, `references/animation-transitions.md`, `references/animation-advanced.md`)
- Use `Button` for tappable controls and add useful accessibility labels/grouping (see `references/accessibility-patterns.md`)
- Apply glass effects after layout/appearance modifiers (see `references/liquid-glass.md`)
- Gate iOS 26+ features with `#available` and provide fallbacks

### 4) Standardize or refactor an existing SwiftUI feature
- Reorder declarations and helpers for consistent file structure
- Prefer a stable view tree over top-level conditional branch swapping
- Replace optional root view models when they can be constructed deterministically
- Move lightweight orchestration back into the view before inventing a view model
- Prefer `@Observable` + `@State` / `@Bindable` for modern code when platform support allows

### 5) Analyze or record an Instruments trace
- Trigger when the user references an Xcode Instruments `.trace` file or asks to record/profile a SwiftUI app
- For existing traces, scope the requested time window first, then inspect SwiftUI updates, hitches, hangs, Time Profiler symbols, and cause graph fan-in (see `references/trace-analysis.md`)
- For recording requests, confirm whether to attach, launch, or record all processes, and choose the SwiftUI template for real devices/host Mac or Time Profiler for iOS Simulator (see `references/trace-recording.md`)
- Only edit app code after trace analysis if the user asked for edits

## Core Guidelines

### API Currency
- Consult `references/latest-apis.md` at the start of SwiftUI implementation or review tasks
- Prefer native SwiftUI APIs over UIKit/AppKit bridging unless bridging is necessary
- Use `Button` instead of `onTapGesture` for ordinary tappable controls
- Gate version-specific APIs with `#available` and provide sensible fallbacks

### Architecture Stance
- Prefer simple MV over MVVM for SwiftUI unless the existing codebase already uses view models heavily
- Keep business logic in models/services; keep views focused on state expression and UI orchestration
- Do not introduce a view model just to "be clean"
- Standardize toward Apple-native patterns first, custom architecture second

### State Management
- `@State` must be `private`; use for internal view state
- `@Binding` only when a child needs to **modify** parent state
- Prefer `@Observable` for new reference-type UI state when the platform baseline allows it
- Store root `@Observable` models in `@State`; use `@Bindable` in children that need bindings
- `@StateObject` when view **creates** the object; `@ObservedObject` when **injected**
- Keep `ObservableObject` / `@StateObject` / `@ObservedObject` for legacy code or lower platform baselines
- iOS 17+: Use `@State` with `@Observable` classes; use `@Bindable` for injected observables needing bindings
- Use `let` for read-only values; `var` + `.onChange()` for reactive reads
- Never pass values into `@State` or `@StateObject` — they only accept initial values
- Nested `ObservableObject` doesn't propagate changes — pass nested objects directly; `@Observable` handles nesting fine

### View Composition
- Extract complex views into separate subviews for better readability and performance
- Prefer modifiers over conditional views for state changes (maintains view identity)
- Prefer a stable base view and push conditions down into sections/modifiers where possible
- Keep view `body` simple and pure (no side effects or complex logic)
- Use `@ViewBuilder` functions only for small, simple sections
- Prefer `@ViewBuilder let content: Content` over closure-based content properties
- Keep business logic in services and models; views should orchestrate UI flow
- Action handlers should reference methods, not contain inline logic
- Views should work in any context (don't assume screen size or presentation style)

### Performance
- Pass only needed values to views (avoid large "config" or "context" objects)
- Eliminate unnecessary dependencies to reduce update fan-out
- Check for value changes before assigning state in hot paths
- Avoid redundant state updates in `onReceive`, `onChange`, scroll handlers
- Minimize work in frequently executed code paths
- Use `LazyVStack`/`LazyHStack` for large lists
- Use stable identity for `ForEach` (never `.indices` for dynamic content)
- Ensure constant number of views per `ForEach` element
- Avoid inline filtering in `ForEach` (prefilter and cache)
- Avoid `AnyView` in list rows
- Consider POD views for fast diffing (or wrap expensive views in POD parents)
- Suggest image downsampling when `UIImage(data:)` is encountered (as optional optimization)
- Avoid layout thrash (deep hierarchies, excessive `GeometryReader`)
- Gate frequent geometry updates by thresholds
- Use `Self._printChanges()` to debug unexpected view updates

### Animations
- Use `.animation(_:value:)` with value parameter (deprecated version without value is too broad)
- Use `withAnimation` for event-driven animations (button taps, gestures)
- Prefer transforms (`offset`, `scale`, `rotation`) over layout changes (`frame`) for performance
- Transitions require animations outside the conditional structure
- Custom `Animatable` implementations must have explicit `animatableData`
- Use `.phaseAnimator` for multi-step sequences (iOS 17+)
- Use `.keyframeAnimator` for precise timing control (iOS 17+)
- Animation completion handlers need `.transaction(value:)` for reexecution
- Implicit animations override explicit animations (later in view tree wins)
- iOS 26+: prefer `@Animatable` over manual `animatableData` when the deployment target allows it

### Liquid Glass (iOS 26+)
**Only adopt when explicitly requested by the user.**
- Use native `glassEffect`, `GlassEffectContainer`, and glass button styles
- Wrap multiple glass elements in `GlassEffectContainer`
- Apply `.glassEffect()` after layout and visual modifiers
- Use `.interactive()` only for tappable/focusable elements
- Use `glassEffectID` with `@Namespace` for morphing transitions

### Accessibility
- Prefer semantic controls over gesture-only custom controls
- Use Dynamic Type-aware fonts and `@ScaledMetric` for values that should scale
- Mark decorative images as decorative or hidden from accessibility
- Group related content with `accessibilityElement(children:)`
- Provide `accessibilityLabel`, `accessibilityValue`, and `accessibilityHint` when defaults are unclear
- Use dedicated accessibility modifiers instead of deprecated generic `accessibility(...)` variants

## Quick Reference

### Property Wrapper Selection
| Wrapper | Use When |
|---------|----------|
| `@State` | Internal view state (must be `private`) |
| `@Binding` | Child modifies parent's state |
| `@StateObject` | View owns an `ObservableObject` |
| `@ObservedObject` | View receives an `ObservableObject` |
| `@Bindable` | iOS 17+: Injected `@Observable` needing bindings |
| `let` | Read-only value from parent |
| `var` | Read-only value watched via `.onChange()` |

### Liquid Glass Patterns
```swift
// Basic glass effect with fallback
if #available(iOS 26, *) {
    content
        .padding()
        .glassEffect(.regular.interactive(), in: .rect(cornerRadius: 16))
} else {
    content
        .padding()
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
}

// Grouped glass elements
GlassEffectContainer(spacing: 24) {
    HStack(spacing: 24) {
        GlassButton1()
        GlassButton2()
    }
}

// Glass buttons
Button("Confirm") { }
    .buttonStyle(.glassProminent)
```

## Review Checklist

### State Management
- [ ] `@State` properties are `private`
- [ ] New reference-type UI state prefers `@Observable` when supported
- [ ] Root `@Observable` models are stored in `@State`
- [ ] `@Bindable` is used for injected observables that need bindings
- [ ] `@Binding` only where child modifies parent state
- [ ] `@StateObject` for owned, `@ObservedObject` for injected
- [ ] iOS 17+: `@State` with `@Observable`, `@Bindable` for injected
- [ ] Passed values NOT declared as `@State` or `@StateObject`
- [ ] Nested `ObservableObject` avoided (or passed directly to child views)
- [ ] `@FocusState` properties are `private`
- [ ] No redundant `@FocusState` writes inside tap handlers on `.focusable()` views

### Sheets & Navigation (see `references/sheet-navigation-patterns.md`)
- [ ] Using `.sheet(item:)` for model-based sheets
- [ ] Sheets own their actions and dismiss internally

### ScrollView (see `references/scroll-patterns.md`)
- [ ] Using `ScrollViewReader` with stable IDs for programmatic scrolling

### View Structure (see `references/view-structure.md`)
- [ ] Using modifiers instead of conditionals for state changes
- [ ] Avoiding top-level branch swapping when a stable view tree works
- [ ] Complex views extracted to separate subviews
- [ ] Container views use `@ViewBuilder let content: Content`

### Performance (see `references/performance-patterns.md`)
- [ ] View `body` kept simple and pure (no side effects)
- [ ] Passing only needed values (not large config objects)
- [ ] Eliminating unnecessary dependencies
- [ ] State updates check for value changes before assigning
- [ ] Hot paths minimize state updates
- [ ] No object creation in `body`
- [ ] Heavy computation moved out of `body`

### List Patterns (see `references/list-patterns.md`)
- [ ] ForEach uses stable identity (not `.indices`)
- [ ] Constant number of views per ForEach element
- [ ] No inline filtering in ForEach
- [ ] No `AnyView` in list rows

### Layout (see `references/layout-best-practices.md`)
- [ ] Avoiding layout thrash (deep hierarchies, excessive GeometryReader)
- [ ] Gating frequent geometry updates by thresholds
- [ ] Business logic kept in services and models (not in views)
- [ ] Action handlers reference methods (not inline logic)
- [ ] Using relative layout (not hard-coded constants)
- [ ] Views work in any context (context-agnostic)

### Animations (see `references/animation-basics.md`, `references/animation-transitions.md`, `references/animation-advanced.md`)
- [ ] Using `.animation(_:value:)` with value parameter
- [ ] Using `withAnimation` for event-driven animations
- [ ] Transitions paired with animations outside conditional structure
- [ ] Custom `Animatable` has explicit `animatableData` implementation
- [ ] Preferring transforms over layout changes for animation performance
- [ ] Phase animations for multi-step sequences (iOS 17+)
- [ ] Keyframe animations for precise timing (iOS 17+)
- [ ] Completion handlers use `.transaction(value:)` for reexecution
- [ ] iOS 26+: `@Animatable` considered instead of manual `animatableData`

### Accessibility (see `references/accessibility-patterns.md`)
- [ ] Tappable controls use `Button` unless tap location/count is required
- [ ] Text supports Dynamic Type
- [ ] Decorative images are hidden from VoiceOver
- [ ] Related content is grouped intentionally
- [ ] Custom controls expose labels, values, traits, or accessibility representations

### Charts (see `references/charts.md`, `references/charts-accessibility.md`)
- [ ] Files using chart types import `Charts`
- [ ] Chart marks use clear axes, labels, and selection patterns
- [ ] Charts provide VoiceOver summaries or accessible fallback content

### Liquid Glass (iOS 26+)
- [ ] `#available(iOS 26, *)` with fallback for Liquid Glass
- [ ] Multiple glass views wrapped in `GlassEffectContainer`
- [ ] `.glassEffect()` applied after layout/appearance modifiers
- [ ] `.interactive()` only on user-interactable elements
- [ ] Shapes and tints consistent across related elements

## References
- `references/latest-apis.md` - Deprecated-to-modern SwiftUI API transitions
- `references/state-management.md` - Property wrappers and data flow
- `references/view-structure.md` - View composition, extraction, and container patterns
- `references/performance-patterns.md` - Performance optimization techniques and anti-patterns
- `references/list-patterns.md` - ForEach identity, stability, and list best practices
- `references/layout-best-practices.md` - Layout patterns, context-agnostic views, and testability
- `references/mv-patterns.md` - MV-first architectural guidance for SwiftUI refactors
- `references/animation-basics.md` - Core animation concepts, implicit/explicit animations, timing, performance
- `references/animation-transitions.md` - Transitions, custom transitions, Animatable protocol
- `references/animation-advanced.md` - Transactions, phase/keyframe animations (iOS 17+), completion handlers (iOS 17+)
- `references/accessibility-patterns.md` - VoiceOver, Dynamic Type, traits, custom controls
- `references/charts.md` - Swift Charts marks, axes, selection, styling, Chart3D
- `references/charts-accessibility.md` - Accessible chart summaries and fallback content
- `references/sheet-navigation-patterns.md` - Sheet presentation and navigation patterns
- `references/scroll-patterns.md` - ScrollView patterns and programmatic scrolling
- `references/focus-patterns.md` - Focus state, focusable views, and focus pitfalls
- `references/image-optimization.md` - AsyncImage, image downsampling, and optimization
- `references/liquid-glass.md` - iOS 26+ Liquid Glass API
- `references/macos-scenes.md` - Settings, MenuBarExtra, WindowGroup, multi-window
- `references/macos-window-styling.md` - Toolbars, window sizing, and Commands
- `references/macos-views.md` - HSplitView, Table, PasteButton, AppKit interop
- `references/text-patterns.md` - Text initializer selection and localization behavior
- `references/trace-analysis.md` - Instruments trace analysis workflow
- `references/trace-recording.md` - Instruments trace recording workflow

## Philosophy

This skill focuses on **facts and best practices** with a strong default architectural stance:
- We prefer simple MV and Apple-native SwiftUI patterns
- We do not reach for MVVM by default
- We do encourage separating business logic for testability
- We optimize for performance and maintainability
- We follow Apple's Human Interface Guidelines and API design patterns
