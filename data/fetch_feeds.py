#!/usr/bin/env python3
"""Fetches the latest @picklebrx YouTube videos and Instagram posts.

Run before build.py. Writes data/youtube.json and data/instagram.json.
If a fetch fails, the old file is kept, so the build never breaks.

YouTube: uses the channel's public RSS feed (no API key).
Instagram: uses a Behold JSON feed (free at behold.so). Paste the feed ID into
INSTAGRAM_FEED_ID below, or set the BEHOLD_FEED_ID environment variable.
"""
import json, os, re, sys, urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
YT_HANDLE = "picklebrx"
YT_CHANNEL_ID = ""          # filled in automatically if empty (looked up from the handle)
INSTAGRAM_FEED_ID = "HKCsNYibzzhqQyeDCWxn"  # Behold feed for @picklebrx (public, read-only)
UA = {"User-Agent": "Mozilla/5.0 (compatible; pickleballrx-site-builder)", "Accept-Language": "en-US,en;q=0.9"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def save(name, data):
    with open(os.path.join(HERE, name), "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
        f.write("\n")


def channel_id():
    cid = os.environ.get("YT_CHANNEL_ID") or YT_CHANNEL_ID
    if cid:
        return cid
    page = get(f"https://www.youtube.com/@{YT_HANDLE}").decode("utf-8", "replace")
    for pat in (r'<link rel="canonical" href="https://www\.youtube\.com/channel/(UC[\w-]{22})"',
                r'"externalId":"(UC[\w-]{22})"', r'"channelId":"(UC[\w-]{22})"'):
        m = re.search(pat, page)
        if m:
            return m.group(1)
    raise RuntimeError("channel ID not found on the channel page")


def youtube():
    cid = channel_id()
    print("YouTube channel ID:", cid)
    root = ET.fromstring(get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
          "media": "http://search.yahoo.com/mrss/"}
    videos = []
    for en in root.findall("a:entry", ns):
        vid = en.findtext("yt:videoId", "", ns)
        link = en.find("a:link", ns)
        href = link.get("href", "") if link is not None else ""
        desc = en.findtext("media:group/media:description", "", ns) or ""
        if not re.fullmatch(r"[\w-]{11}", vid):
            continue
        videos.append(dict(
            id=vid,
            title=en.findtext("a:title", "", ns).strip(),
            published=en.findtext("a:published", "", ns)[:10],
            short="/shorts/" in href,
            description=desc.strip()[:300],
        ))
    if not videos:
        raise RuntimeError("feed had no videos")
    save("youtube.json", {"channel_id": cid, "videos": videos})
    print(f"YouTube: saved {len(videos)} videos (newest: {videos[0]['title']!r})")


def instagram():
    fid = os.environ.get("BEHOLD_FEED_ID") or INSTAGRAM_FEED_ID
    if not fid:
        print("Instagram: no Behold feed ID set yet, skipping")
        return
    if not re.fullmatch(r"[\w-]+", fid):
        raise RuntimeError("feed ID looks wrong")
    data = json.loads(get(f"https://feeds.behold.so/{fid}"))
    raw = data.get("posts", []) if isinstance(data, dict) else data
    posts = []
    for p in raw:
        link = p.get("permalink", "")
        if not link.startswith("https://www.instagram.com/"):
            continue
        sizes = p.get("sizes") or {}
        img = ((sizes.get("medium") or sizes.get("small") or {}).get("mediaUrl")
               or (p.get("thumbnailUrl") if p.get("mediaType") == "VIDEO" else p.get("mediaUrl")) or "")
        if not img.startswith("https://"):
            continue
        posts.append(dict(link=link, image=img, video=p.get("mediaType") == "VIDEO",
                          caption=(p.get("prunedCaption") or p.get("caption") or "").strip()[:200],
                          date=(p.get("timestamp") or "")[:10]))
    if not posts:
        raise RuntimeError("feed had no posts")
    save("instagram.json", {"posts": posts})
    print(f"Instagram: saved {len(posts)} posts")


if __name__ == "__main__":
    ok = True
    for fn in (youtube, instagram):
        try:
            fn()
        except Exception as ex:  # keep the last good file and carry on
            ok = False
            print(f"{fn.__name__}: fetch failed, keeping the old data ({ex})", file=sys.stderr)
    if "--strict" in sys.argv and not ok:
        sys.exit(1)
