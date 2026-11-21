# Knowledge-based & technology company records. Every fact comes from the Wikipedia extract named in src.
# tuple: slug, wiki_key, fa, en, branch, sub, tag_fa, tag_en, [(label, fa, en)], summary_fa, summary_en, official(None|'fa'|'en' = source itself says knowledge-based)
LAB = {"founded": ("تأسیس", "Founded"), "based": ("پایگاه", "Based in"), "activity": ("فعالیت", "Activity"),
       "owner": ("مالکیت", "Owned by"), "innov": ("نوآوری", "Innovation"), "scale": ("مقیاس", "Scale")}
K = []
def add(slug, key, fa, en, br, sub, tfa, ten, facts, sfa, sen, official=None):
    K.append(dict(slug=slug, key=key, fa=fa, en=en, branch=br, sub=sub, tfa=tfa, ten=ten, facts=facts, sfa=sfa, sen=sen, official=official))

# ---- biotech and pharma
add("cinnagen-pharma","cinnagen","سیناژن","CinnaGen","industry","pharma",
 "داروهای زیستی‌مشابه، معرف‌های آزمایشگاهی و پروتئین‌های نوترکیب","Biosimilar drugs, laboratory reagents and recombinant proteins",
 [("founded","۱۹۹۴ میلادی","1994"),("activity","داروی زیستی‌مشابه، معرف آزمایشگاهی، پروتئین نوترکیب","Biosimilar drugs, in-vitro diagnostic reagents, recombinant proteins"),
  ("innov","سینووکس: زیستی‌مشابه اینترفرون بتا برای ام‌اس؛ تأیید سازمان غذا و دارو در ۲۰۰۷","Cinnovex, a biosimilar of interferon-beta for multiple sclerosis; approved by Iran's FDA in 2007")],
 "سیناژن شرکت زیست‌دارویی ایرانی است که در ۱۹۹۴ تأسیس شد. تا ۲۰۱۶ داروی زیستی‌مشابه، معرف آزمایشگاهی و پروتئین نوترکیب می‌ساخت و به خاورمیانه و کشورهای مشترک‌المنافع صادر می‌کرد. سینووکس، زیستی‌مشابه اینترفرون بتا، با دی‌ان‌ای‌ای ساخته‌شده در مؤسسه‌ی فراونهوفر آلمان تولید شد و در ۲۰۰۷ تأییدیه‌ی سازمان غذا و دارو را گرفت.",
 "CinnaGen is an Iranian biopharmaceutical company founded in 1994. As of 2016 it made biosimilar drugs, laboratory reagents and recombinant proteins, and exported to the Middle East and to Commonwealth of Independent States countries. Its Cinnovex, a biosimilar of interferon-beta, uses recombinant DNA made by scientists at Germany's Fraunhofer Institute; development was completed in Iran and approved by the Iranian FDA in 2007.")
add("aryogen","aryogen","آریوژن فارمد","AryoGen Pharmed","industry","pharma",
 "آنتی‌بادی‌های مونوکلونال درمانی و پروتئین‌های نوترکیب","Therapeutic monoclonal antibodies and recombinant proteins",
 [("activity","آنتی‌بادی‌های مونوکلونال درمانی و پروتئین‌های نوترکیب","Therapeutic monoclonal antibodies and other recombinant proteins")],
 "آریوژن فارمد شرکت زیست‌دارویی ایرانی است که در ساخت آنتی‌بادی‌های مونوکلونال درمانی و چند پروتئین نوترکیب دیگر تخصص دارد.",
 "AryoGen Pharmed is an Iranian biopharmaceutical company specialising in therapeutic monoclonal antibodies and some other recombinant proteins.")
add("barekat","barekat","گروه دارویی برکت","Barkat Pharmaceutical Group","industry","pharma",
 "نخستین مرکز تخصصی پژوهش دارویی؛ ۲۵ زیرمجموعه","The first specialised drug research centre in Iran; 25 subsidiaries",
 [("founded","۲۰۱۰ میلادی (با نام «تدبیر نوآوران دارویی»)","2010, as Tadbir innovation pharmaceutical company"),
  ("scale","۲۵ زیرمجموعه؛ ۷۰۰ نوع محصول؛ ۱۴٪ داروهای ضروری کشور","25 subsidiaries; 700 products; 14% of the country's essential drugs"),
  ("innov","نخستین مرکز تخصصی پژوهش دارو و داروسازی در ایران؛ سلول‌درمانی و ساخت داروهای پپتیدی","Established as the first specialised drug research centre in Iran; cell therapy and peptide medicines")],
 "گروه دارویی برکت شرکت سهامی عام دارویی است که در ۲۰۱۰ با نام «تدبیر نوآوران دارویی» تأسیس شد. به نوشته‌ی ویکی‌پدیا ۲۵ زیرمجموعه دارد، ۷۰۰ نوع محصول می‌سازد و ۱۴ درصد داروهای ضروری کشور را تأمین می‌کند. نخستین مرکز تخصصی پژوهش دارو در ایران را هم ساخته است.",
 "Barkat Pharmaceutical Group is a public pharmaceutical company founded in 2010 as Tadbir innovation pharmaceutical company. According to Wikipedia it has 25 subsidiaries, makes 700 products and supplies 14 percent of the country's essential drugs. It also set up what it calls the first specialised drug research centre in Iran.")
add("ronak","ronak","داروسازی روناک","Ronak Pharma","industry","pharma",
 "فرآورده‌های دارویی تزریقی؛ بیش از ۲۰ محصول","Injectable drugs; more than 20 products",
 [("founded","۱۳۸۲ خورشیدی","1382 (Iranian calendar, 2003–04)"),("activity","فرآورده‌های دارویی تزریقی","Injectable drug products"),
  ("scale","بیش از ۲۰ محصول؛ بیش از ۴۰۰ شغل مستقیم","20+ products; 400+ direct jobs")],
 "داروسازی روناک را ویکی‌پدیا «مجموعه‌ی اقتصادی دانش‌محور» با تمرکز بر داروهای تزریقی معرفی می‌کند. در ۱۳۸۲ تأسیس شد، بیش از ۲۰ محصول دارد و بیش از ۴۰۰ شغل مستقیم ساخته است.",
 "Wikipedia describes Ronak Pharma as a knowledge-oriented economic group focused on injectable drug products. It was founded in 1382 (2003–04), has more than 20 products and over 400 direct jobs.")
