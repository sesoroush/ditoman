/* Ditoman join bar: an inline "follow us" block placed just above the footer.
   It no longer floats over the page, so it never covers what people are reading.
   Pages that already have their own follow section (marked data-follow) skip it.

   To add Rubika, put the channel address in CHANNELS below.
   A channel with an empty address is not shown. Styles live in theme.css (.jb-inline). */
(function () {
  var CHANNELS = [
    { name: "تلگرام", url: "https://t.me/Ditoman_tm", bg: "linear-gradient(100deg,#7ff5de,#3ddc97)", fg: "#05110d" },
    { name: "بله", url: "https://ble.ir/Ditoman", bg: "#3ddc97", fg: "#05110d" },
    { name: "اینستاگرام", url: "https://www.instagram.com/ditoman.tmn/", bg: "linear-gradient(45deg,#f09433,#dc2743,#bc1888)", fg: "#fff" },
    { name: "روبیکا", url: "", bg: "#e83f6f", fg: "#fff" }
  ];
  if (document.querySelector("[data-follow], .instagram-box")) return;
  var live = CHANNELS.filter(function (c) { return c.url; });
  if (!live.length) return;

  var box = document.createElement("aside");
  box.className = "jb-inline";
  box.setAttribute("lang", "fa");
  box.setAttribute("aria-label", "دنبال کردن دیتومان");
  var html = "<p>دیتومان را دنبال کن<small>گزارش‌ها و آموزش‌های تازه، هر روز در کانال‌های دیتومان</small></p>";
  live.forEach(function (c) {
    html += '<a href="' + c.url + '" target="_blank" rel="noopener noreferrer" style="background:' + c.bg + ';color:' + c.fg + '">' + c.name + "</a>";
  });
  box.innerHTML = html;
  var foot = document.querySelector("body > footer") || document.querySelector("footer");
  if (foot && foot.parentNode) foot.parentNode.insertBefore(box, foot);
  else document.body.appendChild(box);
})();
