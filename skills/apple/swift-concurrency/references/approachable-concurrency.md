## Approachable Concurrency (Swift 6.2)

Use this reference when the project has opted into main-actor-by-default or a
similar approachable concurrency mode.

## Detect it

- Swift language version is 6.2+.
- The target defaults actor isolation to the main actor.
- Strict concurrency level is still relevant; do not ignore it just because the
  code now compiles more easily.

## Expected behavior

- Async functions usually stay on the caller's actor.
- UI code and global mutable state become easier to model safely.
- Some annotations that were previously required can now be simplified.

## How to work in this mode

- Prefer minimal annotations on clearly UI-bound code.
- Use isolated conformances instead of `nonisolated` workarounds.
- Keep shared mutable state on the main actor unless there is a real need to
  run it elsewhere.
- Keep respecting Sendable when values cross actors or tasks.

## Watch-outs

- `Task.detached` ignores inherited actor context.
- Main-actor-by-default can hide performance regressions if expensive work never
  leaves the main actor.
- Do not cargo-cult `@MainActor` everywhere without checking whether the module
  already defaults to it.
