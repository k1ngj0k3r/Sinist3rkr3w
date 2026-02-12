#!/data/data/com.termux/files/usr/bin/bash
set -e

OUT="$HOME/kr3w/output"
D="$(date +%F)"

echo "📝 BLOG (today)"
echo "----------------"
cat "$OUT/blog_${D}.md" || echo "No blog file for $D yet."

echo
echo "📣 FACEBOOK AD (today)"
echo "----------------------"
cat "$OUT/ad_facebook_${D}.txt" || echo "No FB ad file for $D yet."

echo
echo "🎬 YOUTUBE POST (today)"
echo "-----------------------"
cat "$OUT/youtube_${D}.txt" || echo "No YouTube file for $D yet."
