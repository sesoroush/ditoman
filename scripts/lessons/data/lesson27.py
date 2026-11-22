LESSON = {
    "slug": "lesson27",
    "number": 27,
    "minutes": 7,
    "badge": ("Blockchain • Mining and Staking", "بلاکچین • استخراج و اعتبارسنجی"),
    "title": ("Who Runs a Blockchain?", "چه کسی بلاکچین را اداره می‌کند؟"),
    "subtitle": (
        "No company owns Bitcoin or Ethereum, yet their ledgers keep growing correctly. This lesson explains how miners and validators keep the books honest, and why that costs something.",
        "هیچ شرکتی مالک بیت‌کوین یا اتریوم نیست، ولی دفترشان درست بزرگ می‌شود. این درس توضیح می‌دهد استخراج‌کننده‌ها و اعتبارسنج‌ها چطور دفتر را صادق نگه می‌دارند و چرا این کار هزینه دارد.",
    ),
    "en": """
A bank has an owner, a manager and a phone number. A public blockchain has none of these. Thousands of computers around the world hold the same ledger, and nobody is in charge of it.

So who decides which transactions go in next? And why would anyone cheat or not cheat?

## The problem to solve
Any ledger needs one rule: everyone must agree on the next page. If two people could add two different next pages, the money could be spent twice.

A bank solves this by being the single referee. A blockchain solves it with a method, called a consensus mechanism, where many strangers agree without trusting each other.

## Proof of work: mining
Bitcoin uses proof of work. Miners collect pending transactions into a block and then try to find a number that, combined with the block's data and hashed, produces a result below a target. As learnmeabitcoin explains, this means hashing the block header, using double SHA-256, over and over until a result falls below the target.

There is no shortcut except trying. The first miner to succeed shares the block, and the others check it quickly.

The network aims for a new block about every 10 minutes. Every 2,016 blocks, roughly two weeks, the difficulty adjusts so the pace stays steady however many miners join or leave.

## What miners are paid
The winning miner collects a reward for the block, called the coinbase, plus the fees from its transactions. The reward cannot be spent until it is 100 blocks old, which protects against a block being replaced.

The cost is the point. Miners spend real electricity and equipment, so cheating has to be worth more than the cost of doing it honestly.

[[fig]]

## Proof of stake: validators
Ethereum changed to proof of stake. Instead of spending energy, validators put money at risk. To run a validator on its own you deposit 32 ETH, and pools exist for people with less.

If a validator behaves dishonestly, part or all of its deposit can be destroyed. This penalty is called slashing. According to ethereum.org, the initial penalty starts at 1/4096 of the effective balance, capped at 0.5 ETH, and then the validator is removed.

## How much energy changed
The change came on 15 September 2022, the day of the Merge. The Cambridge Centre for Alternative Finance estimated that Ethereum's electricity use fell by about 99.99%.

## Nodes: the people who check
Miners and validators propose blocks, but any computer running the software, a node, can check the rules. A block that breaks the rules is rejected even if it was expensive to make.

## Can the majority cheat?
In proof of work, someone controlling most of the mining power could rewrite recent history. This is called a 51% attack. It needs enormous resources, and the target gets weaker the smaller the network.

Both systems answer the same question: make cheating more costly than honesty.

##! What to take from this
A blockchain needs a way for strangers to agree on the next page.

Proof of work: miners spend energy hashing until a result falls below the target.

Proof of stake: validators put money at risk and can be slashed.

Nodes check the rules, even without making blocks.

Both aim to make cheating cost more than honesty.
""",
    "fa": """
یک بانک مالک، مدیر و شماره‌ی تلفن دارد. بلاکچین عمومی هیچ‌کدام را ندارد. هزاران رایانه در سراسر دنیا یک دفتر را نگه می‌دارند و هیچ‌کس مسئولش نیست.

پس چه کسی تصمیم می‌گیرد کدام تراکنش‌ها بعدی وارد شوند؟ و چرا کسی تقلب کند یا نکند؟

## مسئله‌ای که باید حل شود
هر دفتری یک قاعده لازم دارد: همه باید روی صفحه‌ی بعدی توافق کنند. اگر دو نفر بتوانند دو صفحه‌ی بعدی متفاوت اضافه کنند، پول می‌تواند دو بار خرج شود.

بانک با داور واحدبودن این را حل می‌کند. بلاکچین با روشی حلش می‌کند به نام سازوکار اجماع، که در آن غریبه‌های زیادی بدون اعتماد به هم توافق می‌کنند.

## اثبات کار: استخراج
بیت‌کوین از اثبات کار استفاده می‌کند. استخراج‌کننده‌ها تراکنش‌های در انتظار را در یک بلاک جمع می‌کنند و سپس دنبال عددی می‌گردند که همراه داده‌ی بلاک هش شود و نتیجه‌اش زیر یک هدف باشد. به توضیح learnmeabitcoin، این یعنی هش‌کردن سرآیند بلاک با double SHA-256 بارها و بارها تا نتیجه زیر هدف بیفتد.

میان‌بری جز امتحان‌کردن نیست. اولین استخراج‌کننده‌ای که موفق شود بلاک را منتشر می‌کند و بقیه سریع بررسی‌اش می‌کنند.

شبکه هدفش یک بلاک جدید در هر حدود ۱۰ دقیقه است. هر ۲٬۰۱۶ بلاک، تقریباً دو هفته، دشواری تنظیم می‌شود تا هر قدر استخراج‌کننده بیاید یا برود، سرعت ثابت بماند.

## استخراج‌کننده‌ها چه می‌گیرند
استخراج‌کننده‌ی برنده پاداش بلاک را می‌گیرد، به نام «کوین‌بیس»، به‌علاوه‌ی کارمزد تراکنش‌های آن. این پاداش تا ۱۰۰ بلاک بعد قابل خرج نیست، که جلوی جایگزین‌شدن بلاک را می‌گیرد.

هزینه همان نکته است. استخراج‌کننده‌ها برق و تجهیزات واقعی خرج می‌کنند، پس تقلب باید ارزشش از هزینه‌ی صادقانه‌کار‌کردن بیشتر باشد.

[[fig]]

## اثبات سهام: اعتبارسنج‌ها
اتریوم به اثبات سهام تغییر کرد. به‌جای خرج انرژی، اعتبارسنج‌ها پول را در معرض خطر می‌گذارند. برای اداره‌ی یک اعتبارسنج مستقل ۳۲ اتر سپرده می‌کنید و برای کسانی که کمتر دارند «استخر» هست.

اگر اعتبارسنجی نادرست رفتار کند، بخشی از سپرده یا همه‌ی آن می‌تواند نابود شود. این جریمه «اسلشینگ» (slashing) نام دارد. طبق ethereum.org جریمه‌ی اولیه از ۱/۴۰۹۶ موجودی مؤثر شروع می‌شود، سقفش ۰٫۵ اتر است، و بعد اعتبارسنج کنار گذاشته می‌شود.

## مصرف انرژی چقدر عوض شد
این تغییر در ۱۵ سپتامبر ۲۰۲۲، روز «ادغام» (Merge) اتفاق افتاد. مرکز مالی جایگزین دانشگاه کمبریج برآورد کرد مصرف برق اتریوم حدود ۹۹٫۹۹٪ کاهش یافت.

## نودها: کسانی که بررسی می‌کنند
استخراج‌کننده‌ها و اعتبارسنج‌ها بلاک پیشنهاد می‌دهند، ولی هر رایانه‌ای که نرم‌افزار را اجرا کند، یعنی یک نود، می‌تواند قاعده‌ها را بررسی کند. بلاکی که قاعده را بشکند رد می‌شود، حتی اگر ساختنش گران بوده باشد.

## آیا اکثریت می‌تواند تقلب کند؟
در اثبات کار، کسی که بیشترِ توان استخراج را در دست داشته باشد می‌تواند تاریخ اخیر را بازنویسی کند. این «حمله‌ی ۵۱٪» نام دارد. منابع عظیمی می‌خواهد و هر چه شبکه کوچک‌تر باشد هدف ضعیف‌تر است.

هر دو نظام به یک پرسش جواب می‌دهند: تقلب را گران‌تر از صداقت کنید.

##! چه برداشتی کنیم
بلاکچین راهی لازم دارد تا غریبه‌ها روی صفحه‌ی بعدی توافق کنند.

اثبات کار: استخراج‌کننده‌ها انرژی خرج می‌کنند و هش می‌زنند تا نتیجه زیر هدف بیفتد.

اثبات سهام: اعتبارسنج‌ها پول را در معرض خطر می‌گذارند و ممکن است اسلش شوند.

نودها قاعده‌ها را بررسی می‌کنند، حتی بدون ساختن بلاک.

هر دو می‌خواهند تقلب را گران‌تر از صداقت کنند.
""",
    "fig": {
        "type": "table",
        "title": ("Proof of work vs proof of stake", "اثبات کار و اثبات سهام"),
        "cols": [("", ""), ("Proof of work (Bitcoin)", "اثبات کار (بیت‌کوین)"), ("Proof of stake (Ethereum)", "اثبات سهام (اتریوم)")],
        "rows": [
            [("Who proposes blocks", "چه کسی بلاک پیشنهاد می‌دهد"), ("Miners", "استخراج‌کننده‌ها"), ("Validators", "اعتبارسنج‌ها")],
            [("What is at stake", "چه چیزی در خطر است"), ("Electricity and equipment", "برق و تجهیزات"), ("A deposit (32 ETH to run one alone)", "یک سپرده (۳۲ اتر برای اجرای مستقل)")],
            [("Penalty for cheating", "جریمه‌ی تقلب"), ("Wasted work", "کار هدررفته"), ("Slashing of the deposit", "اسلشینگ سپرده")],
            [("Energy use", "مصرف انرژی"), ("High", "زیاد"), ("About 99.99% lower after the Merge (estimate)", "حدود ۹۹٫۹۹٪ کمتر پس از ادغام (برآورد)")],
        ],
    },
    "related": {
        "title": ("Two lessons that connect", "دو درس مرتبط"),
        "text": (
            "Lesson 28 shows what Ethereum runs on top of this: programs that execute by themselves. Lesson 30 explains the schedule that governs how Bitcoin's miners are paid.",
            "درس ۲۸ نشان می‌دهد اتریوم روی این پایه چه چیزی اجرا می‌کند: برنامه‌هایی که خودشان اجرا می‌شوند. درس ۳۰ برنامه‌ای را توضیح می‌دهد که پاداش استخراج‌کننده‌های بیت‌کوین را تعیین می‌کند.",
        ),
        "links": [("lesson28.html", "Ethereum and smart contracts", "اتریوم و قرارداد هوشمند"), ("lesson30.html", "What is the Bitcoin halving?", "هاوینگ بیت‌کوین چیست؟")],
    },
    "concepts": (
        ["Consensus mechanism", "Proof of work", "Mining and difficulty", "Block reward", "Proof of stake", "Validator and slashing", "Node", "51% attack"],
        ["سازوکار اجماع", "اثبات کار", "استخراج و دشواری", "پاداش بلاک", "اثبات سهام", "اعتبارسنج و اسلشینگ", "نود", "حمله‌ی ۵۱٪"],
    ),
    "objectives": (
        ["Explain why a blockchain needs a consensus method.", "Describe proof of work in simple words.", "Describe proof of stake and slashing.", "Say what a node does.", "Explain what a 51% attack is."],
        ["توضیح بدهید چرا بلاکچین به روش اجماع نیاز دارد.", "اثبات کار را ساده توصیف کنید.", "اثبات سهام و اسلشینگ را توصیف کنید.", "بگویید نود چه می‌کند.", "توضیح بدهید حمله‌ی ۵۱٪ چیست."],
    ),
    "quiz": [
        {"q": ("Roughly how often does the Bitcoin network aim to produce a block?", "شبکه‌ی بیت‌کوین تقریباً هر چند وقت یک بلاک را هدف می‌گیرد؟"),
         "options": [("About every 10 minutes", "تقریباً هر ۱۰ دقیقه"), ("Every second", "هر ثانیه"), ("Once a day", "روزی یک بار")], "answer": 0},
        {"q": ("How often does Bitcoin's difficulty adjust?", "دشواری بیت‌کوین هر چند وقت تنظیم می‌شود؟"),
         "options": [("Every 2,016 blocks, about two weeks", "هر ۲٬۰۱۶ بلاک، حدود دو هفته"), ("Every block", "هر بلاک"), ("Never", "هرگز")], "answer": 0},
        {"q": ("What is slashing?", "اسلشینگ چیست؟"),
         "options": [("Destroying part or all of a dishonest validator's deposit", "نابودکردن بخشی یا همه‌ی سپرده‌ی اعتبارسنج نادرست"), ("A fee discount", "تخفیف کارمزد"), ("A new coin", "یک کوین جدید")], "answer": 0},
        {"q": ("How much ETH is needed to run a validator on your own?", "برای اجرای مستقل یک اعتبارسنج چند اتر لازم است؟"),
         "options": [("32 ETH", "۳۲ اتر"), ("1 ETH", "۱ اتر"), ("1,000 ETH", "۱٬۰۰۰ اتر")], "answer": 0},
        {"q": ("What do both consensus methods aim for?", "هر دو روش اجماع چه هدفی دارند؟"),
         "options": [("Making cheating cost more than honesty", "گران‌تر کردن تقلب از صداقت"), ("Hiding the ledger", "پنهان‌کردن دفتر"), ("Choosing one company as boss", "انتخاب یک شرکت به‌عنوان رئیس")], "answer": 0},
    ],
    "sources": [
        ("https://learnmeabitcoin.com/mining", "learnmeabitcoin: mining, block time, difficulty retarget every 2,016 blocks, coinbase maturity, 51% attack"),
        ("https://ethereum.org/pt/developers/docs/consensus-mechanisms/pos", "ethereum.org: proof of stake, the 32 ETH deposit, staking pools and slashing"),
        ("https://ccaf.io/cbnsi/ethereum/ethereum_merge", "Cambridge Centre for Alternative Finance: Ethereum's electricity use after the Merge (15 September 2022)"),
    ],
    "source_note": (
        "The 99.99% figure is an estimate by the Cambridge Centre for Alternative Finance. The block interval and difficulty period are design targets, not guarantees for any single block. General explanation, not investment advice.",
        "رقم ۹۹٫۹۹٪ برآورد مرکز مالی جایگزین کمبریج است. فاصله‌ی بلاک‌ها و دوره‌ی دشواری اهداف طراحی‌اند، نه تضمین برای هر بلاک. توضیح عمومی است، نه توصیه‌ی سرمایه‌گذاری.",
    ),
}
