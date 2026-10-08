"""Checks that keep one CG Ember plugin working in both Claude and ChatGPT.

    python tests/chatgpt_checks.py [plugin folder]     (default: plugins/cg-ember)

Prints one line per problem and exits 1 if there is any. tests/chatgpt.test.sh runs it on
the real plugin and on broken copies (the red controls), so each check is shown to fail.

What it checks:
1. hooks.json uses only fields that both apps read. Codex refuses an unknown field in the
   file's top level (codex-rs/config/src/hook_config.rs, `deny_unknown_fields`), so one
   stray key would switch the whole safety check off there.
2. The hook patterns use nothing Rust's regex engine lacks (Codex compiles them with the
   `regex` crate: no lookaround, no backreferences).
3. On Windows: each commandWindows, run through cmd.exe exactly as Codex runs it
   (codex-rs/hooks/src/engine/command_runner.rs: `cmd.exe /C "<command>"`), refuses and
   allows the same cases as the Mac and Linux commands in send-block.test.sh, for all three
   checks: sending, calendar guests, and a scheduled post that is not a draft.
4. Every skill carries the same never-send sentence (camp-background holds the full rule).
5. No skill names Claude's screens or Claude itself outside screens-claude.md, apart from
   the lines on the allow list below.
6. Both screens pages have the same sections, A to H.
7. Descriptions: each at most 400 characters, all together at most 6,500 (the readme's
   rule, under Codex's 8,000-character budget for the skill list).
"""
import glob
import json
import os
import re
import subprocess
import sys

NEVER_SEND = "Emails, messages, invitations and posts are drafted, never sent, as camp-background section 1 says."
CLAUDE_WORDS = re.compile(r"\b(Claude|Cowork|Customize|Capabilities|Anthropic)\b")
# Lines that may name Claude because they are about both apps.
ALLOWED = [
    "This plugin works in Claude (in Cowork or in Claude chat) and in the ChatGPT app.",
    "`reference/screens-claude.md` in this skill's folder if you are Claude, or",
    "follow written instructions. Claude's Cowork and the Codex part of the ChatGPT app are",
    "- You can now use CG Ember in the ChatGPT app as well as in Claude.",
    # The Hub's own share page labels its upload box with these words, whichever app saved it.
    '3. Click "Choose File" or "Browse..." under "The file Claude saved".',
]
HOOK_TOP = {"description", "hooks"}
HOOK_GROUP = {"matcher", "hooks"}
# Every field Codex's command handler reads (codex-rs/config/src/hook_config.rs,
# HookHandlerConfig::Command, read 2026-10-04); Claude reads type, command and timeout.
HOOK_HANDLER = {"type", "command", "commandWindows", "timeout", "async", "statusMessage",
                "additionalContextLimit"}
NOT_IN_RUST = [r"(?=", r"(?!", r"(?<=", r"(?<!", r"(?>", r"(?P=", r"\Z", r"\G", "*+", "++", "?+"]

