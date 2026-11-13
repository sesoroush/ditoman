/* Ditoman learn-and-earn: ten lessons, a ten-question test, a claim code.

   Settings live in CONFIG. The test runs entirely in the browser; the code is a short
   fingerprint of the wallet address, so the team can check that a code and an address
   belong together (open learn-earn.html#check). Payouts are reviewed and sent by hand.
*/
(function () {
  var CONFIG = {
    rewardFa: "معادل حدود ۱ دلار توکن TMN",
    rewardEn: "About $1 worth of TMN",
    capFa: "",          // e.g. "برای ۱۰۰ نفر اول"
    capEn: "",          // e.g. "For the first 100 people"
    telegram: "",       // username that receives claims, without @
    bale: "",           // Bale username that receives claims, without @
    pass: 8,
    salt: "ditoman-learn-earn-1|"
  };

  var LESSONS = [
    ["lesson01.html", "بلاکچین چیست؟", "What is blockchain?"],
    ["lesson02.html", "چرا بلاکچین مهم است", "Why blockchain matters"],
    ["lesson03.html", "چرا بیت‌کوین ساخته شد", "Why Bitcoin was created"],
    ["lesson04.html", "ساتوشی ناکاموتو کیست؟", "Who is Satoshi Nakamoto?"],
    ["lesson05.html", "پیش از دست زدن به هر توکن، این‌ها را بررسی کنید", "How to check any token before you touch it"],
    ["lesson06.html", "پنج پرسش پیش از خرید", "Five questions to ask before you buy"],
    ["lesson07.html", "خبرهای بزرگ چطور قیمت بیت‌کوین را تکان می‌دهند", "How big news moves Bitcoin"],
    ["lesson08.html", "اگر پولت تاریخ انقضا داشت؟", "What if your money had an expiry date?"],
    ["lesson09.html", "قفل لیکوئیدیتی واقعاً یعنی چه؟", "What does a liquidity lock actually mean?"],
    ["lesson10.html", "چرا قیمت یک‌دفعه می‌ریزد؟", "Why do prices suddenly crash?"]
  ];

  // Two questions per lesson; each attempt draws one. The first option is the right one
  // (options are shuffled on screen).
  var BANK = [
    [
      { fa: "بلاکچین بیشتر برای چه کاری استفاده می‌شود؟", en: "What is blockchain mainly used for?",
        o: [["ثبت اطلاعات به شکلی شفاف و قابل بررسی", "Recording information in a transparent, verifiable way"],
            ["جایگزین کردن همه‌ی وب‌سایت‌ها", "Replacing all websites"],
            ["پنهان کردن همیشگی همه‌ی تراکنش‌ها", "Hiding every transaction forever"],
            ["حذف نیاز به اینترنت", "Removing the need for the internet"]] },
      { fa: "تمرکززدایی در بلاکچین یعنی چه؟", en: "What does decentralization mean in blockchain?",
        o: [["کنترل و داده‌ها میان یک شبکه پخش شده‌اند", "Control and data are spread across a network"],
            ["یک شرکت همه‌ی سوابق را کنترل می‌کند", "One company controls all records"],
            ["شبکه در اختیار یک بانک است", "A single bank runs the network"],
            ["کاربران نمی‌توانند چیزی را بررسی کنند", "Users cannot verify anything"]] }
    ],
    [
      { fa: "ایده‌ی اصلی درس «چرا بلاکچین مهم است» چیست؟", en: "What is the main idea of “Why blockchain matters”?",
        o: [["بلاکچین شیوه‌ی کار کردن اعتماد را تغییر می‌دهد", "Blockchain changes how trust works"],
            ["بلاکچین فقط درباره‌ی خرید و فروش کوین است", "Blockchain is only about trading coins"],
            ["بلاکچین نیاز به همه‌ی سیستم‌ها را از بین می‌برد", "Blockchain removes the need for all systems"],
            ["بلاکچین فقط برای بانک‌ها مفید است", "Blockchain is only useful for banks"]] },
      { fa: "بلاکچین اعتماد را به کدام سمت می‌برد؟", en: "Where does blockchain move trust?",
        o: [["به سمت سیستم‌های شفاف و قابل بررسی", "Toward transparent, verifiable systems"],
            ["به سمت سیستم‌های پنهان", "Toward hidden systems"],
            ["به سمت یک شرکت واحد", "Toward a single company"],
            ["فقط به سمت سوابق خصوصی", "Toward private records only"]] }
    ],
    [
      { fa: "بیت‌کوین در اصل پاسخی به چه مشکلی بود؟", en: "Bitcoin was mainly a response to what problem?",
        o: [["اعتمادی که بیش از حد به نهادهای متمرکز و اجازه‌ی آن‌ها وابسته بود", "Trust that depended too much on central institutions and their permission"],
            ["کمبود اسکناس کاغذی", "A shortage of paper money"],
            ["کند بودن وب‌سایت‌ها", "Slow websites"],
            ["ممنوع شدن کارت‌های اعتباری", "A ban on credit cards"]] },
      { fa: "بیت‌کوین درباره‌ی جابه‌جایی ارزش در اینترنت چه چیزی را نشان داد؟", en: "What did Bitcoin show about moving value on the internet?",
        o: [["ارزش می‌تواند بدون دروازه‌بان مرکزی در اینترنت جابه‌جا شود", "Value can move online without a central gatekeeper"],
            ["فقط بانک‌ها می‌توانند ارزش را آنلاین جابه‌جا کنند", "Only banks can move value online"],
            ["پول هرگز نمی‌تواند دیجیتال باشد", "Money can never be digital"],
            ["هر پرداختی به تأیید دولت نیاز دارد", "Every payment needs government approval"]] }
    ],
    [
      { fa: "ساتوشی ناکاموتو کیست؟", en: "Who is Satoshi Nakamoto?",
        o: [["نامی که سازنده یا سازندگان ناشناس بیت‌کوین با آن شناخته می‌شوند", "The name used by the unknown creator or creators of Bitcoin"],
            ["مدیرعامل فعلی بیت‌کوین", "Bitcoin's current CEO"],
            ["رئیس بانک مرکزی ژاپن", "The governor of Japan's central bank"],
            ["شرکتی که مالک بیت‌کوین است", "The company that owns Bitcoin"]] },
      { fa: "چرا بیت‌کوین بعد از کنار رفتن ساتوشی به کارش ادامه داد؟", en: "Why did Bitcoin keep working after Satoshi stepped away?",
        o: [["چون قواعد باز آن به دیگران اجازه داد شبکه را بررسی، اجرا و حفظ کنند", "Its open rules let others verify, run and protect the network"],
            ["چون یک شرکت اداره‌اش را به دست گرفت", "A company took it over"],
            ["چون یک دولت دوباره راهش انداخت", "A government restarted it"],
            ["چون ساتوشی هنوز پنهانی کنترلش می‌کند", "Satoshi still controls it in secret"]] }
    ],
    [
      { fa: "اگر تابع owner یک قرارداد آدرسی تماماً صفر برگرداند، یعنی چه؟", en: "If a contract's owner function returns an all-zero address, what does it mean?",
        o: [["مالکیت واگذار شده و دیگر نمی‌شود از توابع مخصوص مالک استفاده کرد", "Ownership was renounced and owner-only functions can no longer be used"],
            ["قرارداد خراب است", "The contract is broken"],
            ["توکن حذف شده است", "The token has been deleted"],
            ["حالا هر کسی می‌تواند توکن جدید بسازد", "Anyone can now create new tokens"]] },
      { fa: "چرا تمرکز عرضه‌ی یک توکن اهمیت دارد؟", en: "Why does supply concentration matter?",
        o: [["تعداد کمی دارنده می‌توانند با یک تصمیم کل بازار را جابه‌جا کنند", "A few holders can move the whole market with one decision"],
            ["همیشه یعنی پروژه صادق نیست", "It always means the project is dishonest"],
            ["قرارداد را غیرقابل تأیید می‌کند", "It makes the contract unverifiable"],
            ["مانع لیست شدن توکن در هر جایی می‌شود", "It stops the token being listed anywhere"]] }
    ],
    [
      { fa: "کدام‌یک دلیل واقعی برای انتظار افزایش ارزش یک توکن است؟", en: "Which is a real reason to expect a token to gain value?",
        o: [["آدم‌های بیشتری از کاری که انجام می‌دهد استفاده می‌کنند", "More people are using what it does"],
            ["قیمتش هفته‌ی پیش بالا رفت", "Its price rose last week"],
            ["یک دوست درباره‌اش مطمئن است", "A friend is certain about it"],
            ["همه در اینترنت درباره‌اش حرف می‌زنند", "Everyone online is talking about it"]] },
      { fa: "چرا عجله نشانه‌ی هشدار به حساب می‌آید؟", en: "Why is urgency treated as a warning sign?",
        o: [["چون فشار برای تصمیم گرفتن پیش از فکر کردن، ویژگی رایج دست‌کاری است", "Pressure to act before thinking is a common feature of manipulation"],
            ["چون فرصت‌های خوب همیشه کُند پیش می‌روند", "Good opportunities are always slow"],
            ["چون تصمیم سریع همیشه اشتباه است", "Fast decisions are always wrong"],
            ["چون بازار شب‌ها تعطیل است", "Markets close at night"]] }
    ],
    [
      { fa: "به ساده‌ترین بیان، نرخ بهره چیست؟", en: "In the simplest terms, what is an interest rate?",
        o: [["قیمت قرض گرفتن پول", "The price of borrowing money"],
            ["مالیاتی بر کریپتو", "A tax on crypto"],
            ["قیمت بیت‌کوین", "The price of Bitcoin"],
            ["کارمزدی که به صرافی‌ها پرداخت می‌شود", "A fee paid to exchanges"]] },
      { fa: "وقتی می‌گویند نتیجه‌ای «از قبل در قیمت لحاظ شده»، یعنی چه؟", en: "What does it mean when an outcome is “priced in”?",
        o: [["بازار از قبل روی نتیجه‌ی مورد انتظار حرکت کرده است", "The market already moved in advance on the expected result"],
            ["تصمیم لغو شده است", "The decision has been cancelled"],
            ["قیمت دیگر نمی‌تواند تغییر کند", "The price can no longer change"],
            ["صرافی‌ها قیمت ثابتی تعیین کرده‌اند", "Exchanges have fixed the price"]] }
    ],
    [
      { fa: "پول دیجیتال بانک مرکزی (CBDC) را چه کسی منتشر می‌کند؟", en: "Who issues a central bank digital currency (CBDC)?",
        o: [["بانک مرکزی همان کشور", "The country's central bank"],
            ["یک شرکت خصوصی", "A private company"],
            ["استخراج‌کنندگان بیت‌کوین", "Bitcoin miners"],
            ["فقط بانک‌های تجاری", "Commercial banks only"]] },
      { fa: "چه چیزی پول را «برنامه‌پذیر» می‌کند؟", en: "What makes money “programmable”?",
        o: [["قواعدی که در خود پول نوشته می‌شود، مثل تاریخ انقضا یا محدودیت محل خرج", "Rules written into the money itself, such as an expiry date or limits on where it is spent"],
            ["این‌که روی گوشی موبایل نگه داشته می‌شود", "Being kept on a mobile phone"],
            ["این‌که با کارت بانکی خرج می‌شود", "Being spent with a bank card"],
            ["این‌که قیمتش هر روز تغییر می‌کند", "Its price changing every day"]] }
    ],
    [
      { fa: "توکن‌های LP نشان‌دهنده‌ی چه چیزی هستند؟", en: "What do LP tokens represent?",
        o: [["رسیدی برای پولی که به استخر لیکوئیدیتی اضافه شده", "A receipt for money added to a liquidity pool"],
            ["سهمی از شرکت سازنده‌ی توکن", "A share in the token's company"],
            ["تخفیف کارمزد معامله", "A trading-fee discount"],
            ["حق رأی در اداره‌ی پروژه", "A governance vote"]] },
      { fa: "درباره‌ی قفل لیکوئیدیتی کدام جمله درست است؟", en: "Which statement about a liquidity lock is true?",
        o: [["فقط جلوی بیرون کشیدن لیکوئیدیتی قفل‌شده را تا تاریخ آزادسازی می‌گیرد", "It only stops the locked liquidity being removed before the unlock date"],
            ["ثابت می‌کند قیمت توکن بالا می‌رود", "It proves the token's price will rise"],
            ["یعنی توکن هرگز فروخته نمی‌شود", "It means the token can never be sold"],
            ["یعنی سازنده‌ی توکن ناشناس است", "It means the token's creator is anonymous"]] }
    ],
    [
      { fa: "لیکوئیدیشن چیست؟", en: "What is a liquidation?",
        o: [["وقتی صرافی یک معامله‌ی اهرمی را به‌خاطر تمام شدن وثیقه، خودکار می‌بندد", "When the exchange automatically closes a leveraged position because the margin is running out"],
            ["وقتی یک توکن تازه به صرافی اضافه می‌شود", "When a new token is added to an exchange"],
            ["وقتی کسی سود معامله‌اش را برداشت می‌کند", "When someone withdraws their trading profit"],
            ["وقتی یک بانک مرکزی نرخ بهره را پایین می‌آورد", "When a central bank cuts interest rates"]] },
      { fa: "با اهرم ۱۰ برابر و ۱۰۰ دلار وثیقه، قیمت حدوداً چقدر باید بیفتد تا وثیقه از دست برود؟", en: "With 10× leverage and $100 of margin, roughly how far must the price fall before the margin is gone?",
        o: [["حدود ۱۰٪", "About 10%"], ["حدود ۱٪", "About 1%"], ["حدود ۵۰٪", "About 50%"], ["۱۰۰٪", "100%"]] }
    ]
  ];

  var FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
  function faNum(n) { return String(n).replace(/\d/g, function (d) { return FA_DIGITS[d]; }); }
  function isEn() { return document.documentElement.getAttribute("data-lang") === "en"; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function both(fa, en) { return '<span lang="fa" dir="rtl">' + esc(fa) + '</span><span lang="en">' + esc(en) + "</span>"; }
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  function $(id) { return document.getElementById(id); }

  // reward box
  $("leReward").innerHTML = both(CONFIG.rewardFa, CONFIG.rewardEn);
  if (CONFIG.capFa) $("leCap").innerHTML = both(CONFIG.capFa, CONFIG.capEn);

  // lesson list
  $("leLessons").innerHTML = LESSONS.map(function (l, i) {
    return '<li><a href="' + l[0] + '"><b>' + '<span lang="fa">' + faNum(i + 1) + '</span><span lang="en">' + (i + 1) + "</span></b>" +
      both(l[1], l[2]) + "</a></li>";
  }).join("");

  // quiz
  var current = [];
  function build() {
    current = BANK.map(function (pair, li) {
      var q = pair[Math.floor(Math.random() * pair.length)];
      var opts = q.o.map(function (o, k) { return { fa: o[0], en: o[1], ok: k === 0 }; });
      return { li: li, q: q, opts: shuffle(opts) };
    });
    var html = current.map(function (c, n) {
      var name = "q" + n;
      return '<fieldset class="le-q"><legend><span class="le-n"><span lang="fa">' + faNum(n + 1) + '</span><span lang="en">' + (n + 1) +
        "</span></span>" + both(c.q.fa, c.q.en) + "</legend>" +
        c.opts.map(function (o, k) {
          return '<label class="le-opt"><input type="radio" name="' + name + '" value="' + k + '" />' + both(o.fa, o.en) + "</label>";
        }).join("") + "</fieldset>";
    }).join("");
    html += '<button type="submit" class="le-btn le-submit">' + both("ثبت جواب‌ها", "Submit answers") + "</button>" +
      '<p class="le-err" id="leMissing" hidden>' + both("به همه‌ی ده سؤال جواب بده.", "Answer all ten questions.") + "</p>";
    $("leQuiz").innerHTML = html;
    $("leQuiz").hidden = false;
    $("leResult").hidden = true;
  }

  $("leQuiz").addEventListener("submit", function (e) {
    e.preventDefault();
    var wrong = [], answered = 0;
    current.forEach(function (c, n) {
      var pick = $("leQuiz").querySelector('input[name="q' + n + '"]:checked');
      if (pick) answered++;
      if (!pick || !c.opts[+pick.value].ok) wrong.push(c.li);
    });
    if (answered < current.length) { $("leMissing").hidden = false; return; }
    var score = current.length - wrong.length;
    var r = $("leResult");
    if (score >= CONFIG.pass) {
      store("ditoman-le-pass", String(score));
      r.innerHTML = '<p class="le-big ok">' + both("قبول شدی: " + faNum(score) + " از " + faNum(10), "You passed: " + score + " of 10") + "</p>" +
        "<p>" + both("حالا آدرس کیف پولت را وارد کن تا کد پاداش ساخته شود.", "Now enter your wallet address to get your reward code.") + "</p>";
      $("leQuiz").hidden = true;
      showClaim(score);
    } else {
      r.innerHTML = '<p class="le-big">' + both(faNum(score) + " از " + faNum(10) + " جواب درست", score + " of 10 right") + "</p>" +
        "<p>" + both("برای قبولی دست‌کم " + faNum(CONFIG.pass) + " جواب درست لازم است. این درس‌ها را دوباره بخوان:", "You need at least " + CONFIG.pass + " to pass. Reread these lessons:") + "</p>" +
        '<ul class="le-review">' + wrong.map(function (li) {
          var l = LESSONS[li];
          return '<li><a href="' + l[0] + '" target="_blank" rel="noopener">' + both(l[1], l[2]) + "</a></li>";
        }).join("") + "</ul>" +
        '<button type="button" class="le-btn" id="leRetry">' + both("دوباره امتحان کن", "Try again") + "</button>";
      $("leQuiz").hidden = true;
    }
    r.hidden = false;
    r.scrollIntoView({ behavior: "smooth", block: "start" });
    var retry = $("leRetry");
    if (retry) retry.addEventListener("click", function () { build(); $("test").scrollIntoView({ behavior: "smooth" }); });
  });

  // claim
  var passScore = 0;
  function showClaim(score) {
    passScore = score;
    $("claim").hidden = false;
  }

  function codeFor(wallet) {
    var data = new TextEncoder().encode(CONFIG.salt + wallet.toLowerCase());
    return crypto.subtle.digest("SHA-256", data).then(function (buf) {
      var h = Array.prototype.map.call(new Uint8Array(buf), function (b) { return ("0" + b.toString(16)).slice(-2); }).join("").toUpperCase();
      return "DTM-" + h.slice(0, 4) + "-" + h.slice(4, 8);
    });
  }
  function validWallet(w) { return /^0x[0-9a-fA-F]{40}$/.test(w); }

  $("leMake").addEventListener("click", function () {
    var w = $("leWallet").value.trim();
    var user = $("leUser").value.trim();
    if (!validWallet(w)) { $("leErr").hidden = false; return; }
    $("leErr").hidden = true;
    codeFor(w).then(function (code) {
      $("leCode").textContent = code;
      var en = isEn();
      var msg = en
        ? "Ditoman · Learn and earn\nCode: " + code + "\nWallet: " + w + "\nScore: " + passScore + "/10" + (user ? "\nUsername: " + user : "")
        : "دیتومان · یاد بگیر، توکن بگیر\nکد: " + code + "\nکیف پول: " + w + "\nنمره: " + passScore + "/10" + (user ? "\nآیدی: \u2066" + user + "\u2069" : "");
      $("leMsg").textContent = msg;
      var tg = $("leTg"), bale = $("leBale");
      if (CONFIG.telegram) { tg.href = "https://t.me/" + CONFIG.telegram + "?text=" + encodeURIComponent(msg); tg.hidden = false; }
      if (CONFIG.bale) { bale.href = "https://ble.ir/" + CONFIG.bale; bale.hidden = false; }
      var where = [];
      if (CONFIG.telegram) where.push(["تلگرام @" + CONFIG.telegram, "Telegram @" + CONFIG.telegram]);
      if (CONFIG.bale) where.push(["بله @" + CONFIG.bale, "Bale @" + CONFIG.bale]);
      $("leWhere").innerHTML = where.length
        ? both("پیام را برای این حساب بفرست: " + where.map(function (x) { return x[0]; }).join(" یا "),
               "Send the message to: " + where.map(function (x) { return x[1]; }).join(" or "))
        : "";
      $("leTicket").hidden = false;
      store("ditoman-le-code", code + "|" + w);
    });
  });

  $("leCopy").addEventListener("click", function () {
    var b = this, orig = b.innerHTML, t = $("leMsg").textContent;
    var done = function () { b.innerHTML = both("کپی شد", "Copied"); setTimeout(function () { b.innerHTML = orig; }, 1600); };
    if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, function () {});
    else { var ta = document.createElement("textarea"); ta.value = t; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); done(); } catch (e) {} ta.remove(); }
  });

  // team check: learn-earn.html#check
  if (location.hash === "#check") {
    $("check").hidden = false;
    $("ckGo").addEventListener("click", function () {
      var w = $("ckWallet").value.trim(), c = $("ckCode").value.trim().toUpperCase();
      if (!validWallet(w)) { $("ckOut").textContent = "آدرس کیف پول درست نیست."; return; }
      codeFor(w).then(function (code) {
        $("ckOut").textContent = code === c ? "✅ کد با این کیف پول می‌خواند." : "❌ کد با این کیف پول نمی‌خواند.";
      });
    });
    $("check").scrollIntoView();
  }

  build();
  var prev = store("ditoman-le-pass");
  if (prev && +prev >= CONFIG.pass) {
    $("leResult").innerHTML = '<p class="le-big ok">' + both("قبلاً قبول شده‌ای: " + faNum(prev) + " از " + faNum(10), "You already passed: " + prev + " of 10") + "</p>";
    $("leResult").hidden = false;
    $("leQuiz").hidden = true;
    showClaim(+prev);
  }
})();
