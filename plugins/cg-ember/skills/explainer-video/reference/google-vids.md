# A presenter in Google Vids

Read this only when the person chose a presenter in Step 4 and their camp's Google account
has Google Vids. The person makes the presenter part in Vids, in their own camp account,
and you join the camp's opening and closing around it. You never sign in for them, and you
never click anything in Vids yourself.

What they get: a widescreen video of a made-up person reading the script, with the camp's
own opening and closing. Vids' presenters are widescreen only, so there is no phone version
of this one. The captions-only video from Steps 5 to 7 is still theirs, in both shapes.

## 1. Give them the words

Write out the presenter's words, one block per scene, numbered, with nothing else in them:
each scene's `say` line if it has one, otherwise its caption. Then say:

> Here are the presenter's words, one block per scene. Keep this message open; you'll copy
> from it in a minute.

## 2. The steps, one message, nothing else in it

Send these steps on their own, then wait. Vids changes its screens from time to time; if a
button is not where a step says, ask them what they see on their screen and work from that.

1. Click [Open Google Vids](https://docs.google.com/videos) while you are signed in to your
   camp account.
2. Check that the account in the top right corner is your camp account, not a personal one.
3. Start a new video. Keep it "Landscape".
4. Choose "AI avatar".
5. Pick a presenter. Click the small circle at the top left of their picture, then click
   "Select".
6. Name the video with the title of your video.
7. In the presenter's panel, click "Current scene", then paste the words for scene 1.
8. Click the blue "+" to add the next scene, then paste the words for that scene. Do this
   for every scene.
9. For each scene: click the scene, click "Preview", then click "Generate". Each scene takes
   one or two minutes.
10. When every scene is done, click "File", then "Download", then "MP4 video".
11. Keep this tab open until the file appears in your Downloads folder.
12. Drag that file into this chat, or tell me where it is.

## 3. Join it

When the file is here, run:

`<py> scripts/make_video.py join "<plan>" "<their downloaded file>" "<the video's folder>"`

It draws the camp's opening and closing in the same shape as their file, and joins the three
into one video. The line starting **MADE** names the file and its length. Look at a few
frames of it before telling them it is ready. Then tell them where it is, as Step 7 says,
and that it has not been posted or shared anywhere.

If they only want the opening and closing on their own, to add in Vids themselves, run
`<py> scripts/make_video.py bumpers "<plan>" "<the video's folder>"` instead.
