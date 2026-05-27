# SwiftUI Text Patterns

Choose the `Text` initializer intentionally. Some initializers localize automatically, while others render verbatim strings.

## Localized Text

String literals passed to `Text` are localized.

```swift
Text("Settings")
Text("Welcome, \(userName)")
```

## Verbatim Text

Use `Text(verbatim:)` for user-generated strings, identifiers, logs, code, or values that must not be treated as localization keys.

```swift
Text(verbatim: commitHash)
Text(verbatim: userInput)
```

## Rich Text

- Use Markdown in localized strings when it keeps copy maintainable.
- Use `AttributedString` when styling needs to come from data or parsing.
- Keep text composition close to the view unless formatting is business logic.

## Accessibility

- Prefer semantic text styles over fixed sizes.
- Avoid truncation for important information unless there is a way to inspect the full value.
