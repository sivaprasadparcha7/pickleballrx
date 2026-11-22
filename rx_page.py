# Paddle Rx finder (finder.html): asks country, level, budget, construction, foam, shape, top style and priority,
# then ranks paddles with the Pickleball RX scoring rules in assets/rx.js.
# Paddle pool: every paddle in data/catalog.json, plus paddles we've tested that aren't in the catalog,
# plus other reviewers' public picks (RX_EXTRA). Our own lab data (X-ray, Spin Lab, Spec Lab) is joined in.
# Run from build.py (uses its page/write/e/slugify/CODES/XRAY/LABS/LINKS/LEADERBOARD/STYLE_PICKS/TOP_PICKS).
import re

_RX_DIR = os.path.dirname(os.path.abspath(__file__))
_RXCAT = json.load(open(os.path.join(_RX_DIR, "data", "catalog.json")))
_RXSPEC = json.load(open(os.path.join(_RX_DIR, "data", "specs.json")))["paddles"]
_XR = {x["slug"]: x for x in XRAY}

# ---------- sources for other reviewers' public lists (checked 2026-11-18) ----------
SRC = {
    "matt": ("Matt's Pickleball", "https://www.mattspickleball.com/best-pickleball-paddles", "Best paddles list, updated Nov 8, 2026"),
    "matt-spin": ("Matt's Pickleball", "https://www.mattspickleball.com/best-pickleball-paddles", "Ranked by spin, updated Nov 8, 2026"),
    "matt-ac": ("Matt's Pickleball", "https://www.mattspickleball.com/best-all-court-pickleball-paddles", "Best all-court list"),
    "kitchen": ("The Kitchen", "https://thekitchenpickle.com/blogs/gear/best-pickleball-paddles-available/", "Top paddles list, updated Nov 17, 2026"),
    "effect-power": ("Pickleball Effect", "https://pickleballeffect.com/hot-list/", "Hot List: power"),
    "effect-ac": ("Pickleball Effect", "https://pickleballeffect.com/hot-list/", "Hot List: all-court"),
    "effect-control": ("Pickleball Effect", "https://pickleballeffect.com/hot-list/", "Hot List: control"),
    "effect-budget": ("Pickleball Effect", "https://pickleballeffect.com/hot-list/", "Hot List: under about $100"),
    "kew": ("John Kew", "https://www.johnkewpickleball.com/paddle-index", "Written review"),
    "senpai": ("Supasenpai", "https://supasenpai.com/", "Top picks (via Pickleball RX)"),
}
# Which priority each list speaks to (adds a small nudge to that trait).
SRC_TRAIT = {"matt-spin": "spin", "matt-ac": "allcourt", "effect-power": "power", "effect-ac": "allcourt", "effect-control": "control"}

