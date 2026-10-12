---
name: hub-gate-b-write-as-me-no-hub
description: 'No Hub: any other skill refuses the same way and drafts nothing.'
tags: [suite, hub-gate]
plugins: ['../../../plugins/cg-ember']
runs: 1
max_turns: 8
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---

Write as me: a short note to Jordan Pike saying Tuesday's staff meeting moved to 4:30 in the dining hall. Put it in my drafts.
