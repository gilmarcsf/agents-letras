---
name: kmp-bootstrap
description: Scaffold, build, test, run, and release Kotlin Multiplatform Android+iOS apps from the command line.
---

# KMP Bootstrap (No Android Studio, No Xcode iteration required)

## Overview
Bootstrap a Kotlin Multiplatform project following the AGP 9 full restructure layout: a pure KMP library (`shared/`) consumed by per-platform application modules (`androidApp/`, `iosApp/`). Compose Multiplatform UI on top. Dev loop runs on `xcrun simctl` for iOS and `adb` for Android — no IDE required for day-to-day work.

## Two-Step Workflow
1) Bootstrap the project folder
   - Run `assets/templates/scripts/bootstrap.sh <AppName> <package.id> [dest-dir]`.
   - Script generates root Gradle + version catalog (AGP 9.2.x, Gradle 9.4.x, Kotlin 2.3.x, Compose MP 1.10.x), writes `shared/` (`com.android.kotlin.multiplatform.library` + `org.jetbrains.compose`) and `androidApp/` (`com.android.application`), copies a vendored `iosApp/` skeleton (xcodeproj under `assets/templates/iosApp/`), writes `Config.xcconfig` Letras-style, wires `version.env`, installs the pre-commit hook, and asks about Koin DI + Apple `DEVELOPMENT_TEAM`.
   - If the repo should carry project-local agent instructions, run `agents-bootstrap` after scaffold. This skill no longer creates `AGENTS.md` directly.

2) Build, run, and release the bootstrapped app
   - Use the `Makefile` at the project root:
     - `make setup` — restore hooks and `agents/openai.yaml`.
     - `make dev-android` — start emulator, install debug APK, launch.
     - `make emulator` — start Android emulator only.
     - `make emulator-cold` / `make emulator-wipe` — explicit Android recovery when snapshots or userdata are bad.
     - `make run-android-emulator` / `make run-android-device` — target emulator vs physical device explicitly.
     - `make run-android-emulator-cold` — cold boot + install + launch in one step.
     - `make dev-ios` / `make run-ios` — boot simulator (or device), build `embedAndSignAppleFrameworkForXcode`, `xcodebuild`, install, launch.
     - `make run-ios-simulator` / `make run-ios-device` — pin to simulator vs physical iPhone explicitly.
     - `make ios-open` — open the Xcode workspace if you want IDE debugging.
     - `make xcframework` — produce a release XCFramework.
     - `make test` — runs `:shared:androidHostTest` + `androidApp:testDebugUnitTest`.
     - `make ios-test` — runs `:shared:iosSimulatorArm64Test` (Intel Mac: `iosX64Test`).
     - `make release` — `bundleRelease` + `assembleSharedXCFramework` + `gh release create` with both artifacts.

## Minimum End-to-End Example
Shortest path from zero to a running app on Android and iOS:
```bash
skills/mobile/kmp-bootstrap/assets/templates/scripts/bootstrap.sh HelloKMP com.example.hellokmp ~/Projects/HelloKMP
cd ~/Projects/HelloKMP

# Android
make setup
make dev-android

# iOS (simulator)
make dev-ios

# Optional: add repo-local agent instructions
# Use the agents-bootstrap skill to create AGENTS.md + CLAUDE.md
```

## Validation Checkpoints

**After bootstrap (`bootstrap.sh`):**
```bash
# Gradle parses
./gradlew --version && ./gradlew help --quiet

# Android build
./gradlew :androidApp:assembleDebug

# iOS framework embeds (needs simulator config env vars)
./gradlew :shared:assembleXCFramework

# Xcode project is valid
plutil -lint iosApp/iosApp.xcodeproj/project.pbxproj
```

**After dev-ios:**
```bash
# App on simulator
xcrun simctl listapps booted | grep -i <BundleID>
```

**After release (`make release`):**
```bash
# AAB signed
jarsigner -verify -verbose androidApp/build/outputs/bundle/release/androidApp-release.aab | tail -5

# XCFramework produced
test -d shared/build/XCFrameworks/release/shared.xcframework

# gh release has both
gh release view v$(grep '^VERSION_NAME=' version.env | cut -d= -f2)
```

