# SwiftUI Latest APIs Reference

Use this reference before implementation or review. Prefer the newest SwiftUI API that fits the project deployment target, and gate newer APIs with `#available` when needed.

## Common Replacements

| Older pattern | Prefer |
|---------------|--------|
| `.animation(_:)` | `.animation(_:value:)` |
| Gesture-only taps for controls | `Button` |
| `NavigationView` | `NavigationStack` or `NavigationSplitView` |
| Boolean-only sheets for model data | `.sheet(item:)` |
| `ObservableObject` for new iOS 17+ state | `@Observable` with `@State` / `@Bindable` |
| Manual `animatableData` on iOS 26+ | `@Animatable` when supported |
| Generic deprecated accessibility modifier forms | Dedicated modifiers such as `.accessibilityLabel`, `.accessibilityValue`, `.accessibilityHint` |

## Review Rules

- Check compiler deprecation warnings before inventing custom replacements.
- Prefer SwiftUI-native components before bridging to UIKit or AppKit.
- Keep fallbacks simple and scoped to the availability boundary.
- Do not introduce a newer API when the project deployment target cannot support it and a fallback would add more complexity than value.

## iOS 26+ Notes

- Use native Liquid Glass APIs only when requested or when the app already adopts the design language.
- Prefer `@Animatable` for custom animation state when the deployment target allows it.
- Keep iOS 26 APIs inside availability gates unless the package or target baseline is already iOS 26+.
