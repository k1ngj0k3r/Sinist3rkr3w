#!/data/data/com.termux/files/usr/bin/bash
set -e

cd "$HOME/kr3w"

OUT="$HOME/kr3w/output"
mkdir -p "$OUT"

# Copy brand core into output so it’s always ready to paste
cp -f "$HOME/kr3w/brand/manifesto.md" "$OUT/manifesto.md"
cp -f "$HOME/kr3w/brand/guardrails.md" "$OUT/guardrails.md"

echo "✅ Brand pack exported:"
echo " - $OUT/manifesto.md"
echo " - $OUT/guardrails.md"
