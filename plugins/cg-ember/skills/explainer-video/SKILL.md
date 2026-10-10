---
name: explainer-video
description: "Make an explainer video. Write a short script, get their OK, then draw a captioned video in the camp's logo, colors and fonts, for phones and widescreen. Never posts it. Use when someone says 'make an explainer video', 'a short video about', 'animated video', 'video that explains' or 'turn this into a video'."
metadata:
  cg-ember-name: "explainer-video"
  cg-ember-version: "1"
---

# Make an explainer video

A short video, under about a minute, that explains one thing: how early pickup works, what
to pack, the three steps to sign up. Big words move on screen in the camp's own colors and
fonts, captions carry the message, and every video opens and closes with the camp's own
logo and name. Everything is drawn by a small program on this computer. No footage, no
photos, and no account anywhere.

It makes two copies: one shaped for phones (tall) and one for widescreen (a website, an
email, a TV in the lobby). It saves them as files and stops there.

Read the camp-background skill too, for the ground rules.

Emails, messages, invitations and posts are drafted, never sent, as camp-background section 1 says.

## The rules that never bend

- **It never posts, uploads or shares the video**, even when asked: not to a social media
  account, a video site, a website, a group chat, or a shared folder. It saves the files
  where the person can find them. If they ask you to post it, say once that this skill only
  saves the file, say where it is, and stop.
- **Nothing is drawn until the person approves the script**, word for word.
- **Never invent a camp fact.** Every time, place, rule and name in the script comes from
  the person, their Personal Notes, or the Camp Wiki. If one is missing, ask.
- **Never invent a color code or a font**, the same rule as the brand-guide skill. Never
  make or change a logo; use the camp's file exactly as it is.
- **No camper in the video.** A video travels, so treat it as something that leaves camp
  (camp-background section 3): no camper's name, no family's name, nothing medical, and no
  staff member's private details.

## How to talk

- One question at a time. Under each question, offer an example so they can answer quickly.
- Short sentences, plain words. Never show the plan file, a command or a folder path, and
  never name a program unless they ask. Say what you are doing in one plain sentence per
  step, so it never looks like nothing is happening.
- Words to use: **script** (what the video says), **caption** (the words at the bottom of
  the screen), **scene** (one screen of the video), **phone version** and **widescreen
  version**.

## Step 0: can this computer draw the video?

This skill carries a small program in its `scripts` folder. Run the tool check quietly:

`python scripts/check_tools.py` (or `python3`)

- If it says everything is here, note the `PY=` line it prints. Every command below runs
  with that Python, called `<py>` here.
- If it lists something as missing, say what it is in plain words and ask once:

  > To make the video I need two free programs on this computer: a helper program that
  > draws each picture, and a program that joins the pictures into a video. Setting them up
  > takes a few minutes, uses some space on your computer, and changes nothing else on your
  > computer. Is it OK to set them up?

  Only on a clear yes, run the install command the check printed (the same check with
  `--install`), and run the check again. Anything other than a yes is a no: go to "When
  this computer cannot draw the video" at the end.
- If Python itself will not run, or the install does not finish, say plainly that it is
  not their fault, then go to "When this computer cannot draw the video". Offer once to
  write what happened in the problem log, as camp-background section 6 says.

Never install anything else, and never run a command that needs an administrator.

## Step 1: what the video is about

Ask:

> What should the video explain, and who will watch it? For example: "how early pickup
> works, for new families."

If their request already says what the video explains and who it is for, or gives the
facts, skip this question and go on.

Then find the facts. Look in their Personal Notes and the Camp Wiki first (camp-background
section 4), and note the page and its date for each fact you use. Ask for anything still
missing, one question at a time. If the subject would take more than about a minute
to explain, say so and offer to make two short videos instead.

## Step 2: the camp's look

Look, and say nothing about looking, for **Our brand** on the **My camp** page of their
Personal Notes, or a brand guide page in the Camp Wiki (the brand-guide skill writes these).
The video needs:

- **The camp's name**, written the way the guide says.
- **The logo file.** The guide says what it is called and where it lives; the program
  needs the file itself. Ask them to drag it into this chat, or to say where it is on this
  computer. A picture of the logo works. If the background will be dark, use the version
  of the logo made for dark backgrounds, if the camp has one.
- **Four colors**, as color codes: the **background** (usually white or the camp's
  lightest color), the **text** color, the **main** color (headings and the caption box)
  and an **accent** color (the moving dot and the lines it draws).
- **Two fonts**: one for headings and one for regular text.

These are needed only before Step 5, so when the person has already given the facts, write
the script first and ask about the look once they approve it.

**When there is no brand guide**, offer once: "Want to build your brand guide first? It's
a few short questions, and everything I make for camp uses it after that." If they would
rather not, ask for just these four things, one at a time.

**When a color code or a font is not known**, never fill it in. Ask, and offer a choice
they make:

> I don't have the code for your green. If you know it, type it in (it starts with a #).
> Or I can use a plain dark green, #1E5631, for now. Which would you like?

For a font, the program can use a font installed on this computer, by its name, or a font
file they give you (a file ending in .ttf, .otf or .woff2, often from whoever designed the
logo). Two fonts come with this skill, Jost for headings and Figtree for regular text; offer
them only as a stand-in the person chooses, never as the camp's font.

No logo is fine too: the opening and closing then show the camp's name on its own.

## Step 3: the script, and the person's OK

Write a script of 3 to 6 scenes, 30 to 60 seconds in all. Each scene is one idea, in one of
four kinds:

- **Headline**: a few words, up to about six, with an optional small line under them.
- **Big**: one big word, time or number, 14 letters at most ("3:15 PM", "Free"), with a small
  line under it.
