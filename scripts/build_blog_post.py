#!/usr/bin/env python3
import json, os
from datetime import datetime

HOME = os.path.expanduser("~")
OUTDIR = os.path.join(HOME, "kr3w", "output")

def load_cfg():
    cfg_path = os.path.join(HOME, "kr3w", "kr3w_config.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_dashboard_json():
    path = os.path.join(OUTDIR, "dashboard.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def pick_theme(cfg):
    themes = cfg.get("themes", [])
    if not themes:
        return None
    day = datetime.now().day
    return themes[(day - 1) % len(themes)]

def md_escape(s: str) -> str:
    return s.replace("\n", " ").strip()

def main():
    os.makedirs(OUTDIR, exist_ok=True)

    cfg = load_cfg()
    brand = cfg.get("brand", {})
    brand_name = brand if isinstance(brand, str) else brand.get("name", "Sinist3rKr3w")

    links = cfg.get("links", {})
    theme = pick_theme(cfg)

    dash = load_dashboard_json() or {}
    hashtags = " ".join(cfg.get("hashtags", [])[:6])

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    label = theme["label"] if theme else "Daily Drop"
    primary_key = theme["primary_link"] if theme else "hub"
    primary_url = links.get(primary_key, links.get("hub", ""))

    hooks = theme.get("hooks", []) if theme else []
    ctas = theme.get("ctas", []) if theme else []

    hook = hooks[0] if hooks else "Creators don’t need clutter. They need clarity."
    angle = hooks[1] if len(hooks) > 1 else "One link. One destination. Everything connected."
    cta = ctas[0] if ctas else "Bookmark the hub"

    title = f"{label}: One Link. One Hub. Everything Connected."

    # Route to Linktree if present, otherwise use theme primary link
    route_url = links.get("linktree") or primary_url

    blog = f"""# {title}

**Date:** {today}  
**Brand:** {brand_name}  
**Generated:** {now}

## The point (no fluff)
{md_escape(hook)}

{md_escape(angle)}

## What to do next
- **{md_escape(cta)}**
- Tap here: {route_url}

## Why this matters
People don’t want clutter — they want clarity.  
So we’re building a simple hub that keeps everything connected.

**Stay locked in.** 🔥  
{hashtags}
"""

    out_path = os.path.join(OUTDIR, f"blog_{today}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(blog)

    print(f"✅ Blog draft written: {out_path}")

if __name__ == "__main__":
    main()
