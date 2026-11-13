/* Ditoman channels: one list of every place to follow Ditoman, drawn the same way on every page.

   To add or change a link, edit CHANNELS below. That is the only place the links live.
   A channel with an empty url is still shown, dimmed and marked "soon", until its link is added.

   Where it appears:
   - inside every existing follow box (.instagram-box, .follow-card). Old Telegram / Bale /
     Instagram profile buttons in those boxes are replaced by the icon row; other buttons
     (a specific Instagram post, Back to Learn, Home) stay.
   - pages with no follow box get one just above the footer.
   Styles live in theme.css (.ch-grid). */
(function () {
  var CHANNELS = [
    { id: "telegram",  fa: "تلگرام",     en: "Telegram",  url: "https://t.me/Ditoman_tm" },
    { id: "bale",      fa: "بله",        en: "Bale",      url: "https://ble.ir/Ditoman" },
    { id: "rubika",    fa: "روبیکا",     en: "Rubika",    url: "" },
    { id: "eitaa",     fa: "ایتا",       en: "Eitaa",     url: "" },
    { id: "instagram", fa: "اینستاگرام", en: "Instagram", url: "https://www.instagram.com/ditoman.tmn/" }
  ];
  // profile links the icon row replaces
  var OLD = /^https?:\/\/(t\.me\/Ditoman_tm|ble\.ir\/Ditoman|(www\.)?instagram\.com\/ditoman\.tmn)\/?$/i;

  function grid() {
    var g = document.createElement("div");
    g.className = "ch-grid";
    CHANNELS.forEach(function (c) {
      var el = document.createElement(c.url ? "a" : "span");
      el.className = "ch ch-" + c.id + (c.url ? "" : " is-soon");
      if (c.url) {
        el.href = c.url;
        el.target = "_blank";
        el.rel = "noopener noreferrer";
      }
      el.innerHTML =
        '<img src="/img/social/' + c.id + '.png" alt="" width="52" height="52" loading="lazy" decoding="async">' +
        '<span lang="fa">' + c.fa + "</span><span lang=\"en\">" + c.en + "</span>" +
        (c.url ? "" : '<small><span lang="fa">به‌زودی</span><span lang="en">Soon</span></small>');
      g.appendChild(el);
    });
    return g;
  }

  function fill(box) {
    if (box.querySelector(".ch-grid")) return;
    var old = [];
    box.querySelectorAll("a[href]").forEach(function (a) {
      if (OLD.test(a.getAttribute("href"))) old.push(a);
    });
    var g = grid();
    var anchor = old.length ? old[0].parentNode : box.querySelector(".cta-row, .follow-actions, .buttons");
    if (anchor && anchor !== box) anchor.parentNode.insertBefore(g, anchor);
    else box.appendChild(g);
    old.forEach(function (a) { a.remove(); });
    box.querySelectorAll(".cta-row, .follow-actions, .buttons").forEach(function (row) {
      if (!row.querySelector("a")) row.remove();
    });
  }

  var boxes = document.querySelectorAll(".instagram-box, .follow-card");
  if (boxes.length) {
    boxes.forEach(fill);
    return;
  }
  var box = document.createElement("aside");
  box.className = "jb-inline";
  box.setAttribute("aria-label", "Follow Ditoman");
  box.innerHTML =
    '<p><span lang="fa">با هم دنبال می‌کنیم</span><span lang="en">Follow along</span>' +
    '<small><span lang="fa">گزارش‌ها و آموزش‌های تازه، هر روز در کانال‌های دیتومان</span>' +
    '<span lang="en">New reports and lessons every day on Ditoman’s channels</span></small></p>';
  box.appendChild(grid());
  var foot = document.querySelector("body > footer") || document.querySelector("footer");
  if (foot && foot.parentNode) foot.parentNode.insertBefore(box, foot);
  else document.body.appendChild(box);
})();
