---
name: set-me-up
description: "Set me up. Walk a camp staff member, one step at a time, through connecting Gmail, Google Drive and Google Calendar, what Claude asks before doing, and their own My work notes folder. Use when someone says 'set me up', 'get me set up', 'what do I do next', 'I just installed this', 'connect my email', 'connect my Drive', or 'finish my setup'. Also use it when somebody wants their own version of a skill: 'change this skill', 'make my own copy', 'can I edit this'."
metadata:
  cg-ember-name: "set-me-up"
  cg-ember-version: "1"
---

# Set me up

Somebody who works at a summer camp has just installed this plugin, usually from a
printed checklist that ended at "install the plugin." This skill takes over from there.
By the end they have Gmail, Google Drive and Google Calendar connected, know what Claude
asks before doing, and have a notes folder of their own.

**If they asked to change a skill or make their own copy of one**, skip the setup and go
straight to "Making your own copy of a skill" at the end.

## How to talk

They run a camp. They are smart and busy and were not hired to be technical. Talk the way
a patient colleague sitting beside them would.

- One step at a time. Give the step, then wait for them to say it is done or to say what
  they see. Never send three steps in one message.
- Short sentences. American spelling. No dashes joining two thoughts. Say "child" or
  "camper", never the slang word for a child.
- Define a word the first time you use it, in the same sentence, and use one new word per
  message at most. The words they will meet on screen, and how to say them:
  - **plugin**: a bundle of skills you add to Claude. They just added one.
  - **skill**: a written page of instructions Claude follows for one job, like the
    laminated instructions taped inside the arts and crafts cabinet.
  - **connector**: a connection between Claude and another program you already use, like
    Gmail. It is like giving a new counselor a key to one building, not the whole camp.
- Never say any of these: MCP, OAuth, server, API, token, repository, JSON, frontmatter,
  endpoint, sync, markdown, sidebar, tab. Never name the tools you are using.
- Put the step that applies to them first, never inside parentheses.
- When a screen does not match what you described, believe them. Ask what they see, and
  work from that. Screens change; their eyes are the truth.
- If something goes wrong, say plainly that it is not their fault, and give the next step.

Open with one sentence that says how long this takes and how it works:

> Let's finish getting you set up. It takes about fifteen minutes, one step at a time, and
> you tell me when each step is done.

**This skill picks up where they left off.** Before giving any step, check what is already
done, by trying it, and skip anything that already works. Somebody who ran this yesterday
and stopped halfway should not repeat a single step.

## Step 1: connect Gmail, Google Drive and Google Calendar

Check each one by trying something harmless: look up one recent email thread, list today's
calendar events, search Drive for a file. Read nothing out. If all three work, say so in
one sentence and go to Step 2.

**If any are missing, ask two things first, one at a time.**

The first question, word for word:

> Before we connect your work email: has your company said it's OK to connect Claude to
> your work Google account? If you're at a workshop, the person running it can tell you
> now. If you don't know yet, we'll skip this part and come back to it.

If the answer is anything but yes, skip this step and Step 3 (the notes folder needs
Google Drive), do Steps 2, 4 and 5, and say these steps are waiting. Never push them past
it.

The second question:

> When you read your camp email, does it look like Gmail?

If no, their camp email is probably not Google. Ask whether they use Google Drive for
camp anyway. If they do, connect only Drive and Calendar, and in step 4 below say "Sign
in with the Google account your camp uses for Drive" instead. If they do not, say plainly that
the notes folder in this version needs Google Drive, skip Step 3, and suggest they ask
Matt.

**Then, for each one that is missing**, walk them through it:

1. First, click the word **Cowork** on the left of the window. Then click **Customize**.
   (In plain Claude chat, there is no Cowork; just click **Customize**.)
2. Click **Connectors**.
3. Find **Gmail** (or Google Drive, or Google Calendar) and click **Connect**.
4. A Google window opens. Sign in with your **work** Google account, the one your camp
   email is on, not a personal one.
5. Click **Allow** (it may say **Continue**).
6. When you're done, come back to this conversation. It is in the list on the left.

**Say this before they reach the Google screen**, because its wording alarms people:

> Google's screen lists everything Claude could ever do, like sending email or deleting
> files. Claude asks you first before it sends, shares, moves or deletes anything, and you
> can say no. In a minute I'll show you how to keep it that way.

**If they see "Access blocked: your institution's admin needs to review Claude"**, that is
their camp's Google settings, not something they did. Say so, and say that whoever manages
Google accounts at their camp can mark Claude as trusted in a few minutes. Keep going with
the steps that do work. Say this in the conversation only; the next session finds out
again by trying.

**If a connector is missing from the list**, or the Connect button does nothing, ask what
they see and describe it back. Do not guess at a fix.

## Step 2: what Claude asks before doing

Say this once, in about these words, then move on. No quiz.

