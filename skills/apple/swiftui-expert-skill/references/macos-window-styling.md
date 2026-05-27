# SwiftUI macOS Window Styling

Use SwiftUI window APIs first. Bridge to AppKit only when SwiftUI lacks the needed behavior.

## Common Patterns

- Use `.toolbar` and `ToolbarItem` for window toolbar actions.
- Use `.windowResizability(...)` to control sizing behavior when supported.
- Use `.defaultSize(...)` for initial window dimensions.
- Use `Commands` for menu bar actions and keyboard shortcuts.

```swift
WindowGroup {
    ContentView()
        .toolbar {
            ToolbarItem {
                Button("Refresh", action: refresh)
            }
        }
}
.defaultSize(width: 900, height: 600)
```

## Review Rules

- Do not hard-code AppKit window mutation in views unless the requirement cannot be met with SwiftUI scene modifiers.
- Keep toolbar actions explicit and testable.
- Prefer adaptive layouts over fixed window-only assumptions.