add("exir","exir","داروسازی اکسیر","Exir Pharmaceutical","industry","pharma",
 "بیش از ۲۷۰ فرآورده‌ی دارویی؛ کارخانه‌ی بروجرد","270+ drug products; plant in Borujerd",
 [("based","بروجرد، لرستان","Borujerd, Lorestan"),("scale","بیش از ۲۷۰ فرآورده‌ی دارویی؛ زمین ۳۶ هکتار","270+ drug products; 36-hectare site"),
  ("innov","فرآورده‌های بیوتکنولوژی و داروهای تحت لیسانس در کنار تولید داروهای انسانی","Biotechnology products and licensed drugs alongside human medicines")],
 "کارخانه‌ی داروسازی اکسیر در بروجرد، روی زمینی ۳۶ هکتاری، یکی از بزرگ‌ترین واحدهای تولید داروی انسانی کشور است. بیش از ۲۷۰ فرآورده در شکل‌های قرص، کپسول، آمپول، شربت و سافت‌ژل می‌سازد و فرآورده‌های بیوتکنولوژی هم دارد.",
 "The Exir plant in Borujerd sits on a 36-hectare site and is among the country's largest makers of human drugs. It produces over 270 products as tablets, capsules, ampoules, syrups and soft gels, and also has biotechnology products.")
add("faran-shimi","faran-shimi","داروسازی فاران شیمی","Faran Chemi Pharmaceuticals","industry","pharma",
 "مادهٔ اولیهٔ بوپرنورفین و محصولات ترک اعتیاد؛ شرکت بورسی","Buprenorphine raw material and addiction-treatment products; listed company",
 [("founded","۱۳۸۱ خورشیدی (تویسرکان)","1381 (Iranian calendar, 2002–03), Tuyserkan"),("owner","گروه صنعتی گلرنگ (از ۱۳۸۶)","Golrang Industrial Group (since 1386)"),
  ("innov","تولید مادهٔ اولیهٔ بوپرنورفین هیدروکلراید در ایران","Produces buprenorphine hydrochloride raw material in Iran"),
  ("scale","۵۹ داروی ژنریک؛ خط قرص با ظرفیت ۱۵۰ میلیون قرص در سال","59 generic drugs; tablet line of 150 million a year")],
 "فاران شیمی در ۱۳۸۱ با اسید سالیسیلیک شروع کرد و در ۱۳۸۶ به گروه صنعتی گلرنگ پیوست. ویکی‌پدیا آن را «شرکت دانش‌بنیان» می‌نامد؛ مادهٔ اولیهٔ بوپرنورفین هیدروکلراید را در ایران می‌سازد که برای قرص جایگزین متادون به کار می‌رود.",
 "Faran Chemi began in 1381 (2002–03) with salicylic acid and joined Golrang Industrial Group in 1386. Wikipedia calls it a knowledge-based company; it makes the raw material buprenorphine hydrochloride in Iran, used for tablets that replace methadone.","fa")
add("jaber","jaber","داروسازی جابر ابن حیان","Jaber Ebne Hayyan Pharmaceutical","industry","pharma",
 "آنتی‌بیوتیک تزریقی و خوراکی، پماد، اسپری؛ پیش‌تر اسکوئیب ایران","Injectable and oral antibiotics, ointments, sprays; formerly Squibb Iran",
 [("founded","۱۹۶۰ میلادی؛ تهران","1960; Tehran"),("activity","آنتی‌بیوتیک تزریقی و خوراکی، پماد، اسپری استنشاقی و بینی، سافت‌ژل","Injectable and oral antibiotics, ointments, inhalers, nasal sprays, soft gels")],
 "داروسازی جابر ابن حیان در ۱۹۶۰ تأسیس شد و تا ۱۹۷۹ «اسکوئیب ایران» نام داشت. شرکت سهامی عام و عضو بورس تهران است.",
 "Jaber Ebne Hayyan Pharmaceutical was founded in 1960 and was known as Squibb Iran until 1979. It is a public joint-stock company on the Tehran Stock Exchange.")
add("loghman","loghman","دارویی و بهداشتی لقمان","Loghman Pharmaceutical & Hygienic","industry","pharma",
 "کشف، توسعه، ساخت و عرضه‌ی دارو","Drug discovery, development, manufacture and marketing",
 [("activity","کشف، توسعه، تولید و بازاریابی دارو در ایران","Discovery, development, manufacture and marketing of drugs in Iran")],
 "شرکت دارویی و بهداشتی لقمان شرکت داروسازی ایرانی است که کشف، توسعه، تولید و عرضه‌ی دارو را در ایران انجام می‌دهد.",
 "Loghman Pharmaceutical & Hygienic Co. is an Iranian pharmaceuticals company engaged in the discovery, development, manufacture and marketing of drugs in Iran.")
add("zahravi","zahravi","داروسازی زهراوی","Zahravi Pharmaceutical","industry","pharma",
 "داروسازی ایرانی؛ زیرمجموعه‌ی تیپیکو","Iranian drug maker; subsidiary of TIPICO",
 [("owner","شرکت سرمایه‌گذاری دارویی تأمین (تیپیکو)","Tamin Pharmaceutical Investment Company (TIPICO)")],
 "داروسازی زهراوی شرکت داروسازی ایرانی و زیرمجموعه‌ی شرکت سرمایه‌گذاری دارویی تأمین (تیپیکو) است. منبع عمومی ما درباره‌اش کوتاه است و جز این چیزی تأیید نکرده‌ایم.",
 "Zahravi Pharmaceutical is an Iranian drug maker and a subsidiary of Tamin Pharmaceutical Investment Company (TIPICO). Our public source on it is short and we have confirmed little beyond this.")
add("sobhan","sobhan","گروه دارویی سبحان","Sobhan Darou Group","industry","pharma",
 "هلدینگ دارویی از گروه برکت؛ نماد دسبحا","Pharmaceutical holding in the Barkat group; listed on the Tehran exchange",
 [("founded","۱۳۵۵ خورشیدی","1355 (Iranian calendar, 1976–77)"),("owner","از شرکت‌های تابعه‌ی گروه دارویی برکت","A Barkat Pharmaceutical Group subsidiary"),("based","تهران","Tehran")],
 "گروه دارویی سبحان (سهامی عام) هلدینگ دارویی ایرانی و از شرکت‌های تابعه‌ی گروه دارویی برکت است، دفتر مرکزی‌اش در تهران است و با نماد «دسبحا» در بورس تهران پذیرفته شده.",
 "Sobhan Darou Group is an Iranian pharmaceutical holding and a subsidiary of Barkat Pharmaceutical Group, headquartered in Tehran and listed on the Tehran Stock Exchange.")
