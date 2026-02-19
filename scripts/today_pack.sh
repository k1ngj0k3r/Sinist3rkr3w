#!/bin/bash

OUT="$HOME/kr3w/output"
TODAY=$(date +%F)

echo "===== SINIST3RKR3W | TODAY PACK ====="
echo ""
echo "BLOG:"
cat "$OUT/blog_${TODAY}.md"
echo ""
echo "------------------------------------"
echo "SHORT CAPTION:"
cat "$OUT/caption_short_${TODAY}.txt"
echo ""
echo "------------------------------------"
echo "YOUTUBE:"
cat "$OUT/youtube_${TODAY}.txt"
echo ""
echo "------------------------------------"
echo "SMS / CTA:"
cat "$OUT/sms_cta_${TODAY}.txt"
echo ""
echo "===== END ====="