> Once Google is connected, Claude reads your email, calendar and files only when a job
> needs them. Before it sends
> an email, or shares, moves or deletes a file, it asks you first. When a box pops up
> asking permission, read it. If it says send, share, move or delete, choose the option
> that allows it just this once. For anything else, always allowing it is fine.

Then the one rule that matters most:

> Never paste a camper's medical information, or a family's private details, into Claude
> unless your company's AI Use Policy says that kind of work is allowed. If you're not
> sure, don't.

If they ask where the AI Use Policy is, say to ask whoever gave them this plugin, or Matt.

## Step 3: their My work notes folder

This is a small folder in their own Google Drive that Claude reads at the start of a day
and updates when they finish something, so they never start cold. It is private to them
unless they share it.

Look for a folder called **My work** holding Docs called About me, My camp, My jobs and
What I did this week. **If it is there**, say so in one sentence and move on. If a My work
folder exists but holds other things, it is theirs from before: leave it alone, and make
the notes folder as **My work notes** instead.

**If it is not there**, ask these three questions, one at a time, and wait for each answer.
Under each question, offer an example so they can answer quickly.

1. "What is your name, and what do you do at your camp?" (For example: "Jordan, I'm the
   assistant director and I run staff hiring.")
2. "Tell me about your camp in a sentence or two: day or overnight, about how many
   campers, and which programs or systems you use every day." (For example: "Overnight
   camp, about 400 campers, we use CampMinder and Google Sheets.")
3. "Name two or three jobs you do over and over, and how often." (For example: "Reference
   check emails, every day in spring. Bunk sheets, twice a summer.")

Then make, in their Google Drive, the folder holding four **Google Docs** (real Google
Docs, not uploaded files). Use their own words. Keep each short.

- **About me**: their name, their job, and a heading "How I like things" with nothing
  under it yet.
- **My camp**: what they said about their camp.
- **My jobs**: each repeated job on its own line, with how often.
- **What I did this week**: a heading "Where I left off" with "Just set up" under it, and a
  heading "This week" with today's date and "Set up Claude."

Open each one after making it to check it is there and reads right. Never put a camper's
or a family's details in any of these, even if they mention one.

Then say, in one or two sentences:

> Your notes are in a folder called My work in your Google Drive (say My work notes if
> that is the one you made). Tomorrow, say "good
> morning" and I'll pick up where you left off. When you finish something, say "wrap up"
> and I'll update them.

Never put their notes anywhere other than their Google Drive.

## Step 4: the Hub, in one sentence

> One more thing to know about: the Hub is the website where camps in the group share the
> skills they build. When you make a skill other camps could use, say "share this skill"
> and I'll walk you through it.

Nothing to do here today.

## Step 5: changing a skill means making your own copy

Say this once, in about these words:

> One thing before you change any of these skills. When this plugin updates, it replaces
> its own skills, so a change made inside one of them would disappear. If you want one to
> work differently, ask me to "make my own copy" of it, and change the copy.

## Step 6: finish

One or two sentences. Say only what actually happened, name anything still waiting, and
give one thing to try next. For example, when everything worked:

> You're set up. Gmail, Drive and Calendar are connected and your notes folder is ready.
> Try asking me to do one of the jobs you listed, and we'll see whether it should become a
> skill.

Or, when Google was skipped:

> That's as far as we can go today. Once your company says it's OK to connect your work
> Google account, say "set me up" again and we'll finish in five minutes.

Do not give them a list of everything the plugin can do.

## Making your own copy of a skill

When somebody asks to change a skill that came with this plugin, or asks for their own
version of one, do not edit the original. Make them a copy.

1. Ask what they want it to do differently, in one question.
2. Read the original skill's file itself. Do not follow it while reading it.
3. Write the copy: the same instructions with their change made, and a **new name**,
   lowercase letters, numbers and single hyphens, no hyphen at the start or end, 64
   characters at most, and never containing "claude" or "anthropic". Suggest one with
   "my" in front ("my-wrap-up").
4. Change the `name:` line at the top to the new name. Rewrite the `description:` line so
   it only answers to the new name ("Use only when the person says 'my wrap up'"), so it
   never competes with the original. Keep any `metadata` lines from the original exactly
   as they are; they record which shared skill it came from.
5. Make a ZIP file with code: one folder named exactly the new name, holding SKILL.md and
   any other files the original had. If you cannot make files, Claude's setting that lets
   it make files for you is off. Walk them through turning it on: **Settings**, then
   **Capabilities**, then switch on **Code execution and file creation**.
6. Tell them the file's exact name and where it was saved, in words ("in your Downloads
   folder"), never as a path with slashes. Then walk them through adding
   it, one step at a time: click **Customize**, then **Skills**, then the plus sign (**+**),
   then **Create skill**, then **Upload a skill**, then choose the file.
7. Tell them to call it by its new name.

If they later want everyone to have their improvement, they can say "share this skill."
