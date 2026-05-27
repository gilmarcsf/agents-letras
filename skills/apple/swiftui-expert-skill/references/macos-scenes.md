# SwiftUI macOS Scenes

macOS SwiftUI apps often need scene-level APIs that do not apply to iOS.

## App Scenes

- Use `WindowGroup` for document-like or multi-window app content.
- Use `Settings` for app preferences.
- Use `MenuBarExtra` for menu bar utilities.
- Use `Commands` for menu commands and keyboard shortcuts.

```swift
@main
struct ExampleApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        Settings {
            SettingsView()
        }
    }
}
```

## Guidance

- Keep window creation and app-level commands in the `App` scene layer.
- Keep feature state in models or services, not in the `App` type unless it is truly app-global.
- Use platform availability when sharing code with iOS targets.
