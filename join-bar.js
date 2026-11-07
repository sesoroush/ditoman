/* Ditoman join bar: a slim bar fixed to the bottom of the screen on phones,
   inviting readers to follow the channels. It appears after a little scrolling,
   and stays hidden for 14 days once someone closes it.

   To add Bale or Rubika, put the channel address in CHANNELS below.
   A channel with an empty address is not shown. */
(function () {
  var CHANNELS = [
    { name: "تلگرام", url: "https://t.me/Ditoman_tm", color: "#2aa3e0" },
    { name: "بله", url: "https://ble.ir/Ditoman", color: "#13b886" },
    { name: "اینستاگرام", url: "https://www.instagram.com/ditoman.tmn/", color: "linear-gradient(45deg,#f09433,#dc2743,#bc1888)" },
    { name: "روبیکا", url: "", color: "#e83f6f" }
  ];
  var KEY = "ditoman-join-bar-closed";
  var DAYS = 14;

  var live = CHANNELS.filter(function (c) { return c.url; });
  if (!live.length) return;
  try {
    var closed = Number(localStorage.getItem(KEY) || 0);
    if (closed && Date.now() - closed < DAYS * 864e5) return;
  } catch (e) {}

  var css = [
    ".jb{position:fixed;left:12px;right:12px;bottom:12px;z-index:60;display:none;align-items:center;gap:10px;",
    "padding:10px 10px 10px 14px;border-radius:18px;background:rgba(6,20,24,.96);border:1px solid rgba(127,245,222,.35);",
    "box-shadow:0 10px 30px rgba(0,0,0,.45);direction:rtl;font-family:Vazirmatn,Tahoma,sans-serif;color:#eef6f2;",
    "transform:translateY(140%);transition:transform .3s ease}",
    ".jb.show{transform:none}",
    ".jb p{flex:1;margin:0;font-size:.92rem;line-height:1.5;font-weight:700}",
    ".jb a{flex:none;padding:9px 12px;border-radius:999px;color:#fff;font-weight:800;font-size:.9rem;text-decoration:none}",
    ".jb button{flex:none;width:34px;height:34px;border-radius:50%;border:1px solid rgba(255,255,255,.2);background:none;",
    "color:#eef6f2;font-size:1.1rem;line-height:1;cursor:pointer}",
    ".jb a:focus-visible,.jb button:focus-visible{outline:2px solid #7ff5de;outline-offset:2px}",
    "@media (max-width:900px){.jb{display:flex}body.jb-on{padding-bottom:84px}}",
    "@media (max-width:400px){.jb{gap:6px;padding:8px 8px 8px 10px}.jb p{font-size:.82rem}.jb a{padding:8px 9px;font-size:.8rem}.jb button{width:30px;height:30px}}",
    "@media (prefers-reduced-motion:reduce){.jb{transition:none}}"
  ].join("");
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  var bar = document.createElement("aside");
  bar.className = "jb";
  bar.setAttribute("lang", "fa");
  bar.setAttribute("aria-label", "دنبال کردن دیتومان");
  var text = live.length === 1
    ? "در " + live[0].name + " همراه دیتومان باش"
    : "دیتومان را دنبال کن";
  var html = "<p>" + text + "</p>";
  live.forEach(function (c) {
    html += '<a href="' + c.url + '" target="_blank" rel="noopener noreferrer" style="background:' + c.color + '">' +
      (live.length === 1 ? "عضو شو" : c.name) + "</a>";
  });
  html += '<button type="button" aria-label="بستن">×</button>';
  bar.innerHTML = html;
  document.body.appendChild(bar);

  function reveal() {
    if (window.scrollY < 300) return;
    bar.classList.add("show");
    document.body.classList.add("jb-on");
    window.removeEventListener("scroll", reveal);
  }
  window.addEventListener("scroll", reveal, { passive: true });
  reveal();

  bar.querySelector("button").addEventListener("click", function () {
    bar.classList.remove("show");
    document.body.classList.remove("jb-on");
    try { localStorage.setItem(KEY, String(Date.now())); } catch (e) {}
    setTimeout(function () { bar.remove(); }, 320);
  });
})();
