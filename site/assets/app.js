(function () {
  var P = window.PADDLES || [];
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  /* ---------- mobile menu ---------- */
  var tog = $('.nav-toggle'), navEl = $('#site-nav');
  if (tog && navEl) tog.addEventListener('click', function () {
    var open = navEl.classList.toggle('open');
    tog.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  P.forEach(function (p) { p.overall = Math.round((p.power + p.spin + p.control + p.forgiveness) / 4 * 10) / 10; });
  var bar = function (v) { return '<span class="cell-bar"><i style="width:' + v * 10 + '%"></i></span>'; };

  /* ---------- database ---------- */
  var db = $('#db');
  if (db) {
    var tbody = $('tbody', db), sortKey = 'overall', dir = -1;
    var uniq = function (k) { return P.map(function (p) { return p[k]; }).filter(function (v, i, a) { return a.indexOf(v) === i; }).sort(); };
    uniq('shape').forEach(function (v) { $('#f-shape').insertAdjacentHTML('beforeend', '<option>' + esc(v) + '</option>'); });
    uniq('core_mm').forEach(function (v) { $('#f-core').insertAdjacentHTML('beforeend', '<option value="' + v + '">' + v + ' mm</option>'); });
    var params = new URLSearchParams(location.search);
    if (params.get('style')) $('#f-style').value = params.get('style');
    var render = function () {
      var q = $('#f-q').value.toLowerCase(), st = $('#f-style').value, sh = $('#f-shape').value, co = $('#f-core').value,
        pr = parseFloat($('#f-price').value), xr = $('#f-xray').checked, vi = $('#f-video').checked;
      var rows = P.filter(function (p) {
        return (!q || (p.name + ' ' + p.brand).toLowerCase().indexOf(q) > -1) && (!st || p.style === st) && (!sh || p.shape === sh) &&
          (!co || String(p.core_mm) === co) && (isNaN(pr) || p.price <= pr) && (!xr || p.xray) && (!vi || p.video);
      }).sort(function (a, b) { var x = a[sortKey], y = b[sortKey]; return (x > y ? 1 : x < y ? -1 : 0) * dir; });
      tbody.innerHTML = rows.map(function (p) {
        var ex = [p.xray ? 'X-ray' : '', p.micro ? 'Micro' : '', p.video ? 'Video' : ''].filter(Boolean).map(function (t) { return '<span class="badge">' + t + '</span>'; }).join(' ');
        return '<tr><td><a href="reviews/' + p.slug + '.html">' + esc(p.name) + '</a><br><span class="muted" style="font-size:.8rem">' + esc(p.brand) + '</span></td>' +
          '<td class="num"><b>' + p.overall + '</b></td>' +
          ['power', 'spin', 'control', 'forgiveness'].map(function (k) { return '<td class="num">' + p[k] + bar(p[k]) + '</td>'; }).join('') +
          '<td class="num">' + p.swing_weight + '</td><td class="num">' + p.twist_weight + '</td><td class="num">' + p.weight_oz + ' oz</td>' +
          '<td class="num">' + p.core_mm + ' mm</td><td>' + esc(p.shape) + '</td><td class="num">$' + p.price + '</td><td>' + (ex || '<span class="muted">&ndash;</span>') + '</td></tr>';
      }).join('') || '<tr><td colspan="13" class="muted">No paddles match those filters.</td></tr>';
      $('#db-count').textContent = rows.length + ' of ' + P.length + ' paddles';
      $$('th[data-k]', db).forEach(function (th) {
        if (th.dataset.k === sortKey) th.setAttribute('aria-sort', dir > 0 ? 'ascending' : 'descending'); else th.removeAttribute('aria-sort');
      });
    };
    $$('th[data-k] button', db).forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.parentNode.dataset.k;
        if (k === sortKey) dir = -dir; else { sortKey = k; dir = (k === 'name' || k === 'price' || k === 'shape') ? 1 : -1; }
        render();
      });
    });
    $$('#db-filters input, #db-filters select').forEach(function (el) { el.addEventListener('input', render); });
    render();
  }

  /* ---------- compare ---------- */
  var cmp = $('#cmp');
  if (cmp) {
    var pick = (new URLSearchParams(location.search).get('p') || '').split(',').filter(Boolean);
    if (!pick.length) pick = P.slice(0, 2).map(function (p) { return p.slug; });
    var pickers = $('#cmp-pickers');
    for (var i = 0; i < 4; i++) {
      var opts = '<option value="">' + (i < 2 ? 'Choose a paddle' : 'Add a paddle (optional)') + '</option>' +
        P.map(function (p) { return '<option value="' + p.slug + '">' + esc(p.name) + '</option>'; }).join('');
      pickers.insertAdjacentHTML('beforeend', '<label><span class="muted" style="font-size:.85rem">Paddle ' + (i + 1) + '</span><select data-i="' + i + '">' + opts + '</select></label>');
    }
    var sels = $$('select', pickers);
    sels.forEach(function (s, i) { s.value = pick[i] || ''; s.addEventListener('change', draw); });
    var ROWS = [
      ['Scores'], ['overall', 'Overall', 1], ['power', 'Power', 1], ['spin', 'Spin', 1], ['control', 'Control', 1], ['forgiveness', 'Forgiveness', 1],
      ['Measured specs'], ['swing_weight', 'Swing weight', 0], ['twist_weight', 'Twist weight', 1], ['weight_oz', 'Weight (oz)', 0], ['core_mm', 'Core (mm)', 0],
      ['length_in', 'Length (in)', 0], ['width_in', 'Width (in)', 0], ['grip_in', 'Grip length (in)', 0], ['shape', 'Shape'], ['face', 'Face'],
      ['Buying'], ['price', 'Price ($)', -1], ['level', 'Best for']
    ];
    function draw() {
      var chosen = sels.map(function (s) { return P.find(function (p) { return p.slug === s.value; }); }).filter(Boolean);
      history.replaceState(null, '', '?p=' + chosen.map(function (p) { return p.slug; }).join(','));
      if (!chosen.length) { cmp.innerHTML = '<tbody><tr><td class="muted">Choose at least one paddle.</td></tr></tbody>'; return; }
      var h = '<thead><tr><th></th>' + chosen.map(function (p) { return '<th><a href="reviews/' + p.slug + '.html">' + esc(p.name) + '</a></th>'; }).join('') + '</tr></thead><tbody>';
      ROWS.forEach(function (r) {
        if (r.length === 1) { h += '<tr class="group"><th colspan="' + (chosen.length + 1) + '">' + r[0] + '</th></tr>'; return; }
        var vals = chosen.map(function (p) { return p[r[0]]; }), best = null;
        if (r[2] === 1 && chosen.length > 1) best = Math.max.apply(null, vals);
        if (r[2] === -1 && chosen.length > 1) best = Math.min.apply(null, vals);
        h += '<tr><th>' + r[1] + '</th>' + vals.map(function (v) {
          var cell = typeof v === 'number' && r[2] === 1 && r[0] !== 'twist_weight' ? v + bar(v) : esc(v);
          return '<td' + (best !== null && v === best ? ' class="best"' : '') + '>' + cell + '</td>';
        }).join('') + '</tr>';
      });
      cmp.innerHTML = h + '</tbody>';
    }
    draw();
  }

  /* finder: see rx.js */

  /* ---------- X-Ray Rx filter ---------- */
  var xg = $('#x-grid');
  if (xg) {
    var tag = '';
    var xr = function () {
      var q = $('#x-q').value.toLowerCase(), n = 0;
      $$('.xcard', xg).forEach(function (c) {
        var show = (!tag || (' ' + c.dataset.tags + ' ').indexOf(' ' + tag + ' ') > -1) && (!q || c.dataset.name.indexOf(q) > -1);
        c.hidden = !show; if (show) n++;
      });
      $('#x-count').textContent = n + ' paddles';
    };
    $$('#x-chips button').forEach(function (b) {
      b.addEventListener('click', function () {
        tag = b.dataset.t;
        $$('#x-chips button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
        xr();
      });
    });
    $('#x-q').addEventListener('input', xr);
    xr();
  }
})();

