#!/usr/bin/env python3
"""Builds the PickleballRx static site.

Usage:  python3 build.py            (writes into ./site next to this file)

Edit data/paddles.json to add or change paddles, then run this and zip site/.
Edit VIDEOS, LAB and CODES below for the Videos, Paddle lab and Discount codes pages.
"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
DATA = json.load(open(os.path.join(ROOT, "data", "paddles.json")))
PADDLES = DATA["paddles"]
LABS = json.load(open(os.path.join(ROOT, "data", "labs.json")))
SPECS = json.load(open(os.path.join(ROOT, "data", "specs.json")))["paddles"]
XRAY = json.load(open(os.path.join(ROOT, "data", "xray.json")))["paddles"]

YOUTUBE = "https://www.youtube.com/@picklebrx"
INSTAGRAM = "https://www.instagram.com/picklebrx/"

# YouTube videos for the Videos page. id = the part after watch?v=
VIDEOS = [
    # dict(id="XXXXXXXXXXX", title="Paddle name review", paddle="slug-of-paddle"),
]

# Lab images: put files in site/assets/lab/ and list them here.
LAB = {
    "xray": [],   # dict(src="assets/lab/name.jpg", paddle="Paddle name", caption="What it shows")
    "micro": [],
    "other": [],
}

# Discount codes. Leave empty until you have real codes from brands.
CODES = [  # confirmed by Siva 2026-11-17
    dict(brand="Arronax", code="PBRX", offer="15% off", url="https://arronaxpickleball.com/"),
    dict(brand="Evolv", code="PBRX", offer="15% off", url="https://evolvpickleball.com/"),
    dict(brand="Holbrook", code="PBRX", offer="15% off", url="https://holbrookpickleball.com/"),
    dict(brand="Luzz", code="PBRX", offer="15% off", url="https://luzzpickleball.com/"),
    dict(brand="RPM", code="PBRX", offer="15% off", url="https://rpmpb.com/"),
    dict(brand="MARK", code="PBRX", offer="10% off", url="https://markpickleball.com/"),
    dict(brand="Pakle", code="PBRX", offer="10% off", url="https://paklepickleball.com/"),
    dict(brand="Speedup", code="PBRX", offer="10% off", url="https://speeduppickle.com/"),
    dict(brand="Grit", code="PBRX", offer="10% off", url="https://www.grit-shop.com/", no_disc=True),
]



def product_photo(slug):
    """Brand product photo supplied by Siva, keyed by X-ray slug (assets/paddles/product/<slug>.jpg)."""
    rel = f"assets/paddles/product/{slug}.jpg"
    return rel if slug and os.path.exists(os.path.join(OUT, rel)) else ""


# Product photos keyed by the paddle name used in the lab data.
NAME_PHOTO = {"Gearbox Pressure XE": "gearbox-pressure-x-8e", "Gearbox Pressure X 8E": "gearbox-pressure-x-8e", "Gearbox Pressure X M": "gearbox-pressure-xm", "RPM Friction Pro V2": "rpm-v2", "Evolv Origin (CarbonSkyn)": "evolv-origin", "Luzz Cannon XPP": "luzz-cannon-xpp",
              "Grit E2CF": "grit-e2-cf", "Grit E1 CW": "grit-e1-cw", "Grit E1 TW": "grit-e1-tw",
              "Holbrook Fuze": "holbrook-fuze", "Holbrook Fuze VantaGrit": "holbrook-fuze", "Mark Unmarked 2026": "mark-unmarked-2026",
              "MARK unMARKed 2026": "mark-unmarked-2026", "Luzz Inferno M2": "luzz-inferno-2", "Luzz Inferno2": "luzz-inferno-2",
              "CPX Hyper+": "cpx-hyper-plus", "E6 Ignis": "e6-ignis",
              "RPM Jade": "rpm-jade", "Mehau S5": "mehau-s5", "Proton Project Coyote": "proton-project-coyote",
              "VANWIN Alpha Control": "vanwin-alpha-control", "Luzz Glider 2026": "luzz-glider-2026",
              "Selkirk LABS Project Boomstik": "selkirk-labs-project-boomstik", "Zcebra Gazelle": "zcebra-gazelle"}
# Extra colorways shown on a paddle's own page (assets/paddles/product/<slug>-<color>.jpg).
COLORWAYS = {"grit-e2-cf": [("", "Green, Launch Edition"), ("pink", "Pink"), ("white", "White")]}


LINKS = {  # X-ray slug -> (grit collection name, spin table name)
    "11six24-hurache-jelly-bean-2": (None, "Jelly Bean Hurache 2"),
    "crush-covert": ("Crush Covert", None), "cpx-hyper-plus": ("CPX Hyper+", None), "e6-ignis": ("E6 Ignis", None),
    "evolv-origin": ("Evolv", "Evolv Origin"), "friday-aura-pro-tour": ("Friday Aura Pro Tour (beta)", "Friday Aura Pro Tour (Beta)"),
    "gearbox-pressure-x-8e": ("Gearbox Pressure X 8E", "Gearbox Pressure XE"), "gearbox-pressure-xm": (None, "Gearbox Pressure X M"),
    "grit-e2-cf": (None, "Grit E2CF"), "holbrook-fuze": ("Holbrook Fuze VantaGrit", "Holbrook Fuze"),
    "honolulu-j6cr": ("Honolulu J6CR", "Honolulu J6CR"), "luzz-inferno-2": ("Luzz Inferno2", None),
    "pickle-poppers-pop-n-treasure": ("Pickle Poppers Pop n Treasure", None), "pickle-poppers-pop-n-rush": ("Pickle Poppers Pop N Rush", "Pop N Rush"),
    "pact-teflon": ("PACT Teflon Evolve", None), "rpm-jade": ("RPM Jade", "RPM Jade"), "mark-unmarked-2026": ("MARK unMARKed 2026", "Mark Unmarked 2026"),
    "zcebra-gazelle": ("Zcebra Gazelle", "Zcebra Gazelle"),
    "luzz-cannon-xpp": ("Luzz Cannon XPP M1", "Luzz Cannon XPP"), "luzz-glider-2026": ("Luzz Glider 2026", None),
    "mehau-e5": ("Mehau E5", None), "mehau-s5": ("Mehau S5", None), "sypik-triton-5": ("Sypik Triton 5", None),
    "vanwin-alpha-control": ("VANWIN Alpha Control", None), "proton-project-coyote": ("Proton Project Coyote", None), "spartus-spitfire": ("Spartus Spitfire", "Spartus Spitfire"),
    "speedup-tide": ("Speed Up Tide", "Speed Up Tide"), "vanwin-alpha-power": ("VANWIN Alpha Power", None), "mehau-e4": ("Mehau E4", None),
}


import hashlib
def _asset_ver():
    h = hashlib.md5()
    for f in ("style.css", "app.js", "rx.js", "logo.svg", "logo-white.svg"):
        fp = os.path.join(OUT, "assets", f)
        if os.path.exists(fp): h.update(open(fp, "rb").read())
    return h.hexdigest()[:8]
ASSET_V = _asset_ver()  # cache-busting query string so browsers fetch new CSS/JS/logo after each change


def code_box(brand, depth=0):
    c = next((c for c in CODES if c["brand"].lower() == brand.lower() and c["code"]), None)
    if not c:
        return ""
    r = "../" * depth
    return (f'<div class="deal" style="text-align:left;margin:18px 0"><strong>Get {e(c["offer"])} at {e(c["brand"])}</strong> with code'
            f'<code style="display:inline-block;margin:0 6px">{e(c["code"])}</code><a href="{e(c["url"])}" rel="sponsored noopener">Shop {e(c["brand"])} &rarr;</a>'
            f'<div class="muted" style="font-size:.82rem;margin-top:4px">{"Brands have no input into our results." if c.get("no_disc") else "We earn a commission on code purchases. It never changes our results."} <a href="{r}disclaimers.html">Disclaimers</a></div></div>')

STYLES = [
    ("power", "Power", "Drives, put-aways, pop"),
    ("spin", "Spin", "Grit and dwell for heavy topspin"),
    ("control", "Control", "Soft hands at the kitchen"),
    ("all-court", "All-court", "A bit of everything"),
    ("beginner", "Beginner", "Forgiving and affordable"),
]

e = html.escape


def overall(p):
    return round((p["power"] + p["spin"] + p["control"] + p["forgiveness"]) / 4, 1)


def page(title, body, depth=0, current="", desc="Data-driven pickleball paddle reviews with X-rays, microscope images and on-court video."):
    r = "../" * depth

    def nav(href, label, key, cls=""):
        cur = ' aria-current="page"' if key == current else ""
        c = f' class="{cls}"' if cls else ""
        return f'<a href="{r}{href}"{cur}{c}>{label}</a>'

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{r}assets/style.css?v={ASSET_V}">
<link rel="icon" href="{r}assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">
</head>
<body>
<div class="placeholder-banner">Preview site. X-Ray, Grit and Spin Lab data is real. Paddles in the review database are sample placeholders for now.</div>
<header class="site-header"><div class="wrap">
  <a class="logo" href="{r}index.html"><img src="{r}assets/logo-white.svg?v={ASSET_V}" alt="Pickleball Rx" width="149" height="58"></a>
  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu"><span></span><span></span><span></span></button>
  <nav class="nav" id="site-nav" aria-label="Main">
    {nav("paddles.html", "Paddle database", "paddles")}
    {nav("best.html", "Top picks", "best")}
    {nav("pros.html", "Pro paddles", "pros")}
    {nav("compare.html", "Compare", "compare")}
    {nav("lab.html", "X-Ray Rx", "lab")}
    {nav("grit.html", "Grit Lab", "grit")}
    {nav("spin.html", "Spin Lab", "spin")}
    {nav("specs.html", "Spec Lab", "specs")}
    {nav("videos.html", "Videos", "videos")}
    {nav("codes.html", "Deals", "codes")}
    {nav("finder.html", "Get your paddle Rx", "finder", "nav-cta")}
  </nav>
</div></header>
<main>
{body}
</main>
<footer class="site-footer"><div class="wrap">
  <div class="cols">
    <div><img src="{r}assets/logo.svg?v={ASSET_V}" alt="Pickleball Rx" width="129" height="50" style="height:50px;width:auto;margin-bottom:10px">
      <p style="margin:0">Paddle reviews that look inside the paddle: X-rays, microscope images, measured specs and on-court video.</p><p style="margin:8px 0 0">Started by Don, Beni and Siva.</p></div>
    <div><h4>Tools</h4><ul><li><a href="{r}finder.html">Paddle finder</a></li><li><a href="{r}compare.html">Compare</a></li><li><a href="{r}paddles.html">Database</a></li></ul></div>
    <div><h4>Learn</h4><ul><li><a href="{r}guide.html">Buying guide</a></li><li><a href="{r}lab.html">X-Ray Rx</a></li><li><a href="{r}grit.html">Grit Lab</a></li><li><a href="{r}spin.html">Spin Lab</a></li><li><a href="{r}specs.html">Spec Lab</a></li><li><a href="{r}best.html">Our top picks</a></li><li><a href="{r}pros.html">What the pros play</a></li><li><a href="{r}grit-pickleball.html">Brand spotlight: Grit</a></li><li><a href="{r}evolv-pickleball.html">Brand spotlight: Evolv</a></li><li><a href="{r}gearbox-pickleball.html">Brand spotlight: Gearbox</a></li><li><a href="{r}about.html">How we test</a></li><li><a href="{r}disclaimers.html">Disclaimers</a></li></ul></div>
    <div><h4>Follow</h4><ul><li><a href="{YOUTUBE}" rel="noopener">YouTube</a></li><li><a href="{INSTAGRAM}" rel="noopener">Instagram</a></li><li><a href="{r}about.html#contact">Contact</a></li></ul></div>
  </div>
  <p class="legal">&copy; 2026 PickleballRx.org &middot; <a href="{r}disclaimers.html">Disclaimers</a> &middot; Pickleball RX earns commission on some discount codes. Brands have no input into results.</p>
</div></footer>
<script src="{r}assets/paddles.js?v={ASSET_V}"></script>
<script src="{r}assets/app.js?v={ASSET_V}"></script>
</body>
</html>
'''


def badges(p):
    b = []
    if p.get("xray"): b.append('<span class="badge">X-ray</span>')
    if p.get("micro"): b.append('<span class="badge">Microscope</span>')
    if p.get("video"): b.append('<span class="badge">Video</span>')
    if p.get("placeholder"): b.append('<span class="tag ph">Placeholder</span>')
    return '<div class="badges">' + "".join(b) + "</div>"


def card(p, depth):
    r = "../" * depth
    return f'''<article class="card">
  <div class="paddle-art" aria-hidden="true">{e(p["name"][-1])}</div>
  {badges(p)}
  <h3><a href="{r}reviews/{p["slug"]}.html">{e(p["name"])}</a></h3>
  <div class="meta">{e(p["brand"])} &middot; {e(p["shape"])} &middot; {p["core_mm"]} mm &middot; ${p["price"]}</div>
  <div class="mini-scores">
    <div><b>{p["power"]}</b><span>Power</span></div><div><b>{p["spin"]}</b><span>Spin</span></div>
    <div><b>{p["control"]}</b><span>Control</span></div><div><b>{p["forgiveness"]}</b><span>Forgive</span></div>
  </div>
  <a class="more" href="{r}reviews/{p["slug"]}.html">Read review &rarr;</a>
</article>'''


def embed(vid, title):
    return f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{e(vid)}" title="{e(title)}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'


def _fmt_date(s):
    import datetime
    d = datetime.date.fromisoformat(s)
    return f'{d.strftime("%B")} {d.day}, {d.year}'


def _feed(name, key):
    try:
        return json.load(open(os.path.join(ROOT, "data", name))).get(key, [])
    except (OSError, ValueError):
        return []


# Filled in automatically by data/fetch_feeds.py (runs every few hours on GitHub).
YT_FEED = _feed("youtube.json", "videos")
IG_FEED = _feed("instagram.json", "posts")


def yt_card(v):
    """Thumbnail that turns into the YouTube player when tapped (fast pages, no 15 iframes)."""
    vid = v["id"]
    url = f"https://www.youtube.com/{'shorts/' + vid if v.get('short') else 'watch?v=' + vid}"
    date = f'<span class="meta">{_fmt_date(v["published"])}</span>' if v.get("published") else ""
    return (f'<article class="card"><a class="video yt" href="{e(url)}" data-yt="{e(vid)}" rel="noopener" aria-label="Play {e(v["title"])}">'
            f'<img src="https://i.ytimg.com/vi/{e(vid)}/hqdefault.jpg" alt="" loading="lazy"><span class="play" aria-hidden="true"></span></a>'
            f'<h3><a href="{e(url)}" rel="noopener">{e(v["title"])}</a></h3>{date}</article>')


def ig_grid(posts):
    return '<div class="ig-grid">' + "".join(
        f'<a href="{e(p["link"])}" rel="noopener" title="{e(p.get("caption", "")[:120])}">'
        f'<img src="{e(p["image"])}" alt="{e(p.get("caption", "")[:120] or "Instagram post by @picklebrx")}" loading="lazy">'
        f'{"<span class=play aria-hidden=true></span>" if p.get("video") else ""}</a>' for p in posts) + '</div>'


def video_ph(label="Video coming soon"):
    return f'<div class="video ph"><span>&#9654; {label}</span></div>'


def lab_fig(src, alt, caption, ph_label):
    if src:
        return f'<figure class="lab-item"><a href="{src}"><img src="{src}" alt="{e(alt)}" loading="lazy"></a><figcaption>{caption}</figcaption></figure>'
    return f'<figure class="lab-item"><div class="lab-ph">{ph_label} coming soon</div><figcaption>{caption}</figcaption></figure>'


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)


# ---------- data for the browser ----------
write("assets/paddles.js", "window.PADDLES = " + json.dumps(PADDLES, indent=1) + ";\n")

# ---------- Leader Board (Siva's wall, top spot first) ----------
import re as _re
_slug = lambda t: _re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
# (brand, model, X-ray slug, spin table name, grit collection name, spec card id, note)
LEADERBOARD = [
    ("Gearbox", "Pressure X 8E", "gearbox-pressure-x-8e", "Gearbox Pressure XE", "Gearbox Pressure X 8E", "gearbox-8e", ""),
    ("Luzz", "Cannon XPP", "luzz-cannon-xpp", "Luzz Cannon XPP", "Luzz Cannon XPP M1", "luzz-cannon", ""),
    ("Bread & Butter", "Loco 2 Elongated", None, "Bread & Butter Loco 2 Elongated", "Bread & Butter LOCO 2", "bnb-loco", ""),
    ("Gearbox", "Pressure X 8M", "gearbox-pressure-xm", "Gearbox Pressure X M", None, "gearbox-8m", ""),
    ("Facolos", "Elite X V2.0", "facolos-elite-x-2-0", None, None, None, ""),
    ("Sypik", "Triton 5", "sypik-triton-5", None, "Sypik Triton 5", "sypik-triton", ""),
    ("Speedup", "Tide 14 Hybrid", "speedup-tide", "Speed Up Tide", "Speed Up Tide", None, "X-ray is of the Tide Elongated"),
    ("Grit", "E2-CF", "grit-e2-cf", "Grit E2CF", None, None, ""),
    ("Evolv", "Origin Elongated", "evolv-origin", "Evolv Origin", "Evolv", None, ""),
    ("Honolulu", "J6CR", "honolulu-j6cr", "Honolulu J6CR", "Honolulu J6CR", None, ""),
    ("Spartus", "Spitfire", "spartus-spitfire", "Spartus Spitfire", "Spartus Spitfire", None, ""),
    ("Arronax", "KVL 005", "arronax-kvl-005", None, None, None, ""),
    ("Mehau", "E5", "mehau-e5", None, "Mehau E5", None, ""),
    ("PACT", "Teflon Evolve TE16", "pact-teflon", None, "PACT Teflon Evolve", None, ""),
    ("Zcebra", "Gazelle", "zcebra-gazelle", "Zcebra Gazelle", "Zcebra Gazelle", None, ""),
]


def lb_card(i, row, star=True):
    brand, model, xs, sp, gr, sc, note = row
    # Thumbnail: prefer a real paddle photo (assets/paddles/<brand-model>.jpg), else the X-ray, else the grit scan.
    photo = product_photo(xs or _slug(brand + " " + model)) or f"assets/paddles/{_slug(brand + ' ' + model)}.jpg"
    if os.path.exists(os.path.join(OUT, photo)):
        thumb, fit = photo, "contain"
    elif xs and os.path.exists(os.path.join(OUT, f"assets/xray/{xs}-labeled.jpg")):
        thumb, fit = f"assets/xray/{xs}-labeled.jpg", "cover"
    else:
        thumb, fit = (f"assets/grit/{_slug(gr)}.jpg" if gr else ""), "cover"
    img = (f'<img class="lb-thumb" src="{thumb}" alt="{e(brand)} {e(model)}" loading="lazy" style="object-fit:{fit}">' if thumb
           else '<div class="lb-thumb"></div>')
    links = []
    if xs: links.append(f'<a class="badge" href="xray/{xs}.html">X-ray</a>')
    if sp:
        r = next((x for x in LABS["spin"] + LABS["spin_extra"] if x["paddle"] == sp), None)
        if r: links.append(f'<a class="badge" href="spin.html#{_slug(sp)}">{r["avg"]:,} RPM</a>')
    if gr: links.append(f'<a class="badge" href="grit.html#{_slug(gr)}">Grit</a>')
    if sc: links.append(f'<a class="badge" href="specs.html#{sc}">Specs</a>')
    code = next((c for c in CODES if c["brand"].lower() == brand.lower() and c["code"]), None)
    code_html = f'<div style="font-size:.82rem;margin-top:6px">Code <strong>{e(code["code"])}</strong> &middot; {e(code["offer"])} at <a href="{e(code["url"])}" rel="sponsored noopener">{e(brand)}</a></div>' if code else ""
    if brand in ("Grit", "Evolv", "Gearbox"):
        code_html += f'<div style="font-size:.82rem;margin-top:4px"><a href="{brand.lower()}-pickleball.html">Brand spotlight</a></div>'
    top = star and i == 0
    return (f'<div class="lb-item{" lb-top" if top else ""}"><div class="lb-rank">{"&#9733;" if top else i + 1}</div>{img}<div style="min-width:0">'
            f'<div class="muted" style="font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700">{e(brand)}{" &middot; top spot" if top else ""}</div>'
            f'<div style="font-weight:800;font-size:1.05rem;line-height:1.25">{e(model)}</div>'
            f'<div class="badges" style="margin-top:6px">{"".join(links)}</div>'
            + (f'<div class="muted" style="font-size:.78rem;margin-top:4px">{e(note)}</div>' if note else "") + code_html + '</div></div>')


lb_html = "".join(lb_card(i, r) for i, r in enumerate(LEADERBOARD))


# ---------- home ----------
n_x = len(XRAY)
n_m = sum(1 for p in PADDLES if p.get("micro"))
n_v = len({v["id"] for v in VIDEOS} | {p["video"] for p in PADDLES if p.get("video")})
style_tiles = "".join(f'<a class="style-tile" href="best.html#{k}"><b>{l}</b><span>{d}</span></a>' for k, l, d in STYLES)
style_tiles += '<a class="style-tile" href="codes.html"><b>Deals</b><span>Discount codes</span></a>'
style_tiles += '<a class="style-tile" href="pros.html"><b>Pro paddles</b><span>What the top pros play</span></a>'
latest = "\n".join(card(p, 0) for p in PADDLES[:3])
# ---------- Upcoming releases (public news only; mark unconfirmed items) ----------
UPCOMING = [
    dict(brand="Proton", name="Series One: Project Bluejay and Project Cardinal", status="Pre-order",
         when="Elongated, 15 mm &middot; $295 pre-order price",
         photos=[("assets/paddles/product/proton-project-bluejay.jpg", "Proton Project Bluejay"), ("assets/paddles/product/proton-project-cardinal.jpg", "Proton Project Cardinal")],
         text="Proton's next paddles come in two colorways, Bluejay and Cardinal, both elongated at 15 mm. The new paddle was in the hands of pros at the Pickleball World Championships in early November, including Meghan Dizon, Zane Ford and Naomi Nguyen. Proton hasn't published full specs yet.",
         links=[("X-ray: Project Coyote", "xray/proton-project-coyote.html"), ("X-ray: Project Peacock", "xray/proton-project-peacock.html"), ("Grit: Project Coyote", "grit.html#proton-project-coyote")],
         sources=[("The Kitchen, Nov 6, 2026", "https://thekitchenpickle.com/blogs/gear/what-paddles-top-pickleball-pros-use-worlds-november-2026/"), ("Nico the Lefty release calendar", "https://www.nicothelefty.com/news")]),
    dict(brand="Selkirk", name="Boomstik ST with Sharktooth Groove Technology", status="Just released",
         when="Released Nov 10, 2026 &middot; $350",
         photos=[("assets/paddles/product/selkirk-boomstik-st.jpg", "Selkirk Boomstik ST")],
         text="The next version of the LABS Project Boomstik. Selkirk says its new InfiniGrit Ultra surface has four times the spin friction and twice the grit durability of the original InfiniGrit. It adds a perimeter Sharktooth groove and hand-adjustable perimeter weights, and keeps the BoomCore foam core.",
         links=[("Grit: original Project Boomstik", "grit.html#selkirk-labs-project-boomstik")],
         sources=[("Selkirk press release, Nov 10, 2026", "https://www.selkirk.com/pages/press-releases/selkirk-sport-launches-boomstik-st-the-next-evolution-of-its-premier-power-paddle")]),
]


def upcoming_card(u):
    links = "".join(f'<a class="badge" href="{e(h)}">{e(t)}</a>' for t, h in u["links"])
    srcs = " &middot; ".join(f'<a href="{e(h)}" rel="noopener">{e(t)}</a>' for t, h in u["sources"])
    return (f'<div class="card" style="padding:18px"><div class="muted" style="font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700">{e(u["brand"])}</div>'
            + ('<div style="display:flex;gap:10px;margin:8px 0">' + "".join(f'<img src="{s}" alt="{e(a)}" width="80" height="120" loading="lazy" style="border-radius:8px;background:#fff;object-fit:contain">' for s, a in u["photos"]) + '</div>' if u.get("photos") else "")
            + f'<h3 style="margin:4px 0 6px">{e(u["name"])}</h3><span class="tag" style="align-self:flex-start">{e(u["status"])}</span>'
            f'<p class="muted" style="font-size:.88rem;margin:6px 0 8px">{u["when"]}</p><p style="font-size:.95rem">{e(u["text"])}</p>'
            f'<div class="badges" style="margin-bottom:10px">{links}</div><div class="muted" style="font-size:.78rem">Sources: {srcs}</div></div>')


upcoming_html = "".join(upcoming_card(u) for u in UPCOMING)

# Reviewers we like and learn from. Links go to each reviewer's own public page.
REVIEWERS = [
    ("John Kew", "Johnkew Pickleball", "Detailed paddle reviews and spin testing, plus The KewCast podcast.",
     "https://www.johnkewpickleball.com/paddle-reviews", "Paddle reviews"),
    ("Pickleball Studio", "Chris Olson", "In-depth paddle reviews, a newsletter and the Pickleball Studio podcast.",
     "https://www.youtube.com/@PickleballStudio", "YouTube"),
    ("Supasenpai", "Pickleball Senpai", "Paddle reviews and pickleball videos.",
     "https://supasenpai.com/", "Website"),
    ("Ed", "Pickleball Freak Show", "Paddle reviews and gear talk.",
     "https://www.youtube.com/@pickleballfreakshow", "YouTube"),
    ("PB on Call", "Pickleball On Call", "Paddle reviews and gear videos.",
     "https://www.youtube.com/@PickleballOnCall", "YouTube"),
]
# Supasenpai's links, supplied by Siva (2026-11-18). Shown wherever Supasenpai appears.
SENPAI_LINKS = [
    ("Website", "https://supasenpai.com/"),
    ("Paddle discounts", "https://supasenpai.com/pickleball-paddle-discount-codes"),
    ("Submit a paddle to review", "https://pickleballsenpai.com/"),
    ("YouTube", "https://www.youtube.com/@SupaSenpai"),
    ("Instagram", "https://www.instagram.com/supasenpaiofficial"),
    ("Facebook", "https://www.facebook.com/SupaSenpai"),
]
# Pickleball Studio's links, from their YouTube channel page (Siva, 2026-11-18).
STUDIO_LINKS = [
    ("Website", "https://thepickleballstudio.com/"),
    ("YouTube", "https://www.youtube.com/@PickleballStudio"),
    ("Instagram", "https://www.instagram.com/thepickleballstudio"),
]
# Johnkew Pickleball's links, from their YouTube channel page (Siva, 2026-11-18).
KEW_LINKS = [
    ("Website", "https://www.johnkewpickleball.com/"),
    ("YouTube", "https://www.youtube.com/@johnkewpickleball"),
]
# Pickleball On Call's links, from their YouTube channel page (Siva, 2026-11-18).
ONCALL_LINKS = [
    ("YouTube", "https://www.youtube.com/@PickleballOnCall"),
    ("Discount codes", "https://linktr.ee/pickleballoncall"),
    ("Instagram", "https://www.instagram.com/pboncall"),
]
# Pickleball Freak Show's links, from their Instagram profile (Siva, 2026-11-18).
FREAKSHOW_LINKS = [
    ("YouTube", "https://www.youtube.com/@pickleballfreakshow"),
    ("Website", "https://www.freakshow.com/"),
    ("Instagram", "https://www.instagram.com/pickleballfreakshow"),
    ("Facebook", "https://www.facebook.com/pickleballfreakshow"),
]
REVIEWER_LINKS = {"John Kew": KEW_LINKS, "Ed": FREAKSHOW_LINKS, "PB on Call": ONCALL_LINKS, "Supasenpai": SENPAI_LINKS, "Pickleball Studio": STUDIO_LINKS}

def _link_row(links, skip=()):
    return ('<div class="badges" style="margin:8px 0 4px">'
        + "".join(f'<a class="badge" href="{e(h)}" target="_blank" rel="noopener">{e(t)}</a>' for t, h in links if t not in skip) + '</div>')
senpai_links_html = _link_row(SENPAI_LINKS)

reviewers_html = "".join(
    f'<div class="card" style="padding:18px"><div class="muted" style="font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700">#{i}</div>'
    + (f'<div class="rev-head"><img class="rev-avatar" src="assets/reviewers/{_slug(n)}.jpg" alt="{e(n)}" width="64" height="64" loading="lazy"><div>' if os.path.exists(os.path.join(OUT, f"assets/reviewers/{_slug(n)}.jpg")) else "<div><div>")
    + f'<h3 style="margin:4px 0 2px">{e(n)}</h3><div class="muted" style="font-size:.88rem;margin-bottom:8px">{e(sub)}</div></div></div>'
    f'<p style="font-size:.95rem">{e(d)}</p><a class="btn ghost" style="align-self:flex-start" href="{e(h)}" rel="noopener" target="_blank">{e(lbl)} &rarr;</a>'
    + (_link_row(REVIEWER_LINKS[n], skip=(lbl,)) if n in REVIEWER_LINKS else "")
    + (f'<a style="font-size:.88rem;margin-top:8px" href="best.html#supa-senpai">See Supasenpai\'s top picks &rarr;</a>' if n == "Supasenpai" else "") + '</div>'
    for i, (n, sub, d, h, lbl) in enumerate(REVIEWERS, 1))

# Latest reviews only show on the home page once at least one real (non-placeholder) review exists.
_real = [p for p in PADDLES if not p.get("placeholder")]
latest_section = (f'''<section>
  <div class="section-head"><div><h2>Latest reviews</h2><p class="section-lead">Our newest full reviews.</p></div><a class="btn ghost" href="reviews/index.html">All reviews</a></div>
  <div class="grid">{"".join(card(p, 0) for p in _real[:3])}</div>
</section>
''') if _real else ""
_long = [v for v in YT_FEED if not v.get("short")] or YT_FEED
home_videos = (f'''<section id="latest-videos">
  <div class="section-head"><div><span class="tag">New on YouTube</span><h2 style="margin-top:8px">Latest videos</h2>
  <p class="section-lead">Our newest videos from <a href="{YOUTUBE}" rel="noopener">YouTube @picklebrx</a>. This updates on its own when we post.</p></div><a class="btn ghost" href="videos.html">All videos</a></div>
  <div class="grid">{"".join(yt_card(v) for v in _long[:3])}</div>
</section>
''') if YT_FEED else ""
home_ig = (f'''<section id="instagram" style="padding-top:0">
  <div class="section-head"><div><span class="tag">On Instagram</span><h2 style="margin-top:8px">Latest from @picklebrx</h2></div><a class="btn ghost" href="{INSTAGRAM}" rel="noopener">Follow on Instagram</a></div>
  {ig_grid(IG_FEED[:6])}
</section>
''') if IG_FEED else ""
write("index.html", page("PickleballRx | Pickleball paddle reviews, X-rays and data", f'''
<section class="hero"><div class="wrap">
  <div>
    <span class="tag">Paddle reviews, inside and out</span>
    <h1>See what's <em>inside</em> your next pickleball paddle.</h1>
    <p>We X-ray paddles, put their faces under a 4K microscope and measure spin at 960 frames per second. Then we play them, and test them again.</p>
    <div class="btn-row"><a class="btn yellow" href="spin.html">See the spin results</a><a class="btn ghost" href="lab.html">Inside {n_x} paddles</a></div>
  </div>
  <figure class="hero-art"><a href="#leaderboard"><img src="assets/leaderboard.jpg" alt="The Pickleball RX Leader Board: 15 paddles on the wall, Gearbox Pressure X 8E in the top spot" style="border-radius:12px;width:100%;height:auto"></a><figcaption>The Pickleball RX Leader Board. <a href="#leaderboard" style="color:#fcb92d">See the paddles</a>.</figcaption></figure>
</div></section>
<div class="stats"><div class="wrap">
  <div class="stat"><b>{n_x}</b><span>paddles X-rayed</span></div>
  <div class="stat"><b>{len(LABS["grit"])}</b><span>paddle faces under the microscope</span></div>
  <div class="stat"><b>{len(LABS["spin"]) + len(LABS["spin_extra"])}</b><span>paddles spin-tested at 960 fps</span></div>
  <div class="stat"><b>{len(LABS["durability"])}</b><span>spin durability re-tests</span></div>
</div></div>
<div class="wrap">
<section id="leaderboard">
  <div class="section-head"><div><span class="tag">Rx top picks</span><h2 style="margin-top:8px">The Leader Board</h2>
  <p class="section-lead">The paddles that earned a spot on our wall after X-rays, microscope scans, spin tests and a lot of games. One paddle holds the top spot. Tap any badge to see the lab results behind it. <a href="best.html">See our top picks by core type &rarr;</a></p></div></div>
  <div class="lb-grid">{lb_html}</div>
</section>
<section id="spotlight" style="padding-top:0">
  <a class="spotlight-band" href="grit-pickleball.html">
    <img src="assets/paddles/product/grit-e2-cf.jpg" alt="Grit E2-CF Launch Edition" width="120" height="180" loading="lazy">
    <div><span class="tag">Brand spotlight</span><h2 style="margin:8px 0 6px">Grit: the most passionate owners in pickleball</h2>
    <p>Grit is a paddle brand from Baton Rouge, Louisiana. Their E1 paddles top our spin chart, and the E2-CF kept its spin after 50+ hours of play. Use code PBRX for 10% off.</p>
    <span class="go">Meet Grit &rarr;</span></div>
  </a>
  <a class="spotlight-band" href="evolv-pickleball.html" style="margin-top:16px">
    <img src="assets/paddles/product/evolv-origin.jpg" alt="Evolv Origin" width="120" height="180" loading="lazy">
    <div><span class="tag">Brand spotlight</span><h2 style="margin:8px 0 6px">Evolv: the spin that doesn't fade</h2>
    <p>We tested three Evolv Origins at new, one month and six months of play. The CarbonSkyn face kept its spin with no measurable loss. Use code PBRX for 15% off.</p>
    <span class="go">Meet Evolv &rarr;</span></div>
  </a>
  <a class="spotlight-band" href="gearbox-pickleball.html" style="margin-top:16px">
    <img src="assets/paddles/product/gearbox-pressure-x-8e.jpg" alt="Gearbox Pressure X 8E" width="120" height="180" loading="lazy" style="background:#fff;object-fit:contain">
    <div><span class="tag">Brand spotlight</span><h2 style="margin:8px 0 6px">Gearbox: passion, engineered</h2>
    <p>Founder Rafael Filippini is one of the most passionate people in the paddle business. He went from pro racquetball and the Marines to building paddles with his own patented carbon cores. His Pressure X 8E holds the top spot on our Leader Board.</p>
    <span class="go">Meet Gearbox &rarr;</span></div>
  </a>
</section>
<section>
  <h2>Shop by how you play</h2>
  <p class="section-lead">Start with the thing you care about most.</p>
  <div class="styles">{style_tiles}</div>
</section>
<section style="padding-top:0">
  <div class="tools">
    <a class="tool" href="finder.html"><div class="ico">Rx</div><h3>Paddle finder</h3><p>Answer four quick questions and get a short list of paddles that match your game.</p><span class="go">Get your Rx &rarr;</span></a>
    <a class="tool" href="compare.html"><div class="ico">VS</div><h3>Compare paddles</h3><p>Put up to four paddles side by side: scores, measured specs and price.</p><span class="go">Compare &rarr;</span></a>
    <a class="tool" href="paddles.html"><div class="ico">DB</div><h3>Paddle database</h3><p>Every paddle from 32 brands, with key specs, prices and links to each model. Filter by brand, shape, thickness and price.</p><span class="go">Open database &rarr;</span></a>
    <a class="tool" href="lab.html"><div class="ico">X</div><h3>X-Ray Rx</h3><p>{n_x} paddles X-rayed and labeled: core, ring, inserts and handle.</p><span class="go">See inside &rarr;</span></a>
  </div>
</section>
<section id="upcoming">
  <div class="section-head"><div><span class="tag">On our radar</span><h2 style="margin-top:8px">Upcoming releases we're excited about</h2>
  <p class="section-lead">New paddles we can't wait to get into the lab. Details come from public announcements and news, linked below each one. Anything a brand hasn't confirmed is marked.</p></div></div>
  <div class="grid">{upcoming_html}</div>
</section>
<section id="reviewers">
  <div class="section-head"><div><span class="tag">Worth watching</span><h2 style="margin-top:8px">Our favorite reviewers</h2>
  <p class="section-lead">Other paddle reviewers we watch and learn from. We're not affiliated with them, and they don't endorse us.</p></div></div>
  <div class="grid">{reviewers_html}</div>
</section>
{latest_section}
<section>
  <h2>The labs</h2>
  <p class="section-lead">Most reviews stop at "it feels poppy." We look inside, zoom in and measure.</p>
  <div class="tools">
    <a class="tool" href="lab.html"><div class="ico">X</div><h3>X-Ray Rx</h3><p>Core, perimeter ring, inserts and handle, labeled from the X-ray for {n_x} paddles.</p><span class="go">See inside &rarr;</span></a>
    <a class="tool" href="grit.html"><div class="ico">&micro;</div><h3>Grit Lab</h3><p>{len(LABS["grit"])} paddle faces under a 4K microscope, plus wear studies after months of play.</p><span class="go">See the grit &rarr;</span></a>
    <a class="tool" href="spin.html"><div class="ico">RPM</div><h3>Spin Lab</h3><p>Same rig, same ball machine, 960 frames per second. Test, play, then test again.</p><span class="go">See spin results &rarr;</span></a>
    <a class="tool" href="specs.html"><div class="ico">SW</div><h3>Spec Lab</h3><p>Swing weight, twist weight and static weight, measured ourselves for {len(SPECS)} paddles.</p><span class="go">See the specs &rarr;</span></a>
  </div>
</section>
{home_videos}{home_ig}<section>
  <div class="social-band"><div><h2>Watch the reviews</h2><p>Full video reviews on YouTube, and lab images and quick takes on Instagram.</p></div>
  <div class="btn-row"><a class="btn yellow" href="{YOUTUBE}" rel="noopener">YouTube @picklebrx</a><a class="btn ghost" style="color:#fff;border-color:#3a5182" href="{INSTAGRAM}" rel="noopener">Instagram @picklebrx</a></div></div>
</section>
</div>''', 0, "home"))

# ---------- database ----------
# paddles.html is built by catalog_page.py (every paddle by brand).

# ---------- compare ----------
write("compare.html", page("Compare paddles | PickleballRx", '''
<div class="wrap"><section>
  <h1 class="page-title">Compare paddles</h1>
  <p class="section-lead">Pick up to four paddles. The best value in each row is highlighted. Copy the page link to share your comparison.</p>
  <div class="compare-pickers" id="cmp-pickers"></div>
  <div class="table-wrap"><table class="cmp" id="cmp"></table></div>
</section></div>''', 0, "compare", desc="Compare pickleball paddles side by side."))

# ---------- finder ----------
# finder.html is built by rx_page.py (the Rx algorithm), run near the end of this file.

# ---------- best ----------
# Playing-style lists. No scores yet (Siva, 2026-11-17): spin follows measured RPM; the others wait for Siva's picks.
_NO_XRAY = {"Arronax Boost": ("Arronax", "Boost-1", None, "Arronax Boost", "Arronax Boost-1", "arronax-boost-1")}
def _spin_rows(n=10):
    inv = {sp: xs for xs, (g, sp) in LINKS.items() if sp}
    xr = {x["slug"]: x for x in XRAY}
    out = []
    for r in sorted(LABS["spin"] + LABS["spin_extra"], key=lambda r: -r["avg"]):
        if r.get("usap") is False:
            continue
        xs = inv.get(r["paddle"])
        x = xr.get(xs)
        if not x and r["paddle"] in _NO_XRAY:
            out.append(_NO_XRAY[r["paddle"]] + (r["condition"],))
            if len(out) == n:
                break
            continue
        brand = x["brand"] if x else r["paddle"].split()[0]
        model = x["name"][len(x["brand"]):].strip() if x and x["name"].startswith(x["brand"]) else (x["name"] if x else r["paddle"])
        g = LINKS.get(xs, (None, None))[0] if xs else None
        out.append((brand, model, xs, r["paddle"], g, None, r["condition"]))
        if len(out) == n:
            break
    return out
# Siva's lists (2026-11-17). Rows: (brand, model, X-ray slug, spin name, grit name, spec id, note)
_GBX_E = ("Gearbox", "Pressure X 8E", "gearbox-pressure-x-8e", "Gearbox Pressure XE", "Gearbox Pressure X 8E", "gearbox-8e", "")
_GBX_M = ("Gearbox", "Pressure X 8M", "gearbox-pressure-xm", "Gearbox Pressure X M", None, "gearbox-8m", "")
_JADE = ("RPM", "Jade", "rpm-jade", "RPM Jade", "RPM Jade", "rpm-jade", "")
_INF2 = ("Luzz", "Inferno 2", "luzz-inferno-2", "Luzz Inferno M2", "Luzz Inferno2", None, "")
_GLIDER = ("Luzz", "Glider 2026", "luzz-glider-2026", None, "Luzz Glider 2026", "luzz-glider", "")
_ORIGIN = ("Evolv", "Origin Elongated", "evolv-origin", "Evolv Origin", "Evolv", None, "")
_E2CF = ("Grit", "E2-CF", "grit-e2-cf", "Grit E2CF", None, None, "")
_SPITFIRE = ("Spartus", "Spitfire", "spartus-spitfire", "Spartus Spitfire", "Spartus Spitfire", None, "")
STYLE_PICKS = {
    "power": [
        ("MARK", "unMARKed 2026", "mark-unmarked-2026", "Mark Unmarked 2026", "MARK unMARKed 2026", None, ""),
        ("Pakle", "Fuse", "pakle-fuse", None, None, None, ""),
        _GBX_M,
        ("RPM", "Q2", "rpm-q2", None, None, None, ""),
        ("Selkirk", "LABS Project Boomstik", None, None, "Selkirk LABS Project Boomstik", None, "The original Boomstik, not the new Boomstik ST."),
        ("CPX", "Hyper+", "cpx-hyper-plus", None, "CPX Hyper+", "cpx-hyper", "Currently delisted by USA Pickleball (Nov 2026)."),
        _SPITFIRE,
    ],
    "spin": [
        ("Holbrook", "Fuze (VantaGrit)", "holbrook-fuze", "Holbrook Fuze", "Holbrook Fuze VantaGrit", None, ""),
        ("Gearbox", "Pressure X 8M or 8E", "gearbox-pressure-x-8e", "Gearbox Pressure XE", "Gearbox Pressure X 8E", "gearbox-8e", "Either one. Badges show the 8E; see the 8M in the Spin Lab."),
        ("Luzz", "Cannon XPP", "luzz-cannon-xpp", "Luzz Cannon XPP", "Luzz Cannon XPP M1", "luzz-cannon", ""),
        _E2CF, _JADE, _SPITFIRE,
    ],
    "control": [
        ("Sypik", "Triton 5", "sypik-triton-5", None, "Sypik Triton 5", "sypik-triton", ""),
        ("Mehau", "S5", "mehau-s5", None, "Mehau S5", None, ""),
        _GLIDER, _INF2, _JADE,
    ],
    "all-court": [_GBX_E, _INF2, _JADE, _ORIGIN, _E2CF],
    "beginner": [_ORIGIN, _GLIDER, ("VANWIN", "Alpha Control", "vanwin-alpha-control", None, "VANWIN Alpha Control", None, "")],
}
sections = []
for key, label, desc in STYLES:
    if key == "spin" and not STYLE_PICKS.get(key):
        rows = _spin_rows()
        sections.append(f'<section id="spin"><h2>Spin paddles</h2><p class="section-lead">No scores yet. This list follows our measured <a href="spin.html">Spin Lab</a> results, highest average RPM first, USA Pickleball approved paddles only. Condition is shown under each paddle, since used paddles were tested as they were.</p><div class="lb-grid">{"".join(lb_card(i, r, star=False) for i, r in enumerate(rows))}</div></section>')
    elif STYLE_PICKS.get(key):
        sections.append(f'<section id="{key}"><h2>{label} paddles</h2><p class="section-lead">{desc}. Picked by the Pickleball RX team, no scores yet.{" More to come." if key == "beginner" else ""}</p><div class="lb-grid">{"".join(lb_card(i, r, star=False) for i, r in enumerate(STYLE_PICKS[key]))}</div></section>')
_soon = [(k, l) for k, l, _ in STYLES if k != "spin" and not STYLE_PICKS.get(k)]
if _soon:
    _names = [l.lower() for _, l in _soon]
    sections.append('<section style="padding-top:0"><h2>More lists coming soon</h2>'
                    + "".join(f'<span id="{k}"></span>' for k, _ in _soon)
                    + '<p class="section-lead">' + (", ".join(_names[:-1]) + " and " + _names[-1] if len(_names) > 1 else _names[0]).capitalize() + ' paddle lists are on the way. Until then, see <a href="#epp">our top picks</a> and the <a href="lab.html">X-ray</a> and <a href="specs.html">Spec Lab</a> data.</p></section>')

# ---------- Our top picks (chosen by Siva, 2026-11-17) ----------
# Same row format as LEADERBOARD: (brand, model, X-ray slug, spin table name, grit name, spec id, note)
TOP_PICKS = [
    ("epp", "EPP foam", "Paddles with an EPP foam core.", [
        ("Gearbox", "Pressure X 8E", "gearbox-pressure-x-8e", "Gearbox Pressure XE", "Gearbox Pressure X 8E", "gearbox-8e", ""),
        ("Grit", "E2-CF", "grit-e2-cf", "Grit E2CF", None, None, ""),
        ("Evolv", "Origin Elongated", "evolv-origin", "Evolv Origin", "Evolv", None, ""),
        ("Honolulu", "J6CR", "honolulu-j6cr", "Honolulu J6CR", "Honolulu J6CR", None, ""),
        ("Spartus", "Spitfire", "spartus-spitfire", "Spartus Spitfire", "Spartus Spitfire", None, ""),
        ("Facolos", "Elite X V2.0", "facolos-elite-x-2-0", None, None, None, ""),
    ]),
    ("mpp", "MPP foam", "Paddles with an MPP foam core.", [
        ("Gearbox", "Pressure X 8M", "gearbox-pressure-xm", "Gearbox Pressure X M", None, "gearbox-8m", ""),
        ("Speedup", "Tide 14 Hybrid", "speedup-tide", "Speed Up Tide", "Speed Up Tide", None, "X-ray is of the Tide Elongated"),
        ("RPM", "Jade", "rpm-jade", "RPM Jade", "RPM Jade", "rpm-jade", ""),
        ("Luzz", "Inferno 2", "luzz-inferno-2", "Luzz Inferno M2", "Luzz Inferno2", None, ""),
        ("E6", "Ignis", "e6-ignis", None, "E6 Ignis", None, ""),
        ("Kamito", "Alpha X", "kamito-alpha-x", None, None, None, ""),
    ]),
    ("gen3", "Gen 3", "Honeycomb core with a foam perimeter.", [
        ("Sypik", "Triton 5", "sypik-triton-5", None, "Sypik Triton 5", "sypik-triton", ""),
        ("PACT", "Teflon Evolve TE16", "pact-teflon", None, "PACT Teflon Evolve", None, ""),
        ("Proton", "Project Coyote", "proton-project-coyote", None, "Proton Project Coyote", "proton-coyote", ""),
        ("RPM", "V2", "rpm-v2", None, None, None, ""),
        ("Mehau", "S5", "mehau-s5", None, "Mehau S5", None, ""),
        ("Zocker", "Aspire", "zocker-aspire", None, None, None, ""),
    ]),
    ("foreign", "Foreign picks", "Five more favorites from the team.", [
        ("Zcebra", "Gazelle", "zcebra-gazelle", "Zcebra Gazelle", "Zcebra Gazelle", None, ""),
        ("PACT", "Teflon Evolve TE16", "pact-teflon", None, "PACT Teflon Evolve", None, ""),
        ("Standout", "CF4 Absolute Black", "standout-cf4", None, None, None, ""),
        ("Kamito", "Alpha X", "kamito-alpha-x", None, None, None, ""),
        ("Sypik", "Triton 5", "sypik-triton-5", None, "Sypik Triton 5", "sypik-triton", ""),
    ]),
]
# Supasenpai's picks, as relayed by Siva (2026-11-17). Names checked against retailer listings.
SENPAI_PICKS = [
    ("Diadem", "Edge BluCore Pro 14", "", None),
    ("Crush", "Pro Force 5G", "", None),
    ("Sypik", "Avatar Pro", "We've X-rayed this one.", ("Avatar Pro X-ray", "xray/sypik-avatar-pro.html")),
    ("Luzz", "Inferno (original)", "We've X-rayed this one.", ("Inferno X-ray", "xray/luzz-inferno.html")),
    ("GRUVN", "MUVN-16HD", "", None),
]
def _ext_card(i, b, m, n, l):
    ph = product_photo(_slug(b + " " + m)) or (product_photo(l[1][5:-5]) if l and l[1].startswith("xray/") else "")
    img = f'<img class="lb-thumb" src="{ph}" alt="{e(b)} {e(m)}" loading="lazy" style="object-fit:contain">' if ph else ""
    return (f'<div class="lb-item"{"" if ph else " style=\'grid-template-columns:auto 1fr\'"}><div class="lb-rank">{i}</div>{img}<div style="min-width:0">'
            f'<div class="muted" style="font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700">{e(b)}</div>'
            f'<div style="font-weight:800;font-size:1.05rem;line-height:1.25">{e(m or b)}</div>'
            + (f'<div class="muted" style="font-size:.82rem;margin-top:4px">{e(n)}</div>' if n else "")
            + (f'<div class="badges" style="margin-top:6px"><a class="badge" href="{l[1]}">{e(l[0])}</a></div>' if l else "")
            + '</div></div>')
senpai_html = "".join(_ext_card(i, *r) for i, r in enumerate(SENPAI_PICKS, 1))

# Supasenpai's top 5 Canadian paddles, relayed by Siva (2026-11-17). Names checked against brand and Canadian retailer listings.
CANADIAN_PICKS = [
    ("GRUVN", "MUVN-16HD", "", None),
    ("Combat", "Titan Foam Pro", "", None),
    ("Apollo", "MK47 Signature Pro", "", None),
    ("NXTGEN", "Hydra", "Comes in standard and elongated shapes. The elongated Hydra E is pictured.", None),
    ("BOOMA", "Aerofoam", "", ("BOOMA store", "https://boomastore.com/en/products/aerofoam-pickleball-paddle")),
]
canadian_html = "".join(_ext_card(i, *r) for i, r in enumerate(CANADIAN_PICKS, 1))

picks_html = "".join(
    f'<section id="{k}" style="padding-top:10px"><h2>{e(t)}</h2><p class="section-lead">{e(d)}</p><div class="lb-grid">{"".join(lb_card(i, r, star=False) for i, r in enumerate(rows))}</div></section>'
    for k, t, d, rows in TOP_PICKS)

write("best.html", page("Best pickleball paddles | PickleballRx", f'''
<div class="wrap">
<section style="padding-bottom:0">
  <h1 class="page-title">Our top picks</h1>
  <p class="section-lead">Our favorite paddles by core type, picked by the Pickleball RX team after X-rays, microscope scans, spin tests and a lot of games. Tap any badge to see the lab results behind a pick.</p>
  <div class="chips">{"".join(f'<a href="#{k}">{e(t)}</a>' for k, t, _, _ in TOP_PICKS)}<a href="#canadian">Canadian picks</a><a href="#supa-senpai">Supasenpai's picks</a></div>
</section>
{picks_html}
<section id="canadian" style="padding-top:10px">
  <div class="rev-head" style="margin-bottom:6px"><img class="rev-avatar" src="assets/reviewers/supasenpai.jpg" alt="Supasenpai" width="64" height="64" loading="lazy"><h2 style="margin:0">Top 5 Canadian paddles</h2></div>
  <p class="section-lead">We did not test these paddles. These picks come from our Canadian neighbor, reviewer <a href="https://supasenpai.com/" target="_blank" rel="noopener">Supasenpai</a>, one of <a href="index.html#reviewers">our favorite reviewers</a>.</p>
  {senpai_links_html}
  <div class="lb-grid">{canadian_html}</div>
</section>
<section id="supa-senpai" style="padding-top:10px">
  <div class="rev-head" style="margin-bottom:6px"><img class="rev-avatar" src="assets/reviewers/supasenpai.jpg" alt="Supasenpai" width="64" height="64" loading="lazy"><h2 style="margin:0">Supasenpai's top picks</h2></div>
  <p class="section-lead">Paddle picks from Supasenpai, one of <a href="index.html#reviewers">our favorite reviewers</a>. These are Supasenpai's choices, not ours, and we haven't lab-tested them yet.</p>
  {senpai_links_html}
  <div class="lb-grid">{senpai_html}</div>
</section>
<section style="padding-bottom:0"><h2>By playing style</h2>
  <p class="section-lead">Our picks for each playing style. Paddles only for now, with no scores. Tap any badge to see the lab results behind a pick.</p>
  <div class="chips">{"".join(f'<a href="#{k}">{l}</a>' for k, l, _ in STYLES)}</div>
</section>
{"".join(sections)}
</div>''', 0, "best"))

# ---------- reviews index ----------
write("reviews/index.html", page("All reviews | PickleballRx", f'''
<div class="wrap"><section>
  <h1 class="page-title">All paddle reviews</h1>
  <p class="section-lead">Prefer a table? Use the <a href="../paddles.html">paddle database</a>.</p>
  <div class="grid">{"".join(card(p, 1) for p in PADDLES)}</div>
</section></div>''', 1, "paddles"))

# ---------- review pages ----------
for p in PADDLES:
    ov = overall(p)
    bars = "".join(f'<div class="score"><span>{k}</span><div class="bar"><i style="width:{p[k.lower()]*10}%"></i></div><b>{p[k.lower()]}</b></div>' for k in ["Power", "Spin", "Control", "Forgiveness"])
    vid = p.get("video") or next((v["id"] for v in VIDEOS if v.get("paddle") == p["slug"]), "")
    deal = f'<div class="deal">Discount code<code>{e(p["discount"])}</code></div>' if p.get("discount") else ""
    others = [o for o in PADDLES if o["slug"] != p["slug"]]
    rivals = sorted(others, key=lambda o: abs(o["power"] - p["power"]) + abs(o["control"] - p["control"]) + abs(o["spin"] - p["spin"]))[:2]
    cmp_link = "../compare.html?p=" + ",".join([p["slug"]] + [o["slug"] for o in rivals])
    ph_note = '<div class="note"><strong>Placeholder.</strong> This paddle, its specs and scores are made up to show the review layout. They are not real test results.</div>' if p.get("placeholder") else ""
    write(f"reviews/{p['slug']}.html", page(f"{p['name']} review | PickleballRx", f'''
<div class="review-hero"><div class="wrap">
  <div>
    <div class="crumbs"><a href="../paddles.html">Paddles</a> / {e(p["brand"])}</div>
    <h1>{e(p["name"])} review</h1>
    <p class="muted" style="margin:0 0 14px">{e(p["quick"])}</p>
    {badges(p)}
    <div class="btn-row" style="margin-top:16px"><a class="btn" href="#video">Watch the review</a><a class="btn ghost" href="{cmp_link}">Compare with similar</a></div>
  </div>
  <div class="scorecard">
    <div class="overall"><b>{ov}</b><span>/ 10 overall</span></div>
    {bars}
  </div>
</div></div>
<div class="wrap review-body">
  <article>
    {ph_note}
    <h2 id="verdict">Verdict</h2>
    <p>{e(p["verdict"])}</p>
    <div class="proscons">
      <div><h3>What we liked</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in p["pros"])}</ul></div>
      <div><h3>What could be better</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in p["cons"])}</ul></div>
    </div>
    <h2 id="video">Video review</h2>
    {embed(vid, p["name"] + " review") if vid else video_ph("YouTube review will go here")}
    <h2 id="inside">Inside the paddle</h2>
    <p class="muted">What the X-ray and microscope show about how this paddle is built.</p>
    <div class="lab-grid">
      {lab_fig(("../" + p["xray"]) if p.get("xray") else "", p["name"] + " X-ray", "<strong>X-ray</strong> &middot; core, edge and weighting", "X-ray")}
      {lab_fig(("../" + p["micro"]) if p.get("micro") else "", p["name"] + " face under microscope", "<strong>Microscope</strong> &middot; face grit and texture", "Microscope scan")}
    </div>
    <h2 id="specs">Measured specs</h2>
    <table class="specs">
      <tr><th>Weight</th><td>{p["weight_oz"]} oz</td></tr>
      <tr><th>Swing weight</th><td>{p["swing_weight"]}</td></tr>
      <tr><th>Twist weight</th><td>{p["twist_weight"]}</td></tr>
      <tr><th>Core thickness</th><td>{p["core_mm"]} mm</td></tr>
      <tr><th>Face</th><td>{e(p["face"])}</td></tr>
      <tr><th>Shape</th><td>{e(p["shape"])}</td></tr>
      <tr><th>Length x width</th><td>{p["length_in"]} x {p["width_in"]} in</td></tr>
      <tr><th>Grip length</th><td>{p["grip_in"]} in</td></tr>
      <tr><th>Price</th><td>${p["price"]}</td></tr>
    </table>
    <h2 id="similar">Similar paddles</h2>
    <div class="grid">{"".join(card(o, 1) for o in rivals)}</div>
  </article>
  <aside class="toc">
    <strong>On this page</strong>
    <ol><li><a href="#verdict">Verdict</a></li><li><a href="#video">Video review</a></li><li><a href="#inside">Inside the paddle</a></li><li><a href="#specs">Measured specs</a></li><li><a href="#similar">Similar paddles</a></li></ol>
    {deal}
    <p style="margin:14px 0 0"><a class="btn yellow" style="display:block;text-align:center" href="#" aria-disabled="true" onclick="return false">Check price (link coming soon)</a></p>
  </aside>
</div>''', 1, "paddles", desc=f"{p['name']} pickleball paddle review with scores and specs."))

# ---------- videos ----------
# Videos come from the YouTube feed automatically; VIDEOS (top of file) can add extra ones by hand.
_seen = {v["id"] for v in YT_FEED}
_all_v = YT_FEED + [dict(id=v["id"], title=v["title"]) for v in VIDEOS if v["id"] not in _seen]
_reg = [v for v in _all_v if not v.get("short")]
_shorts = [v for v in _all_v if v.get("short")]
if _all_v:
    vbody = (f'<div class="grid">{"".join(yt_card(v) for v in _reg)}</div>' if _reg else "") + \
        (f'<h2 style="margin-top:34px">Shorts</h2><div class="grid shorts">{"".join(yt_card(v) for v in _shorts)}</div>' if _shorts else "") + \
        f'<p style="margin-top:22px">These are our newest {len(_all_v)} videos. <a href="{YOUTUBE}/videos" rel="noopener">See every video on YouTube &rarr;</a></p>'
else:
    vbody = f'<div class="note">Our latest YouTube videos will show here. <a href="{YOUTUBE}" rel="noopener">Watch them on YouTube @picklebrx</a> for now.</div>'
igbody = ig_grid(IG_FEED[:12]) if IG_FEED else \
    f'<div class="note">Lab images, X-rays and quick takes. <a href="{INSTAGRAM}" rel="noopener">See them on Instagram @picklebrx</a>.</div>'
write("videos.html", page("Videos | PickleballRx", f'''
<div class="wrap"><section>
  <h1 class="page-title">Videos</h1>
  <p class="section-lead">Paddle reviews, lab tests and on-court play. New videos show up here on their own a few hours after we post them.</p>
  <div class="btn-row" style="margin-bottom:24px"><a class="btn" href="{YOUTUBE}?sub_confirmation=1" rel="noopener">Subscribe on YouTube</a><a class="btn ghost" href="{INSTAGRAM}" rel="noopener">Follow @picklebrx</a></div>
  {vbody}
</section>
<section id="instagram" style="padding-top:0">
  <div class="section-head"><div><h2>Instagram</h2><p class="section-lead">Our latest posts from <a href="{INSTAGRAM}" rel="noopener">@picklebrx</a>.</p></div></div>
  {igbody}
</section></div>''', 0, "videos", desc="PickleballRx YouTube paddle reviews and Instagram posts."))

# ---------- lab cross-links ----------


def slugify(t):
    import re
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


SPEC_LINKS = {  # spec card id -> (X-ray slug, spin table name, grit collection name)
    "rpm-jade": ("rpm-jade", "RPM Jade", "RPM Jade"),
    "luzz-cannon": ("luzz-cannon-xpp", "Luzz Cannon XPP", "Luzz Cannon XPP M1"),
    "sypik-triton": ("sypik-triton-5", None, "Sypik Triton 5"),
    "cpx-hyper": ("cpx-hyper-plus", None, "CPX Hyper+"),
    "luzz-glider": ("luzz-glider-2026", None, "Luzz Glider 2026"),
    "proton-coyote": ("proton-project-coyote", None, "Proton Project Coyote"),
    "gearbox-8m": ("gearbox-pressure-xm", "Gearbox Pressure X M", None),
    "gearbox-8e": ("gearbox-pressure-x-8e", "Gearbox Pressure XE", "Gearbox Pressure X 8E"),
    "pop-n-rush": ("pickle-poppers-pop-n-rush", "Pop N Rush", "Pickle Poppers Pop N Rush"),
    "bnb-loco": (None, "Bread & Butter Loco 2 Elongated", "Bread & Butter LOCO 2"),
    "arronax-boost-1": (None, "Arronax Boost", "Arronax Boost-1"),
}


def lab_links(x):
    g, sp = LINKS.get(x["slug"], (None, None))
    out = []
    sc = next((c for c in SPECS if SPEC_LINKS.get(c["id"], (None,))[0] == x["slug"]), None)
    if sc:
        m = sc["measured"]
        out.append(f'<tr><th>Measured (Spec Lab)</th><td><a href="../specs.html#{sc["id"]}">Swing weight {m["swingWeight"]}, twist weight {m["twistWeight"]:.2f}, {m["staticWeightOz"]:.2f} oz</a></td></tr>')
    if g:
        gi = next((i for i in LABS["grit"] if i["name"] == g), None)
        if gi: out.append(f'<tr><th>Face surface (Grit Lab)</th><td><a href="../grit.html#{slugify(g)}">{e(gi["surface"])}</a></td></tr>')
    if sp:
        si = next((i for i in LABS["spin"] + LABS["spin_extra"] if i["paddle"] == sp), None)
        if si: out.append(f'<tr><th>Spin (Spin Lab)</th><td><a href="../spin.html#{slugify(sp)}">{si["avg"]:,} RPM average, {si["top"]:,} highest</a> <span class="muted">({e(si["condition"])})</span></td></tr>')
    return "".join(out)


# ---------- X-Ray Rx (lab) ----------
XRAY_DISCLAIMER = "Labels are our read of the X-ray, not a cutaway. Measurements are approximate."
VIEWS = [("clean", "Clean"), ("labeled", "Labeled"), ("density", "Density estimate")]


def xray_img(slug, view):
    for ext in ("jpg", "jpeg", "png", "webp"):
        rel = f"assets/xray/{slug}-{view}.{ext}"
        if os.path.exists(os.path.join(OUT, rel)):
            return rel
    return ""


def xray_card(x, depth):
    r = "../" * depth
    img = xray_img(x["slug"], "labeled") or xray_img(x["slug"], "clean")
    thumb = f'<img src="{r}{img}" alt="{e(x["name"])} X-ray" loading="lazy" style="aspect-ratio:4/3;object-fit:cover;border-radius:10px">' if img else '<div class="lab-ph" style="border-radius:10px">X-ray image coming soon</div>'
    tags = "".join(f'<span class="badge">{e(t)}</span>' for t in x["tags"])
    if x["unreleased"]: tags += '<span class="tag">Unreleased</span>'
    if x["reel"]: tags += '<span class="badge">Reel</span>'
    summary = e(x["core"]) if x["core"] else '<span class="muted">Findings coming soon</span>'
    return f'''<article class="card xcard" data-tags="{" ".join(x["tags"])}" data-name="{e(x["name"].lower())} {e(x["brand"].lower())}">
  <a href="{r}xray/{x["slug"]}.html">{thumb}</a>
  <div class="badges">{tags}</div>
  <h3><a href="{r}xray/{x["slug"]}.html">{e(x["name"])}</a></h3>
  <p style="font-size:.93rem">{summary}</p>
  <a class="more" href="{r}xray/{x["slug"]}.html">See inside &rarr;</a>
</article>'''


reels = [x for x in XRAY if x["reel"]]
reel_items = "".join(f'<li><a href="xray/{x["slug"]}.html"><strong>{e(x["reel"].split(":")[0])}</strong></a>{(": " + e(x["reel"].split(":",1)[1].strip())) if ":" in x["reel"] else ""}</li>' for x in sorted(reels, key=lambda x: x["reel"]))
write("lab.html", page("X-Ray Rx: pickleball paddle X-rays | PickleballRx", f'''
<section class="hero" style="padding:44px 0"><div class="wrap" style="grid-template-columns:1fr">
  <div>
    <span class="tag">X-Ray Rx</span>
    <h1>What's <em>inside</em> {len(XRAY)} pickleball paddles.</h1>
    <p>We X-ray each paddle and label what's inside: core, perimeter ring, inserts and handle, alongside the published specs and where they came from.</p>
    <p style="font-size:.95rem;margin:0">{XRAY_DISCLAIMER} <a href="disclaimers.html#xray">Disclaimers</a>.</p>
  </div>
</div></section>
<div class="wrap">
<section>
  <div class="tools">
    <div class="tool"><div class="ico">8</div><h3>Honeycomb cells are about 7 to 8.5 mm</h3><p>Nearly every honeycomb core we've measured falls in that range. The Vanwin Alpha Control and the 11SIX24 Hurache-X Alpha Pro Power, both at about 10 mm, are the only large-cell paddles so far.</p></div>
    <div class="tool"><div class="ico">F</div><h3>Foam has taken over</h3><p>{sum(1 for x in XRAY if "foam" in x["tags"])} of {len(XRAY)} paddles have no honeycomb in the face: full foam cores (EPP, MPP, EVA or dual-density), usually inside a denser perimeter ring.</p></div>
    <div class="tool"><div class="ico">R</div><h3>Rings range from about 7 to 28 mm</h3><p>Perimeter rings vary a lot, from about 7 to 8 mm (Jelly Bean 2, Kamito Dominus) to 26 to 28 mm (Facolos Elite X 2.0, Luzz Inferno 2).</p></div>
  </div>
</section>
<section style="padding-top:0">
  <div class="section-head"><div><h2>All X-rayed paddles</h2><p class="section-lead">Filter by core type, or search for a paddle.</p></div></div>
  <div class="filters">
    <label>Search<input type="search" id="x-q" placeholder="Paddle or brand"></label>
  </div>
  <div class="chips" id="x-chips">
    <button aria-pressed="true" data-t="">All</button><button aria-pressed="false" data-t="honeycomb">Honeycomb</button><button aria-pressed="false" data-t="foam">Full foam</button><button aria-pressed="false" data-t="epp">EPP</button><button aria-pressed="false" data-t="mpp">MPP</button><button aria-pressed="false" data-t="floating">Floating core</button><button aria-pressed="false" data-t="voids">Voids</button>
  </div>
  <p class="count" id="x-count"></p>
  <div class="grid" id="x-grid">{"".join(xray_card(x, 0) for x in XRAY)}</div>
</section>
<section>
  <div class="social-band"><div><h2>The X-Ray Rx reel series</h2><p>Short vertical episodes on Instagram, one paddle at a time.</p>
  <ul style="color:#c9d3ea;margin:12px 0 0;padding-left:18px">{reel_items.replace('<a ', '<a style="color:#fcb92d" ')}</ul></div>
  <div class="btn-row"><a class="btn yellow" href="{INSTAGRAM}" rel="noopener">Watch on Instagram</a></div></div>
</section>

</div>''', 0, "lab", desc=f"X-rays of {len(XRAY)} pickleball paddles, labeled: core, ring, inserts and handle."))

for x in XRAY:
    lab_img = xray_img(x["slug"], "labeled")
    main_fig = (f'<figure class="lab-item" style="margin-top:12px"><a href="../{lab_img}"><img src="../{lab_img}" alt="{e(x["name"])} labeled X-ray with spec panel" style="aspect-ratio:auto;object-fit:contain;background:#fff"></a><figcaption><strong>Labeled X-ray</strong> &middot; tap to open full size</figcaption></figure>'
                if lab_img else '<div class="lab-ph" style="border-radius:14px;margin-top:12px">Labeled X-ray coming soon</div>')
    extra = "".join(lab_fig(("../" + xray_img(x["slug"], v)) if xray_img(x["slug"], v) else "", f'{x["name"]} X-ray, {l.lower()}', f"<strong>{l}</strong>", l + " X-ray") for v, l in VIEWS if v != "labeled")
    head_rows = [("Core", x["core"]), ("Cells", x["cell_size"]), ("Perimeter", x["ring"]), ("Thickness", x["thickness"])]
    spec_rows = "".join(f'<tr><th>{e(k)}</th><td>{e(v) if v else "<span class=muted>Not listed</span>"}</td></tr>' for k, v in x["specs"])
    review = next((p for p in PADDLES if p["name"].lower() == x["name"].lower()), None)
    same_brand = [o for o in XRAY if o["brand"] == x["brand"] and o["slug"] != x["slug"]]
    unrel = '<div class="note"><strong>Unreleased paddle.</strong> No maker specs are published yet, so some values are inferred from the X-ray.</div>' if x["unreleased"] else ""
    ll = lab_links(x)
    write(f"xray/{x['slug']}.html", page(f"{x['name']} X-ray: what's inside | PickleballRx", f'''
<div class="review-hero"><div class="wrap">
  <div>
    {f'<img class="product-shot" src="../{product_photo(x["slug"])}" alt="{e(x["name"])}" width="120" height="180">' if product_photo(x["slug"]) else ""}
    <div class="crumbs"><a href="../lab.html">X-Ray Rx</a> / {e(x["brand"])}</div>
    <h1>{e(x["name"])} X-ray</h1>
    <p class="muted" style="margin:0 0 14px">{e(x["core"])}. {e(x["ring"])}.</p>
    <div class="badges">{"".join(f'<span class="badge">{e(t)}</span>' for t in x["tags"])}{'<span class="tag">Unreleased</span>' if x["unreleased"] else ""}</div>
    <div class="btn-row" style="margin-top:16px"><a class="btn" href="#xray">See the X-ray</a>{f'<a class="btn ghost" href="../reviews/{review["slug"]}.html">Read the full review</a>' if review else ""}</div>
  </div>
  <div class="scorecard">
    <div style="font-weight:800;color:#fcb92d;margin-bottom:6px">What's inside</div>
    <table style="width:100%;border-collapse:collapse;font-size:.93rem">{"".join(f'<tr><td style="padding:6px 0;color:#c9d3ea;width:34%;vertical-align:top">{k}</td><td style="padding:6px 0">{e(v) if v else "&ndash;"}</td></tr>' for k, v in head_rows)}</table>
  </div>
</div></div>
<div class="wrap" style="padding-top:30px;padding-bottom:20px">
  {unrel}
  {code_box(x["brand"], 1)}
  {('<h2>Colorways</h2><div class="colorways">' + "".join(f'<figure><img src="../assets/paddles/product/{x["slug"]}{"-" + c if c else ""}.jpg" alt="{e(x["name"])}, {e(lbl)}" width="200" height="300" loading="lazy"><figcaption>{e(lbl)}</figcaption></figure>' for c, lbl in COLORWAYS[x["slug"]]) + '</div>') if x["slug"] in COLORWAYS else ""}
  <h2 id="xray">The X-ray</h2>
  <p class="muted" style="margin:0">{XRAY_DISCLAIMER} <a href="../disclaimers.html#xray">Disclaimers</a>.</p>
  {main_fig}
  <h3 style="margin-top:26px">More views</h3>
  <div class="lab-grid">{extra}</div>
  <h2 style="margin-top:34px">Specs</h2>
  <table class="specs">{spec_rows}</table>
  <p class="muted" style="font-size:.85rem;margin-top:8px">{e(x["sources"])}. Ring widths are measured from the X-ray, so they are estimates (&asymp;).</p>
  {('<h2 style="margin-top:34px">From our other labs</h2><table class="specs">' + ll + '</table>') if ll else ""}
  {f'<h2 style="margin-top:34px">Watch the reel</h2><p>{e(x["reel"].rstrip("."))}{"" if x["reel"].endswith("?") else "."} <a href="{INSTAGRAM}" rel="noopener">See it on Instagram @picklebrx</a>.</p>' if x["reel"] else ""}
  {f'<h2 style="margin-top:34px">More from {e(x["brand"])}</h2><div class="grid">' + "".join(xray_card(o, 1) for o in same_brand) + '</div>' if same_brand else ""}
  <p style="margin-top:30px"><a href="../lab.html">&larr; All X-rayed paddles</a></p>
</div>''', 1, "lab", desc=f"Labeled X-ray of the {x['name']} pickleball paddle: core, ring, cells and specs."))


# ---------- Grit Lab ----------
GRIT_DISCLAIMER = "Microscope images were taken on an Elikliv 4K digital microscope. Wear percentages are conservative visual estimates comparing each paddle's hitting zone with its own low-contact throat under matched zoom and lighting. They are not profilometer measurements, and results vary with play style, ball and court surface. Surface names are as published by each brand."


def grit_img(name):
    for ext in ("jpg", "jpeg", "png", "webp"):
        rel = f"assets/grit/{slugify(name)}.{ext}"
        if os.path.exists(os.path.join(OUT, rel)):
            return rel
    return ""


NOT_USAP = '<span class="tag" style="background:#fde2e2;color:#8a1c1c">Not USAP approved</span>'
grit_cards = "".join(
    f'<figure class="lab-item" id="{slugify(g["name"])}">' +
    (f'<a href="{grit_img(g["name"])}"><img src="{grit_img(g["name"])}" alt="{e(g["name"])} face under the microscope, M lens" loading="lazy"></a>' if grit_img(g["name"]) else '<div class="lab-ph">Microscope image coming soon</div>') +
    f'<figcaption>' + (f'<img class="product-thumb" src="{product_photo(NAME_PHOTO[g["name"]])}" alt="{e(g["name"])}" width="40" height="60" loading="lazy">' if product_photo(NAME_PHOTO.get(g["name"], "")) else "") +
    f'<span class="muted" style="font-size:.78rem">#{i + 1}</span> <strong style="color:var(--ink)">{e(g["name"])}</strong><br>{e(g["surface"])}' +
    (f' {NOT_USAP}' if g["name"].startswith("Grit E1") else "") + '</figcaption></figure>'
    for i, g in enumerate(LABS["grit"]))
wear_rows = "".join(f'<tr><td><strong>{e(w["paddle"])}</strong></td><td>{e(w["use"])}</td><td><strong>{e(w["result"])}</strong>{("<br><span class=muted>" + e(w["notes"]) + "</span>") if w["notes"] else ""}</td></tr>' for w in LABS["wear"])
cmp_cards = "".join(f'<div class="tool"><h3>{e(c["title"])}</h3><p>{e(c["text"])}</p></div>' for c in LABS["compare"])
note_cards = "".join(f'<div class="tool"><h3>{e(n["paddle"])}</h3><p>{e(n["text"])}</p></div>' for n in LABS["grit_notes"])


def card_fig(name, caption, alt):
    src = f"assets/grit/cards/{name}"
    if not os.path.exists(os.path.join(OUT, src)):
        return ""
    return f'<figure class="lab-item"><a href="{src}"><img src="{src}" alt="{e(alt)}" loading="lazy" style="aspect-ratio:auto;object-fit:contain;background:#fff"></a><figcaption>{caption}</figcaption></figure>'


def gallery(items, min_w=300):
    figs = "".join(card_fig(*i) for i in items)
    return f'<div class="lab-grid" style="grid-template-columns:repeat(auto-fill,minmax({min_w}px,1fr));margin-top:18px;align-items:start">{figs}</div>' if figs else ""


collection_fig = card_fig("all-39-grit.jpg", f"<strong>All {len(LABS['grit'])} paddles</strong> &middot; same 4K microscope, M lens &middot; tap to open full size", f"Grid of {len(LABS['grit'])} paddle faces under the microscope")
new_gallery = gallery([
    ("card-arronax-boost-1.jpg", "<strong>Arronax Boost-1</strong> &middot; GritBite surface, M lens", "Arronax Boost-1 GritBite surface under the microscope"),
    ("card-volair-cmd.jpg", "<strong>Volair CMD</strong> &middot; HexGrit (licensed from 11SIX24)", "Volair CMD HexGrit surface under the microscope"),
    ("card-arronax-kvl-005.jpg", "<strong>Arronax KVL 005</strong> &middot; T800 carbon, peel-ply texture", "Arronax KVL 005 peel-ply surface under the microscope"),
    ("card-rpm-friction-pro-v2.jpg", "<strong>RPM Friction Pro V2</strong> &middot; CarbonBite surface, M lens", "RPM Friction Pro V2 CarbonBite surface under the microscope"),
    ("card-rpm-friction-pro-v2-lm.jpg", "<strong>RPM Friction Pro V2</strong> &middot; CarbonBite surface, L and M lenses", "RPM Friction Pro V2 at the L and M lenses"),
    ("card-li-ning-90s.jpg", "<strong>Li-Ning HyperPower 90S (14mm)</strong> &middot; micro-sanding finish", "Li-Ning HyperPower 90S surface under the microscope"),
    ("card-loco2-l.jpg", "<strong>Bread &amp; Butter LOCO 2</strong> &middot; Space Dust Grit, L lens", "Bread and Butter LOCO 2 at the L lens"),
    ("card-loco2-m.jpg", "<strong>Bread &amp; Butter LOCO 2</strong> &middot; Space Dust Grit, M lens", "Bread and Butter LOCO 2 at the M lens"),
], 260)
ig_gallery = gallery([
    ("ig-arronax-l-1.jpg", "Arronax Boost-1 &middot; L lens", "Arronax Boost-1 face, L lens"),
    ("ig-arronax-l-2.jpg", "Arronax Boost-1 &middot; L lens", "Arronax Boost-1 face, L lens"),
    ("ig-arronax-l-close-1.jpg", "Arronax Boost-1 &middot; L lens, close", "Arronax Boost-1 face, L lens close-up"),
    ("ig-arronax-l-close-2.jpg", "Arronax Boost-1 &middot; L lens, close", "Arronax Boost-1 face, L lens close-up"),
    ("ig-arronax-m-1.jpg", "Arronax Boost-1 &middot; M lens", "Arronax Boost-1 face, M lens"),
], 180)
wear_gallery = gallery([
    ("wear-rpm-jade-throat-center.jpg", "<strong>RPM Jade (SICmatrix)</strong> &middot; throat vs center", "RPM Jade throat versus center wear"),
    ("wear-rpm-jade-scan.jpg", "<strong>RPM Jade (SICmatrix)</strong> &middot; L lens scan summary", "RPM Jade L lens scan summary"),
])
cmp_gallery = gallery([
    ("cmp-loco2-vs-hexgrit.jpg", "<strong>LOCO 2 (Space Dust) vs 11SIX24 HexGrit</strong> &middot; L and M lenses", "LOCO 2 versus HexGrit comparison"),
    ("cmp-volair-vs-hexgrit.jpg", "<strong>Volair CMD vs 11SIX24 HexGrit</strong> &middot; L and M lenses", "Volair CMD versus HexGrit comparison"),
    ("cmp-rpm-jade-vs-friction-pro-v2.jpg", "<strong>RPM Jade (SICmatrix) vs Friction Pro V2 (CarbonBite)</strong> &middot; L and M lenses", "RPM Jade versus RPM Friction Pro V2 comparison"),
    ("cmp-grit-e1-cw-vs-tw.jpg", f"<strong>Grit E1 CW vs E1 TW</strong> {NOT_USAP}", "Grit E1 CW versus E1 TW comparison"),
    ("card-grit-e1-cw.jpg", f'<img class="product-thumb" src="assets/paddles/product/grit-e1-cw.jpg" alt="Grit E1 CW" width="40" height="60" loading="lazy">' + f"<strong>Grit E1 CW</strong> &middot; L and M lenses {NOT_USAP}", "Grit E1 CW under the microscope"),
    ("card-grit-e1-tw.jpg", f'<img class="product-thumb" src="assets/paddles/product/grit-e1-tw.jpg" alt="Grit E1 TW" width="40" height="60" loading="lazy">' + f"<strong>Grit E1 TW</strong> &middot; L and M lenses {NOT_USAP}", "Grit E1 TW under the microscope"),
])
write("grit.html", page("Grit Lab: pickleball paddle grit under the microscope | PickleballRx", f"""
<section class="hero" style="padding:44px 0"><div class="wrap" style="grid-template-columns:1fr"><div>
  <span class="tag">Grit Lab</span>
  <h1>{len(LABS["grit"])} paddle faces under a <em>4K microscope</em>.</h1>
  <p>We photograph every paddle's surface up close, match it to the brand's own name for its grit, and track how it wears after real play.</p>
