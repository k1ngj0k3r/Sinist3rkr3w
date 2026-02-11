#!/data/data/com.termux/files/usr/bin/bash
set -e

cd "$HOME/kr3w"

# 1) Generate today’s assets
python3 kr3w.py

# 2) Commit + push only if something changed
git add -A

if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

MSG="Auto publish: $(date +%F)"
git commit -m "$MSG"
git push
echo "✅ Published."