# (brand, model regex, source key). Matched against brand + model of every paddle in the pool.
REVIEWER_PICKS = [
    ("RPM", r"friction pro.*hybrid.*flat", "matt"), ("Volair", r"cmd hyb", "matt"), ("Spartus", r"spitfire elongated", "matt"),
    ("RPM", r"^jade", "matt"), ("11SIX24", r"ultr[eé] power 2", "matt"), ("Selkirk", r"^omni", "matt"),
    ("Enhance", r"mpp turbo with armorgrit", "matt"), ("Six Zero", r"^coral 16mm$", "matt"), ("Honolulu", r"j2cr crystal blue", "matt"),
    ("MARK", r"unmarked 2026", "matt"),
    ("Six Zero", r"coral pro 16mm$", "matt-spin"), ("Honolulu", r"j6cr crystal blue", "matt-spin"), ("CRBN", r"trufoam", "matt-spin"),
    ("Spartus", r"p1", "matt-spin"), ("RPM", r"^q2", "matt-spin"), ("RPM", r"friction pro v2", "matt-spin"), ("Selkirk", r"boomstik", "matt-spin"),
    ("Six Zero", r"^coral 16mm$", "matt-ac"), ("Engage", r"^x2", "matt-ac"), ("Chorus", r"coda", "matt-ac"), ("Honolulu", r"^j2nf$", "matt-ac"),
    ("Franklin", r"aurelius", "matt-ac"), ("Friday", r"fever", "matt-ac"), ("JOOLA", r"kosmos pro v", "matt-ac"), ("Ronbus", r"quanta r4", "matt-ac"),
    ("Honolulu", r"^j6fc\+", "matt-ac"), ("Vatic Pro", r"v-sol power flash", "matt-ac"),
    ("JOOLA", r"pro v$", "kitchen"), ("RPM", r"friction pro v2", "kitchen"), ("Paddletek", r"bantam jolt", "kitchen"), ("Honolulu", r"^j6cr$", "kitchen"),
    ("Selkirk", r"boomstik st", "kitchen"), ("RPM", r"^jade", "kitchen"), ("11SIX24", r"jelly bean 2", "kitchen"), ("Paddletek", r"tempest veyra", "kitchen"),
    ("Proton", r"project coyote", "kitchen"), ("Holbrook", r"fuze", "kitchen"), ("Bread & Butter", r"loco 2", "kitchen"), ("Six Zero", r"coral pro 16mm$", "kitchen"),
    ("Enhance", r"mpp turbo with armorgrit", "kitchen"),
    ("11SIX24", r"ultr[eé] power 2", "effect-power"), ("Thrive", r"ignite foam hybrid", "effect-power"), ("Pickleball Apes", r"zen s\+", "effect-power"),
    ("Honolulu", r"j2cr crystal blue", "effect-power"), ("MARK", r"unmarked 2026", "effect-power"), ("Spartus", r"spitfire elongated", "effect-power"),
    ("Six Zero", r"coral pro 16mm$", "effect-ac"), ("Luzz", r"glider 2026", "effect-ac"), ("Spartus", r"p1", "effect-ac"), ("Volair", r"cmd hyb", "effect-ac"),
    ("Selkirk", r"slk era power", "effect-ac"),
    ("11SIX24", r"vapor jelly bean 2", "effect-control"), ("Vatic Pro", r"prism flash", "effect-control"), ("Chorus", r"shapeshifter", "effect-control"),
    ("Vatic Pro", r"v-sol tour flash", "effect-budget"), ("Spartus", r"spitfire elongated", "effect-budget"), ("Luzz", r"glider 2026", "effect-budget"),
    ("Vatic Pro", r"prism flash", "effect-budget"),
    ("Bread & Butter", r"loco", "kew"), ("JOOLA", r"power fx|kosmos pro v", "kew"), ("Gearbox", r"pressure x 8[em]|gbx power", "kew"),
    ("Friday", r"aura pro", "kew"), ("Thrive", r"ignite", "kew"), ("Honolulu", r"^j3cr|^j6cr", "kew"), ("11SIX24", r"jelly bean 2|power 2", "kew"),
    ("Spartus", r"spitfire", "kew"), ("Six Zero", r"coral pro", "kew"), ("Selkirk", r"^omni|slk era", "kew"), ("Enhance", r"turbo", "kew"),
    ("Speedup", r"tide", "kew"), ("Franklin", r"c45", "kew"), ("Holbrook", r"arma", "kew"), ("Pakle", r"^fuse", "kew"),
    ("Sypik", r"avatar pro", "senpai"), ("Luzz", r"pro 4 inferno", "senpai"),
]

# Hybrid top style, only where the brand's product name or a named source says so. Everything else stays "not confirmed".
# (brand, model regex, "flat" | "round", source)
TOP_STYLE = [
    ("Friday", r"round top", "round", "Friday's own product name"),
    ("Friday", r"flat top|challenger", "flat", "Friday's own product name"),
    ("E6", r"flat top hybrid", "flat", "E6's own product name"),
    ("RPM", r"hybrid flat top", "flat", "RPM's own product name"),
    ("RPM", r"hybrid rounded top", "round", "RPM's own product name"),
    ("11SIX24", r"ultr[eé] power 2", "flat", "Paddle Review Hub shape guide"),
    ("JOOLA", r"kosmos", "flat", "The Dink, flat-top hybrid feature"),
    ("Vatic Pro", r"tour flash ft", "flat", "Paddle Review Hub shape guide"),
]

