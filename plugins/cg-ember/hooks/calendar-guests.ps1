# Windows version of the second CG Ember safety check (hooks/hooks.json, second PreToolUse entry).
# Reads the tool call from standard input and refuses a new calendar event that lists any guest,
# with the same pattern as the Mac and Linux grep (case-sensitive, so -cmatch).
$call = [Console]::In.ReadToEnd()
if ($call -cmatch '"(attendees|attendeeEmails|addedAttendees|guests|invitees)"\s*:\s*(\[\s*[^\]"\s]|\[\s*"[^"])') {
    [Console]::Error.WriteLine('Nothing is wrong. CG Ember never adds an event with guests, because that emails every guest. Create it with no guests, or write out the event details so the person can add it themselves.')
    exit 2
}
exit 0
