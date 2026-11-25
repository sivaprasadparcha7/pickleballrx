# Builds xray.json for the X-Ray Rx pages from xray-labeled.json (Siva's labeled X-ray spec panels).
# Run: python3 data/xray.py && python3 build.py
import json, os
D = os.path.dirname(os.path.abspath(__file__))
SRC = json.load(open(os.path.join(D, "xray-labeled.json")))

# MARK unMARKed 2026 has two X-rays. Siva picked v2 (2026-11-17).
MARK_VERSION = "mark-unmarked-2026-v2-labeled.png"

# file stem -> (site slug, display name, brand)
NAMES = {
 "11six24-hurache-jelly-bean-2": ("11six24-hurache-jelly-bean-2", "11SIX24 Hurache-X Jelly Bean 2", "11SIX24"),
 "arronax-kvl-005": ("arronax-kvl-005", "Arronax KVL-005", "Arronax"),
 "cpx-hyper-plus": ("cpx-hyper-plus", "CPX Hyper+", "CPX"),
 "crush-covert": ("crush-covert", "Crush Covert Gen 4", "Crush"),
 "e6-ignis": ("e6-ignis", "E6 Ignis 16mm", "E6"),
 "evolv-origin": ("evolv-origin", "Evolv Origin", "Evolv"),
 "facolos-elite-x": ("facolos-elite-x", "Facolos Elite X (1st gen)", "Facolos"),
 "facolos-elite-x-v2": ("facolos-elite-x-2-0", "Facolos Elite X 2.0", "Facolos"),
 "facolos-nexx": ("facolos-nexx", "Facolos Nexx 16mm", "Facolos"),
 "franklin-dynasty-whip-16mm": ("franklin-dynasty-whip-16mm", "Franklin Dynasty Whip 16mm", "Franklin"),
 "friday-aura-pro-tour": ("friday-aura-pro-tour", "Friday Aura Pro Tour", "Friday"),
 "gearbox-pressure-x-8e": ("gearbox-pressure-x-8e", "Gearbox Pressure X 8E", "Gearbox"),
 "gearbox-pressure-xm": ("gearbox-pressure-xm", "Gearbox Pressure X 8M", "Gearbox"),
 "grit-e2-cf": ("grit-e2-cf", "Grit E2-CF", "Grit"),
 "holbrook-fuze": ("holbrook-fuze", "Holbrook Fuze", "Holbrook"),
 "honolulu-j6-cr": ("honolulu-j6cr", "Honolulu J6CR", "Honolulu"),
 "kamito-alpha-x": ("kamito-alpha-x", "Kamito Alpha-X", "Kamito"),
 "kamito-dominus": ("kamito-dominus", "Kamito Dominus", "Kamito"),
 "lining-hyper-power-90s": ("li-ning-hyper-power-90s", "Li-Ning HyperPower 90S", "Li-Ning"),
 "luzz-cannon-xpp": ("luzz-cannon-xpp", "Luzz Cannon XPP", "Luzz"),
 "luzz-glider-2026": ("luzz-glider-2026", "Luzz Glider 2026", "Luzz"),
 "luzz-inferno-2-m1": ("luzz-inferno-2", "Luzz Inferno 2 M1", "Luzz"),
 "luzz-inferno": ("luzz-inferno", "Luzz Inferno (Pro 4)", "Luzz"),
 "mark-02r2": ("mark-02r2", "MARK 02R2 (twoR2) 16mm", "MARK"),
 "mark-02r3": ("mark-02r3", "MARK 02R3 (twoR3)", "MARK"),
 "mark-unmarked-2026-v2": ("mark-unmarked-2026", "MARK unMARKed 2026", "MARK"),
 "mehau-e4": ("mehau-e4", "Mehau E4", "Mehau"),
 "mehau-e5": ("mehau-e5", "Mehau E5", "Mehau"),
 "mehau-s5": ("mehau-s5", "Mehau S5 Airpoom", "Mehau"),
 "pact-teflon": ("pact-teflon", "PACT Teflon Evolve Te16", "PACT"),
 "pakle-fuse": ("pakle-fuse", "Pakle Fuse", "Pakle"),
 "pakle-infinity": ("pakle-infinity", "Pakle Infinity", "Pakle"),
 "pickle-poppers-pop-n-rush": ("pickle-poppers-pop-n-rush", "Pickle Poppers Pop N Rush", "Pickle Poppers"),
 "pickle-poppers-pop-n-treasure": ("pickle-poppers-pop-n-treasure", "Pickle Poppers Pop N Treasure", "Pickle Poppers"),
 "pisgah-ridge": ("pisgah-ridge", "Pisgah Ridge", "Pisgah"),
 "proton-peacock": ("proton-project-peacock", "Proton Project Peacock", "Proton"),
 "proton-project-coyote": ("proton-project-coyote", "Proton Project Coyote", "Proton"),
 "rpm-jade": ("rpm-jade", "RPM Jade", "RPM"),
 "rpm-q2": ("rpm-q2", "RPM Q2 Elongated", "RPM"),
 "rpm-v2": ("rpm-v2", "RPM V2 (Friction Pro V2)", "RPM"),
 "spartus-spitfire": ("spartus-spitfire", "Spartus Spitfire", "Spartus"),
 "speedup-tide-elongated": ("speedup-tide", "Speedup Tide Elongated (14L)", "Speedup"),
 "standout-cf4": ("standout-cf4", "Standout CF4 Absolute Black", "Standout"),
 "sypik-triton-5": ("sypik-triton-5", "Sypik Triton 5", "Sypik"),
 "vanwin-alpha-control": ("vanwin-alpha-control", "Vanwin Alpha Control", "Vanwin"),
 "vanwin-alpha-power": ("vanwin-alpha-power", "Vanwin Alpha Power", "Vanwin"),
 "zcebra-gazelle": ("zcebra-gazelle", "Zcebra Gazelle", "Zcebra"),
 "zocker-aspire": ("zocker-aspire", "Zocker Aspire", "Zocker"),
 "11six24-hurache-alpha-power-2": ("11six24-hurache-x-alpha-pro-power", "11SIX24 Hurache-X Alpha Pro Power", "11SIX24"),
 "arronax-kvl-004": ("arronax-kvl-004", "Arronax KVL-004", "Arronax"),
 "arronax-thunder-gen1": ("arronax-thunder-gen-1", "Arronax Thunder (Gen 1)", "Arronax"),
 "bread-and-butter-loco-1": ("bread-butter-loco-1", "Bread & Butter LOCO 1", "Bread & Butter"),
 "bread-and-butter-loco-2": ("bread-butter-loco-2", "Bread & Butter LOCO 2", "Bread & Butter"),
 "reload-rld1": ("reload-rld1-16mm", "Reload RLD-1 16mm", "Reload"),
 "flik-f1": ("flik-f1", "FLiK F1 Elongated", "FLiK"),
 "nox-jc6-16mm": ("nox-x-foam-jc6", "NOX X-Foam JC6 16mm", "NOX"),
 "nox-jma": ("nox-x-foam-jma", "NOX X-Foam JMA 16mm", "NOX"),
 "sypik-avatar-pro": ("sypik-avatar-pro", "Sypik Avatar Pro", "Sypik"),
 "wika-air-1": ("wika-qd-air", "Wika QD Air (Air 1) 16mm", "Wika"),
 "aireo-cyclone": ("aireo-cyclone", "Aireo Cyclone 16mm", "Aireo"),
 "arronax-boost": ("arronax-boost-1", "Arronax Boost-1", "Arronax"),
 "gearbox-gx2": ("gearbox-gx2", "Gearbox GX2 Power", "Gearbox"),
 "joola-perseus-3s": ("joola-perseus-3s", "JOOLA Perseus 3S", "JOOLA"),
 "joola-perseus-v": ("joola-perseus-pro-v", "JOOLA Perseus Pro V", "JOOLA"),
 "joola-scorpeus-iv": ("joola-scorpeus-pro-iv", "JOOLA Scorpeus Pro IV", "JOOLA"),
 "li-ning-hyperpower-90s-gen3": ("li-ning-hyperpower-90s-gen-3", "Li-Ning HyperPower 90S Gen 3", "Li-Ning"),
 "luzz-cannon": ("luzz-cannon", "Luzz Pro Cannon (original)", "Luzz"),
 "mehau-x4": ("mehau-x4", "Mehau X4 Power Series", "Mehau"),
 "mehau-x5": ("mehau-x5", "Mehau X5 Power Series", "Mehau"),
 "soxter-impact-pro": ("soxter-impact-pro", "Soxter Impact Pro 3.0 16mm", "Soxter"),
 "wika-bao-fire-2": ("wika-bao-fire-evolution-2", "Wika Bao Fire Evolution 2 16mm", "Wika"),
 "wika-next-x": ("wika-next-x", "Wika Next-X 16mm", "Wika"),
 "wika-predator": ("wika-predator", "Wika Predator 16mm", "Wika"),
 "wika-qd-fire-2": ("wika-qd-fire-2", "Wika QD Fire 2", "Wika"),
 "friday-aura-pro": ("friday-aura-pro", "Friday Aura Pro", "Friday"),
 "joola-perseus-iv": ("joola-perseus-pro-iv", "JOOLA Perseus Pro IV 16mm", "JOOLA"),
 "nordic-dots": ("nordic-dots", "Nordic Dots Pro Series SE", "Nordic"),
 "pakle-evo-1": ("pakle-evolution-01", "Pakle Evolution 01 (Evo-1)", "Pakle"),
 "selkirk-boomstik": ("selkirk-labs-project-boomstik", "Selkirk LABS Project Boomstik", "Selkirk"),
 "boomstick-clone-alibaba": ("boomstik-clone-alibaba", "Boomstik clone (Alibaba)", "Unbranded"),
 "arronax-boost-1-luminous": ("arronax-boost-1-luminous", "Arronax Boost-1 Luminous", "Arronax"),
 "rpm-v2-ella-oh-14mm": ("rpm-v2-ella-oh-14mm", "RPM V2 Ella Oh 14mm (Friction Pro V2)", "RPM"),
 "volair-cmd-hybrid": ("volair-cmd-hybrid", "Volair CMD Hybrid 16mm", "Volair"),
}

