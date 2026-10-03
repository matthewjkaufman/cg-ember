#!/usr/bin/env bash
# Checks plugins/cg-ember/hooks/hooks.json without a model: every send-shaped tool name must be
# refused, every read, search, draft or plain-create name must pass, and the calendar check must
# refuse an event with guests and allow one without. Then it proves the check can fail, by running
# the same names against a copy of the matcher with "reply" removed.
#
#   bash tests/send-block.test.sh
#
# Tool names marked "measured" were copied from a live Claude desktop tool list on 2026-10-03
# (Gmail, Google Calendar, Google Drive, Dropbox, Egnyte, Metricool connectors; Egnyte has no
# send-shaped tool, so its names appear only in the pass list). The others are
# shapes we expect from Slack, Microsoft 365 and other connections, unmeasured.
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
H="$here/plugins/cg-ember/hooks/hooks.json"
py() { python3 "$@" 2>/dev/null || python "$@"; }
SEND_RE="$(py -c 'import json,sys;print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][0]["matcher"])' "$H")"
EVENT_RE="$(py -c 'import json,sys;print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][1]["matcher"])' "$H")"
SEND_CMD="$(py -c 'import json,sys;print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][0]["hooks"][0]["command"])' "$H")"
EVENT_CMD="$(py -c 'import json,sys;print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][1]["hooks"][0]["command"])' "$H")"
pass=0; fail=0
ok() { pass=$((pass+1)); }
bad() { fail=$((fail+1)); echo "WRONG $1"; }
# JavaScript regex is what the app uses; node when present, else Python's re (same for these constructs).
matches() { py -c 'import re,sys;sys.exit(0 if re.search(sys.argv[1],sys.argv[2]) else 1)' "$1" "$2"; }

BLOCK=(
  # measured
  mcp__c29f0049__send_message mcp__c29f0049__reply mcp__c29f0049__forward
  mcp__37427ece__respond_to_event mcp__37427ece__update_event mcp__37427ece__delete_event
  mcp__24039824__share_file
  mcp__bfa060d9__createScheduledPost mcp__bfa060d9__createScheduledPostForReview
  mcp__bfa060d9__sendScheduledPostForReview mcp__bfa060d9__updateScheduledPost
  # expected shapes, unmeasured
  mcp__claude_ai_Gmail__send_draft mcp__claude_ai_Gmail__reply_all mcp__gmail__gmail_send_email
  mcp__slack__slack_send_message mcp__slack__chat_post_message mcp__slack__post_message
  mcp__slack__slack_schedule_message mcp__slack__schedule_message
  mcp__outlook__send_mail mcp__outlook__reply_to_message mcp__outlook__forward_message
  mcp__outlook__replyAll mcp__outlook__sendMail mcp__ms365__createReplyAndSend
  mcp__calendar__cancel_event mcp__calendar__patch_event mcp__teams__send_chat_message
  mcp__drive__share_folder mcp__x__invite_user mcp__x__publish_page
  # dashes, dots and camel case (Andy, 2026-10-03)
  mcp__x__send-email mcp__x__gmail-send mcp__x__reply-to-message mcp__x__messages.send
  mcp__slack__postMessage mcp__slack__chat_postMessage mcp__x__share-file mcp__x__update-event
)
PASS_NAMES=(
  # measured
  mcp__c29f0049__create_draft mcp__c29f0049__update_draft mcp__c29f0049__delete_draft
  mcp__c29f0049__list_drafts mcp__c29f0049__get_draft mcp__c29f0049__get_message
  mcp__c29f0049__get_thread mcp__c29f0049__search_threads mcp__c29f0049__list_labels
  mcp__37427ece__list_events mcp__37427ece__get_event mcp__37427ece__search_events
  mcp__37427ece__suggest_time mcp__37427ece__list_calendars
  mcp__24039824__search_files mcp__24039824__read_file_content mcp__24039824__create_file
  mcp__24039824__update_file mcp__24039824__get_file_permissions
  mcp__1de42c91__create_shared_link mcp__1de42c91__list_shared_links mcp__1de42c91__create_file
  mcp__bfa060d9__getScheduledPosts mcp__bfa060d9__getBrandSettings
  mcp__b7bd6534__advanced_search mcp__b7bd6534__get_file_content mcp__b7bd6534__get_download_url
  mcp__b7bd6534__get_upload_url mcp__b7bd6534__list_filesystem_by_path mcp__b7bd6534__whoami
  mcp__x__list-posts mcp__x__get-thread mcp__x__create-draft
  mcp__cg-hub__hub_hello mcp__cg-hub__share_skill mcp__cg-hub__hub_save_my_page
  mcp__cg-hub__hub_suggest_page mcp__cg-hub__hub_log_problem
  mcp__scheduled-tasks__create_scheduled_task mcp__scheduled-tasks__update_scheduled_task
  # tools that are not connections must never match
  Bash Write Edit Read Task Agent Skill mcp__workspace__bash
  # near misses
  mcp__x__get_sender mcp__x__list_sent_messages mcp__x__list_replies mcp__x__list_posts
)