</div></div></section>
<div class="wrap">
<section>
  <h2>How we test</h2>
  <div class="tools">
    <div class="tool"><div class="ico">W</div><h3>Three lenses</h3><p>Elikliv 4K digital microscope. W: whole area. L: about 10 to 20 weave squares across. M: about 5 to 7 squares across, the standard lens for the collection.</p></div>
    <div class="tool"><div class="ico">ID</div><h3>Surface ID</h3><p>Every surface is photographed, then matched to the brand's own published name for its grit, so labels reflect what the brand calls it.</p></div>
    <div class="tool"><div class="ico">%</div><h3>Wear against the throat</h3><p>The throat barely touches the ball, so it shows what the grit looked like new. We compare hitting zones to it at the same zoom and light, and judge only sharp frames from a full-face video scan.</p></div>
  </div>
  <p class="section-lead" style="margin-top:20px"><strong>What we've noticed so far:</strong> larger, coarser grit tends to feel sticky, while finer grit tends to feel softer and plusher. Big raised crystals take every hit directly, so they dull and chip fastest. Fine grit set inside the coating wears by slow polishing instead.</p>
</section>
<section style="padding-top:0">
  <div class="section-head"><div><h2>The grit collection</h2><p class="section-lead">{len(LABS["grit"])} paddles under the M lens. Surface names are as published by each brand.</p></div></div>
  {('<div style="max-width:620px;margin:0 auto 26px">' + collection_fig + '</div>') if collection_fig else ""}
  <h3>Each paddle up close</h3>
  <div class="lab-grid">{grit_cards}</div>