add("sina-robotics","sina-surgical","نوآوران رباتیک و پزشکی سینا","Sina Robotics and Medical Innovators","technology","health",
 "سامانه‌ی جراحی رباتیک سینا","Sina Robotic Surgical System",
 [("innov","سامانه‌ی جراحی رباتیک سینا؛ جراحی کم‌تهاجمی (پروستات، دریچه‌ی قلب، کلیه، زنان)","Sina Robotic Surgical System for minimally invasive surgery (prostate, cardiac valve, kidney, gynaecology)"),
  ("scale","دو دستگاه در مه ۲۰۲۳ به اندونزی صادر شد","Two devices exported to Indonesia in May 2023")],
 "سامانه‌ی رباتیک سینا محصول شرکت نوآوران رباتیک و پزشکی سینا است و جراحی لاپاراسکوپی را کم‌تهاجمی انجام می‌دهد. ویکی‌پدیا می‌نویسد در اداره‌ی ثبت اختراع آمریکا ثبت شده و در مه ۲۰۲۳ دو دستگاه به اندونزی صادر شده است.",
 "The Sina Robotic Surgical System is a product of Sina Robotics and Medical Innovators and performs minimally invasive surgery. Wikipedia reports it is registered at the US patent office and that two devices were exported to Indonesia in May 2023.")
add("royan","royan","پژوهشگاه رویان","Royan Institute","technology","health",
 "پژوهش پزشکی تولیدمثل و زیست‌فناوری؛ وابسته به جهاد دانشگاهی","Reproductive-medicine and biotechnology research; part of ACECR",
 [("activity","تحقیقات پزشکی تولیدمثل و زیست‌فناوری","Reproductive medicine and biotechnology research"),("owner","جهاد دانشگاهی","Academic Center for Education, Culture and Research (ACECR)")],
 "رویان بنیاد پژوهشی ایرانی در حوزه‌ی پزشکی تولیدمثل و زیست‌فناوری است و وابسته به جهاد دانشگاهی است. پژوهشگاه است، نه شرکت؛ به‌خاطر نقشش در فناوری‌های زیستی ایران در این فهرست آمده.",
 "Royan is an Iranian research foundation in reproductive medicine and biotechnology, part of the Academic Center for Education, Culture and Research. It is a research institute, not a company; it is listed here for its role in Iranian biotechnology.")
# ---- software and IT
add("pactos","pactos","پکتوس","Pactos","technology","knowledge",
 "نرم‌افزار فارسی و سخت‌افزار برای نابینایان؛ شرکت دانش‌بنیان","Persian software and hardware for blind people; knowledge-based company",
 [("founded","۱۹۹۲ میلادی؛ تهران؛ چهار فارغ‌التحصیل دانشگاه شریف","1992; Tehran; four graduates of Sharif University of Technology"),
  ("activity","نرم‌افزار بسته‌بندی‌شده‌ی فارسی برای کاربران خانگی و دولت","Packaged Persian software for consumers and government"),
  ("innov","ساخت سخت‌افزار برای نابینایان در ایران","Manufactures hardware for blind people in Iran")],
 "پکتوس شرکت نرم‌افزاری ایرانی در تهران است که در ۱۹۹۲ چهار فارغ‌التحصیل دانشگاه صنعتی شریف آن را بنیان گذاشتند. نام فارسی‌اش «شرکت دانش‌بنیان پکتوس» است؛ نرم‌افزار فارسی می‌فروشد و سخت‌افزار ویژه‌ی نابینایان می‌سازد.",
 "Pactos is a Tehran software company founded in 1992 by four graduates of Sharif University of Technology. Its Persian name translates as “Pactos Knowledge Enterprise”; it sells Persian packaged software and makes hardware for blind people.","en")
add("hamkaran-system","system-group","همکاران سیستم","Hamkaran System (System Group)","technology","knowledge",
 "نرم‌افزار سازمانی؛ بیش از ۵۳ هزار مشتری از ۱۹۸۷","Enterprise software; 53,000+ clients since 1987",
 [("founded","۱۹۸۷ میلادی (آغاز خدمت‌رسانی)","1987 (serving clients since)"),("scale","مجموعه‌ی ۵۸ شرکت؛ بیش از ۵۳ هزار مشتری","Conglomerate of 58 companies; 53,000+ clients"),("activity","نرم‌افزار و پشتیبانی سازمانی (ERP)","Enterprise software and support (ERP)")],
 "همکاران سیستم بزرگ‌ترین شرکت نرم‌افزاری بخش خصوصی ایران توصیف می‌شود. به نوشته‌ی ویکی‌پدیا مجموعه‌ای از ۵۸ شرکت است، از ۱۹۸۷ به بیش از ۵۳ هزار مشتری خدمت داده و در فهرست ۵۰۰ شرکت برتر ایران بوده است.",
 "Hamkaran System (System Group) is described as Iran's largest private software developer. Wikipedia says it is a conglomerate of 58 companies that has served over 53,000 clients since 1987 and was listed among Iran's top 500 companies.")
add("dotin","dotin","داتیس آرین قشم (دوتین)","Dotin (Datis Arian Qeshm)","technology","knowledge",
 "فناوری اطلاعات، نرم‌افزار، خدمات مالی و امنیت","Information technology, software, financial services and security",
 [("founded","۲۰۰۵ میلادی","2005"),("owner","هلدینگ فناپ (گروه مالی پاسارگاد)","Fanap Holding (Pasargad Financial Group)")],
 "دوتین (داتیس آرین قشم) در ۲۰۰۵ تأسیس شد و در فناوری اطلاعات، تولید نرم‌افزار، خدمات مالی و امنیت کار می‌کند. مالک آن هلدینگ فناپ از گروه مالی پاسارگاد است.",
 "Dotin (Datis Arian Qeshm) was founded in 2005 and works in IT, software, financial services and security. It is owned by Fanap Holding of the Pasargad Financial Group.")
