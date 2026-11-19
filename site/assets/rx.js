/* Pickleball RX paddle finder: the Rx algorithm. Data comes from rx-data.js (built by rx_page.py). */
(function () {
  var R = window.RX, form = document.getElementById('finder');
  if (!R || !form) return;
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var money = function (v) { return '$' + (Math.round(v * 100) / 100).toLocaleString('en-US', { minimumFractionDigits: v % 1 ? 2 : 0, maximumFractionDigits: 2 }); };
  var SHAPE = { e: 'Elongated', h: 'Hybrid', w: 'Standard / wide body' };
  var PRI = { power: 'power', spin: 'spin', control: 'defense', allcourt: 'all-court control' };
  var BANDS = { '100': [0, 100], '200': [100, 200], '300': [200, 300], any: null };
  var COUNTRY = {}; R.countries.forEach(function (c) { COUNTRY[c.k] = c; });

  /* Show the follow-up questions only when they apply. */
  var sync = function () {
    var f = new FormData(form);
    $('#q-foam').hidden = f.get('build') !== 'foam';
    $('#q-top').hidden = f.get('shape') !== 'h';
  };
  form.addEventListener('change', sync);
  try { var saved = localStorage.getItem('rx-country'); if (saved && COUNTRY[saved]) $('#rx-country').value = saved; } catch (e) {}
  sync();

  var priRating = function (t, pri) {
    if (pri === 'power') return t[0];
    if (pri === 'spin') return t[1];
    if (pri === 'control') return t[2];
    var m = (t[0] + t[1] + t[2]) / 3, spread = Math.max(t[0], t[1], t[2]) - Math.min(t[0], t[1], t[2]);
    return Math.max(0, m - 0.25 * spread);
  };

  var passes = function (p, a, relax) {
    if (a.codes && !p.cb) return false;
    var band = BANDS[a.budget];
    if (band && (p.p == null || p.p > band[1] + 1)) return false;
    if (a.build !== 'any' && !relax.build && p.c !== a.build) return false;
    if (a.build === 'foam' && a.foam !== 'any' && !relax.foam && p.f !== a.foam) return false;
    if (a.shape !== 'any' && !relax.shape && p.sh.indexOf(a.shape) < 0) return false;
    if (a.shape === 'h' && a.top !== 'any' && !relax.top && p.top && p.top !== a.top) return false;
    return true;
  };

  var score = function (p, a, local) {
    var t = p.t, pri = priRating(t, a.priority);
    var s1 = pri * 5.5;
    var lv;
    if (a.level === 'beginner') {
      lv = (t[3] * 0.6 + t[2] * 0.4) * 2;
      if (p.p != null && p.p > 200) lv -= 3;
      if (p.sh === 'e' && p.mm.length && Math.max.apply(null, p.mm) <= 14) lv -= 3;
    } else if (a.level === 'intermediate') lv = (t[0] + t[1] + t[2] + t[3]) / 4 * 2;
    else lv = (t[0] + t[1]) / 2 * 2;
    var ev = (p.x ? 4 : 0) + (p.rpm ? 4 : 0) + (p.sw ? 2 : 0) + (p.rx ? 4 : 0) + Math.min(6, (p.rv || []).length * 2);
    ev = Math.min(15, ev);
    var band = BANDS[a.budget], fit = 0;
    if (band) fit += p.p >= band[0] ? 6 : 2; else fit += p.p != null ? 6 : 3;
    if (a.shape === 'h' && a.top !== 'any' && p.top === a.top) fit += 2;
    if (local) fit += 2;
    return Math.max(0, Math.min(100, Math.round(s1 + Math.max(0, lv) + ev + Math.min(10, fit))));
  };

  var srcLink = function (k) { var s = R.src[k]; return s ? '<a href="' + esc(s[1]) + '" target="_blank" rel="noopener">' + esc(s[0]) + '</a>' : ''; };
  var build = function (p) {
    if (p.c === 'gen3') return 'Gen 3 honeycomb';
    if (p.c === 'foam') return p.f === 'epp' ? 'EPP full foam' : p.f === 'mpp' ? 'MPP full foam' : p.f === 'other' ? 'Full foam (other foam)' : 'Full foam (foam type not listed)';
    return 'Core type not listed';
  };

  var reasons = function (p, a) {
    var r = [], t = p.t;
    var pr = Math.round(priRating(t, a.priority) * 10) / 10;
    if (p.rpm && (a.priority === 'spin' || a.priority === 'allcourt')) r.push('Averaged <b>' + p.rpm.toLocaleString('en-US') + ' RPM</b> in our <a href="spin.html">Spin Lab</a> (' + esc(p.rc === 'New' || p.rc === 'Brand new' ? 'tested new' : p.rc) + ').');
    r.push('Rx rating for ' + PRI[a.priority] + ': <b>' + pr + '/10</b>.');
    if (p.rx) r.push('On Pickleball RX\'s ' + esc(p.rx.slice(0, 2).join(' and ')) + '.');
    if (p.rv) {
      var seen = {}, names = [];
      p.rv.forEach(function (k) { var s = R.src[k]; if (s && !seen[s[0]]) { seen[s[0]] = 1; names.push(srcLink(k)); } });
      r.push('Also picked or reviewed by ' + names.join(', ') + '.');
    }
    if (p.rpm && r.length < 4 && a.priority !== 'spin' && a.priority !== 'allcourt') r.push('Averaged ' + p.rpm.toLocaleString('en-US') + ' RPM in our <a href="spin.html">Spin Lab</a>.');
    if (p.sw && r.length < 4) r.push('We measured swing weight ' + p.sw + ' and twist weight ' + p.tw + ' in our <a href="specs.html">Spec Lab</a>' + (a.priority === 'control' ? (p.sw < 115 ? ', light enough for quick hands.' : '.') : (p.sw >= 118 ? ', heavy enough to plow through drives.' : '.')));
    if (p.x && r.length < 4) r.push('We X-rayed this model: ' + esc(build(p)) + ' core.');
    if (r.length < 3) {
      if (a.priority === 'power' && p.sh === 'e') r.push('Elongated shape for extra reach and leverage.');
      else if (a.priority === 'control' && p.sh.indexOf('w') > -1) r.push('Wider face for a bigger sweet spot at the kitchen.');
      else if (p.c === 'foam' && a.priority === 'power') r.push('Full foam core, which tends to add pop.');
      else if (p.c === 'gen3' && a.priority === 'control') r.push('Gen 3 honeycomb core, which tends to feel more controlled.');
    }
    if (r.length < 3 && !p.x && !p.rpm && !p.sw) r.push('We haven\'t tested this one yet, so its ratings come from brand specs' + (p.rv ? ' and other reviewers\' lists.' : '.'));
    return r.slice(0, 4);
  };

  var card = function (p, i, a, s) {
    var initials = p.b.split(/\s+/).map(function (w) { return w[0]; }).join('').slice(0, 3);
    var img = p.ph ? '<img class="rx-thumb" src="' + esc(p.ph) + '" alt="' + esc(p.b + ' ' + p.m) + '" loading="lazy">' : '<div class="rx-thumb rx-ph" aria-hidden="true">' + esc(initials) + '</div>';
    var chips = [];
    chips.push(p.sh ? p.sh.split('').map(function (c) { return SHAPE[c]; }).join(', ') : 'Shape not listed');
    if (p.sh.indexOf('h') > -1) chips.push(p.top ? (p.top === 'flat' ? 'Flat top' : 'Round top') : 'Top style not confirmed');
    chips.push(build(p));
    if (p.mm.length) chips.push(p.mm.join(' / ') + ' mm');
    if (p.usap === true) chips.push('USAP approved');
    var links = [];
    if (p.x) links.push('<a class="badge" href="xray/' + esc(p.x) + '.html">X-ray</a>');
    if (p.rpm) links.push('<a class="badge" href="spin.html">' + p.rpm.toLocaleString('en-US') + ' RPM</a>');
    if (p.g) links.push('<a class="badge" href="grit.html#' + esc(p.g) + '">Grit</a>');
    if (p.sid) links.push('<a class="badge" href="specs.html#' + esc(p.sid) + '">Specs</a>');
    if (p.spot) links.push('<a class="badge" href="' + esc(p.spot) + '">Brand spotlight</a>');
    if (p.u) links.push('<a class="badge" href="' + esc(p.u) + '" target="_blank" rel="noopener nofollow">' + esc(p.b) + ' store</a>');
    var price = p.p != null ? money(p.p) : (p.lp ? esc(p.lp) : 'Price not confirmed');
    return '<article class="rx-result' + (i === 0 ? ' rx-first' : '') + '"><div class="rx-rank">' + (i + 1) + '</div>' + img +
      '<div class="rx-body"><div class="muted rx-brand">' + esc(p.b) + '</div><h3>' + esc(p.m) + '</h3>' +
      '<div class="rx-price">' + price + (p.p != null ? ' <span class="muted">US list price</span>' : '') + '</div>' +
      '<div class="rx-chips">' + chips.map(function (c) { return '<span>' + esc(c) + '</span>'; }).join('') + '</div>' +
      (p.warn ? '<div class="rx-warn">' + esc(p.warn) + '</div>' : '') +
      '<h4>Why this paddle</h4><ul class="rx-why">' + reasons(p, a).map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul>' +
      '<div class="badges">' + links.join('') + '</div>' +
      (p.code ? '<div class="rx-code"><span class="code-tag">Code PBRX</span> ' + (p.code === 'PBRX' ? 'at ' + esc(p.b) : esc(p.code) + ' at ' + esc(p.b) + ' &middot; <a href="codes.html">All codes</a>') + '</div>' : '') +
      '</div><div class="rx-score"><b>' + s + '</b><span>Rx score</span></div></article>';
  };

  var strip = function (c) {
    var k = c.picks, pk = k && R.picks[k];
    if (!pk || !pk.rows.length) return '';
    var src = R.csrc[c.k];
    return '<section class="rx-local"><h3>' + esc(pk.title) + '</h3><p class="muted">' + esc(pk.by) + (src ? ' Source: <a href="' + esc(src[1]) + '" target="_blank" rel="noopener">' + esc(src[0]) + '</a>.' : '') + '</p><ul>' +
      pk.rows.map(function (r) {
        var name = esc(r.b) + ' ' + esc(r.m);
        if (r.x) name = '<a href="xray/' + esc(r.x) + '.html">' + name + '</a>';
        else if (r.u) name = '<a href="' + esc(r.u) + '" target="_blank" rel="noopener nofollow">' + name + '</a>';
        return '<li>' + name + (r.lp ? ' <span class="muted">&middot; ' + esc(r.lp) + '</span>' : '') + (r.n ? '<div class="muted" style="font-size:.82rem">' + esc(r.n) + '</div>' : '') + '</li>';
      }).join('') + '</ul></section>';
  };

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var f = new FormData(form), a = {};
    ['country', 'level', 'budget', 'build', 'foam', 'shape', 'top', 'priority'].forEach(function (k) { a[k] = f.get(k) || 'any'; });
    a.codes = f.get('codes') === '1';
    try { localStorage.setItem('rx-country', a.country); } catch (e) {}
    var c = COUNTRY[a.country] || COUNTRY.other, local = {};
    (c.local || []).forEach(function (b) { local[b.toLowerCase()] = 1; });
    var relax = {}, steps = [['foam', 'foam type'], ['build', 'core construction'], ['shape', 'shape']], notes = [];
    var pool = R.paddles.filter(function (p) { return passes(p, a, relax); });
    for (var i = 0; pool.length < 3 && i < steps.length; i++) {
      var k = steps[i][0];
      if ((k === 'foam' && (a.build !== 'foam' || a.foam === 'any')) || (k === 'build' && a.build === 'any') || (k === 'shape' && a.shape === 'any')) continue;
      relax[k] = true; notes.push(steps[i][1]);
      pool = R.paddles.filter(function (p) { return passes(p, a, relax); });
    }
    var ranked = pool.map(function (p) { return { p: p, s: score(p, a, local[p.b.toLowerCase()]) }; })
      .sort(function (x, y) { return y.s - x.s || (x.p.p || 999) - (y.p.p || 999); });
    if (a.shape === 'h' && a.top !== 'any') ranked.sort(function (x, y) { return (y.p.top === a.top) - (x.p.top === a.top) || y.s - x.s; });
    var top = ranked.slice(0, 6);
    var unconfirmed = top.filter(function (r) { return r.p.sh.indexOf('h') > -1 && !r.p.top; }).length;
    var out = '<h2>Your paddle Rx</h2><p class="section-lead">' + pool.length + ' of ' + R.paddles.length + ' paddles fit your answers. Here are the best ' + top.length + ' by Rx score.</p>';
    if (notes.length) out += '<div class="note rx-note">Only a few paddles matched everything, so we loosened the ' + notes.join(' and ') + ' filter' + (notes.length > 1 ? 's' : '') + '.</div>';
    if (a.shape === 'h' && a.top !== 'any' && unconfirmed) out += '<div class="note rx-note">' + unconfirmed + ' of these hybrids don\'t have a confirmed top style yet, so check the brand\'s photos before you buy. Confirmed ' + a.top + '-top hybrids are listed first.</div>';
    if (!top.length) out += '<div class="note rx-note">No paddles in our database match that budget yet. Try the next budget up.</div>';
    out += '<div class="rx-results">' + top.map(function (r, i) { return card(r.p, i, a, r.s); }).join('') + '</div>';
    out += '<div class="note rx-note"><strong>' + esc(c.n) + '.</strong> ' + esc(c.note) + '</div>' + strip(c);
    out += '<p class="muted" style="font-size:.85rem;margin-top:14px">Rx score is out of 100. <a href="#how">How our Rx algorithm works</a>. Discount codes never change the ranking.</p>';
    var o = $('#finder-out');
    o.innerHTML = out;
    o.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
})();