WITH_GUEST = '{"tool_name":"mcp__37427ece__create_event","tool_input":{"summary":"Bus meeting","attendees":[{"email":"a@example.com"}]}}'
WITH_EMAILS = '{"tool_input":{"summary":"x","attendeeEmails": ["a@example.com"]}}'
NO_GUEST = '{"tool_input":{"summary":"Hold: write budget","startTime":"2026-10-20T10:00:00-04:00"}}'
EMPTY_LIST = '{"tool_input":{"summary":"Hold","attendees":[]}}'
IN_TEXT = '{"tool_input":{"summary":"Hold","description":"notes say \\"attendees\\": [{ later"}}'
# The draft-only scheduled post, the same cases as send-block.test.sh.
D_TRUE = '{"tool_name":"mcp__bfa060d9__createScheduledPost","tool_input":{"info":"{\\"text\\":\\"Open house Saturday\\",\\"draft\\":true,\\"autoPublish\\":true}"}}'
D_OBJECT = '{"tool_input":{"info":{"text":"Hi","draft":true}}}'
D_FALSE = '{"tool_input":{"info":"{\\"text\\":\\"Hi\\",\\"draft\\":false}"}}'
D_STRING = '{"tool_input":{"info":"{\\"text\\":\\"Hi\\",\\"draft\\":\\"true\\"}"}}'
D_CASE = '{"tool_input":{"info":"{\\"text\\":\\"Hi\\",\\"Draft\\":true}"}}'
D_BROKEN = '{"tool_input":{"info":"{draft: true"}}'
D_NOINFO = '{"tool_input":{"text":"Hi","draft":true}}'
D_INTEXT = '{"tool_input":{"info":"{\\"text\\":\\"say \\\\\\"draft\\\\\\": true here\\"}"}}'
D_NESTED = '{"tool_input":{"info":"{\\"text\\":\\"Hi\\",\\"extra\\":{\\"draft\\":true}}"}}'