</section>
<section>
  <h2>Newest additions</h2>
  <div class="tools">{note_cards}</div>
  {new_gallery}
  {('<h3 style="margin-top:26px">Arronax Boost-1, more angles</h3>' + ig_gallery) if ig_gallery else ""}
</section>
<section>
  <h2>Wear studies</h2>
  <p class="section-lead">Conservative visual estimates, about &plusmn;10 points. Each paddle is compared with its own throat under matched light.</p>
  <div class="table-wrap"><table class="cmp" style="min-width:680px"><thead><tr><th>Paddle</th><th>Use</th><th>Result</th></tr></thead><tbody>{wear_rows}</tbody></table></div>
  {wear_gallery}
</section>
<section>
  <h2>Head-to-head surface comparisons</h2>
  <div class="tools">{cmp_cards}</div>
  {cmp_gallery}
  <p id="grit-e1" class="muted" style="font-size:.9rem;margin-top:12px">Grit E1 CW and E1 TW are recreational-play paddles that are not USA Pickleball approved.</p>
</section>
<section style="padding-top:0"><div class="note">{GRIT_DISCLAIMER} <a href="disclaimers.html#grit">Disclaimers</a>.</div></section>
</div>""", 0, "grit", desc=f"{len(LABS['grit'])} pickleball paddle faces under a 4K microscope, plus grit wear studies."))

# ---------- Spin Lab ----------
spin_all = LABS["spin"]
smax = max(r["top"] for r in spin_all)
def spin_thumb(name):
    ph = product_photo(NAME_PHOTO.get(name, ""))
    return f'<img class="product-thumb" src="{ph}" alt="" width="28" height="42" loading="lazy">' if ph else ""
def spin_row(i, r):
    flags = ""
    if r.get("usap") is False: flags += ' <span class="tag" style="background:#fde2e2;color:#8a1c1c">Not USAP approved</span>'
    if r.get("as_shot"): flags += ' <span class="muted" title="Shown as shot at about 37 to 38 mph, not speed-adjusted">&dagger;</span>'
    return (f'<tr id="{slugify(r["paddle"])}"><td class="num muted">{i}</td><td>{spin_thumb(r["paddle"])}<strong>{e(r["paddle"])}</strong>{flags}<br><span class="muted" style="font-size:.82rem">{e(r["condition"])}</span></td>'
            f'<td style="min-width:220px"><div style="display:flex;align-items:center;gap:8px"><span style="flex:1;height:12px;background:var(--line);border-radius:6px;overflow:hidden;display:block"><i style="display:block;height:100%;width:{r["avg"] / smax * 100:.1f}%;background:{"#c9ccd6" if r.get("usap") is False else "var(--yellow)"}"></i></span><b class="num">{r["avg"]:,}</b></div></td>'
            f'<td class="num">{r["top"]:,}</td></tr>')
spin_rows = "".join(spin_row(i + 1, r) for i, r in enumerate(spin_all))
extra_rows = "".join(f'<tr id="{slugify(r["paddle"])}"><td><strong>{e(r["paddle"])}</strong></td><td>{e(r["condition"])}</td><td class="num">{r["avg"]:,}</td><td class="num">{r["top"]:,}</td><td class="muted">{e(r["note"])}</td></tr>' for r in LABS["spin_extra"])
dur_summary = "".join(f'<tr><td><strong>{e(d["paddle"])}</strong></td><td>{e(d["time"])}</td><td>{e(d["result"])}</td><td><strong style="color:{"var(--good)" if d["good"] else "#b45309"}">{e(d["verdict"])}</strong></td></tr>' for d in LABS["durability"])
def dur_block(d):
    t = ""
    if d["table"]:
        t = '<div class="table-wrap" style="margin:10px 0"><table class="cmp" style="min-width:520px"><thead><tr>' + "".join(f"<th>{e(c)}</th>" for c in d["table"][0]) + "</tr></thead><tbody>" + \
            "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in row) + "</tr>" for row in d["table"][1:]) + "</tbody></table></div>"
    ph = product_photo(NAME_PHOTO.get(d["paddle"], ""))
    img = f'<img class="product-shot" src="{ph}" alt="{e(d["paddle"])}" width="96" height="144" style="float:right;margin:0 0 10px 16px">' if ph else ""
    return f'<div class="card" id="dur-{slugify(d["paddle"])}" style="display:block">{img}<h3>{e(d["paddle"])} <span style="color:{"var(--good)" if d["good"] else "#b45309"};font-size:.9rem">&middot; {e(d["verdict"])}</span></h3>{t}<ul style="margin:0;padding-left:20px">' + "".join(f"<li>{e(n)}</li>" for n in d["notes"]) + "</ul></div>"
dur_blocks = "".join(dur_block(d) for d in LABS["durability"])
detail_rows = "".join(f'<tr><td><strong>{e(r["paddle"])}</strong></td><td>{e(r["condition"])}</td><td>{e(r["avg"])}</td><td>{e(r["top"])}</td><td>{e(r["rebound"])}</td><td>{e(r["date"])}</td></tr>' + (f'<tr><td colspan="6" class="muted" style="font-size:.88rem">{e(r["note"])}</td></tr>' if r["note"] else "") for r in LABS["spin_detail"])
write("spin.html", page("Spin Lab: pickleball paddle spin test results | PickleballRx", f"""
<section class="hero" style="padding:44px 0"><div class="wrap" style="grid-template-columns:1fr"><div>
  <span class="tag">Spin Lab</span>
  <h1>Same rig, same ball machine, <em>960 frames per second</em>.</h1>
  <p>We test a paddle, play it, then test it again. {len(spin_all) + len(LABS["spin_extra"])} paddles measured so far, and {len(LABS["durability"])} re-tested after weeks or months of play.</p>
