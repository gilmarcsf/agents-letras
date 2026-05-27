---
name: product-ui-direction
description: >-
  Turn a fuzzy product brief into a concrete UI direction before implementation. Use when the product,
  feature, app screen, dashboard, or landing page needs a clear category, operating mode, interface
  pattern, style family, palette direction, typography character, interaction intensity, anti-patterns,
  and delivery checklist. Complements `frontend-skill` by choosing the right product direction before
  art direction and execution.
---

# Product UI Direction

Use this skill when the hard question is not "how do I code this?" but "what kind of interface should this product become?"

This skill complements `frontend-skill`:

- `product-ui-direction` decides product fit, operating mode, UI pattern, style family, and anti-patterns
- `frontend-skill` executes the chosen direction with strong composition and motion

Skip this skill for pure backend work, non-visual automation, infrastructure tasks, or performance work that does not change how the interface looks, feels, moves, or is used.

## Output

Produce a compact but complete UI direction with:

1. product category
2. product mode
3. primary pattern
4. supporting sections or surface areas
5. style family
6. color direction
7. typography direction
8. interaction and motion intensity
9. anti-patterns
10. pre-delivery checklist

## Workflow

1. Classify the product with `references/product-categories.md`.
2. Decide the operating mode with `references/product-modes.md`.
3. Choose the right pattern with `references/pattern-families.md`.
4. Pick a style family with `references/style-families.md`.
5. Set palette and typography direction from product mood, trust level, and content density, not trend bias.
6. Set motion intensity from the core job: conversion, scanning, exploration, creation, or data work.
7. List anti-patterns specific to the domain.
8. End with a concrete implementation brief the execution skill can follow.

## Product Modes

- **High-trust**: banking, healthcare, legal, security, government. Bias to clarity, credibility, calm hierarchy, explicit affordances.
- **Operational**: dashboards, admin, analytics, internal tools. Bias to scanability, density, utility copy, durable structure.
- **Expressive**: creative tools, media, music, fashion, lifestyle. Bias to stronger visual identity, but keep one clear operating model.
- **Editorial**: publishing, storytelling, brand campaigns, portfolios. Bias to rhythm, pacing, image treatment, typography voice.

If two modes seem valid, choose the one that governs the user's main job, then borrow carefully from the second.

## Deliverable Shape

Write the result in this structure:

- Product category
- Product mode
- Primary pattern
- Suggested section order or surface layout
- Style family
- Color direction
- Typography direction
- Motion direction
- Anti-patterns to avoid
- Delivery checklist

## Guardrails

- Do not jump straight to colors or fonts before deciding operating mode and pattern.
- Do not recommend the same style family for every product type.
- High-trust products should not look like experimental AI demos.
- Operational tools should not be dressed like marketing landing pages.
- Expressive products can push identity harder, but still need usability and hierarchy.
- Anti-patterns are mandatory output, not optional garnish.
- Use real product surfaces, screenshots, data, or examples when the execution phase needs visual proof.
- Keep motion purposeful: state changes, continuity, feedback, or guided discovery. Avoid decorative animation that slows the task.
- Delivery checklists must include accessibility, responsive behavior, interaction states, and reduced-motion expectations.
