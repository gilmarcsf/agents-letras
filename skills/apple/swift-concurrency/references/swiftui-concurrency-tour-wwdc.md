# SwiftUI Concurrency Notes

Use this reference when the concurrency question sits inside SwiftUI.

## Main points

- SwiftUI views are usually main-actor-oriented, but some APIs evaluate work
  off the main thread for performance.
- `Shape`, `Layout`, `visualEffect`, and geometry-related closures can require
  `Sendable` thinking even inside SwiftUI.
- Avoid sending `self` into a sendable closure just to read one property;
  capture a value copy instead.

## Working pattern

- Keep action callbacks synchronous and bridge to async work with `Task`.
- Let state be the boundary: async work updates state; the view reacts.
- Move expensive work away from the main actor deliberately.

## Common mistake

- Assuming SwiftUI means everything runs on the main actor all the time.
- It does not. Some closures are modeled as `Sendable` because SwiftUI may run
  them off the main thread.
