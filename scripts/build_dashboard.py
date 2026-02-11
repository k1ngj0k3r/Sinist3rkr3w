#!/usr/bin/env python3
import os
import json
from datetime import datetime

HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, "kr3w")
OUT_DIR = os.path.join(ROOT, "output")
CFG_PATH = os.path.join(ROOT, "kr3w_config.json")

FILES = [
    ("caption_short", "caption_short_", ".txt"),
    ("ad_tiktok", "ad_tiktok_", ".txt"),
    ("ad_facebook", "ad_facebook_", ".txt"),
    ("youtube", "youtube_", ".txt"),
    ("blog", "blog_", ".md"),
    ("sms_cta", "sms_cta_", ".txt"),
]

def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def latest_date_from_output():
    # Find the newest youtube_YYYY-MM-DD.txt or caption_short_YYYY-MM-DD.txt and extract date
    candidates = []
    if not os.path.isdir(OUT_DIR):
        return None

    for fn in os.listdir(OUT_DIR):
        for key, prefix, suffix in FILES:
            if fn.startswith(prefix) and fn.endswith(suffix):
                # expects prefix + YYYY-MM-DD + suffix
                date_part = fn[len(prefix):-len(suffix)]
                if len(date_part) == 10 and date_part[4] == "-" and date_part[7] == "-":
                    full = os.path.join(OUT_DIR, fn)
                    candidates.append((os.path.getmtime(full), date_part))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]

def load_cfg():
    try:
        with open(CFG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def html_escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#39;"))

def build_dashboard_html(data):
    brand = data.get("brand_name", "Sinist3rKr3w")
    day = data.get("date", "")
    links = data.get("links", {})
    blocks = data.get("blocks", {})

    def link_li(label, url):
        if not url:
            return ""
        return f'<li><a href="{html_escape(url)}" target="_blank" rel="noopener noreferrer">{html_escape(label)}</a></li>'

    def block_section(title, content):
        if not content:
            content = "(missing)"
        return f"""
        <section class="card">
          <div class="card-head">
            <h2>{html_escape(title)}</h2>
            <button class="copy" data-copy="{html_escape(content)}">Copy</button>
          </div>
          <pre>{html_escape(content)}</pre>
        </section>
        """

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{html_escape(brand)} Dashboard — {html_escape(day)}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 0; background: #0b0b0b; color: #f2f2f2; }}
    .wrap {{ max-width: 980px; margin: 0 auto; padding: 18px; }}
    .top {{ display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:space-between; margin-bottom: 14px; }}
    .title h1 {{ margin:0; font-size: 20px; }}
    .title p {{ margin:4px 0 0 0; opacity:.8; font-size: 13px; }}
    .links {{ background:#141414; border:1px solid #222; border-radius: 14px; padding: 12px; }}
    .links ul {{ margin:0; padding-left: 18px; }}
    a {{ color: #7dd3fc; text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    .grid {{ display:grid; grid-template-columns: 1fr; gap: 12px; }}
    @media (min-width: 860px) {{ .grid {{ grid-template-columns: 1fr 1fr; }} }}
    .card {{ background:#141414; border:1px solid #222; border-radius: 14px; padding: 12px; }}
    .card-head {{ display:flex; align-items:center; justify-content:space-between; gap: 10px; }}
    h2 {{ margin:0; font-size: 15px; }}
    pre {{ white-space: pre-wrap; word-wrap: break-word; margin: 10px 0 0 0; background:#0f0f0f; border:1px solid #232323; padding: 10px; border-radius: 12px; font-size: 13px; }}
    .copy {{ background:#1f2937; border:1px solid #374151; color:#fff; padding: 8px 10px; border-radius: 12px; cursor:pointer; font-size: 12px; }}
    .copy:hover {{ filter: brightness(1.1); }}
    .foot {{ opacity:.7; font-size: 12px; margin-top: 16px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <div class="title">
        <h1>{html_escape(brand)} — Daily Dashboard</h1>
        <p>Date: <strong>{html_escape(day)}</strong> • Generated: {html_escape(data.get("generated_at",""))}</p>
      </div>

      <div class="links">
        <strong>Quick Links</strong>
        <ul>
          {link_li("Main Hub", links.get("hub"))}
          {link_li("YouTube", links.get("youtube"))}
          {link_li("MyDailyChoice", links.get("mydailychoice"))}
          {link_li("Linktree", links.get("linktree"))}
        </ul>
      </div>
    </div>

    <div class="grid">
      {block_section("Short Caption", blocks.get("caption_short",""))}
      {block_section("TikTok Ad", blocks.get("ad_tiktok",""))}
      {block_section("Facebook Ad", blocks.get("ad_facebook",""))}
      {block_section("YouTube Description", blocks.get("youtube",""))}
      {block_section("SMS/DM CTA", blocks.get("sms_cta",""))}
      {block_section("Blog (Markdown)", blocks.get("blog",""))}
    </div>

    <div class="foot">Tip: open this file anytime: <code>~/kr3w/output/dashboard.html</code></div>
  </div>

<script>
  document.querySelectorAll(".copy").forEach(btn => {{
    btn.addEventListener("click", async () => {{
      const text = btn.getAttribute("data-copy") || "";
      try {{
        await navigator.clipboard.writeText(text);
        const old = btn.textContent;
        btn.textContent = "Copied ✅";
        setTimeout(() => btn.textContent = old, 900);
      }} catch (e) {{
        alert("Copy failed. Long-press inside the block and copy manually.");
      }}
    }});
  }});
</script>
</body>
</html>
"""

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    day = latest_date_from_output()
    if not day:
        print("No output files found yet. Run: python3 kr3w.py")
        return

    cfg = load_cfg()
    brand = cfg.get("brand", {})
    if isinstance(brand, str):
        brand_name = brand
    else:
        brand_name = brand.get("name", "Sinist3rKr3w")

    links = cfg.get("links", {}) if isinstance(cfg.get("links", {}), dict) else {}

    blocks = {}
    for key, prefix, suffix in FILES:
        blocks[key] = read_text(os.path.join(OUT_DIR, f"{prefix}{day}{suffix}"))

    data = {
        "date": day,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "brand_name": brand_name,
        "links": links,
        "blocks": blocks,
    }

    # write JSON snapshot (nice for debugging)
    with open(os.path.join(OUT_DIR, "dashboard.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # write HTML dashboard
    html = build_dashboard_html(data)
    with open(os.path.join(OUT_DIR, "dashboard.html"), "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Dashboard built: {os.path.join(OUT_DIR, 'dashboard.html')}")

if __name__ == "__main__":
    main()
