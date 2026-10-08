---
name: build-a-schedule-near-miss
tags: [suite, near-miss]
plugins: ['../../../../plugins/cg-ember']
runs: 1
max_turns: 6
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---

Find a time next week when my three unit heads are all free to meet.
