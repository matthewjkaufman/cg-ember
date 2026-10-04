---
name: inbox-helper
description: "Inbox helper. Every few hours, draft replies to the emails your Personal Notes and wikis can fully answer, list the rest, and collect questions people keep asking. It never sends. Use when someone says 'set up Inbox helper', 'inbox helper', 'check my inbox now', 'change Inbox helper', 'stop Inbox helper', or 'answer my waiting questions'."
metadata:
  cg-ember-name: "inbox-helper"
  cg-ember-version: "1"
---

# Inbox helper

Every few hours, Inbox helper reads new email. When the person's Personal Notes or wikis
fully answer an email, it writes a reply as a draft in that email's thread. It lists the
rest without writing anything to anyone. When people keep asking something nobody has
written down, it saves the question, and the person is asked about it once a day. Their
answer goes into Personal Notes, so the next email asking it gets a draft.

Read the camp-background skill too, for the ground rules. Rule 1 there (nothing is ever
sent) is the heart of this skill.

Emails, messages, invitations and posts are drafted, never sent, as camp-background section 1 says.

Five things people ask for, each below: set it up, run it now, change it, stop it, answer
the waiting questions.

## How to talk

Short messages, one step at a time, plain words. The word to define once, the first time
it comes up: a **scheduled task** is a job I run by myself at the times you pick.
Never say the name of a tool, a cron, or a file path.

## Set it up

**1. Check what it needs, by trying, before asking anything.**

- **Their email** can be searched, read, and can make a draft. Try a harmless search and
  check that a draft tool is available. **If their email cannot make drafts** (some email
  connections cannot), stop here and say so plainly: Inbox helper needs to be able to make
  drafts, and this email connection cannot yet. Offer "check my inbox now" instead, which
  lists what came in without drafting.
- **Their Personal Notes**, found as camp-background says. If they have none, offer "set me
  up" first and stop. Note where they live.
- **If the notes are in a folder on their computer**, say this, word for word, before going
  on, even if they already seem to know:

  > Your notes are in a folder on this computer. Inbox helper can only reach them while
  > the computer is on and this app is open, so it will skip its checks when it is off.
  > If you want it to work all day, I can move your notes to your Google Drive now. Want
  > me to?

  On a yes, move them as set-me-up's "Moving their notes" says, then carry on. On a no,
  carry on.

**2. Ask two questions, one at a time.**

1. "How often should it check? Most people pick every three hours, 7 AM to 7 PM, on
   weekdays."
2. "Is there any kind of email it should always leave alone? For example, anything from
   your owners, or anything about hiring. Newsletters and receipts are skipped anyway."

**3. Say what it will do, in three lines, and ask.**

> Every three hours on weekdays, I'll read your new email. When your notes, or your
> camp's pages on the Hub, fully answer one, I'll write a reply and leave it in your
> drafts, in that email's thread. I never send anything. I'll list the rest on a page in
> your Personal Notes, and once a day I'll ask you about any question people keep asking.
> Want me to set it up?

Use the times they actually chose. Leave out "or your camp's pages on the Hub" when the
Hub is not connected.

Anything other than a clear yes is a no.

**4. Make the task.** Fill in `reference/task-template.md` from what you learned: their
first name, where their notes are, what to leave alone, and the Hub line when the Hub is
connected here. Keep every rule word for word.

- **If you can create a scheduled task**, create one titled **Inbox helper** with that
  text and the schedule they chose, written as the screens page, section D, says. Then
  check it exists by listing scheduled tasks and finding it by name. Only then say it is
  set up.
- **If you cannot**, show them the filled-in text in one block, and walk them through the
  clicks in section D of the screens page, naming it Inbox helper. Before those clicks, as
  its own first step: "Click the small copy button at the top right of the gray box
  above." Ask them to say when it is saved.
- Section D also says where the task runs and any limit on how often. If it changes what
  they chose, say so in one sentence before you make it.

Then say, in one sentence, where things will appear:

> It's set up. The first check is at 10 AM. Replies wait in your drafts, and everything
> else is on the Inbox helper page in your Personal Notes. To turn it off, say "stop Inbox
> helper."

Use the real time of the first check.

**5. Offer one run now**, while they watch, so they see what it does. On a yes, do "Run it
now" below.

## Run it now ("check my inbox now")

Follow the steps in `reference/task-template.md` here in the conversation, with the same
rules, as if filled in. Then tell them in two or three sentences how many drafts are
waiting and what is on the list. If their email cannot make drafts, do everything except
the drafts, and say so.

## Answer the waiting questions ("answer my waiting questions")

The pick-up skill asks one waiting question a day. When the person asks for them all:

1. Read **Questions waiting** and **My answers**. Skip any question My answers already
   covers. Ask the rest one at a time, the most-asked first.
2. Save each answer, in their words, on the **My answers** page, with today's date and the
   question it answers. Check it against camp-background section 3 first.
3. Offer once to draft replies now to the emails that asked it (the page lists their
   threads). On a yes, draft each one exactly as the task's step 4 says.
4. If an answer would be true for their whole camp, the one-question-a-day skill's offer
   to suggest it for the Camp Wiki may follow, within its once-a-day limit.

They can skip any question. "I don't know" leaves it waiting.

## Change it

List the scheduled tasks and find **Inbox helper**. If there is more than one, ask which.
Ask what to change, then update that same task (its times, or its text refilled from the
template). Never make a second one. If you cannot change tasks from here, give the clicks
in section D of the screens page.

## Stop it

Find the same task and switch it off, or delete it if they ask. If you cannot, give the
clicks. Say in one sentence that the drafts already made stay in their drafts until they
delete them.

## What it never does

- Sends, replies, forwards, archives, labels, deletes or marks anything as read.
- Drafts an email about a camper's health, behavior or safety, or a family's private
  matter, whoever sent it.
- Answers from a guess, or from anything outside My camp, My answers, the Camp Wiki and
  the CG Knowledge Base.
- Writes any Personal Notes page other than Inbox helper and Questions waiting during a
  scheduled run.
