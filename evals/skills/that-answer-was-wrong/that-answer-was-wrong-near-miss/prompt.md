---
name: that-answer-was-wrong-near-miss
tags: [suite, near-miss]
plugins: ['../../../../plugins/cg-ember']
runs: 1
max_turns: 6
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---

Fix the typo in this sentence: 'Teh pool closes at five.'
