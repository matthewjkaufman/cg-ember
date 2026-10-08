# CG Ember

CG Ember is a plugin for Claude made for people who run summer camps. A **plugin** is a
bundle of skills you add to Claude. A **skill** is a written page of instructions Claude
follows for one job.

It works in Claude Cowork and in Claude chat, on any paid Claude plan.

**It never sends anything.** Emails, messages and invitations come out as drafts, waiting
in your drafts. You read them and you press send.

## What it does

Say these in your own words. You do not need the exact phrase.

| Say | What happens |
|---|---|
| **Getting started** | |
| "Set me up" | Claude connects your email, files and calendar, and makes your Personal Notes. It asks first whether your camp is okay with connecting. About twenty minutes, one step at a time. |
| "Show me what I can say" | Claude lists what you can ask for and suggests one to try first. |
| "What's new" | Claude tells you what changed since the last update. |
| "Explain that" | Claude explains a word, or what it just did, in plain words. |
| **Every day** | |
| "Good morning" | Claude tells you where you left off. |
| "Wrap up" | Claude saves your place and what you did today. |
| "Prep me for my meeting" | Claude gives you a one-screen brief before you walk in. |
| "Set up Inbox helper" | Claude drafts replies for you during the day. See below. |
| **Writing** | |
| "Write as me" | Claude drafts a message in your own voice, in your drafts. |
| "Build my writing styles" | Claude learns how you write, from a few emails you already sent. |
| "Is this clear?" | Claude reads your writing as the person receiving it would. |
| **Your camp's questions** | |
| "Look it up" | Ask anything about your camp. Claude answers from what is written down, says where it came from, and never guesses. |
| "That answer was wrong" | Claude fixes it in your Personal Notes and tells whoever looks after that wiki page. |
| **Sharing** | |
| "Share this skill" | Claude shares a skill you built for review, only after you say yes. See the end of this page. |

Claude may also ask you one quick question a day about how your camp works. Never more
than one.

## Where answers come from

Claude looks in three places, in this order:

1. **Personal Notes** are yours and private. They live in your Google Drive, on the Hub,
   or in a folder on your computer, wherever you choose at setup. (An older **My work**
   folder still works.)
2. **Camp Wiki** is what your camp has written down. It lives on the Hub.
3. **CG Knowledge Base** is what every camp in the group shares. It lives on the Hub too.

The **Hub** is the website where camps in the group keep these. The Camp Wiki and CG
Knowledge Base work once your camp is on the Hub. Until then, Claude uses your Personal
Notes and your files.

Nothing moves from your notes to a wiki unless you say yes, and the wiki's approver
decides. Claude keeps campers' and families' private details out of all three.

## Inbox helper

Say **"set up Inbox helper"** and, every few hours, Claude reads your new email.

- When your notes and wikis fully answer an email, it writes a reply and leaves it in your
  drafts.
- It lists the rest for you and writes nothing to anyone.
- Once a day, it asks you about a question people keep asking, so the next one gets a
  draft.

It never sends. If your notes are in a folder on your computer, it only runs while the
computer is on.

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
instructions with no name or camp on them. On the Hub, which only people at the group's
camps can sign in to, your name is shown as the person who made the skill.

---

## For the maintainer

- Layout: `.claude-plugin/marketplace.json` lists one plugin, `plugins/cg-ember/`, whose
  skills are one folder each under `plugins/cg-ember/skills/<name>/SKILL.md`.
- Every skill uses the shared SKILL.md format (a `name` and `description` at the top, plain
  instructions below), so the same files can be packaged for OpenAI Codex later. Keep each
  description under 400 characters and all of them together under 6,500.
- Approved shared skills are committed here by the Hub, which also raises the patch number
  of `version` in `plugins/cg-ember/.claude-plugin/plugin.json`. The Hub never changes the
  skills that ship with the plugin (every folder it did not publish is reserved), the
  manifests other than that number, or this readme.
- The connection to the Hub (`plugins/cg-ember/.mcp.json`) is added in the first version
  after the Hub's connection answers with sign-in working. Until then every Hub step in
  the skills stays silent.
- `plugins/cg-ember/hooks/hooks.json` refuses send-shaped tools on any connection, and
  calendar events with guests. Its commands are POSIX shell (Cowork runs them on Linux,
  Claude Code on Windows runs them in Git Bash); Windows PowerShell cannot parse them, so
  there they would not block. The written rule in every skill is the control that holds
  either way. Run `bash tests/send-block.test.sh` after any change to it.
- Test questions live in `evals/` (see `evals/README.md`). From the repository root:
  `claude plugin eval . --tag suite --runs 1 --scaffold --allow-tools Write Edit
  --judge-model sonnet --max-cost-usd 15`. The `control` case is left out of that run on purpose; it must fail.
- The send block also refuses a few tools that only make drafts (for example a
  `draft_reply` or `createReply` on some email connections), because their names look like
  sending. That is deliberate: those drafts then appear in the conversation instead.
- Two kinds of tool are let through by exact name, at the front of the send matcher. A
  `send_feedback` tool (any letter case, with `_`, `-`, `.` or nothing between the words)
  files a note inside the person's own work system and reaches nobody outside it. A
  `createScheduledPost` or `createScheduledPostForReview` tool (or `create_scheduled_post`,
  `create_scheduled_post_for_review`) puts a post in the queue of the person's own
  scheduling tool, where they can read, change or cancel it before it goes out. Anything
  longer or prefixed (`send_feedback_email`, `gmail_send_feedback`, `createScheduledPostNow`),
  any tool that posts or publishes at once, and changing or sending on an already queued post
  are still refused. Add a name here only when it sends nothing beyond the person's own tool,
  and add it to both lists in `tests/send-block.test.sh`.
- Nothing in this repository may name the company that owns it, a camp, or the person who
  made a skill. Run `grep -rliE "camp[g]roup" .` before every push; it must print nothing.
- American spelling, no dashes joining two thoughts, "child" or "camper" and never the
  slang word, in every file.