# Paddles that aren't in the catalog: other reviewers' picks and a few we've tested.
# Prices are US list prices from the named source, checked 2026-11-18. None = we couldn't confirm a US price.
# c: "foam" | "gen3"; f: "epp" | "mpp" | "other" | None; sh: shapes offered (e, h, w).
RX_EXTRA = [
    dict(b="RPM", m="Friction Pro V2 Hybrid Flat Top", p=249.99, c="gen3", f=None, sh="h", mm="14 / 16", usap=True, x="rpm-v2", src="RPM, Matt's Pickleball"),
    dict(b="RPM", m="Q2 Hybrid Flat Top", p=249.99, c="foam", f="epp", sh="h", mm="14 / 16", usap=True, x="rpm-q2", src="RPM, Paddle Review Hub"),
    dict(b="RPM", m="Q2 Hybrid Rounded Top", p=249.99, c="foam", f="epp", sh="h", mm="14 / 16", usap=True, x="rpm-q2", src="RPM, Paddle Review Hub"),
    dict(b="Volair", m="CMD HYB 16mm", p=179.99, c=None, f=None, sh="h", mm="16", usap=None, src="The Kitchen, Matt's Pickleball"),
    dict(b="11SIX24", m="Ultre Power 2 16mm", p=209.99, c="gen3", f=None, sh="h", mm="16", usap=None, src="The Kitchen"),
    dict(b="11SIX24", m="Vapor Power 2 16mm", p=209.99, c="gen3", f=None, sh="h", mm="16", usap=None, src="Matt's Pickleball"),
    dict(b="11SIX24", m="Hurache-X Alpha Pro Power", p=199.99, c="gen3", f=None, sh="e", mm="16", usap=None, x="11six24-hurache-x-alpha-pro-power", src="11SIX24 store (regular price)"),
    dict(b="11SIX24", m="Hurache-X Jelly Bean 2", p=169.99, c="foam", f="other", sh="e", mm="16", usap=None, x="11six24-hurache-jelly-bean-2", src="The Kitchen"),
    dict(b="11SIX24", m="Vapor Jelly Bean 2", p=169.99, c="foam", f="other", sh="h", mm="16", usap=None, src="Pickleball Effect"),
    dict(b="11SIX24", m="Ultre Jelly Bean 2", p=169.99, c="foam", f="other", sh="h", mm="16", usap=None, src="The Kitchen"),
    dict(b="11SIX24", m="Pegasus Jelly Bean 2", p=169.99, c="foam", f="other", sh="w", mm="16", usap=None, src="The Kitchen"),
    dict(b="CRBN", m="CRBN 3 TruFoam Waves", p=280, c="foam", f=None, sh="", mm="14", usap=None, src="Matt's Pickleball"),
    dict(b="Vatic Pro", m="Prism Flash 16mm", p=99.99, c=None, f=None, sh="", mm="16", usap=None, src="Pickleball Effect"),
    dict(b="Vatic Pro", m="V-Sol Power Flash 16mm", p=80, c=None, f=None, sh="e", mm="16", usap=None, src="Matt's Pickleball"),
    dict(b="Vatic Pro", m="V-Sol Tour Flash", p=109.99, c=None, f=None, sh="h", mm="16", usap=None, src="Pickleball Effect"),
    dict(b="Chorus", m="Coda 16mm", p=180, c=None, f=None, sh="", mm="16", usap=None, src="Matt's Pickleball"),
    dict(b="Chorus", m="Shapeshifter HX", p=139.99, c=None, f=None, sh="", mm="", usap=None, src="Pickleball Effect"),
    dict(b="Ronbus", m="Quanta R4 16mm", p=120, c=None, f=None, sh="h", mm="16", usap=None, src="Matt's Pickleball"),
    dict(b="Friday", m="Fever 16mm Standard", p=99, c=None, f=None, sh="w", mm="16", usap=None, src="Matt's Pickleball"),
    dict(b="Pickleball Apes", m="Zen S+", p=199, c=None, f=None, sh="", mm="", usap=None, src="Pickleball Effect"),
    dict(b="Bread & Butter", m="Loco 2", p=220, c="foam", f=None, sh="eh", mm="16", usap=None, spin="Bread & Butter Loco 2 Elongated", spec="bnb-loco", x="bread-butter-loco-2", crop="bread-butter-loco-2-elongated", src="The Kitchen"),
    dict(b="Facolos", m="Elite X (1st gen)", p=139.99, c="gen3", f=None, sh="e", mm="16", usap=None, x="facolos-elite-x", src="Matt's Pickleball"),
    dict(b="Selkirk", m="Boomstik ST (original Project Boomstik line)", p=None, skip=True),  # placeholder, never shown
]
RX_EXTRA = [r for r in RX_EXTRA if not r.get("skip")]

# Tested paddles (X-ray) not in the catalog get added from the X-ray data; price unknown unless listed here.
XRAY_PRICE = {}  # slug -> (US price, source)

# Catalog paddles that are in the Spin Lab but have no X-ray: (brand, catalog model) -> spin table name.
CAT_SPIN = {("Grit", "E1-CW Elongated"): "Grit E1 CW", ("Grit", "E1-TW Elongated"): "Grit E1 TW", ("Arronax", "Boost-1"): "Arronax Boost"}

# Brands Siva wants featured in the finder (2026-11-18). Codes come only from CODES in build.py;
# a brand here without a confirmed code shows no code until Siva confirms one.
CODE_BRANDS = ["Arronax", "Bread & Butter", "11SIX24", "Aireo", "RPM", "Holbrook", "Luzz", "PACT", "Speedup", "Pickle Poppers",
               "Evolv", "E6", "Grit", "Mehau", "Honolulu", "FLiK", "CPX", "Vanwin"]
_CB = {b.lower() for b in CODE_BRANDS}

# Never in the finder: unreleased, pre-release or pre-order-only paddles, and trainers.
EXCLUDE = [r"dynasty whip", r"aura pro tour", r"project bluejay", r"project cardinal", r"trainer|training|trickshot|champion 12mm|essentials dash"]

