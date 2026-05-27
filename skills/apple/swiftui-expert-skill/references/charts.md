# Swift Charts Reference

Use Swift Charts for native, accessible chart rendering. Files using chart types must import `Charts`.

```swift
import Charts
```

## Basic Chart

```swift
Chart(sales) { sale in
    BarMark(
        x: .value("Month", sale.month),
        y: .value("Revenue", sale.revenue)
    )
}
```

## Selection

- Use chart selection APIs when the deployment target supports them.
- Keep selected values in local `@State`.
- Show selected values outside the chart when VoiceOver or small screens need a clearer representation.

## Styling

- Prefer system colors and semantic foreground styles.
- Keep axes readable; hide axes only when labels or surrounding UI preserve meaning.
- Avoid encoding meaning with color alone.

## Chart3D

- Use 3D charts only when depth communicates real data.
- Provide a 2D or textual fallback when 3D would reduce readability or accessibility.
