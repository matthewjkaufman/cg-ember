---
name: hub-gate-g-good-morning-no-hub
description: 'CG Ember alone, no Hub: good morning gets the Hub sentence and nothing else.'
tags: [suite, hub-gate]
plugins: ['../../../plugins/cg-ember']
runs: 1
max_turns: 8
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---

good morning
