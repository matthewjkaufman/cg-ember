# Windows version of the second CG Ember safety check (hooks/hooks.json, second PreToolUse entry).
# Reads the tool call from standard input and exits 2 for a new calendar event that lists any
# guest, with the same pattern as the Mac and Linux grep (case-sensitive, so -cmatch). It prints
# nothing: the command in hooks.json prints the reason for any exit other than 0, so a script that
# cannot run at all also refuses, with the same reason.
$call = [Console]::In.ReadToEnd()
if ($call -cmatch '"(attendees|attendeeEmails|addedAttendees|guests|invitees)"\s*:\s*(\[\s*[^\]"\s]|\[\s*"[^"])') {
    exit 2
}
exit 0
