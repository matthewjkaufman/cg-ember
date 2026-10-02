# CG Ember

CG Ember is a plugin for Claude made for people who run summer camps. A **plugin** is a
bundle of skills you add to Claude. A **skill** is a written page of instructions Claude
follows for one job.

It works in Claude Cowork and in Claude chat, on any paid Claude plan.

## What it does

Say these in your own words. You do not need the exact phrase.

| Say | What happens |
|---|---|
| "Set me up" | Claude walks you through connecting Gmail, Google Drive and Google Calendar, what Claude asks you before it acts, and your own notes folder. It asks first whether your camp is okay with connecting, and waits if you are not sure. One step at a time, about fifteen minutes. |
| "Good morning" | Claude reads your notes and tells you where you left off. For the rest of that conversation, it also saves your place as you go. |
| "Wrap up" | Claude saves your place and what you did today. |
| "Share this skill" | Claude packages a skill you built and sends it to Matt to review, but only after you say yes. If he approves it, every camp using CG Ember gets it. |
| "Explain that" | Claude explains a word, what it just did, or how to ask for something better, in plain words. |

Your notes live in a folder called **My work** in your own Google Drive: About me, My
camp, My jobs, and What I did this week. They are private to you unless you share them.
Claude keeps campers' and families' private details out of them.

## Installing it

1. In Claude Cowork, click **Cowork** on the left, then click **Customize**. In Claude
   chat, just click **Customize**.
2. Click **Plugins**, then **Add**, then **Add marketplace**.
3. Choose **Add from a repository**. A pink box says Anthropic does not control plugins
   added this way. That is expected here.
4. Paste in `matthewjkaufman/cg-ember` (copy it from this page or from the email it came
   in, rather than typing it), and click **Sync**.
5. Install **cg-ember** from the list.
6. Start a new conversation and say **"set me up."**

## Changing a skill

When CG Ember updates, it replaces its own skills, so a change made inside one of them
would disappear. To make one work differently, say **"make my own copy"** of it. Claude
makes a copy with a new name that is yours to change, walks you through adding it, and
updates never touch it.

## Built a skill other camps could use?

Say **"share this skill."** Matt reviews every shared skill by hand. Other camps get the
instructions with no name or camp on them.

The Hub is the website where camps in the group share the skills they build. Only people
at those camps can sign in to it. There, your name is shown as the person who made the
skill.

---

## For the maintainer

- Layout: `.claude-plugin/marketplace.json` lists one plugin, `plugins/cg-ember/`, whose
  skills are one folder each under `plugins/cg-ember/skills/<name>/SKILL.md`.
- Every skill uses the shared SKILL.md format (a `name` and `description` at the top, plain
  instructions below), so the same files can be packaged for OpenAI Codex later.
- Approved shared skills are committed here by the Hub, which also raises the patch number
  of `version` in `plugins/cg-ember/.claude-plugin/plugin.json`. The Hub never changes the
  five skills above, the manifests other than that number, or this readme.
- The connection to the Hub (`plugins/cg-ember/.mcp.json`) is added in the first version
  after the Hub's connection answers with sign-in working.
- Nothing in this repository may name the company that owns it, a camp, or the person who
  made a skill. Run `grep -rliE "camp[g]roup" .` before every push; it must print nothing.
- American spelling, no dashes joining two thoughts, "child" or "camper" and never the
  slang word, in every file.
