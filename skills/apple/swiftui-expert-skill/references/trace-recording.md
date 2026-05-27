# Instruments Trace Recording Workflow

Use this when the user asks to record or profile a SwiftUI app.

## Choose The Recording Mode

- Attach to a running process when the app is already in the target state.
- Launch under Instruments when startup behavior matters.
- Record all processes only when cross-process work is part of the symptom.

## Template Choice

- Use the SwiftUI template for real devices or host Mac SwiftUI apps.
- Use Time Profiler for iOS Simulator when the SwiftUI template is unavailable or insufficient.
- Add Animation Hitches when the symptom is stutter.

## Before Recording

- Identify the exact interaction to perform.
- Keep the recording short and focused.
- Record device, OS, app build, and target screen.

## After Recording

- Save the trace path.
- Note the time range that contains the reproduced symptom.
- Analyze before editing code.
