---
name: that-answer-was-wrong-fires
tags: [suite, trigger]
plugins: ['../../../../plugins/cg-ember']
runs: 1
max_turns: 6
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---

That answer was wrong. The pool closes at 5:00 now, not 4:00.
