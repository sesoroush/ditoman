LESSON = {
    "slug": "lesson29",
    "number": 29,
    "minutes": 6,
    "badge": ("Blockchain • Coins and Tokens", "بلاکچین • کوین و توکن"),
    "title": ("What Is the Difference Between a Coin and a Token?", "کوین و توکن چه فرقی دارند؟"),
    "subtitle": (
        "People use the two words as if they were the same. They are not. This lesson gives one simple test and shows why it matters, including where TMN fits.",
        "مردم دو واژه را مثل هم به کار می‌برند، ولی یکی نیستند. این درس یک آزمون ساده می‌دهد و نشان می‌دهد چرا مهم است، از جمله جای TMN.",
    ),
    "en": """
In a shop you can pay with the country's own banknotes, or with a voucher the shop itself issued. Both are called money in daily speech, but they live in different places.

Crypto has the same split, and the words are coin and token.

## The one-line test
A coin is native to its own blockchain. A token is built on top of another blockchain. Kraken's guide gives the examples: BTC and ETH are coins; USDT and UNI are tokens.

Ask one question: does this asset have its own chain, or does it live on someone else's? That settles it.

[[fig]]

## Why coins exist
A coin is what the chain itself uses. It pays the fees and rewards the people who keep it running, as Lesson 27 showed. Without the coin the network would have no way to pay for its own operation.

## How tokens are made
Tokens are made by smart contracts, the programs from Lesson 28. A developer writes a contract that keeps a list of balances and rules for moving them. No new blockchain is needed.

## Why a standard helps
Ethereum has a standard for this called ERC-20, for fungible tokens, where one unit is interchangeable with another. The standard fixes the common names of the functions: name, symbol, decimals, total supply, balance of an address, transfer and approve, and two events that record transfers and approvals.

Because every compliant token speaks the same language, a wallet or an app that supports the standard can work with any of them without special code.

## One warning from the standard
ethereum.org notes that a plain ERC-20 can lose tokens that are sent to a contract that does not know how to handle them. Tokens are not magic: sending to a wrong address is still a mistake you cannot undo.

## Other chains, similar standards
Other chains have their own versions. BNB Smart Chain uses BEP-20, which follows the same idea. TMN, the digital toman, is a BEP-20 token on BNB Smart Chain, as described on its page on this site.

## Why the difference matters to you
A coin depends on its chain's own security. A token depends on both its chain and its contract. Understanding what an asset sits on tells you what could go wrong, and who, if anyone, can change it.

The question is not which is better. It is knowing which one you hold.

##! What to take from this
A coin is native to its own blockchain; a token is built on another.

BTC and ETH are coins; USDT and UNI are tokens.

Tokens are created by smart contracts, with no new chain needed.

Standards such as ERC-20 and BEP-20 let wallets work with many tokens.

TMN is a BEP-20 token on BNB Smart Chain.
""",
    "fa": """
در یک مغازه می‌توانید با اسکناس خود کشور پرداخت کنید یا با کوپنی که خود مغازه صادر کرده. در گفتار روزمره هر دو «پول» نامیده می‌شوند، ولی در جاهای متفاوتی زندگی می‌کنند.

در رمزارز هم همین تقسیم هست و واژه‌هایش کوین و توکن است.

## آزمون یک‌خطی
کوین بومیِ بلاکچین خودش است. توکن روی بلاکچین دیگری ساخته می‌شود. راهنمای Kraken مثال می‌زند: BTC و ETH کوین‌اند؛ USDT و UNI توکن.

یک پرسش بپرسید: این دارایی زنجیره‌ی خودش را دارد یا روی زنجیره‌ی دیگری زندگی می‌کند؟ همین تعیین می‌کند.

[[fig]]

## کوین‌ها چرا وجود دارند
کوین چیزی است که خود زنجیره به کار می‌برد. کارمزدها را می‌پردازد و به کسانی که زنجیره را روشن نگه می‌دارند پاداش می‌دهد، همان‌طور که درس ۲۷ نشان داد. بدون کوین شبکه راهی برای پرداخت هزینه‌ی کار خودش نداشت.

## توکن‌ها چطور ساخته می‌شوند
توکن‌ها را قراردادهای هوشمند می‌سازند، همان برنامه‌های درس ۲۸. توسعه‌دهنده قراردادی می‌نویسد که فهرستی از موجودی‌ها و قواعد جابه‌جایی‌شان را نگه می‌دارد. بلاکچین تازه‌ای لازم نیست.

## چرا استاندارد کمک می‌کند
اتریوم برای این کار استانداردی دارد به نام ERC-20، برای توکن‌های هم‌ارز، که در آن هر واحد با واحد دیگر قابل‌جایگزینی است. استاندارد نام‌های مشترک توابع را ثابت می‌کند: نام، نماد، تعداد ارقام اعشار، عرضه‌ی کل، موجودی یک نشانی، انتقال و تأیید، و دو رویداد که انتقال‌ها و تأییدها را ثبت می‌کنند.

چون هر توکنِ منطبق همان زبان را حرف می‌زند، کیف پول یا برنامه‌ای که استاندارد را پشتیبانی کند می‌تواند بدون کد ویژه با همه‌شان کار کند.

## یک هشدار از خود استاندارد
ethereum.org یادآوری می‌کند ERC-20 ساده می‌تواند توکن‌هایی را که به قراردادی فرستاده می‌شود که نمی‌داند چطور با آن‌ها کار کند از دست بدهد. توکن‌ها جادو نیستند: فرستادن به نشانی اشتباه هنوز اشتباهی است که برگشت ندارد.

## زنجیره‌های دیگر، استانداردهای مشابه
زنجیره‌های دیگر نسخه‌ی خودشان را دارند. BNB Smart Chain از BEP-20 استفاده می‌کند که همان ایده را دنبال می‌کند. TMN، تومان دیجیتال، یک توکن BEP-20 روی BNB Smart Chain است، همان‌طور که در صفحه‌اش در همین سایت آمده.

## چرا این فرق برای شما مهم است
کوین به امنیت خود زنجیره‌اش وابسته است. توکن هم به زنجیره‌اش وابسته است و هم به قراردادش. دانستن این‌که دارایی روی چه چیزی نشسته نشان می‌دهد چه چیزی می‌تواند خراب شود و چه کسی، اگر کسی باشد، می‌تواند تغییرش دهد.

پرسش این نیست که کدام بهتر است. این است که بدانید کدام را در دست دارید.

##! چه برداشتی کنیم
کوین بومی بلاکچین خودش است؛ توکن روی بلاکچین دیگری ساخته می‌شود.

BTC و ETH کوین‌اند؛ USDT و UNI توکن.

توکن‌ها را قراردادهای هوشمند می‌سازند، بدون زنجیره‌ی تازه.

استانداردهایی مثل ERC-20 و BEP-20 کیف پول‌ها را قادر می‌کنند با توکن‌های بسیار کار کنند.

TMN یک توکن BEP-20 روی BNB Smart Chain است.
""",
    "fig": {
        "type": "table",
        "title": ("Coin vs token", "کوین و توکن"),
        "cols": [("", ""), ("Coin", "کوین"), ("Token", "توکن")],
        "rows": [
            [("Where it lives", "کجا زندگی می‌کند"), ("On its own blockchain", "روی بلاکچین خودش"), ("On another blockchain", "روی بلاکچین دیگر")],
            [("Examples", "نمونه‌ها"), ("BTC, ETH", "BTC، ETH"), ("USDT, UNI, TMN", "USDT، UNI، TMN")],
            [("Created by", "ساخته‌شده توسط"), ("The chain's own rules", "قواعد خود زنجیره"), ("A smart contract", "یک قرارداد هوشمند")],
            [("Depends on", "وابسته به"), ("Its chain", "زنجیره‌اش"), ("Its chain and its contract", "زنجیره و قرارداد خودش")],
        ],
    },
    "related": {
        "title": ("Two lessons that connect", "دو درس مرتبط"),
        "text": (
            "Lesson 28 explains the smart contracts that make tokens. Lesson 5 shows how to check any token before you touch it.",
            "درس ۲۸ قراردادهای هوشمندی را توضیح می‌دهد که توکن می‌سازند. درس ۵ نشان می‌دهد هر توکن را پیش از دست‌زدن چطور بررسی کنید.",
        ),
        "links": [("lesson28.html", "Ethereum and smart contracts", "اتریوم و قرارداد هوشمند"), ("lesson05.html", "How to check any token before you touch it", "پیش از دست زدن به هر توکن، این‌ها را بررسی کنید")],
    },
    "concepts": (
        ["Coin", "Token", "Native asset", "ERC-20", "BEP-20", "Fungible", "Wallet compatibility"],
        ["کوین", "توکن", "دارایی بومی", "ERC-20", "BEP-20", "هم‌ارز", "سازگاری با کیف پول"],
    ),
    "objectives": (
        ["Apply the one-line test to any asset.", "Give two examples of coins and two of tokens.", "Explain how a token is created.", "Say why a standard such as ERC-20 helps.", "Place TMN correctly."],
        ["آزمون یک‌خطی را روی هر دارایی به کار ببرید.", "دو مثال کوین و دو مثال توکن بزنید.", "توضیح بدهید توکن چطور ساخته می‌شود.", "بگویید چرا استانداردی مثل ERC-20 کمک می‌کند.", "TMN را درست جا بدهید."],
    ),
    "quiz": [
        {"q": ("Which one is a coin?", "کدام یک کوین است؟"),
         "options": [("ETH", "ETH"), ("USDT", "USDT"), ("UNI", "UNI")], "answer": 0},
        {"q": ("What is the one-line test?", "آزمون یک‌خطی چیست؟"),
         "options": [("Does it have its own blockchain?", "آیا بلاکچین خودش را دارد؟"), ("Is its price high?", "آیا قیمتش بالاست؟"), ("Is its name short?", "آیا اسمش کوتاه است؟")], "answer": 0},
        {"q": ("What creates a token?", "چه چیزی توکن می‌سازد؟"),
         "options": [("A smart contract", "یک قرارداد هوشمند"), ("A new mining rig", "یک دستگاه استخراج تازه"), ("A central bank", "یک بانک مرکزی")], "answer": 0},
        {"q": ("What does ERC-20 standardise?", "ERC-20 چه چیزی را استاندارد می‌کند؟"),
         "options": [("The common functions of fungible tokens", "توابع مشترک توکن‌های هم‌ارز"), ("The price of tokens", "قیمت توکن‌ها"), ("Block time", "زمان بلاک")], "answer": 0},
        {"q": ("TMN is a token of which standard and chain?", "TMN توکن کدام استاندارد و زنجیره است؟"),
         "options": [("BEP-20 on BNB Smart Chain", "BEP-20 روی BNB Smart Chain"), ("A coin on Bitcoin", "یک کوین روی بیت‌کوین"), ("Its own blockchain", "بلاکچین مستقل خودش")], "answer": 0},
    ],
    "sources": [
        ("https://www.kraken.com/learn/crypto-coins-tokens-difference", "Kraken Learn: the difference between crypto coins and tokens (BTC and ETH are coins; USDT and UNI are tokens)"),
        ("https://ethereum.org/developers/docs/standards/tokens/erc-20.md", "ethereum.org: the ERC-20 token standard (shared interface, risk of tokens sent to contracts that cannot handle them)"),
    ],
    "source_note": (
        "TMN's standard and chain follow the token page on this site. General explanation, not investment advice.",
        "استاندارد و زنجیره‌ی TMN از صفحه‌ی توکن همین سایت گرفته شده. توضیح عمومی است، نه توصیه‌ی سرمایه‌گذاری.",
    ),
}
