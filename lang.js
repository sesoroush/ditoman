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
  var SKIP = "script, style, svg, code, textarea, .lang-btn, [data-en], body [lang='fa'], body [lang='en']";

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
    root.lang = lang;
    root.dir = lang === "en" ? "ltr" : "rtl";
    show(texts, lang);
    swaps.forEach(function (el) { el.innerHTML = el.getAttribute(lang === "en" ? "data-en" : "data-fa"); });
    document.querySelectorAll("[data-en-label]").forEach(function (n) {
      if (!n.hasAttribute("data-fa-label")) n.setAttribute("data-fa-label", n.getAttribute("aria-label") || "");
      n.setAttribute("aria-label", n.getAttribute(lang === "en" ? "data-en-label" : "data-fa-label"));
    });
    btn.textContent = lang === "en" ? "فارسی" : "EN";
    btn.setAttribute("lang", lang === "en" ? "fa" : "en");
    btn.setAttribute("aria-label", lang === "en" ? "نمایش به فارسی" : "Show in English");
    try { localStorage.setItem(KEY, lang); } catch (e) {}
  }

  // Toggle button in the header
  var btn = document.createElement("button");
  btn.type = "button";
  btn.className = "lang-btn";
  var spot = document.querySelector(".nav-right");
  if (spot) spot.insertBefore(btn, spot.firstChild);
  btn.addEventListener("click", function () { apply(root.getAttribute("data-lang") === "en" ? "fa" : "en"); });

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
