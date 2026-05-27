---
name: web-design-guidelines
description: >-
  Audit web UI code against the latest Vercel Web Interface Guidelines.
  Use when: "vercel web guidelines", "guidelines compliance", "latest web rules",
  "audit this web UI against latest guidelines", "compliance web", "auditar UI web com guideline".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Vercel Web Guidelines Audit

Audit files for compliance with the latest Vercel Web Interface Guidelines.

Use this skill for implementation-level web review: semantics, focus, loading states,
mobile behavior, URL state, layout, content resilience, and other concrete web rules.

Do not use this skill for:

- high-level UX/product critique -> use `ui-audit`
- art direction or visual concept work -> use `frontend-skill`
- React/Tailwind local implementation rules -> use `react-ui-standards`

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use the available web fetch tooling to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.

## Output Contract

- Prefer concrete findings tied to exact files and lines.
- Prioritize correctness, accessibility, resilience, and web behavior over visual taste.
- If the latest remote guideline cannot be fetched, say that explicitly and do not pretend the audit is current.
