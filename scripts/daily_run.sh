#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/kr3w"
OUT="$BASE/output"
LOG="$BASE/logs"

mkdir -p "$OUT" "$LOG"

DATE=$(date +%Y-%m-%d)

echo "=== KR3W RUN $DATE ===" >> "$LOG/run.log"

python "$BASE/kr3w.py" > "$OUT/blog_$DATE.md"

echo "Generated: blog_$DATE.md" >> "$LOG/run.log"
echo "=== DONE ===" >> "$LOG/run.log"
