# Paddle database (paddles.html): every paddle from the brands we follow, grouped by brand.
# Specs and prices are what each brand (or a retailer) lists, not our measurements.
# Paddles we've tested carry "tested" and link to our lab results.
# Run from build.py (uses its page/write/e/slugify/CODES).
CAT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "catalog.json")))
_codes = {c["brand"]: c for c in CODES}


def _cat_lab(t):
    if not t:
        return ""
    if t.startswith("grit:"):
        return f'<a class="badge" href="grit.html#{slugify(t[5:])}">Tested by us: Grit Lab</a>'
    return f'<a class="badge" href="xray/{t}.html">Tested by us: X-ray</a>'


def _price(p):
    if p.get("price") is None:
        return '<td data-v="" class="muted">See store</td>'
    c = p.get("cur", "$")
    s = f'{c}{p["price"]:,.2f}'.replace(".00", "")
    if p.get("was"):
        s += f' <s class="muted">{c}{p["was"]:,.2f}</s>'.replace(".00", "")
    return f'<td data-v="{p["price"]}">{s}</td>'


def _approval(p):
    n = p.get("note", "")
    if "approved" in n.lower():
        return n
    return p.get("approval", "")


_rows, _shapes, _cov, _chips = [], set(), [], []
for b in CAT["brands"]:
    if not b["paddles"]:
        continue
    bid = "brand-" + slugify(b["brand"])
    c = _codes.get(b["brand"])
    code = f' &middot; <span class="code-tag">Code PBRX, {e(c["offer"])}</span>' if c else ""
    _chips.append(f'<a class="chip" href="#{bid}">{e(b["brand"])}</a>')
    _rows.append(f'<tr class="brand-row" id="{bid}" data-b="{e(b["brand"])}"><th colspan="11">{e(b["brand"])} <span class="muted" style="font-weight:400">&middot; {len(b["paddles"])} paddles &middot; <a href="{e(b["store"])}" rel="noopener nofollow">{e(b["brand"])} store</a>{code}</span></th></tr>')
    for p in b["paddles"]:
        for s in (p.get("shape") or "").split(" / "):
            if s: _shapes.add(s)
        name = e(p["model"])
        if p.get("url"):
            name = f'<a href="{e(p["url"])}" rel="noopener nofollow">{name}</a>'
        note = p.get("note", "")
        note = "" if "approved" in note.lower() else note
        _rows.append(
            f'<tr data-b="{e(b["brand"])}" data-s="{e((p.get("shape") or "").lower())}" data-mm="{e(p.get("mm", ""))}" data-t="{1 if p.get("tested") else 0}">'
            f'<th scope="row">{name}' + (f'<div class="muted" style="font-size:.8rem;font-weight:400">{e(note)}</div>' if note else "") + '</th>'
            f'<td>{e(p.get("shape") or "")}</td><td>{e(p["mm"]) + " mm" if p.get("mm") else ""}</td><td>{e(p.get("weight", ""))}</td>'
            f'<td class="wrap">{e(p.get("core", ""))}</td><td class="wrap">{e(p.get("face", ""))}</td><td>{e(p.get("size", ""))}</td>'
            f'<td>{e(p.get("handle", ""))}</td><td>{e(_approval(p))}</td>{_price(p)}<td>{_cat_lab(p.get("tested"))}</td></tr>')
    if not b["complete"] or b.get("note"):
        _cov.append(f'<li><b>{e(b["brand"])}</b>: {e(b.get("note") or "Partial list.")}</li>')

_n = sum(len(b["paddles"]) for b in CAT["brands"])
_nb = sum(1 for b in CAT["brands"] if b["paddles"])
_nt = sum(1 for b in CAT["brands"] for p in b["paddles"] if p.get("tested"))
_bopts = "".join(f'<option>{e(b["brand"])}</option>' for b in CAT["brands"] if b["paddles"])
_sopts = "".join(f'<option value="{e(s.lower())}">{e(s)}</option>' for s in sorted(_shapes))
_checked = CAT["checked"]

