# The screens page: Claude

Read this page only when you are Claude (in Cowork or in Claude chat). camp-background
section 8 says how to tell. Every other skill points here by section letter. The words in
quotation marks or **bold** are the words on Claude's screens.

## A. Connecting email, files and calendar

Walk them through it, one step at a time:

Note: In plain Claude chat there is no "Cowork", so start at step 2. Claude decides; do not
say this to them.

1. Click "Cowork" on the left of the window.
2. Click "Customize".
3. Click "Connectors".
4. Find the one you need, for example "Gmail".
5. Click "Connect".
6. Sign in with your **work** account in the sign-in window, not a personal one.
7. Click "Allow". If the button says "Continue", click "Continue".
8. Come back to this conversation, in the list on the left.

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
through turning it on, one click per step:

1. Click your name at the bottom left.
2. Click "Settings".
3. Click "Capabilities".
4. Switch on "Code execution and file creation".

## F. Adding their own copy of a skill

1. Make a ZIP file with code: one folder named exactly the new name, holding SKILL.md and
   any other files the skill has. If you cannot make files, follow section E first.
2. Tell them the file's exact name and where it was saved, in words ("in your Downloads
   folder"), never as a path with slashes. Then walk them through adding it, one click per
   step:
   1. Click "Customize".
   2. Click "Skills".
   3. Click the plus sign ("+").
   4. Click "Create skill".
   5. Click "Upload a skill".
   6. Click "Downloads" on the left of the window that opens.
   7. Click the file named [the file's exact name].
   8. Click "Open".

## G. Removing their own copy

Under **Customize**, then **Skills**.

## H. What to write as "made on"

`cowork` in Cowork, `chat` in Claude chat, `claude-code` in Claude Code.

## I. Signing out

Note: If the menu says "Sign out" instead, click "Sign out".

1. Click your name at the bottom left.
2. Click "Log out".