</div></div></section>
<div class="wrap">
<section>
  <div class="section-head"><div><h2>Spin results, all paddles</h2><p class="section-lead">Spin average is the average of each paddle's best hits, scaled to a 37.5 mph incoming ball. Updated {LABS["updated"]}.</p></div></div>
  <div class="table-wrap"><table class="db" style="min-width:600px"><thead><tr><th>#</th><th>Paddle</th><th>Spin, average (RPM)</th><th>Highest hit</th></tr></thead><tbody>{spin_rows}</tbody></table></div>
  <ul class="muted" style="font-size:.9rem;margin-top:12px">
    <li>Grit E1 TW and E1 CW are recreational-play paddles that are <strong>not USA Pickleball approved</strong>. They're shown for reference only, and are the highest spin recorded on this rig.</li>
    <li>&dagger; Shown as shot at about 37 to 38 mph, not speed-adjusted.</li>
    <li>USAP-approved paddles on this rig land between roughly 1,750 and 2,200 RPM.</li>
    <li>A few other paddles are still in testing. Results will be published once we understand what is going on.</li>
  </ul>
  <h3 style="margin-top:24px">Also tested</h3>
  <div class="table-wrap"><table class="cmp" style="min-width:640px"><thead><tr><th>Paddle</th><th>Condition</th><th>Spin, average</th><th>Highest hit</th><th>Note</th></tr></thead><tbody>{extra_rows}</tbody></table></div>
