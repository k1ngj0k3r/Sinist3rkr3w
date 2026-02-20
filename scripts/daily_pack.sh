#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE="$HOME/kr3w"
CFG="$BASE/kr3w_config.json"
OUTBASE="$BASE/output"
LOGDIR="$BASE/logs"
LOG="$LOGDIR/daily_pack.log"

mkdir -p "$OUTBASE" "$LOGDIR" "$BASE/scripts"

ts() { date '+%Y-%m-%d %H:%M:%S'; }

echo "[$(ts)] daily_pack start" | tee -a "$LOG"

# --- Preconditions ---
if [ ! -f "$CFG" ]; then
  echo "[$(ts)] ERROR: Config not found: $CFG" | tee -a "$LOG"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "[$(ts)] ERROR: jq not installed. Run: pkg install jq" | tee -a "$LOG"
  exit 1
fi

# --- Date / Day mapping ---
TODAY="$(date +%F)"
DOW="$(date +%a | tr '[:upper:]' '[:lower:]')"  # mon tue wed thu fri sat sun
OUTDIR="$OUTBASE/$TODAY"
mkdir -p "$OUTDIR"

echo "[$(ts)] Today: $TODAY | DOW: $DOW" | tee -a "$LOG"

# --- Read today's rotation themes (array) ---
THEMES_JSON="$(jq -c --arg dow "$DOW" '.weekly_rotation[$dow] // empty' "$CFG")"

if [ -z "$THEMES_JSON" ] || [ "$THEMES_JSON" = "null" ]; then
  echo "[$(ts)] ERROR: No weekly_rotation entry for '$DOW' in config." | tee -a "$LOG"
  exit 1
fi

# Convert JSON array -> bash array
mapfile -t THEMES < <(echo "$THEMES_JSON" | jq -r '.[]')

if [ "${#THEMES[@]}" -eq 0 ]; then
  echo "[$(ts)] ERROR: weekly_rotation['$DOW'] is empty." | tee -a "$LOG"
  exit 1
fi

echo "[$(ts)] Themes for $DOW: ${THEMES[*]}" | tee -a "$LOG"

# --- Load global bits ---
LINKTREE="$(jq -r '.links.linktree // empty' "$CFG")"
HASHTAGS="$(jq -r '.hashtags[]? // empty' "$CFG" | tr '\n' ' ')"
MANIFESTO_FILE="$OUTBASE/manifesto.md"
MANIFESTO_TEXT=""
if [ -f "$MANIFESTO_FILE" ]; then
  MANIFESTO_TEXT="$(sed -n '1,120p' "$MANIFESTO_FILE")"
fi

# --- Helper: get theme object by id ---
get_theme_field() {
  local id="$1"
  local field="$2"
  jq -r --arg id "$id" --arg field "$field" '
    (.themes[] | select(.id == $id) | .[$field]) // empty
  ' "$CFG"
}

get_theme_list_field() {
  local id="$1"
  local field="$2"
  jq -r --arg id "$id" --arg field "$field" '
    (.themes[] | select(.id == $id) | .[$field][]?) // empty
  ' "$CFG"
}

# --- Generate per theme ---
MASTER_MD="$OUTDIR/daily_pack.md"
: > "$MASTER_MD"

TITLE_DATE="$(date '+%A, %B %d')"
echo "# SINIST3RKR3W | DAILY PACK — $TITLE_DATE" >> "$MASTER_MD"
echo "" >> "$MASTER_MD"

for T in "${THEMES[@]}"; do
  LABEL="$(get_theme_field "$T" "label")"
  [ -z "$LABEL" ] && LABEL="$T"

  PRIMARY_LINK_KEY="$(get_theme_field "$T" "primary_link")"
  PRIMARY_LINK=""
  if [ -n "$PRIMARY_LINK_KEY" ]; then
    PRIMARY_LINK="$(jq -r --arg k "$PRIMARY_LINK_KEY" '.links[$k] // empty' "$CFG")"
  fi

  # Hooks + CTAs
  mapfile -t HOOKS < <(get_theme_list_field "$T" "hooks")
  mapfile -t CTAS  < <(get_theme_list_field "$T" "ctas")

  HOOK="${HOOKS[0]:-}"
  CTA="${CTAS[0]:-}"

  echo "## $LABEL" >> "$MASTER_MD"
  echo "" >> "$MASTER_MD"

  # Wellness specific structure if theme == wellness
  if [ "$T" = "wellness" ]; then
    echo "**Today focus:** Powerful + grounding. (Wellness day)" >> "$MASTER_MD"
    echo "" >> "$MASTER_MD"
    echo "$HOOK" >> "$MASTER_MD"
    echo "" >> "$MASTER_MD"
    echo "### Micro plan (10 minutes)" >> "$MASTER_MD"
    echo "- 2 min: water + breathe (in 4, hold 2, out 6)" >> "$MASTER_MD"
    echo "- 3 min: quick reset (dishes / counter / trash run)" >> "$MASTER_MD"
    echo "- 3 min: body check (stretch shoulders/neck/hips)" >> "$MASTER_MD"
    echo "- 2 min: write 3 lines: *What matters today? What’s one win? What can wait?*" >> "$MASTER_MD"
    echo "" >> "$MASTER_MD"
    echo "### Grounding line" >> "$MASTER_MD"
    echo "> I’m not behind. I’m building. One clean step at a time." >> "$MASTER_MD"
    echo "" >> "$MASTER_MD"
  else
    # Generic theme output
    [ -n "$HOOK" ] && echo "$HOOK" >> "$MASTER_MD"
    echo "" >> "$MASTER_MD"
  fi

  if [ -n "$PRIMARY_LINK" ]; then
    echo "👉 $PRIMARY_LINK" >> "$MASTER_MD"
    echo "" >> "$MASTER_MD"
  elif [ -n "$LINKTREE" ]; then
    echo "👉 $LINKTREE" >> "$MASTER_MD"
    echo "" >> "$MASTER_MD"
  fi

  [ -n "$CTA" ] && echo "**CTA:** $CTA" >> "$MASTER_MD"
  echo "" >> "$MASTER_MD"

  if [ -n "$HASHTAGS" ]; then
    echo "$HASHTAGS" >> "$MASTER_MD"
    echo "" >> "$MASTER_MD"
  fi

  # Save per-theme file too
  THEME_FILE="$OUTDIR/${T}.md"
  awk '1' "$MASTER_MD" > "$THEME_FILE"

done

# Also output a short caption for quick posting
SHORT="$OUTDIR/short_caption.txt"
{
  echo "Wellness day: powerful + grounding."
  echo "${LINKTREE:-}"
  echo "${HASHTAGS:-}"
} > "$SHORT"

echo "[$(ts)] Wrote: $MASTER_MD" | tee -a "$LOG"
echo "[$(ts)] Wrote: $SHORT" | tee -a "$LOG"
echo "[$(ts)] daily_pack done" | tee -a "$LOG"
