/* Ditoman: market map for "What Iran Has".
   Draws every company as a tile whose area follows its market value, grouped by branch
   (or by sub-branch on a branch page). Tapping a tile opens a sheet with the details and
   lights up the companies in the same ownership family and the same sub-branch. */
(function () {
  var host = document.querySelector(".ir-map");
  var src = document.getElementById("ir-map-data");
  if (!host || !src) return;
  var D = JSON.parse(src.textContent);
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function fa(n) { return String(n).replace(/[0-9]/g, function (d) { return "۰۱۲۳۴۵۶۷۸۹"[d]; }); }
  function both(o, cls) {
    return '<span class="i-fa' + (cls ? " " + cls : "") + '">' + o.fa + '</span><span class="i-en' + (cls ? " " + cls : "") + '">' + o.en + "</span>";
  }

  /* ---- squarified treemap ---- */
  function worst(row, side, total, area) {
    var s = 0, mx = 0, mn = Infinity;
    row.forEach(function (r) { s += r.a; mx = Math.max(mx, r.a); mn = Math.min(mn, r.a); });
    var s2 = s * s, w2 = side * side;
    return Math.max(w2 * mx / s2, s2 / (w2 * mn));
  }
  function squarify(items, x, y, w, h) {
    var total = items.reduce(function (s, i) { return s + i.v; }, 0), out = [];
    var area = w * h;
    var rest = items.map(function (i) { return { item: i, a: i.v / total * area }; });
    while (rest.length) {
      var side = Math.min(w, h), row = [rest[0]], i = 1;
      while (i < rest.length && worst(row.concat([rest[i]]), side) <= worst(row, side)) { row.push(rest[i]); i++; }
      rest = rest.slice(row.length);
      var ra = row.reduce(function (s, r) { return s + r.a; }, 0);
      if (w >= h) {
        var cw = ra / h, cy = y;
        row.forEach(function (r) { var rh = r.a / cw; out.push({ item: r.item, x: x, y: cy, w: cw, h: rh }); cy += rh; });
        x += cw; w -= cw;
      } else {
        var ch = ra / w, cx = x;
        row.forEach(function (r) { var rw = r.a / ch; out.push({ item: r.item, x: cx, y: y, w: rw, h: ch }); cx += rw; });
        y += ch; h -= ch;
      }
    }
    return out;
  }

  /* ---- groups ---- */
  var groups = {};
  D.items.forEach(function (c) {
    var g = groups[c.g] || (groups[c.g] = { key: c.g, name: c.gname, color: c.color, v: 0, items: [] });
    g.items.push(c); g.v += c.w;
  });
  var glist = Object.keys(groups).map(function (k) { return groups[k]; }).sort(function (a, b) { return b.v - a.v; });

  /* legend */
  var legend = document.createElement("div");
  legend.className = "ir-map-legend";
  legend.innerHTML = glist.map(function (g) {
    return '<button type="button" data-g="' + g.key + '" style="--c:' + g.color + '"><i></i>' + both(g.name) +
      '<small>' + both({ fa: fa(g.items.length) + " شرکت", en: g.items.length + (g.items.length === 1 ? " company" : " companies") }) + "</small></button>";
  }).join("");
  host.parentNode.insertBefore(legend, host);

  var tiles = [];
  function draw() {
    var W = host.clientWidth, H = host.clientHeight;
    host.innerHTML = "";
    tiles = [];
    var gap = 3;
    squarify(glist.map(function (g) { return { v: g.v, g: g }; }), 0, 0, W, H).forEach(function (gb) {
      var g = gb.item.g;
      var box = document.createElement("div");
      box.className = "ir-map-g";
      box.style.cssText = "inset-inline-start:" + gb.x + "px;top:" + gb.y + "px;width:" + gb.w + "px;height:" + gb.h + "px;--c:" + g.color;
      host.appendChild(box);
      var lab = gb.w > 90 && gb.h > 60;
      var top = lab ? 26 : 0;
      var items = g.items.slice().sort(function (a, b) { return b.w - a.w; }).map(function (c) { return { v: c.w, c: c }; });
      if (lab) {
        var h = document.createElement("span");
        h.className = "ir-map-gl";
        h.innerHTML = both(g.name);
        box.appendChild(h);
      }
      squarify(items, 0, top, gb.w, gb.h - top).forEach(function (r, i) {
        var c = r.item.c;
        var t = document.createElement("button");
        t.type = "button";
        t.className = "ir-tile";
        var big = r.w > 120 && r.h > 76, mid = r.w > 54 && r.h > 34;
        t.style.cssText = "inset-inline-start:" + (r.x + gap / 2) + "px;top:" + (r.y + gap / 2) + "px;width:" + Math.max(r.w - gap, 1) + "px;height:" + Math.max(r.h - gap, 1) +
          "px;--k:" + (0.62 - Math.min(i, 12) * 0.035);
        t.setAttribute("aria-label", c.fa + " · " + c.en);
        t.innerHTML = mid ? "<b>" + both({ fa: c.sym, en: c.short }) + "</b>" + (big ? '<span class="nm">' + both({ fa: c.fa, en: c.en }) + '</span><span class="vl">' + both(c.val || D.pending) + "</span>" : "") : "";
        t.addEventListener("click", function () { open(c); });
        box.appendChild(t);
        tiles.push({ el: t, c: c });
      });
    });
    if (current) mark(current);
  }

  /* ---- sheet ---- */
  var sheet = document.createElement("div");
  sheet.className = "ir-sheet";
  sheet.setAttribute("role", "dialog");
  sheet.setAttribute("aria-modal", "false");
  sheet.hidden = true;
  document.body.appendChild(sheet);
  var current = null;

  function mark(c) {
    host.classList.add("focus");
    tiles.forEach(function (t) {
      var same = t.c === c, fam = c.fam && t.c.fam === c.fam, sub = t.c.sub === c.sub && t.c.b === c.b;
      t.el.classList.toggle("on", same);
      t.el.classList.toggle("fam", !same && !!fam);
      t.el.classList.toggle("sib", !same && !fam && sub);
    });
  }
  function close() {
    current = null;
    sheet.classList.remove("show");
    host.classList.remove("focus");
    tiles.forEach(function (t) { t.el.classList.remove("on", "fam", "sib"); });
    setTimeout(function () { if (!current) sheet.hidden = true; }, reduce ? 0 : 260);
  }
  function chipsFor(list) {
    return list.map(function (x) {
      return '<button type="button" class="ir-sheet-rel" data-sym="' + x.sym + '" style="--c:' + x.color + '">' + both({ fa: "<b>" + x.sym + "</b> " + x.fa, en: x.en }) + "</button>";
    }).join("");
  }
  function open(c) {
    current = c;
    var fam = c.fam ? D.items.filter(function (x) { return x.fam === c.fam && x !== c; }) : [];
    var sib = D.items.filter(function (x) { return x.sub === c.sub && x.b === c.b && x !== c && fam.indexOf(x) < 0; }).slice(0, 6);
    var rank = (c.approx ? "≈" : "") ;
    var facts = c.facts.map(function (f) {
      return '<div class="' + (f.v ? "" : "pending") + '"><dt>' + both(f.k) + "</dt><dd>" + both(f.v || D.pending) + "</dd></div>";
    }).join("");
    sheet.style.setProperty("--c", c.color);
    sheet.innerHTML =
      '<button type="button" class="ir-sheet-x" aria-label="بستن">×</button>' +
      '<p class="ir-sheet-k">' + both({ fa: "رتبه‌ی " + rank + fa(c.rank) + " · " + c.sym, en: "Rank " + rank + c.rank }) + "</p>" +
      "<h3>" + both({ fa: c.fa, en: c.en }) + "</h3>" +
      '<p class="ir-sheet-path">' + both(c.bname) + " › " + both(c.subname) + "</p>" +
      '<p class="ir-sheet-v">' + both(c.val || D.pending) + "</p>" +
      '<dl class="ir-sheet-facts">' + facts + "</dl>" +
      (fam.length ? '<p class="ir-sheet-h">' + both({ fa: "هم‌خانواده · " + c.famname.fa, en: "Same family · " + c.famname.en }) + '</p><div class="ir-sheet-rels">' + chipsFor(fam) + "</div>" : "") +
      (sib.length ? '<p class="ir-sheet-h">' + both({ fa: "هم‌رشته", en: "Same sub-branch" }) + '</p><div class="ir-sheet-rels">' + chipsFor(sib) + "</div>" : "") +
      (c.href ? '<a class="ir-sheet-go" href="' + c.href + '">' + both({ fa: "رفتن به شاخه‌ی " + c.bname.fa + " ←", en: "Open the " + c.bname.en + " branch →" }) + "</a>" : "");
    sheet.hidden = false;
    requestAnimationFrame(function () { sheet.classList.add("show"); });
    sheet.querySelector(".ir-sheet-x").addEventListener("click", close);
    sheet.querySelectorAll(".ir-sheet-rel").forEach(function (b) {
      b.addEventListener("click", function () {
        var x = D.items.filter(function (i) { return i.sym === b.getAttribute("data-sym"); })[0];
        if (x) open(x);
      });
    });
    mark(c);
  }
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape" && current) close(); });
  document.addEventListener("click", function (ev) {
    if (current && !sheet.contains(ev.target) && !ev.target.closest(".ir-tile")) close();
  });

  /* legend: hover or tap a group to light it up */
  legend.querySelectorAll("button").forEach(function (b) {
    function on() { host.classList.add("focus"); tiles.forEach(function (t) { t.el.classList.toggle("sib", t.c.g === b.getAttribute("data-g")); }); }
    function off() { if (current) mark(current); else { host.classList.remove("focus"); tiles.forEach(function (t) { t.el.classList.remove("sib"); }); } }
    b.addEventListener("mouseenter", on);
    b.addEventListener("mouseleave", off);
    b.addEventListener("focus", on);
    b.addEventListener("blur", off);
  });

  draw();
  var rt;
  window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(draw, 120); });
})();
