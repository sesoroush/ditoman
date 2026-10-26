/* Ditoman quick-jump menu: opens a full-screen panel of destinations from the header. */
(function () {
  var btn = document.getElementById("menuBtn");
  var panel = document.getElementById("menuPanel");
  if (!btn || !panel) return;

  function setOpen(open) {
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("menu-open", open);
    if (open) {
      panel.hidden = false;
      requestAnimationFrame(function () { panel.classList.add("show"); });
      var first = panel.querySelector("a");
      if (first) first.focus({ preventScroll: true });
    } else {
      panel.classList.remove("show");
      setTimeout(function () { if (!panel.classList.contains("show")) panel.hidden = true; }, 220);
    }
  }

  btn.addEventListener("click", function () {
    setOpen(btn.getAttribute("aria-expanded") !== "true");
  });

  panel.addEventListener("click", function (e) {
    if (e.target.closest("a")) setOpen(false);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      btn.focus();
    }
  });

  window.addEventListener("resize", function () {
    if (window.innerWidth > 960 && btn.getAttribute("aria-expanded") === "true") setOpen(false);
  });

  /* Homepage: highlight the section currently on screen in the desktop menu. */
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
  if (!links.length || !("IntersectionObserver" in window)) return;
  var map = {};
  links.forEach(function (a) {
    var s = document.querySelector(a.getAttribute("href"));
    if (s) map[s.id] = a;
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting && map[en.target.id]) {
        links.forEach(function (a) { a.classList.remove("active"); });
        map[en.target.id].classList.add("active");
      }
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
})();
