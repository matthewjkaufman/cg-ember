---
name: hub-gate-f-reads-the-hub-not-the-office
description: 'Hub and an office wiki both present: a camp question reads the Hub, never the office wiki.'
tags: [suite, hub-gate]
plugins: ['../../../plugins/cg-ember']
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---

What's our policy on hiring international counselors on J-1 visas? When can they start work?
