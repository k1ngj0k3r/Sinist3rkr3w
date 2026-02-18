#!/data/data/com.termux/files/usr/bin/bash
set -e

cd "$HOME/kr3w"
fail() {
  termux-notification --title "❌ Kr3w Publish" --content "$1" --priority high
  echo "FAIL: $1"
  exit 1
}
# 1) Generate today’s assets
python3 kr3w.py || fail "Generator crashed (kr3w.py)"
bash scripts/brand_pack.sh
python3 scripts/build_dashboard.py
# 2) Commit + push only if something changed
git add -A

if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

MSG="Auto publish: $(date +%F)"
git commit -m "$MSG"
git push || fail "Git push failed"
echo "✅ Published."
termux-notification --title "✅ Kr3w Publish" --content "Published successfully." --priority high