# ---------- countries ----------
# Chosen from DUPR's ranking of countries by players (The Dink, Oct 2024) plus the countries Siva named.
# local: brands with a store or strong presence in that country (small ranking nudge). strip: country picks shown above results.
COUNTRIES = [
    dict(k="us", n="United States", note="Prices are US list prices from each brand's own store. For tournaments, check that the paddle is USA Pickleball approved; we show approval where the brand lists it."),
    dict(k="ca", n="Canada", local=["GRUVN", "Combat", "Apollo", "NXTGEN", "BOOMA"], picks="canada",
         note="Prices below are US list prices. Shipping, duty and the exchange rate change what you pay in Canada, so check the brand ships to you. The Canadian picks come from reviewer Supasenpai."),
    dict(k="au", n="Australia", local=["PACT"], picks="au",
         note="PACT is an Australian brand and its prices are in Australian dollars from its own store. Other prices are US list prices; shipping and import costs change what you pay, so check the brand ships to Australia."),
    dict(k="uk", n="United Kingdom", note="We don't have UK store data yet, so prices are US list prices. Shipping, VAT and the exchange rate change what you pay."),
    dict(k="my", n="Malaysia", local=["Arronax"], picks="my",
         note="We don't have Malaysian store prices yet, so prices are US list prices. Arronax also sells through its own Malaysian store."),
    dict(k="vn", n="Vietnam", local=["Facolos", "Kamito", "Sypik", "Wika", "Zocker"], picks="vn",
         note="Vietnam has its own strong paddle scene. The local picks show prices in dong from a Vietnamese retailer; other prices are US list prices."),
    dict(k="ph", n="Philippines", note="We don't have Philippine store data yet, so prices are US list prices. Shipping and import costs change what you pay."),
    dict(k="es", n="Spain", local=["Zcebra"], picks="es",
         note="Zcebra is a Spanish brand and its prices are in euros from its own store. Other prices are US list prices."),
    dict(k="in", n="India", note="We don't have Indian store data yet, so prices are US list prices. Many international paddles are imported in India and cost more there."),
    dict(k="mx", n="Mexico", note="We don't have Mexican store data yet, so prices are US list prices."),
    dict(k="other", n="Somewhere else", note="Prices are US list prices. Check that the brand ships to your country and what import costs apply."),
]
COUNTRY_PICKS = {
    "canada": dict(title="Top Canadian paddles", by="Supasenpai's top 5 Canadian paddles. We haven't tested these.",
                   rows=[dict(b=b, m=m, n=n) for b, m, n, _ in CANADIAN_PICKS]),
    "au": dict(title="Australian brand: PACT", by="Prices in Australian dollars from PACT's own store. We've X-rayed the Teflon Evolve, one of our top picks.",
               rows=[]),  # filled from the catalog below
    "es": dict(title="Spanish brand: Zcebra", by="Prices in euros from Zcebra's own store. We've X-rayed and spin-tested the Gazelle.", rows=[]),
    "my": dict(title="Arronax", by="Arronax sells through its own Malaysian store as well as its US store. US prices shown; we've X-rayed the KVL-004, KVL-005 and Thunder.", rows=[]),
    "vn": dict(title="Popular in Vietnam", by="From pickleplay.vn's top Vietnam paddles list, prices in dong (checked Nov 18, 2026). We've X-rayed each of these models.",
               rows=[dict(b="Facolos", m="Elite X", lp="2,690,000 ₫", x="facolos-elite-x"), dict(b="Kamito", m="Alpha-X", lp="3,490,000 ₫", x="kamito-alpha-x"),
                     dict(b="Kamito", m="Dominus", lp="2,890,000 ₫", x="kamito-dominus"), dict(b="Sypik", m="Pro Tour Ultimate Triton 5", lp="3,950,000 ₫", x="sypik-triton-5"),
                     dict(b="Zocker", m="Aspire Signature x Phuc Huynh", lp="3,090,000 ₫", x="zocker-aspire")]),
}
COUNTRY_SRC = {"vn": ("pickleplay.vn", "https://pickleplay.vn/en/collections/top-vietnam-padlle")}


# ---------- helpers that read brand spec text ----------
def _shapes(s):
    s = (s or "").lower()
    out = ""
    if re.search(r"elongat|invikta|t-shape", s): out += "e"
    if re.search(r"hybrid|round top|flat top", s): out += "h"
    if re.search(r"wide|standard|square|\bmax\b|quad|epic", s): out += "w"
    return out


def _construction(core, tags=()):
    t = (core or "").lower()
    if re.search(r"full foam|no honeycomb|all-foam|gen ?4", t):
        return "foam"
    if "foam" in tags and "honeycomb" not in tags:
        return "foam"
    if "honeycomb" in tags or re.search(r"honeycomb|polypropylene|\bpp\b|polymer|nomex|polyethylene", t):
        return "gen3"
    if "foam" in tags or re.search(r"foam|\bepp\b|\bmpp|purefoam|boomcore|peba|eva", t):
        return "foam"
    return None


def _foam(core, tags=()):
    t = (core or "").upper()
    if "epp" in tags or re.search(r"\bEPP\b|XPOP|XOP", t): return "epp"
    if "mpp" in tags and "MPPE" not in t: return "mpp"
    if re.search(r"\bMPP(?!E)|MPP2|MPP-Z", t): return "mpp"
    if re.search(r"MPPE|EMA|PEBA|PUREFOAM|EVA|NANOCELLULAR|TPE|BOOMCORE", t): return "other"
    return None


def _dims_shape(s):
    """Elongated if the listed size is at least 16.4 in long and at most 7.6 in wide (the usual elongated cut)."""
    m = re.search(r"(1[5-7]\.\d+)\s*[\"″]?\s*[×x]\s*(\d\.\d+)", s or "")
    if m and float(m.group(1)) >= 16.4 and float(m.group(2)) <= 7.6:
        return "e"
    return ""


