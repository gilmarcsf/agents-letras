## Swift 6.2 Concurrency Quick Guide

Use this reference when a project is on Swift 6.2+ and concurrency behavior seems
different from Swift 6.0 / 6.1 expectations.

## What changed

- Async functions can stay on the caller's actor by default instead of eagerly
  hopping away.
- Main-actor-by-default / approachable concurrency makes UI-heavy code much
  easier to express safely.
- Isolated conformances reduce friction for protocol conformances on actor-bound
  types.
- Explicit offloading matters more. `async` does not mean "background work".

## Practical implications

- A call from `@MainActor` code to another async function is not automatically a
  background hop.
- Some older data-race errors disappear when default actor isolation protects
  the code already.
- The new risk is performance: CPU-heavy work can accidentally remain on the
  main actor if you never introduce an explicit offload boundary.

## Preferred fixes

- UI-bound code: prefer minimal annotations and let actor isolation do the work.
- Protocol conformances on actor-bound types: prefer isolated conformances such
  as `extension Foo: @MainActor SomeProtocol`.
- Shared mutable state: keep it on `@MainActor` or move it into an `actor`.
- CPU-heavy work: move it into an explicitly offloaded async boundary.

## Questions to answer first

1. Is the module default actor-isolated?
2. Is the code meant to remain UI-bound?
3. Is this a real cross-actor send, or a diagnostic that changes under 6.2?
4. Does the fix preserve performance, not just compile?
