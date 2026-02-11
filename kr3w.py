import json
import os
import argparse
from datetime import date as dt_date, datetime, timedelta
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_config():
    cfg_path = os.path.join(BASE_DIR, "kr3w_config.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_dirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

def pick(rng, items, fallback=""):
    if not items:
        return fallback
    return rng.choice(items)

def fmt_links(cfg):
    links = cfg.get("links", {})
    return links

def build_assets(cfg, for_date: dt_date):
    # deterministic per-day output
    rng = random.Random(for_date.isoformat())

    brand = cfg.get("brand", {})
    links = fmt_links(cfg)

    # Defaults if not in config (we’ll expand this in Step 2)
    hooks = cfg.get("hooks", [
        "One Link. One Hub. Everything Connected.",
        "If you’re building something real, you need one place that ties it all together.",
        "Creators don’t need clutter. They need clarity."
    ])
    themes = cfg.get("themes", [
        {"id": "hub", "label": "hub-first", "primary_link": "linktree"},
        {"id": "merch", "label": "merch", "primary_link": "tiktok_shop"},
        {"id": "wellness", "label": "wellness", "primary_link": "mydailychoice_daily_spray"},
    ])
    ctas = cfg.get("ctas", [
        "Tap the hub 👇",
        "Bookmark the hub and stay locked in 🔥",
        "Start here 👇"
    ])
    hashtags = cfg.get("hashtags", ["#LinkInBio", "#CreatorLife", "#SmallBusiness"])

    theme = pick(rng, themes, {"id":"hub","label":"hub-first","primary_link":"linktree"})
    hook = pick(rng, hooks)
    cta = pick(rng, ctas)
    tag_str = " ".join(hashtags[:6])

    primary_key = theme.get("primary_link", "linktree")
    primary_url = links.get(primary_key, links.get("linktree", ""))

    name = brand.get("name", "Sinist3rkr3w")
    tagline = brand.get("tagline", "Where you matter most.")
    sms_keyword = brand.get("sms_keyword", "KR3W")

    # --- BLOG (markdown) ---
    blog = []
    blog.append(f"# {hook}\n")
    blog.append(f"In today’s world, creators need one simple place where everything connects.\n")
    blog.append(f"That’s why I use a central hub that keeps all my content, products, and updates together.\n")
    blog.append(f"Whether you’re here for **{theme.get('label','everything')}**, it all starts in one place.\n")
    blog.append(f"👉 {primary_url}\n")
    blog.append("## Why this matters\n")
    blog.append("People don’t want clutter. They want clarity.\n")
    blog.append("One link. One destination. Everything connected.\n")
    blog.append("## Final Thoughts\n")
    blog.append(f"If you support independent creators and real hustle, bookmark the hub and stay tuned.\n")
    blog_md = "\n".join(blog).strip() + "\n"

    # --- FACEBOOK AD (short) ---
    fb_ad = (
        f"{name}: {tagline}\n\n"
        f"{hook}\n"
        f"One hub for merch, wellness, and updates.\n\n"
        f"{cta}\n{primary_url}\n\n"
        f"{tag_str}\n"
    )

    # --- TIKTOK CAPTION / AD ---
    tt_ad = (
        f"{hook}\n"
        f"{cta} {primary_url}\n"
        f"{tag_str}\n"
    )

    # --- SHORT CAPTION ---
    caption = (
        f"{hook}\n"
        f"{primary_url}\n"
        f"{tag_str}\n"
    )
    # --- YOUTUBE DESCRIPTION ---
    yt = (
         f"{hook}\n\n"
         f"{cta}\n"
         f"{primary_url}\n\n"
         f"{tag_str}\n"
    )

    # --- SMS/DM CTA (opt-in style) ---
    sms = (
        f"{name}: {tagline}\n"
        f"Want the hub link + updates? Reply '{sms_keyword}' and I’ll send it.\n"
        f"{primary_url}\n"
    )

    return {
        "blog": blog_md,
        "ad_facebook": fb_ad,
        "ad_tiktok": tt_ad,
        "caption_short": caption,
        "sms_cta": sms,
        "youtube": yt,
        "meta": {
            "date": for_date.isoformat(),
            "theme": theme,
            "primary_link": primary_key,
            "primary_url": primary_url
        }
    }

def write_assets(out_dir, assets):
    d = assets["meta"]["date"]
    def w(fname, content):
        path = os.path.join(out_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    w(f"blog_{d}.md", assets["blog"])
    w(f"ad_facebook_{d}.txt", assets["ad_facebook"])
    w(f"ad_tiktok_{d}.txt", assets["ad_tiktok"])
    w(f"caption_short_{d}.txt", assets["caption_short"])
    w(f"sms_cta_{d}.txt", assets["sms_cta"])
    w(f"youtube_{d}.txt", assets["youtube"])
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="YYYY-MM-DD (default: today)")
    p.add_argument("--days", type=int, default=1, help="Generate N days starting at --date (or today)")
    return p.parse_args()

def main():
    args = parse_args()
    cfg = load_config()

    start = dt_date.today()
    if args.date:
        start = datetime.strptime(args.date, "%Y-%m-%d").date()

    out_dir = os.path.join(BASE_DIR, "output")
    log_dir = os.path.join(BASE_DIR, "logs")
    ensure_dirs(out_dir, log_dir)

    log_path = os.path.join(log_dir, "run.log")
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"=== KR3W RUN {start.isoformat()} days={args.days} ===\n")

        for i in range(args.days):
            day = start + timedelta(days=i)
            assets = build_assets(cfg, day)
            write_assets(out_dir, assets)
            log.write(f"Generated: {day.isoformat()} theme={assets['meta']['theme'].get('id','')}\n")

        log.write("=== DONE ===\n")

    print(f"✅ Generated {args.days} day(s) starting {start.isoformat()}")
    print(f"📁 Output: {out_dir}")
    print(f"🧾 Log: {log_path}")

if __name__ == "__main__":
    main()