def _mm(s):
    return [int(round(float(v))) for v in re.findall(r"\d+(?:\.\d+)?", str(s or "")) if 9 <= float(v) <= 20]


_SPIN = {r["paddle"]: r for r in LABS["spin"] + LABS["spin_extra"]}
_SPIN_BY_X = {xs: _SPIN.get(sp) for xs, (g, sp) in LINKS.items() if sp}
_SPEC_BY_X = {}
for _sid, (_xs, _sp, _gr) in SPEC_LINKS.items():
    if _xs: _SPEC_BY_X[_xs] = _sid
_SPEC = {p["id"]: p for p in _RXSPEC}
# Pickleball RX picks: Leader Board, style lists and top picks, keyed by X-ray slug.
_RXPICK = {}
for _i, _r in enumerate(LEADERBOARD):
    if _r[2]: _RXPICK.setdefault(_r[2], []).append("Leader Board #%d" % (_i + 1))
for _k, _rows in STYLE_PICKS.items():
    for _r in _rows:
        if _r[2]: _RXPICK.setdefault(_r[2], []).append({"power": "power picks", "spin": "spin picks", "control": "control picks", "all-court": "all-court picks", "beginner": "beginner picks"}[_k])
for _k, _t, _d, _rows in TOP_PICKS:
    for _r in _rows:
        if _r[2]: _RXPICK.setdefault(_r[2], []).append("top picks (" + _t + ")")
# Leader Board wall-photo crops are named after the pick's brand + model (assets/paddles/<slug>.jpg).
_CROP = {}
for _r in list(LEADERBOARD) + [x for rows in STYLE_PICKS.values() for x in rows] + [x for t in TOP_PICKS for x in t[3]]:
    if _r[2]: _CROP.setdefault(_r[2], []).append(_slug(_r[0] + " " + _r[1]))
_PICK_TRAIT = {"power picks": "power", "spin picks": "spin", "control picks": "control", "all-court picks": "allcourt", "beginner picks": "beginner"}


def _excluded(name):
    n = name.lower()
    return any(re.search(p, n) for p in EXCLUDE)


def _rx_entry(brand, model, price, cur, core, shape_txt, mm_txt, approval, url, tested, extra=None):
    extra = extra or {}
    xs = extra.get("x") or (tested if tested and not tested.startswith("grit:") else None)
    xr = _XR.get(xs) if xs else None
    if xr and xr.get("unreleased"):
        return None
    tags = xr["tags"] if xr else ()
    core_txt = ((xr["core"] + " " + xr["thickness"]) if xr else "") or core or ""
    c = extra.get("c", "") if "c" in extra else None
    c = c if c else _construction(core_txt, tags)
    f = extra.get("f") if "f" in extra and extra.get("f") else (_foam(core_txt, tags) if c == "foam" else None)
    sh = extra.get("sh") if "sh" in extra else _shapes(shape_txt)
    if not sh and xr: sh = _shapes(xr.get("size", ""))
    if not sh and xr: sh = _dims_shape(xr.get("size", ""))
    if not sh: sh = _shapes(re.sub(r"(?i)gen ?\d|v\d", "", model).replace("Hyper ", "Widebody ").replace("Hyper", "Widebody") if brand == "Gearbox" else model)
    if not sh: sh = _FAMILY.get((brand, model.split()[0].lower()), "")
    if not c and re.search(r"(?i)gen[- ]?3|honeycomb", model): c = "gen3"
    if not c and re.search(r"(?i)foam", model): c = "foam"
    mm = _mm(mm_txt) or (_mm(xr["thickness"]) if xr else [])
    if model.lower().startswith(brand.lower() + " "): model = model[len(brand) + 1:]
    name = f"{brand} {model}"
    top, top_src = None, ""
    if "h" in sh:
        for b, rx, ts, src in TOP_STYLE:
            if b.lower() == brand.lower() and re.search(rx, model, re.I):
                top, top_src = ts, src
                break
    spin = _SPIN.get(extra.get("spin")) if extra.get("spin") else (_SPIN_BY_X.get(xs) if xs else None)
    if not spin: spin = _SPIN.get(CAT_SPIN.get((brand, model), ""))
    spec = _SPEC.get(extra.get("spec") or _SPEC_BY_X.get(xs or "", ""))
    revs = []
    for b, rx, k in REVIEWER_PICKS:
        if b.lower() == brand.lower() and re.search(rx, model, re.I) and k not in [r[0] for r in revs]:
            revs.append((k,))
    usap = extra.get("usap") if "usap" in extra else (None if not approval else ("usap" in approval.lower() and "not usap" not in approval.lower() and "pending" not in approval.lower()))
    if approval and re.search(r"not usap|not usa pickleball", approval, re.I): usap = False
    d = dict(b=brand, m=model, p=price, cur=cur or "", c=c, f=f, sh=sh, top=top, mm=mm, usap=usap, u=url or "")
    if top_src: d["ts"] = top_src
    if xs and xr: d["x"] = xs
    if tested and tested.startswith("grit:"): d["g"] = slugify(tested[5:])
    if spin: d["rpm"], d["rc"] = spin["avg"], spin["condition"]
    if spec:
        d["sw"], d["tw"] = spec["measured"]["swingWeight"], spec["measured"]["twistWeight"]
        d["sid"] = spec["id"]
    picks = _RXPICK.get(xs, []) if xs else []
    if picks: d["rx"] = picks
    if revs: d["rv"] = [r[0] for r in revs]
    if extra.get("src"): d["ps"] = extra["src"]
    if brand == "Grit" and model.startswith("E1"): d["warn"] = "Not USA Pickleball approved"
    elif approval and re.search(r"not usap|not usa", approval, re.I): d["warn"] = "Not USA Pickleball approved" if re.fullmatch(r"(?i)not usap approved", approval.strip()) else approval
    if xs == "cpx-hyper-plus": d["warn"] = "Currently delisted by USA Pickleball (Nov 2026)"
    d["slug"] = xs or slugify(name)
    ph = (product_photo(xs) if xs else "") or product_photo(slugify(name))
    for cand in [slugify(name)] + _CROP.get(xs, []) + ([extra["crop"]] if extra.get("crop") else []):
        if not ph and os.path.exists(os.path.join(OUT, f"assets/paddles/{cand}.jpg")): ph = f"assets/paddles/{cand}.jpg"
    if ph: d["ph"] = ph
    code = next((cc for cc in CODES if cc["brand"].lower() == brand.lower()), None)
    if code: d["code"] = code["offer"]
    if brand.lower() in _CB or code: d["cb"] = 1
    _traits(d)
    return d