REELS = {
 "honolulu-j6cr": "Ep 02: Honolulu J6CR (floating core, notched frame)",
 "spartus-spitfire": "Ep 03: Spartus Spitfire",
 "pickle-poppers-pop-n-rush": "Ep 04: Pop N Rush vs Pop N Treasure",
 "pickle-poppers-pop-n-treasure": "Ep 04: Pop N Rush vs Pop N Treasure",
 "rpm-jade": "Ep 05: The most hyped pickleball paddle of 2026. What's inside?",
 "facolos-elite-x-2-0": "Ep 06: Facolos Elite X 2.0 vs Gen 1",
 "gearbox-pressure-x-8e": "Gearbox Pressure X 8E reel",
 "pact-teflon": "PACT Teflon Evolve review, and PACT vs Gen 3 comparison",
}
UNRELEASED = set()


# Core filters go by what fills the CENTRE of the face, not the ring or edge foam around it
# (Siva 2026-11-25). A honeycomb centre is "honeycomb" even with an EVA/EPP perimeter, and the
# foam-type tags (EPP, MPP, floating, voids) only describe a foam centre.
# Per-paddle calls made from the X-ray where the text alone would mislead:
CENTER = {
 "pickle-poppers-pop-n-rush": "foam",      # MPPE foam centre; the 7.4 mm honeycomb is only in the handle
 "pickle-poppers-pop-n-treasure": "foam",  # MPP foam centre; honeycomb only in the handle
 "soxter-impact-pro": "foam",              # X-ray face reads full foam (retailers list PP honeycomb)
 "wika-predator": "honeycomb",             # honeycomb star fills the centre, EPP foam around it
 "wika-qd-fire-2": "honeycomb",            # 6 mm honeycomb centre wrapped in EPP
 "gearbox-gx2": "carbon",                  # SST 2.0 carbon ribs, not honeycomb (Siva 2026-11-25)
 "gearbox-pressure-x-8e": "foam",          # carbon ribs inside foam: counts as foam (Siva 2026-11-25)
 "gearbox-pressure-xm": "foam",
 "li-ning-hyper-power-90s": "honeycomb",   # cells too fine to see; honeycomb per Siva 2026-11-25
}