</section>
<section>
  <h2>Does the spin last?</h2>
  <p class="section-lead">The same paddles, re-tested after real play.</p>
  <div class="table-wrap"><table class="cmp" style="min-width:680px"><thead><tr><th>Paddle</th><th>Time in play</th><th>Result</th><th>Verdict</th></tr></thead><tbody>{dur_summary}</tbody></table></div>
  <div class="grid" style="grid-template-columns:minmax(0,1fr);margin-top:20px">{dur_blocks}</div>
</section>
<section>
  <h2>Single-paddle results in detail</h2>
  <div class="table-wrap"><table class="cmp" style="min-width:680px"><thead><tr><th>Paddle</th><th>Condition</th><th>Spin, average</th><th>Highest hit</th><th>Rebound speed</th><th>Test date</th></tr></thead><tbody>{detail_rows}</tbody></table></div>
</section>
<section id="method">
  <h2>How the test works</h2>
  <table class="specs">
    <tr><th>Paddle</th><td>Clamped in a vise, tilted back about 30 to 35&deg; from vertical</td></tr>
    <tr><th>Ball feed</th><td>Rallie ball machine, about 34 to 39 mph at the paddle</td></tr>
    <tr><th>Camera</th><td>GoPro, 1080p at 960 frames per second</td></tr>
    <tr><th>Ball</th><td>Marked with thick black lines so its rotation can be read</td></tr>
    <tr><th>Spin</th><td>Worked out from how far the markings turn between frames</td></tr>
    <tr><th>Speed adjustment</th><td>Every result is scaled to a 37.5 mph incoming ball (spin &times; 37.5 &divide; actual incoming speed)</td></tr>
    <tr><th>Target impact angle</th><td>Ball meets the face at about 34&deg;</td></tr>
    <tr><th>Hits counted</th><td>Face and throat hits; balls that hit the vise or miss are excluded</td></tr>
  </table>
  <h3 style="margin-top:24px">The three numbers we report</h3>
  <ul><li><strong>Spin (average):</strong> the average of the paddle's best hits (best 3 or best 5; the two differ by about 20 RPM).</li><li><strong>Top spin (highest hit):</strong> the single highest hit.</li><li><strong>Rebound speed:</strong> average ball speed coming off the paddle, a simple indicator of power.</li></ul>
  <h3 style="margin-top:24px">Limits</h3>
  <ul>
    <li>This is a static rig with no swing, so on-court spin will be higher and varies by player. It's a tool for comparing paddles with each other and with themselves over time.</li>
    <li>It is not an official USA Pickleball test. <a href="disclaimers.html#spin">Disclaimers</a>.</li>
    <li>One sample of each paddle was tested. Paddles were tested on different days and have different use histories.</li>
    <li>Where the ball lands on the face changes the result: the lower-middle of the face spins the most, the tip the least.</li>
    <li>Results are adjusted for ball speed but not for small differences in impact angle between sessions. The rig was re-set during October 2026, and numbers from different setups aren't directly comparable.</li>
  </ul>
