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
# shapes we expect from Slack, Microsoft 365 and other connections, unmeasured. The send_feedback
# exception and the draft-only scheduled post (2026-10-07) are explained in the readme, "For the
# maintainer".
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
H="$here/plugins/cg-ember/hooks/hooks.json"
py() { python3 "$@" 2>/dev/null || python "$@"; }
SEND_RE="$(py -c 'import json,sys;print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][0]["matcher"])' "$H")"
EVENT_RE="$(py -c 'import json,sys;print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][1]["matcher"])' "$H")"
SEND_CMD="$(py -c 'import json,sys;print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][0]["hooks"][0]["command"])' "$H")"
EVENT_CMD="$(py -c 'import json,sys;print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][1]["hooks"][0]["command"])' "$H")"
DRAFT_RE="$(py -c 'import json,sys;print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][2]["matcher"])' "$H")"
DRAFT_CMD="$(py -c 'import json,sys;print(json.load(open(sys.argv[1]))["hooks"]["PreToolUse"][2]["hooks"][0]["command"])' "$H")"
pass=0; fail=0
ok() { pass=$((pass+1)); }
bad() { fail=$((fail+1)); echo "WRONG $1"; }
# Claude uses JavaScript regular expressions and ChatGPT uses Rust's regex crate; Python's re agrees
# with both on every construct used here (Trevor confirmed Claude with a real hook run, 2026-10-03;
# tests/chatgpt_checks.py refuses constructs Rust lacks).
matches() { py -c 'import re,sys;sys.exit(0 if re.search(sys.argv[1],sys.argv[2]) else 1)' "$1" "$2"; }

BLOCK=(
  # measured
  mcp__c29f0049__send_message mcp__c29f0049__reply mcp__c29f0049__forward
  mcp__37427ece__respond_to_event mcp__37427ece__update_event mcp__37427ece__delete_event
  mcp__24039824__share_file
  mcp__bfa060d9__sendScheduledPostForReview mcp__bfa060d9__updateScheduledPost
  # emails its reviewers (measured from the tool's own description, 2026-10-07)
  mcp__bfa060d9__createScheduledPostForReview
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
  # letter case and run-together names (Trevor, 2026-10-03)
  mcp__x__GMAIL_SEND_EMAIL mcp__x__Send_Email mcp__x__sendemail mcp__x__sendmail mcp__x__replyall
  mcp__x__chat_postmessage mcp__x__SLACK_SEND_MESSAGE mcp__x__OUTLOOK_REPLY_EMAIL
  # the two exceptions are exact names; anything longer or prefixed still counts as sending (2026-10-07)
  mcp__x__send_feedback_email mcp__x__sendFeedbackEmail mcp__x__send_feedback_to_parents
  mcp__x__gmail_send_feedback mcp__x__send_note mcp__x__sendNote mcp__x__send_message_feedback
  mcp__x__createScheduledPostNow mcp__x__createScheduledPostAndPublish mcp__x__createPost
  mcp__x__publishScheduledPost mcp__x__create_post mcp__x__publish_post mcp__x__post_now
  mcp__x__schedule_post mcp__slack__schedule_message
  # other letter cases and spellings of the exceptions still count as sending
  mcp__x__SEND_FEEDBACK mcp__x__Send_Feedback mcp__x__send_Feedback mcp__x__sendFeedback
  mcp__x__send-feedback mcp__x__send_feedbacks mcp__x__send_ mcp__x__send
  mcp__x__create_scheduled_post mcp__x__create_scheduled_post_for_review
  mcp__x__createScheduledPostForReviewNow
  mcp__x__createSchedulePost mcp__x__createScheduledPostForRevie
  # letter cases 0.2.0 let through (Andy, 2026-10-07)
  mcp__x__createscheduledpost mcp__x__CreateScheduledPost mcp__x__SchedulePost mcp__x__CreatePost
  mcp__x__PostTweet mcp__x__schedulepost mcp__x__PUBLISHPOST mcp__x__CreateScheduledPostForReview
  # ChatGPT shapes, unmeasured: Codex runs ChatGPT's own connections through a server named
  # codex_apps (codex-rs source, 2026-10-04); the tool names after it are guesses until a
  # real ChatGPT tool list is copied in.
  mcp__codex_apps__gmail_send_email mcp__codex_apps__gmail_reply_to_email
  mcp__codex_apps__outlook_email_send_message mcp__codex_apps__gmail_forward_email
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
  mcp__bfa060d9__getBestTimeToPostByNetwork mcp__bfa060d9__getAnalyticsDataByMetrics mcp__x__getPostAnalytics
  mcp__x__GMAIL_LIST_DRAFTS mcp__x__GMAIL_FETCH_EMAILS mcp__x__get_sender mcp__x__sender_info mcp__x__repost_count
  mcp__cg-hub__hub_hello mcp__cg-hub__share_skill mcp__cg-hub__hub_save_my_page
  mcp__cg-hub__hub_suggest_page mcp__cg-hub__hub_log_problem
  mcp__scheduled-tasks__create_scheduled_task mcp__scheduled-tasks__update_scheduled_task
  # files a note inside the person's own office system and sends nothing outside (measured 2026-10-07)
  mcp__0917fdf5__send_feedback
  # passes this pattern only to meet the draft-only check below (measured 2026-10-07)
  mcp__bfa060d9__createScheduledPost
  # names with "post" inside that do not post
  mcp__x__getPostalCode mcp__x__compost_report mcp__x__Postcode_lookup
  # tools that are not connections must never match
  Bash Write Edit Read Task Agent Skill mcp__workspace__bash
  # near misses
  mcp__x__get_sender mcp__x__list_sent_messages mcp__x__list_replies mcp__x__list_posts
)