for n in "${BLOCK[@]}"; do matches "$SEND_RE" "$n" && ok || bad "should refuse: $n"; done
# share_skill and create_scheduled_task are the plugin's own tools; check the expected ones pass.
for n in "${PASS_NAMES[@]}"; do
  if matches "$SEND_RE" "$n"; then bad "should pass: $n"; else ok; fi
done
# share_skill is the Hub's tool for a person's own skill, which must stay usable.

# The refusal command: exit 2 with the reason on stderr.
out="$(echo '{}' | bash -c "$SEND_CMD" 2>&1 >/dev/null)"; code=$?
[ "$code" -eq 2 ] && echo "$out" | grep -q "never sends" && ok || bad "send command exit $code: $out"

# Calendar: events with guests refused, without guests allowed.
for n in mcp__37427ece__create_event mcp__x__insert_event mcp__x__createEvent; do
  matches "$EVENT_RE" "$n" && ok || bad "event matcher should catch: $n"
done
with_guest='{"tool_name":"mcp__37427ece__create_event","tool_input":{"summary":"Bus meeting","startTime":"2026-10-20T10:00:00-04:00","endTime":"2026-10-20T11:00:00-04:00","attendees":[{"email":"a@example.com"}]}}'
with_emails='{"tool_input":{"summary":"x","attendeeEmails": ["a@example.com"]}}'
no_guest='{"tool_input":{"summary":"Hold: write budget","startTime":"2026-10-20T10:00:00-04:00","endTime":"2026-10-20T11:00:00-04:00"}}'
empty_list='{"tool_input":{"summary":"Hold","attendees":[]}}'
in_text='{"tool_input":{"summary":"Hold","description":"notes say \"attendees\": [{ later"}}'
r() { echo "$1" | bash -c "$EVENT_CMD" >/dev/null 2>&1; echo $?; }
[ "$(r "$with_guest")" = 2 ] && ok || bad "event with attendees should be refused"
[ "$(r "$with_emails")" = 2 ] && ok || bad "event with attendeeEmails should be refused"
[ "$(r "$no_guest")" = 0 ] && ok || bad "event with no guests should pass"
[ "$(r "$empty_list")" = 0 ] && ok || bad "event with an empty guest list should pass"
[ "$(r "$in_text")" = 0 ] && ok || bad "the word attendees inside a description should pass"

# Red control: the same check against a matcher with "reply" removed must miss the reply tool.
broken="${SEND_RE//reply|/}"; broken="${broken//Reply|/}"
if [ "$broken" = "$SEND_RE" ]; then bad "red control did not change the matcher"
elif matches "$broken" mcp__c29f0049__reply; then bad "red control: broken matcher still caught reply"
else ok; fi

echo "$pass passed, $fail wrong"
[ "$fail" -eq 0 ]