## Common Failures
| Symptom | Likely Cause | Recovery |
|---|---|---|
| `com.android.kotlin.multiplatform.library plugin not found` | AGP < 9 or repo missing google() | Confirm AGP 9.2.x + `google()` in settings.gradle.kts |
| `embedAndSignAppleFrameworkForXcode` not found | Xcode build phase running before framework task | Check the "Run Script" build phase in `iosApp.xcodeproj` references the correct Gradle task name |
| `KeyNotFoundException: DEVELOPMENT_TEAM` in Xcode | Empty `TEAM_ID` in `Config.xcconfig` | Set TEAM_ID in `iosApp/Configuration/Config.xcconfig` (or leave blank for simulator-only) |
| `xcrun simctl: no booted simulator` | No simulator running | `scripts/ios_list.sh` to pick one, then `scripts/ios_run.sh <UDID>` |
| `MARKETING_VERSION / CURRENT_PROJECT_VERSION mismatch` | Edited Xcode UI instead of xcconfig | `make sync-version` rewrites `Config.xcconfig` from `version.env` |
| Compose MP version conflict with Compose Compiler plugin | Kotlin plugin version drift | Bump Kotlin + Compose MP in lockstep — see `references/kmp-targets.md` version matrix |

## Templates
- `assets/templates/Makefile`: All targets (`setup`, `dev-android`, `emulator`, `emulator-cold`, `emulator-wipe`, `run-android*`, `dev-ios`, `ios-open`, `xcframework`, test/lint/release, `sync-version`, `clean`).
- `assets/templates/version.env`: Single source of truth for `VERSION_NAME` / `VERSION_CODE` (Android) which `sync_version.sh` mirrors to `MARKETING_VERSION` / `CURRENT_PROJECT_VERSION` (iOS).
- `assets/templates/bootstrap/`: Overlay files — `.editorconfig`, `.gitignore.extras`, `.githooks/pre-commit`, `version.env`.
- `assets/templates/iosApp/`: Vendored iOS app skeleton (Xcode project, Swift sources, asset catalog). Copied in by `bootstrap.sh`; no network fetch.
- `assets/templates/scripts/bootstrap.sh`: Generates Gradle + modules + copies vendored iosApp/; prompts for Koin and Apple DEVELOPMENT_TEAM.
- `assets/templates/scripts/setup.sh`: Restore hooks and local Codex project metadata.
- `assets/templates/scripts/setup_codex_environment.sh`: Create `agents/openai.yaml` when the project does not have one yet.
- `assets/templates/scripts/compile_and_run.sh`: Android dev loop (`:androidApp:assembleDebug`, resolved APK install via `adb -s <serial> install -r`, then launch) with target selection (`any`, `emulator`, `device`). Auto-launches the emulator via `launch.sh` when no Android target is connected and the requested target allows it.
- `assets/templates/scripts/launch.sh`: Start Android emulator with the SDK `emulator` binary, `pm`-based health checks, and explicit `--cold-boot` / `--wipe-data` recovery.
- `assets/templates/scripts/resolve_metadata.sh`: Read Android + iOS version metadata without shelling out to `:androidApp:properties`.
- `assets/templates/scripts/ios_run.sh`: Boot simulator, build iOS app, install, launch.
- `assets/templates/scripts/ios_list.sh`: `xcrun simctl list devices available`.
- `assets/templates/scripts/ios_open.sh`: Open `iosApp.xcworkspace` in Xcode.
- `assets/templates/scripts/build_xcframework.sh`: Produce release XCFramework.
- `assets/templates/scripts/sync_version.sh`: Propagate `version.env` → `Config.xcconfig`.
- `assets/templates/scripts/setup_signing.sh`: Android debug + release keystores.
- `assets/templates/scripts/sign_release.sh`: Sign an AAB.
- `assets/templates/scripts/make_release.sh`: bundleRelease + assembleSharedXCFramework + gh release with both.
- `assets/templates/scripts/build_icon.sh`: Android launcher icons (iOS AppIcon.appiconset is edited in Xcode).

