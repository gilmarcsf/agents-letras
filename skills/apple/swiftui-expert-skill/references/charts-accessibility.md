# Swift Charts Accessibility

Charts need meaningful non-visual summaries. Do not assume VoiceOver can infer the intended comparison from marks alone.

## Checklist

- Provide a short summary of what the chart shows.
- Surface the most important trend, min, max, or selected value in text.
- Avoid color-only encoding.
- Use accessible labels for custom legends and controls.
- Keep chart interactions reachable by keyboard and VoiceOver when possible.

## Pattern

```swift
VStack(alignment: .leading) {
    Text("Revenue increased from January to March.")
        .font(.caption)

    Chart(values) { value in
        LineMark(
            x: .value("Month", value.month),
            y: .value("Revenue", value.revenue)
        )
    }
    .accessibilityLabel("Monthly revenue chart")
    .accessibilityValue("Revenue increased from January to March")
}
```