for n in "${BLOCK[@]}"; do matches "$SEND_RE" "$n" && ok || bad "should refuse: $n"; done
# share_skill is the Hub's tool and create_scheduled_task the app's; both must stay usable.
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
broken="${SEND_RE//reply|/}"; broken="${broken//Reply|/}"; broken="${broken//\[rR\]\[eE\]\[pP\]\[lL\]\[yY\]|/}"
if [ "$broken" = "$SEND_RE" ]; then bad "red control did not change the matcher"
elif matches "$broken" mcp__c29f0049__reply; then bad "red control: broken matcher still caught reply"
else ok; fi

# The pattern in hooks.json is built by tests/send_matcher.py; it must hold exactly that output.
built="$(py "$here/tests/send_matcher.py")"
[ "$built" = "$SEND_RE" ] && ok || bad "hooks.json does not hold the pattern tests/send_matcher.py builds"
# Red control for the exceptions: the 0.2.0 pattern, before they were carved out, must still
# refuse each of them, so the pass list above can fail.
base="$(py "$here/tests/send_matcher.py" --base)"
if [ "$base" = "$SEND_RE" ]; then bad "exception red control: base pattern is the same as the shipped one"
else
  for n in mcp__0917fdf5__send_feedback mcp__bfa060d9__createScheduledPost; do
    matches "$base" "$n" && ok || bad "exception red control: the 0.2.0 pattern let $n through"
  done
fi
# The scheduled-post check: only createScheduledPost, and only when its "info" (a JSON string)
# says draft is true. Measured 2026-10-07: without draft it publishes on its own at the time.
for n in mcp__bfa060d9__createScheduledPost mcp__x__createScheduledPost; do
  matches "$DRAFT_RE" "$n" && ok || bad "draft check should catch: $n"
done
for n in mcp__x__createScheduledPostForReview mcp__x__createscheduledpost mcp__x__xcreateScheduledPost; do
  matches "$DRAFT_RE" "$n" && bad "draft check should not catch: $n" || ok
done
dr() { echo "$1" | bash -c "$2" >/dev/null 2>&1; echo $?; }
d_true='{"tool_name":"mcp__bfa060d9__createScheduledPost","tool_input":{"info":"{\"text\":\"Open house Saturday\",\"draft\":true,\"autoPublish\":true}"}}'
d_false='{"tool_input":{"info":"{\"text\":\"Hi\",\"draft\":false}"}}'
d_missing='{"tool_input":{"info":"{\"text\":\"Hi\"}"}}'
d_string='{"tool_input":{"info":"{\"text\":\"Hi\",\"draft\":\"true\"}"}}'
d_broken='{"tool_input":{"info":"{draft: true"}}'
d_noinfo='{"tool_input":{"text":"Hi","draft":true}}'
d_intext='{"tool_input":{"info":"{\"text\":\"say \\\"draft\\\": true here\"}"}}'
d_nested='{"tool_input":{"info":"{\"text\":\"Hi\",\"extra\":{\"draft\":true}}"}}'
[ "$(dr "$d_true" "$DRAFT_CMD")" = 0 ] && ok || bad "draft check should allow draft true"
for c in d_false d_missing d_string d_broken d_noinfo d_intext d_nested; do
  [ "$(dr "${!c}" "$DRAFT_CMD")" = 2 ] && ok || bad "draft check should refuse: $c"
done
out="$(echo "$d_false" | bash -c "$DRAFT_CMD" 2>&1 >/dev/null)"
echo "$out" | grep -q "draft" && ok || bad "draft check refusal has no reason: $out"
# Red control: a check that never looks at draft must let the false case through.
broken_d="${DRAFT_CMD//d.get(\"draft\") is True/True}"
if [ "$broken_d" = "$DRAFT_CMD" ]; then bad "draft red control did not change the check"
elif [ "$(dr "$d_false" "$broken_d")" = 0 ]; then ok
else bad "draft red control: the broken check still refused draft false"; fi
# No Python at all must refuse, never allow.
[ "$(echo "$d_true" | env PATH=/nonexistent /bin/bash -c "$DRAFT_CMD" >/dev/null 2>&1; echo $?)" = 2 ] \
  && ok || bad "draft check without Python should refuse"
# Every other failure must also end in exit 2: a hook exit other than 2 lets the tool call through.
for c in "" "not json {"; do
  [ "$(dr "$c" "$DRAFT_CMD")" = 2 ] && ok || bad "draft check should refuse input: '$c'"
done
stub="$(mktemp -d)"
printf '#!/bin/sh
exit 1
' > "$stub/python3"; chmod +x "$stub/python3"
[ "$(echo "$d_true" | env PATH="$stub" /bin/bash -c "$DRAFT_CMD" >/dev/null 2>&1; echo $?)" = 2 ]   && ok || bad "draft check with a Python that crashes should refuse"
printf '#!/bin/sh
kill -9 $$
' > "$stub/python3"
[ "$(echo "$d_true" | env PATH="$stub" /bin/bash -c "$DRAFT_CMD" >/dev/null 2>&1; echo $?)" = 2 ]   && ok || bad "draft check with a Python that is killed should refuse"
rm -rf "$stub"

# ChatGPT reads these patterns with Rust's regex engine: no lookaround, no backreferences.
case "$SEND_RE" in *'(?'*) bad "send pattern uses (? which Rust's regex engine may refuse";; *) ok;; esac

echo "$pass passed, $fail wrong"
[ "$fail" -eq 0 ]