</section>
<section style="padding-top:0"><div class="note"><strong>Disclosures.</strong> Evolv requested the CarbonSkyn durability testing and provided the three Origin paddles. The Grit E2CF paddles were provided by the owner of Grit. Pickleball RX has discount codes with some brands (including Arronax, Evolv, Holbrook, Luzz, MARK, Pakle and RPM) and earns commission on code or link purchases. Brands have no input into the results. Static-rig numbers from one setup; not an official USA Pickleball test.</div></section>
</div>""", 0, "spin", desc="Pickleball paddle spin test results at 960 fps, plus spin durability re-tests."))

# ---------- Spec Lab ----------
def spec_row(c):
    m, d = c["measured"], c["dimensions"]
    xs, sp, gr = SPEC_LINKS.get(c["id"], (None, None, None))
    links = []
    if xs: links.append(f'<a class="badge" href="xray/{xs}.html">X-ray</a>')
    if sp: links.append(f'<a class="badge" href="spin.html#{slugify(sp)}">Spin</a>')
    if gr: links.append(f'<a class="badge" href="grit.html#{slugify(gr)}">Grit</a>')
    mine = d.get("measuredByPickleballRx", [])
    star = lambda k: ' <span class="muted" title="Measured by Pickleball RX">*</span>' if k in mine else ""
    return (f'<tr><td><a href="#{c["id"]}">{e(c["brand"])} {e(c["model"])}</a></td><td class="num" data-v="{m["swingWeight"]}"><b>{m["swingWeight"]}</b></td>'
            f'<td class="num" data-v="{m["twistWeight"]}"><b>{m["twistWeight"]:.2f}</b></td><td class="num" data-v="{m["staticWeightOz"]}">{m["staticWeightOz"]:.2f} oz</td>'
            f'<td class="num" data-v="{d["lengthIn"]}">{d["lengthIn"]}&Prime;{star("len")}</td><td class="num" data-v="{d["widthIn"]}">{d["widthIn"]}&Prime;{star("wid")}</td>'
            f'<td class="num" data-v="{d["thicknessMm"]}">{d["thicknessMm"]} mm{star("mm")}</td><td class="num" data-v="{d["handleIn"]}">{d["handleIn"]}&Prime;</td>'
            f'<td data-v="{e(c["shape"])}">{e(c["shape"])}</td><td>{" ".join(links) or "<span class=muted>&ndash;</span>"}</td></tr>')


def spec_card(c):
    img = "assets/specs/" + os.path.basename(c["cardImage"])
    notes = "".join(f"<li>{e(n)}</li>" for n in c["notes"])
    return (f'<figure class="lab-item" id="{c["id"]}" style="scroll-margin-top:90px"><a href="{img}"><img src="{img}" alt="{e(c["brand"])} {e(c["model"])} spec card: swing weight {c["measured"]["swingWeight"]}, twist weight {c["measured"]["twistWeight"]}, {c["measured"]["staticWeightOz"]} oz" loading="lazy" style="aspect-ratio:auto;object-fit:contain;background:#fff"></a>'
            f'<figcaption><strong style="color:var(--ink)">{e(c["brand"])} {e(c["model"])}</strong> &middot; published specs: <a href="{e(c["source"]["url"])}" rel="noopener">{e(c["source"]["name"])}</a>'
            + (f'<ul style="margin:6px 0 0;padding-left:18px">{notes}</ul>' if notes else "") + '</figcaption></figure>')


spec_rows = "".join(spec_row(c) for c in sorted(SPECS, key=lambda c: -c["measured"]["swingWeight"]))
spec_cards = "".join(spec_card(c) for c in sorted(SPECS, key=lambda c: c["card"]))
sw = [c["measured"]["swingWeight"] for c in SPECS]; tw = [c["measured"]["twistWeight"] for c in SPECS]
h2h = "assets/specs/proton-coyote-vs-sypik-triton-5.webp"
write("specs.html", page("Spec Lab: measured swing weight and twist weight | PickleballRx", f"""
<section class="hero" style="padding:44px 0"><div class="wrap" style="grid-template-columns:1fr"><div>
  <span class="tag">Spec Lab</span>
  <h1>Swing weight and twist weight, <em>measured by us</em>.</h1>
  <p>Published specs tell you length and width. How heavy a paddle swings, and how stable it is on off-center hits, we measure ourselves. {len(SPECS)} paddles so far.</p>
</div></div></section>
<div class="wrap">
<section>
  <div class="tools">
    <div class="tool"><div class="ico">SW</div><h3>Swing weight</h3><p>How heavy the paddle feels when you swing it. Higher means more plow-through and power, but slower hands. Ours range from {min(sw)} to {max(sw)}.</p></div>
    <div class="tool"><div class="ico">TW</div><h3>Twist weight</h3><p>How much the paddle resists twisting on off-center hits. Higher means a bigger, more stable sweet spot. Ours range from {min(tw):.2f} to {max(tw):.2f}.</p></div>
    <div class="tool"><div class="ico">oz</div><h3>Static weight</h3><p>What the paddle weighs on a scale. Two paddles with the same static weight can swing very differently.</p></div>
  </div>
</section>
<section style="padding-top:0">
  <div class="section-head"><div><h2>All measured paddles</h2><p class="section-lead">Swing, twist and static weight measured by Pickleball RX. Click a column to sort. Other specs are published by the brand or a retailer and may differ from your paddle; * marks ones we measured ourselves. <a href="disclaimers.html#specs">Disclaimers</a>.</p></div></div>
  <div class="table-wrap"><table class="db sortable" id="spec-table" style="min-width:860px">
    <thead><tr><th><button>Paddle</button></th><th aria-sort="descending"><button>Swing wt</button></th><th><button>Twist wt</button></th><th><button>Static wt</button></th><th><button>Length</button></th><th><button>Width</button></th><th><button>Core</button></th><th><button>Handle</button></th><th><button>Shape</button></th><th>Labs</th></tr></thead>
    <tbody>{spec_rows}</tbody></table></div>
</section>
{f'<section style="padding-top:0"><h2>Head to head</h2><p class="section-lead">Proton Project Coyote vs Sypik Triton 5 Ultimate Pro.</p><div style="max-width:640px"><figure class="lab-item"><a href="{h2h}"><img src="{h2h}" alt="Proton Project Coyote vs Sypik Triton 5 spec comparison" loading="lazy" style="aspect-ratio:auto;object-fit:contain;background:#fff"></a><figcaption>Coyote: lighter with a crisper 15mm core, for quicker hands. Triton 5: heavier with a 16mm core, for more plow and stability.</figcaption></figure></div></section>' if os.path.exists(os.path.join(OUT, h2h)) else ""}
<section style="padding-top:0">
  <h2>Spec cards</h2>
  <p class="section-lead">One card per paddle. Tap a card to open it full size.</p>
  <div class="lab-grid" style="grid-template-columns:repeat(auto-fill,minmax(340px,1fr));align-items:start">{spec_cards}</div>
