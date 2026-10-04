#!/usr/bin/env bash
# Runs tests/chatgpt_checks.py on the real plugin, then on broken copies that must fail
# (the red controls), so a green result means the checks can actually go red.
#
#   bash tests/chatgpt.test.sh
#
# The Windows command cases run only on Windows; elsewhere the output says how many were
# skipped. Prints the safety check's fingerprint: ChatGPT asks people to approve the check
# again whenever hooks/hooks.json changes, so a new fingerprint means the release's
# whats-new entry must say so (see the readme, "For the maintainer").
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
P="$here/plugins/cg-ember"
PY="$(command -v python3 || command -v python)"
py() { "$PY" "$@"; }
fail=0

echo "== the plugin"
base="$(py "$here/tests/chatgpt_checks.py" "$P")" || fail=1
echo "$base"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
control() {  # control <label> <python that breaks the copy at sys.argv[1]>
  local c="$tmp/$1"
  cp -r "$P" "$c"
  py -c "$2" "$c"
  # A control counts only when it reports a problem the plugin itself does not have, so a
  # failing plugin cannot make every control look red.
  local out new
  out="$(py "$here/tests/chatgpt_checks.py" "$c")"
  new="$(comm -13 <(echo "$base" | grep '^WRONG' | sed "s#$P##" | sort) <(echo "$out" | grep '^WRONG' | sed "s#$c##" | sort))"
  if [ -n "$new" ]; then
    echo "ok red control failed as it should: $1"
  else
    echo "WRONG red control did not fail: $1"; fail=1
  fi
}

echo "== red controls"
control drop-never-send '
import sys,os; f=os.path.join(sys.argv[1],"skills","pick-up","SKILL.md"); s=open(f,encoding="utf-8").read()
open(f,"w",encoding="utf-8").write(s.replace("Emails, messages, invitations and posts are drafted, never sent","Drafts only"))'
control plant-customize '
import sys,os; f=os.path.join(sys.argv[1],"skills","wrap-up","SKILL.md")
open(f,"a",encoding="utf-8").write("\nClick Customize, then Skills.\n")'
control unknown-hook-field '
import sys,os,json; f=os.path.join(sys.argv[1],"hooks","hooks.json"); d=json.load(open(f,encoding="utf-8"))
d["version"]="1"; json.dump(d,open(f,"w",encoding="utf-8"))'
control lookahead-in-matcher '
import sys,os,json; f=os.path.join(sys.argv[1],"hooks","hooks.json"); d=json.load(open(f,encoding="utf-8"))
d["hooks"]["PreToolUse"][0]["matcher"]="^mcp__(?!x).*send.*$"; json.dump(d,open(f,"w",encoding="utf-8"))'
control long-description '
import sys,os,re; f=os.path.join(sys.argv[1],"skills","whats-new","SKILL.md"); s=open(f,encoding="utf-8").read()
open(f,"w",encoding="utf-8").write(re.sub(r"^description: \"", "description: \"" + "x"*400, s, count=1, flags=re.M))'
control missing-screens-section '
import sys,os; f=os.path.join(sys.argv[1],"skills","camp-background","reference","screens-chatgpt.md"); s=open(f,encoding="utf-8").read()
open(f,"w",encoding="utf-8").write(s.replace("## G. ","## Removing "))'
if [ "${OS:-}" = "Windows_NT" ]; then
  control windows-send-lets-through '
import sys,os,json; f=os.path.join(sys.argv[1],"hooks","hooks.json"); d=json.load(open(f,encoding="utf-8"))
h=d["hooks"]["PreToolUse"][0]["hooks"][0]; h["commandWindows"]=h["commandWindows"].replace("exit /b 2","exit /b 0"); json.dump(d,open(f,"w",encoding="utf-8"))'
  control windows-calendar-fails-open '
import sys,os,json; f=os.path.join(sys.argv[1],"hooks","hooks.json"); d=json.load(open(f,encoding="utf-8"))
h=d["hooks"]["PreToolUse"][1]["hooks"][0]; h["commandWindows"]=h["commandWindows"].split(" || ")[0]; json.dump(d,open(f,"w",encoding="utf-8"))'
  control windows-wrong-root-variable '
import sys,os,json; f=os.path.join(sys.argv[1],"hooks","hooks.json"); d=json.load(open(f,encoding="utf-8"))
h=d["hooks"]["PreToolUse"][1]["hooks"][0]; h["commandWindows"]=h["commandWindows"].replace("%PLUGIN_ROOT%","%NOPE%"); json.dump(d,open(f,"w",encoding="utf-8"))'
  control windows-guests-pattern-broken '
import sys,os; f=os.path.join(sys.argv[1],"hooks","calendar-guests.ps1"); s=open(f,encoding="utf-8").read()
open(f,"w",encoding="utf-8").write(s.replace("attendees|",""))'
else
  echo "SKIPPED 4 Windows red controls (not on Windows)"; skips=4
fi

echo "== safety check fingerprint (hooks/hooks.json)"
py -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest()[:16])' "$P/hooks/hooks.json"

skips="${skips:-0}"
[ "$fail" -eq 0 ] && echo "all ChatGPT checks passed ($skips red controls skipped; see any SKIPPED lines above)" || echo "ChatGPT checks FAILED"
[ "$fail" -eq 0 ]
