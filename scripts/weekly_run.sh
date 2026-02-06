#!/data/data/com.termux/files/usr/bin/bash
BASE="$HOME/kr3w"
python "$BASE/kr3w.py" --days 7
chmod +x ~/kr3w/scripts/weekly_run.sh
bash ~/kr3w/scripts/weekly_run.sh