/* ---------- generic sortable tables ---------- */
(function () {
  document.querySelectorAll('table.sortable').forEach(function (t) {
    var ths = Array.prototype.slice.call(t.querySelectorAll('thead th'));
    ths.forEach(function (th, i) {
      var b = th.querySelector('button'); if (!b) return;
      b.addEventListener('click', function () {
        var dir = th.getAttribute('aria-sort') === 'descending' ? 1 : -1;
        if (!th.hasAttribute('aria-sort') && i === 0) dir = 1;
        ths.forEach(function (x) { x.removeAttribute('aria-sort'); });
        th.setAttribute('aria-sort', dir > 0 ? 'ascending' : 'descending');
        var tb = t.tBodies[0], rows = Array.prototype.slice.call(tb.rows);
        rows.sort(function (a, b) {
          var x = a.cells[i].dataset.v || a.cells[i].textContent.trim(), y = b.cells[i].dataset.v || b.cells[i].textContent.trim();
          var nx = parseFloat(x), ny = parseFloat(y);
          if (!isNaN(nx) && !isNaN(ny)) return (nx - ny) * dir;
          return x.localeCompare(y) * dir;
        });
        rows.forEach(function (r) { tb.appendChild(r); });
      });
    });
  });
})();

/* ---------- YouTube: tap thumbnail to play ---------- */
(function () {
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a.video.yt[data-yt]');
    if (!a || ev.ctrlKey || ev.metaKey || ev.shiftKey) return;
    ev.preventDefault();
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(a.dataset.yt) + '?autoplay=1&rel=0';
    f.title = a.getAttribute('aria-label') || 'YouTube video';
    f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
    f.allowFullscreen = true;
    var d = document.createElement('div'); d.className = a.className.replace(' yt', ''); d.appendChild(f);
    a.parentNode.replaceChild(d, a);
  });
})();