</section>
</div>""", 0, "specs", desc="Measured swing weight, twist weight and static weight for pickleball paddles."))

# ---------- codes ----------
ccards = "\n".join(
    f'<div class="code-card"><h3>{e(c["brand"])}</h3><p class="muted" style="margin:0">{e(c["offer"])} with our code</p><code>{e(c["code"])}</code>'
    f'<a href="{e(c["url"])}" rel="sponsored noopener">Shop {e(c["brand"])} &rarr;</a></div>' for c in CODES)
# Black Friday deals: only deals seen on the brand's own site. Re-check before each upload.
DEALS_CHECKED = "Nov 17, 2026"
DEALS = [
    dict(brand="Luzz", deal="Black Friday: 20% off select paddles and gear", code="", ends="Dec 1, 2026", url="https://luzzpickleball.com/",
         tested=[("Cannon XPP", "xray/luzz-cannon-xpp.html"), ("Glider 2026", "xray/luzz-glider-2026.html"), ("Inferno 2", "xray/luzz-inferno-2.html")]),
    dict(brand="Friday", deal="Black Friday early access: 30% off Aura Pro, 2 Friday Originals for $89, 30% off bags and gear", code="", ends="Nov 22, 2026", url="https://fridaypickle.com/products/aura-pro-paddle",
         tested=[("Aura Pro Tour", "xray/friday-aura-pro-tour.html")]),
    dict(brand="Holbrook", deal="Early Black Friday: $100 off Arma and Aero paddles", code="BFCM", ends="Nov 24, 2026", url="https://holbrookpickleball.com/collections/arma-aero",
         tested=[]),
    dict(brand="11SIX24", deal="11/6 Sale: $50 off Power 2 paddles", code="", ends="Dec 4, 2026", url="https://11six24.com/pages/power-2",
         tested=[]),
    dict(brand="RPM", deal="Black Friday: 25% off apparel", code="", ends="Not stated", url="https://rpmpb.com/", checked="The Kitchen\u2019s tracker, Nov 16",
         tested=[("Jade X-ray", "xray/rpm-jade.html"), ("Q2 X-ray", "xray/rpm-q2.html"), ("V2 X-ray", "xray/rpm-v2.html")]),
    dict(brand="Selkirk", deal="Black Friday: up to 60% off paddles, 50% off apparel", code="", ends="Not stated", url="https://selkirk.com/paddles", checked="The Kitchen\u2019s tracker, Nov 16",
         tested=[("Project Boomstik grit", "grit.html#selkirk-labs-project-boomstik")]),
    dict(brand="Diadem", deal="Black Friday: up to 58% off paddles", code="", ends="Not stated", url="https://diademsports.com/", checked="The Kitchen\u2019s tracker, Nov 16",
         tested=[]),
    dict(brand="FLiK", deal="Black Friday: 2 paddles for $140", code="", ends="Nov 20, 2026", url="https://flikpickleball.com/", checked="The Kitchen\u2019s tracker, Nov 16",
         tested=[("F1 X-ray", "xray/flik-f1.html")]),
    dict(brand="MARK", label="Starts Nov 20", deal="Black Friday sale starts Nov 20. Details not announced yet.", code="", code_note="Details to come", ends="Not stated", url="https://markpickleball.com/", checked="The Kitchen\u2019s tracker, Nov 16",
         tested=[("unMARKed 2026 X-ray", "xray/mark-unmarked-2026.html")]),
    dict(brand="Grit", label="Sale price", deal="E2-CF $135 (was $175). E1-TW $110 (was $185); the E1 is not USA Pickleball approved.", code="", ends="Not stated", url="https://grit-shop.com/",
         tested=[("E2-CF X-ray", "xray/grit-e2-cf.html"), ("E2-CF spin", "spin.html#grit-e2cf")]),
    dict(brand="Vanwin", label="Black Friday", deal="Alpha Control $83.99 \u00b7 Alpha Power $83.99 \u00b7 Pro T7 $47.99 \u00b7 Pro T8 $63.99", code="", code_note="Goes live Nov 18 at 12:00 AM PST", ends="Not stated", url="https://www.vanwinsports.com/",
         checked="Nov 18, 2026", tested=[("Alpha Control", "xray/vanwin-alpha-control.html"), ("Alpha Power", "xray/vanwin-alpha-power.html")]),
]


def deal_card(d):
    tested = " &middot; ".join(f'<a href="{u}">{e(n)}</a>' for n, u in d["tested"])
    return (f'<div class="code-card"><span class="tag" style="align-self:flex-start">{e(d.get("label", "Black Friday"))}</span><h3>{e(d["brand"])}</h3><p style="margin:0">{e(d["deal"])}</p>'
            + (f'<code>{e(d["code"])}</code>' if d["code"] else f'<p class="muted" style="margin:0;font-size:.9rem">{e(d.get("code_note", "No code needed"))}</p>')
            + f'<p class="muted" style="margin:0;font-size:.85rem">Ends: {e(d["ends"])} &middot; checked {d.get("checked", DEALS_CHECKED)}</p>'
            + (f'<p style="margin:0;font-size:.88rem">Our lab data: {tested}</p>' if tested else "")
            + (f'<p style="margin:0;font-size:.88rem"><span class="tag" style="background:#e6f4ea;color:#1e6b35">PBRX works here</span> {next(c["offer"] for c in CODES if c["brand"] == d["brand"])} with code <strong>PBRX</strong>. Check at checkout whether it stacks with the sale.</p>' if any(c["brand"] == d["brand"] for c in CODES) else "")
            + f'<a href="{e(d["url"])}" rel="noopener">See the deal on {e(d["brand"])}&rsquo;s site &rarr;</a></div>')


write("codes.html", page("Pickleball Black Friday deals and discount codes | PickleballRx", f'''
<div class="wrap"><section>
  <h1 class="page-title">Deals</h1>
  <p class="section-lead">Pickleball RX has discount codes with some brands and earns commission on code or link purchases, at no extra cost to you. Brands have no input into our results. <a href="disclaimers.html">Disclaimers</a>.</p>
</section>
<section style="padding-top:0">
  <h2>Black Friday 2026</h2>
  <p class="section-lead">Black Friday and other paddle sales. Each card says where we found it: on the brand&rsquo;s own site, from the brand directly, or from The Kitchen&rsquo;s Black Friday tracker. Every link goes to the brand&rsquo;s own store. Prices and dates change fast, so check the brand&rsquo;s page before you buy.</p>
  <p class="section-lead">Look for the green <strong>PBRX works here</strong> tag: our code works at those brands (Holbrook, RPM, Luzz, Evolv, Arronax, MARK, Pakle, Grit and Speedup). Codes usually don&rsquo;t stack with sale prices, so check at checkout which is better.</p>
  <div class="codes">{"".join(deal_card(d) for d in sorted(DEALS, key=lambda d: not any(c["brand"] == d["brand"] for c in CODES)))}</div>
  <p class="muted" style="font-size:.9rem;margin-top:16px">Also on sale now, per <a href="https://thekitchenpickle.com/pickleball-black-friday-deals/" rel="noopener">The Kitchen&rsquo;s Black Friday tracker</a> (updated Nov 16): Six Zero up to 65% off paddles (ends Nov 30), Warping Point 20% off Neon, Sophon and Nightblade (ends Nov 30), Thrive 25% off sitewide, and Dominator 15% off sitewide (ends Nov 30). We haven&rsquo;t checked these on the brands&rsquo; own sites.</p>
</section>
<section style="padding-top:0">
  <h2>Our discount codes</h2>
  <p class="section-lead">Use code <strong>PBRX</strong> at checkout with these brands. Codes usually do not stack with sale prices, so check which gives the better deal. More brands coming soon.</p>
  <div class="codes">{ccards}</div>
</section></div>''', 0, "codes", desc="Black Friday pickleball paddle deals and Pickleball RX discount codes."))

# ---------- guide ----------
write("guide.html", page("How to choose a pickleball paddle | PickleballRx", '''
<article class="article">
  <span class="tag">Buying guide</span>
  <h1>How to choose a pickleball paddle</h1>
  <div class="byline">PickleballRx team</div>
  <p>The best paddle is the one that matches how you play. Start with these questions, or let the <a href="finder.html">paddle finder</a> do it for you.</p>
  <h2>1. How heavy should it be?</h2>
  <p>Lighter paddles (roughly under 7.8 oz) are quicker at the kitchen line and easier on the arm. Heavier paddles (over about 8.2 oz) add stability and drive power but can tire you out. Swing weight matters even more than static weight: it measures how heavy the paddle feels when you swing it.</p>
  <h2>2. What is twist weight?</h2>
  <p>Twist weight measures how much a paddle resists twisting on off-center hits. Higher twist weight means a more forgiving, stable paddle.</p>
  <h2>3. What core thickness?</h2>
  <p>Thicker cores (around 16 mm) tend to feel softer and more controlled. Thinner cores (around 13 to 14 mm) usually feel crisper with more pop.</p>
  <h2>4. Which shape?</h2>
  <ul><li><strong>Standard / wide body:</strong> biggest sweet spot, most forgiving.</li><li><strong>Elongated:</strong> more reach and power, smaller sweet spot.</li><li><strong>Hybrid:</strong> a middle ground.</li></ul>
  <h2>5. What face material?</h2>
  <p>Fiberglass faces often feel springier. Carbon fiber faces usually give more control and, with a textured surface, more spin. Our <a href="lab.html#micro">microscope scans</a> show how much grit a face really has.</p>
  <div class="note">Check your league's rules: sanctioned events require approved paddles, so look for an approval mark before you buy.</div>
  <p><a class="btn" href="finder.html">Get your paddle Rx</a></p>
</article>''', 0, "guide"))

# ---------- about ----------
write("about.html", page("About and how we test | PickleballRx", f'''
<article class="article">
  <h1>About PickleballRx</h1>
  <p>Pickleball RX was started by Don, Beni and Siva (<a href="{INSTAGRAM}">@picklebrx</a>). We review pickleball paddles from the inside out: X-rays, microscope grit scans and spin measured at 960 frames per second. <em>(Placeholder: add a few sentences about your playing background.)</em></p>
  <h2 id="testing">How we test</h2>
  <ol>
    <li><strong>Play it.</strong> Every paddle gets drills and real games, and a video review on <a href="{YOUTUBE}">YouTube</a>.</li>
    <li><strong>Measure it.</strong> Weight, swing weight, twist weight, dimensions and core thickness, measured ourselves.</li>
    <li><strong>Look inside.</strong> <a href="lab.html">X-rays</a> show the core and ring. A <a href="grit.html">4K microscope</a> shows face grit and wear.</li>
    <li><strong>Measure spin.</strong> A fixed <a href="spin.html">spin rig</a> filmed at 960 fps, then re-tested after real play.</li>
    <li><strong>Score it.</strong> Power, spin, control and forgiveness on the same 10-point scale.</li>
  </ol>
  <h2 id="disclosure">Disclosures</h2>
  <p>We earn commission on some discount codes, and brands have no input into our results. Some test paddles were supplied by brands, and we say so wherever it applies. Read the full <a href="disclaimers.html">disclaimers</a>.</p>
  <h2 id="contact">Contact</h2>
  <p>Message us on <a href="{INSTAGRAM}">Instagram @picklebrx</a>. <em>(Placeholder: add a contact email.)</em></p>
</article>''', 0, "about"))

write("disclaimers.html", page("Disclaimers | PickleballRx", f'''
<article class="article">
  <span class="tag">Disclaimers</span>
  <h1>Disclaimers and disclosures</h1>
  <p class="muted">Last updated {LABS["updated"]}. Here is how our results are made, who supplied what, and where the limits are.</p>

  <h2 id="affiliate">Discount codes and commission</h2>
  <p>Pickleball RX has discount codes with some brands, including Arronax, Evolv, Holbrook, Luzz, MARK, Pakle and RPM, and may earn a commission when you buy with a code or through some links. It costs you nothing extra. Deals and prices are checked on the brand's own site when we post them, but they can change or end at any time, so confirm the final price at checkout.</p>

  <h2 id="independence">Brands have no input into results</h2>
  <p>No brand sees, edits or approves our results before they are published. Having a code with a brand never changes a number, a score or a ranking, and a brand can't pay for a spot on the Leader Board.</p>

  <h2 id="supplied">Paddles supplied by brands</h2>
  <ul>
    <li>Evolv requested the CarbonSkyn spin durability test and supplied the three Origin paddles used in it. The testing and the numbers are our own.</li>
    <li>The Grit E2CF paddles were supplied by the owner of Grit.</li>
    <li>Grit E1 CW and E1 TW are recreational-play paddles that are not USA Pickleball approved.</li>
  </ul>

  <h2 id="spin">Spin Lab</h2>
  <p>Spin numbers come from our own static rig: the same ball machine and setup, filmed at 960 frames per second. It is not an official USA Pickleball test. Results depend on the ball, the impact angle and where the ball hits the face, so treat small gaps between paddles as a tie, and compare paddles within our table rather than against other testers' numbers.</p>

  <h2 id="xray">X-Ray Rx</h2>
  <p>X-ray labels (core, perimeter ring, inserts, handle) are our interpretation of the X-ray image. They are not a cutaway, and brands have not confirmed them. Ring widths and other measurements taken from an X-ray are estimates.</p>

  <h2 id="grit">Grit Lab</h2>
  <p>Microscope images were taken with a 4K digital microscope. Wear percentages are conservative visual estimates, about plus or minus 10 points, made by comparing each paddle's hitting zone with its own throat under matched light. They are not profilometer measurements, and grit wears at different rates depending on how much and how you play.</p>

  <h2 id="specs">Specs</h2>
  <p>Swing weight, twist weight and static weight marked as ours are measured by Pickleball RX. Other specs come from the sources listed with each paddle, usually the brand or a retailer. Paddles vary from unit to unit and brands update models, so your paddle can differ from what we list.</p>

  <h2 id="advice">Not professional advice</h2>
  <p>Everything on this site is our own testing and opinion, for general information only. It is not professional advice. Check specs, approval status and warranty terms with the brand before you buy, and check the current USA Pickleball approved list before using a paddle in sanctioned play.</p>

  <h2 id="corrections">Questions or corrections</h2>
  <p>If you think something here is wrong, message us on <a href="{INSTAGRAM}">Instagram @picklebrx</a> and we'll check it.</p>
</article>''', 0, "disclaimers", desc="How Pickleball RX tests paddles, who supplied what, and the limits of our results."))


# ---------- Brand spotlight: Grit ----------
# Public facts only: from grit-shop.com (about page) and Siva. Confidential Grit prototypes stay off the site.
GRIT_SHOP = "https://www.grit-shop.com/"
GRIT_LINEUP = [
    dict(slug="grit-e2-cf", name="E2-CF", spin="Grit E2CF", usap=True,
         text="16 mm flex-foam paddle. Comes in several colorways, including the green Launch Edition, pink and white.",
         links=[("X-ray", "xray/grit-e2-cf.html"), ("Spin", "spin.html#grit-e2cf"), ("Spin durability", "spin.html#dur-grit-e2cf")]),
    dict(slug="grit-e1-cw", name="E1-CW", spin="Grit E1 CW", usap=False,
         text="16 mm, elongated, with a tight plain carbon weave under a thin glossy coat. Made for recreational play.",
         links=[("Spin", "spin.html#grit-e1-cw"), ("Microscope", "grit.html#grit-e1")]),
    dict(slug="grit-e1-tw", name="E1-TW", spin="Grit E1 TW", usap=False,
         text="16 mm, elongated. The same carbon weave with titanium strands woven through it in a grid. Made for recreational play.",
         links=[("Spin", "spin.html#grit-e1-tw"), ("Microscope", "grit.html#grit-e1")]),
]
_NOT_USAP = '<span class="tag" style="background:#fde2e2;color:#8a1c1c">Not USAP approved</span>'


def grit_lineup_card(g):
    r = next((x for x in LABS["spin"] + LABS["spin_extra"] if x["paddle"] == g["spin"]), None)
    spin = f'<div class="spot-stat"><b>{r["avg"]:,}</b><span>RPM spin average</span></div>' if r else ""
    label = _NOT_USAP if not g["usap"] else '<span class="tag">USAP approved</span>'
    links = "".join(f'<a class="badge" href="{h}">{e(t)}</a>' for t, h in g["links"])
    return (f'<div class="card spot-card"><img src="{product_photo(g["slug"])}" alt="Grit {e(g["name"])}" width="200" height="300" loading="lazy">'
            f'<div><div class="muted" style="font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700">Grit</div>'
            f'<h3 style="margin:2px 0 6px">{e(g["name"])}</h3>{label}<p style="font-size:.95rem;margin:10px 0">{e(g["text"])}</p>{spin}'
            f'<div class="badges" style="margin:10px 0">{links}</div>'
            f'<a class="btn yellow" href="{GRIT_SHOP}" rel="noopener" target="_blank">Buy at Grit: code PBRX, 10% off &rarr;</a></div></div>')


_dur = next((d for d in LABS["durability"] if d["paddle"] == "Grit E2CF"), None)
write("grit-pickleball.html", page("Grit Pickleball: brand spotlight | PickleballRx", f"""
<section class="hero" style="padding:48px 0"><div class="wrap">
  <div>
    <span class="tag">Brand spotlight</span>
    <h1>The most passionate owners in <em>pickleball</em>.</h1>
    <p>That's our take on GRIT. PICKLEBALL, a paddle brand born in Baton Rouge, Louisiana. We've X-rayed, scoped and spin-tested their paddles, and the numbers hold up.</p>
    <div class="btn-row"><a class="btn yellow" href="{GRIT_SHOP}" rel="noopener" target="_blank">Shop Grit</a><a class="btn ghost" href="#lab">See our lab results</a></div>
  </div>
  <figure class="hero-art" style="margin:0;text-align:center"><img src="assets/paddles/product/grit-e2-cf.jpg" alt="Grit E2-CF Launch Edition" width="300" height="450" style="border-radius:14px;max-width:300px;width:100%;height:auto"></figure>
</div></section>
<div class="wrap">
<section style="padding-bottom:0">
  <div class="deal" style="text-align:left"><strong>Get 10% off at Grit</strong> with code <code style="display:inline-block;margin:0 6px">PBRX</code><a href="{GRIT_SHOP}" rel="noopener" target="_blank">Shop Grit &rarr;</a>
  <div class="muted" style="font-size:.82rem;margin-top:4px">Grit provided the E2-CF paddles we tested, and we say so wherever those results appear. Brands have no input into our results. <a href="disclaimers.html">Disclaimers</a></div></div>
</section>
<section class="story-split">
  <figure class="story-fig"><img src="assets/paddles/product/grit-lsu.jpg" alt="Jacob of Grit Pickleball with Ethan Martin, president of the LSU pickleball team" width="640" height="983" loading="lazy"><figcaption>Jacob of Grit Pickleball with Ethan Martin, president of the LSU pickleball team.</figcaption></figure>
  <div>
  <h2>Their story</h2>
  <p class="section-lead">In Grit's own words, the brand "was born in Baton Rouge, Louisiana" and started with "a simple belief: that the players who grind the hardest, compete the smartest" deserve equipment built to match their drive. Their paddles are designed in Baton Rouge, and every one says "Made for more" on the face.</p>
  <p class="muted" style="font-size:.85rem">Source: <a href="https://www.grit-shop.com/pages/about-us" rel="noopener">Grit's About page</a>.</p>
  </div>
</section>
<section style="padding-top:0">
  <h2>The paddles we've tested</h2>
  <p class="section-lead">Product photos supplied to Pickleball RX. Grit makes more models than these. See the full lineup on <a href="{GRIT_SHOP}" rel="noopener">grit-shop.com</a>.</p>
  <div class="spot-grid">{"".join(grit_lineup_card(g) for g in GRIT_LINEUP)}</div>
  <p class="muted" style="font-size:.9rem;margin-top:12px">Grit E1-CW and E1-TW are recreational-play paddles that are not USA Pickleball approved.</p>
</section>
<section id="lab" style="padding-top:0">
  <h2>What our labs found</h2>
  <div class="tools">
    <a class="tool" href="spin.html"><div class="ico">RPM</div><h3>Top of our spin chart</h3><p>The E1-TW and E1-CW hold the two highest spin averages we've recorded on our rig. They're not USAP approved, so we show them for reference.</p><span class="go">See spin results &rarr;</span></a>
    <a class="tool" href="spin.html#dur-grit-e2cf"><div class="ico">&#8635;</div><h3>Spin that lasts</h3><p>We re-tested the E2-CF after {e(_dur["time"]) if _dur else "real play"} of play. Verdict: {e(_dur["verdict"].split(":")[-1].strip()) if _dur else "see results"}{", about 2,020 RPM on the used paddle" if _dur else ""}.</p><span class="go">See durability &rarr;</span></a>
    <a class="tool" href="xray/grit-e2-cf.html"><div class="ico">X</div><h3>E2-CF X-ray</h3><p>See inside the E2-CF: core, perimeter ring and handle, labeled from the X-ray.</p><span class="go">See inside &rarr;</span></a>
    <a class="tool" href="grit.html#grit-e1"><div class="ico">&micro;</div><h3>Under the microscope</h3><p>E1-CW versus E1-TW at the L and M lenses: plain carbon weave versus a titanium grid.</p><span class="go">See the grit &rarr;</span></a>
  </div>
