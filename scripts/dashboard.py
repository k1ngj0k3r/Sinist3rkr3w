#!/usr/bin/env python3
import os
import json

HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, "kr3w")
OUT_DIR = os.path.join(ROOT, "output")
DASH_JSON = os.path.join(OUT_DIR, "dashboard.json")
DASH_HTML = os.path.join(OUT_DIR, "dashboard.html")

def main():
    if not os.path.exists(DASH_JSON):
        print("❌ dashboard.json not found.")
        print("Run these:")
        print("  python3 kr3w.py")
        print("  python3 scripts/build_dashboard.py")
        return

    with open(DASH_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n📊 KR3W DASHBOARD")
    print("────────────────────────────")
    print(f"Brand: {data.get('brand_name','')}")
    print(f"Date:  {data.get('date','')}")
    print(f"Gen:   {data.get('generated_at','')}\n")

    links = data.get("links", {})
    print("🔗 Links")
    for k in ["hub", "youtube", "mydailychoice", "linktree"]:
        v = links.get(k, "")
        if v:
            print(f"  - {k}: {v}")

    blocks = data.get("blocks", {})
    def preview(key, n=120):
        t = (blocks.get(key,"") or "").replace("\n", " ").strip()
        return (t[:n] + "…") if len(t) > n else t

    print("\n🧾 Previews")
    print(f"  Short caption: {preview('caption_short')}")
    print(f"  TikTok ad:     {preview('ad_tiktok')}")
    print(f"  Facebook ad:   {preview('ad_facebook')}")
    print(f"  YouTube desc:  {preview('youtube')}")
    print(f"  SMS CTA:       {preview('sms_cta')}")
    print(f"  Blog:          {preview('blog')}")

    print("\n📁 Files")
    print(f"  HTML: {DASH_HTML}")
    print(f"  JSON: {DASH_JSON}\n")

if __name__ == "__main__":
    main()