add("nosa","nosa","نرم‌افزار و سخت‌افزار ایران (نوسا)","Iran Software & Hardware Co. (NOSA)","technology","knowledge",
 "نرم‌افزار سازمانی (ERP، BPMS، RFID، کتابخانه) از ۱۹۸۸","Enterprise software (ERP, BPMS, RFID, library) since 1988",
 [("founded","۱۹۸۸ میلادی","1988"),("activity","نرم‌افزار تجاری یکپارچه، ERP، MIS، BPMS، RFID و راهکار کتابخانه","Integrated business software, ERP, MIS, BPMS, RFID and library solutions")],
 "نوسا شرکت توسعه و مشاوره‌ی نرم‌افزار است که از ۱۹۸۸ نرم‌افزار سازمانی و راهکارهای ERP و RFID و کتابخانه برای سازمان‌های دولتی، خصوصی و غیرانتفاعی ایران ساخته است.",
 "NOSA is an independently owned software development and consulting company that since 1988 has built enterprise software and ERP, RFID and library solutions for public, private and not-for-profit organisations in Iran.")
add("dpi","dpi","داده‌پردازی ایران","Data Processing Iran (DPI)","technology","knowledge",
 "سخت‌افزار، نرم‌افزار، میزبانی و مشاوره فناوری","Hardware, software, hosting and IT consulting",
 [("based","تهران","Tehran"),("activity","ساخت و فروش سخت‌افزار و نرم‌افزار؛ زیرساخت، میزبانی، مشاوره، امنیت","Hardware and software (mostly software), infrastructure, hosting, consulting, security")],
 "داده‌پردازی ایران شرکت فناوری و مشاوره‌ی فناوری اطلاعات در تهران است. سخت‌افزار و بیشتر نرم‌افزار می‌سازد و خدمات زیرساخت، میزبانی وب، سرور اختصاصی و امنیت می‌دهد.",
 "Data Processing Iran is a Tehran-based computer technology and IT consulting corporation. It makes hardware and mainly software and offers infrastructure, web hosting, dedicated servers and security services.")
add("fanap","fanap","فناپ (فناوری اطلاعات و ارتباطات پاسارگاد آریان)","Fanap (Pasargad Arian ICT)","technology","knowledge",
 "شرکت بزرگ فناوری اطلاعات گروه مالی پاسارگاد","Large IT group of the Pasargad Financial Group",
 [("owner","گروه مالی پاسارگاد (نیمه‌دولتی)","Pasargad Bank Financial Group (semi-public)")],
 "فناپ شرکت فناوری اطلاعات و ارتباطات متعلق به گروه مالی پاسارگاد است. ویکی‌پدیا نوشته عرضه‌ی اولیه‌ی سهام آن در پیش است و در ۲۰۲۳ بانک داده‌ی کد منبع تشخیص چهره‌اش هک شد.",
 "Fanap is the information and communication technology corporation of the semi-public Pasargad Bank Financial Group. Wikipedia notes an IPO is expected, and that a facial-recognition source-code database was hacked in August 2023.")
add("fanap-infra","fanap-infra","فناپ‌زیرساخت","Fanap Infrastructure","technology","knowledge",
 "زیرساخت فناوری اطلاعات، شهر هوشمند، مرکز داده؛ حدود ۹۰۰ کارمند","IT infrastructure, smart city, data centres; about 900 staff",
 [("scale","حدود ۹۰۰ کارمند","About 900 employees"),("activity","زیرساخت IT، شهر هوشمند، مرکز داده، اتوماسیون و هوش مصنوعی، حمل‌ونقل هوشمند","IT infrastructure, smart city, data centres, automation and AI, smart transport")],
 "فناپ‌زیرساخت در زیرساخت فناوری اطلاعات، شهر هوشمند، مرکز داده و تحول دیجیتال فعال است و حدود ۹۰۰ کارمند دارد. زیرمجموعه‌ی فناپ است.",
 "Fanap Infrastructure works in IT infrastructure, smart cities, data centres and digital transformation, with about 900 staff. It is owned by Fanap.")
add("parse-semiconductor","parse-semi","نیمه‌هادی پارسه","Parsé Semiconductor","technology","knowledge",
 "طراحی تراشه‌ی ASIC، SoC و FPGA؛ ریزپردازنده‌ی ۳۲ بیتی آریستو","ASIC, SoC and FPGA design; the 32-bit Aristo microprocessor",
 [("founded","۲۰۰۳ میلادی؛ تهران","2003; Tehran"),("innov","ریزپردازنده‌ی ۳۲ بیتی «آریستو»؛ ۲۰۰۶، نخستین بار طراحی و ساخت در داخل کشور","The 32-bit «Aristo» microprocessor; 2006, announced as designed and produced inside Iran for the first time")],
 "نیمه‌هادی پارسه در ۲۰۰۳ در تهران تأسیس شد و تراشه‌های ASIC، SoC و FPGA طراحی می‌کند. در ۲۰۰۶ اعلام کرد ریزپردازنده‌ی ۳۲ بیتی «آریستو» را برای نخستین بار در داخل ایران طراحی و ساخته است.",
 "Parsé Semiconductor was established in 2003 in Tehran as a design house for ASIC, SoC and FPGA chips. In 2006 it announced it had both designed and produced a 32-bit microprocessor, Aristo, inside the country for the first time.")
# ---- payments
add("asan-pardakht","asan-pardakht","آسان پرداخت","Asan Pardakht","technology","fintech",
 "پرداخت الکترونیک، شارژ، قبض؛ از نخستین ۱۲ PSP کشور","Electronic payment, top-ups, bills; one of the first 12 PSPs",
 [("founded","۲۰۰۹ میلادی","2009"),("activity","کارت و پرداخت الکترونیک، شارژ موبایل، قبض","Card and electronic payment, mobile top-up, bill payment")],
 "آسان پرداخت (AP) در ۲۰۰۹ با سامانه‌های کارت پرداخت الکترونیک شروع کرد و بعد شارژ موبایل و پرداخت قبض را اضافه کرد. از ۱۲ شرکت نخست خدمات پرداخت الکترونیک ایران است.",
 "Asan Pardakht (AP) began in 2009 with electronic payment card systems and later added mobile top-up and bill payment. It is one of the first 12 electronic payment service providers in Iran.")
