"""Make a short explainer video for a camp from an approved plan, drawn entirely in code.

  python make_video.py check   plan.json                    checks the plan and that every scene fits
  python make_video.py stills  plan.json <folder>           one picture per scene, both shapes, plus a sheet
  python make_video.py video   plan.json <folder> [options] the finished video
  python make_video.py bumpers plan.json <folder>           the camp's opening and closing alone (widescreen)
  python make_video.py join    plan.json presenter.mp4 <folder>   opening + a presenter video + closing
  python make_video.py voices                               the built-in computer voices here, if any

video options:
  --shape both | phone | widescreen   (default both; phone is 1080x1920, widescreen 1920x1080)
  --music                              a short CC0 steel-drum tune under the opening and the closing
  --voice "<voice name>"               read each scene's caption aloud with a built-in computer voice
  --fps 30

The plan (JSON), with paths relative to the plan file:
  {"title": "How early pickup works", "camp": "Pine Hollow Day Camp",
   "brand": {"background": "#FFFFFF", "text": "#1B2A41", "main": "#1F4E79", "accent": "#F2A900",
             "logo": "logo.png",                       optional; used exactly as given
             "heading_font": {"name": "Jost"},         a font that comes with this skill (Jost, Figtree),
             "body_font": {"name": "Figtree"}},        one installed here by name, or {"name", "file"}
   "scenes": [{"kind": "headline", "words": "Early pickup", "small": "optional line",
               "caption": "What the captions say.", "say": "optional spoken copy, spelled by sound"},
              {"kind": "big", "words": "3:15 PM", "small": "...", "caption": "..."},
              {"kind": "steps" | "checklist", "words": "...", "items": ["...", "..."], "caption": "..."}]}

Every problem is printed in plain words with "PROBLEM:" in front, and the script exits 2 (the
plan) or 3 (the drawing). Nothing here sends, uploads or posts anything; it writes files into
<folder> only.
"""
import argparse, datetime, json, os, pathlib, platform, re, shutil, subprocess, sys, tempfile, time

HERE = pathlib.Path(__file__).resolve().parent
SKILL = HERE.parent
PAGE = SKILL / "page" / "explainer.html"
sys.path.insert(0, str(HERE))
from _ff import ffmpeg, probe  # noqa: E402

BUILTIN_FONTS = {"jost": SKILL / "page/fonts/jost-700.ttf", "figtree": SKILL / "page/fonts/figtree-600.ttf"}
KINDS = {"headline", "big", "steps", "checklist"}
SHAPES = {"phone": (1080, 1920), "widescreen": (1920, 1080)}
MUSIC_IN, MUSIC_OUT = SKILL / "music/jingles_STEEL09.ogg", SKILL / "music/jingles_STEEL07.ogg"
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def problem(msg, code=2):
    print("PROBLEM: " + msg)
    sys.exit(code)


# ---- the plan ------------------------------------------------------------------------------

def default_seconds(s):
    """How long a scene stays on screen: long enough to read its caption, and for a list,
    for every item to land."""
    words = len((s.get("caption") or "").split()) + len(s.get("words", "").split())
    secs = max(3.6, words / 2.6 + 1.4)
    if s.get("kind") in ("steps", "checklist"):
        secs = max(secs, 1.7 + 0.9 * len(s.get("items", [])) + 1.0)
    return round(secs, 2)


