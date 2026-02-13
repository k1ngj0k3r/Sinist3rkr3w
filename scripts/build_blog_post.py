#!/data/data/com.termux/files/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import random
import sys


def load_config(cfg_path: Path) -> dict:
    with cfg_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def pick_from(items, rng: random.Random, fallback: str) -> str:
    if not items:
        return fallback
    return rng.choice(items)


def build_blog_post(cfg: dict, theme_id: str | None = None, now: datetime | None = None) -> str:
    """
    Medium/Substack-ready markdown blog post with built-in variation.
    Linktree is pinned so the link never drifts.
    """
    now = now or datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    generated_str = now.strftime("%Y-%m-%d %H:%M")

    brand = cfg.get("brand")
    if isinstance(brand, dict):
        brand_name = brand.get("name", "Sinist3rKr3w")
    else:
        brand_name = str(brand) if brand else "Sinist3rKr3w"

    # Pinned linktree (your requirement)
    linktree_url = "https://linktr.ee/k1ngj0k"

    themes = cfg.get("themes", [])
    themes_by_id = {t.get("id"): t for t in themes if isinstance(t, dict) and t.get("id")}

    # Deterministic randomness per day (so it changes daily but stays stable if rerun)
    rng = random.Random(date_str)

    # Choose theme
    if theme_id and theme_id in themes_by_id:
        theme = themes_by_id[theme_id]
    else:
        theme = rng.choice(themes) if themes else {"id": "hub", "label": "One Hub", "hooks": [], "ctas": []}

    label = theme.get("label", theme.get("id", "One Hub"))
    hooks = theme.get("hooks", [])
    ctas = theme.get("ctas", [])

    hook = pick_from(hooks, rng, "One link. One hub. Everything connected.")
    cta = pick_from(ctas, rng, "Stay locked in 🔥")

    hashtags = cfg.get("hashtags", [])
    if isinstance(hashtags, list):
        tag_line = " ".join([h for h in hashtags if isinstance(h, str)])
    else:
        tag_line = "#Sinist3rKr3w #CreatorLife #LinkInBio"

    # --- NEW: Rotation pools to avoid repeating the same blog every time ---
    intro_pool = [
        "In today’s world, creators need one simple place where everything connects.",
        "Creators don’t need 15 links. They need one clean hub.",
        "If you’ve ever had to hunt down a creator’s links… you get why a hub matters.",
        "Everything is scattered online. A hub fixes that."
    ]

    bridge_pool = [
        "That’s why I run everything through one place — content, drops, updates, all of it.",
        "So I keep it simple: one place that connects the whole ecosystem.",
        "That’s why I centralize it — less friction, more focus.",
        "One hub keeps the noise down and the momentum up."
    ]

    why_pool = [
        "People don’t want clutter. They want clarity.",
        "If it’s hard to find, it’s easy to ignore. A hub removes friction.",
        "The easier it is to follow, the more likely people actually stick around.",
        "A clean path beats a complicated maze — every time."
    ]

    final_pool = [
        "If you support independent creators and real hustle, bookmark the hub and stay tuned.",
        "If you’ve been here rocking with us, you already know — this is just the beginning.",
        "This is the build. If you feel it, you’re part of it.",
        "No fluff. Just progress. Stay locked in."
    ]

    whatnext_pool = [
    f"- {cta}\n- Browse the latest: {linktree_url}",
    f"- {cta}\n- Check what’s new: {linktree_url}",
    f"- {cta}\n- Follow the hub: {linktree_url}",
    f"- {cta}\n- Bookmark this: {linktree_url}",
    f"- {cta}\n- If you want to support, start here: {linktree_url}",
    f"- {cta}\n- New drops + updates live here: {linktree_url}",
]
    # Assemble with rotation
    intro = pick_from(intro_pool, rng, intro_pool[0])
    bridge = pick_from(bridge_pool, rng, bridge_pool[0])
    why = pick_from(why_pool, rng, why_pool[0])
    final = pick_from(final_pool, rng, final_pool[0])
    what_next = pick_from(whatnext_pool, rng, whatnext_pool[0])

    title = "One Link. One Hub. Everything Connected."

    body = f"""# {title}

**Pillar:** {label}  
**Date:** {date_str}  
**Brand:** {brand_name}  
**Generated:** {generated_str}

{intro}

{bridge}

Whether you’re here for **{label}**, it all starts in one place.

👉 {linktree_url}

## Why this matters
{why}

## What to do next
{what_next}

## Final Thoughts
{final}

---
{tag_line}
"""
    return body


def main() -> int:
    base_dir = Path.home() / "kr3w"
    cfg_path = base_dir / "kr3w_config.json"
    out_dir = base_dir / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Optional: python3 build_blog_post.py merch (forces a theme)
    theme_id = sys.argv[1] if len(sys.argv) > 1 else None

    cfg = load_config(cfg_path)
    post = build_blog_post(cfg, theme_id=theme_id)

    today = datetime.now().strftime("%Y-%m-%d")
    out_file = out_dir / f"blog_{today}.md"
    out_file.write_text(post, encoding="utf-8")

    print(post.strip())
    print(f"\n✅ Saved: {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