add("zarinpal","zarinpal","زرین‌پال","ZarinPal","technology","fintech",
 "درگاه پرداخت آنلاین؛ نخستین پرداختیار ایرانی","Online payment gateway; Iran's first payment facilitator",
 [("based","تهران","Tehran"),("innov","نخستین شرکت پرداختیار ایرانی؛ درگاه پرداخت آنلاین و سرویس‌های تسویه","First Iranian payment-facilitator company; online gateway and settlement services"),("scale","بیش از یک میلیون کاربر","More than one million users")],
 "زرین‌پال را ویکی‌پدیا نخستین شرکت پرداختیار ایرانی می‌نامد؛ در تهران است و برای فروشگاه‌های اینترنتی و استارتاپ‌ها درگاه پرداخت و تسویه فراهم می‌کند. بیش از یک میلیون کاربر دارد.",
 "Wikipedia calls ZarinPal the first Iranian payment-facilitator company. Based in Tehran, it gives online shops and startups a payment gateway and settlement services, and has over one million users.")
# ---- network and cloud
add("arvan-cloud","arvan","ابر آروان","ArvanCloud","technology","telecom",
 "شبکه‌ی توزیع محتوا و ابر؛ هشتمین CDN جهان به نوشته‌ی W3Techs","CDN and cloud; eighth CDN in the world per W3Techs",
 [("activity","CDN، ابر، ذخیره‌سازی شیء، IaaS و PaaS، VOD","CDN, cloud, object storage, IaaS, PaaS, VOD"),("scale","۵۰ هزار مشتری (۲۰۲۰)؛ ۳۰۰ شرکت با ابر رایگان","50,000 clients (2020); free cloud for 300 Iranian companies")],
 "ابر آروان شرکت شبکه‌ی توزیع محتوا و خدمات ابری ایرانی است. در ۲۰۲۰ ۵۰ هزار مشتری داشت و به ۳۰۰ شرکت ایرانی ابر رایگان داد؛ به نوشته‌ی W3Techs هشتمین ارائه‌دهنده‌ی CDN دنیا بود.",
 "ArvanCloud is an Iranian content delivery network and cloud company. In 2020 it had 50,000 clients and gave free cloud services to 300 Iranian companies; by W3Techs it was the eighth CDN provider in the world.")
add("pars-online","pars-online","پارس‌آنلاین","ParsOnline","technology","telecom",
 "بزرگ‌ترین ارائه‌دهنده‌ی اینترنت خصوصی؛ بیش از ۷۵۰ کارمند","Largest private ISP; 750+ employees",
 [("founded","۱۹۹۹ میلادی؛ تهران","1999; Tehran"),("scale","بیش از ۷۵۰ کارمند","750+ employees"),("owner","خریداری‌شده توسط های‌وب","Acquired by Hiweb")],
 "پارس‌آنلاین در ۱۹۹۹ در تهران تأسیس شد و بزرگ‌ترین ارائه‌دهنده‌ی خصوصی اینترنت ایران است. بیش از ۷۵۰ کارمند دارد و های‌وب آن را خریده است.",
 "ParsOnline was founded in 1999 in Tehran and is the largest private ISP in Iran, with over 750 employees. It was acquired by Hiweb.")
add("mobinnet","mobinnet","مبین‌نت","Mobinnet","technology","telecom",
 "اینترنت پهن‌باند بی‌سیم LTE","Wireless broadband internet on LTE",
 [("founded","دسامبر ۲۰۰۸","December 2008"),("innov","شبکه‌ی سراسری بی‌سیم TD-LTE؛ راه‌اندازی ۲۹ ژانویه ۲۰۱۷","Nationwide TD-LTE wireless network, launched 29 January 2017")],
 "مبین‌نت از بزرگ‌ترین ارائه‌دهندگان اینترنت پهن‌باند بی‌سیم ایران است. در دسامبر ۲۰۰۸ تأسیس شد و در ژانویه‌ی ۲۰۱۷ شبکه‌ی سراسری TD-LTE را راه انداخت.",
 "Mobinnet is one of Iran's largest wireless broadband providers. It was founded in December 2008 and launched its nationwide TD-LTE network on 29 January 2017.")
add("asiatech","asiatech","آسیاتک","Asiatech","technology","telecom",
 "انتقال داده، CDN، میزبانی و پهن‌باند","Data transmission, CDN, hosting and broadband",
 [("activity","انتقال داده، CDN، اپراتور مجازی، VPS، میزبانی، پهن‌باند","Data transmission, CDN, virtual mobile operator, VPS, hosting, broadband")],
 "آسیاتک شرکت ایرانی انتقال داده است که CDN، اپراتور مجازی تلفن همراه، سرور مجازی، میزبانی وب و پهن‌باند ارائه می‌دهد. منبع عمومی ما کوتاه است و فقط همین را تأیید کرده‌ایم.",
 "Asiatech is an Iranian data-transmission company offering a CDN, a virtual mobile operator, VPS, web hosting and broadband. Our public source is short and this is all we confirmed.")
# ---- platforms
add("cafebazaar","cafebazaar","کافه‌بازار","Cafe Bazaar","technology","platforms",
 "فروشگاه برنامه‌ی اندروید برای فارسی‌زبانان؛ بیش از ۵۰۰ هزار برنامه","Android app store for Persian speakers; 500,000+ apps",
 [("founded","آوریل ۲۰۱۱","April 2011"),("scale","بیش از ۵۰۰ هزار برنامه؛ ۴۰ میلیون کاربر (آوریل ۲۰۱۹)","500,000+ apps; 40 million users (April 2019)"),("innov","فروشگاه اندروید ویژه‌ی فارسی‌زبانان","An Android store built for Persian-speaking users")],
 "کافه‌بازار در آوریل ۲۰۱۱ تأسیس شد و فروشگاه برنامه‌ی اندروید ویژه‌ی فارسی‌زبانان است. به نوشته‌ی ویکی‌پدیا بیش از ۵۰۰ هزار برنامه دارد و در آوریل ۲۰۱۹ از ۴۰ میلیون کاربر گذشته بود.",
 "Cafe Bazaar was founded in April 2011 as an Android app store tailored to Persian speakers. Wikipedia says it offers over 500,000 apps and passed 40 million users in April 2019.")
add("sabaidea","sabaidea","صباایده","Saba Idea","technology","platforms",
 "شرکت پشت آپارات و فیلیمو","The company behind Aparat and Filimo",
 [("founded","۱۳۸۳ خورشیدی؛ تهران","1383 (Iranian calendar, 2004–05); Tehran"),("scale","بیش از ۱۶۰ کارمند","160+ employees"),("activity","آپارات، فیلیمو و پلتفرم‌های دیگر","Aparat, Filimo and other platforms")],
 "صباایده (فناوران ایده‌پرداز صبا) در ۱۳۸۳ تأسیس شد و وبگاه‌هایی مثل آپارات و فیلیمو را اداره می‌کند. مقرش در تهران است و بیش از ۱۶۰ نفر کارمند دارد.",
 "Saba Idea (Fanavaran Ide-Pardaz Saba) was founded in 1383 (2004–05) and runs sites such as Aparat and Filimo. It is based in Tehran and has more than 160 staff.")
