"""Start a headless Chromium for drawing the frames, using one already on the computer if needed.

Some workspaces block the download Playwright makes for its own Chromium while a Chromium is
already installed there (measured in one such workspace on 2026-10-05). launch() tries
Playwright's own browser first, then every Chromium it can find, newest first. Set
EXPLAINER_CHROMIUM to a browser's full path to use that one.
"""
import os, pathlib, platform, re, shutil


def _cache_dirs():
    if os.environ.get("PLAYWRIGHT_BROWSERS_PATH") not in (None, "", "0"):
        yield pathlib.Path(os.environ["PLAYWRIGHT_BROWSERS_PATH"])
    home = pathlib.Path.home()
    yield home / ".cache/ms-playwright"
    yield home / "Library/Caches/ms-playwright"
    if os.environ.get("LOCALAPPDATA"):
        yield pathlib.Path(os.environ["LOCALAPPDATA"]) / "ms-playwright"
    yield pathlib.Path("/ms-playwright")


_PATTERNS = ["chromium-*/chrome-linux*/chrome", "chromium_headless_shell-*/chrome-*/headless_shell",
             "chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell",
             "chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell.exe",
             "chromium-*/chrome-win*/chrome.exe", "chromium_headless_shell-*/chrome-*/headless_shell.exe",
             "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium"]


def candidates():
    """Chromium executables on this computer, the newest Playwright download first."""
    if os.environ.get("EXPLAINER_CHROMIUM"):
        yield os.environ["EXPLAINER_CHROMIUM"]
    found = []
    for d in _cache_dirs():
        for pat in _PATTERNS:
            found += [p for p in d.glob(pat) if p.is_file()]

    def rev(p):
        m = re.search(r"chromium(?:_headless_shell)?-(\d+)", str(p))
        return int(m.group(1)) if m else 0
    yield from (str(p) for p in sorted(found, key=rev, reverse=True))
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome"):
        exe = shutil.which(name)
        if exe:
            yield exe
    if platform.system() == "Windows":
        for base in (os.environ.get("PROGRAMFILES", ""), os.environ.get("PROGRAMFILES(X86)", "")):
            p = pathlib.Path(base) / "Google/Chrome/Application/chrome.exe"
            if base and p.is_file():
                yield str(p)


def launch(p):
    """Return a launched browser from a sync_playwright() handle, or raise the first failure.

    A Chromium from another Playwright version can start and still fail partway through a
    render; trying the newest first makes that least likely.
    """
    try:
        return p.chromium.launch()
    except Exception as first:
        for exe in candidates():
            try:
                return p.chromium.launch(executable_path=exe)
            except Exception:
                continue
        raise first
