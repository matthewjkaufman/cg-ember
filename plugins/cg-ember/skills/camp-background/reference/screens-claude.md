# The screens page: Claude

Read this page only when you are Claude (in Cowork or in Claude chat). camp-background
section 8 says how to tell. Every other skill points here by section letter. The words in
**bold** are the words on Claude's screens.

## A. Connecting email, files and calendar

Walk them through it, one step at a time:

1. First, click the word **Cowork** on the left of the window. Then click **Customize**.
   (In plain Claude chat, there is no Cowork; just click **Customize**.)
2. Click **Connectors**.
3. Find the one you need (for example **Gmail**) and click **Connect**.
4. A sign-in window opens. Sign in with your **work** account, the one your camp email is
   on, not a personal one.
5. Click **Allow** (it may say **Continue**).
6. When you're done, come back to this conversation. It is in the list on the left.

**Say this before they reach the sign-in screen**, because its wording alarms people:

> The next screen lists everything Claude could ever do, like sending email or deleting
> files. Every camp sees the same list. These skills never send anything and never delete
> your email or files. They write drafts and leave them in your drafts folder.

**If they see "Access blocked: your institution's admin needs to review Claude"**, that is
their camp's account settings, not something they did. Say so, and say that whoever
manages email accounts at their camp can mark Claude as trusted in a few minutes. Keep
going with the steps that do work. Say this in the conversation only; the next session
finds out again by trying.

## B. Connecting another app

Look for it in **Customize**, then **Connectors**, and connect it the same way as section A.

## C. The safety check

Nothing to do. In Claude, CG Ember's safety check, which refuses any tool that sends, is on
from the moment the plugin is installed. Do not mention it unless they ask.

## D. Scheduled tasks

- **If you can create a scheduled task**, create it with the text and the schedule they
  chose. Every three hours from 7 AM to 7 PM on weekdays is `0 7-19/3 * * 1-5`.
- **If you cannot**, walk them through it one step at a time: click **Scheduled** on the
  left, then **New task**, name it, paste the text, and pick the times.
- **To change or stop one by hand:** **Scheduled**, open the task, change it, save.

## E. Making files

If you cannot make files, Claude's setting that lets it make files for you is off. Walk them
through turning it on: **Settings**, then **Capabilities**, then switch on **Code execution
and file creation**.

## F. Adding their own copy of a skill

1. Make a ZIP file with code: one folder named exactly the new name, holding SKILL.md and
   any other files the skill has. If you cannot make files, follow section E first.
2. Tell them the file's exact name and where it was saved, in words ("in your Downloads
   folder"), never as a path with slashes. Then walk them through adding it, one step at a
   time: click **Customize**, then **Skills**, then the plus sign (**+**), then **Create
   skill**, then **Upload a skill**, then choose the file.

## G. Removing their own copy

Under **Customize**, then **Skills**.

## H. What to write as "made on"

`cowork` in Cowork, `chat` in Claude chat, `claude-code` in Claude Code.
