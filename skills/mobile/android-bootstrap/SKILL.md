---
name: android-bootstrap
description: Scaffold, build, test, run, and package Kotlin/Compose Android apps from the command line.
---

# Android Bootstrap (No Android Studio)

## Overview
Bootstrap a Kotlin + Jetpack Compose Android app folder using the `android` CLI, overlay ktlint + tests + dev scripts, then build, run, and release without Android Studio. Uses `assets/templates/bootstrap/` for the overlay files, `assets/templates/scripts/` for dev loop scripts, and `references/` for details. See the `android-cli` skill for the underlying CLI commands.

## Two-Step Workflow
1) Bootstrap the project folder
   - Run `assets/templates/scripts/bootstrap.sh <AppName> <package.id>`.
   - Script runs `android create`, pins the Gradle wrapper to the current AGP-compatible Gradle line, enables Gradle configuration cache in `gradle.properties`, copies the overlay, patches `build.gradle.kts` (JDK 21, minSdk 26, ktlint, MockK, Turbine), wires `version.env`, installs the pre-commit hook, and asks about optional add-ons (Koin DI, multi-module split).
   - If the repo should carry project-local agent instructions, run `agents-bootstrap` after scaffold. This skill no longer creates `AGENTS.md` directly.

2) Build, run, and release the bootstrapped app
   - Use the `Makefile` at the project root:
     - `make setup` — restore hooks and `agents/openai.yaml`.
     - `make dev` — start emulator, install debug, launch app.
     - `make emulator` — start emulator only.
     - `make emulator-cold` / `make emulator-wipe` — explicit recovery when snapshots or userdata are bad.
     - `make run-emulator` / `make run-device` — target emulator vs physical device explicitly.
     - `make run-emulator-cold` — cold boot + install + launch in one step.
     - `make test` / `make android-test` — unit + instrumented tests.
     - `make lint` / `make format` — ktlint.
     - `make release` — `bundleRelease` + sign + `gh release create` with the AAB.
   - Or call scripts directly: `scripts/setup.sh`, `scripts/launch.sh`, `scripts/compile_and_run.sh --target emulator|device`, `scripts/sign_release.sh`, `scripts/make_release.sh`.

## Minimum End-to-End Example
Shortest path from zero to a running app:
```bash
# 1. Bootstrap a new project
skills/mobile/android-bootstrap/assets/templates/scripts/bootstrap.sh HelloApp com.example.hello ~/Projects/HelloApp
cd ~/Projects/HelloApp

# 2. Dev loop
make setup
make dev

# 3. Optional: add repo-local agent instructions
# Use the agents-bootstrap skill to create AGENTS.md + CLAUDE.md
```

## Validation Checkpoints

**After bootstrap (`bootstrap.sh`):**
```bash
# Confirm overlay applied
test -f .editorconfig && test -f version.env && test -x .githooks/pre-commit

# Confirm Gradle wrapper works
./gradlew --version
```

**After first build (`make build`):**
```bash
# Confirm debug APK produced
ls app/build/outputs/apk/debug/*.apk
```

**After release bundle (`make release` or `scripts/sign_release.sh`):**
```bash
# Inspect AAB signature
jarsigner -verify -verbose -certs app/build/outputs/bundle/release/app-release.aab | tail -5

# Confirm applicationId, versionCode, versionName match version.env
./scripts/resolve_metadata.sh
```

## Common Failures
| Symptom | Likely Cause | Recovery |
|---|---|---|
| `Failed to install the following Android SDK packages` | Missing platform/build-tools | `android sdk install platforms;android-36 build-tools;36.0.0` |
| `Could not find tools.jar` or JDK errors | JDK < 21 or `JAVA_HOME` unset | Install JDK 21 (`sdk install java 21-tem`), set `JAVA_HOME` |
| `ktlintCheck` fails on generated files | ktlint inspecting `build/` | Confirm `.editorconfig` and build.gradle.kts `ktlint { filter { exclude { ... } } }` exclude generated sources |
| `INSTALL_FAILED_INSUFFICIENT_STORAGE` on emulator | AVD full | `adb shell pm uninstall <pkg>` or recreate AVD with more storage |
| `KeyStore was tampered with, or password was incorrect` | Release keystore password mismatch | Check `KEYSTORE_PASSWORD` + `KEY_PASSWORD` env vars match keystore |
| Pre-commit hook not firing | `core.hooksPath` not set | `git config core.hooksPath .githooks` |
| `gh release create` fails | Not authenticated | `gh auth login` |
| `make dev` says the emulator is ready, then install or tests fail with `device is still booting` or `Can't find service: package` | Boot checks are too weak or the snapshot is unhealthy | Wait for `sys.boot_completed=1`, `dev.bootcomplete=1`, `init.svc.bootanim=stopped`, plus successful `pm` queries; if installs still fail, retry with `make emulator-cold`, then `make emulator-wipe` |
| Emulator exits when launched through `android emulator start` | CLI wrapper is not durable enough for automation on some machines | Start the SDK `emulator` binary directly and background that process |
| `make dev` looks stuck and `adb devices` shows `unauthorized` | ADB key auth is broken, not Android boot | Export `ADB_VENDOR_KEYS="$HOME/.android"`, run `adb kill-server && adb start-server`, then accept the RSA prompt in the emulator |
| App installs but does not open | Launcher uses `monkey` instead of the resolved activity | Resolve the activity with `cmd package resolve-activity --brief <appId>` and start it with `am start -W -n <activity>` |

