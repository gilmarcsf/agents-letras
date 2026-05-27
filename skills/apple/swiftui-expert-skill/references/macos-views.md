# SwiftUI macOS Views

macOS has SwiftUI views and behaviors that differ from iOS.

## Native Views

- Use `Table` for multi-column tabular data.
- Use `HSplitView` / `VSplitView` for resizable panes.
- Use `PasteButton` for paste workflows when supported.
- Use `Settings` scenes for preferences instead of custom iOS-style settings navigation.

## AppKit Interop

- Use `NSViewRepresentable` only when a native SwiftUI view cannot meet the requirement.
- Keep representables thin. Put behavior in SwiftUI models/services where possible.
- Avoid leaking AppKit details into feature views.

## Layout

- Support resizable windows.
- Avoid assuming full-screen width, compact iPhone spacing, or touch-only interaction.
- Provide keyboard shortcuts for common actions.
