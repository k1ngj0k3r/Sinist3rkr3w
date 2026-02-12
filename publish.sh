#!/data/data/com.termux/files/usr/bin/bash
set -e

cd "$HOME/kr3w"

# Generate today's assets
python3 kr3w.py

# Commit + push if changes exist
git add -A
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

MSG="Auto publish: $(date +%F)"
git commit -m "$MSG"
git push

echo "✅ Published to GitHub."
echo "📁 Output: $HOME/kr3w/output"
