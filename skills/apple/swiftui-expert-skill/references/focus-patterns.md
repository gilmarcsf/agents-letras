# SwiftUI Focus Patterns

Use focus state to model keyboard, tvOS, visionOS, and macOS focus explicitly.

## Property Wrapper

- Keep `@FocusState` properties `private`.
- Use `Bool` for one focusable field.
- Use an optional `Hashable` enum for multiple fields.

```swift
private enum Field: Hashable {
    case email
    case password
}

@FocusState private var focusedField: Field?
```

## Text Input

```swift
TextField("Email", text: $email)
    .focused($focusedField, equals: .email)

SecureField("Password", text: $password)
    .focused($focusedField, equals: .password)
```

## Focusable Views

- Use `.focusable()` for custom focusable elements.
- Avoid writing `@FocusState` inside a tap handler attached to the same `.focusable()` view. The focus system already updates focus and redundant writes can cause loops or confusing ordering.
- Prefer `Button` when the view is just an action.