write("paddles.html", page("Paddle database: every paddle by brand | PickleballRx", f'''
<div class="wrap"><section>
  <h1 class="page-title">Paddle database</h1>
  <p class="section-lead">{_n} paddles from {_nb} brands, with the key specs each brand lists. Tap a paddle's name to open its page on the brand's website. The {_nt} paddles marked <b>Tested by us</b> link to our X-ray and Grit Lab results.</p>
  <p class="muted" style="font-size:.88rem">Specs and prices as listed by the brand, checked {_checked}. Prices change often, especially around sales. Blank cells mean the brand didn't state it.</p>
  <nav class="chips" aria-label="Jump to a brand">{"".join(_chips)}</nav>
  <div class="filters" id="cat-filters">
    <label>Search<input type="search" id="c-q" placeholder="Paddle or brand"></label>
    <label>Brand<select id="c-b"><option value="">Any</option>{_bopts}</select></label>
    <label>Shape<select id="c-s"><option value="">Any</option>{_sopts}</select></label>
    <label>Core<select id="c-mm"><option value="">Any</option><option>10</option><option>12</option><option>12.7</option><option>13</option><option>14</option><option>14.3</option><option>15</option><option>16</option></select></label>
    <label>Max price ($)<input type="number" id="c-p" min="0" step="10" placeholder="Any"></label>
    <label class="check"><input type="checkbox" id="c-t"> Tested by us</label>
  </div>
  <p class="count" id="c-count"></p>
  <div class="table-wrap"><table class="db" id="cat">
    <thead><tr><th>Paddle</th><th>Shape</th><th>Thickness</th><th>Weight</th><th>Core</th><th>Face</th><th>Size (L x W)</th><th>Handle</th><th>Approval</th><th>Price</th><th>Our data</th></tr></thead>
    <tbody>{"".join(_rows)}</tbody>
  </table></div>
</section>
<section style="padding-top:0">
  <h2>About this database</h2>
  <ul class="section-lead">{"".join(_cov)}</ul>
  <p class="muted" style="font-size:.85rem">Specs and prices are as listed by the brand or retailer, not our measurements. Discount codes may earn us a commission; see <a href="disclaimers.html">Disclaimers</a>.</p>
</section></div>
<style>
#cat th[scope=row]{{white-space:normal;min-width:170px;text-transform:none;letter-spacing:0;font-size:.9rem;color:var(--ink);background:none}}
#cat td.wrap{{white-space:normal;min-width:150px}}
#cat tr.brand-row th{{background:var(--navy,#112240);color:#fff;font-size:.95rem;text-transform:none;letter-spacing:0;padding:12px}}
#cat tr.brand-row a{{color:#fcb92d}} #cat tr.brand-row .muted{{color:#c8d1e6}}
.chips{{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 16px}}
.chips .chip{{font-size:.82rem;padding:4px 10px;border:1px solid var(--line);border-radius:999px;text-decoration:none;color:var(--ink);background:var(--surface)}}
.code-tag{{color:#fcb92d}}
</style>
<script>
(function(){{
  var $=function(i){{return document.getElementById(i)}}, all=[].slice.call(document.querySelectorAll('#cat tbody tr'));
  var rows=all.filter(function(r){{return !r.classList.contains('brand-row')}}), heads=all.filter(function(r){{return r.classList.contains('brand-row')}});
  function go(){{
    var q=$('c-q').value.toLowerCase().trim(), b=$('c-b').value, s=$('c-s').value, mm=$('c-mm').value, p=parseFloat($('c-p').value), t=$('c-t').checked, n=0, seen={{}};
    rows.forEach(function(r){{
      var pr=parseFloat(r.querySelector('td[data-v]').getAttribute('data-v')), txt=(r.dataset.b+' '+r.textContent).toLowerCase();
      var ok=(!q||txt.indexOf(q)>=0)&&(!b||r.dataset.b===b)&&(!s||r.dataset.s.split(' / ').indexOf(s)>=0)
        &&(!mm||r.dataset.mm.split(' / ').indexOf(mm)>=0)&&(isNaN(p)||(!isNaN(pr)&&pr<=p))&&(!t||r.dataset.t==='1');
      r.hidden=!ok; if(ok){{n++;seen[r.dataset.b]=1}}
    }});
    heads.forEach(function(h){{h.hidden=!seen[h.dataset.b]}});
    $('c-count').textContent=n+' of '+rows.length+' paddles';
  }}
  ['c-q','c-b','c-s','c-mm','c-p','c-t'].forEach(function(i){{$(i).addEventListener('input',go);$(i).addEventListener('change',go)}});
  var u=new URLSearchParams(location.search); if(u.get('brand')){{$('c-b').value=u.get('brand')}}
  go();
}})();
</script>''', 0, "paddles", desc=f"Pickleball paddle database: {_n} paddles from {_nb} brands, with brand-listed shape, thickness, weight, core, face, size and price, plus links to our lab results."))

write("all-paddles.html", '<!doctype html><meta charset="utf-8"><title>Paddle database | PickleballRx</title><meta http-equiv="refresh" content="0; url=paddles.html"><link rel="canonical" href="https://pickleballrx.org/paddles.html"><a href="paddles.html">Paddle database</a>')