def load_plan(path):
    path = pathlib.Path(path).resolve()
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        problem(f"The plan file could not be read ({e}).")
    base = path.parent
    issues = []
    for k in ("title", "camp"):
        if not str(plan.get(k, "")).strip():
            issues.append(f'The plan needs a "{k}".')
    b = plan.get("brand") or {}
    for k in ("background", "text", "main", "accent"):
        if not HEX.match(str(b.get(k, ""))):
            issues.append(f"The brand's {k} color must be a color code like #1F4E79, and it is {b.get(k)!r}.")
    for k in ("heading_font", "body_font"):
        f = b.get(k) or {}
        if not f.get("name"):
            issues.append(f"The brand needs a {k.replace('_', ' ')} name.")
            continue
        if f.get("file"):
            fp = (base / f["file"]).resolve()
            if not fp.is_file():
                issues.append(f"The font file for {f['name']} is not where the plan says: {fp}")
            f["url"] = fp.as_uri()
        elif f["name"].lower() in BUILTIN_FONTS:
            f["url"] = BUILTIN_FONTS[f["name"].lower()].as_uri()
        else:
            f["url"] = None
    if b.get("logo"):
        lp = (base / b["logo"]).resolve()
        if not lp.is_file():
            issues.append(f"The logo file is not where the plan says: {lp}")
        elif lp.suffix.lower() not in (".png", ".svg", ".jpg", ".jpeg", ".webp"):
            issues.append("The logo must be a PNG, SVG, JPG or WEBP picture file.")
        b["logo_url"] = lp.as_uri()
    else:
        b["logo_url"] = None
    scenes = plan.get("scenes") or []
    if not 1 <= len(scenes) <= 10:
        issues.append(f"The plan needs between 1 and 10 scenes, and it has {len(scenes)}.")
    for i, s in enumerate(scenes, 1):
        if s.get("kind") not in KINDS:
            issues.append(f"Scene {i}'s kind must be one of {', '.join(sorted(KINDS))}.")
        if not str(s.get("words", "")).strip():
            issues.append(f"Scene {i} needs its on-screen words.")
        if s.get("kind") in ("steps", "checklist") and not 2 <= len(s.get("items") or []) <= 5:
            issues.append(f"Scene {i} is a list, so it needs 2 to 5 items.")
        if s.get("kind") == "big" and len(str(s.get("words", ""))) > 14:
            issues.append(f"Scene {i} is a big-word scene, so its words must be 14 letters or fewer.")
        s["seconds"] = float(s["seconds"]) if s.get("seconds") else default_seconds(s)
    if issues:
        print("\n".join("PROBLEM: " + m for m in issues))
        sys.exit(2)
    return plan


def contrast_note(plan):
    """A warning when the words would be hard to read against the background."""
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    b = plan["brand"]
    x, y = lum(b["text"]), lum(b["background"])
    if (max(x, y) + 0.05) / (min(x, y) + 0.05) < 4.5:
        print("NOTE: the text color and the background color are close, so the words may be hard to read.")


def file_stem(plan):
    title = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", plan["title"]).strip().rstrip(".")
    return f"{datetime.date.today().isoformat()} {title}"


# ---- drawing -------------------------------------------------------------------------------

class Drawer:
    """One browser for the whole run; one page per shape and part."""

    def __enter__(self):
        try:
            from playwright.sync_api import sync_playwright
        except Exception:
            problem("The drawing browser is not set up here. Run check_tools.py first.", 3)
        import _browser
        self._pw = sync_playwright().start()
        try:
            self.browser = _browser.launch(self._pw)
        except Exception as e:
            self._pw.stop()
            problem(f"The drawing browser would not start ({str(e).splitlines()[0][:200]}). Run check_tools.py.", 3)
        return self

    def __exit__(self, *a):
        self.browser.close(); self._pw.stop()

    def open(self, plan, shape, part="full"):
        w, h = SHAPES[shape]
        page = self.browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)))
        page.add_init_script(f"window.PLAN = {json.dumps(plan)}; window.PART = {json.dumps(part)};")
        page.goto(PAGE.as_uri())
        try:
            page.wait_for_function("window.__ready === true || window.__failed !== undefined", timeout=60000)
        except Exception:
            problem(f"The {shape} video did not finish drawing its first frame within a minute.", 3)
        failed = page.evaluate("window.__failed || null") or next((e for e in errs if "PLAIN:" in e), None)
        if failed:
            msg = failed.split("PLAIN: ", 1)[-1]
            problem(f"({shape}) {msg}", 3)
        page.errs = errs
        return page, page.evaluate("window.TIMELINE")


def frames_to_mp4(page, duration, out, fps, start=0.0):
    """Pipe one PNG per frame into FFmpeg. The result has no sound yet."""
    w, h = page.viewport_size["width"], page.viewport_size["height"]
    cmd = [ffmpeg(), "-y", "-hide_banner", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps),
           "-c:v", "png", "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
           "-r", str(fps), "-fps_mode", "cfr", "-movflags", "+faststart", str(out)]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(duration * fps))
    t0 = time.time()
    try:
        for i in range(n):
            page.evaluate(f"window.seek({start + i / fps:.5f})")
            ff.stdin.write(page.screenshot(type="png"))
            if i and i % (fps * 10) == 0:
                print(f"  {w}x{h}: {i} of {n} frames, {time.time() - t0:.0f} s so far", flush=True)
    except Exception as e:
        # the browser or the joining program stopped partway: end both, and say so plainly
        ff.kill(); ff.wait()
        problem(f"Drawing the {w}x{h} video stopped partway through ({str(e).splitlines()[0][:200]}). "
                "Nothing was saved for this shape. Try again; if it happens twice, offer the problem log.", 3)
    ff.stdin.close(); ff.wait()
    if ff.returncode:
        problem("The video joining program stopped before the video was finished.", 3)
    if page.errs:
        problem("The page reported a problem while drawing: " + page.errs[0][:300], 3)
    print(f"  {n} frames {w}x{h} in {time.time() - t0:.0f} s")


