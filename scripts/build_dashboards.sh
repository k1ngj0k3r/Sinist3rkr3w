#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

BASE="$HOME/kr3w"
OUT="$BASE/output"

PUB_HTML="$OUT/dashboard.html"
PRIV_HTML="$OUT/dashboard_private.html"

PUB_JSON="$OUT/dashboard.json"
PRIV_JSON="$OUT/dashboard_private.json"

mkdir -p "$OUT"

python3 - <<'PY'
import json, os, html, datetime

base = os.path.expanduser("~/kr3w")
out  = os.path.join(base, "output")

pub_json  = os.path.join(out, "dashboard.json")
priv_json = os.path.join(out, "dashboard_private.json")

# ----- Load public dashboard data -----
with open(pub_json, "r", encoding="utf-8") as f:
    pub = json.load(f)

# ----- Build private dashboard data safely -----
# This pulls from your private folder if it exists. If not, it still builds.
private_path = os.path.join(base, "private", "skpu.json")
priv = {"title": "SKPU (Private)", "sections": [], "updated": datetime.datetime.now().isoformat(timespec="seconds")}

if os.path.exists(private_path):
    with open(private_path, "r", encoding="utf-8") as f:
        priv = json.load(f)
        if "updated" not in priv:
            priv["updated"] = datetime.datetime.now().isoformat(timespec="seconds")

# ----- Save private JSON to output (NOT meant to be pushed) -----
os.makedirs(out, exist_ok=True)
with open(priv_json, "w", encoding="utf-8") as f:
    json.dump(priv, f, ensure_ascii=False, indent=2)

def render_dashboard(data, title_fallback="Dashboard"):
    title = data.get("title") or data.get("brand") or title_fallback
    updated = data.get("updated", "")
    sections = data.get("sections", [])

    def esc(x): return html.escape(str(x))

    rows = []
    for sec in sections:
        name = esc(sec.get("name",""))
        items = sec.get("items", [])
        li = []
        for it in items:
            t = esc(it.get("title",""))
            d = esc(it.get("detail",""))
            li.append(f"<li><b>{t}</b> — {d}</li>" if d else f"<li><b>{t}</b></li>")
        ul = "<ul>" + "".join(li) + "</ul>" if li else "<div class='muted'>No items yet.</div>"
        rows.append(f"<div class='card'><h2>{name}</h2>{ul}</div>")

    body = "".join(rows) if rows else "<div class='card'><h2>Empty</h2><div class='muted'>No sections yet.</div></div>"

    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<style>
  body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial; background:#0b0b0b; color:#f2f2f2; margin:0; padding:16px}}
  .wrap{{max-width:900px; margin:0 auto}}
  .top{{display:flex; justify-content:space-between; align-items:baseline; gap:12px; flex-wrap:wrap}}
  .muted{{color:#b5b5b5; font-size:12px}}
  .card{{background:#151515; border:1px solid #2a2a2a; border-radius:14px; padding:14px; margin-top:12px}}
  h1{{margin:0; font-size:20px}}
  h2{{margin:0 0 8px 0; font-size:16px}}
  ul{{margin:0; padding-left:18px}}
  li{{margin:6px 0}}
  a{{color:#7dd3fc}}
</style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <h1>{esc(title)}</h1>
      <div class="muted">{("Updated: " + esc(updated)) if updated else ""}</div>
    </div>
    {body}
    <div class="card muted">Tip: Public dashboard is safe to publish. Private dashboard is local-only.</div>
  </div>
</body>
</html>"""

# ----- Write HTML files -----
pub_html  = os.path.join(out, "dashboard.html")
priv_html = os.path.join(out, "dashboard_private.html")

with open(pub_html, "w", encoding="utf-8") as f:
    f.write(render_dashboard(pub, "Public Dashboard"))

with open(priv_html, "w", encoding="utf-8") as f:
    f.write(render_dashboard(priv, "SKPU (Private)"))

print("✅ Public dashboard:", pub_html)
print("✅ Private dashboard:", priv_html)
print("✅ Private JSON:", priv_json)
PY

echo "Done."