def _traits(d):
    """Pickleball RX trait ratings, 0-10. Measured lab data beats brand specs; brand specs beat nothing."""
    sh, mm, c, f = d["sh"], d["mm"], d["c"], d["f"]
    thin = bool(mm) and min(mm) <= 14 and max(mm) <= 14
    thick = bool(mm) and min(mm) >= 16
    pw = 5.0 + (1.0 if c == "foam" else 0) + (0.5 if f == "epp" else 0) + (0.4 if c == "gen3" else 0) * 0
    pw += 1.0 if sh == "e" else (0.5 if "e" in sh else 0) + (0.3 if sh == "h" else 0)
    pw += 1.0 if thin else 0
    if "sw" in d: pw += max(-1.5, min(1.5, (d["sw"] - 115) * 0.2))
    ct = 5.0 + (1.2 if c == "gen3" else 0) + (0.4 if f == "mpp" else 0) + (0.8 if thick else 0) - (0.8 if thin else 0)
    ct += 1.0 if sh == "w" else (0.6 if sh == "h" else (-0.3 if sh == "e" else 0.3))
    if "sw" in d and d["sw"] < 114: ct += 0.6
    if "tw" in d and d["tw"] >= 6.25: ct += 0.5
    fg = 5.0 + (1.5 if "w" in sh else 0) + (0.8 if sh == "h" else 0) + (0.5 if thick else 0) + (0.5 if c == "gen3" else 0)
    if "tw" in d: fg += max(-1, min(1, (d["tw"] - 6.15) * 4))
    if "rpm" in d:
        sp = max(3.0, min(10.0, 4 + (d["rpm"] - 1600) / 1000 * 6))
    else:
        sp = 6.0
    for k in d.get("rv", []):
        t = SRC_TRAIT.get(k)
        if t == "spin": sp = max(sp, 7.8)
        if t == "power": pw += 0.8
        if t == "control": ct += 0.8
        if t == "allcourt": pw += 0.3; ct += 0.4
    for lab in d.get("rx", []):
        t = _PICK_TRAIT.get(lab)
        if t == "spin": sp += 0.6
        if t == "power": pw += 1.0
        if t == "control": ct += 1.0
        if t == "allcourt": pw += 0.4; ct += 0.4
        if t == "beginner": fg += 1.0
    cl = lambda v: round(max(0, min(10, v)), 1)
    d["t"] = [cl(pw), cl(sp), cl(ct), cl(fg)]  # power, spin, control/defense, forgiveness


# Shape family: if every listed paddle in a brand's model family (first word of the name) has the same shape,
# use it for family members whose listing leaves shape blank (e.g. JOOLA Perseus is elongated).
_fam = {}
for _b in _RXCAT["brands"]:
    for _p in _b["paddles"]:
        _s = _shapes(_p.get("shape"))
        if _s: _fam.setdefault((_b["brand"], _p["model"].split()[0].lower()), set()).add(_s)
_FAMILY = {k: next(iter(v)) for k, v in _fam.items() if len(v) == 1}