def main(plugin):
    problems = []
    skipped = []

    def bad(msg):
        problems.append(msg)

    # 1 and 2: the hooks file.
    hooks = json.load(open(os.path.join(plugin, "hooks", "hooks.json"), encoding="utf-8"))
    for key in set(hooks) - HOOK_TOP:
        bad(f"hooks.json: field {key!r} would make ChatGPT ignore the whole file")
    groups = hooks.get("hooks", {}).get("PreToolUse", [])
    for g in groups:
        for key in set(g) - HOOK_GROUP:
            bad(f"hooks.json: group field {key!r} is not one ChatGPT reads")
        m = g.get("matcher", "")
        for c in NOT_IN_RUST:
            if c in m:
                bad(f"hooks.json: matcher uses {c}, which ChatGPT's pattern engine cannot read")
        if re.search(r"\\[1-9]", m):
            bad("hooks.json: matcher uses a backreference, which ChatGPT's pattern engine cannot read")
        for h in g.get("hooks", []):
            for key in set(h) - HOOK_HANDLER:
                bad(f"hooks.json: handler field {key!r} is not one ChatGPT reads")
            if "commandWindows" not in h:
                bad("hooks.json: a check has no commandWindows, so it would not run on Windows in ChatGPT")

    # 3: the Windows commands, run the way Codex runs them.
    if os.name == "nt" and len(groups) != 3:
        bad(f"hooks.json has {len(groups)} checks, expected 3, so the Windows cases cannot run")
    elif os.name == "nt":
        # Codex sets both names (codex-rs/hooks/src/engine/discovery.rs); start from neither.
        base_env = {k: v for k, v in os.environ.items() if k not in ("PLUGIN_ROOT", "CLAUDE_PLUGIN_ROOT")}
        env = dict(base_env, PLUGIN_ROOT=os.path.abspath(plugin), CLAUDE_PLUGIN_ROOT=os.path.abspath(plugin))

        def run(cmd, stdin, e=None):
            p = subprocess.run('cmd.exe /C "' + cmd + '"', input=stdin.encode("utf-8"),
                               capture_output=True, env=e or env, timeout=60)
            return p.returncode, p.stderr.decode(errors="ignore")

        send_cmd = groups[0]["hooks"][0].get("commandWindows", "")
        event_cmd = groups[1]["hooks"][0].get("commandWindows", "")
        draft_cmd = groups[2]["hooks"][0].get("commandWindows", "")
        code, err = run(send_cmd, "{}")
        if code != 2 or "never sends" not in err:
            bad(f"Windows send check: exit {code}, expected 2 with the reason")
        for name, case, want in [("event with attendees", WITH_GUEST, 2),
                                 ("event with attendeeEmails", WITH_EMAILS, 2),
                                 ("event with no guests", NO_GUEST, 0),
                                 ("event with an empty guest list", EMPTY_LIST, 0),
                                 ("the word attendees inside a description", IN_TEXT, 0)]:
            code, err = run(event_cmd, case)
            if code != want:
                bad(f"Windows calendar check, {name}: exit {code}, expected {want}")
            if want == 2 and "never adds an event with guests" not in err:
                bad(f"Windows calendar check, {name}: the reason is missing")
        # Fails closed: when its script cannot run, the calendar check refuses.
        code, err = run(event_cmd, NO_GUEST, base_env)
        if code != 2 or "never adds an event with guests" not in err:
            bad(f"Windows calendar check with its script unreachable: exit {code}, expected 2 (it fails open)")
        for name, case, want in [("draft true, info as text", D_TRUE, 0),
                                 ("draft true, info as an object", D_OBJECT, 0),
                                 ("draft false", D_FALSE, 2),
                                 ("draft as the word true in quotes", D_STRING, 2),
                                 ("Draft with a capital", D_CASE, 2),
                                 ("info that is not JSON", D_BROKEN, 2),
                                 ("no info at all", D_NOINFO, 2),
                                 ("the word draft inside the text", D_INTEXT, 2),
                                 ("draft true one level down", D_NESTED, 2)]:
            code, err = run(draft_cmd, case)
            if code != want:
                bad(f"Windows draft check, {name}: exit {code}, expected {want}")
            if want == 2 and "only makes a scheduled post as a draft" not in err:
                bad(f"Windows draft check, {name}: the reason is missing")
        code, err = run(draft_cmd, D_TRUE, base_env)
        if code != 2 or "only makes a scheduled post as a draft" not in err:
            bad(f"Windows draft check with its script unreachable: exit {code}, expected 2 (it fails open)")
    else:
        skipped.append("17 Windows command cases (not on Windows)")

    # 4 to 7: the skills.
    skills = sorted(glob.glob(os.path.join(plugin, "skills", "*", "SKILL.md")))
    total = 0
    for f in skills:
        name = os.path.basename(os.path.dirname(f))
        text = open(f, encoding="utf-8").read()
        if name == "camp-background":
            if "**drafted, never sent**" not in text:
                bad("camp-background: section 1's never-send rule is missing")
        elif NEVER_SEND not in text:
            bad(f"{name}: the never-send sentence is missing")
        m = re.search(r'^description: "(.*)"$', text, re.M)
        if not m:
            bad(f"{name}: no description line")
        else:
            total += len(m.group(1))
            if len(m.group(1)) > 400:
                bad(f"{name}: description is {len(m.group(1))} characters, over 400")
    if total > 6500:
        bad(f"all descriptions together are {total} characters, over 6,500")
    for f in glob.glob(os.path.join(plugin, "skills", "**", "*.md"), recursive=True):
        if os.path.basename(f) == "screens-claude.md":
            continue
        for i, line in enumerate(open(f, encoding="utf-8"), 1):
            if CLAUDE_WORDS.search(line) and not any(a in line for a in ALLOWED):
                rel = os.path.relpath(f, plugin)
                bad(f"{rel}:{i}: names Claude or its screens outside screens-claude.md")
    ref = os.path.join(plugin, "skills", "camp-background", "reference")
    sections = {}
    for app in ("claude", "chatgpt"):
        p = os.path.join(ref, f"screens-{app}.md")
        sections[app] = re.findall(r"^## ([A-Z])\. ", open(p, encoding="utf-8").read(), re.M) if os.path.exists(p) else []
    if sections["claude"] != list("ABCDEFGH") or sections["chatgpt"] != list("ABCDEFGH"):
        bad(f"screens pages: sections differ or are missing: {sections}")

    for p in problems:
        print("WRONG " + p)
    for s in skipped:
        print("SKIPPED " + s)
    print(f"{len(problems)} wrong, {len(skipped)} skipped groups, {len(skills)} skills, descriptions {total} characters")
    return 1 if problems else 0


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "plugins", "cg-ember")))
