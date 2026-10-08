"""Builds the send block's pattern in plugins/cg-ember/hooks/hooks.json.

    python tests/send_matcher.py            print the pattern hooks.json should hold
    python tests/send_matcher.py --write    write it into hooks.json
    python tests/send_matcher.py --base     print the pattern before the exceptions

BASE is the 0.2.0 pattern, unchanged. EXCEPTIONS are whole tool names that send nothing
beyond the person's own tool (the readme, "For the maintainer", says why each one is safe).
The pattern cannot simply skip a name, because ChatGPT reads these patterns with Rust's
regex engine, which has no lookahead. So each exception is carved out by rewriting the one
part of BASE that caught it, spelling out "anything except this word" letter by letter.
tests/send-block.test.sh checks that hooks.json holds exactly this output, and uses --base
as its red control: the base pattern must still refuse every exception.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, '..', 'plugins', 'cg-ember', 'hooks', 'hooks.json')

BASE = (
    r"^mcp__.+__(([A-Za-z0-9]+[_.-])*([sS][eE][nN][dD]|[rR][eE][pP][lL][yY]|[fF][oO][rR][wW][aA][rR][dD]"
    r"|[rR][eE][sS][pP][oO][nN][dD]|[iI][nN][vV][iI][tT][eE]|[pP][oO][sS][tT]|[pP][uU][bB][lL][iI][sS][hH])"
    r"([_.-][A-Za-z0-9_.-]*)?|([A-Za-z0-9]+[_.-])*share[_.-](file|folder|document|doc|item|drive[_.-]item|with)"
    r"([_.-][A-Za-z0-9_.-]*)?|[A-Za-z0-9_.-]*(Send|Reply|Forward|Respond|Invite|Publish)([A-Z][A-Za-z0-9]*)?"
    r"|([A-Za-z0-9]+[_.-])*(send|reply|forward|respond|invite|post|publish)[A-Z][A-Za-z0-9]*"
    r"|([A-Za-z0-9]+[_.-])*([sS][eE][nN][dD]|[rR][eE][pP][lL][yY]|[fF][oO][rR][wW][aA][rR][dD]|[pP][oO][sS][tT])"
    r"([eE][mM][aA][iI][lL]|[mM][aA][iI][lL]|[mM][eE][sS][sS][aA][gG][eE]|[mM][eE][sS][sS][aA][gG][eE][sS]"
    r"|[aA][lL][lL]|[dD][rR][aA][fF][tT]|[nN][oO][wW])([_.-][A-Za-z0-9_.-]*)?"
    r"|[A-Za-z0-9_.-]*share(File|Folder|Document|Item)[A-Za-z0-9]*|[A-Za-z0-9_.-]*Share(File|Folder|Document|Item)[A-Za-z0-9]*"
    r"|(create|send|publish|update|schedule)[A-Za-z0-9]*Post[A-Za-z0-9]*"
    r"|[A-Za-z0-9_.-]*schedule[_.-]?(message|send)[A-Za-z0-9_.-]*|[A-Za-z0-9_.-]*scheduled[_.-]send[A-Za-z0-9_.-]*"
    r"|([A-Za-z0-9]+[_.-])*(update|delete|patch|move|cancel)[_.-]event([_.-][A-Za-z0-9_.-]*)?"
    r"|(update|delete|patch|move|cancel)[A-Za-z0-9]*Event[A-Za-z0-9]*)$"
)

# The exceptions, exactly. Nothing longer, prefixed, or in another letter case passes.
EXCEPTIONS = ['send_feedback', 'createScheduledPost', 'createScheduledPostForReview']

ALNUM = [chr(c) for c in range(ord('A'), ord('Z') + 1)] + \
        [chr(c) for c in range(ord('a'), ord('z') + 1)] + [chr(c) for c in range(ord('0'), ord('9') + 1)]
ALNUM_SEP = ALNUM + ['_', '.', '-']


def cls(chars):
    """A character class for chars, written as ranges, with '-' last."""
    order = {c: i for i, c in enumerate(ALNUM_SEP)}
    chars = sorted(set(chars), key=lambda c: order[c])
    out, run = [], []
    def flush():
        if len(run) > 2:
            out.append(run[0] + '-' + run[-1])
        else:
            out.extend(run)
    tail = ''
    for c in chars:
        if c == '-':
            tail = '-'
            continue
        if run and c.isalnum() and run[-1].isalnum() and ord(c) == ord(run[-1]) + 1 \
                and c.isdigit() == run[-1].isdigit() and c.isupper() == run[-1].isupper():
            run.append(c)
        else:
            flush()
            run = [c]
    flush()
    return '[' + ''.join(out) + tail + ']'


def not_word(w, alphabet, allow_empty=True):
    """Every string over alphabet except w (and except '' when allow_empty is False)."""
    a = cls(alphabet)
    parts = []
    for i in range(len(w)):
        if i > 0:
            parts.append(w[:i])  # a proper beginning of w
        parts.append(w[:i] + cls([c for c in alphabet if c != w[i]]) + a + '*')
    parts.append(w + a + '+')
    # An empty choice is written as a trailing "?", never as "(|...)", which some engines refuse.
    return '(' + '|'.join(parts) + ')' + ('?' if allow_empty else '')


def build():
    s = BASE
    # 1. send_feedback. The first part of BASE caught it as the verb "send" with "_feedback"
    #    after it. Take "send" out of that verb list and add it back in three pieces: with a
    #    word in front, in any letter case other than "send", and as "send" followed by
    #    anything except "_feedback".
    head = r"^mcp__.+__(([A-Za-z0-9]+[_.-])*([sS][eE][nN][dD]|"
    assert s.count(head) == 1
    upper_send = r"([S][eE][nN][dD]|s[E][nN][dD]|se[N][dD]|sen[D])"
    send_parts = (
        r"([A-Za-z0-9]+[_.-])+[sS][eE][nN][dD]([_.-][A-Za-z0-9_.-]*)?"
        + "|" + upper_send + r"([_.-][A-Za-z0-9_.-]*)?"
        + r"|send([.-][A-Za-z0-9_.-]*|_" + not_word('feedback', ALNUM_SEP) + ")?"
    )
    s = s.replace(head, r"^mcp__.+__(" + send_parts + r"|([A-Za-z0-9]+[_.-])*(", 1)
    # 2. createScheduledPost and createScheduledPostForReview. BASE caught them as
    #    "create", anything, "Post", anything. Keep that for every middle except "Scheduled",
    #    and after "createScheduledPost" refuse anything except nothing or "ForReview".
    post = r"(create|send|publish|update|schedule)[A-Za-z0-9]*Post[A-Za-z0-9]*"
    assert s.count(post) == 1
    s = s.replace(post,
                  r"(send|publish|update|schedule)[A-Za-z0-9]*Post[A-Za-z0-9]*"
                  + "|create" + not_word('Scheduled', ALNUM) + r"Post[A-Za-z0-9]*"
                  + "|createScheduledPost" + not_word('ForReview', ALNUM, allow_empty=False))
    return s


if __name__ == '__main__':
    if '--base' in sys.argv:
        print(BASE)
    elif '--write' in sys.argv:
        text = open(HOOKS, encoding='utf-8').read()
        data = json.loads(text)
        old = data['hooks']['PreToolUse'][0]['matcher']
        new = build()
        text = text.replace(json.dumps(old)[1:-1], json.dumps(new)[1:-1], 1)
        assert json.loads(text)['hooks']['PreToolUse'][0]['matcher'] == new
        open(HOOKS, 'w', encoding='utf-8', newline='\n').write(text)
        print('written')
    else:
        print(build())
