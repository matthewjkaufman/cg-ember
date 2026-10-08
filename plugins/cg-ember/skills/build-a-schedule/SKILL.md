---
name: build-a-schedule
description: "Build our schedule. Draft a whole activity schedule for camp groups over the cycle, with no area booked twice at once, re-check it after every change, and make a printable spreadsheet. Use when someone says 'build our schedule', 'activity schedule', 'schedule my groups', 'draft the cycle', or 'check my schedule'."
metadata:
  cg-ember-name: "build-a-schedule"
  cg-ember-version: "1"
---

# Build our schedule

Many camp directors build the activity schedule by hand: every group, every period, every
day of the cycle, on a big sheet of paper or a spreadsheet, checking that two groups are
never sent to the same place at once. Eighteen groups over a five-day cycle is hundreds of
boxes and a week of evenings.

This skill drafts the whole cycle, the director changes what she wants, and after every
change it checks the schedule again. At the end she gets an Excel workbook ready to print:
one sheet per group, one per activity area, and one master grid.

Read the camp-background skill too, for the ground rules.

Emails, messages, invitations and posts are drafted, never sent, as camp-background section 1 says.

## The one rule that is always on

**No area holds more groups than it can in one period.** An area is a place an activity
happens: the pool, the gaga pit, the art room. Each area holds one group at a time, unless
she says it can hold more (a big field may hold three) or marks it shared (the dining hall
holds everyone).

Nothing else is a built-in rule. Fair rotation, fixed periods such as swim or lunch, and
staff limits are only on when she asks for them in Step 2. Never add a rule she did not
give, never "improve" the schedule with one, and never tell her a schedule breaks a rule
she never set.

## How to talk

- One question at a time, about one topic. Under each question, offer an example so she can
  answer quickly.
- Short sentences, plain words. Say "group", "activity", "area", "period" and "day", and
  use her words for them once she gives them ("bunk", "rotation", "Day A").
- Never show her the setup file or the commands. Say what you are doing in one plain
  sentence per step, so it never looks like nothing is happening.
- Groups only. Never put a camper's name, or anything about a camper, into the schedule.

## Step 0: can this app run the helper?

This skill carries a small program, `scripts/schedule.py` in this skill's folder, that
drafts the schedule, checks it, and writes the workbook. Try it quietly once:
`python scripts/schedule.py` (or `python3`) should print how to use it. If the workbook
step later says a piece called openpyxl is missing, install it once with
`python -m pip install openpyxl` and try again.

**If it will not run**, follow the screens page, section E, once: in some apps a setting
for running code and making files is off. **If this app still cannot run code**, say so in
one sentence, and use "When the app cannot run the helper" at the end instead. Everything
else in this skill still applies.

## Step 1: last year's schedule

Ask:

> Do you have last year's schedule, as a spreadsheet or photos of the paper one? If you
> share it, I'll start from it. If not, I'll ask you a few questions instead.

