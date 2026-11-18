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
 "flik-f1": ("flik-f1", "FLiK F1 Elongated", "FLiK"),
 "nox-jc6-16mm": ("nox-x-foam-jc6", "NOX X-Foam JC6 16mm", "NOX"),
 "nox-jma": ("nox-x-foam-jma", "NOX X-Foam JMA 16mm", "NOX"),
 "sypik-avatar-pro": ("sypik-avatar-pro", "Sypik Avatar Pro", "Sypik"),
 "wika-air-1": ("wika-qd-air", "Wika QD Air (Air 1) 16mm", "Wika"),
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
UNRELEASED = {"franklin-dynasty-whip-16mm"}


def tags(x):
    core = (x["core"] + " " + x["cell_size"]).lower()
    t = []
    c, cs = x["core"].lower(), x["cell_size"].lower().strip()
    hc = ("honeycomb" in c and "no honeycomb" not in c) or cs.startswith("honeycomb,") or "listed" in cs or "narrow cell" in cs or (cs.startswith("≈") and "×" not in cs)
    if hc: t.append("honeycomb")
    if "foam" in x["core"].lower() and not hc: t.append("foam")
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
                    specs=x["specs"], sources=x["specs_sources"], tags=tags(x), reel=REELS.get(slug, ""), unreleased=slug in UNRELEASED))
out.sort(key=lambda p: p["name"].lower())
json.dump({"paddles": out}, open(os.path.join(D, "xray.json"), "w"), indent=1, ensure_ascii=False)
print(len(out), "paddles")
for p in out: print(p["slug"], p["tags"])
