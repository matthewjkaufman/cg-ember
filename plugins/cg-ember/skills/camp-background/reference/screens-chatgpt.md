# The screens page: ChatGPT

Read this page only when you are ChatGPT (including Codex inside the ChatGPT app).
camp-background section 8 says how to tell. Every other skill points here by section letter.
The words in **bold** are the words on ChatGPT's screens as OpenAI's own help pages give
them. Screens change, and some accounts name things differently: when what they see does not
match, believe them, ask what they see, and work from that.

## A. Connecting email, files and calendar

Walk them through it, one step at a time:

1. Click **Plugins** on the left of the window. (On some accounts it is called **Apps**.)
2. Find the one you need, for example **Gmail**. Click it.
3. Click **Install plugin**. Then click **Connect**.
4. A sign-in window opens. Sign in with your **work** account, the one your camp email is
   on, not a personal one.
5. Click **Allow** (it may say **Continue**).
6. Come back to this conversation. Your conversation is in the list on the left.

**Say this before they reach the sign-in screen**, because its wording alarms people:

> The next screen lists everything ChatGPT could ever do, like sending email or deleting
> files. Every camp sees the same list. These skills never send anything and never delete
> your email or files. They write drafts and leave them in your drafts folder.

**If a box asks how much ChatGPT may do on its own** in that app, tell them to choose
**Allow read actions**. Say ChatGPT may still ask before it makes a draft, and approving a
draft is fine. Never tell them to choose **Allow all actions**. It lets ChatGPT act without
asking first.

**If a screen says their camp's administrator has to approve the app**, that is their camp's
account settings, not something they did. Say so, and say that whoever manages email
accounts at their camp can approve it. Keep going with the steps that do work. Say this in
the conversation only; the next session finds out again by trying.

## B. Connecting another app

Look for it in **Plugins**, and connect it the same way as section A.

## C. The safety check

CG Ember carries a safety check that refuses any tool that sends, as a second lock behind
the written rule. In ChatGPT it works only after they approve it once, and only when you
are working on this computer in the ChatGPT desktop app. In ChatGPT in a web browser, on a
phone, or in a scheduled task, it does not run, and the written rule is what holds.

If they are using ChatGPT in a web browser or on a phone, skip the rest of this section.
Say this step needs the ChatGPT desktop app, and that where they are, only the written
instructions keep you from sending. Otherwise, say this first, in about these words:

> One more step. CG Ember has a safety check. It is a second lock that stops me from
> pressing send, even by mistake. ChatGPT asks you to approve it. The next screen shows a
> few lines of code. That is normal. They are the check itself.

Never tell them the safety check protects them in a browser, on a phone, or in a scheduled
task.

Then, one step at a time:

1. Click **Settings**.
2. Click **Hooks**.
3. Find the two checks from CG Ember. Approve each one. The button may say trust or allow.
4. Tell me when both are approved.

If they do not see **Hooks**, ask what they see under **Settings** and work from that. Say
the written rule still holds. Do not guess at other screens.

ChatGPT asks again whenever an update changes the safety check. When the whats-new skill
says an update did, walk them through these steps again.

## D. Scheduled tasks

- **If you can create a scheduled task**, create it with the text, and say the schedule in
  plain words ("every three hours from 7 AM to 7 PM on weekdays").
- **On ChatGPT's free plan**, a task runs at most once a day. Say so, and offer 7 AM on
  weekdays.
- **Where it runs.** A task made in ChatGPT in a web browser runs on OpenAI's computers, so
  it keeps working when their computer is off, and it can reach notes in their Google
  Drive. If their notes are in a folder on this computer, the task must be made in the
  desktop app, and it runs only while the computer is on and the app is open.
- **When you make Inbox helper or any task**, say: "When this runs on its own, the safety
  check does not run. My written instructions still tell me never to send."
- **If you cannot create it**, walk them through it one step at a time: click **Scheduled**
  on the left, start a new task, name it, paste the text, and pick the times.
- **To change or stop one by hand:** **Scheduled**, open the task, change it, save.

## E. Making files

In the ChatGPT desktop app you can save files on this computer, after they say yes. In a web
browser you can make a file for them to download. If you can do neither, say so plainly and
suggest the ChatGPT desktop app.

## F. Adding their own copy of a skill

**In the desktop app:** ask first, in these words:

> I'll save your copy on this computer, in the folder where ChatGPT looks for your own
> skills. OK?

On a yes, save one folder named exactly the new name, holding SKILL.md and any other files
the skill has, inside the `.agents/skills` folder in their home folder. Never say that path
to them. Then tell them to start a new conversation and call it by its new name.

**In a web browser:** make a ZIP file of that folder for them to download. Walk them through
adding it, one step at a time:

1. Click **Plugins**.
2. Click the **Skills** tab.
3. Click **Create**.
4. Click **Upload from your computer**.
5. Choose the file.

If there is no **Skills** tab, say plainly that their own copy needs the
ChatGPT desktop app, and offer to save it there the next time they use it.

## G. Removing their own copy

Offer to move their copy's folder out of the skills folder into a folder beside it called
"old skills". Never delete it.

## H. What to write as "made on"

`chatgpt`.