**If she shares it**, read it for the shape: the groups, the activities, the areas, the
days and the periods. Never guess a box you cannot read on a photo; list those and ask.
Read the shape back in a few plain sentences ("18 groups, 5 days, 6 periods a day, 12
activities in 11 areas"), then ask one question: "What's different this year?" Then go on
to the rules questions in Step 2, which she has to answer either way.

**If she does not**, go through Step 2 in full.

## Step 2: the interview, one topic at a time

Ask each in its own message, and wait for the answer.

1. **Groups.** "What are your groups called, and how many are there?" (For example: "Group
   1 to Group 18", or "Bunks 1A to 9B".)
2. **Days.** "How many days are in your cycle, and what do you call them?" (For example:
   "Day 1 to Day 5", or "Monday to Friday".)
3. **Periods.** "How many periods are in a day, and what do you call them?" (For example:
   "Period 1 to Period 6", or times like "9:00".)
4. **Activities and areas.** "What are the activities, and where does each one happen?"
   (For example: "Swim at the pool, gaga at the gaga pit, soccer and kickball both on the
   field.") Ask whether any activity is only for some groups.
5. **Shared areas.** "Can any place hold more than one group at the same time? If so, how
   many?" (For example: "The field holds three groups. The dining hall holds everyone.")

Then the three rules questions. Each is a separate question, and a "no" means that rule
stays off:

6. **Fixed periods.** "Is anything always at the same time, for everyone or for some
   groups, like lunch or swim?"
7. **Rotation.** "Do you want me to keep the activities fair, like each group swimming a
   set number of times a cycle, or no group doing the same activity twice in one day?" Take
   the exact numbers she gives.
8. **Staff limits.** "Is any activity limited by staff, like only two groups at archery at
   once because you have two instructors?"

Last: "Anything else I should know?" If she names a rule the helper does not know (for
example "Group 3 and Group 4 never at the waterfront together"), say plainly that you will
check that one by reading, after each draft, and say each time whether it holds.

Read it all back in five or six plain sentences, including every rule she turned on and
"nothing else is a rule". Change what she corrects.

## Step 3: the draft

Write her answers into a setup file in the shape the top of `scripts/schedule.py`
describes, in a folder of your own working space, with her names exactly as she gave them.
Rules go in only when she turned them on. Then run:

`python scripts/schedule.py draft setup.json schedule.json`

The helper places the fixed periods first, then fills every other period it can. It
spreads activities around so the draft reads sensibly, but nothing checks for that unless
she asked for a rotation. Any period it could not fill is left open, never forced.

Tell her in two or three sentences what came back: how many periods are filled, any left
open and why if it is clear, and that no area is double booked. Then show one day as a
table (`python scripts/schedule.py table schedule.json` prints them) and ask whether she
wants the whole cycle on screen or goes straight to the workbook.

## Step 4: the workbook

`python scripts/schedule.py build schedule.json "<her camp's name> schedule.xlsx"`

The helper checks the schedule first and refuses to write a workbook with a double booking.
After writing, it opens the file again and checks what is actually in it. Only offer the
workbook when it says so.

Save it where she can open it: in her files, or as a file she downloads in this app (the
screens page, section E, covers making files). Say where in words, never as a
path. Tell her what is inside in one sentence: "The first sheet is the master grid, then
one sheet for each group and one for each area, and the last sheet lists your areas and
rules. Open periods are shaded yellow." Each sheet prints on its own page.

## Step 5: her edits, and a check after every one

She changes things. Either way, check again after every change, before anything else:

- **She tells you** ("swap Group 3's Day 2 morning with Group 7"): change the schedule file
  and run `python scripts/schedule.py check schedule.json`.
- **She edits the workbook herself** and gives it back: run
  `python scripts/schedule.py check "<the workbook>"`. It reads her Master sheet, so her
  typing is what gets checked. Copy her changes into the schedule file before building a
  new workbook, so nothing she typed is lost.

Say the result in one sentence. When it is clean: "Still no area double booked." When it is
not, name exactly where ("The gaga pit has Group 4 and Group 9 on Day 2, Period 3") and
offer two ways to fix it, then let her choose. Report a rule she asked for that her edit
broke the same way, and say it is her call; only the double booking blocks a new workbook.
Then build the workbook again.

## When the app cannot run the helper

Do the same steps, by reading instead of running.

- Draft the schedule as one table per day: groups down the side, periods across the top,
  the activity in each box. She can copy each table into Excel or Google Sheets.
- Check it by hand, every time: for each day and each period, list every area and the
  groups in it, and compare with how many it holds. Say plainly that this check was done
  by reading, not by a program, and suggest she spot-check one day herself.
- Say once that the printable workbook needs an app that can run a small program, such
  as the desktop app.

## What this does not do

- It never adds a rule she did not ask for.
- It never offers a workbook the helper did not check, and never says "no double
  bookings" without a check run since the last change.
- It never invents a group, an activity or an area.
- It never touches another scheduling program or its data, even one she uses today. Last
  year's schedule is read only when she shares it.
- It never puts a camper's name or details in the schedule.
- It never sends the schedule to anyone.
