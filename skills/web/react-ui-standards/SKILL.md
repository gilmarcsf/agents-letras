---
name: react-ui-standards
description: "Apply opinionated React and Tailwind UI standards when building components, reviewing UI code, or preventing generic AI-looking interfaces."
user-invocable: true
---

# React UI Standards

Opinionated constraints for React + Tailwind interfaces. Prevents common AI slop patterns.

## Usage

- `/react-ui-standards` — Apply these constraints to UI work in this conversation
- `/react-ui-standards <file>` — Review file against all constraints, output violations with fixes

## Stack

- MUST use Tailwind CSS defaults unless custom values already exist or are explicitly requested
- MUST use `motion/react` (formerly `framer-motion`) when JavaScript animation is required
- SHOULD use `tw-animate-css` for entrance and micro-animations
- MUST use `cn` utility (`clsx` + `tailwind-merge`) for class logic

## Components

- MUST use accessible primitives for keyboard/focus behavior (`Base UI`, `React Aria`, `Radix`)
- MUST use project's existing component primitives first
- NEVER mix primitive systems within the same interaction surface
- SHOULD prefer [`Base UI`](https://base-ui.com/react/components) for new primitives if stack-compatible
- MUST add `aria-label` to icon-only buttons
- NEVER rebuild keyboard/focus behavior by hand unless explicitly requested

## Interaction

- MUST use `AlertDialog` for destructive/irreversible actions
- SHOULD use structural skeletons for loading states
- NEVER use `h-screen`, use `h-dvh`
- MUST respect `safe-area-inset` for fixed elements
- MUST show errors next to where the action happens
- NEVER block paste in `input` or `textarea`

## Animation

- NEVER add animation unless explicitly requested
- MUST animate only compositor props (`transform`, `opacity`)
- NEVER animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`)
- SHOULD avoid animating paint properties (`background`, `color`) except for small UI (text, icons)
- SHOULD use `ease-out` on entrance
- NEVER exceed `200ms` for interaction feedback
- MUST pause looping animations when off-screen
- SHOULD respect `prefers-reduced-motion`
- NEVER introduce custom easing curves unless explicitly requested
- SHOULD avoid animating large images or full-screen surfaces

## Typography

- MUST use `text-balance` for headings and `text-pretty` for body/paragraphs
- MUST use `tabular-nums` for data
- SHOULD use `truncate` or `line-clamp` for dense UI
- NEVER modify `letter-spacing` (`tracking-*`) unless explicitly requested

## Layout

- MUST use a fixed `z-index` scale (no arbitrary `z-*`)
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

## Performance

- NEVER animate large `blur()` or `backdrop-filter` surfaces
- NEVER apply `will-change` outside an active animation
- NEVER use `useEffect` for anything that can be expressed as render logic

## Design

- NEVER use gradients unless explicitly requested
- NEVER use purple or multicolor gradients
- NEVER use glow effects as primary affordances
- SHOULD use Tailwind CSS default shadow scale unless explicitly requested
- MUST give empty states one clear next action
- SHOULD limit accent color usage to one per view
- SHOULD use existing theme or Tailwind color tokens before introducing new ones
