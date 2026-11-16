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
    "Why do prices suddenly crash?": "چرا قیمت یک‌دفعه می‌ریزد؟",
    "Digital dollars: what backs them?": "دلار دیجیتال، پشتوانه‌اش کجاست؟",
    "How will AI change the future of money?": "هوش مصنوعی چطور آینده‌ی پول را تغییر می‌دهد؟",
    "News starts the fall. Thin order books, slippage, leverage and liquidations decide how far it goes, with the 5 November 2026 sell-off as the example.":
      "خبر سقوط را شروع می‌کند. دفتر سفارش کم‌عمق، لغزش قیمت، اهرم و لیکوئیدیشن‌ها تعیین می‌کنند سقوط تا کجا برود؛ با ریزش ۱۴ آبان ۱۴۰۵ به‌عنوان نمونه.",
    "Slippage, leverage and the liquidation cascade: what happens inside an exchange after bad news, and how to protect yourself.":
      "لغزش قیمت، اهرم و آبشار لیکوئیدیشن: بعد از خبر بد داخل صرافی چه می‌گذرد و چطور از خودمان محافظت کنیم.",
    "Contract verified, ownership renounced, about 20% of supply out of circulation, bilingual lessons published, whitepaper final.":
      "قرارداد تأیید شد، مالکیت واگذار شد، حدود ۲۰٪ عرضه از گردش خارج شد، درس‌های دوزبانه منتشر شد و وایت‌پیپر نسخه‌ی ۵ نهایی شد.",
    "Contract verified, ownership renounced, about 20% of supply out of circulation, bilingual lessons published, Whitepaper V5 final.":
      "قرارداد تأیید شد، مالکیت واگذار شد، حدود ۲۰٪ عرضه از گردش خارج شد، درس‌های دوزبانه منتشر شد و وایت‌پیپر نسخه‌ی ۵ نهایی شد.",
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
    "Whitepaper V5: Final direction": "وایت‌پیپر نسخه‌ی ۵ به انگلیسی: مسیر نهایی",
    "What Ditoman is, the three pillars, full token facts, supply plan, roadmap and an honest risk disclosure. This is the reference for everything on this site.":
      "دیتومان چیست، سه محور، همه‌ی واقعیت‌های توکن، برنامه‌ی عرضه، نقشه‌ی راه و افشای صادقانه‌ی ریسک‌ها. مرجع همه‌ی مطالب این سایت.",
    "Read V5 (PDF)": "خواندن نسخه‌ی انگلیسی (PDF)", "Earlier version (V1)": "نسخه‌ی قبلی (نسخه‌ی ۱)",
    "The first whitepaper from 2022, kept as a public record of where the project started. Some figures and plans in it are out of date. V5 replaces it.":
      "نخستین وایت‌پیپر از ۲۰۲۲، که به‌عنوان سند عمومی نقطه‌ی شروع پروژه نگه داشته شده. بعضی اعداد و برنامه‌هایش قدیمی‌اند و نسخه‌ی ۵ جایگزین آن است.",
    "Early foundation": "پایه‌ی اولیه", "Open PDF": "باز کردن PDF",
    "New lessons arrive in our Telegram channel automatically, with a visual summary on Instagram.":
      "درس‌های تازه خودکار به کانال تلگرام و بله می‌رسند و خلاصه‌ی تصویری‌شان در اینستاگرام.",
    "Join on Telegram": "عضویت در تلگرام", "Follow on Instagram": "دنبال کردن در اینستاگرام",

    // prices page
    "Price history.": "تاریخچه‌ی قیمت‌ها.", "Every day, on record.": "هر روز، ثبت‌شده.",
    "Iran's free-market dollar against the official rate, gold and the Emami coin, going back more than a decade. Below, every Ditoman daily market report, by date. New data is added automatically every night.":
      "دلار بازار آزاد ایران در برابر نرخ رسمی، طلا و سکه‌ی امامی، از بیش از یک دهه پیش تا امروز. پایین‌تر، همه‌ی گزارش‌های روزانه‌ی بازار دیتومان به ترتیب تاریخ آمده است. داده‌های تازه هر شب خودکار اضافه می‌شوند.",
    "The gap between the two lines is what the official rate hides. Prices in toman.":
      "فاصله‌ی دو خط همان چیزی است که نرخ رسمی پنهان می‌کند. قیمت‌ها به تومان.",
    "Free market, latest": "بازار آزاد، آخرین", "Official, latest": "نرخ رسمی، آخرین",
    "Free vs official": "آزاد در برابر رسمی", "Change in period": "تغییر در این بازه",
    "Linear": "خطی", "Log": "لگاریتمی", "Free": "آزاد", "Official": "رسمی", "Gap": "فاصله",
    "Official rate: SANA (bank exchange houses) until November 2018, NIMA (exporters' system) from then on. Gaps in the official line are periods the source did not publish. Source: TGJU daily closes.":
      "نرخ رسمی: تا نوامبر ۲۰۱۸ سامانه‌ی سنا (صرافی‌های بانکی) و از آن پس سامانه‌ی نیما (صادرکنندگان). جاهای خالی خط رسمی دوره‌هایی است که منبع عددی منتشر نکرده. منبع: قیمت‌های پایانی روزانه‌ی TGJU.",
    "18k gold per gram and the Emami coin, in toman.": "طلای ۱۸ عیار هر گرم و سکه‌ی امامی، به تومان.",
    "18k gold, gram, latest": "طلای ۱۸ عیار، گرم، آخرین", "18k gold, gram": "طلای ۱۸ عیار، گرم",
    "In US dollars": "به دلار آمریکا", "toman": "تومان", "Go to date": "رفتن به تاریخ",
    "Source: TGJU daily closes.": "منبع: قیمت‌های پایانی روزانه‌ی TGJU.",
    "Published every night at 20:00 Tehran time on": "هر شب ساعت ۲۰:۰۰ به وقت تهران منتشر می‌شود در",
    "and Instagram.": "و اینستاگرام.", "Home": "خانه",
    "Ditoman • Learn. Connect. Evolve. • Est. 2022": "دیتومان • یاد بگیر، ارتباط بگیر، رشد کن • از ۲۰۲۲",

    // calendar page
    "Market calendar.": "تقویم بازار.", "What moves markets, every day.": "آنچه هر روز بازار را تکان می‌دهد.",
    "Each morning: the central bank decisions, data releases and earnings that matter that day and that week, with Tehran and Lisbon times. Every day is kept here, so the record grows over time.":
      "هر صبح: تصمیم‌های بانک‌های مرکزی، انتشار داده‌ها و گزارش‌های مالی مهم همان روز و همان هفته، با ساعت تهران و لیسبون. همه‌ی روزها این‌جا می‌مانند تا سابقه کم‌کم کامل شود.",
    "Get it on Telegram": "دریافت در تلگرام", "Tonight's prices": "قیمت‌های امشب",
    "Today": "امروز", "This week": "این هفته", "Post image": "تصویر پست", "Story image": "تصویر استوری",

    // lessons page
    "All lessons": "همه‌ی درس‌ها", "Learn the systems": "سیستم‌هایی را بشناس", "behind the future.": "که آینده را می‌سازند.",
    "Short, free lessons in Farsi and English. Each one takes about five minutes and ends with a quiz so you can check what stuck.":
      "درس‌های کوتاه و رایگان به فارسی و انگلیسی. هر کدام حدود پنج دقیقه است و با یک آزمونک تمام می‌شود تا ببینی چه چیزی در ذهنت مانده.",
    "Start from the beginning": "از اول شروع کن", "Browse lessons": "دیدن درس‌ها", "Beginner": "مقدماتی",
    "Quiz": "آزمونک", "Read lesson": "خواندن درس",
    "What does a liquidity lock actually mean?": "قفل نقدینگی واقعاً یعنی چه؟",
    "We locked TMN's liquidity today. What a pool and LP tokens are, how a rug pull happens, what a lock proves and what it does not, and how to check any lock yourself.":
      "نقدینگی TMN را قفل کردیم. استخر نقدینگی و توکن LP چیست، «رگ‌پول» چطور اتفاق می‌افتد، قفل چه چیزی را ثابت می‌کند و چه چیزی را نه، و هر قفلی را خودت چطور بررسی کنی.",
    "New lessons are added as they are written, and posted to our Telegram channel the moment they go live.":
      "درس‌های تازه همین که نوشته شوند اضافه می‌شوند و همان لحظه در کانال تلگرام هم منتشر می‌شوند.",
    "Money": "پول", "What money is, who controls it, and how it is changing.": "پول چیست، چه کسی آن را کنترل می‌کند و چطور در حال تغییر است.",
    "Central bank digital currencies, programmable money, the real trials behind the headlines, and Iran's digital rial.":
      "پول دیجیتال بانک مرکزی، پول برنامه‌پذیر، آزمایش‌های واقعی پشت تیترها و ریال دیجیتال ایران.",
    "Why prices move, and what nobody can predict.": "چرا قیمت‌ها تکان می‌خورند و چه چیزی را هیچ‌کس نمی‌تواند پیش‌بینی کند.",
    "Interest rates, elections and expectations: how an announcement can reach the market, and why history rarely gives a clear answer.":
      "نرخ بهره، انتخابات و انتظارات: یک اعلام رسمی چطور به بازار می‌رسد و چرا تاریخ به‌ندرت جواب روشنی می‌دهد.",
    "How to protect yourself before you touch any token.": "پیش از دست زدن به هر توکنی، چطور از خودت محافظت کنی.",
    "Five free checks anyone can run: contract verification, holder distribution, ownership, hidden restrictions and liquidity.":
      "پنج بررسی رایگان که هر کسی می‌تواند انجام دهد: تأیید قرارداد، پراکندگی دارندگان، مالکیت، محدودیت‌های پنهان و نقدینگی.",
    "The checks tell you about the token. These questions tell you about your own reasoning, your risk, and why you are buying now.":
      "آن بررسی‌ها درباره‌ی توکن چیزی می‌گویند؛ این پرسش‌ها درباره‌ی استدلال خودت، ریسکت و اینکه چرا همین حالا می‌خری.",
    "Liquidity pools, LP tokens and rug pulls, with TMN's own lock as the worked example, and what a lock does not prove.":
      "استخرهای نقدینگی، توکن LP و رگ‌پول، با قفل خود TMN به‌عنوان نمونه، و آنچه یک قفل ثابت نمی‌کند.",
    "Doing business in Iran": "کسب‌وکار در ایران",
    "Which body licenses what, and where to start, sector by sector.": "کدام نهاد چه مجوزی می‌دهد و از کجا باید شروع کرد، حوزه به حوزه.",
    "Iran Navigator: the licence guide": "راهنمای مجوزها (ایران نویگیتر)",
    "The map of ministries, organisations and permits, from registering a company to each sector's licence.": "نقشه‌ی وزارتخانه‌ها، سازمان‌ها و مجوزها، از ثبت شرکت تا مجوز هر حوزه.",
    "Open the guide": "باز کردن راهنما",
    "Energy": "انرژی", "How electricity markets work, and what it means for your bill.": "بازار برق چطور کار می‌کند و چه معنایی برای قبض تو دارد.",
    "When electricity prices go negative": "وقتی قیمت برق منفی می‌شود",
    "Why producers pay to sell power, the numbers from Germany and France, and why a negative wholesale price is not a negative bill.":
      "چرا تولیدکننده برای فروش برق پول می‌دهد، عددهای آلمان و فرانسه، و چرا قیمت منفی عمده‌فروشی به معنای قبض منفی نیست.",
    "The foundation everything else builds on.": "پایه‌ای که همه‌چیز روی آن ساخته می‌شود.",
    "A simple introduction to blockchain as a new way of storing, verifying and protecting information.":
      "معرفی ساده‌ی بلاک‌چین، به‌عنوان راهی تازه برای نگهداری، تأیید و محافظت از اطلاعات.",
    "How blockchain moves trust from institutions and platforms into transparent systems anyone can verify.":
      "بلاک‌چین چطور اعتماد را از نهادها و پلتفرم‌ها به سیستم‌های شفافی می‌برد که هر کسی می‌تواند بررسی‌شان کند.",
    "Where it came from and why it was built.": "از کجا آمد و چرا ساخته شد.",
    "How Bitcoin emerged as a response to broken trust, central control and the need for native internet money.":
      "بیت‌کوین چطور در پاسخ به اعتماد ازدست‌رفته، کنترل متمرکز و نیاز به پولی بومی اینترنت پدید آمد.",
    "The unknown creator behind Bitcoin, and why the mystery matters more than the identity.":
      "سازنده‌ی ناشناس بیت‌کوین، و اینکه چرا خود این راز از هویت او مهم‌تر است.",
    "Later, a small learn-and-earn pilot may reward completed lessons. Until it exists, we won't promise rewards.":
      "بعدها شاید آزمایشی کوچک برای پاداش دادن به درس‌های تمام‌شده راه بیفتد. تا وقتی راه نیفتاده، قول پاداش نمی‌دهیم.",
  };

  var KEY = "ditoman-lang";
  var root = document.documentElement;
  // Pages built for this switch carry data-lang on <html> and flip direction with it.
  // Older pages (lessons, stories) keep their own layout; only their text changes.
  var native = root.hasAttribute("data-lang") && !!document.querySelector('link[href*="site.css"]');
  // English twins (X.en.html) are locked to English; the switch then goes to the Persian URL.
  var lock = root.getAttribute("data-lang-lock");
  if (lock) root.setAttribute("data-lang", lock);
  if (!root.hasAttribute("data-lang")) {
    var saved0 = null;
    try { saved0 = localStorage.getItem(KEY); } catch (e) {}
    root.setAttribute("data-lang", saved0 === "en" ? "en" : "fa");
  }
  if (!document.querySelector('link[href*="site.css"]')) {
    var css = document.createElement("style");
    css.textContent =
      'html[data-lang="fa"] body [lang="en"]:not(.lang-btn){display:none!important}' +
      'html[data-lang="en"] body [lang="fa"]:not(.lang-btn){display:none!important}' +
      '.lang-btn{flex:none;height:38px;min-width:44px;padding:0 12px;border-radius:999px;border:1px solid rgba(127,245,222,.45);' +
      'background:rgba(127,245,222,.08);color:#eef6f2;font:700 .85rem Inter,-apple-system,Segoe UI,sans-serif;cursor:pointer;margin-inline-start:12px}' +
      '.lang-btn[lang="fa"]{font-family:"IRANYekanX Fa",IRANYekanX,Tahoma,sans-serif}' +
      '.lang-btn:hover{border-color:#57d9c7;color:#57d9c7}.lang-btn:focus-visible{outline:2px solid #57d9c7;outline-offset:2px}';
    document.head.appendChild(css);
  }
  var norm = function (s) { return s.replace(/\s+/g, " ").trim(); };
  var FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
  var faNum = function (s) { return String(s).replace(/\d/g, function (d) { return FA_DIGITS[d]; }); };
  var MONTHS = { Jan: "ژانویه", Feb: "فوریه", Mar: "مارس", Apr: "آوریل", May: "مه", Jun: "ژوئن", Jul: "ژوئیه",
    Aug: "اوت", Sep: "سپتامبر", Oct: "اکتبر", Nov: "نوامبر", Dec: "دسامبر" };
  // Patterns for text that repeats with different numbers (dates, times, durations)
  var PATTERNS = [
    [/^(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4})( ·)?$/, function (m) { return faNum(m[1]) + " " + MONTHS[m[2]] + " " + faNum(m[3]) + (m[4] || ""); }],
    [/^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4})$/, function (m) { return MONTHS[m[1]] + " " + faNum(m[2]); }],
    [/^Tehran (~?)(\d{1,2}:\d{2})$/, function (m) { return "تهران " + (m[1] ? "حدود " : "") + faNum(m[2]); }],
    [/^Lisbon (~?)(\d{1,2}:\d{2})$/, function (m) { return "لیسبون " + (m[1] ? "حدود " : "") + faNum(m[2]); }],
    [/^(\d+) min$/, function (m) { return faNum(m[1]) + " دقیقه"; }]
  ];
  function translate(text) {
    var key = norm(text);
    if (!key) return null;
    if (DICT.hasOwnProperty(key)) return DICT[key];
    for (var i = 0; i < PATTERNS.length; i++) {
      var m = key.match(PATTERNS[i][0]);
      if (m) return PATTERNS[i][1](m);
    }
    return null;
  }

  var texts = [];        // [{node, en, fa}]
  var swaps = [];        // elements with data-en
  var SKIP = "script, style, svg, code, textarea, [translate='no'], .lang-btn, [data-en], body [lang='fa'], body [lang='en']";

  // Bilingual pairs: wrap loose English text next to a Persian twin, and mark English siblings
  function pairs(scope) {
    var twins = scope.querySelectorAll ? scope.querySelectorAll("[lang='fa']") : [];
    for (var j = 0; j < twins.length; j++) {
      var fa = twins[j], parent = fa.parentElement;
      if (!parent || parent === document.body || parent === root || parent.closest("[data-en]")) continue;
      if (parent.getAttribute("lang") === "fa") continue;
      Array.prototype.slice.call(parent.childNodes).forEach(function (n) {
        if (n.nodeType === 3 && norm(n.textContent)) {
          var span = document.createElement("span");
          span.setAttribute("lang", "en");
          span.className = "lang-en";
          parent.insertBefore(span, n);
          span.appendChild(n);
        }
      });
      var prev = fa.previousElementSibling;
      if (prev && !prev.hasAttribute("lang") && !prev.hasAttribute("data-en") &&
          (prev.tagName === fa.tagName || /fa-sub|fa-line|mt-fa|co-fa|hero-fa/.test(fa.className))) {
        prev.setAttribute("lang", "en");
        prev.classList.add("lang-en");
      }
    }
  }

  // Dictionary and patterns, per text node
  function collect(scope) {
    var found = [];
    if (scope.nodeType === 1) {
      if (scope.hasAttribute("data-en") && !scope.hasAttribute("data-fa")) {
        scope.setAttribute("data-fa", scope.innerHTML); swaps.push(scope); found.push({ el: scope });
      }
      scope.querySelectorAll("[data-en]:not([data-fa])").forEach(function (el) {
        el.setAttribute("data-fa", el.innerHTML); swaps.push(el); found.push({ el: el });
      });
    }
    var walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT);
    var n;
    while ((n = walker.nextNode())) {
      if (n.__lang) continue;
      var host = n.parentElement;
      if (!host || host.closest(SKIP)) continue;
      var fa = translate(n.nodeValue);
      if (fa === null) continue;
      var lead = n.nodeValue.match(/^\s*/)[0], tail = n.nodeValue.match(/\s*$/)[0];
      var item = { node: n, en: n.nodeValue, fa: lead + fa + tail };
      n.__lang = item;
      texts.push(item); found.push(item);
    }
    return found;
  }

  function show(items, lang) {
    items.forEach(function (it) {
      if (it.el) it.el.innerHTML = it.el.getAttribute(lang === "en" ? "data-en" : "data-fa");
      else it.node.nodeValue = lang === "en" ? it.en : it.fa;
    });
  }

  function apply(lang) {
    root.setAttribute("data-lang", lang);
    if (native) {
      root.lang = lang;
      root.dir = lang === "en" ? "ltr" : "rtl";
    }
    // Pages with their own switch (Iran, companies, Navigator, lessons, stories) follow this one
    document.body.setAttribute("data-lang", lang);
    document.querySelectorAll(".k-toggle button[data-set]").forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-set") === lang ? "true" : "false");
    });
    if (typeof window.showLanguage === "function") { try { window.showLanguage(lang); } catch (e) {} }
    try { localStorage.setItem("ditoman-karnameh-lang", lang); } catch (e) {}
    show(texts, lang);
    swaps.forEach(function (el) { el.innerHTML = el.getAttribute(lang === "en" ? "data-en" : "data-fa"); });
    document.querySelectorAll("[data-en-label]").forEach(function (n) {
      if (!n.hasAttribute("data-fa-label")) n.setAttribute("data-fa-label", n.getAttribute("aria-label") || "");
      n.setAttribute("aria-label", n.getAttribute(lang === "en" ? "data-en-label" : "data-fa-label"));
    });
    btn.setAttribute("aria-label", lang === "en" ? "Language" : "زبان");
    menu.querySelectorAll(".lang-opt[data-code]").forEach(function (o) {
      o.setAttribute("aria-current", o.getAttribute("data-code") === (lang === "en" ? "en" : "fa") ? "true" : "false");
    });
    if (!lock || lang !== lock) { try { localStorage.setItem(KEY, lang); } catch (e) {} }
  }

  // Language switch: one globe button; it opens a row of flags. Persian and English work now,
  // the other languages are shown dimmed until their pages exist.
  var FLAGS = {"fa": "<rect width=\"36\" height=\"8\" fill=\"#239F40\"/><rect y=\"8\" width=\"36\" height=\"8\" fill=\"#fff\"/><rect y=\"16\" width=\"36\" height=\"8\" fill=\"#DA0000\"/><circle cx=\"18\" cy=\"12\" r=\"2.6\" fill=\"none\" stroke=\"#DA0000\" stroke-width=\"1.3\"/><path d=\"M18 9.4v5.2\" stroke=\"#DA0000\" stroke-width=\"1.1\"/>", "en": "<rect width=\"36\" height=\"24\" fill=\"#012169\"/><path d=\"M0 0 36 24M36 0 0 24\" stroke=\"#fff\" stroke-width=\"4.2\"/><path d=\"M0 0 36 24M36 0 0 24\" stroke=\"#C8102E\" stroke-width=\"1.4\"/><path d=\"M18 0v24M0 12h36\" stroke=\"#fff\" stroke-width=\"7\"/><path d=\"M18 0v24M0 12h36\" stroke=\"#C8102E\" stroke-width=\"4\"/>", "pt": "<rect width=\"36\" height=\"24\" fill=\"#FF0000\"/><rect width=\"14\" height=\"24\" fill=\"#006600\"/><circle cx=\"14\" cy=\"12\" r=\"4.6\" fill=\"#FFCC00\"/><path d=\"M11.8 9.4h4.4v3.4a2.2 2.2 0 0 1-4.4 0z\" fill=\"#FF0000\" stroke=\"#fff\" stroke-width=\".6\"/>", "es": "<rect width=\"36\" height=\"24\" fill=\"#AA151B\"/><rect y=\"6\" width=\"36\" height=\"12\" fill=\"#F1BF00\"/>", "fr": "<rect width=\"12\" height=\"24\" fill=\"#0055A4\"/><rect x=\"12\" width=\"12\" height=\"24\" fill=\"#fff\"/><rect x=\"24\" width=\"12\" height=\"24\" fill=\"#EF4135\"/>", "zh": "<rect width=\"36\" height=\"24\" fill=\"#DE2910\"/><polygon points=\"7.00,2.80 7.94,5.70 10.99,5.70 8.53,7.50 9.47,10.40 7.00,8.60 4.53,10.40 5.47,7.50 3.01,5.70 6.06,5.70\" fill=\"#FFDE00\"/><polygon points=\"13.94,1.98 13.91,2.92 14.80,3.25 13.89,3.51 13.86,4.45 13.33,3.67 12.42,3.93 13.00,3.18 12.48,2.40 13.36,2.72\" fill=\"#FFDE00\"/><polygon points=\"16.64,5.00 16.28,5.88 17.01,6.49 16.06,6.42 15.71,7.30 15.48,6.38 14.54,6.31 15.34,5.81 15.11,4.90 15.83,5.50\" fill=\"#FFDE00\"/><polygon points=\"17.02,8.96 16.28,9.54 16.60,10.42 15.82,9.90 15.07,10.48 15.33,9.57 14.55,9.04 15.49,9.01 15.75,8.10 16.08,8.99\" fill=\"#FFDE00\"/><polygon points=\"14.15,10.87 13.95,11.80 14.77,12.27 13.83,12.37 13.64,13.29 13.25,12.43 12.31,12.53 13.01,11.90 12.63,11.03 13.45,11.51\" fill=\"#FFDE00\"/>", "de": "<rect width=\"36\" height=\"8\" fill=\"#000\"/><rect y=\"8\" width=\"36\" height=\"8\" fill=\"#DD0000\"/><rect y=\"16\" width=\"36\" height=\"8\" fill=\"#FFCE00\"/>", "tr": "<rect width=\"36\" height=\"24\" fill=\"#E30A17\"/><circle cx=\"13.5\" cy=\"12\" r=\"6\" fill=\"#fff\"/><circle cx=\"15.2\" cy=\"12\" r=\"4.8\" fill=\"#E30A17\"/><polygon points=\"21.10,9.53 21.10,11.42 22.90,12.00 21.10,12.58 21.10,14.47 19.99,12.94 18.20,13.53 19.31,12.00 18.20,10.47 19.99,11.06\" fill=\"#fff\"/>", "ru": "<rect width=\"36\" height=\"8\" fill=\"#fff\"/><rect y=\"8\" width=\"36\" height=\"8\" fill=\"#0039A6\"/><rect y=\"16\" width=\"36\" height=\"8\" fill=\"#D52B1E\"/>"};
  var LANGS = [
    ["fa", "فارسی", "Persian", true], ["en", "English", "English", true],
    ["pt", "Português", "Portuguese", false], ["es", "Español", "Spanish", false], ["fr", "Français", "French", false],
    ["zh", "中文", "Chinese", false], ["de", "Deutsch", "German", false], ["tr", "Türkçe", "Turkish", false], ["ru", "Русский", "Russian", false]
  ];
  if (!document.getElementById("lang-menu-css")) {
    var lcss = document.createElement("style");
    lcss.id = "lang-menu-css";
    lcss.textContent =
      '.lang-wrap{position:relative;flex:none;display:inline-flex}' +
      'header .container.nav .lang-wrap{order:2;margin-inline-start:auto}' +
      '.lang-wrap .lang-btn{display:inline-flex;align-items:center;justify-content:center;width:38px;min-width:38px;height:38px;padding:0;margin:0}' +
      '.lang-btn svg{width:20px;height:20px}' +
      '.lang-menu{position:absolute;top:calc(100% + 10px);inset-inline-end:0;z-index:120;display:grid;grid-template-columns:repeat(3,auto);gap:10px;padding:12px;' +
      'background:#192b2e;border:1px solid rgba(87,217,199,.35);border-radius:16px;box-shadow:0 18px 40px rgba(0,0,0,.45)}' +
      '.lang-menu[hidden]{display:none}' +
      '.lang-opt{display:block;padding:3px;border:2px solid transparent;border-radius:9px;background:none;cursor:pointer;line-height:0}' +
      '.lang-opt svg{width:44px;height:29px;border-radius:5px;display:block;box-shadow:0 0 0 1px rgba(255,255,255,.18)}' +
      '.lang-opt[aria-current="true"]{border-color:#57d9c7}' +
      '.lang-opt:not(.is-soon):hover{border-color:rgba(87,217,199,.6)}' +
      '.lang-opt.is-soon{opacity:.38;cursor:default}' +
      '.lang-opt:focus-visible{outline:2px solid #57d9c7;outline-offset:2px}';
    document.head.appendChild(lcss);
  }
  var wrap = document.createElement("span");
  wrap.className = "lang-wrap";
  var btn = document.createElement("button");
  btn.type = "button";
  btn.className = "lang-btn";
  btn.setAttribute("aria-haspopup", "true");
  btn.setAttribute("aria-expanded", "false");
  btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 12h18M12 3c2.6 2.6 3.9 5.6 3.9 9s-1.3 6.4-3.9 9c-2.6-2.6-3.9-5.6-3.9-9S9.4 5.6 12 3z" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>';
  var menu = document.createElement("div");
  menu.className = "lang-menu";
  menu.hidden = true;
  LANGS.forEach(function (l) {
    var o = document.createElement("button");
    o.type = "button";
    o.className = "lang-opt" + (l[3] ? "" : " is-soon");
    o.setAttribute("data-code", l[0]);
    o.setAttribute("title", l[1] + (l[3] ? "" : " · soon"));
    o.setAttribute("aria-label", l[1] + (l[3] ? "" : " (soon)"));
    if (!l[3]) o.setAttribute("aria-disabled", "true");
    o.innerHTML = '<svg viewBox="0 0 36 24" aria-hidden="true">' + FLAGS[l[0]] + "</svg>";
    menu.appendChild(o);
  });
  wrap.appendChild(btn);
  wrap.appendChild(menu);
  var spot = document.querySelector(".nav-right");
  if (spot) spot.insertBefore(wrap, spot.firstChild);
  else {
    var bar = document.querySelector("header .nav") || document.querySelector("header .container") || document.querySelector("header");
    if (bar) bar.appendChild(wrap);
  }
  // One switch for the whole site: the old in-page switches are hidden, and if one is
  // ever clicked it drives the site-wide setting.
  document.querySelectorAll(".k-toggle, .language-toggle").forEach(function (el) { el.style.display = "none"; });
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest(".k-toggle button[data-set], .lang-button");
    if (!b) return;
    var l = b.getAttribute("data-set") || (/English/.test(b.textContent) ? "en" : "fa");
    apply(l);
  });
  // Each language has its own address (X.html and X.en.html); the switch moves between them
  // so links, bookmarks and search results always open in the language they show.
  function switchTo(to) {
    var alt = document.querySelector('link[rel="alternate"][hreflang="' + to + '"]');
    try { localStorage.setItem(KEY, to); } catch (e) {}
    if (alt && alt.href) {
      var target = alt.href.replace(/^https:\/\/ditoman\.com\//, location.protocol === "file:" ? "" : location.origin + "/");
      if (target.split("#")[0] !== location.href.split("#")[0]) { location.href = target + location.hash; return; }
    }
    apply(to);
  }
  function closeMenu() { menu.hidden = true; btn.setAttribute("aria-expanded", "false"); }
  btn.addEventListener("click", function (ev) {
    ev.stopPropagation();
    menu.hidden = !menu.hidden;
    btn.setAttribute("aria-expanded", menu.hidden ? "false" : "true");
  });
  menu.addEventListener("click", function (ev) {
    var o = ev.target.closest(".lang-opt");
    if (!o || o.classList.contains("is-soon")) return;
    closeMenu();
    var to = o.getAttribute("data-code");
    if (to !== root.getAttribute("data-lang")) switchTo(to);
  });
  document.addEventListener("click", function (ev) { if (!wrap.contains(ev.target)) closeMenu(); });
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") closeMenu(); });

  pairs(document.body);
  collect(document.body);
  apply(root.getAttribute("data-lang") === "en" ? "en" : "fa");

  // Content drawn later by the page (prices, calendar) gets the same treatment
  if (window.MutationObserver) {
    new MutationObserver(function (records) {
      records.forEach(function (r) {
        r.addedNodes.forEach(function (node) {
          if (node.nodeType === 1) pairs(node);
          var scope = node.nodeType === 1 ? node : node.parentNode;
          if (!scope) return;
          var found = collect(node.nodeType === 3 ? node.parentNode : node);
          var lang = root.getAttribute("data-lang");
          var swapsFound = found.filter(function (f) { return f.el; });
          show(found.filter(function (f) { return !f.el; }), lang);
          swapsFound.forEach(function (f) { f.el.innerHTML = f.el.getAttribute(lang === "en" ? "data-en" : "data-fa"); });
        });
      });
    }).observe(document.body, { childList: true, subtree: true });
  }
})();
