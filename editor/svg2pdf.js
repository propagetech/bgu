/* Vector PDF export for the Ganesha Utsava logo editor.
 *
 * Scoped to the artwork this editor draws: flat-filled and radial-gradient
 * filled path groups, no strokes, no text, no images. That is the whole of the
 * trace, so the PDF comes out as real vector art rather than a placed bitmap,
 * and stays sharp at any size a printer asks for.
 *
 * No dependencies. Exposes window.SvgToPdf.export(svgEl, opts) -> Promise<Blob>.
 */
(function (global) {
  'use strict';

  var enc = function (s) { return new TextEncoder().encode(s); };

  /* ---------- numbers ---------- */

  /* Path and page coordinates are large, so two decimals is ample for them. The
   * cm matrices and object-bounding-box gradient coords are small fractions,
   * where two decimals would round a scale factor to zero and drop the artwork
   * off the page, so those keep six significant digits. */
  function num(v) {
    if (!isFinite(v) || v === 0) return '0';
    var r = Math.abs(v) >= 1 ? Math.round(v * 100) / 100
                             : parseFloat(v.toPrecision(6));
    if (Math.abs(r) < 1e-9) return '0';
    return String(Object.is(r, -0) ? 0 : r);
  }

  function hexToRgb(hex) {
    var h = String(hex).trim().replace('#', '');
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    var n = parseInt(h, 16);
    if (isNaN(n)) return [0, 0, 0];
    return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
  }

  function col(c) { return c.map(function (v) { return num(v); }).join(' '); }

  /* ---------- matrices, as PDF [a b c d e f] ---------- */

  var IDENT = [1, 0, 0, 1, 0, 0];

  // the matrix that applies m1 first, then m2
  function mul(m1, m2) {
    return [
      m1[0] * m2[0] + m1[1] * m2[2],
      m1[0] * m2[1] + m1[1] * m2[3],
      m1[2] * m2[0] + m1[3] * m2[2],
      m1[2] * m2[1] + m1[3] * m2[3],
      m1[4] * m2[0] + m1[5] * m2[2] + m2[4],
      m1[4] * m2[1] + m1[5] * m2[3] + m2[5]
    ];
  }

  function parseTransform(str) {
    var m = IDENT;
    if (!str) return m;
    var re = /(matrix|translate|scale|rotate)\s*\(([^)]*)\)/g, hit;
    while ((hit = re.exec(str))) {
      var a = hit[2].split(/[\s,]+/).filter(Boolean).map(Number), t;
      if (hit[1] === 'matrix') t = a.slice(0, 6);
      else if (hit[1] === 'translate') t = [1, 0, 0, 1, a[0] || 0, a[1] || 0];
      else if (hit[1] === 'scale') t = [a[0], 0, 0, a.length > 1 ? a[1] : a[0], 0, 0];
      else {
        var r = (a[0] || 0) * Math.PI / 180, c = Math.cos(r), s = Math.sin(r);
        t = [c, s, -s, c, 0, 0];
        if (a.length > 2) t = mul(mul([1, 0, 0, 1, -a[1], -a[2]], t), [1, 0, 0, 1, a[1], a[2]]);
      }
      m = mul(t, m);
    }
    return m;
  }

  /* ---------- path data -> PDF path operators ----------
   * The trace emits an absolute M followed by relative c and l runs. Arcs never
   * appear in it, so an arc throws rather than being silently mis-drawn.
   */

  function pathOps(d) {
    var tok = d.match(/[MmLlHhVvCcSsQqTtZz]|-?\d*\.?\d+(?:[eE][-+]?\d+)?/g) || [];
    var out = [], i = 0, cmd = '', x = 0, y = 0, sx = 0, sy = 0;
    var px = 0, py = 0;            // last cubic control point, for S
    var qx = 0, qy = 0;            // last quadratic control point, for T
    var open = false;

    function n() { return parseFloat(tok[i++]); }
    function moveTo(nx, ny) { out.push(num(nx) + ' ' + num(ny) + ' m'); x = nx; y = ny; }
    function lineTo(nx, ny) { out.push(num(nx) + ' ' + num(ny) + ' l'); x = nx; y = ny; }
    function curveTo(x1, y1, x2, y2, nx, ny) {
      out.push(num(x1) + ' ' + num(y1) + ' ' + num(x2) + ' ' + num(y2) + ' ' +
               num(nx) + ' ' + num(ny) + ' c');
      px = x2; py = y2; x = nx; y = ny;
    }

    while (i < tok.length) {
      if (/[A-Za-z]/.test(tok[i])) { cmd = tok[i++]; }
      else if (cmd === 'M') cmd = 'L';
      else if (cmd === 'm') cmd = 'l';
      var rel = cmd === cmd.toLowerCase();
      var C = cmd.toUpperCase();

      if (C === 'Z') { if (open) out.push('h'); open = false; x = sx; y = sy; continue; }
      if (C === 'A') throw new Error('arc segments are not supported');

      if (C === 'M') {
        var mx = n(), my = n();
        if (rel) { mx += x; my += y; }
        moveTo(mx, my); sx = x; sy = y; open = true; px = x; py = y; qx = x; qy = y;
      } else if (C === 'L') {
        var lx = n(), ly = n();
        if (rel) { lx += x; ly += y; }
        lineTo(lx, ly); px = x; py = y; qx = x; qy = y;
      } else if (C === 'H') {
        var hx = n(); lineTo(rel ? x + hx : hx, y); px = x; py = y; qx = x; qy = y;
      } else if (C === 'V') {
        var vy = n(); lineTo(x, rel ? y + vy : vy); px = x; py = y; qx = x; qy = y;
      } else if (C === 'C') {
        var a1 = n(), b1 = n(), a2 = n(), b2 = n(), a3 = n(), b3 = n();
        if (rel) { a1 += x; b1 += y; a2 += x; b2 += y; a3 += x; b3 += y; }
        curveTo(a1, b1, a2, b2, a3, b3); qx = x; qy = y;
      } else if (C === 'S') {
        var s2x = n(), s2y = n(), s3x = n(), s3y = n();
        if (rel) { s2x += x; s2y += y; s3x += x; s3y += y; }
        curveTo(2 * x - px, 2 * y - py, s2x, s2y, s3x, s3y); qx = x; qy = y;
      } else if (C === 'Q' || C === 'T') {
        var cxq, cyq, ex, ey;
        if (C === 'Q') {
          cxq = n(); cyq = n(); ex = n(); ey = n();
          if (rel) { cxq += x; cyq += y; ex += x; ey += y; }
        } else {
          ex = n(); ey = n();
          if (rel) { ex += x; ey += y; }
          cxq = 2 * x - qx; cyq = 2 * y - qy;
        }
        curveTo(x + 2 / 3 * (cxq - x), y + 2 / 3 * (cyq - y),
                ex + 2 / 3 * (cxq - ex), ey + 2 / 3 * (cyq - ey), ex, ey);
        qx = cxq; qy = cyq;
      }
    }
    return out.join('\n');
  }

  /* ---------- PDF object graph ---------- */

  function PdfDoc() { this.objs = [null]; }

  PdfDoc.prototype.add = function (body) { this.objs.push(body); return this.objs.length - 1; };
  PdfDoc.prototype.reserve = function () { this.objs.push(null); return this.objs.length - 1; };
  PdfDoc.prototype.set = function (i, body) { this.objs[i] = body; };

  PdfDoc.prototype.build = function () {
    var parts = [], len = 0;
    function push(u8) { parts.push(u8); len += u8.length; }
    push(new Uint8Array([0x25, 0x50, 0x44, 0x46, 0x2d, 0x31, 0x2e, 0x37, 0x0a,
                         0x25, 0xe2, 0xe3, 0xcf, 0xd3, 0x0a]));
    var offsets = [0];
    for (var i = 1; i < this.objs.length; i++) {
      offsets[i] = len;
      var o = this.objs[i];
      if (o && o.stream) {
        push(enc(i + ' 0 obj\n' + o.dict.replace('>>', '/Length ' + o.stream.length + ' >>') +
                 '\nstream\n'));
        push(o.stream);
        push(enc('\nendstream\nendobj\n'));
      } else {
        push(enc(i + ' 0 obj\n' + o + '\nendobj\n'));
      }
    }
    var xref = len, n = this.objs.length;
    var s = 'xref\n0 ' + n + '\n0000000000 65535 f \n';
    for (var j = 1; j < n; j++) {
      s += ('0000000000' + offsets[j]).slice(-10) + ' 00000 n \n';
    }
    s += 'trailer\n<< /Size ' + n + ' /Root 1 0 R >>\nstartxref\n' + xref + '\n%%EOF\n';
    push(enc(s));
    return new Blob(parts, { type: 'application/pdf' });
  };

  /* ---------- gradients ---------- */

  function readStops(grad) {
    return Array.prototype.map.call(grad.querySelectorAll('stop'), function (s) {
      var o = (s.getAttribute('offset') || '0').trim();
      return {
        t: o.indexOf('%') > -1 ? parseFloat(o) / 100 : parseFloat(o),
        c: hexToRgb(s.getAttribute('stop-color') || '#000')
      };
    }).sort(function (a, b) { return a.t - b.t; });
  }

  // a PDF function mapping 0..1 to the stop colours
  function stopFunction(doc, stops) {
    if (stops.length === 1) stops = [stops[0], stops[0]];
    var segs = [], bounds = [], encode = [];
    for (var i = 0; i < stops.length - 1; i++) {
      segs.push(doc.add('<< /FunctionType 2 /Domain [0 1] /C0 [' + col(stops[i].c) +
                        '] /C1 [' + col(stops[i + 1].c) + '] /N 1 >>'));
      if (i > 0) bounds.push(num(stops[i].t));
      encode.push('0 1');
    }
    if (segs.length === 1) return segs[0];
    return doc.add('<< /FunctionType 3 /Domain [0 1] /Functions [' +
      segs.map(function (r) { return r + ' 0 R'; }).join(' ') +
      '] /Bounds [' + bounds.join(' ') + '] /Encode [' + encode.join(' ') + '] >>');
  }

  /* ---------- the export ---------- */

  // Content streams are mostly digits and repeat heavily, so Flate takes a
  // typical page from ~750KB to ~250KB. Uncompressed is a valid fallback.
  function deflate(bytes) {
    if (typeof CompressionStream !== 'function') return Promise.resolve(null);
    try {
      var stream = new Blob([bytes]).stream().pipeThrough(new CompressionStream('deflate'));
      return new Response(stream).arrayBuffer().then(function (buf) {
        return new Uint8Array(buf);
      }).catch(function () { return null; });
    } catch (e) {
      return Promise.resolve(null);
    }
  }

  /**
   * @param {SVGSVGElement} svg   live artwork, read as currently styled
   * @param {Object} o
   *   o.page      {w, h} page size in points
   *   o.art       {x, y, size} artwork box in points, y from the page top
   *   o.background hex string, or null for no background at all
   * @returns {Promise<Blob>}
   */
  function exportPdf(svg, o) {
    var vb = (svg.getAttribute('viewBox') || '0 0 1 1').split(/[\s,]+/).map(Number);
    var vw = vb[2], vh = vb[3];
    var k = o.art.size / Math.max(vw, vh);
    // SVG user units (y down, origin top left) -> PDF points (y up, origin bottom left)
    var place = [k, 0, 0, -k, o.art.x, o.page.h - o.art.y];

    var doc = new PdfDoc();
    var catalog = doc.reserve(), pages = doc.reserve(), page = doc.reserve();
    var content = doc.reserve();

    var ops = [], shadings = [];

    if (o.background) {
      ops.push(col(hexToRgb(o.background)) + ' rg');
      ops.push('0 0 ' + num(o.page.w) + ' ' + num(o.page.h) + ' re f');
    }

    Array.prototype.forEach.call(svg.children, function (g) {
      if (g.tagName.toLowerCase() !== 'g') return;
      if (g.getAttribute('display') === 'none' || g.style.display === 'none') return;

      var paths = g.querySelectorAll('path');
      if (!paths.length) return;

      var m = mul(parseTransform(g.getAttribute('transform')), place);
      var fill = (g.getAttribute('fill') || '#000').trim();
      var evenOdd = (g.getAttribute('fill-rule') || '') === 'evenodd';
      var geometry = Array.prototype.map.call(paths, function (p) {
        return pathOps(p.getAttribute('d'));
      }).join('\n');

      ops.push('q');
      ops.push(m.map(num).join(' ') + ' cm');

      var url = fill.match(/^url\(#(.+)\)$/);
      if (!url) {
        if (fill === 'none') { ops.push('Q'); return; }
        ops.push(col(hexToRgb(fill)) + ' rg');
        ops.push(geometry);
        ops.push(evenOdd ? 'f*' : 'f');
        ops.push('Q');
        return;
      }

      // gradient fill: clip to the path, then paint the shading through it
      var grad = svg.querySelector('#' + CSS.escape(url[1]));
      var stops = readStops(grad);
      var userSpace = grad.getAttribute('gradientUnits') === 'userSpaceOnUse';
      var name = 'Sh' + shadings.length;

      ops.push(geometry);
      ops.push(evenOdd ? 'W* n' : 'W n');

      function len(attr, dflt, span) {
        var v = grad.getAttribute(attr);
        if (v == null) v = dflt;
        v = String(v).trim();
        return v.indexOf('%') > -1 ? parseFloat(v) / 100 * span : parseFloat(v);
      }

      var cx, cy, r;
      if (userSpace) {
        cx = len('cx', '50%', vw); cy = len('cy', '50%', vh); r = len('r', '50%', vw);
      } else {
        // objectBoundingBox: a unit square stretched over the path bounds, so a
        // circle in that space is an ellipse on the page. Concatenate the box
        // matrix and define the shading in unit space.
        var b = paths[0].getBBox();
        for (var i = 1; i < paths.length; i++) {
          var e = paths[i].getBBox();
          var x1 = Math.min(b.x, e.x), y1 = Math.min(b.y, e.y);
          b = { x: x1, y: y1,
                width: Math.max(b.x + b.width, e.x + e.width) - x1,
                height: Math.max(b.y + b.height, e.y + e.height) - y1 };
        }
        ops.push([b.width, 0, 0, b.height, b.x, b.y].map(num).join(' ') + ' cm');
        cx = len('cx', '50%', 1); cy = len('cy', '50%', 1); r = len('r', '50%', 1);
      }

      shadings.push({
        name: name,
        dict: '<< /ShadingType 3 /ColorSpace /DeviceRGB /Coords [' +
              num(cx) + ' ' + num(cy) + ' 0 ' + num(cx) + ' ' + num(cy) + ' ' + num(r) +
              '] /Function @FN /Extend [true true] >>',
        stops: stops
      });
      ops.push('/' + name + ' sh');
      ops.push('Q');
    });

    var shRefs = shadings.map(function (s) {
      var fn = stopFunction(doc, s.stops);
      return '/' + s.name + ' ' + doc.add(s.dict.replace('@FN', fn + ' 0 R')) + ' 0 R';
    });

    doc.set(page, '<< /Type /Page /Parent ' + pages + ' 0 R /MediaBox [0 0 ' +
      num(o.page.w) + ' ' + num(o.page.h) + '] /Resources << /Shading << ' +
      shRefs.join(' ') + ' >> >> /Contents ' + content + ' 0 R >>');
    doc.set(pages, '<< /Type /Pages /Kids [' + page + ' 0 R] /Count 1 >>');
    doc.set(catalog, '<< /Type /Catalog /Pages ' + pages + ' 0 R >>');

    var raw = enc(ops.join('\n'));
    return deflate(raw).then(function (packed) {
      doc.set(content, packed
        ? { stream: packed, dict: '<< /Filter /FlateDecode >>' }
        : { stream: raw, dict: '<< >>' });
      return doc.build();
    });
  }

  global.SvgToPdf = { export: exportPdf };
})(window);
