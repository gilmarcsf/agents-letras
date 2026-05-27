# SwiftUI Accessibility Patterns

Accessibility is part of the UI contract. Prefer semantic SwiftUI controls and system behavior before adding manual modifiers.

## Controls

- Use `Button` for ordinary tappable actions.
- Use gestures only when the gesture itself matters, such as drag, magnification, long press, or tap location.
- If a custom view acts like a control, expose its role with traits and clear labels.

```swift
Button {
    favorite.toggle()
} label: {
    Label("Favorite", systemImage: favorite ? "star.fill" : "star")
}
.accessibilityValue(favorite ? "On" : "Off")
```

## Dynamic Type

- Use system text styles such as `.headline`, `.body`, and `.caption`.
- Use `@ScaledMetric` for custom sizes that should scale with text size.
- Avoid fixed frames around text unless they can grow.

```swift
@ScaledMetric private var iconSize = 24

Image(systemName: "bell")
    .font(.system(size: iconSize))
```

## Images

- Hide decorative images from VoiceOver.
- Give meaningful images labels.

```swift
Image("background-pattern")
    .accessibilityHidden(true)

Image(systemName: "wifi")
    .accessibilityLabel("Wi-Fi connected")
```

## Grouping

- Group related content when VoiceOver should read it as one item.
- Keep independent controls separate.

```swift
VStack(alignment: .leading) {
    Text(account.name)
    Text(account.balance, format: .currency(code: "USD"))
}
.accessibilityElement(children: .combine)
```

## Custom Controls

- Provide `accessibilityLabel`, `accessibilityValue`, and `accessibilityHint` when visible text is not enough.
- Use `.accessibilityRepresentation` when a custom visualization can map to a standard control.
- Do not use hidden text as an accessibility workaround when a proper modifier is clearer.
