"""Tests for the explainer-video skill's helper, scripts/make_video.py.

    python tests/explainer_test.py

Uses an invented camp (Pine Hollow Day Camp) and an invented logo. Every check that must
refuse is paired with one that must pass, so a green result means the checks can go red:

- the plan check refuses a bad color code, a missing logo, a list with one item and a big
  word that is too long, and passes the good plan;
- the drawing refuses words too long to fit and a font that is not on the computer;
- a short video is drawn in both shapes, with a sound track, and its length matches.

The drawing checks need Playwright and a Chromium (scripts/check_tools.py says whether they
are here). Without them those checks are SKIPPED, and the count of skipped checks is printed
beside the count of failures, every time.
"""
import json, os, pathlib, re, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "plugins/cg-ember/skills/explainer-video/scripts"
MAKE = SCRIPTS / "make_video.py"
sys.path.insert(0, str(SCRIPTS))
from _ff import probe  # noqa: E402

LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="480" height="480">
<circle cx="120" cy="120" r="112" fill="#1E5631"/><path d="M120 44 L160 104 H140 L172 150 H134 V176 H106 V150 H68
L100 104 H80 Z" fill="#FFFFFF"/></svg>"""
GOOD = {
    "title": "How early pickup works", "camp": "Pine Hollow Day Camp",
    "brand": {"background": "#FBF8F1", "text": "#1F2A24", "main": "#1E5631", "accent": "#F4B942",
              "logo": "logo.svg", "heading_font": {"name": "Jost"}, "body_font": {"name": "Figtree"}},
    "scenes": [{"kind": "checklist", "words": "Bring", "items": ["Water bottle", "Sunscreen"],
                "caption": "Pack a water bottle and sunscreen.", "seconds": 3.6}],
}

fails, skips, passes = [], [], 0


def run(args):
    r = subprocess.run([sys.executable, str(MAKE), *args], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def plan(tmp, name, change=None):
    p = json.loads(json.dumps(GOOD))
    if change:
        change(p)
    f = pathlib.Path(tmp) / f"{name}.json"
    f.write_text(json.dumps(p), encoding="utf-8")
    return str(f)


def expect(label, code, out, want_code, want_text=None):
    global passes
    if code != want_code or (want_text and not re.search(want_text, out)):
        fails.append(f"{label}: exit {code}, expected {want_code}" + (f" with /{want_text}/" if want_text else "")
                     + "\n    " + out.strip()[-300:].replace("\n", "\n    "))
    else:
        passes += 1


def drawing_here():
    r = subprocess.run([sys.executable, str(SCRIPTS / "check_tools.py")], capture_output=True, text=True)
    return r.returncode == 0


def main():
    global passes
    with tempfile.TemporaryDirectory() as tmp:
        (pathlib.Path(tmp) / "logo.svg").write_text(LOGO, encoding="utf-8")
        # 1. the plan check, with no drawing (exit 2 is a plan problem)
        cases = [
            ("bad color code", lambda p: p["brand"].update(main="green"), r"main color must be a color code"),
            ("missing logo", lambda p: p["brand"].update(logo="nope.png"), r"logo file is not where"),
            ("one-item list", lambda p: p["scenes"][0].update(items=["Water bottle"]), r"2 to 5 items"),
            ("big word too long", lambda p: p["scenes"][0].update(kind="big", words="Absolutely everything"),
             r"14 letters or fewer"),
            ("no scenes", lambda p: p.update(scenes=[]), r"between 1 and 10 scenes"),
        ]
        for label, change, text in cases:
            code, out = run(["video", plan(tmp, label.replace(" ", "-"), change), tmp])
            expect(f"plan check refuses {label}", code, out, 2, text)
        if not drawing_here():
            skips.extend(["good plan draws", "too-long words refused", "missing font refused",
                          "video drawn in both shapes"])
            return
        # 2. the drawing check (exit 3 is a drawing problem)
        code, out = run(["check", plan(tmp, "good")])
        expect("the good plan draws in both shapes", code, out, 0, r"The plan is fine")
        code, out = run(["check", plan(tmp, "long", lambda p: p["scenes"][0].update(
            words="Everything a family needs to know about picking a camper up early from camp on any day "
                  "of the summer, including rainy days and trip days and special events"))])
        expect("words too long to fit are refused", code, out, 3, r"too long to fit")
        code, out = run(["check", plan(tmp, "font", lambda p: p["brand"].update(
            heading_font={"name": "No Such Font Sans 9"}))])
        expect("a font that is not on the computer is refused", code, out, 3, r"is not on this computer")
        # 3. a whole short video, both shapes
        out_dir = pathlib.Path(tmp) / "out"
        code, out = run(["video", plan(tmp, "good"), str(out_dir), "--music"])
        expect("the video is drawn", code, out, 0, r"MADE .*\(phone\)\.mp4")
        made = sorted(out_dir.glob("*.mp4"))
        if len(made) != 2:
            fails.append(f"expected 2 videos, found {len(made)}: {[m.name for m in made]}")
            return
        for m, size in zip(made, [(1080, 1920), (1920, 1080)]):
            w, h, audio, secs = probe(m)
            want = 3.4 + 0.45 + 3.6 + 0.45 + 0.5 + 2.4   # opening, hop, scene, hop, line, closing hold
            ok = (w, h) == size and audio and abs(secs - want) < 0.15
            if not ok:
                fails.append(f"{m.name}: {w}x{h}, sound {audio}, {secs:.2f} s; expected {size}, sound, {want:.2f} s")
            else:
                passes += 1
        if not list(out_dir.glob("*captions.vtt")):
            fails.append("no captions file was written")
        else:
            passes += 1


if __name__ == "__main__":
    main()
    for f in fails:
        print("FAIL", f)
    print(f"{passes} passed, {len(fails)} failed, {len(skips)} skipped" + (f" ({', '.join(skips)})" if skips else ""))
    sys.exit(1 if fails else 0)
