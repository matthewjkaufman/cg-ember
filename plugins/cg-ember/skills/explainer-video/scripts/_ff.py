"""Find a usable FFmpeg on any computer, and read a video's size and length without ffprobe.

Order: FFmpeg on PATH, then a winget install on Windows that a fresh shell has not loaded
onto PATH yet, then the copy inside the imageio-ffmpeg Python package. An FFmpeg older than
5.1 is skipped, because the tools use -fps_mode, which 5.1 added.
"""
import os, pathlib, platform, re, shutil, subprocess, sys

_found = None


def version_ok(exe):
    try:
        out = subprocess.run([exe, "-version"], capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return False
    m = re.search(r"version n?(\d+)\.(\d+)", out)
    if not m:
        return "version" in out   # builds named after a date or a commit ("version N-12345-g...") are recent
    return (int(m.group(1)), int(m.group(2))) >= (5, 1)


def candidates():
    exe = shutil.which("ffmpeg")
    if exe:
        yield exe
    if platform.system() == "Windows":
        base = pathlib.Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/WinGet/Packages"
        yield from (str(f) for f in base.glob("Gyan.FFmpeg*/**/bin/ffmpeg.exe"))
    try:
        import imageio_ffmpeg
        yield imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass


def find():
    """Return a usable FFmpeg path, or None."""
    global _found
    if _found is None:
        _found = next((c for c in candidates() if version_ok(c)), "")
    return _found or None


def ffmpeg():
    exe = find()
    if not exe:
        sys.exit("PROBLEM: The video joining program (FFmpeg) is not on this computer. Run check_tools.py first.")
    return exe


def probe(path):
    """Return (width, height, has_audio, seconds) for a video or sound file (0x0 for sound only)."""
    r = subprocess.run([ffmpeg(), "-hide_banner", "-i", str(path)], capture_output=True, text=True)
    err = r.stderr
    m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", err)
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    secs = int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3)) if d else 0.0
    w, h = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return w, h, "Audio:" in err, secs
