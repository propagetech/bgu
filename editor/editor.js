/* Logo editor. Vanilla JS, no build step, no network calls beyond fetching the
 * two artwork files that sit next to this script. */
(function () {
  'use strict';

  var ART_PATH = 'art/';
  var VB = 3762;                       // the artwork is a square this many units wide

  /* ---------- colourways ----------
   * Presets carry the approved ramps verbatim. The five pickers below them are a
   * friendlier model: touch one and the ramps are derived from the seed colours
   * instead, which is close to the presets but not bit-identical to them.
   */
  var PRESETS = [
    { id: 'cherry-gold', label: 'Cherry & gold',
      ring: [[0, '#E8C86B'], [45, '#D4AF37'], [75, '#C2922E'], [92, '#C41E3A'], [100, '#A31530']],
      disc: [[0, '#FDF7E4'], [60, '#F8EAC0'], [100, '#F1DC9E']],
      ink: '#6B0F1E', accent: '#C41E3A',
      seed: { sun: '#D4AF37', edge: '#C41E3A', disc: '#F8EAC0' } },
    { id: 'reversed', label: 'Reversed',
      ring: [[0, '#A81528'], [46, '#C41E3A'], [78, '#9E1229'], [100, '#6B0F1E']],
      disc: [[0, '#8E1024'], [62, '#7E0B21'], [100, '#6B0F1E']],
      ink: '#E8C25A', accent: '#F2DFA8',
      seed: { sun: '#C41E3A', edge: '#6B0F1E', disc: '#7E0B21' } },
    { id: 'original', label: 'Original',
      ring: [[0, '#F9C742'], [46, '#F7B01E'], [78, '#F5910E'], [100, '#EE7A05']],
      disc: [[0, '#FCE58A'], [62, '#F8D452'], [100, '#F3C233']],
      ink: '#141414', accent: '#8E1420',
      seed: { sun: '#F7B01E', edge: '#EE7A05', disc: '#F8D452' } },
    { id: 'mono-gold', label: 'Mono gold',
      ring: [[0, '#EBD9A4'], [45, '#DCC077'], [75, '#C9A44E'], [100, '#B88C33']],
      disc: [[0, '#FBF3DC'], [60, '#F5E9C4'], [100, '#EEDDA8']],
      ink: '#A9822B', accent: '#C39A3A',
      seed: { sun: '#DCC077', edge: '#B88C33', disc: '#F5E9C4' } },
    { id: 'mono-cherry', label: 'Mono cherry',
      ring: [[0, '#E9A7B2'], [45, '#D9808F'], [75, '#C4566A'], [100, '#A83549']],
      disc: [[0, '#FBEAED'], [60, '#F6D7DD'], [100, '#EFC0C9']],
      ink: '#A81528', accent: '#C41E3A',
      seed: { sun: '#D9808F', edge: '#A83549', disc: '#F6D7DD' } },
    { id: 'mono-black', label: 'Mono black',
      ring: [[0, '#D8D8D8'], [45, '#B8B8B8'], [75, '#8E8E8E'], [100, '#6E6E6E']],
      disc: [[0, '#F4F4F4'], [60, '#E6E6E6'], [100, '#D6D6D6']],
      ink: '#141414', accent: '#3A3A3A',
      seed: { sun: '#B8B8B8', edge: '#6E6E6E', disc: '#E6E6E6' } },
    { id: 'rose-gold', label: 'Rose gold',
      ring: [[0, '#F2A6A6'], [45, '#E77B7B'], [75, '#D9534F'], [100, '#C0392B']],
      disc: [[0, '#FADBD8'], [60, '#F5B7B1'], [100, '#F1948A']],
      ink: '#7B241C', accent: '#C0392B',
      seed: { sun: '#E77B7B', edge: '#C0392B', disc: '#F5B7B1' } }
  ];

  var BOARDS = [
    { id: 'square', label: 'Square 1080', w: 1080, h: 1080, unit: 'px' },
    { id: 'post', label: 'Instagram post 4:5', w: 1080, h: 1350, unit: 'px' },
    { id: 'story', label: 'Story 9:16', w: 1080, h: 1920, unit: 'px' },
    { id: 'dp', label: 'Profile picture 640', w: 640, h: 640, unit: 'px' },
    { id: 'cover', label: 'Facebook cover', w: 1640, h: 624, unit: 'px' },
    { id: 'a4p', label: 'A4 portrait', w: 210, h: 297, unit: 'mm' },
    { id: 'a4l', label: 'A4 landscape', w: 297, h: 210, unit: 'mm' },
    { id: 'a3p', label: 'A3 poster', w: 297, h: 420, unit: 'mm' },
    { id: 'card', label: 'Business card', w: 90, h: 54, unit: 'mm' },
    { id: 'custom', label: 'Custom', w: 1080, h: 1080, unit: 'px' }
  ];

  var state = {
    lockup: 'english',
    crown: 'center',
    scheme: 'cherry-gold',
    custom: null,
    bg: 'transparent',
    board: 'square',
    customW: 1080,
    customH: 1080,
    size: 0.78,
    cx: 0.5,
    cy: 0.5
  };

  var art = null;                    // the live <svg> in the artboard
  var cache = {};
  var el = {};

  /* ---------- colour helpers ---------- */

  function hexToRgb(hex) {
    var h = String(hex).replace('#', '');
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    var n = parseInt(h, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }

  function rgbToHex(r, g, b) {
    return '#' + [r, g, b].map(function (v) {
      return ('0' + Math.round(Math.min(255, Math.max(0, v))).toString(16)).slice(-2);
    }).join('').toUpperCase();
  }

  function toHsl(hex) {
    var c = hexToRgb(hex).map(function (v) { return v / 255; });
    var max = Math.max.apply(null, c), min = Math.min.apply(null, c);
    var l = (max + min) / 2, h = 0, s = 0;
    if (max !== min) {
      var d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      if (max === c[0]) h = ((c[1] - c[2]) / d + (c[1] < c[2] ? 6 : 0));
      else if (max === c[1]) h = (c[2] - c[0]) / d + 2;
      else h = (c[0] - c[1]) / d + 4;
      h /= 6;
    }
    return { h: h, s: s, l: l };
  }

  function fromHsl(o) {
    var h = o.h, s = o.s, l = Math.min(1, Math.max(0, o.l));
    if (s === 0) return rgbToHex(l * 255, l * 255, l * 255);
    var q = l < 0.5 ? l * (1 + s) : l + s - l * s, p = 2 * l - q;
    function ch(t) {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    }
    return rgbToHex(ch(h + 1 / 3) * 255, ch(h) * 255, ch(h - 1 / 3) * 255);
  }

  function shift(hex, dl) {
    var c = toHsl(hex);
    c.l += dl;
    return fromHsl(c);
  }

  function preset(id) {
    return PRESETS.filter(function (p) { return p.id === id; })[0] || PRESETS[0];
  }

  // the ramps currently in force, whether from a preset or derived from the pickers
  function scheme() {
    var p = preset(state.scheme);
    if (!state.custom) return p;
    var c = state.custom;
    return {
      id: 'custom',
      ring: [[0, shift(c.sun, 0.09)], [45, c.sun], [75, shift(c.sun, -0.07)],
             [92, c.edge], [100, shift(c.edge, -0.09)]],
      disc: [[0, shift(c.disc, 0.05)], [60, c.disc], [100, shift(c.disc, -0.07)]],
      ink: c.ink,
      accent: c.accent
    };
  }

  /* ---------- artwork ---------- */

  function loadArt(lockup) {
    if (cache[lockup]) return Promise.resolve(cache[lockup]);
    return fetch(ART_PATH + lockup + '.svg').then(function (r) {
      if (!r.ok) throw new Error(r.status + ' ' + r.statusText);
      return r.text();
    }).then(function (txt) {
      var doc = new DOMParser().parseFromString(txt, 'image/svg+xml');
      if (doc.querySelector('parsererror')) throw new Error('artwork could not be parsed');
      cache[lockup] = doc.documentElement;
      return cache[lockup];
    });
  }

  function setStops(grad, stops) {
    if (!grad) return;
    while (grad.firstChild) grad.removeChild(grad.firstChild);
    stops.forEach(function (s) {
      var node = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
      node.setAttribute('offset', s[0] + '%');
      node.setAttribute('stop-color', s[1]);
      grad.appendChild(node);
    });
  }

  function paint() {
    if (!art) return;
    var s = scheme();
    setStops(art.querySelector('#ringG'), s.ring);
    setStops(art.querySelector('#headG'), s.disc);
    var fills = { ink: s.ink, text: s.accent, 'crown-side': s.ink, 'crown-center': s.accent };
    Object.keys(fills).forEach(function (id) {
      var g = art.querySelector('#' + id);
      if (g) g.setAttribute('fill', fills[id]);
    });
    ['crown-side', 'crown-center'].forEach(function (id) {
      var g = art.querySelector('#' + id);
      if (!g) return;
      var on = state.crown === 'all' || (state.crown === 'center' && id === 'crown-center');
      if (on) g.removeAttribute('display');
      else g.setAttribute('display', 'none');
    });
  }

  /* ---------- geometry ---------- */

  function board() {
    var b = BOARDS.filter(function (x) { return x.id === state.board; })[0];
    if (b.id !== 'custom') return b;
    return { id: 'custom', label: b.label, w: state.customW, h: state.customH, unit: 'px' };
  }

  function boardPx(b) {
    return b.unit === 'mm'
      ? { w: b.w / 25.4 * 96, h: b.h / 25.4 * 96 }
      : { w: b.w, h: b.h };
  }

  function boardPt(b) {
    return b.unit === 'mm'
      ? { w: b.w * 72 / 25.4, h: b.h * 72 / 25.4 }
      : { w: b.w * 0.75, h: b.h * 0.75 };
  }

  // the artwork box inside a board of the given size, in that size's units
  function artBox(w, h) {
    var side = state.size * Math.min(w, h);
    return { x: state.cx * w - side / 2, y: state.cy * h - side / 2, size: side };
  }

  function pngChoices(b) {
    var out;
    if (b.unit === 'mm') {
      out = [150, 300, 600].map(function (d) {
        return { w: Math.round(b.w / 25.4 * d), h: Math.round(b.h / 25.4 * d), note: d + ' dpi' };
      });
    } else {
      out = [1, 2, 3].map(function (m) {
        return { w: Math.round(b.w * m), h: Math.round(b.h * m), note: m + 'x' };
      });
    }
    return out.filter(function (o) { return o.w * o.h <= 40e6; });
  }

  /* ---------- rendering the stage ---------- */

  function layout() {
    if (!art) return;
    var b = board(), px = boardPx(b);
    var frame = el.frame.clientWidth - 64;
    var tall = Math.max(260, Math.min(window.innerHeight * 0.62, 680));
    var k = Math.min(frame / px.w, tall / px.h);
    var dw = px.w * k, dh = px.h * k;

    el.artboard.style.width = dw + 'px';
    el.artboard.style.height = dh + 'px';
    el.artboard.dataset.transparent = state.bg === 'transparent' ? 'true' : 'false';
    el.artboard.style.background = state.bg === 'transparent' ? '' : state.bg;

    var box = artBox(dw, dh);
    art.style.left = box.x + 'px';
    art.style.top = box.y + 'px';
    art.style.width = box.size + 'px';
    art.style.height = box.size + 'px';

    el.dims.textContent = b.w + ' x ' + b.h + ' ' + b.unit +
      (b.unit === 'mm' ? '  (' + Math.round(px.w) + ' x ' + Math.round(px.h) + ' px at 96 dpi)' : '');
    el.schemeName.textContent = state.custom ? 'Custom colours' : preset(state.scheme).label;
  }

  /* ---------- export ---------- */

  function serialise(w, h) {
    var ser = new XMLSerializer();
    var clone = art.cloneNode(true);
    Array.prototype.slice.call(clone.querySelectorAll('[display="none"]')).forEach(function (n) {
      n.parentNode.removeChild(n);
    });
    var inner = Array.prototype.map.call(clone.childNodes, function (n) {
      return ser.serializeToString(n);
    }).join('');
    var box = artBox(w, h);
    var s = box.size / VB;
    var bg = state.bg === 'transparent' ? ''
      : '<rect x="0" y="0" width="' + w + '" height="' + h + '" fill="' + state.bg + '"/>';
    return '<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h +
      '" viewBox="0 0 ' + w + ' ' + h + '">' + bg +
      '<g transform="translate(' + box.x.toFixed(2) + ',' + box.y.toFixed(2) +
      ') scale(' + s.toFixed(6) + ')">' + inner + '</g></svg>';
  }

  function filename(ext) {
    var b = board();
    return ['bellanduru-ganesha-utsava', state.lockup,
            state.custom ? 'custom' : state.scheme, b.id].join('-') + '.' + ext;
  }

  function save(blob, name) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
  }

  function status(msg, tone) {
    el.status.textContent = msg || '';
    if (tone) el.status.setAttribute('data-tone', tone);
    else el.status.removeAttribute('data-tone');
  }

  function exportSvg() {
    var px = boardPx(board());
    save(new Blob([serialise(Math.round(px.w), Math.round(px.h))],
                  { type: 'image/svg+xml;charset=utf-8' }), filename('svg'));
    status('SVG saved.');
  }

  function exportPng() {
    var choice = pngChoices(board())[el.png.selectedIndex] || pngChoices(board())[0];
    if (!choice) return;
    status('Rendering PNG at ' + choice.w + ' x ' + choice.h + '...');
    var url = URL.createObjectURL(new Blob([serialise(choice.w, choice.h)],
                                           { type: 'image/svg+xml;charset=utf-8' }));
    var img = new Image();
    img.onload = function () {
      var c = document.createElement('canvas');
      c.width = choice.w;
      c.height = choice.h;
      c.getContext('2d').drawImage(img, 0, 0, choice.w, choice.h);
      c.toBlob(function (blob) {
        URL.revokeObjectURL(url);
        if (!blob) { status('The browser ran out of memory for that size. Pick a smaller PNG.', 'error'); return; }
        save(blob, filename('png'));
        status('PNG saved at ' + choice.w + ' x ' + choice.h + '.');
      }, 'image/png');
    };
    img.onerror = function () {
      URL.revokeObjectURL(url);
      status('The PNG could not be rendered.', 'error');
    };
    img.src = url;
  }

  function exportPdf() {
    var b = board(), pt = boardPt(b), box = artBox(pt.w, pt.h);
    el.pdf.disabled = true;
    status('Building the PDF...');
    // yield a frame so the disabled state paints before the main-thread work
    requestAnimationFrame(function () {
      Promise.resolve().then(function () {
        return window.SvgToPdf.export(art, {
          page: pt,
          art: box,
          background: state.bg === 'transparent' ? null : state.bg
        });
      }).then(function (blob) {
        save(blob, filename('pdf'));
        status('PDF saved, ' + Math.round(pt.w / 72 * 25.4) + ' x ' +
               Math.round(pt.h / 72 * 25.4) + ' mm of vector art.');
      }).catch(function (err) {
        status('PDF export failed: ' + err.message, 'error');
      }).then(function () {
        el.pdf.disabled = false;
      });
    });
  }

  /* ---------- controls ---------- */

  function pressGroup(root, attr, value) {
    root.querySelectorAll('button[' + attr + ']').forEach(function (btn) {
      btn.setAttribute('aria-pressed', btn.getAttribute(attr) === value ? 'true' : 'false');
    });
  }

  function buildSwatches() {
    el.scheme.innerHTML = '';
    PRESETS.forEach(function (p) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'swatch';
      btn.setAttribute('data-scheme', p.id);
      btn.setAttribute('aria-pressed', p.id === state.scheme ? 'true' : 'false');
      var chips = document.createElement('span');
      chips.className = 'chips';
      [p.ring[1][1], p.disc[1][1], p.ink, p.accent].forEach(function (c) {
        var s = document.createElement('span');
        s.style.background = c;
        chips.appendChild(s);
      });
      btn.appendChild(chips);
      btn.appendChild(document.createTextNode(p.label));
      btn.addEventListener('click', function () {
        state.scheme = p.id;
        state.custom = null;
        syncPickers();
        pressGroup(el.scheme, 'data-scheme', p.id);
        paint();
        layout();
      });
      el.scheme.appendChild(btn);
    });
  }

  function syncPickers() {
    var p = preset(state.scheme), c = state.custom || {
      sun: p.seed.sun, edge: p.seed.edge, disc: p.seed.disc, ink: p.ink, accent: p.accent
    };
    el.sun.value = c.sun;
    el.edge.value = c.edge;
    el.disc.value = c.disc;
    el.ink.value = c.ink;
    el.accent.value = c.accent;
  }

  function onPicker() {
    var p = preset(state.scheme);
    state.custom = {
      sun: el.sun.value, edge: el.edge.value, disc: el.disc.value,
      ink: el.ink.value, accent: el.accent.value
    };
    void p;
    el.scheme.querySelectorAll('button').forEach(function (b) {
      b.setAttribute('aria-pressed', 'false');
    });
    paint();
    layout();
  }

  function buildBoards() {
    BOARDS.forEach(function (b) {
      var o = document.createElement('option');
      o.value = b.id;
      o.textContent = b.label + (b.id === 'custom' ? '' : '  ' + b.w + ' x ' + b.h + ' ' + b.unit);
      el.board.appendChild(o);
    });
    el.board.value = state.board;
  }

  function buildPngChoices() {
    var list = pngChoices(board());
    el.png.innerHTML = '';
    list.forEach(function (o) {
      var opt = document.createElement('option');
      opt.textContent = o.w + ' x ' + o.h + '  (' + o.note + ')';
      el.png.appendChild(opt);
    });
    el.png.selectedIndex = Math.min(1, list.length - 1);
  }

  function initDrag() {
    var start = null;
    el.artboard.addEventListener('pointerdown', function (e) {
      start = { x: e.clientX, y: e.clientY, cx: state.cx, cy: state.cy,
                w: el.artboard.clientWidth, h: el.artboard.clientHeight };
      el.artboard.setPointerCapture(e.pointerId);
      el.artboard.classList.add('is-dragging');
    });
    el.artboard.addEventListener('pointermove', function (e) {
      if (!start) return;
      state.cx = Math.min(1.25, Math.max(-0.25, start.cx + (e.clientX - start.x) / start.w));
      state.cy = Math.min(1.25, Math.max(-0.25, start.cy + (e.clientY - start.y) / start.h));
      layout();
    });
    ['pointerup', 'pointercancel'].forEach(function (t) {
      el.artboard.addEventListener(t, function () {
        start = null;
        el.artboard.classList.remove('is-dragging');
      });
    });
  }

  function show(lockup) {
    status('Loading artwork...');
    return loadArt(lockup).then(function (node) {
      if (art && art.parentNode) art.parentNode.removeChild(art);
      art = node;
      art.removeAttribute('width');
      art.removeAttribute('height');
      el.artboard.appendChild(art);
      paint();
      layout();
      status('');
    }).catch(function (err) {
      status('Could not load the artwork (' + err.message +
             '). This page needs to be served over http, not opened as a file.', 'error');
    });
  }

  function init() {
    el = {
      artboard: document.getElementById('artboard'),
      frame: document.querySelector('.stage-frame'),
      scheme: document.getElementById('ctl-scheme'),
      board: document.getElementById('ctl-board'),
      customBoard: document.getElementById('ctl-custom-board'),
      boardW: document.getElementById('board-w'),
      boardH: document.getElementById('board-h'),
      size: document.getElementById('ctl-size'),
      png: document.getElementById('ctl-png'),
      pdf: document.getElementById('btn-pdf'),
      status: document.getElementById('status'),
      dims: document.getElementById('stage-dims'),
      schemeName: document.getElementById('stage-scheme'),
      sun: document.getElementById('c-sun'),
      edge: document.getElementById('c-edge'),
      disc: document.getElementById('c-disc'),
      ink: document.getElementById('c-ink'),
      accent: document.getElementById('c-accent'),
      bgColour: document.getElementById('c-bg')
    };

    buildSwatches();
    syncPickers();
    buildBoards();
    buildPngChoices();
    initDrag();

    document.getElementById('ctl-lockup').addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-lockup]');
      if (!btn) return;
      state.lockup = btn.getAttribute('data-lockup');
      pressGroup(this, 'data-lockup', state.lockup);
      show(state.lockup);
    });

    document.getElementById('ctl-crown').addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-crown]');
      if (!btn) return;
      state.crown = btn.getAttribute('data-crown');
      pressGroup(this, 'data-crown', state.crown);
      paint();
    });

    document.getElementById('ctl-bg').addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-bg]');
      if (!btn) return;
      state.bg = btn.getAttribute('data-bg');
      pressGroup(this, 'data-bg', state.bg);
      layout();
    });

    el.bgColour.addEventListener('input', function () {
      state.bg = this.value;
      pressGroup(document.getElementById('ctl-bg'), 'data-bg', '');
      layout();
    });

    [el.sun, el.edge, el.disc, el.ink, el.accent].forEach(function (input) {
      input.addEventListener('input', onPicker);
    });

    el.board.addEventListener('change', function () {
      state.board = this.value;
      el.customBoard.hidden = state.board !== 'custom';
      buildPngChoices();
      layout();
    });

    [el.boardW, el.boardH].forEach(function (input) {
      input.addEventListener('input', function () {
        state.customW = Math.max(1, parseInt(el.boardW.value, 10) || 1);
        state.customH = Math.max(1, parseInt(el.boardH.value, 10) || 1);
        buildPngChoices();
        layout();
      });
    });

    el.size.addEventListener('input', function () {
      state.size = parseInt(this.value, 10) / 100;
      layout();
    });

    document.getElementById('btn-fit').addEventListener('click', function () {
      state.size = 0.88;
      el.size.value = 88;
      layout();
    });

    document.getElementById('btn-centre').addEventListener('click', function () {
      state.cx = 0.5;
      state.cy = 0.5;
      layout();
    });

    document.getElementById('btn-svg').addEventListener('click', exportSvg);
    document.getElementById('btn-png').addEventListener('click', exportPng);
    el.pdf.addEventListener('click', exportPdf);

    window.addEventListener('resize', layout);
    show(state.lockup);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
