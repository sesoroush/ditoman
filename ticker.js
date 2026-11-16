/* Ditoman price strip: one line of prices under the site header, on every page.
   Swipe it sideways; any price opens the prices page.

   First it shows the site's own market file (market/latest.json, refreshed by the market workflow),
   so it works everywhere the site works. Then it asks Nobitex and CoinGecko for live tether and
   bitcoin prices and, if they answer, replaces those two numbers and marks the strip "live".
   Loaded by search.js. Styles are in theme.css (.tk). */
(function () {
  var header = document.querySelector("header");
  if (!header || document.querySelector(".tk")) return;
  var en = document.documentElement.getAttribute("data-lang-lock") === "en";
  var pricesUrl = en ? "prices.en.html" : "prices.html";
  if (/(^|\/)prices(\.en)?\.html$/.test(location.pathname)) return; // the prices page already shows all of this

  var bar = document.createElement("div");
  bar.className = "tk";
  bar.innerHTML = '<div class="tk-track" tabindex="0" aria-label="Prices"></div>';
  header.parentNode.insertBefore(bar, header.nextSibling);
  var track = bar.firstChild;

  var nf = function (v, d) { return Number(v).toLocaleString("en-US", { maximumFractionDigits: d || 0, minimumFractionDigits: d || 0 }); };
  var both = function (fa, e) { return '<span lang="fa">' + fa + '</span><span lang="en">' + e + "</span>"; };
  var data = {}, live = false, stamp = "";

  function item(key, fa, e, value, unitFa, unitEn, chg) {
    var c = "";
    if (chg != null && !isNaN(chg) && Math.abs(chg) >= 0.005) {
      c = '<i class="' + (chg >= 0 ? "up" : "dn") + '">' + (chg >= 0 ? "▲" : "▼") + " " + Math.abs(chg).toFixed(2) + "%</i>";
    }
    return '<a class="tk-item" data-k="' + key + '" href="' + pricesUrl + '"><span class="tk-l">' + both(fa, e) + "</span><b>" + value +
      "</b><small>" + both(unitFa, unitEn) + "</small>" + c + "</a>";
  }

  function draw() {
    var h = "", d = data;
    h += '<a class="tk-item tk-head" href="' + pricesUrl + '"><em class="' + (live ? "on" : "") + '"></em>' +
      (live ? both("قیمت زنده", "Live prices") : both("قیمت‌ها", "Prices")) + (stamp ? "<small>" + stamp + "</small>" : "") + "</a>";
    if (d.usdt) h += item("usdt", "تتر", "Tether", nf(d.usdt.v), "تومان", "toman", d.usdt.c);
    if (d.usd) h += item("usd", "دلار", "US dollar", nf(d.usd.v), "تومان", "toman", d.usd.c);
    if (d.gold18) h += item("gold18", "طلای ۱۸ عیار", "18k gold, gram", nf(d.gold18.v / 1e6, 2), "میلیون تومان", "M toman", d.gold18.c);
    if (d.coin) h += item("coin", "سکه امامی", "Emami coin", nf(d.coin.v / 1e6, 1), "میلیون تومان", "M toman", d.coin.c);
    if (d.btc) h += item("btc", "بیت‌کوین", "Bitcoin", nf(d.btc.v), "دلار", "USD", d.btc.c);
    if (d.xau) h += item("xau", "اونس طلا", "Gold, ounce", nf(d.xau.v), "دلار", "USD", d.xau.c);
    if (d.brent) h += item("brent", "نفت برنت", "Brent oil", nf(d.brent.v, 1), "دلار", "USD", d.brent.c);
    if (d.eur) h += item("eur", "یورو", "Euro", nf(d.eur.v), "تومان", "toman", d.eur.c);
    h += '<a class="tk-item tk-all" href="' + pricesUrl + '">' + both("همه‌ی قیمت‌ها و نمودارها ←", "All prices and charts →") + "</a>";
    var keep = track.scrollLeft;
    track.innerHTML = h;
    track.scrollLeft = keep;
  }

  function hhmm(dt) {
    var p = function (n) { return (n < 10 ? "0" : "") + n; };
    return p(dt.getHours()) + ":" + p(dt.getMinutes());
  }

  fetch("market/latest.json", { cache: "no-cache" }).then(function (r) { return r.json(); }).then(function (j) {
    var ir = j.iran || {}, g = j.global || {};
    var put = function (k, src, field) { if (src && src[field] != null) data[k] = data[k] || { v: +src[field], c: src.chg }; };
    put("usd", ir.usd, "value_toman"); put("eur", ir.eur, "value_toman");
    put("gold18", ir.gold18_gram, "value_toman"); put("coin", ir.coin_emami, "value_toman");
    put("btc", g.btc, "value"); put("xau", g.gold, "value"); put("brent", g.brent, "value");
    if (!live && j.fetched_utc) stamp = hhmm(new Date(j.fetched_utc));
    draw();
    pull();
    setInterval(pull, 60000);
  }).catch(function () { bar.remove(); });

  function pull() {
    if (document.hidden) return;
    var got = false, done = 0;
    var fin = function () { if (++done < 2) return; if (got) { live = true; stamp = hhmm(new Date()); draw(); } };
    fetch("https://api.nobitex.ir/market/stats?srcCurrency=usdt&dstCurrency=rls", { cache: "no-store" })
      .then(function (r) { return r.json(); }).then(function (j) {
        var s = (j.stats || {})["usdt-rls"];
        if (s && +s.latest) { data.usdt = { v: +s.latest / 10, c: +s.dayChange }; got = true; }
      }).catch(function () {}).then(fin);
    fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true", { cache: "no-store" })
      .then(function (r) { return r.json(); }).then(function (j) {
        if (j.bitcoin && j.bitcoin.usd) { data.btc = { v: j.bitcoin.usd, c: j.bitcoin.usd_24h_change }; got = true; }
      }).catch(function () {}).then(fin);
  }
})();
