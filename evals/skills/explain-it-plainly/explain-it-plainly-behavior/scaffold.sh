#!/usr/bin/env bash
# Runs only with --scaffold. $0 is this file's own path (measured 2026-10-03);
# cygpath turns a Windows path into one Git Bash can cd into.
set -e
src="$0"
if command -v cygpath >/dev/null 2>&1; then src="$(cygpath -u "$src")"; fi
here="$(cd "$(dirname "$src")" && pwd)"
bash "$here/../../../_fixtures/seed-notes.sh" "$here"
