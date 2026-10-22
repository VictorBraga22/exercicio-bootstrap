"""Conteúdo único do CV, compartilhado pelas duas versões de design."""

NAME_FIRST, NAME_LAST = "Victor", "Braga"
ROLES = ["Graphic Designer", "Front of House", "Kitchen Hand", "Brand Ambassador"]

# (rótulo, texto exibido, link)
CONTACT = [
    ("Location", "Brisbane QLD", None),
    ("Phone", "0451 084 505", "tel:+61451084505"),
    ("Email", "victorbcsa@gmail.com", "mailto:victorbcsa@gmail.com"),
    ("Portfolio", "behance.net/victorbragacsa", "https://www.behance.net/victorbragacsa"),
]

PROFILE = [
    "Graphic designer with 7 years of agency experience in Brazil, producing print and "
    "point-of-sale material, large-format signage and digital artwork for brands such as "
    "Cinemark, Wickbold and Seven Boys. Looking for a role in screen printing, print "
    "production, signage or a creative studio.",
    "Now based in Brisbane, with 2026 experience in Australian hospitality and promotions: "
    "front of house, kitchen and pizza chef roles, and brand ambassador work for Activ8. "
    "Trusted to open and close venues, manage stock and lead on-site activations.",
]

# (título, empresa, local, datas, bullets). Bullet pode ser (destaque, texto).
AUSTRALIA = [
    ("Front of House", "Austino Cuisine – Maroochydore Club", "Sunshine Coast", "2026", [
        "Served food and drinks, took orders accurately and kept the floor clean and presentable.",
        "Organised the pass in busy services and supported the kitchen and dishwashing station.",
    ]),
    ("Front of House / Kitchen Hand / Pizza Chef", "Baretto Pizza", "Brisbane", "2026", [
        "Opened and closed the restaurant and kitchen, including all cleaning procedures.",
        "Managed stock, ordering and storage, plus Uber Eats and takeaway orders.",
        "Prepared ingredients and cooked pizzas in busy services, following food safety standards.",
    ]),
    ("Brand Ambassador & Promotional Staff", "Activ8", "Brisbane", "2026", [
        ("Woolworths – Product Sampling & On-site Activation Lead.",
         "Engaged customers, introduced products and handed out samples. Led on site: stock, "
         "deliveries, operational decisions and reporting to campaign coordinators."),
        ("Australian Retirement Trust – Mascot Minder, Riverfire 2026.",
         "Accompanied the mascot Artie, supported interactions with the public and guided it "
         "safely through crowds."),
        ("Street & Event Promotion.",
         "Handed out flyers in busy areas and explained event details."),
    ]),
]

DESIGN = [
    ("Senior Art Director / Graphic Designer", "Essenza Comunicação", "São Paulo",
     "Dec 2020 – Feb 2026", [
        "Designed key visuals, in-store and point-of-sale material, large-format outdoor ads and "
        "social content for Cinemark (Brazil and Argentina), Wickbold and Seven Boys.",
        "Lead designer on brand collaborations, incl. Seven Boys x Sonic, Seven Boys x GOAT and "
        "Cinemark with Coca-Cola, Monster Energy and Free Fire.",
        "Created and named the Cinemark Club loyalty program, a major sponsor at CCXP 2022.",
        "Adapted each campaign into multiple print and digital formats, often on tight deadlines.",
    ]),
    ("Graphic Designer", "Do It Comunicação", "Petrópolis", "Mar 2019 – Sep 2020", [
        "Designed and prepared print files for flyers, posters, menus, labels and signage for "
        "supermarkets, craft breweries (Brewpoint, Odin, Da Corte) and restaurants.",
    ]),
    ("Photographer (Freelance)", "Self-employed", "Petrópolis", "Feb 2017 – Mar 2019", [
        "Product, food and event photography for local businesses, incl. lighting and retouching.",
    ]),
]

SKILLS = ["Meeting deadlines", "attention to detail", "teamwork", "customer service",
          "stock control", "hands-on and physical work"]

EDUCATION = [
    ("Graphit School of Design", "Petrópolis, Brazil", "2017 – 2018",
     "Graphic Design, Advertising Design, Web Design, Digital Illustration, Photo Retouching"),
    ("Lordstown High School", "Ohio, USA", "2015", "Exchange program"),
]

LANGUAGES = [("English", "Fluent"), ("Portuguese", "Native"), ("Spanish", "Basic")]
