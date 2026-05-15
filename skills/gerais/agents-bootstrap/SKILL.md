---
name: agents-bootstrap
description: Create or refresh repo-local AGENTS.md and CLAUDE.md from a compact project-specific template.
---

# Agents Bootstrap

## Overview
Create a project-local `AGENTS.md` from a compact template. This skill owns local agent-instruction bootstrapping. Other bootstrap skills should not generate `AGENTS.md` directly.

The goal is a short, operational repo contract that prevents common wrong moves:
- workflow
- main commands
- source-of-truth files
- architecture boundaries
- repeated decision points
- naming and testing rules that matter in this repo
- validation commands
- a few focused references

Keep it compact, but not timid. Lean does not mean vague. If agents keep making the same mistake in a repo, encode a clear local rule.

## When To Use
- A repo has no local `AGENTS.md` yet.
- A generated or scaffolded repo needs repo-specific agent instructions.
- A repo already has `AGENTS.md`, but it is stale, vague, too generic, or missing source-of-truth guidance.
- You want `CLAUDE.md -> AGENTS.md` as the local single source of truth.

## Required Flow
Do not start by filling the template.

First scan the repo. Then extract evidence-backed facts. Then write `AGENTS.md` from those facts.

The parent agent owns synthesis. Subagents gather evidence. Subagents should not write final sections directly.

## Scan With Subagents
Default to `2-4` subagents max. Use them as evidence buckets, not one agent per final section.

Recommended split:

1. Workflow / Commands
   - Find real entrypoints: `Makefile`, package scripts, Gradle tasks, shell scripts, release commands.
   - Identify the normal dev loop, test loop, build loop, and release path.
   - Identify which commands are wrappers and which commands should not be used by default.

2. Source Of Truth / Architecture
   - Find canonical config files, contracts, schemas, generated sources, and operational ownership boundaries.
   - Map module boundaries and where business rules vs side effects live.
   - Identify the repo's most important anti-patterns or wrong placement traps.

3. Conventions / Validation
   - Find naming rules, file placement rules, test style, validation expectations, and repeated mistakes likely to happen in this repo.
   - Identify what should become hard local rules versus soft references.

Optional 4th bucket:

4. References / Docs
   - Use only when the repo has enough docs that picking the right 2-5 links matters.
   - Select only the docs worth linking from local `AGENTS.md`.

## Subagent Contract
Each scan subagent should return:
- Facts
- Evidence
- Proposed local rules
- Open ambiguities

Prefer this shape:
- Fact: `<what is true in the repo>`
- Evidence: `<file path / command / doc backing it>`
- Proposed rule: `<what should go into AGENTS.md>`
- Ambiguity: `<what still needs a parent decision>`

Examples:
- Fact: `make test` is the normal test entrypoint
- Evidence: `Makefile`, `README.md`
- Proposed rule: `Use make for the normal loop. Do not call gradle directly unless asked.`

- Fact: API schemas are generated from `openapi.yaml`
- Evidence: `scripts/generate.sh`, `docs/backend.md`
- Proposed rule: `Do not edit generated clients directly. Edit openapi.yaml and regenerate.`

Reject generic findings with no repo evidence.

## Parent-Agent Workflow
1. Scan the repo structure yourself first
   - Get enough context to assign the right subagent buckets.
   - Identify likely entrypoints and major docs before delegating.

2. Spawn the scan subagents
   - Give each subagent exact scope and a disjoint evidence bucket.
   - Ask for findings, not prose and not final section drafts.

3. Build a repo inventory
   - Merge the subagent findings into one short internal inventory:
     - entrypoints
     - build/test/release commands
     - source-of-truth files
     - architecture boundaries
     - repeated confusion points
     - candidate hard local rules

4. Write or refresh `AGENTS.md`
   - Start from `templates/AGENTS.md`.
   - Fill only sections backed by repo evidence.
   - Prefer concrete paths, commands, and decisions over generic engineering advice.
   - If the repo needs a stronger local rule than the global file provides, state it directly.

5. Create or refresh `CLAUDE.md`
   - Use `CLAUDE.md -> AGENTS.md` as a symlink when the repo wants a single local source of truth.
   - Do not maintain duplicated content in both files.

6. Validate
   - Re-read the generated file for contradictions, generic filler, or fake specificity.
   - Verify any referenced commands or paths actually exist.
   - Make sure the file is opinionated where it needs to be and silent where it does not.
   - Keep references few and task-driven.

## Local Contract Rules
- Local instructions win over global fallback preferences.
- Do not copy the user's global `~/.agents/AGENTS.md` into the repo.
- Do not dump every architecture note into `AGENTS.md`.
- Do encode the repo-specific rules that repeatedly affect code quality or agent accuracy.
- Naming, testing, source-of-truth, and placement rules are valid local hard rules when they matter in this repo.
- If a section grows long, move details into a focused repo doc and link it from `AGENTS.md`.
- Prefer decision tables when the repo has `2-3` valid patterns that agents often confuse.
- Omit sections that would be generic filler.

## Output Shape
Your local `AGENTS.md` should usually cover:
- `Purpose`
- `Scope`
- `Workflow`
- `Commands`
- `Source Of Truth`
- `Architecture`
- `Decision Tables`
- `Project Conventions`
- `Validation`
- `References`

`Project Conventions` should usually include at least the repo's naming and testing expectations when they are important enough to prevent mistakes.

## Template
- `templates/AGENTS.md`: compact repo-local template with placeholders and section guidance.

## Related Skills
- `android-bootstrap`: scaffold Android apps, but do not create local `AGENTS.md`.
- `kmp-bootstrap`: scaffold KMP apps, but do not create local `AGENTS.md`.
- `create-cli`, `how`, `next-best-practices`, `cloudflare`, etc.: use after local agent bootstrapping when the repo needs deeper domain guidance.