## References
- `references/toolchain.md`: Current AGP/Gradle/Kotlin/Compose Multiplatform defaults and source-of-truth links.
- `references/scaffold.md`: Bootstrap flow — Gradle generation, vendored iosApp skeleton, Koin opt-in.
- `references/kmp-targets.md`: Targets, source sets, `expect/actual`, hierarchy template (`applyDefaultHierarchyTemplate()`).
- `references/kmp-ios.md`: `Config.xcconfig`, `xcrun simctl`, `xcodebuild`, `embedAndSignAppleFrameworkForXcode`, SwiftPM/SPM consumption.
- `references/ktlint.md`: JLLeitschuh plugin + CLI pre-commit hook; applies across all KMP source sets.
- `references/testing.md`: `commonTest` with `kotlin.test`, Android host tests, optional iOS simulator tests, MockK guidance, Turbine for Flow.
- `references/packaging.md`: AAB (`:androidApp:bundleRelease`), XCFramework (`:shared:assembleSharedXCFramework`), framework embedding via `embedAndSignAppleFrameworkForXcode`.
- `references/release.md`: `gh release create` with AAB + XCFramework; future `.ipa` is out of bootstrap scope.

## Related Skills (do not duplicate)
- `agents-bootstrap`: Create repo-local `AGENTS.md` + `CLAUDE.md` after scaffold when the project needs local agent instructions.
- `android-bootstrap`: Android-only projects. Use it when iOS target is not needed.
- `android-cli`: `android *` subcommand reference. Used by this skill for Android SDK/emulator.
- `android-emulator-qa`: Validating Android flows via adb.
- `agp-9-upgrade`: Upgrading an existing Android/KMP project to AGP 9 (bootstrap already targets AGP 9).
- `edge-to-edge`, `navigation-3`, `r8-analyzer`, `migrate-xml-views-to-jetpack-compose`: Follow-ups.
- `kotlin-tooling-cocoapods-spm-migration` (upstream Kotlin skill): CocoaPods → SPM migration for KMP iOS integration. Load when you want SPM export.

## Notes
- **Layout = AGP 9 full restructure**: `shared/` (pure KMP lib) + `androidApp/` (Android app depending on `:shared`) + `iosApp/` (Xcode project). Not the monolithic `composeApp/` pattern from the older KMP wizard.
- **Defaults**: JDK 21, minSdk 26 (Android 8), compileSdk 36, Kotlin 2.3.x, AGP 9.2.x, Gradle 9.4.x, Compose Multiplatform 1.10.x. iOS targets: `iosX64 + iosArm64 + iosSimulatorArm64`. Framework `baseName = "shared"`, static.
- **No ktor, no Firebase by default**: bootstrap is minimal. Add networking/Firebase as follow-up based on app needs.
- **iosApp skeleton is vendored**: fully local under `assets/templates/iosApp/`. No network fetch during bootstrap; no xcodegen dependency.
- **Koin**: opt-in via bootstrap prompt (default: no). If yes, installs `koin-core` (common), `koin-android`, `koin-compose`, and Android startup wiring. Add iOS startup only when the app has real shared dependencies to initialize.
- **Version sync is one-way**: edit `version.env`, run `make sync-version`, commit. `Config.xcconfig` is the computed artifact.
- **Local agent instructions are separate**: bootstrap does not create `AGENTS.md` directly. Use `agents-bootstrap` when the repo should carry local agent instructions, and do not copy the user's global `~/.agents/AGENTS.md` into the repo.
- **Local Codex project metadata**: `make setup` creates `agents/openai.yaml` if the repo does not already define one.
- **Release = AAB + XCFramework only**: `.ipa` requires Apple signing + provisioning and is out of bootstrap scope. See `references/release.md`.
- **Desktop/web targets not in scope**: this skill is for Android + iOS only. Add `desktopApp/`/`webApp/` by hand if needed, or use a separate skill.
- **Android emulator health**: treat boot props plus successful `pm` queries as readiness; if warm boot is unhealthy, use the cold-boot / wipe-data targets instead of `installDebug`.
