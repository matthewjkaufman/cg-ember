# Windows version of the first CG Ember safety check (hooks/hooks.json, first PreToolUse entry).
# The matcher has already picked a send-shaped tool; this only refuses it, as the Mac and
# Linux command does: the reason goes to the error stream and exit code 2 refuses the call.
[Console]::Error.WriteLine('Nothing is wrong. CG Ember never sends, replies, forwards, posts, shares, invites or changes an existing calendar event. Do not try another way. Write it as a draft where the person sends things from (an email reply is a new draft in that thread), and tell them in one sentence where the draft is.')
exit 2
