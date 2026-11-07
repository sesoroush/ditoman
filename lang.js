/* Ditoman language switch.
   Persian is the default. The button in the header switches the page to English,
   and the choice is remembered.

   Three ways a piece of text gets both languages:
   1. data-en="..." on an element: the element shows Persian, data-en holds the English.
   2. A bilingual pair already in the page (English text with a lang="fa" twin):
      the language not chosen is hidden.
   3. The DICT below: English text that appears on its own is shown in Persian.
      Add new lines here as pages are translated. */
(function () {
  var DICT = {
    // navigation and menu
    "Learn": "آموزش", "Iran": "ایران", "Navigator": "راهنمای مجوزها", "Prices": "قیمت‌ها",
    "Calendar": "تقویم", "Whitepaper": "وایت‌پیپر", "Posts": "یادداشت‌ها", "Companies": "شرکت‌ها",
    "Start learning": "شروع یادگیری", "Menu": "منو", "Telegram": "تلگرام", "Instagram": "اینستاگرام",
    "Short bilingual lessons with quizzes": "درس‌های کوتاه دوزبانه با آزمونک",
    "Industry, energy, transport, mines, tech, tourism": "صنعت، انرژی، حمل‌ونقل، معدن، فناوری، گردشگری",
    "Who licenses what, in Iran": "کدام نهاد در ایران چه مجوزی می‌دهد",
    "What if your money had an expiry date?": "اگر پولت تاریخ انقضا داشت؟",
    "Contract, facts and honest disclosure": "قرارداد، واقعیت‌ها و افشای صادقانه",
    "Every channel post, on the web": "همه‌ی پست‌های کانال، روی وب",
    "The full direction, as a PDF": "مسیر کامل پروژه، فایل PDF",
    "What moves markets, every day": "آنچه هر روز بازار را تکان می‌دهد",
    "Dollar, gold and every daily report": "دلار، طلا و همه‌ی گزارش‌های روزانه",
    "Iranian companies, with sources": "شرکت‌های ایرانی، با منبع",
    "Join the Telegram channel": "عضویت در کانال تلگرام",

    // three pillars
    "One permanent editorial rule across all three: real knowledge and real achievement, no political commentary from any side.":
      "یک قاعده‌ی ثابت در هر سه: دانش واقعی و دستاورد واقعی، بدون اظهارنظر سیاسی به نفع یا علیه هیچ طرفی.",
    "How blockchains work, how to check a token before you touch it, and how to protect yourself from scams.":
      "بلاک‌چین چطور کار می‌کند، هر توکنی را پیش از خرید چطور بررسی کنیم و چطور از کلاهبرداری در امان بمانیم.",
    "Honest analysis of the shifts coming, read from where our audience actually stands.":
      "تحلیل صادقانه‌ی تغییرهای پیش رو، از جایی که مخاطب ما واقعاً ایستاده است.",
    "Documenting people and businesses who keep building under pressure, on their own terms.":
      "روایت مستند آدم‌ها و کسب‌وکارهایی که در سخت‌ترین شرایط، چراغ کار و تولید را روشن نگه داشته‌اند.",

    // what Iran has
    "A structured map of what is made, mined, moved and seen in Iran: six branches, their official sub-branches, the leading companies, and a source for every number.":
      "نقشه‌ای منظم از آنچه در ایران ساخته، استخراج، جابه‌جا و دیده می‌شود: شش شاخه، زیرشاخه‌های رسمی، شرکت‌های پیشرو و منبع هر عدد.",
    "What Iran Has": "ایران چه دارد",
    "From dairy to steel and medicine": "از لبنیات تا فولاد و دارو",
    "Oil, gas, power, renewables, water": "نفت، گاز، برق، انرژی تجدیدپذیر، آب",
    "Roads, rail, ports, airports, logistics": "جاده، ریل، بندر، فرودگاه، لجستیک",
    "Iron, copper, zinc, stone, minerals": "آهن، مس، روی، سنگ و مواد معدنی",
    "Platforms, fintech, knowledge-based firms, health": "پلتفرم‌ها، فین‌تک، شرکت‌های دانش‌بنیان، سلامت",
    "World heritage, nature, crafts, food, art": "میراث جهانی، طبیعت، صنایع‌دستی، خوراک، هنر",
    "Who licenses what? The map of ministries and permits, from company registration to each sector's licence":
      "چه نهادی چه مجوزی می‌دهد؟ نقشه‌ی وزارتخانه‌ها و مجوزها، از ثبت شرکت تا مجوز هر حوزه",

    // companies and stories
    "History, products, leadership and figures, sector by sector, with a source for each number.":
      "سابقه، محصول، مدیران و آمار، حوزه به حوزه، با منبع هر عدد.",
    "View the record": "دیدن پرونده", "See all companies": "همه‌ی شرکت‌ها",
    "Iranian industry, new technology and what they mean for the future.":
      "صنعت ایران، فناوری‌های تازه و معنای آن‌ها برای آینده.",
    "Read the story": "خواندن روایت",

    // story
    "Ditoman takes its name from the Toman, the everyday name for Iranian money: a \"digital Toman\". TMN was deployed on BNB Smart Chain in February 2022 with one question behind it: can knowledge itself carry real value?":
      "نام دیتومان از «تومان» آمده، همان اسمی که هر روز برای پول ایران به کار می‌بریم: یک «تومان دیجیتال». توکن TMN در فوریه‌ی ۲۰۲۲ روی شبکه‌ی BNB Smart Chain ساخته شد، با یک پرسش: آیا خود دانش می‌تواند ارزش واقعی داشته باشد؟",
    "For nearly four years we stayed deliberately quiet. No marketing, no token sale, no launch. That history is on-chain for anyone to check, and it is the clearest sign this was never built for a quick pump.":
      "نزدیک چهار سال آگاهانه بی‌صدا ماندیم: نه تبلیغ، نه فروش توکن، نه رونمایی. این سابقه روی بلاک‌چین ثبت است و هر کسی می‌تواند بررسی‌اش کند؛ روشن‌ترین نشانه که این پروژه هیچ‌وقت برای جهش سریع قیمت ساخته نشد.",
    "See the full history": "دیدن تاریخچه‌ی کامل",

    // lessons
    "Short lessons by topic, about five minutes each, in both languages, each ending with a quiz.":
      "درس‌های کوتاه موضوعی، هر کدام حدود پنج دقیقه، به دو زبان و با یک آزمونک در پایان.",
    "Newest lesson": "تازه‌ترین درس",
    "Central bank digital currencies and programmable money: what is real, what is exaggerated, and where Iran's digital rial stands.":
      "پول دیجیتال بانک مرکزی و پول برنامه‌پذیر: چه چیزی واقعی است، چه چیزی اغراق، و ریال دیجیتال ایران کجا ایستاده است.",
    "Read the lesson": "خواندن درس", "See all lessons": "همه‌ی درس‌ها",
    "Markets": "بازار", "Safety": "امنیت", "Bitcoin": "بیت‌کوین", "Basics": "مبانی",
    "How big news moves Bitcoin": "خبرهای بزرگ چطور قیمت بیت‌کوین را تکان می‌دهند",
    "Five questions to ask before you buy": "پنج پرسش پیش از خرید",
    "How to check any token before you touch it": "هر توکنی را پیش از خرید چطور بررسی کنیم",
    "Who is Satoshi Nakamoto?": "ساتوشی ناکاموتو کیست؟",
    "Why Bitcoin was created": "بیت‌کوین چرا ساخته شد",
    "Why blockchain matters": "چرا بلاک‌چین مهم است",
    "What is blockchain?": "بلاک‌چین چیست؟",
    "Lessons, short news explainers and updates, in Farsi and English. No signals, no hype.":
      "درس‌ها، توضیح کوتاه خبرها و تازه‌ها، به فارسی و انگلیسی. بدون سیگنال، بدون هیاهو.",
    "Join the channel": "عضویت در کانال",

    // TMN
    "TMN is a tool, not the point.": "TMN ابزار است، نه هدف.",
    "TMN is the BEP-20 token behind Ditoman, planned for recognising real learning and contribution. It is not an investment product and we do not ask anyone to buy it.":
      "TMN توکن BEP-20 دیتومان است و برای قدردانی از یادگیری و مشارکت واقعی طراحی شده. محصول سرمایه‌گذاری نیست و از کسی نمی‌خواهیم آن را بخرد.",
    "Several unrelated tokens use the ticker TMN. This is the only official contract:":
      "چند توکن بی‌ربط دیگر هم نماد TMN دارند. تنها قرارداد رسمی این است:",
    "Copy": "کپی", "Token facts and disclosure": "واقعیت‌های توکن و افشا", "Verify on BscScan": "بررسی در BscScan",
    "Network": "شبکه", "Source code": "کد منبع", "Verified": "تأییدشده", "Ownership": "مالکیت",
    "Renounced": "واگذارشده", "New minting": "ضرب توکن جدید", "Impossible": "غیرممکن",
    "Out of circulation": "خارج از گردش", "About 20% of supply": "حدود ۲۰٪ عرضه",
    "Liquidity": "نقدینگی", "Very low": "بسیار کم", "Supply": "عرضه",
    "Concentrated with founders": "متمرکز نزد بنیان‌گذاران",

    // roadmap
    "Phases, not dates. We report progress honestly, including what did not work.":
      "مرحله‌به‌مرحله، نه با تاریخ. پیشرفت را صادقانه گزارش می‌کنیم، حتی آنچه جواب نداد.",
    "Complete": "انجام شد", "In progress": "در حال انجام", "Next": "بعدی", "Later": "بعدتر",
    "Foundation": "پایه‌گذاری",
    "Contract verified, ownership renounced, about 20% of supply out of circulation, bilingual lessons published, Whitepaper V5 final.":
      "قرارداد تأیید شد، مالکیت واگذار شد، حدود ۲۰٪ عرضه از گردش خارج شد، درس‌های دوزبانه منتشر شد و وایت‌پیپر V5 نهایی شد.",
    "Community structure": "ساختار جامعه",
    "A Telegram community with real rules, seeded lessons and clear onboarding, before any invitation.":
      "جامعه‌ای در تلگرام با قواعد روشن، درس‌های آماده و راهنمای ورود، پیش از هر دعوتی.",
    "Controlled growth": "رشد سنجیده",
    "Joining Persian-language crypto and diaspora communities, and the first public supply removal with proof.":
      "پیوستن به جامعه‌های فارسی‌زبان کریپتو و ایرانیان خارج از کشور، و نخستین خروج عمومی توکن از گردش با مدرک.",
    "Learn-and-earn pilot": "آزمایش «یاد بگیر و پاداش بگیر»",
    "Small, transparent rewards tied to verifiable learning, with a public review of results.":
      "پاداش‌های کوچک و شفاف برای یادگیری قابل‌تأیید، با بررسی عمومی نتیجه‌ها.",

    // questions
    "What is Ditoman?": "دیتومان چیست؟",
    "A bilingual education project built around three pillars: practical crypto and financial literacy, honest analysis of AI, energy and the future of work, and coverage of real achievements by Iranian people and businesses.":
      "یک پروژه‌ی آموزشی دوزبانه با سه محور: سواد کاربردی کریپتو و مالی، تحلیل صادقانه‌ی هوش مصنوعی، انرژی و آینده‌ی کار، و روایت دستاوردهای واقعی مردم و کسب‌وکارهای ایرانی.",
    "Should I buy TMN?": "آیا TMN بخرم؟",
    "Is this financial advice?": "آیا این توصیه‌ی مالی است؟",
    "No. Ditoman is an education project. Nothing here is investment advice, and the lessons are built to help you decide for yourself.":
      "نه. دیتومان یک پروژه‌ی آموزشی است. هیچ مطلبی در این سایت توصیه‌ی سرمایه‌گذاری نیست و درس‌ها برای این ساخته شده‌اند که خودت تصمیم بگیری.",
    "Why no politics?": "چرا سیاست نه؟",
    "It is a permanent editorial rule. We document real knowledge and real achievement, and stay out of political commentary from any side.":
      "این یک قاعده‌ی دائمی تحریریه است. دانش و دستاورد واقعی را ثبت می‌کنیم و از اظهارنظر سیاسی به نفع یا علیه هیچ طرفی دور می‌مانیم.",
    "Will learners be rewarded?": "آیا به یادگیرنده‌ها پاداش داده می‌شود؟",
    "That is the plan for Phase 4: a small learn-and-earn pilot, tested openly before anything bigger. Until it exists, we won't promise rewards.":
      "این برنامه‌ی مرحله‌ی چهارم است: آزمایشی کوچک و شفاف، پیش از هر کار بزرگ‌تر. تا وقتی راه نیفتاده، قول پاداش نمی‌دهیم.",

    // whitepapers and closing
    "One document sets the direction. Read it before you trust anything we say.":
      "یک سند مسیر را مشخص می‌کند. پیش از اینکه به حرف ما اعتماد کنی، آن را بخوان.",
    "Whitepaper V5: Final direction": "وایت‌پیپر V5: مسیر نهایی",
    "What Ditoman is, the three pillars, full token facts, supply plan, roadmap and an honest risk disclosure. This is the reference for everything on this site.":
      "دیتومان چیست، سه محور، همه‌ی واقعیت‌های توکن، برنامه‌ی عرضه، نقشه‌ی راه و افشای صادقانه‌ی ریسک‌ها. مرجع همه‌ی مطالب این سایت.",
    "Read V5 (PDF)": "خواندن V5 (PDF)", "Earlier version (V1)": "نسخه‌ی قبلی (V1)",
    "The first whitepaper from 2022, kept as a public record of where the project started. Some figures and plans in it are out of date. V5 replaces it.":
      "نخستین وایت‌پیپر از ۲۰۲۲، که به‌عنوان سند عمومی نقطه‌ی شروع پروژه نگه داشته شده. بعضی اعداد و برنامه‌هایش قدیمی‌اند و V5 جایگزین آن است.",
    "Early foundation": "پایه‌ی اولیه", "Open PDF": "باز کردن PDF",
    "New lessons arrive in our Telegram channel automatically, with a visual summary on Instagram.":
      "درس‌های تازه خودکار به کانال تلگرام و بله می‌رسند و خلاصه‌ی تصویری‌شان در اینستاگرام.",
    "Join on Telegram": "عضویت در تلگرام", "Follow on Instagram": "دنبال کردن در اینستاگرام"
  };

  var KEY = "ditoman-lang";
  var root = document.documentElement;
  var norm = function (s) { return s.replace(/\s+/g, " ").trim(); };

  // 3. dictionary: leaf elements whose whole text is a known English string
  var leaves = document.querySelectorAll("body *:not(script):not(style)");
  for (var i = 0; i < leaves.length; i++) {
    var el = leaves[i];
    if (el.closest("svg") || el.hasAttribute("data-en") || el.closest("body [lang='fa']") || el.closest("[data-en]")) continue;
    if (el.children.length) continue;
    var key = norm(el.textContent);
    if (key && DICT.hasOwnProperty(key)) { el.setAttribute("data-en", el.innerHTML); el.innerHTML = DICT[key]; }
  }

  // 2. bilingual pairs: wrap loose English text next to a Persian twin, and mark English siblings
  var twins = document.querySelectorAll("body [lang='fa']");
  for (var j = 0; j < twins.length; j++) {
    var fa = twins[j], parent = fa.parentElement;
    if (!parent || parent.closest("[data-en]") || parent === document.body) continue;
    var nodes = Array.prototype.slice.call(parent.childNodes);
    nodes.forEach(function (n) {
      if (n.nodeType === 3 && norm(n.textContent) && parent.getAttribute("lang") !== "fa") {
        var span = document.createElement("span");
        span.setAttribute("lang", "en");
        span.className = "lang-en";
        parent.insertBefore(span, n);
        span.appendChild(n);
      }
    });
    var prev = fa.previousElementSibling;
    if (prev && !prev.hasAttribute("lang") && !prev.hasAttribute("data-en") &&
        (prev.tagName === fa.tagName || /fa-sub|fa-line|mt-fa|co-fa/.test(fa.className))) {
      prev.setAttribute("lang", "en");
      prev.classList.add("lang-en");
    }
  }

  // 1. swap data-en elements
  var swaps = document.querySelectorAll("[data-en]");
  for (var k = 0; k < swaps.length; k++) swaps[k].setAttribute("data-fa", swaps[k].innerHTML);

  function apply(lang) {
    root.setAttribute("data-lang", lang);
    root.lang = lang;
    root.dir = lang === "en" ? "ltr" : "rtl";
    for (var m = 0; m < swaps.length; m++) {
      swaps[m].innerHTML = swaps[m].getAttribute(lang === "en" ? "data-en" : "data-fa");
    }
    document.querySelectorAll("[data-en-label]").forEach(function (n) {
      if (!n.hasAttribute("data-fa-label")) n.setAttribute("data-fa-label", n.getAttribute("aria-label") || "");
      n.setAttribute("aria-label", n.getAttribute(lang === "en" ? "data-en-label" : "data-fa-label"));
    });
    if (btn) {
      btn.textContent = lang === "en" ? "فارسی" : "EN";
      btn.setAttribute("lang", lang === "en" ? "fa" : "en");
      btn.setAttribute("aria-label", lang === "en" ? "نمایش به فارسی" : "Show in English");
    }
    try { localStorage.setItem(KEY, lang); } catch (e) {}
  }

  // toggle button in the header
  var btn = document.createElement("button");
  btn.type = "button";
  btn.className = "lang-btn";
  var spot = document.querySelector(".nav-right");
  if (spot) spot.insertBefore(btn, spot.firstChild);
  btn.addEventListener("click", function () {
    apply(root.getAttribute("data-lang") === "en" ? "fa" : "en");
  });

  apply(root.getAttribute("data-lang") === "en" ? "en" : "fa");
})();