</section>
</div>""", 0, "", desc="Grit Pickleball brand spotlight: a Baton Rouge paddle brand, with Pickleball RX X-ray, microscope and spin results."))


# ---------- Brand spotlight: Evolv ----------
# Story quoted only from evolvpickleball.com/about.
EVOLV_SHOP = "https://evolvpickleball.com/"
_ev_dur = next((d for d in LABS["durability"] if d["paddle"].startswith("Evolv Origin")), None)
_ev_spin = next((x for x in LABS["spin"] + LABS["spin_extra"] if x["paddle"] == "Evolv Origin"), None)
_ev_x = next((x for x in XRAY if x["slug"] == "evolv-origin"), None)
write("evolv-pickleball.html", page("Evolv Pickleball: brand spotlight | PickleballRx", f"""
<section class="hero" style="padding:48px 0"><div class="wrap">
  <div>
    <span class="tag">Brand spotlight</span>
    <h1>The spin that <em>doesn't fade</em>.</h1>
    <p>That's what we found when we tested Evolv. We re-tested the Origin's CarbonSkyn face at new, one month and six months of play, and the spin held.</p>
    <div class="btn-row"><a class="btn yellow" href="{EVOLV_SHOP}" rel="sponsored noopener" target="_blank">Shop Evolv</a><a class="btn ghost" href="#lab">See our lab results</a></div>
  </div>
  <figure class="hero-art" style="margin:0;text-align:center"><img src="assets/paddles/product/evolv-origin.jpg" alt="Evolv Origin" width="300" height="450" style="border-radius:14px;max-width:300px;width:100%;height:auto"></figure>
</div></section>
<div class="wrap">
<section style="padding-bottom:0">
  {code_box("Evolv")}
  <p class="muted" style="font-size:.88rem">Evolv requested the CarbonSkyn durability testing and provided the three Origin paddles. Brands have no input into our results.</p>
</section>
<section class="story-split">
  <figure class="story-fig"><img src="assets/paddles/product/evolv-owner.jpg" alt="The founder of Evolv Pickleball hitting a low shot with an Evolv paddle" width="640" height="960" loading="lazy"><figcaption>Evolv's founder on court with an Evolv paddle.</figcaption></figure>
  <div>
  <h2>Their story</h2>
  <p class="section-lead">Evolv says it was "founded by a former tennis player who initially underestimated the game of pickleball." He gave the game another chance during the COVID pandemic and "was instantly hooked." Working with a manufacturing partner, he went through "dozens of prototype iterations," and "that pursuit became the EVOLV Origin." Their motto is "Mastery Through Progress."</p>
  <p class="muted" style="font-size:.85rem">Source: <a href="https://www.evolvpickleball.com/about" rel="noopener">Evolv's About page</a>.</p>
  </div>
</section>
<section style="padding-top:0">
  <h2>The paddle we've tested</h2>
  <div class="spot-grid"><div class="card spot-card"><img src="assets/paddles/product/evolv-origin.jpg" alt="Evolv Origin" width="200" height="300" loading="lazy">
    <div><div class="muted" style="font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700">Evolv</div>
    <h3 style="margin:2px 0 6px">Origin</h3>
    <p style="font-size:.95rem;margin:10px 0">{e(_ev_x["core"]) if _ev_x else "Full foam"} core, {e(_ev_x["face"]) if _ev_x else "CarbonSkyn"} face, {e(_ev_x["size"]) if _ev_x else "elongated"}.</p>
    {f'<div class="spot-stat"><b>{_ev_spin["avg"]:,}</b><span>RPM spin average ({e(_ev_spin["condition"].lower())})</span></div>' if _ev_spin else ""}
    <div class="badges" style="margin:10px 0"><a class="badge" href="xray/evolv-origin.html">X-ray</a><a class="badge" href="spin.html#evolv-origin">Spin</a><a class="badge" href="spin.html#dur-{slugify(_ev_dur["paddle"]) if _ev_dur else ""}">Spin durability</a><a class="badge" href="grit.html#evolv">Microscope</a></div>
    <a class="btn yellow" href="{EVOLV_SHOP}" rel="sponsored noopener" target="_blank">Buy at Evolv: code PBRX, 15% off &rarr;</a></div></div></div>
</section>
<section id="lab" style="padding-top:0">
  <h2>What our labs found</h2>
  <div class="tools">
    <a class="tool" href="spin.html#dur-{slugify(_ev_dur["paddle"]) if _ev_dur else ""}"><div class="ico">&#8635;</div><h3>Spin that lasts</h3><p>{f'Three Origins tested: new, one month and six months ({e(_ev_dur["time"].split(",")[-1].strip())}). Top spin went {e(_ev_dur["result"].replace(" (top spin)", ""))}. Verdict: no measurable loss.' if _ev_dur else "Re-tested after real play."}</p><span class="go">See durability &rarr;</span></a>
    <a class="tool" href="grit.html#evolv"><div class="ico">&micro;</div><h3>CarbonSkyn up close</h3><p>The same face under a 4K microscope at three ages, plus a side-by-side with the 11SIX24 HexGrit Power 2.</p><span class="go">See the grit &rarr;</span></a>
    <a class="tool" href="xray/evolv-origin.html"><div class="ico">X</div><h3>Origin X-ray</h3><p>See inside the Origin: {e(_ev_x["core"]) if _ev_x else "full foam"} core, perimeter band and handle, labeled from the X-ray.</p><span class="go">See inside &rarr;</span></a>
  </div>
</section>
</div>""", 0, "", desc="Evolv Pickleball brand spotlight: the Origin's CarbonSkyn spin durability, X-ray and microscope results."))


# ---------- Brand spotlight: Gearbox (replaced Speedup, per Siva 2026-11-17) ----------
# Founder story from press: The Dink (Jul 2026) and San Diego Business Journal. No PBRX code for Gearbox unless Siva confirms one.
GEARBOX_SHOP = "https://gearboxsports.com/"
_gb_spin = {x["paddle"]: x for x in LABS["spin"]}
_gb_e, _gb_m = _gb_spin.get("Gearbox Pressure XE"), _gb_spin.get("Gearbox Pressure X M")
_gb_x = {x["slug"]: x for x in XRAY}
def _gb_card(model, photo, xs, spin, spin_anchor, grit_anchor, blurb):
    x = _gb_x.get(xs)
    return (f'<div class="card spot-card"><img src="{photo}" alt="Gearbox {e(model)}" width="200" height="300" loading="lazy" style="background:#fff;object-fit:contain">'
            f'<div><div class="muted" style="font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700">Gearbox</div><h3 style="margin:2px 0 6px">{e(model)}</h3>'
            f'<p style="font-size:.95rem;margin:10px 0">{blurb} {e(x["core"]) if x else ""} core, {e(x["thickness"]) if x else ""}, {e(x["face"]) if x else ""} face.</p>'
            + (f'<div class="spot-stat"><b>{spin["avg"]:,}</b><span>RPM spin average ({e(spin["condition"].lower())})</span></div>' if spin else "")
            + f'<div class="badges" style="margin:10px 0"><a class="badge" href="xray/{xs}.html">X-ray</a><a class="badge" href="spin.html#{spin_anchor}">Spin</a>'
            + (f'<a class="badge" href="grit.html#{grit_anchor}">Microscope</a>' if grit_anchor else "") + '</div></div></div>')
write("gearbox-pickleball.html", page("Gearbox Pickleball: brand spotlight | PickleballRx", f"""
<section class="hero" style="padding:48px 0"><div class="wrap">
  <div>
    <span class="tag">Brand spotlight</span>
    <h1>Passion, <em>engineered</em>.</h1>
    <p>Rafael Filippini, Gearbox's founder and CEO, is one of the most passionate people in the paddle business. He went from pro racquetball and the Marines to building paddles in San Diego with his own patented carbon cores, and he calls his team "extremely passionate about what we do." His Pressure X 8E holds the top spot on our Leader Board.</p>
    <div class="btn-row"><a class="btn yellow" href="{GEARBOX_SHOP}" rel="noopener" target="_blank">Shop Gearbox</a><a class="btn ghost" href="#lab">See our lab results</a></div>
  </div>
  <figure class="hero-art" style="margin:0;text-align:center"><img src="assets/paddles/product/gearbox-pressure-x-8e.jpg" alt="Gearbox Pressure X 8E on the Pickleball RX Leader Board" width="300" height="450" style="border-radius:14px;max-width:300px;width:100%;height:auto;background:#fff;object-fit:contain"></figure>
</div></section>
<div class="wrap">
<section>
  <h2>Rafael's story</h2>
  <p class="section-lead">Rafael Filippini moved to the U.S. from Mexico as a young child, before he spoke English. He joined the Marines, where he first worked with composites on high-performance aircraft, then studied engineering while playing professional racquetball. After 13 years with a racquetball equipment maker, he founded Gearbox in 2007 as a racquetball racquet company.</p>
  <p class="section-lead">He first saw pickleball in 2009 in St. George, Utah, where older players beat him and his friends. Gearbox added pickleball paddles in 2015, and Rafael set out to give players "an actual edge" rather than a new color or logo. Today Gearbox sells in close to 30 countries, is the official paddle of the National Pickleball League, and holds a long list of its own patents, including the SST carbon-rib core we see in our X-rays.</p>
  <p class="muted" style="font-size:.85rem">Sources: <a href="https://www.thedinkpickleball.com/the-story-behind-gearbox-pickleball-50-patents-in-10-years/" rel="noopener">The Dink</a> and the <a href="https://sdbj.com/sports-2/san-diego-businesses-net-success-with-pickleball/" rel="noopener">San Diego Business Journal</a>.</p>
</section>
<section style="padding-top:0">
  <h2>The paddles we've tested</h2>
  <div class="spot-grid">
    {_gb_card("Pressure X 8E", "assets/paddles/product/gearbox-pressure-x-8e.jpg", "gearbox-pressure-x-8e", _gb_e, "gearbox-pressure-xe", "gearbox-pressure-x-8e", "The top spot on our Leader Board.")}
    {_gb_card("Pressure X 8M", "assets/paddles/product/gearbox-pressure-xm.jpg", "gearbox-pressure-xm", _gb_m, "gearbox-pressure-x-m", "", "The MPP-foam sibling of the 8E.")}
  </div>
</section>
<section id="lab" style="padding-top:0">
  <h2>What our labs found</h2>
  <div class="tools">
    <a class="tool" href="xray/gearbox-pressure-x-8e.html"><div class="ico">X</div><h3>Inside the core</h3><p>Both paddles show Gearbox's SST carbon ribs running through the foam core, with a TPE perimeter band.</p><span class="go">See the X-ray &rarr;</span></a>
    <a class="tool" href="spin.html#gearbox-pressure-xe"><div class="ico">RPM</div><h3>Spin</h3><p>{f'The 8E averaged {_gb_e["avg"]:,} RPM new, tied for the highest of any USAP-approved paddle on our 960 fps rig.' if _gb_e else "Measured on our 960 fps rig."}</p><span class="go">See spin results &rarr;</span></a>
    <a class="tool" href="grit.html#gearbox-pressure-x-8e"><div class="ico">&micro;</div><h3>Under the microscope</h3><p>The 8E's SpinLock silicon carbide grit under a 4K microscope.</p><span class="go">See the grit &rarr;</span></a>
  </div>
</section>
</div>""", 0, "", desc="Gearbox Pickleball brand spotlight: founder Rafael Filippini's story and our X-ray, microscope and spin results for the Pressure X 8E and 8M."))

# ---------- Pro paddles (reference list from public sources; not our testing) ----------
PROS = json.load(open(os.path.join(ROOT, "data", "pros.json")))
_PSRC = PROS["sources"]
_xray_slugs = {x["slug"] for x in XRAY}
_grit_names = {g["name"] for g in LABS["grit"]}


def _pro_paddle(p):
    if p.get("status") == "unconfirmed" and not p.get("brand"):
        note = f'<br><span class="muted" style="font-size:.82rem">{e(p["note"])}</span>' if p.get("note") else ""
        return f'<span class="muted">Unconfirmed</span>{note}'
    out = f'<strong>{e(p["brand"])}</strong> {e(p["paddle"])}'
    if p.get("status") == "sponsor":
        out += ' <span class="muted" style="font-size:.82rem">(paddle sponsor)</span>'
    return out


def _pro_labs(p):
    links = []
    if p.get("xray") in _xray_slugs: links.append(f'<a class="badge" href="xray/{p["xray"]}.html">X-ray</a>')
    if p.get("grit") in _grit_names: links.append(f'<a class="badge" href="grit.html#{slugify(p["grit"])}">Grit</a>')
    return " ".join(links) or '<span class="muted">&ndash;</span>'


def _pro_table(rows, tid):
    body = "".join(
        f'<tr><td class="num">{p["rank"]}</td><td style="white-space:normal"><strong>{e(p["name"])}</strong></td>'
        f'<td style="white-space:normal">{_pro_paddle(p)}</td><td>{_pro_labs(p)}</td></tr>' for p in rows)
    return (f'<div class="table-wrap"><table class="db" id="{tid}" style="min-width:560px"><thead><tr><th>Rank</th><th>Player</th><th>Paddle</th><th>Our labs</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div>')


_ppa_all = PROS["ppa_men"] + PROS["ppa_women"]
_brand_n = {}
for p in _ppa_all:
    if p.get("brand"): _brand_n[p["brand"]] = _brand_n.get(p["brand"], 0) + 1
_top_brands = sorted(_brand_n.items(), key=lambda kv: (-kv[1], kv[0]))[:6]
_brand_tiles = "".join(f'<div style="background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:12px 14px"><b style="font-size:1.5rem">{n}</b> <span style="font-weight:700">{e(b)}</span></div>' for b, n in _top_brands)
_app_html = "".join(f'<h3 style="margin-top:22px">APP {e(d["division"].lower())}</h3>{_pro_table(d["players"], "app-" + slugify(d["division"]))}' for d in PROS["app"])
_s = lambda k: f'<a href="{e(_PSRC[k]["url"])}" rel="noopener">{e(_PSRC[k]["name"])}</a>'

write("pros.html", page("What paddles do the pros use? PPA and APP top players | PickleballRx", f"""
<section class="hero" style="padding:44px 0"><div class="wrap" style="grid-template-columns:1fr"><div>
  <span class="tag">Pro paddles</span>
  <h1>What the <em>top-ranked pros</em> play.</h1>
  <p>The paddle each top PPA and APP player is using, ordered by current tour ranking. A reference list from public sources, updated {_fmt_date(PROS["updated"])}. This is not Pickleball RX testing.</p>
</div></div></section>
<div class="wrap">
<section>
  <h2>Most-used brands</h2>
  <p class="section-lead">Count of players in the PPA top 20 men and top 20 women using each brand.</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px">{_brand_tiles}</div>
</section>
<section style="padding-top:0" id="ppa-men">
  <h2>PPA Tour: top 20 men</h2>
  <p class="section-lead">Ranking: {_s("ppa_rank")} (checked {_fmt_date(_PSRC["ppa_rank"]["checked"])}). These rankings combine doubles, mixed and singles. Paddles as seen at the PPA World Championships, per {_s("worlds")} ({_fmt_date(_PSRC["worlds"]["asof"])}).</p>
  {_pro_table(PROS["ppa_men"], "ppa-men-table")}
</section>
<section style="padding-top:0" id="ppa-women">
  <h2>PPA Tour: top 20 women</h2>
  <p class="section-lead">Same ranking and paddle sources as the men&rsquo;s list.</p>
  {_pro_table(PROS["ppa_women"], "ppa-women-table")}
</section>
<section style="padding-top:0" id="app">
  <h2>APP Tour: top 5 by division</h2>
  <p class="section-lead">Ranking: {_s("app_rank")} (updated {_fmt_date(_PSRC["app_rank"]["asof"])}). Jack Munro&rsquo;s sponsor is from {_s("kitchen_deals")}; Megan Fudge&rsquo;s signature paddle is from {_s("franklin_fudge")}.</p>
  {_app_html}
</section>
<section style="padding-top:0"><div class="note"><strong>About this list.</strong> Rankings and paddle deals change often, and pros sometimes play unreleased or custom paddles. &ldquo;Unconfirmed&rdquo; means we couldn&rsquo;t find a reliable current source, so we didn&rsquo;t guess. The <strong>Our labs</strong> column links to our own X-ray or Grit Lab results where we have them for that paddle model; a pro&rsquo;s paddle may be a custom build. Know a pro&rsquo;s current paddle? <a href="about.html#contact">Tell us</a>.</div></section>
</div>""", 0, "pros", desc="The paddles used by the top-ranked PPA Tour and APP Tour pickleball pros, by ranking, with sources and dates."))

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalog_page.py")).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rx_page.py")).read())

write("404.html", page("Page not found | PickleballRx", '<article class="article"><h1>Page not found</h1><p>That page doesn\'t exist. <a href="/">Go to the home page</a>.</p></article>', 0))

print("Built", len(PADDLES), "paddles into", OUT)