add("aparat","aparat","آپارات","Aparat","technology","platforms",
 "پربازدیدترین سکوی ویدیوی ایران؛ ۶۰ میلیون کاربر ماهانه","Iran's most-visited video platform; 60 million monthly users",
 [("founded","۲۰۱۱ میلادی؛ تهران","2011; Tehran"),("owner","صباایده","Saba Idea"),("scale","بیش از ۶۰ میلیون کاربر ماهانه","60+ million monthly users")],
 "آپارات در ۲۰۱۱ توسط صباایده راه افتاد و به نوشته‌ی ویکی‌پدیا پربازدیدترین سکوی اشتراک ویدیو در ایران است، با بیش از ۶۰ میلیون کاربر ماهانه.",
 "Aparat was launched in 2011 by Saba Idea. Wikipedia calls it the most-visited video-sharing service in Iran, with over 60 million monthly users.")
add("filimo","filimo","فیلیمو","Filimo","technology","platforms",
 "سرویس ویدیوی درخواستی؛ بیش از نیمی از بازار استریم ایران","Video on demand; over half of Iran's streaming market",
 [("owner","صباایده","Saba Idea"),("scale","بیش از ۴۰۰ هزار مشترک ماهانه؛ سهم بازار بیش از ۵۰٪","400,000+ monthly subscribers; 50%+ market share")],
 "فیلیمو سرویس ویدیوی درخواستی متعلق به صباایده است. ویکی‌پدیا سهم بازارش را بیش از ۵۰ درصد استریم ایران و مشترکانش را بیش از ۴۰۰ هزار نفر در ماه می‌نویسد.",
 "Filimo is a video-on-demand streaming service owned by Saba Idea. Wikipedia puts its share of Iranian streaming above 50 percent, with over 400,000 monthly subscribers.")
add("fidibo","fidibo","فیدیبو","Fidibo","technology","platforms",
 "فروشگاه قانونی کتاب الکترونیک فارسی","Legal Persian e-book store",
 [("founded","اسفند ۱۳۹۲ (آغاز فعالیت)","Esfand 1392 (Iranian calendar, early 2014)"),("owner","دیجی‌کالا (خرید در ۱۳۹۵)","Digikala (bought in 1395, 2016–17)")],
 "فیدیبو از اسفند ۱۳۹۲ فروشگاه قانونی کتاب الکترونیک فارسی است که قانون کپی‌رایت را رعایت می‌کند. دیجی‌کالا در ۱۳۹۵ آن را خرید.",
 "Fidibo has been a legal Persian e-book store since Esfand 1392 (early 2014), respecting Iranian copyright law. Digikala bought it in 1395 (2016–17).")
add("neshan","neshan","نشان","Neshan","technology","platforms",
 "نقشه و مسیریاب موبایل؛ بیش از ۴ میلیون کاربر فعال روزانه","Mobile map and navigation; 4 million+ daily users",
 [("founded","۲۰۱۷ میلادی (انتشار عمومی)","2017 (public launch)"),("owner","راجمان؛ فناپ از ۲۰۱۸ سرمایه‌گذار","Rajman; Fanap invested in 2018"),("scale","بیش از ۴ میلیون کاربر فعال روزانه","4 million+ daily active users")],
 "نشان نقشه و مسیریاب موبایلی ایرانی است که ۲۰۱۷ را شرکت راجمان منتشر کرد و فناپ از ۲۰۱۸ سرمایه‌گذارش شد. بیش از ۴ میلیون کاربر فعال روزانه گزارش شده است.",
 "Neshan is an Iranian mobile mapping and navigation app launched in 2017 by Rajman; Fanap joined as an investor in 2018. It reports more than 4 million daily active users.")
add("eitaa","eitaa","ایتا","Eitaa","technology","platforms",
 "پیام‌رسان ابری ایرانی؛ بیش از ۷۰ میلیون کاربر","Iranian cloud messenger; 70 million+ users",
 [("activity","پیام‌رسان؛ تماس، پرداخت قبض، سرویس‌ها","Messaging, calls, bill payment, services"),("scale","بیش از ۷۰ میلیون کاربر","70 million+ users")],
 "ایتا پیام‌رسان ابری و چندسکویی ایرانی است. ویکی‌پدیا بیش از ۷۰ میلیون کاربر برایش می‌نویسد.",
 "Eitaa is an Iranian cloud-based, cross-platform messenger. Wikipedia reports more than 70 million users.")
add("bale","bale","بله","Bale","technology","platforms",
 "پیام‌رسان و پرداخت؛ ساخته‌ی بانک ملی؛ بیش از ۶۰ میلیون کاربر","Messenger and payments built by Bank Melli; 60 million+ users",
 [("owner","بانک ملی ایران","National Bank of Iran"),("innov","پیام‌رسان با پرداخت، انتقال پول، ربات و هوش مصنوعی","Messenger with payments, money transfer, bots and AI"),("scale","بیش از ۶۰ میلیون کاربر","60 million+ users")],
 "بله پیام‌رسانی است که بانک ملی ایران ساخته؛ پرداخت موبایلی، انتقال پول، ربات و هوش مصنوعی را کنار پیام‌رسانی دارد و ویکی‌پدیا بیش از ۶۰ میلیون کاربر برایش می‌نویسد.",
 "Bale is a messenger developed by the National Bank of Iran that combines messaging with mobile payments, money transfer, bots and AI. Wikipedia reports over 60 million users.")
add("igap","igap","آی‌گپ","iGap","technology","platforms",
 "پیام‌رسان متن‌باز با رمزنگاری سرتاسری؛ بیش از ۲۰ میلیون کاربر","Open-source messenger with end-to-end encryption; 20 million+ users",
 [("owner","کیان ایرانیان STD","Kian Iranian STD"),("innov","نخستین پیام‌رسان متن‌باز با رمزنگاری سرتاسری AES در غرب آسیا","First end-to-end encrypted, open-source AES messenger in West Asia"),("scale","بیش از ۲۰ میلیون کاربر","20 million+ users")],
 "آی‌گپ پیام‌رسان ابری ایرانی و متن‌باز است که کیان ایرانیان STD ساخته. ویکی‌پدیا آن را نخستین پیام‌رسان متن‌باز با رمزنگاری سرتاسری AES در غرب آسیا می‌نامد و بیش از ۲۰ میلیون کاربر برایش می‌نویسد.",
 "iGap is an Iranian open-source, cloud-based messenger developed by Kian Iranian STD. Wikipedia calls it the first end-to-end encrypted, open-source AES messenger in West Asia, with over 20 million users.")