def add_sound(video, out, duration, voice=(), music=()):
    """Give the video its sound track: voice clips and music cues, each at a start second,
    over silence. A video with neither gets a silent track, so every player treats it the same."""
    cmd = [ffmpeg(), "-y", "-hide_banner", "-loglevel", "error", "-i", str(video),
           "-f", "lavfi", "-t", f"{duration:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
    chains, labels = [], ["[1:a]"]
    cues = [(p, s, 1.0) for p, s in voice] + [(p, s, 0.45 if voice else 1.0) for p, s in music]
    for i, (p, s, vol) in enumerate(cues):
        cmd += ["-i", str(p)]
        chains.append(f"[{i + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},"
                      f"adelay={int(s * 1000)}:all=1[c{i}]")
        labels.append(f"[c{i}]")
    mix = f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{duration:.3f}"
    if cues:
        mix += f",afade=t=out:st={max(0, duration - 0.3):.3f}:d=0.3,alimiter=limit=0.8:level=false"
    fc = ";".join(chains + [mix + "[m]"])
    r = subprocess.run(cmd + ["-filter_complex", fc, "-map", "0:v", "-map", "[m]", "-c:v", "copy",
                              "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-t", f"{duration:.3f}",
                              "-movflags", "+faststart", str(out)], capture_output=True, text=True)
    if r.returncode:
        problem("The sound could not be added to the video: " + r.stderr.strip()[-300:], 3)


def write_vtt(timeline, path):
    def ts(x):
        return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{x % 60:06.3f}"
    lines = ["WEBVTT", ""]
    for i, s in enumerate(timeline["scenes"], 1):
        if s["caption"]:
            lines += [str(i), f"{ts(s['start'])} --> {ts(s['end'])}", s["caption"], ""]
    pathlib.Path(path).write_text("\n".join(lines), encoding="utf-8")


# ---- built-in voices -----------------------------------------------------------------------

def list_voices():
    system = platform.system()
    if system == "Windows":
        r = subprocess.run(["powershell", "-NoProfile", "-Command",
                            "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer)"
                            ".GetInstalledVoices() | Where-Object { $_.Enabled } | ForEach-Object { $_.VoiceInfo.Name }"],
                           capture_output=True, text=True)
        return [v.strip() for v in r.stdout.splitlines() if v.strip()]
    if system == "Darwin" and shutil.which("say"):
        r = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
        return [re.split(r"\s{2,}", l.strip())[0] for l in r.stdout.splitlines() if "en_" in l]
    exe = shutil.which("espeak-ng") or shutil.which("espeak")
    return ["espeak"] if exe else []


def speak(text, voice, out_wav, tmp):
    """Write one spoken clip with the computer's own voice. Nothing leaves the computer."""
    tf = pathlib.Path(tmp) / "say.txt"
    tf.write_text(text, encoding="utf-8")
    system = platform.system()
    if system == "Windows":
        ps = ("Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
              "$s.SelectVoice($env:EXPLAINER_VOICE); $s.Rate = -1; $s.SetOutputToWaveFile($env:EXPLAINER_WAV); "
              "$s.Speak([IO.File]::ReadAllText($env:EXPLAINER_TEXT)); $s.Dispose()")
        env = dict(os.environ, EXPLAINER_VOICE=voice, EXPLAINER_WAV=str(out_wav), EXPLAINER_TEXT=str(tf))
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, env=env)
    elif system == "Darwin":
        aiff = pathlib.Path(tmp) / "say.aiff"
        r = subprocess.run(["say", "-v", voice, "-o", str(aiff), "-f", str(tf)], capture_output=True, text=True)
        if not r.returncode:
            r = subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", str(aiff), str(out_wav)],
                               capture_output=True, text=True)
    else:
        exe = shutil.which("espeak-ng") or shutil.which("espeak")
        r = subprocess.run([exe, "-w", str(out_wav), "-f", str(tf)], capture_output=True, text=True)
    if r.returncode or not pathlib.Path(out_wav).is_file():
        problem(f'The computer voice "{voice}" could not read the script aloud. Make the video without a voice.', 3)


