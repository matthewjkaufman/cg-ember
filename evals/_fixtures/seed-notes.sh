#!/usr/bin/env bash
# Seeds a "Personal Notes" folder in the run's empty workspace from the shared
# fixture, then applies the case's own notes/ overrides. Called by each case's scaffold.sh.
set -e
case_dir="$1"
fix="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "Personal Notes"
cp "$fix/personal-notes/"*.txt "Personal Notes/"
if [ -d "$case_dir/notes" ]; then
  cp "$case_dir/notes/"*.txt "Personal Notes/"
fi