add("soroush-plus","soroush","سروش پلاس","Soroush Plus","technology","platforms",
 "پیام‌رسان ایرانی؛ بیش از ۳۵ میلیون کاربر","Iranian messenger; 35 million+ users",
 [("owner","ستاک هوشمند شریف","Setak Houshmand Sharif"),("scale","بیش از ۳۵ میلیون کاربر","35 million+ users")],
 "سروش پلاس پیام‌رسان ایرانی چندسکویی است که ستاک هوشمند شریف ساخته و ویکی‌پدیا بیش از ۳۵ میلیون کاربر برایش می‌نویسد.",
 "Soroush Plus is an Iranian cross-platform messenger developed by Setak Houshmand Sharif; Wikipedia reports over 35 million users.")
add("rubika","rubika","روبیکا","Rubika","technology","platforms",
 "شبکه‌ی اجتماعی و پیام‌رسان؛ بیش از ۷۰ میلیون کاربر","Social network and messenger; 70 million+ users",
 [("owner","توسکا، همراه اول و ایرانسل","Tusca holding, MCI and MTN Irancell"),("scale","بیش از ۷۰ میلیون کاربر","70 million+ users")],
 "روبیکا شبکه‌ی اجتماعی و پیام‌رسان ابری ایرانی است که توسکا، همراه اول و ایرانسل ساخته‌اند. ویکی‌پدیا بیش از ۷۰ میلیون کاربر برایش می‌نویسد.",
 "Rubika is an Iranian cloud-based social network and messenger developed by Tusca holding, MCI and MTN Irancell. Wikipedia reports over 70 million users.")
add("taaghche","taaghche","طاقچه","Taaghche","technology","platforms",
 "پلتفرم کتاب الکترونیک","E-book distribution platform",
 [("activity","توزیع آنلاین کتاب الکترونیک","Online e-book distribution")],
 "طاقچه پلتفرم محبوب توزیع کتاب الکترونیک ایرانی است. ۳۱ ژوئیه‌ی ۲۰۲۳ وزارت ارشاد آن را بست و روز بعد با دخالت وزیر ارتباطات دوباره باز شد.",
 "Taaghche is a popular Iranian e-book distribution platform. It was taken down on 31 July 2023 by the Ministry of Culture and Islamic Guidance and reopened the next day after the ICT minister intervened.")
add("snapp","snapp","اسنپ","Snapp!","technology","platforms",
 "درخواست خودرو؛ قیمت از پیش مشخص؛ آغاز فوریه‌ی ۲۰۱۴","Ride hailing with fixed prices; launched February 2014",
 [("founded","فوریه ۲۰۱۴","February 2014"),("based","تهران","Tehran"),("innov","قیمت سفر پیش از شروع مشخص می‌شود؛ رانندگان پس از بررسی سوابق و مدارک","Fare fixed before the trip; drivers vetted with background, licence and insurance checks")],
 "اسنپ شرکت خودروی کرایه‌ای ایرانی در تهران است که فوریه‌ی ۲۰۱۴ شروع شد. قیمت سفر از پیش مشخص است و رانندگان پس از بررسی سوابق، گواهینامه و بیمه به کار گرفته می‌شوند. امروز خدماتی مثل سفارش غذا هم دارد.",
 "Snapp! is an Iranian vehicle-for-hire company in Tehran that launched in February 2014. The price is set beforehand and drivers are taken on after a background, licence and insurance check. It now also offers services such as food ordering.")
add("digikala","digikala","دیجی‌کالا","Digikala","technology","platforms",
 "بزرگ‌ترین فروشگاه اینترنتی ایران؛ از ۲۰۰۶","Iranian e-commerce; since 2006",
 [("founded","ژوئیه ۲۰۰۶؛ تهران","July 2006; Tehran"),("activity","کالای ورزشی، الکترونیک، خواروبار، لوازم شخصی و دیجیتال؛ ارسال سریع","Sports, electronics, groceries, personal and digital goods; express delivery")],
 "دیجی‌کالا در ژوئیه‌ی ۲۰۰۶ در تهران تأسیس شد. گروه کالاهای ورزشی، الکترونیک، خواروبار و دیجیتال با امکان بازگشت و ارسال سریع عرضه می‌کند و زیرمجموعه‌هایی در دیگر حوزه‌های تجارت الکترونیک دارد.",
 "Digikala was founded in Tehran in July 2006. It sells sports, electronics, groceries, personal and digital goods with returns and express delivery, and has subsidiaries in other e-commerce areas.")
add("torob","torob","ترب","Torob","technology","platforms",
 "جست‌وجو و مقایسه‌ی قیمت کالا","Product search and price comparison",
 [("activity","مقایسه‌ی قیمت؛ کاربر برای خرید به فروشگاه فروشنده هدایت می‌شود","Price comparison; users are sent to the seller's shop to buy")],
 "ترب وبگاه و اپلیکیشن ایرانی جست‌وجو و مقایسه‌ی قیمت کالا است. برخلاف فروشگاه، واسطه‌ی جست‌وجو است و خریدار برای تکمیل خرید به صفحه‌ی فروشنده می‌رود.",
 "Torob is an Iranian website and app for searching and comparing product prices. Unlike a shop, it acts as a search intermediary and sends buyers to the seller's page to complete the purchase.")
add("divar","divar","دیوار","Divar","technology","platforms",
 "نیازمندی‌ها و تجارت الکترونیک؛ از ۲۰۱۲","Classified ads and e-commerce; since 2012",
 [("founded","۲۰۱۲ میلادی","2012"),("activity","ملک، خودرو، کالا، خدمات، تجهیزات صنعتی و استخدام","Real estate, vehicles, goods, services, industrial equipment and jobs")],
 "دیوار در ۲۰۱۲ شروع شد و اپلیکیشن نیازمندی‌ها و تجارت الکترونیک فارسی‌زبانان است؛ بخش‌هایی برای ملک، خودرو، کالا، خدمات، تجهیزات صنعتی و کار دارد.",
 "Divar started in 2012 as a Persian classified-ads and e-commerce app, with sections for real estate, vehicles, goods, services, industrial equipment and jobs.")
