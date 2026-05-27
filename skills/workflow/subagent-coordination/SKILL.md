---
name: subagent-coordination
description: "Coordinate Codex sub-agents with exact scope, file ownership, interface contracts, and verification criteria."
---

# Subagent Coordination

Use only when the user explicitly asks for sub-agents, delegation, parallel agents, a swarm, or equivalent.

## When To Delegate

Delegate only when work can proceed in parallel without blocking the parent agent's immediate next step.

Good delegation:

- independent repo exploration questions
- disjoint implementation slices with separate file ownership
- read-only review roles over the same diff
- verification that can run while the parent works elsewhere

Keep local:

- one bug
- one file
- one tight codepath
- urgent blocking work
- work needing constant parent judgment

## Contract Template

Every sub-agent gets:

- exact objective
- read-only or write permission
- owned files or directories
- forbidden files or actions
- expected output shape
- verification criterion
- note that other agents may be editing nearby code

For code changes, require the sub-agent to list changed files in its final answer.

## Parent Duties

- Synthesize child results before spawning more agents.
- Do not blindly paste child output.
- Resolve conflicts and duplicated findings.
- Review uploaded changes before integrating.
- Close sub-agents once no longer needed.