def center(x, slug):
    if slug in CENTER:
        return CENTER[slug]
    c, cs = x["core"].lower(), x["cell_size"].lower().strip()
    if "handle only" in cs or cs.startswith(("none", "n/a", "no honeycomb")):
        return "foam"
    hc = ("honeycomb" in c and "no honeycomb" not in c) or "listed" in cs or "narrow cell" in cs or (cs.startswith("≈") and "×" not in cs)
    return "honeycomb" if hc else "foam"


def tags(x, slug):
    c = center(x, slug)
    if c in ("honeycomb", "carbon"):
        return [c]
    core = (x["core"] + " " + x["cell_size"]).lower()
    t = ["foam"]
    if "epp" in core: t.append("epp")
    if "mpp" in core: t.append("mpp")
    if "floating" in core: t.append("floating")
    if "void" in core: t.append("voids")
    return t


out = []
for x in SRC:
    stem = x["file"].replace("-labeled.png", "")
    if stem.startswith("mark-unmarked-2026") and x["file"] != MARK_VERSION:
        continue
    slug, name, brand = NAMES[stem]
    out.append(dict(slug=slug, name=name, brand=brand, image=x["file"], core=x["core"], cell_size=x["cell_size"],
                    ring=x["perimeter_ring"], thickness=x["thickness"], face=x["face"], weight=x["weight"], size=x["size"],
                    specs=x["specs"], sources=x["specs_sources"], tags=tags(x, slug), reel=REELS.get(slug, ""), unreleased=slug in UNRELEASED))
out.sort(key=lambda p: p["name"].lower())
json.dump({"paddles": out}, open(os.path.join(D, "xray.json"), "w"), indent=1, ensure_ascii=False)
print(len(out), "paddles")
for p in out: print(p["slug"], p["tags"])
