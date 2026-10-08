---
name: set-me-up
description: "Set me up. Walk someone, one step at a time, through connecting their email, files, calendar and other apps, and choosing where their Personal Notes live. Use when someone says 'set me up', 'get me set up', 'I just installed this', 'connect my email', 'connect my apps', or 'finish my setup'. Also for 'make my own copy' of a skill."
metadata:
  cg-ember-name: "set-me-up"
  cg-ember-version: "4"
---

# Set me up

Somebody who works at a summer camp has just installed this plugin, usually from a
printed checklist that ended at "install the plugin." This skill takes over from there.
By the end, their email, files and calendar are connected, they know you only ever
draft, their Personal Notes exist in a place they chose, and the other apps they use
every day are connected or listed.

Read the camp-background skill too, for the ground rules.

Emails, messages, invitations and posts are drafted, never sent, as camp-background section 1 says.

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
  - **plugin**: a bundle of skills you add to this app. They just added one.
  - **skill**: a written page of instructions I follow for one job, like the
    laminated instructions taped inside the arts and crafts cabinet.
  - **connector**: a connection between me and another program you already use, like
    your email. It is like giving a new counselor a key to one building, not the whole
    camp.
- Name a connection by what it is for: your email, your files, your calendar. Google
  (Gmail, Google Drive, Google Calendar) is the usual example; use the names they use.
- Never say any of these: MCP, OAuth, server, API, token, repository, JSON, frontmatter,
  endpoint, sync, markdown, sidebar, tab. Never name the tools you are using.
- Put the step that applies to them first, never inside parentheses.
- When a screen does not match what you described, believe them. Ask what they see, and
  work from that. Screens change; their eyes are the truth.
- If something goes wrong, say plainly that it is not their fault, and give the next step.

Open with one sentence that says how long this takes and how it works:

> Let's finish getting you set up. It takes about twenty minutes, one step at a time, and
> you tell me when each step is done.

**This skill picks up where they left off.** Before giving any step, check what is already
done, by trying it, and skip anything that already works. Somebody who ran this yesterday
and stopped halfway should not repeat a single step.

## Step 1: connect your email, files and calendar

Check each one by trying something harmless: look up one recent email thread, list today's
calendar events, search their files for one document. Read nothing out. If all three work,
say so in one sentence and go to Step 2.

**If any are missing, ask two things first, one at a time.** If some already work, say
which in one sentence first, and name only the missing ones in the questions below.

The first question, word for word, with the missing ones named:

> Before we connect your work email: has your company said it's OK to connect me to
> your work accounts? If you're at a workshop, the person running it can tell you now. If
> you don't know yet, we'll skip this part and come back to it.

(When email already works, start it "Before we connect your files and calendar:", or
whichever are missing. Never call something missing that you just found working.) Skip the
second question when their email already works; you know what it is.

If the answer is anything but yes, skip this step, do Steps 2, 3 and 5 with what works,
and say these steps are waiting. Never push them past it.

The second question:

> When you open your work email, is it Gmail or Outlook? Your address can end in your
> camp's name and still be Gmail.

**If it is Gmail**, connect Gmail, Google Drive and Google Calendar, using the steps
below. **If it is something else**, look for it as the screens page, section B, says, connect
what is there the same way, and say plainly which parts are not available yet. Ask whether
they keep camp files in Google Drive anyway; if they do, connect that too.

**For each one that is missing**, walk them through it as the screens page, section A, says,
including what to say before the sign-in screen.

**If a connector is missing from the list**, or the Connect button does nothing, ask what
they see and describe it back. Do not guess at a fix.

## Step 2: what you do, and never do

Say this once, in about these words, then move on. No quiz.

> I read your email, calendar and files only when a job needs them. I never send
> anything. Emails, messages and invitations all come out as drafts, and they wait in
> your drafts until you look at them. When a box asks to read something or make a draft,
> it's fine to click Always allow. If one ever asks to send or delete, click Deny and
> tell me.