def add_voice(plan, voice, tmp):
    """Read every scene aloud, and make each scene last at least as long as its clip."""
    if voice not in list_voices():
        problem(f'There is no computer voice called "{voice}" here. Run "make_video.py voices" for the list.', 2)
    clips = []
    for i, s in enumerate(plan["scenes"], 1):
        text = s.get("say") or s.get("caption") or s["words"]
        wav = pathlib.Path(tmp) / f"voice-{i:02d}.wav"
        speak(text, voice, wav, tmp)
        secs = probe(wav)[3]
        s["seconds"] = round(max(s["seconds"], secs + 0.9), 2)
        clips.append(wav)
        print(f"  scene {i}: {secs:.1f} s of speech")
    return clips


# ---- commands ------------------------------------------------------------------------------

def built_times(tl, plan):
    """The moment each scene is fully built: every item landed, before its words leave."""
    return [s["end"] - 0.35 for s in tl["scenes"]]


def cmd_check(plan):
    contrast_note(plan)
    with Drawer() as d:
        for shape in SHAPES:
            page, tl = d.open(plan, shape)
            page.close()
    print(f"The plan is fine. The video runs {tl['duration']:.1f} seconds, in both shapes.")


def cmd_stills(plan, folder):
    folder.mkdir(parents=True, exist_ok=True)
    contrast_note(plan)
    with Drawer() as d:
        for shape in SHAPES:
            page, tl = d.open(plan, shape)
            times = [2.6] + built_times(tl, plan) + [tl["duration"] - 0.1]
            for k, t in enumerate(times, 1):
                page.evaluate(f"window.seek({t:.3f})")
                page.screenshot(path=str(folder / f"{shape}-{k:02d}.jpg"), type="jpeg", quality=88)
            page.close()
            cols = 4 if shape == "phone" else 3
            rows = -(-len(times) // cols)
            w = 270 if shape == "phone" else 480
            sheet = folder / f"sheet-{shape}.jpg"
            r = subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-framerate", "1", "-start_number", "1",
                                "-i", str(folder / f"{shape}-%02d.jpg"), "-vf",
                                f"scale={w}:-2,tile={cols}x{rows}:padding=8:margin=8:color=white",
                                "-frames:v", "1", "-update", "1", str(sheet)], capture_output=True, text=True)
            if r.returncode:
                print("NOTE: the pictures are ready, but the sheet of them could not be made.")
            print(f"{shape}: {len(times)} pictures and {sheet.name}")
    print(f"The video will run {tl['duration']:.1f} seconds.")


def cmd_video(plan, folder, shapes, music, voice, fps):
    folder.mkdir(parents=True, exist_ok=True)
    contrast_note(plan)
    stem = file_stem(plan)
    made = []
    with tempfile.TemporaryDirectory() as tmp:
        clips = add_voice(plan, voice, tmp) if voice else []
        with Drawer() as d:
            for shape in shapes:
                page, tl = d.open(plan, shape)
                silent = pathlib.Path(tmp) / f"{shape}.mp4"
                print(f"Drawing the {shape} video ({tl['duration']:.1f} s)...", flush=True)
                frames_to_mp4(page, tl["duration"], silent, fps)
                page.close()
                vc = [(c, s["start"] + 0.25) for c, s in zip(clips, tl["scenes"])]
                mc = [(MUSIC_IN, 0.55), (MUSIC_OUT, tl["duration"] - 2.4 - 0.5)] if music else []
                out = folder / f"{stem} ({shape}).mp4"
                add_sound(silent, out, tl["duration"], vc, mc)
                made.append(out)
        vtt = folder / f"{stem} captions.vtt"
        write_vtt(tl, vtt)
    for out in made:
        w, h, _, secs = probe(out)
        print(f"MADE {out.name}: {secs:.1f} seconds, {w}x{h}, {out.stat().st_size / 1e6:.1f} MB")
    print(f"MADE {vtt.name}: the captions as a separate file, for a video site that asks for one")


