"""Check (and, with --install, set up) the programs the explainer video needs.

  python check_tools.py            says what is here and what is missing; installs nothing
  python check_tools.py --install  sets up what is missing, then checks again

Two programs are needed: a hidden web browser that draws each frame (Playwright and its
Chromium) and a program that joins the frames into a video (FFmpeg 5.1 or newer).

It first tries the Python running this script. If that Python lacks a piece, it uses one
video environment in the person's home folder (~/.cg-ember-video, or $EXPLAINER_ENV),
made by --install and reused on later runs. Nothing needs administrator rights, and nothing
is installed into the system Python. FFmpeg comes from the imageio-ffmpeg package unless the
computer already has FFmpeg 5.1 or newer. If the workspace already has Playwright, the
environment gets that same version, so it reuses the Chromium already installed beside it.

Exit 0 and the last lines "PY=<python to use>" and "FFMPEG=<ffmpeg>" when ready; exit 1 with
one "MISSING" line per missing piece otherwise.
"""
import os, pathlib, platform, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ENV = pathlib.Path(os.environ.get("EXPLAINER_ENV", pathlib.Path.home() / ".cg-ember-video"))
VPY = ENV / ("Scripts/python.exe" if platform.system() == "Windows" else "bin/python")
PACKAGES = ["playwright", "imageio-ffmpeg"]

PROBE = r"""
import sys; sys.path.insert(0, sys.argv[1])
missing = []
try:
    from playwright.sync_api import sync_playwright
except Exception:
    missing.append('the drawing browser (Playwright)')
else:
    import _browser
    try:
        with sync_playwright() as p:
            _browser.launch(p).close()
    except Exception:
        missing.append("the drawing browser's Chromium")
import _ff
ff = _ff.find()
if not ff:
    missing.append('the video joining program (FFmpeg 5.1 or newer)')
print('FF=' + (ff or ''))
for m in missing:
    print('MISS=' + m)
"""


def run(args, **kw):
    return subprocess.run([str(a) for a in args], capture_output=True, text=True, **kw)


def probe(py):
    """Return (missing pieces, ffmpeg path) as seen by this Python."""
    try:
        r = run([py, "-c", PROBE, str(HERE)], timeout=180)
    except Exception:
        return ["a working Python"], ""
    if r.returncode:
        return ["a working Python"], ""
    lines = r.stdout.splitlines()
    ff = next((l[3:] for l in lines if l.startswith("FF=")), "")
    return [l[5:] for l in lines if l.startswith("MISS=")], ff


def existing_playwright():
    """The Playwright version already in this workspace (Python or Node), or None."""
    for args in ([sys.executable, "-c", "import importlib.metadata as m; print(m.version('playwright'))"],
                 [shutil.which("npx") or "npx", "--no-install", "playwright", "--version"]):
        try:
            r = run(args, timeout=60)
        except Exception:
            continue
        m = re.search(r"(\d+\.\d+\.\d+)", r.stdout)
        if r.returncode == 0 and m:
            return m.group(1)
    return None


def install():
    if sys.version_info < (3, 8):
        sys.exit("This computer's Python is too old to set up the video programs. Nothing was changed.")
    if not VPY.exists():
        print("Making the video environment...")
        r = run([sys.executable, "-m", "venv", ENV])
        if r.returncode:
            print(r.stderr[-800:])
            sys.exit("I could not make the video environment on this computer. Nothing was changed.")
    packages = list(PACKAGES)
    pw = existing_playwright()
    if pw:
        print(f"Matching the Playwright already here ({pw}), so its Chromium is reused.")
        # The Chromium build follows the minor version, and a patch release may not exist everywhere.
        packages[0] = "playwright==" + ".".join(pw.split(".")[:2]) + ".*"
    print("Adding the video programs (a few minutes)...")
    r = run([VPY, "-m", "pip", "install", "--upgrade", "--quiet", *packages])
    if r.returncode and pw:
        print("That Playwright version is not available; adding the current one instead.")
        r = run([VPY, "-m", "pip", "install", "--upgrade", "--quiet", *PACKAGES])
    if r.returncode:
        print(r.stderr[-800:])
        sys.exit("The video programs did not finish installing. Nothing else on the computer was changed.")
    missing, _ = probe(VPY)
    if "the drawing browser's Chromium" in missing:
        print("Downloading the drawing browser (a few minutes)...")
        r = run([VPY, "-m", "playwright", "install", "chromium"])
        if r.returncode:
            print(r.stderr[-800:])
            print("The drawing browser could not be downloaded, and no browser already on this "
                  "computer would start.")


def main():
    if "--install" in sys.argv:
        install()
    print(f"System: {platform.system()}")
    missing, ff = probe(sys.executable)
    py = sys.executable
    if missing and VPY.exists():
        missing, ff = probe(VPY)
        py = str(VPY)
    if not missing:
        print("Everything the explainer video needs is here.")
        print(f"PY={py}")
        print(f"FFMPEG={ff}")
        return 0
    for m in missing:
        print(f"MISSING  {m}")
    if "--install" in sys.argv:
        if any("Chromium" in m for m in missing) and platform.system() == "Linux":
            print("A browser may be here but cannot start: it lacks system parts that only an "
                  "administrator can add. The video cannot be drawn in this workspace.")
        return 1
    print(f'\nTo set up (ask the person first): "{sys.executable}" "{__file__}" --install')
    return 1


if __name__ == "__main__":
    sys.exit(main())