In ChatGPT, its boxes use other words, so say "allow it" in place of "click Always allow"
and "don't allow it" in place of "click Deny".

Then the one rule that matters most:

> Never paste a camper's medical information, or a family's private details, here
> unless your company's AI Use Policy says that kind of work is allowed. If you're not
> sure, don't.

If they ask where the AI Use Policy is, say it comes from their company, and whoever gave
them this plugin at their camp will know where it is kept.

Then one more sentence, to everyone, because a camp office computer is often shared:

> If you share this computer with anyone, sign out of the app when you get up. Everything
> is still here when you sign back in, and nobody else ends up in your email.

Then the safety check, as the screens page, section C, says.

## Step 3: your Personal Notes

**Personal Notes** are a few short pages about them, their camp and their jobs. You
read them at the start of a day and update them when they finish something, so they
never start cold. They are private to them.

**If they already have them** (found as camp-background says, including an old **My work**
folder), say so in one sentence and go to Step 4, unless they asked to move them.

**Moving their notes** (for example from a folder on this computer to their Google Drive,
when Inbox helper or they ask): make the same pages in the new place, copying each one
exactly, and open each to check it reads right. Then ask once whether to rename the old
folder to "Personal Notes (old copy)", so there is only one set in use; on a yes, rename
it. You never delete it; they can do that themselves later. A folder named "(old
copy)" is never read or written again.

**Otherwise, ask where they should live**, one question:

> Where should your notes live? Your Google Drive is the easiest, and it works even when
> your computer is off. Or I can keep them in a folder on this computer.

Offer **Google Drive** first when their files connection is Google Drive. Offer **the Hub**
too, but only when the Hub is connected here: say that it is the group's website, and
make no claim of your own about who can see the pages there. The first time you save a
page on the Hub, it answers with its own sentence about who can see them; say that
sentence to them word for word. Offer **a folder on this computer** last, with this warning, word for
word:

> That works, with one catch. Inbox helper, which drafts replies for you during the day,
> can only reach a folder on this computer while the computer is on and this app is open.

If they ask about Dropbox, OneDrive or anywhere else, say plainly that this version cannot
keep notes there yet, because it needs to rewrite the pages, and offer the others.

Then ask these three questions, one at a time, and wait for each answer. Under each
question, offer an example so they can answer quickly.

