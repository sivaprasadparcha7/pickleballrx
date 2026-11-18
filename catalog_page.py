# "All paddles" catalog: brand lineups read from each brand's own store.
# Run from build.py (uses its page/write/e/slugify/CODES). These paddles are NOT tested unless "tested" is set.
CAT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "catalog.json")))
_codes = {c["brand"]: c for c in CODES}


def _cat_lab(t):
    if not t:
        return '<span class="tag nt">Not tested</span>'
    if t.startswith("grit:"):
        return f'<a class="badge" href="grit.html#{slugify(t[5:])}">Tested: Grit Lab</a>'
    return f'<a class="badge" href="xray/{t}.html">Tested: X-ray</a>'


def _price(p):
    if p.get("price") is None:
        return '<td data-v="" class="muted">See store</td>'
    s = f'${p["price"]:,.2f}'.replace(".00", "")
    if p.get("was"):
        s += f' <s class="muted">${p["was"]:,.2f}</s>'.replace(".00", "")
    return f'<td data-v="{p["price"]}">{s}</td>'


_rows, _shapes, _cov = [], set(), []
for b in CAT["brands"]:
    c = _codes.get(b["brand"])
    code = f'<div class="muted" style="font-size:.8rem">Code PBRX, {e(c["offer"])}</div>' if c else ""
    for p in b["paddles"]:
        for s in (p.get("shape") or "").split(" / "):
            if s: _shapes.add(s)
        _rows.append(
            f'<tr data-b="{e(b["brand"])}" data-s="{e((p.get("shape") or "").lower())}" data-mm="{e(p.get("mm", ""))}" data-t="{1 if p.get("tested") else 0}">'
            f'<td>{e(b["brand"])}</td><th scope="row">{e(p["model"])}'
            + (f'<div class="muted" style="font-size:.8rem;font-weight:400">{e(p["note"])}</div>' if p.get("note") else "")
            + f'</th><td>{e(p.get("shape") or "")}</td><td>{e(p["mm"]) + " mm" if p.get("mm") else ""}</td>{_price(p)}'
            f'<td>{_cat_lab(p.get("tested"))}</td><td><a href="{e(b["store"])}" rel="noopener nofollow">{e(b["brand"])} store</a>{code}</td></tr>')
    if not b["complete"] or b.get("note"):
        _cov.append(f'<li><b>{e(b["brand"])}</b>: {e(b.get("note") or "Partial list.")}</li>')

_n = sum(len(b["paddles"]) for b in CAT["brands"])
_nt = sum(1 for b in CAT["brands"] for p in b["paddles"] if p.get("tested"))
_bopts = "".join(f'<option>{e(b["brand"])}</option>' for b in CAT["brands"] if b["paddles"])
_sopts = "".join(f'<option value="{e(s.lower())}">{e(s)}</option>' for s in sorted(_shapes))
_checked = CAT["checked"]

write("all-paddles.html", page("All pickleball paddles by brand | PickleballRx", f'''
<div class="wrap"><section>
  <h1 class="page-title">All paddles</h1>
  <p class="section-lead">{_n} paddles from {len(CAT["brands"])} brands, listed from each brand's own store. <b>Most of these we have not tested.</b> The ones we have tested ({_nt}) link to our lab results. For every other paddle, the shape, core thickness and price are what the brand lists, not our measurements, and we haven't rated it.</p>
  <p class="muted" style="font-size:.88rem">Prices checked {_checked} and change often, especially around sales. Blank cells mean the brand's store didn't state it. Want only lab-tested paddles with scores? Use the <a href="paddles.html">paddle database</a>.</p>
  <div class="filters" id="cat-filters">
    <label>Search<input type="search" id="c-q" placeholder="Paddle or brand"></label>
    <label>Brand<select id="c-b"><option value="">Any</option>{_bopts}</select></label>
    <label>Shape<select id="c-s"><option value="">Any</option>{_sopts}</select></label>
    <label>Core<select id="c-mm"><option value="">Any</option><option>12</option><option>12.7</option><option>13</option><option>14</option><option>14.3</option><option>15</option><option>16</option></select></label>
    <label>Max price ($)<input type="number" id="c-p" min="0" step="10" placeholder="Any"></label>
    <label class="check"><input type="checkbox" id="c-t"> Tested by us</label>
  </div>
  <p class="count" id="c-count"></p>
  <div class="table-wrap"><table class="db" id="cat">
    <thead><tr><th>Brand</th><th>Paddle</th><th>Shape</th><th>Core</th><th>Price</th><th>Our data</th><th>Buy</th></tr></thead>
    <tbody>{"".join(_rows)}</tbody>
  </table></div>
</section>
<section style="padding-top:0">
  <h2>About this list</h2>
  <ul class="section-lead">{"".join(_cov)}</ul>
  <p class="muted" style="font-size:.85rem">Brand specs and prices are as listed by each brand. Discount codes may earn us a commission; see <a href="disclaimers.html">Disclaimers</a>.</p>
</section></div>
<style>.tag.nt{{background:#eef1f6;color:#4a5876;border-radius:999px;padding:2px 9px;font-size:.75rem;font-weight:600}} #cat th[scope=row]{{white-space:normal;min-width:180px;text-transform:none;letter-spacing:0;font-size:.9rem;color:var(--ink);background:none}}</style>
<script>
(function(){{
  var $=function(i){{return document.getElementById(i)}}, rows=[].slice.call(document.querySelectorAll('#cat tbody tr'));
  function go(){{
    var q=$('c-q').value.toLowerCase().trim(), b=$('c-b').value, s=$('c-s').value, mm=$('c-mm').value, p=parseFloat($('c-p').value), t=$('c-t').checked, n=0;
    rows.forEach(function(r){{
      var pr=parseFloat(r.children[4].getAttribute('data-v')), ok=(!q||r.textContent.toLowerCase().indexOf(q)>=0)&&(!b||r.dataset.b===b)
        &&(!s||r.dataset.s.split(' / ').indexOf(s)>=0)&&(!mm||r.dataset.mm.split(' / ').indexOf(mm)>=0)&&(isNaN(p)||(!isNaN(pr)&&pr<=p))&&(!t||r.dataset.t==='1');
      r.hidden=!ok; if(ok)n++;
    }});
    $('c-count').textContent=n+' of '+rows.length+' paddles';
  }}
  ['c-q','c-b','c-s','c-mm','c-p','c-t'].forEach(function(i){{$(i).addEventListener('input',go);$(i).addEventListener('change',go)}});
  var u=new URLSearchParams(location.search); if(u.get('brand')){{$('c-b').value=u.get('brand')}}
  go();
}})();
</script>''', 0, "paddles", desc="Every current paddle from 26 brands, from JOOLA and Selkirk to Grit and Gearbox, with brand-listed shape, core and price. Clearly marked: most are not tested by Pickleball Rx."))