RX = []
_seen_x = set()
for _b in _RXCAT["brands"]:
    cur = _b.get("cur", "")
    if _b["brand"] == "PACT": cur = "A$"
    if _b["brand"] == "Zcebra": cur = "€"
    for _p in _b["paddles"]:
        name = f'{_b["brand"]} {_p["model"]}'
        if _excluded(name) or _excluded(_p.get("shape", "")):
            continue
        d = _rx_entry(_b["brand"], _p["model"], _p.get("price"), cur, _p.get("core"), _p.get("shape"), _p.get("mm"), _p.get("approval", ""), _p.get("url"), _p.get("tested"))
        if d:
            RX.append(d)
            if d.get("x"): _seen_x.add(d["x"])
for _r in RX_EXTRA:
    d = _rx_entry(_r["b"], _r["m"], _r.get("p"), "", "", "", _r.get("mm"), "", "", None, _r)
    if d:
        RX.append(d)
        if d.get("x") and d["x"] not in ("rpm-v2", "rpm-q2"): _seen_x.add(d["x"])
FINDER_SKIP = {"boomstik-clone-alibaba"}  # X-rayed for comparison only, not a paddle we recommend
for _x in XRAY:
    if _x["slug"] in _seen_x or _x["slug"] in FINDER_SKIP or _x.get("unreleased") or _excluded(_x["name"]):
        continue
    model = _x["name"][len(_x["brand"]):].strip() if _x["name"].startswith(_x["brand"]) else _x["name"]
    pr, ps = XRAY_PRICE.get(_x["slug"], (None, ""))
    d = _rx_entry(_x["brand"], model, pr, "", "", _x.get("size", ""), _x.get("thickness", ""), "", "", _x["slug"], {"x": _x["slug"], "src": ps} if ps else {"x": _x["slug"]})
    if d: RX.append(d)
# Local-currency prices aren't US prices: keep them for display, but budget matching treats them as unknown.
for d in RX:
    if d["cur"] and d["cur"] != "$":
        d["lp"] = f'{d["cur"]}{d["p"]:,.2f}'.replace(".00", "") if d["p"] is not None else ""
        d["p"] = None
    d.pop("cur", None)
    if d["b"] in ("Grit",):
        d["spot"] = "grit-pickleball.html"
    elif d["b"] in ("Evolv", "Gearbox"):
        d["spot"] = d["b"].lower() + "-pickleball.html"

# Country strips filled from the catalog.
for _k, _brand in (("au", "PACT"), ("es", "Zcebra"), ("my", "Arronax")):
    COUNTRY_PICKS[_k]["rows"] = [dict(b=d["b"], m=d["m"], lp=d.get("lp") or (f'${d["p"]:,.2f}'.replace(".00", "") if d.get("p") else ""), x=d.get("x", ""), u=d.get("u", ""))
                                 for d in RX if d["b"] == _brand][:8]

_RXDATA = dict(paddles=RX, countries=COUNTRIES, picks=COUNTRY_PICKS, src={k: list(v) for k, v in SRC.items()}, csrc={k: list(v) for k, v in COUNTRY_SRC.items()})
write("assets/rx-data.js", "window.RX = " + json.dumps(_RXDATA, ensure_ascii=False, separators=(",", ":")) + ";\n")
_n_rx = len(RX)
_n_tested = sum(1 for d in RX if d.get("x") or d.get("rpm") or d.get("sw"))
_n_rev = sum(1 for d in RX if d.get("rv"))
_n_top = sum(1 for d in RX if d.get("top"))
_n_h = sum(1 for d in RX if "h" in d["sh"])


def _q(name, legend, opts, hint="", hidden=False, first=0):
    o = "".join(f'<label><input type="radio" name="{name}" value="{v}"{" checked" if i == first else ""}><b>{l}</b><span>{dd}</span></label>' for i, (v, l, dd) in enumerate(opts))
    h = f'<p class="muted rx-hint">{hint}</p>' if hint else ""
    return f'<fieldset id="q-{name}"{" hidden" if hidden else ""}><legend>{legend}</legend>{h}<div class="options">{o}</div></fieldset>'


_country_opts = "".join(f'<option value="{c["k"]}">{e(c["n"])}</option>' for c in COUNTRIES)
_rv_names = sorted({v[0] for v in SRC.values()})

