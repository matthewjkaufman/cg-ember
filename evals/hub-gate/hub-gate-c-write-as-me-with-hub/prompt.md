---
name: hub-gate-c-write-as-me-with-hub
description: 'Hub connected: the skill checks the Hub, then works.'
tags: [suite, hub-gate]
plugins: ['../../../plugins/cg-ember']
runs: 1
max_turns: 14
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
---

Write as me: a short note to Jordan Pike saying Tuesday's staff meeting moved to 4:30 in the dining hall. Put it in my drafts.
