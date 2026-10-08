---
name: goal-builder-fires
tags: [suite, trigger]
plugins: ['../../../../plugins/cg-ember']
runs: 1
max_turns: 6
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---

I have about 60 counselor applications in a folder. Work through the whole list, check each one has two references, and keep going until it's done.
