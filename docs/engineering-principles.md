---
summary: "Longer engineering defaults behind the compact global AGENTS.md rules."
read_when:
  - Starting non-trivial implementation work.
  - Deciding between simplicity, abstraction, defensive checks, tests, or UI quality tradeoffs.
---

# Engineering Principles

These are the longer-form defaults behind the short global rules.

## Simplicity

- Start with the simplest implementation that works.
- Avoid abstraction by default.
- Add an interface, protocol, generic, or helper only when it removes real complexity or matches an existing pattern.
- Prefer duplication over premature abstraction when the duplicated code is small and clearer inline.
- Delete dead code completely. Do not leave commented-out code, `_unused`, or compatibility breadcrumbs.

## Codebase Fit

- Read surrounding code before changing it.
- Match local style even when another style looks nicer in isolation.
- Reuse existing helpers, module boundaries, error handling, dependency injection, and test patterns.
- Do not introduce new libraries, frameworks, or paradigms unless the task requires it and existing conventions do not cover it.

## Defensive Code

- Put defensive checks at true boundaries: public APIs, external input, persistence, network, CLI input, and user-provided data.
- Avoid internal defensive checks when callers are trusted and local invariants are clear.
- Do not add defensive copies unless data crosses a trust boundary.

## Tests

- Test interesting behavior, not trivial paths.
- Prefer unit tests for pure logic and end-to-end tests for real user flows.
- Avoid mock-heavy tests unless the repo already uses them or a boundary makes them necessary.
- If the implementation supports cancellation, composition, error recovery, concurrency, or migration behavior, test that behavior.

## UI

- Existing design system wins.
- Build the real usable screen, not a marketing placeholder, unless the task is explicitly a landing page.
- Keep operational tools dense, predictable, and scan-friendly.
- Verify responsive layout and text overflow when UI changes are non-trivial.
