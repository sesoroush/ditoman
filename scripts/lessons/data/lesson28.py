LESSON = {
    "slug": "lesson28",
    "number": 28,
    "minutes": 6,
    "badge": ("Blockchain • Smart Contracts", "بلاکچین • قرارداد هوشمند"),
    "title": ("Ethereum and Smart Contracts: A Program That Runs by Itself", "اتریوم و قرارداد هوشمند: برنامه‌ای که خودش اجرا می‌شود"),
    "subtitle": (
        "Bitcoin keeps a ledger of who owns what. Ethereum also keeps programs. This lesson explains what a smart contract is, using the vending machine, and what it can and cannot do.",
        "بیت‌کوین دفتری از این‌که چه کسی مالک چیست نگه می‌دارد. اتریوم برنامه‌ها را هم نگه می‌دارد. این درس با مثال دستگاه فروش خودکار توضیح می‌دهد قرارداد هوشمند چیست و چه می‌تواند و چه نمی‌تواند.",
    ),
    "en": """
You put a coin in a vending machine and press B4. Nobody checks your request and nobody can talk the machine into giving you two snacks. If the rules are met, it delivers. If not, it does nothing.

That small machine is the best picture of a smart contract.

## What a smart contract is
Ethereum's own documentation says a smart contract is simply a program that runs on the Ethereum blockchain. It is a collection of code, called functions, and data, called state, that lives at a specific address on the chain.

The vending machine comparison is also from there, and the page credits it to the computer scientist Nick Szabo: perhaps the best metaphor for a smart contract.

## Why it is "smart"
It is not intelligent. It is automatic. The name means the rules are written as code and run exactly as written, whoever calls them.

[[fig]]

## What it looks like in practice
Imagine a simple contract: "If the sender pays the price, give them one ticket, and record that the ticket is theirs." There is no cashier. The network checks the payment and the program updates the record.

The same idea can hold a shared saving pot, a swap between two kinds of money, or a vote.

## Where it lives
A contract is deployed to the blockchain, and from then on it sits at an address like an account. Anyone can call its functions. Because many computers run it, the result does not depend on one company staying honest or online.

## Once deployed, it is hard to change
Ethereum's documentation says that once a contract is deployed, no user controls it, and by default it cannot be deleted. That is the strength and also the risk. A rule that cannot be changed gives trust. A mistake that cannot be changed stays.

That is why careful projects choose their power settings openly. In the case of TMN, for example, the token contract's owner was renounced, which means a central switch for changing the rules is deliberately gone.

## What a contract cannot do
A contract only knows what is on the chain. It cannot read a newspaper or check the weather by itself; information from outside has to be brought in. And it cannot fix a bad idea: code that does exactly what it says can still do something unwise.

## The cost of running
Every action takes computation, and users pay a fee, known on Ethereum as gas. Simple operations cost little; complex ones cost more.

## Why this matters
Without smart contracts, there would be no tokens built on Ethereum, which is where the next lesson goes.

##! What to take from this
A smart contract is a program stored on a blockchain: code plus data at an address.

The vending machine is the classic picture: rules met, result delivered, no cashier.

Once deployed, no user controls it, and by default it cannot be deleted.

It only knows what is on the chain.

"Smart" means automatic, not intelligent.
""",
    "fa": """
یک سکه در دستگاه فروش خودکار می‌اندازید و B4 را می‌زنید. هیچ‌کس درخواستتان را بررسی نمی‌کند و هیچ‌کس نمی‌تواند دستگاه را متقاعد کند دو تنقلات به شما بدهد. اگر شرط‌ها برقرار باشد، تحویل می‌دهد. اگر نه، کاری نمی‌کند.

این دستگاه کوچک بهترین تصویر قرارداد هوشمند است.

## قرارداد هوشمند چیست
مستندات خود اتریوم می‌گوید قرارداد هوشمند صرفاً برنامه‌ای است که روی بلاکچین اتریوم اجرا می‌شود. مجموعه‌ای از کد، به نام توابع، و داده، به نام وضعیت، است که در یک نشانی مشخص روی زنجیره قرار دارد.

مقایسه با دستگاه فروش هم از همان‌جاست و صفحه آن را به نیک سابو، دانشمند رایانه، نسبت می‌دهد: شاید بهترین استعاره برای قرارداد هوشمند.

## چرا «هوشمند» است
باهوش نیست؛ خودکار است. اسم یعنی قواعد به شکل کد نوشته شده‌اند و دقیقاً همان‌طور که نوشته شده‌اند اجرا می‌شوند، هر که صدایشان بزند.

[[fig]]

## در عمل چه شکلی است
قرارداد ساده‌ای را تصور کنید: «اگر فرستنده قیمت را بپردازد، یک بلیت به او بده و ثبت کن که بلیت مال اوست.» صندوقداری در کار نیست. شبکه پرداخت را بررسی می‌کند و برنامه ثبت را به‌روز می‌کند.

همین ایده می‌تواند یک قلک مشترک، مبادله‌ی دو نوع پول یا یک رأی‌گیری را نگه دارد.

## کجا زندگی می‌کند
قرارداد روی بلاکچین مستقر می‌شود و از آن به بعد مثل یک حساب در یک نشانی می‌نشیند. هر کسی می‌تواند توابعش را صدا بزند. چون رایانه‌های زیادی اجرایش می‌کنند، نتیجه به صداقت یا آنلاین‌ماندن یک شرکت بستگی ندارد.

## بعد از استقرار تغییرش سخت است
مستندات اتریوم می‌گوید وقتی قرارداد مستقر شد، هیچ کاربری کنترلش نمی‌کند و به‌طور پیش‌فرض قابل حذف نیست. این هم قوت است و هم خطر. قاعده‌ای که تغییر نمی‌کند اعتماد می‌آورد. اشتباهی که تغییر نمی‌کند می‌ماند.

برای همین پروژه‌های دقیق تنظیمات قدرت را آشکارا انتخاب می‌کنند. مثلاً در TMN مالکیت قرارداد توکن «رها» شده، یعنی یک کلید مرکزی برای تغییر قواعد عمداً از میان رفته است.

## قرارداد چه کارهایی نمی‌تواند
قرارداد فقط آنچه روی زنجیره است را می‌داند. خودش نمی‌تواند روزنامه بخواند یا آب‌وهوا را بررسی کند؛ اطلاعات بیرونی باید به زنجیره آورده شود. و نمی‌تواند ایده‌ی بد را درست کند: کدی که دقیقاً همان کار نوشته‌شده را می‌کند هم باز می‌تواند کار نابخردانه‌ای بکند.

## هزینه‌ی اجرا
هر عمل محاسبه می‌خواهد و کاربران کارمزد می‌دهند که در اتریوم «گس» (gas) نام دارد. عملیات ساده کم هزینه دارند و پیچیده‌ها بیشتر.

## چرا مهم است
بدون قرارداد هوشمند، توکنی روی اتریوم ساخته نمی‌شد؛ جایی که درس بعد به آن می‌رود.

##! چه برداشتی کنیم
قرارداد هوشمند برنامه‌ای است ذخیره‌شده روی بلاکچین: کد به‌علاوه‌ی داده در یک نشانی.

دستگاه فروش تصویر کلاسیک است: شرط برقرار، نتیجه تحویل، بدون صندوقدار.

بعد از استقرار هیچ کاربری کنترلش نمی‌کند و به‌طور پیش‌فرض قابل حذف نیست.

فقط آنچه روی زنجیره است را می‌داند.

«هوشمند» یعنی خودکار، نه باهوش.
""",
    "fig": {
        "type": "flow",
        "title": ("A vending-machine contract", "یک قرارداد مثل دستگاه فروش"),
        "steps": [
            ("Someone sends a payment and a request", "کسی پرداخت و درخواست می‌فرستد"),
            ("The contract's code checks the rules", "کد قرارداد قواعد را بررسی می‌کند"),
            ("If the rules are met, the state is updated", "اگر قواعد برقرار باشد، وضعیت به‌روز می‌شود"),
            ("The network records the result for everyone", "شبکه نتیجه را برای همه ثبت می‌کند"),
        ],
    },
    "related": {
        "title": ("Two lessons that connect", "دو درس مرتبط"),
        "text": (
            "Lesson 27 explains who keeps the chain honest. Lesson 29 shows what smart contracts made possible: tokens.",
            "درس ۲۷ توضیح می‌دهد چه کسی زنجیره را صادق نگه می‌دارد. درس ۲۹ نشان می‌دهد قراردادهای هوشمند چه چیزی را ممکن کردند: توکن‌ها.",
        ),
        "links": [("lesson27.html", "Who runs a blockchain?", "چه کسی بلاکچین را اداره می‌کند؟"), ("lesson29.html", "Coin vs token", "کوین و توکن چه فرقی دارند؟")],
    },
    "concepts": (
        ["Smart contract", "Function and state", "Address", "Deployment", "Gas", "Immutability", "On-chain data"],
        ["قرارداد هوشمند", "تابع و وضعیت", "نشانی", "استقرار", "گس", "تغییرناپذیری", "داده‌ی روی زنجیره"],
    ),
    "objectives": (
        ["Define a smart contract in one sentence.", "Use the vending machine to explain it.", "Say why a deployed contract is hard to change.", "Name a limit of what a contract can know.", "Explain what gas pays for."],
        ["قرارداد هوشمند را در یک جمله تعریف کنید.", "با دستگاه فروش آن را توضیح بدهید.", "بگویید چرا قرارداد مستقرشده سخت تغییر می‌کند.", "یک محدودیت در آنچه قرارداد می‌داند نام ببرید.", "توضیح بدهید گس بابت چه چیزی است."],
    ),
    "quiz": [
        {"q": ("What is a smart contract?", "قرارداد هوشمند چیست؟"),
         "options": [("A program that runs on a blockchain", "برنامه‌ای که روی بلاکچین اجرا می‌شود"), ("A paper agreement signed by a lawyer", "توافق کاغذی امضاشده نزد وکیل"), ("A type of bank account", "نوعی حساب بانکی")], "answer": 0},
        {"q": ("Which everyday machine is the classic metaphor?", "کدام دستگاه روزمره استعاره‌ی کلاسیک است؟"),
         "options": [("A vending machine", "دستگاه فروش خودکار"), ("A washing machine", "ماشین لباسشویی"), ("A printer", "چاپگر")], "answer": 0},
        {"q": ("By default, what happens to a deployed contract?", "به‌طور پیش‌فرض، قرارداد مستقرشده چه می‌شود؟"),
         "options": [("No user controls it and it cannot be deleted", "هیچ کاربری کنترلش نمی‌کند و حذف نمی‌شود"), ("Its author can edit it freely", "نویسنده‌اش آزادانه ویرایشش می‌کند"), ("It expires after a year", "پس از یک سال منقضی می‌شود")], "answer": 0},
        {"q": ("What does 'smart' in smart contract mean?", "«هوشمند» در قرارداد هوشمند یعنی چه؟"),
         "options": [("Automatic: rules run as written", "خودکار: قواعد همان‌طور که نوشته شده اجرا می‌شوند"), ("Artificially intelligent", "دارای هوش مصنوعی"), ("Always profitable", "همیشه سودآور")], "answer": 0},
        {"q": ("What can a contract not do by itself?", "قرارداد خودش چه کاری نمی‌تواند بکند؟"),
         "options": [("Read outside information such as the weather", "اطلاعات بیرونی مثل آب‌وهوا را بخواند"), ("Hold data", "داده نگه دارد"), ("Have an address", "نشانی داشته باشد")], "answer": 0},
    ],
    "sources": [
        ("https://ethereum.org/en/developers/docs/smart-contracts/", "ethereum.org: introduction to smart contracts (definition, code and state at an address, vending machine metaphor, cannot be deleted by default)"),
    ],
    "source_note": (
        "The statement about TMN's renounced owner follows the token page on this site. The page we cite does not give a coining date for the term, so none is stated. General explanation, not a security audit of any contract.",
        "بیان درباره‌ی رهاشدن مالکیت TMN از صفحه‌ی توکن همین سایت می‌آید. صفحه‌ی مرجع تاریخی برای ابداع این اصطلاح نمی‌دهد، پس تاریخی ذکر نشده. توضیح عمومی است و ممیزی امنیتی هیچ قراردادی نیست.",
    ),
}
