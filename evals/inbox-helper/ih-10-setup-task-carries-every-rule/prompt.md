---
name: ih-10-setup-task-carries-every-rule
description: 'Setup creates one scheduled task whose text holds every rule word for word.'
tags: [suite, inbox-helper, inbox-setup]
plugins: ['../../../plugins/cg-ember']
runs: 1
max_turns: 20
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob, Grep]
---

Set up Inbox helper for me. To save you asking: check every three hours from 7 AM to 7 PM on weekdays, and leave alone anything from our owners. I know my notes are in a folder on this computer and that it only runs while the computer is on; that's fine. Yes, set it up.
