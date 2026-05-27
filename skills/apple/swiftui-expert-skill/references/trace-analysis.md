# Instruments Trace Analysis Workflow

Use this when the user provides an Xcode Instruments `.trace` file or asks why a SwiftUI flow is slow.

## Workflow

1. Confirm the time range or interaction to inspect.
2. Inspect SwiftUI updates first: body counts, invalidations, and update causes.
3. Check Animation Hitches and hangs for visible stutter.
4. Use Time Profiler to identify expensive symbols in the selected interval.
5. Follow cause graph fan-in to find the state or dependency causing excessive updates.
6. Map findings back to concrete SwiftUI code before proposing changes.

## What To Look For

- Repeated body evaluation from broad observable dependencies.
- State writes in hot paths such as scroll, gesture, timer, publisher, or geometry callbacks.
- Expensive computation or object creation inside `body`.
- List rows with unstable identity or variable view count.
- Animations driven by layout changes instead of transforms.

## Output

Report findings in this order:

1. User-visible symptom.
2. Evidence from the trace.
3. Likely root cause in code.
4. Smallest code change to verify the fix.
5. Follow-up measurement to confirm improvement.