add("sheypoor","sheypoor","شیپور","Sheypoor","technology","platforms",
 "پلتفرم آگهی‌های نیازمندی","Classified ads platform",
 [("based","تهران","Tehran"),("activity","وبگاه و اپلیکیشن آگهی نیازمندی","Classified-ads website and app")],
 "شیپور وبگاه و اپلیکیشن آگهی نیازمندی است و دفتر مرکزی‌اش در تهران است. منبع عمومی ما کوتاه است و فقط همین را تأیید کرده‌ایم.",
 "Sheypoor is a classified-ads website and mobile app headquartered in Tehran. Our public source is short and this is all we confirmed.")
add("namava","namava","نماوا","Namava","technology","platforms",
 "ویدیوی درخواستی؛ از گروه شاتل","Video on demand; part of the Shatel group",
 [("founded","پایان ۲۰۱۳ و آغاز ۲۰۱۴","Late 2013 and early 2014"),("owner","گروه شاتل","Shatel Group")],
 "نماوا سرویس ویدیوی درخواستی اشتراکی است که شاتل در پایان ۲۰۱۳ و آغاز ۲۰۱۴ راه انداخت. فیلم، سریال و انیمیشن ایرانی و خارجی دارد.",
 "Namava is a subscription video-on-demand service launched by Shatel in late 2013 and early 2014, with Iranian and international films, series and animation.")
add("okala","okala","اُکالا","Okala","technology","platforms",
 "سوپرمارکت آنلاین","Online supermarket",
 [("activity","خرید اینترنتی محصولات سوپرمارکتی","Online grocery shopping")],
 "اُکالا سوپرمارکت آنلاینی است که خرید اینترنتی محصولات سوپرمارکتی را ممکن می‌کند و می‌خواهد خرید روزانه را ساده و رفت‌وآمد درون‌شهری را کم کند.",
 "Okala is an online supermarket for ordering grocery products, aiming to make daily shopping easier and cut trips across the city.")
add("tipax","tipax","تیپاکس","Tipax","technology","platforms",
 "نخستین شرکت پست خصوصی ایران","Iran's first private postal company",
 [("innov","نخستین شرکت پست خصوصی ایران","First private postal company in Iran")],
 "تیپاکس اکسپرس پارس را ویکی‌پدیا نخستین شرکت پست خصوصی ایران می‌نامد. منبع عمومی ما کوتاه است و فقط همین را تأیید کرده‌ایم.",
 "Wikipedia calls Tipax Express Pars the first private postal company in Iran. Our public source is short and this is all we confirmed.")
add("telewebion","telewebion","تلوبیون","Telewebion","technology","platforms",
 "پخش زنده و آرشیو شبکه‌های سیما؛ ۶۰ شبکه","Live and archived streaming of IRIB channels; 60 channels",
 [("owner","صدا و سیمای جمهوری اسلامی ایران","Islamic Republic of Iran Broadcasting"),("scale","۶۰ شبکه‌ی زنده و آرشیو","60 live and archived channels")],
 "تلوبیون برنامه‌ی پخش ویدیوی درخواستی و زنده‌ی صدا و سیما است و ۶۰ شبکه‌ی زنده و آرشیو دارد؛ روی iOS و اندروید و وب در دسترس است.",
 "Telewebion is the streaming and video-on-demand service made by the Islamic Republic of Iran Broadcasting, with 60 live and archived channels on iOS, Android and the web.")
add("parsijoo","parsijoo","پارسی‌جو","Parsijoo","technology","knowledge",
 "موتور جست‌وجوی فارسی (سابق)","Persian-language search engine (former)",
 [("activity","موتور جست‌وجوی فارسی؛ ۲۰۱۶: ۱۲۰ هزار جست‌وجو در روز","Persian search engine; 2016: 120,000 searches a day")],
 "پارسی‌جو شرکت مستقل و موتور جست‌وجوی فارسی بود؛ ویکی‌پدیا آن را در زمان گذشته توصیف می‌کند. در ۲۰۱۶ حدود ۱۲۰ هزار جست‌وجو در روز داشت. برای ثبت تاریخچه‌ی نوآوری‌های ایران آمده است.",
 "Parsijoo was an independent Persian-language search-engine company; Wikipedia describes it in the past tense. In 2016 it had about 120,000 searches per day. It is listed for the record of Iranian innovation.")
# ---- hardware
add("x-vision","xvision","ایکس.ویژن","X.Vision","industry","consumer",
 "لوازم الکترونیک مصرفی؛ از گروه ماداران","Consumer electronics; Maadiran Group",
 [("owner","گروه ماداران","Maadiran Group"),("activity","لوازم الکترونیک مصرفی","Consumer electronics")],
 "ایکس.ویژن سازنده‌ی لوازم الکترونیک مصرفی ایرانی و زیرمجموعه‌ی گروه ماداران است. منبع عمومی ما کوتاه است و فقط همین را تأیید کرده‌ایم.",
 "X.Vision is an Iranian consumer-electronics maker and a subsidiary of Maadiran Group. Our public source is short and this is all we confirmed.")
add("snowa","snowa","اسنوا","Snowa","industry","consumer",
 "لوازم خانگی؛ اصفهان؛ از گروه صنعتی انتخاب","Home appliances; Isfahan; Entekhab Industrial Group",
 [("founded","۲۰۰۵ میلادی؛ اصفهان (مورچه‌خورت)","2005; Isfahan (Murche Khort)"),("owner","گروه صنعتی انتخاب","Entekhab Industrial Group"),("scale","کارخانه‌ی ۲۵ هزار متری","25,000 square-metre plant")],
 "اسنوا در ۲۰۰۵ در مورچه‌خورت اصفهان روی ۲۵ هزار متر شروع شد و زیرمجموعه‌ی گروه صنعتی انتخاب است. اجاق، هود، مایکروفر، یخچال، ماشین لباسشویی و تلویزیون هوشمند می‌سازد.",
 "Snowa was established in 2005 in Murche Khort, Isfahan, on 25,000 square metres, and belongs to Entekhab Industrial Group. It makes hobs, range hoods, microwaves, refrigerators, washing machines and smart TVs.")
