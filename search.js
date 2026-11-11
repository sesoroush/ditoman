/* Ditoman site search.
   A small client-side search over search-index.json (built by scripts/build_search.py).
   Adds a search button to the header; opens with the button, "/" or Ctrl/Cmd+K.
   Persian text is normalised so Arabic ي/ك, ZWNJ, diacritics and Persian digits all match. */
(function () {
  "use strict";
  if (window.__ditomanSearch) return;
  window.__ditomanSearch = true;

  var INDEX_URL = "search-index.json?v=20261111";
  var root = document.documentElement;
  var data = null, loading = null;

  function isEn() { return root.getAttribute("data-lang") === "en"; }
  function t(fa, en) { return isEn() ? en : fa; }

  function norm(s) {
    return (s || "").toString().toLowerCase()
      .replace(/[يى]/g, "ی")          // ي ى -> ی
      .replace(/ك/g, "ک")                  // ك -> ک
      .replace(/[ةۀ]/g, "ه")          // ة ۀ -> ه
      .replace(/[آأإ]/g, "ا")    // آ أ إ -> ا
      .replace(/ؤ/g, "و")                  // ؤ -> و
      .replace(/[ً-ٰٟـ]/g, "")   // diacritics, tatweel
      .replace(/[‌‍‎‏]/g, "")    // ZWNJ, ZWJ, marks
      .replace(/[۰-۹]/g, function (d) { return String(d.charCodeAt(0) - 0x06F0); })
      .replace(/[٠-٩]/g, function (d) { return String(d.charCodeAt(0) - 0x0660); })
      .replace(/[«»"'“”‘’()\[\]{}<>:;,.!?؟،؛|\/\\\-–—_]+/g, " ")
      .replace(/\s+/g, " ").trim();
  }

  function load() {
    if (data) return Promise.resolve(data);
    if (loading) return loading;
    loading = fetch(INDEX_URL).then(function (r) {
      if (!r.ok) throw new Error("index " + r.status);
      return r.json();
    }).then(function (rows) {
      data = rows.map(function (e) {
        e._t = norm(e.f + " " + e.t);
        e._c = norm(e.c + " " + e.ce);
        e._d = norm(e.d);
        e._x = norm(e.x);
        return e;
      });
      return data;
    });
    loading.catch(function () { loading = null; });
    return loading;
  }

  function search(q) {
    var toks = norm(q).split(" ").filter(function (w) { return w.length > 1 || /\d/.test(w); });
    if (!toks.length) return [];
    var out = [];
    for (var i = 0; i < data.length; i++) {
      var e = data[i], score = 0, ok = true;
      for (var j = 0; j < toks.length; j++) {
        var w = toks[j], s = 0;
        if (e._t.indexOf(w) > -1) s += (e._t.indexOf(w) === 0 || e._t.indexOf(" " + w) > -1) ? 14 : 10;
        if (e._c.indexOf(w) > -1) s += 6;
        if (e._d.indexOf(w) > -1) s += 3;
        if (e._x.indexOf(w) > -1) s += 1;
        if (!s) { ok = false; break; }
        score += s;
      }
      if (!ok) continue;
      if (e.k === "story" || e.k === "lesson") score += 1;
      out.push({ e: e, s: score, toks: toks });
    }
    out.sort(function (a, b) { return b.s - a.s; });
    return out.slice(0, 30);
  }

  function esc(s) {
    return (s || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }

  // A short excerpt around the first match, taken from the raw text so it reads naturally.
  function snippet(e, toks) {
    var src = e.d || e.x;
    var raw = e.x || "";
    var n = norm(raw);
    for (var j = 0; j < toks.length; j++) {
      var at = n.indexOf(toks[j]);
      if (at > -1 && e._d.indexOf(toks[j]) < 0) {
        // The normalised text is shorter than the raw text; map roughly by ratio.
        var r = Math.max(0, Math.floor(at * raw.length / Math.max(1, n.length)) - 60);
        src = (r > 0 ? "… " : "") + raw.slice(r, r + 180) + " …";
        break;
      }
    }
    return src.length > 200 ? src.slice(0, 200) + " …" : src;
  }

  // ---------- UI ----------
  var icon = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="m16 16 4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';

  var btn = document.createElement("button");
  btn.type = "button";
  btn.className = "search-btn";
  btn.innerHTML = icon + '<span class="sb-word"><span lang="fa">جستجو</span><span lang="en">Search</span></span>';
  btn.setAttribute("aria-haspopup", "dialog");

  function placeButton() {
    var spot = document.querySelector(".nav-right");
    var lang = document.querySelector("header .lang-btn");
    if (spot) {
      if (lang && lang.parentNode === spot) spot.insertBefore(btn, lang); else spot.insertBefore(btn, spot.firstChild);
      return;
    }
    var bar = document.querySelector("header .container.nav") || document.querySelector("header .nav") || document.querySelector("header");
    if (!bar) return;
    if (lang && lang.parentNode === bar) bar.insertBefore(btn, lang); else bar.appendChild(btn);
  }

  var box = document.createElement("div");
  box.className = "sx";
  box.hidden = true;
  box.innerHTML =
    '<div class="sx-back" data-close></div>' +
    '<div class="sx-panel" role="dialog" aria-modal="true" aria-labelledby="sx-label">' +
    '  <div class="sx-bar">' + icon +
    '    <label id="sx-label" class="sx-sr" for="sx-q"></label>' +
    '    <input id="sx-q" class="sx-q" type="search" autocomplete="off" spellcheck="false" enterkeyhint="search" />' +
    '    <button type="button" class="sx-close" data-close></button>' +
    '  </div>' +
    '  <div class="sx-body" aria-live="polite"></div>' +
    '</div>';

  var input = box.querySelector(".sx-q");
  var body = box.querySelector(".sx-body");
  var lastFocus = null;

  function chrome() {
    box.dir = isEn() ? "ltr" : "rtl";
    box.querySelector("#sx-label").textContent = t("جستجو در دیتومان", "Search Ditoman");
    input.placeholder = t("جستجو در مطالب، درس‌ها، شرکت‌ها…", "Search stories, lessons, companies…");
    var c = box.querySelector(".sx-close");
    c.textContent = t("بستن", "Close");
  }

  var SUGGEST = [["چراغ روشن", "Lights On"], ["بیت‌کوین", "Bitcoin"], ["تورم", "inflation"], ["هوش مصنوعی", "AI"], ["انرژی", "energy"], ["زعفران", "saffron"]];

  function idle() {
    var h = '<p class="sx-hint">' + t("چند پیشنهاد:", "Try:") + "</p><p class=\"sx-sugg\">";
    SUGGEST.forEach(function (p) { var w = t(p[0], p[1]); h += '<button type="button" data-q="' + esc(w) + '">' + esc(w) + "</button>"; });
    body.innerHTML = h + "</p>";
  }

  function render() {
    var q = input.value.trim();
    if (!q) return idle();
    if (!data) { body.innerHTML = '<p class="sx-hint">' + t("در حال بارگذاری…", "Loading…") + "</p>"; return; }
    var res = search(q);
    if (!res.length) {
      body.innerHTML =
        '<div class="sx-empty"><p><b>' + t("نتیجه‌ای برای «" + esc(q) + "» پیدا نشد.", 'No results for "' + esc(q) + '".') + "</b></p>" +
        "<p>" + t("واژه‌ی کوتاه‌تر یا املای دیگری را امتحان کن، فارسی یا انگلیسی. یا از این بخش‌ها شروع کن:",
                  "Try a shorter word or another spelling, in English or Persian. Or start from:") + "</p>" +
        '<p class="sx-sugg">' +
        '<a href="learn.html">' + t("آموزش", "Learn") + "</a>" +
        '<a href="iran.html">' + t("ایران چه دارد", "What Iran has") + "</a>" +
        '<a href="companies.html">' + t("شرکت‌ها", "Companies") + "</a>" +
        '<a href="posts.html">' + t("یادداشت‌ها", "Posts") + "</a></p></div>";
      return;
    }
    var en = isEn();
    var h = '<p class="sx-count">' + (en ? res.length + (res.length === 30 ? "+" : "") + " results" : (res.length === 30 ? "۳۰+" : res.length.toLocaleString("fa-IR")) + " نتیجه") + "</p><ol class=\"sx-list\">";
    res.forEach(function (r) {
      var e = r.e;
      var title = en ? (e.t || e.f) : (e.f || e.t);
      var sub = en ? e.f : e.t;
      var cat = en ? e.ce : e.c;
      var light = e.c === "چراغ روشن" ? " is-light" : "";
      h += '<li><a href="' + esc(e.u) + '">' +
        (e.i ? '<img src="' + esc(e.i) + '" alt="" loading="lazy" width="56" height="56" />' : '<span class="sx-noimg"></span>') +
        '<span class="sx-txt"><span class="sx-cat' + light + '">' + esc(cat) + "</span>" +
        '<b class="sx-title">' + esc(title) + "</b>" +
        (sub && sub !== title ? '<span class="sx-sub" dir="auto">' + esc(sub) + "</span>" : "") +
        '<span class="sx-snip" dir="auto">' + esc(snippet(e, r.toks)) + "</span></span></a></li>";
    });
    body.innerHTML = h + "</ol>";
  }

  var timer = null;
  input.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(render, 90);
  });
  input.addEventListener("keydown", function (ev) {
    if (ev.key === "Enter") {
      var first = body.querySelector(".sx-list a");
      if (first) { ev.preventDefault(); location.href = first.getAttribute("href"); }
    }
  });
  box.addEventListener("click", function (ev) {
    if (ev.target.closest("[data-close]")) return close();
    var s = ev.target.closest("[data-q]");
    if (s) { input.value = s.getAttribute("data-q"); render(); input.focus(); }
  });
  document.addEventListener("keydown", function (ev) {
    if (!box.hidden && ev.key === "Escape") { ev.preventDefault(); return close(); }
    if (!box.hidden && ev.key === "Tab") {
      var f = box.querySelectorAll("input, button, a[href]");
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (ev.shiftKey && document.activeElement === first) { ev.preventDefault(); last.focus(); }
      else if (!ev.shiftKey && document.activeElement === last) { ev.preventDefault(); first.focus(); }
      return;
    }
    var typing = /^(input|textarea|select)$/i.test((ev.target && ev.target.tagName) || "") || (ev.target && ev.target.isContentEditable);
    if (box.hidden && !typing && (ev.key === "/" || ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === "k"))) {
      ev.preventDefault(); open();
    }
  });

  function open() {
    lastFocus = document.activeElement;
    chrome();
    box.hidden = false;
    document.body.classList.add("sx-open");
    btn.setAttribute("aria-expanded", "true");
    input.focus();
    render();
    load().then(render, function () {
      body.innerHTML = '<p class="sx-hint">' + t("جستجو فعلاً در دسترس نیست. کمی بعد دوباره امتحان کن.", "Search is not available right now. Please try again shortly.") + "</p>";
    });
  }
  function close() {
    box.hidden = true;
    document.body.classList.remove("sx-open");
    btn.setAttribute("aria-expanded", "false");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  btn.addEventListener("click", open);
  btn.setAttribute("aria-label", "Search | جستجو");

  function markCurrent() {
    var here = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    document.querySelectorAll("header .nav-links a[href]").forEach(function (a) {
      var h = (a.getAttribute("href") || "").split("#")[0].toLowerCase();
      if (h && h === here && here !== "index.html") { a.classList.add("is-current"); a.setAttribute("aria-current", "page"); }
    });
  }

  function init() {
    placeButton();
    markCurrent();
    document.body.appendChild(box);
    // A link with ?q= opens search with that query
    var m = /[?&]q=([^&]+)/.exec(location.search);
    if (m) { open(); input.value = decodeURIComponent(m[1].replace(/\+/g, " ")); render(); }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
