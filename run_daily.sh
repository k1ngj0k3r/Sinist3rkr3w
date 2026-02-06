#!/bin/bash
set -e
cd "$(dirname "$0" )"

python3 kr3w.py

# optional: auto-commit only if output changed
if [ -n "$(git status --porcelain)" ];
then
git add -A
git commit -m "Daily generation :$ (date +%F)"
git push
fi
