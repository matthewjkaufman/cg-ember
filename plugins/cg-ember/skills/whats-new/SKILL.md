---
name: whats-new
description: "What's new. Tell a camp staff member, in a few plain lines, only what changed in this plugin since the last version they heard about, and what to say to use it. Use when someone says 'what's new', 'what changed', 'anything new', or 'what's different since the update'. The pick-up skill also runs it once after an update."
metadata:
  cg-ember-name: "whats-new"
  cg-ember-version: "1"
---

# What's new

Somebody who works at a summer camp has a newer version of this plugin. Tell them what
they can do now that they could not before, in a few lines, and stop.

Read the camp-background skill too, for the ground rules.

## Step 1: read the changes

Read **reference/changes.md** in this skill's own folder. Each version has a heading with
its number, newest at the top, then plain lines in order of importance. The top heading
is the version they have now.

## Step 2: find what they last heard

Find their Personal Notes the way camp-background section 4 says. In **What I did this
week**, look at the housekeeping lines at the bottom for one that reads:

```
Last version told: 0.1.0
```

- **The line is there**: everything in versions newer than that number is new to them.
  Compare numbers part by part (0.10.0 is newer than 0.9.0).
- **No line, and their notes are in an old My work folder**: they set up with 0.1.0, so
  treat it as "Last version told: 0.1.0".
- **No line, and no sign of an earlier version**: this is their first time. Go to
  Step 5.
- **No Personal Notes at all**: say the one sentence in Step 5, suggest "set me up"
  instead of the list, and stop. Nothing can be saved yet.

## Step 3: say what changed

- **Nothing newer than their line**: one sentence, with the number from the top of
  changes.md. "Nothing new since you last heard. You're on 0.2.0." Then stop.
- **Something newer**: two to five plain lines, taken from the top of the newer entries.
  Each line says what they can do and what to say to do it. If there is more than fits in
  five, end with one more line: "There's more. Say 'show me what I can say' for the whole
  list."

Use the words in changes.md. Never mention a folder name, a file, or a version that is
not theirs. No headings, no introduction, no "exciting".

Example:

> A few things are new since you last heard:
> Your notes are now called Personal Notes. Nothing moved; they're where they were.
> Say "set up Inbox helper" and every few hours I'll draft replies to emails your notes
> can answer. It never sends.
> Say "write as me" for a draft in your own voice.
> There's more. Say "show me what I can say" for the whole list.

## Step 4: update the line

Rewrite the "Last version told" line to the version at the top of changes.md. If the line
is not there, add it with the other housekeeping lines at the bottom of What I did this
week. Read the page first and change only that line. Say nothing about saving it.

If the notes could not be saved, say nothing about that either; the only cost is hearing
the same news again next time.

## Step 5: the first time ever

One sentence, with the number from the top of changes.md, then one suggestion, then
write the line as in Step 4:

> You're on the newest version, 0.2.0, so everything here is new to you. Say "show me
> what I can say" to see what you can ask for.

## When the pick-up skill runs this

Pick-up runs this once, right after an update. Keep it inside pick-up's reply: the lines
only, after the "where you left off" sentence, with no greeting of its own. Update the
line the same way, so it is said once and never again.