def cmd_bumpers(plan, folder, shape="widescreen", fps=30, tmp=None):
    folder.mkdir(parents=True, exist_ok=True)
    outs = []
    with tempfile.TemporaryDirectory() as t2:
        with Drawer() as d:
            for part in ("intro", "outro"):
                page, tl = d.open(plan, shape, part)
                silent = pathlib.Path(t2) / f"{part}.mp4"
                frames_to_mp4(page, tl["duration"], silent, fps)
                page.close()
                out = pathlib.Path(tmp or folder) / f"{'Opening' if part == 'intro' else 'Closing'} ({shape}).mp4"
                add_sound(silent, out, tl["duration"])
                outs.append(out)
    if not tmp:
        for o in outs:
            print(f"MADE {o.name}: {probe(o)[3]:.1f} seconds")
    return outs


def cmd_join(plan, presenter, folder):
    presenter = pathlib.Path(presenter)
    if not presenter.is_file():
        problem(f"The presenter video is not where you said: {presenter}")
    w, h, has_audio, secs = probe(presenter)
    if not w:
        problem("That file does not hold a video I can read.")
    folder.mkdir(parents=True, exist_ok=True)
    shape = "phone" if h > w else "widescreen"
    W, H = SHAPES[shape]
    bg = plan["brand"]["background"].replace("#", "0x")
    with tempfile.TemporaryDirectory() as tmp:
        intro, outro = cmd_bumpers(plan, folder, shape, tmp=tmp)
        parts = [intro, presenter, outro]
        inputs, filt, extra = [], [], 0
        for p in parts:
            inputs += ["-i", str(p)]
        for i, p in enumerate(parts):
            _, _, a, s = probe(p)
            filt.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:"
                        f"color={bg},setsar=1,fps=30,format=yuv420p[v{i}]")
            if a:
                src = f"[{i}:a]"
            else:
                inputs += ["-f", "lavfi", "-t", f"{s:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
                src = f"[{len(parts) + extra}:a]"; extra += 1
            filt.append(f"{src}aresample=48000,aformat=channel_layouts=stereo[a{i}]")
        filt.append("".join(f"[v{i}][a{i}]" for i in range(3)) + "concat=n=3:v=1:a=1[v][a]")
        out = folder / f"{file_stem(plan)} with presenter ({shape}).mp4"
        r = subprocess.run([ffmpeg(), "-y", "-hide_banner", "-loglevel", "error", *inputs, "-filter_complex",
                            ";".join(filt), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                            "-crf", "18", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)],
                           capture_output=True, text=True)
        if r.returncode:
            problem("The three parts could not be joined: " + r.stderr.strip()[-300:], 3)
    print(f"MADE {out.name}: {probe(out)[3]:.1f} seconds, {W}x{H}, {out.stat().st_size / 1e6:.1f} MB")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["check", "stills", "video", "bumpers", "join", "voices"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--shape", default="both", choices=["both", "phone", "widescreen"])
    ap.add_argument("--music", action="store_true")
    ap.add_argument("--voice")
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()
    if a.command == "voices":
        v = list_voices()
        print("\n".join(f"VOICE {x}" for x in v) if v else
              "NO VOICE: this computer has no built-in voice I can use. The video will have captions only.")
        return
    need = {"check": 1, "stills": 2, "video": 2, "bumpers": 2, "join": 3}[a.command]
    if len(a.args) != need:
        problem(f"'{a.command}' needs {need} name(s) after it. See the top of this file.")
    if not PAGE.is_file():
        problem("This skill's drawing page is missing. Reinstall the plugin.", 3)
    plan = load_plan(a.args[0])
    if a.command == "check":
        cmd_check(plan)
    elif a.command == "stills":
        cmd_stills(plan, pathlib.Path(a.args[1]))
    elif a.command == "video":
        shapes = list(SHAPES) if a.shape == "both" else [a.shape]
        cmd_video(plan, pathlib.Path(a.args[1]), shapes, a.music, a.voice, a.fps)
    elif a.command == "bumpers":
        cmd_bumpers(plan, pathlib.Path(a.args[1]), "widescreen" if a.shape == "both" else a.shape, a.fps)
    else:
        cmd_join(plan, a.args[1], pathlib.Path(a.args[2]))


if __name__ == "__main__":
    main()