## Templates
- `assets/templates/Makefile`: All dev loop targets (`setup`, `dev`, `emulator`, `emulator-cold`, `emulator-wipe`, `run`, `run-emulator`, `run-emulator-cold`, `run-device`, build/test/lint/release).
- `assets/templates/version.env`: App version file consumed by Gradle build + release scripts.
- `assets/templates/bootstrap/`: Overlay files applied on top of `android create` output — `.editorconfig`, `.gitignore` additions, `.githooks/pre-commit`, unit + UI test examples.
- `assets/templates/scripts/bootstrap.sh`: Runs `android create`, applies overlay, patches build files, installs hooks.
- `assets/templates/scripts/setup.sh`: Restore hooks and local Codex project metadata.
- `assets/templates/scripts/setup_codex_environment.sh`: Create `agents/openai.yaml` when the project does not have one yet.
- `assets/templates/scripts/compile_and_run.sh`: Dev loop — `assembleDebug`, install the resolved APK with `adb -s <serial> install -r`, then launch on a selected target (`any`, `emulator`, `device`).
- `assets/templates/scripts/launch.sh`: Start emulator only, using the SDK `emulator` binary, `pm`-based health checks, and explicit `--cold-boot` / `--wipe-data` recovery.
- `assets/templates/scripts/resolve_metadata.sh`: Read `applicationId`, `versionCode`, and `versionName` from project metadata without shelling out to `:app:properties`.
- `assets/templates/scripts/build_icon.sh`: Generate `ic_launcher` densities from a 1024x1024 PNG (requires ImageMagick).
- `assets/templates/scripts/setup_signing.sh`: Create debug + release keystores.
- `assets/templates/scripts/sign_release.sh`: Sign a release AAB.
- `assets/templates/scripts/make_release.sh`: `bundleRelease` + sign + `gh release create` with the AAB.

## References
- `references/toolchain.md`: Current AGP/Gradle/Kotlin/Compose defaults and source-of-truth links.
- `references/scaffold.md`: `android create` + overlay mechanics, Koin opt-in, multi-module split.
- `references/ktlint.md`: JLLeitschuh Gradle plugin + ktlint CLI pre-commit hook + `.editorconfig`.
- `references/testing.md`: JUnit 4 + MockK + Turbine + Compose UI tests (`createAndroidComposeRule`).
- `references/packaging.md`: APK vs AAB, `assembleDebug`, `assembleRelease`, `bundleRelease`.
- `references/release.md`: Keystore creation, signing config, `gh release create` with AAB.

## Related Skills (do not duplicate)
- `agents-bootstrap`: Create repo-local `AGENTS.md` + `CLAUDE.md` after scaffold when the project needs local agent instructions.
- `android-cli`: All `android *` subcommand usage — consult it for SDK install, emulator, run, docs.
- `android-emulator-qa`: Validating feature flows via adb with screenshots and logcat.
- `agp-9-upgrade`: Upgrading an existing project to AGP 9 (bootstrap already targets AGP 9).
- `edge-to-edge`, `navigation-3`, `r8-analyzer`, `play-billing-library-version-upgrade`, `migrate-xml-views-to-jetpack-compose`: Follow-ups after bootstrap.

## Notes
- Defaults: JDK 21, minSdk 26 (Android 8.0), compileSdk 36, Kotlin 2.3.x, AGP 9.2.x, Gradle 9.4.x, Compose BOM 2026.04.x, Material 3, single-module `:app`.
- Generated projects enable `org.gradle.configuration-cache=true` by default for a faster repeat build loop.
- `bootstrap.sh` prompts interactively for Koin DI and multi-module split; both default to "no".
- Generated projects do not create `AGENTS.md` directly anymore. Use `agents-bootstrap` when the repo should carry local agent instructions, and do not copy the user's global `~/.agents/AGENTS.md` into the repo.
- Generated projects also create `agents/openai.yaml` via `make setup`. Keep that file as the local Codex project interface contract.
- Release uses AAB (`bundleRelease`) for Play Store compatibility. Universal APKs can be produced separately via `bundletool` if needed.
- `version.env` drives `versionCode` and `versionName` in `app/build.gradle.kts` — edit the file, rebuild.
- Pre-commit hook runs ktlint CLI directly (not Gradle) for speed; the Gradle plugin covers CI.
- For generated `make dev` flows, treat emulator readiness as boot props plus a healthy package manager: `sys.boot_completed`, `dev.bootcomplete`, `bootanim`, `pm path android`, and `pm list packages`.
- For generated launch scripts, prefer warm boot first, then use explicit cold boot / wipe-data recovery when snapshots or userdata are unhealthy.
- For generated launch scripts, prefer the SDK emulator binary and `am start -W` over the `android emulator start` wrapper and `monkey`.
- For generated adb-based scripts, export `ADB_VENDOR_KEYS="$HOME/.android"` and fail fast on `unauthorized` instead of looking like a boot hang.
