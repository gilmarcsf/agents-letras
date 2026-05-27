# Material 3

Vendored from [hamen/material-3-skill](https://github.com/hamen/material-3-skill) (MIT). Comprehensive Material Design 3 / Material You reference for Claude Code — tokens, components, theming, layout, and MD3 compliance audit.

## Purpose
Guide MD3-compliant UI generation across three stacks with clear primacy:

| Platform | Role | Notes |
|---|---|---|
| Jetpack Compose | **Primary** | `MaterialTheme`, Material3 composables, adaptive layouts, edge-to-edge/insets, M3 Expressive where available |
| Flutter | Secondary | `ThemeData(useMaterial3: true)`, `ColorScheme.fromSeed`, community packages for dynamic color |
| Web (`@material/web`) | Limited | [In maintenance mode](https://m3.material.io/develop/web); no M3 Expressive parity |

## Modes (via `argument-hint`)
- `component <desc>` — build an MD3 component
- `theme <seed-color or brief>` — generate a theme
- `layout` / `scaffold <desc>` — responsive shell + navigation
- `audit [path|url]` — score against 10 MD3 categories (color, type, shape, elevation, components, layout, navigation, motion, a11y, theming) and propose fixes. Works on Compose/Kotlin, Flutter/Dart, web/CSS

## Relationship to other skills
- `android-bootstrap`, `kmp-bootstrap` — these scaffold Compose/Compose-MP apps; use `material-3` *after* scaffolding to style them
- `migrate-xml-views-to-jetpack-compose` — migration step; apply `material-3` as the new UI comes in
- `edge-to-edge` — MD3 requires edge-to-edge; that skill covers the insets mechanics
- `swiftui-*` — unrelated (SwiftUI, not MD3)

## Upstream updates
```bash
gh repo clone hamen/material-3-skill /tmp/m3 -- --depth 1
rsync -a --delete \
  --exclude='.git' --exclude='CONTRIBUTING.md' --exclude='assets/m3-hero.png' \
  /tmp/m3/ ~/Developer/agents/skills/material-3/
# Preserve local agents/openai.yaml + this README by restoring after rsync, or use --exclude above.
```

Keep `LICENSE` intact (MIT, © Mattia Hamen).
