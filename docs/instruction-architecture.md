---
summary: "Where guidance belongs: AGENTS.md, skills, docs, rules, or repo-local instructions."
read_when:
  - Moving guidance out of AGENTS.md.
  - Deciding whether something should become a skill, doc, rule, or local repo instruction.
---

# Instruction Architecture

This repo separates agent guidance by how often it should load and how concrete it is.

## AGENTS.md

Use `AGENTS.md` for rules that should affect nearly every task:

- safety and destructive-action boundaries
- communication preferences
- default execution discipline
- Git and GitHub guardrails
- security constraints
- where to find deeper docs

Keep it short. Codex loads AGENTS files before work starts, so every extra paragraph competes with repo code and the actual task.

## Skills

Use skills for reusable workflows with a recognizable trigger:

- reviewing a PR
- preparing a worktree handoff
- validating a finished change
- using a CLI with local conventions
- debugging a specific platform or toolchain

Skill descriptions are routing text. Keep them short and front-load trigger words. Put detailed workflow steps in `SKILL.md`, and move long references to `references/`.

## Docs

Use docs for rationale and longer reference material:

- engineering principles
- Git conventions
- import and path layout
- examples and templates
- design notes that are useful but not needed in every prompt

Docs are useful when a skill or local AGENTS file points to them. Do not expect agents to discover every doc automatically.

## Rules

Codex rules are for shell permission policy, not writing guidance. Use them only for command allow/prompt/deny behavior. This repo currently keeps that out of scope.

## Where A New Instruction Goes

- Always relevant and safety-critical: `AGENTS.md`
- Repeated task with a clear trigger: skill
- Longer explanation or examples: doc
- Shell permission behavior: rules
- Project-specific source of truth: local repo `AGENTS.md`