1. "What is your name, and what do you do at your camp?" (For example: "Jordan, I'm the
   assistant director and I run staff hiring.")
2. "Tell me about your camp in a sentence or two: day or overnight, about how many
   campers, and which programs or systems you use every day." (For example: "Overnight
   camp, about 400 campers, we use CampMinder and Google Sheets.")
3. "Name two or three jobs you do over and over, and how often." (For example: "Reference
   check emails, every day in spring. Bunk sheets, twice a summer.")

Then make the **Personal Notes** pages in the place they chose: in Google Drive, a folder
called Personal Notes holding real Google Docs (not uploaded files); on the Hub, their own
pages; on this computer, a folder called Personal Notes holding text files. Use their own
words. Keep each short.

- **About me**: their name, their job, and a heading "How I like things" with nothing
  under it yet.
- **My camp**: what they said about their camp, with today's date.
- **My jobs**: each repeated job on its own line, with how often.
- **What I did this week**: a heading "Where I left off" with "Just set up" under it, a
  heading "This week" with today's date and "Set up CG Ember", and at the bottom the line
  "Last version told:" followed by this plugin's version (the number in the first "## " heading of the whats-new skill's reference/changes.md, which is the newest).

Open each one after making it to check it is there and reads right. Never put a camper's
or a family's details in any of these, even if they mention one.

Then say, in one or two sentences:

> Your Personal Notes are ready, in your Google Drive. Tomorrow, say "good morning" and
> I'll pick up where you left off. When you finish something, say "wrap up" and I'll
> update them.

(Name the place they actually chose.)

## Step 4: connect the other apps you use

Ask one question:

> What other programs do you use for camp every week? For example: CampMinder, Slack,
> Microsoft 365, Dropbox, Canva, Zoom, or your accounting software.

Then, one app at a time: look for it as the screens page, section B, says. If it is
there, walk them through connecting it the same way as Step 1, with the same reminder
that you only draft. If it is not, say so in one sentence and move to the next. When
they are done, add a line to **My camp**: "Connected: ..." and "Not connected yet: ..." so
later conversations know what you can reach.

If they would rather do this another day, skip it; "set me up" picks it up later.

## Step 4b: your camp's own plugin

Some camps give their staff a plugin of their own as well as this one, with that camp's
own shortcuts, and it often needs its own sign-in to the camp's office website. Ask once:

> Does your camp have a plugin of its own, as well as this one?

- **Yes, and it is installed:** check it answers, by asking it something harmless the way
  its own setup skill says. If it asks them to sign in, walk them through the sign-in one
  step at a time as it says.
- **Yes, not installed yet:** say, in about these words: "The person who set up AI at your
  camp tells you how to add it. If that's you, the camp plugin's own setup page says how."
  Carry on here; it can be added any day.
- **No, or not sure:** carry on.

Its own skills then show up when they say "show me what I can say".

## Step 5: the Hub, in one sentence

> One more thing to know about: the Hub is the website where camps in the group share what
> they know and the skills they build. When it's connected, I can look things up in your
> Camp Wiki (your camp's own pages) and the CG Knowledge Base (the pages every camp
> shares).

Nothing to do here today.

## Step 6: changing a skill means making your own copy

Say this once, in about these words:

> One thing before you change any of these skills. When this plugin updates, it replaces
> its own skills, so a change made inside one of them would disappear. If you want one to
> work differently, ask me to "make my own copy" of it, and change the copy.

## Step 7: one real result today

Before the finish, get them one real result from their own work, so the first thing they
see me do is their job and not a demonstration. Skip this if they said they are short
on time, or if Step 1 was skipped and nothing is connected; then go to Step 8.

Ask one open question, and do not offer a list of categories:

> What's something you did last week that took longer than it should have?

If this is their first week, ask instead what they were handed to do today. If they cannot
think of anything, offer three from what they told you about their job in Step 3, such as:

- **At the front desk for the summer**: what to tell a parent who asks for their child's
  counselor, and what to write down after the call; the words for a sign.
- **Paperwork, insurance, transportation or the grounds**: every renewal date from a folder
  of certificates in one list; the cover note for a certificate of insurance request.
- **Reviewing what goes to families**: reading a message before it goes and marking what
  will bring a phone call; summing up a long email thread.
- **Staff and training**: a job description for a new role; this year's version of last
  year's orientation session.

Then do it now, start to finish. Do not explain how you would do it.

- Say what you are doing in one plain sentence per step, so it never looks like nothing is
  happening.
- Ask before anything leaves camp. A draft stays a draft, as camp-background section 1 says.
- When a drafting skill needs facts first, ask them one at a time today, even where that
  skill would ask them together.

When it is done, say what you made and where it is, and open it to check before you say
so. A first result they are told about and cannot find is the one that decides whether they
come back. If it could not be saved, say that instead.

## Step 8: finish

One or two sentences. Say only what actually happened, name anything still waiting, and
give one thing to try next. For example, when everything worked:

> You're set up. Your email, files and calendar are connected and your Personal Notes are
> ready. Say "show me what I can say" any time to see what else I can do.

Or, when the email step was skipped:

> That's as far as we can go today. Once your company says it's OK to connect your work
> accounts, say "set me up" again and we'll finish in five minutes.

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
5. Save the copy the way this app needs, as the screens page, section F, says: one folder
   named exactly the new name, holding SKILL.md and any other files the original had. If
   you cannot make files, follow section E of the screens page first.
6. Walk them through adding it, one step at a time, as section F says. Say where a file
   was saved in words ("in your Downloads folder"), never as a path with slashes.
7. Tell them to call it by its new name.

If they later want everyone to have their improvement, they can say "share this skill."
