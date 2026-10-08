---
name: goal-builder-behavior
tags: [suite, behavior]
plugins: ['../../../../plugins/cg-ember']
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
---

Build a goal that checks my email every morning at 7 and drafts replies to new questions from parents.