- **Steps**: a short title and 2 to 5 numbered steps, up to about six words each.
- **Checklist**: a short title and 2 to 5 items, each ticked off as it appears.

Every scene also has a **caption**: one or two short sentences, at most about 25 words,
that say the scene in full. The words on screen are short; the caption carries the message.

**Every camp fact says where it came from.** A camp fact is a time, a date, a place, a
rule, a price, a phone number or a name. Each one in the script comes from what the person
told you in this conversation, or from a page you read. Under the script, list every fact
that did not come from the person in this conversation, with the page and its date. A fact
you cannot trace to either goes in only as "[check: ...]" and you ask about it; better
still, leave it out.

**Always show the whole script before asking for the OK.** Every message that asks them
to approve shows every scene, in full, even if an earlier message showed it too. Never ask
"looks good?" about a script that is not in that same message.

Show it in this shape (the times and the page here are only an example):

> **How early pickup works**, about 35 seconds
>
> 1. On screen: Early pickup. Call by 1 PM. Come to the front office. Sign your camper out.
>    Caption: Picking up early? Call by 1 PM, come to the front office, and sign your
>    camper out.
> 2. On screen: 3:15 PM. The last early pickup.
>    Caption: Early pickup ends at 3:15 PM. After that, buses and car line run as usual.
>
> Where the camp facts came from: 1 PM and the front office, from what you told me. 3:15 PM
> and the buses, from your My camp page (September 15).
>
> The video opens and closes with your logo and your camp's name. Anything to change?
> Say "looks good" when it's right.

Put nothing before the script but one short sentence. If Step 0 found that this computer
cannot draw the video, say so in one sentence after the script, never instead of it.

Change what they say, in their words, and show the whole script again with the change in
it. Draw nothing until they say it is right.

## Step 4: how it sounds

Ask one question:

> How should it sound? 1) Captions only, with a short cheerful tune at the start and end.
> 2) Captions only, silent. 3) A computer voice reads each caption aloud. It sounds like a
> computer, not a person. 4) A presenter: a made-up person on screen reads the script.
> That needs Google Vids in your camp's Google account, and comes in widescreen only.

Captions are always on, whatever they pick.

- **For 3**, run `<py> scripts/make_video.py voices`. If it lists no voice, say: "This
  computer has no built-in voice I can use, so the video will have captions only." Then
  carry on with 1 or 2, whichever they pick. If there is more than one voice, name them and
  let the person pick; the first one is fine if they have no preference. If a word will be read wrong (a camp
  name, for example), write how it sounds in that scene's `say` line, and keep the caption
  spelled correctly.
- **For 4**, ask first: "Does your camp's Google account have Google Vids? Click
  [Open Google Vids](https://docs.google.com/videos) while you are signed in to your camp
  account. If you see a page for making
  a video, you have it." If they do not, say that the presenter needs Google Vids, and offer
  1, 2 or 3. If they do, finish Steps 5 to 7 first, then follow `reference/google-vids.md`
  in this skill's folder.

## Step 5: build it, and look before you show it

Make a folder called **Explainer videos** in the folder you are working in, and inside it a
folder named for today and the title, like **2026-10-12 How early pickup works**. Copy the
logo and any font files there. Write the plan file there, in the shape the top of
`scripts/make_video.py` describes, with the scenes exactly as approved. Then run:

`<py> scripts/make_video.py stills "<plan>" "<that folder>/pictures to check"`

It draws one picture per scene in both shapes, plus a sheet of them. If it prints a
**PROBLEM** line, say it in plain words and fix it: shorten words that do not fit (and show
the person the new words before going on), or ask for the missing file or font.

Then look at every picture yourself. Check that every word is on screen, nothing is cut off
or crowded, the colors are the camp's, and the logo is the right way up and not stretched.
If something looks wrong, fix the plan and draw the pictures again. If you can show
pictures here, show them the two sheets and ask, "Does this look like your camp?"

## Step 6: draw the video

Say: "Drawing your video now. It takes a few minutes, and you can keep working." Then run:

`<py> scripts/make_video.py video "<plan>" "<that folder>"`

Add `--music` for a tune, and `--voice "<the voice's name>"` for the computer voice. It
draws the phone version and the widescreen version, and also writes the captions as a
separate file, which some video sites ask for. Each finished file is on a line starting
**MADE**, with its length. If it prints a **PROBLEM** line, say it plainly and fix what it
names; if it happens again, offer the problem log.

## Step 7: tell them where it is

Say, in words, where the folder is, and then:

> Your video is ready: about 35 seconds, in two shapes. The phone version is the tall one,
> for phones and stories. The widescreen version is for your website, an email or a TV. I
> haven't posted or shared it anywhere.

If they would like a copy in their own Google Drive and their files are connected, offer
once to put it in a folder they name there. Never share it with anyone.

**Changes after they watch.** For a change to the words, show only the changed scenes for
their OK, then build it again from Step 5. For a change to the look, change the plan and
build it again. The old files stay unless they ask you to remove them.

## When this computer cannot draw the video

Do everything up to the approved script anyway. Then give them the script as a document in
their files, with a short plan for each scene (what is on screen, what the caption says,
and the camp's colors and fonts by name), so they or a volunteer can build it in a slide or
video app they already use. If you cannot make files at all here, the screens page,
section E, says how to turn that on.

Say plainly what happened, in one sentence, for example: "This computer can't run the
drawing program, so here is your script and a scene plan instead."

## What this does not do

- It never posts, uploads, shares or sends the video.
- It never draws anything before the script is approved.
- It never invents a fact, a color code or a font, and never changes a logo.
- It never puts a camper, a family or a staff member's private details in a video.
- It never uses camp photos or footage, or any account, except Google Vids when the person
  chooses a presenter and their camp has it.