write("finder.html", page("Paddle finder: get your paddle Rx | PickleballRx", f'''
<div class="wrap"><section class="finder">
  <h1 class="page-title">Get your paddle Rx</h1>
  <p class="section-lead">Answer a few questions and our Rx algorithm ranks {_n_rx} paddles for you, using our own X-ray, spin and swing-weight testing where we have it.</p>
  <form class="rx-card" id="finder">
    <div class="rx-mark" aria-hidden="true">Rx</div>
    <fieldset id="q-country"><legend>1. Where do you play?</legend>
      <p class="muted rx-hint">Your country changes the local picks, price notes and which brands we nudge up.</p>
      <select name="country" id="rx-country" class="rx-select">{_country_opts}</select></fieldset>
    {_q("level", "2. How long have you been playing?", [("beginner", "Beginner", "Under a year, still learning"), ("intermediate", "Intermediate", "1 to 3 years, about 3.0 to 4.0"), ("advanced", "Advanced", "3+ years, 4.0 and up")])}
    {_q("budget", "3. What's your budget?", [("100", "Under $100", "Value picks"), ("200", "$100 to $200", "Most mid-range paddles"), ("300", "$200 to $300", "Premium paddles"), ("any", "Budget is no problem", "Show me the best")], "In US dollars. Paddles that cost less than your range still count, just ranked a little lower.")}
    {_q("build", "4. Core construction", [("gen3", "Gen 3", "Honeycomb core, usually with a foam perimeter"), ("foam", "Full foam", "Foam core, no honeycomb"), ("any", "Not sure", "Show both")], "", False, 2)}
    {_q("foam", "4b. Which foam?", [("epp", "EPP foam", "Tends to feel firmer and poppier"), ("mpp", "MPP foam", "Tends to feel softer, more dwell"), ("any", "Either one", "Any full foam")], "", True, 2)}
    {_q("shape", "5. Paddle shape", [("e", "Elongated", "More reach and power, smaller sweet spot"), ("h", "Hybrid", "In between"), ("w", "Standard / wide body", "Biggest sweet spot, fastest hands"), ("any", "Not sure", "Show all shapes")], "", False, 3)}
    {_q("top", "5b. Which hybrid?", [("flat", "Flat top hybrid", "Squarer head, more face up top"), ("round", "Round top hybrid", "Rounded head"), ("any", "Either one", "Any hybrid")], "Few brands say which top their hybrid has, so most hybrids are &ldquo;not confirmed&rdquo;. We show confirmed matches first.", True, 2)}
    <label class="rx-check"><input type="checkbox" name="codes" value="1"> Only show brands we partner with (discount code brands)</label>
    {_q("priority", "6. What matters most?", [("power", "Power", "Drives and put-aways"), ("spin", "Spin", "Topspin and slice"), ("control", "Defense", "Blocks, resets and dinks"), ("allcourt", "All-court control", "A bit of everything")])}
    <button class="btn" type="submit">Get my Rx</button>
  </form>
  <div id="finder-out" aria-live="polite" style="margin-top:24px"></div>

  <section id="how" class="rx-how">
    <h2>How our Rx algorithm works</h2>
    <p>Every paddle gets four ratings from 0 to 10: <b>power</b>, <b>spin</b>, <b>defense</b> (control and fast hands) and <b>forgiveness</b> (sweet spot). Where we've tested a paddle, our numbers win:</p>
    <ul>
      <li><b>Spin</b> comes from our <a href="spin.html">Spin Lab</a> average RPM when we've tested it. Otherwise it starts at 6 and rises if another reviewer ranks it highly for spin.</li>
      <li><b>Power</b> rises for full foam (a little more for EPP), elongated shapes, 14 mm cores and a higher measured swing weight from our <a href="specs.html">Spec Lab</a>.</li>
      <li><b>Defense</b> rises for Gen 3 honeycomb, 16 mm cores, wider shapes, a lighter measured swing weight and a higher twist weight.</li>
      <li><b>Forgiveness</b> rises for wide and hybrid shapes, 16 mm cores and a higher measured twist weight.</li>
      <li>Our own picks (the <a href="index.html#leaderboard">Leader Board</a> and <a href="best.html">top picks</a>) nudge the matching rating up.</li>
    </ul>
    <p>Then your answers turn into a match score out of 100:</p>
    <ul>
      <li><b>Up to 55 points</b> for your priority rating. All-court uses the average of power, spin and defense, minus a little for a lopsided paddle.</li>
      <li><b>Up to 20 points</b> for your level. Beginners get forgiveness and defense, intermediates get a balance, advanced players get power and spin.</li>
      <li><b>Up to 15 points</b> for evidence: our X-ray, Spin Lab or Spec Lab data, our own picks, and public picks from {", ".join(_rv_names[:-1])} and {_rv_names[-1]}.</li>
      <li><b>Up to 10 points</b> for fit: in your budget range, a confirmed hybrid top style, and brands with a local presence in your country.</li>
    </ul>
    <p>Budget, construction, foam type and shape are filters: a paddle has to match them to be ranked. If too few paddles match, we loosen the least important filter and tell you which one. Discount codes never change the ranking. Tick &ldquo;Only show brands we partner with&rdquo; to limit the list to our partner brands; where we have a code it shows on the paddle.</p>
    <p class="muted" style="font-size:.88rem">Specs and prices come from each brand's store (checked Nov 2026) and can change. Where a brand doesn't say the foam type or hybrid top style, we mark it unknown rather than guess. {_n_tested} of the {_n_rx} paddles have our own lab data; {_n_rev} appear on another reviewer's public list; {_n_top} of {_n_h} hybrids have a confirmed top style. Other reviewers' lists are credited and linked, not copied. <a href="disclaimers.html">Disclaimers</a>.</p>
  </section>
</section></div>
<script src="assets/rx-data.js?v={ASSET_V}"></script>
<script src="assets/rx.js?v={ASSET_V}"></script>''', 0, "finder", desc="Get your pickleball paddle Rx: answer a few questions on level, budget, core, shape and priority, and we rank paddles using our own lab testing.", crumbs=[("Paddle finder", None)]))
