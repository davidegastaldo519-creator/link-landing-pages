# Genera il sito statico dello store NewHorizon Builds nella root del repo.
# Uso: python3 _src/build.py   (rilanciare dopo aver cambiato CHECKOUT o i testi)
#
# Sorgenti (in _src/):  build.py, template.html, gallery.json
# Generati (nella root): index.html, sitemap.xml, img/*.webp
# Mantenuti a mano (nella root): license.html, legal.html, 404.html, robots.txt,
#                                favicon.svg, img/*.jpg  -> build.py non li tocca.
import json, os, html, re

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)

# Lingue del selettore. REGOLA: una lingua sta qui SOLO se esiste la sua
# traduzione completa. Aggiungerne una = aggiungere la voce qui e il file
# i18n/<code>.json con le stesse chiavi di i18n/en.json (le chiavi mancanti
# ricadono automaticamente sull'inglese).
# La bandiera e' decorativa: su Windows le emoji bandiera non vengono
# disegnate, quindi il nome della lingua accanto NON e' opzionale.
LANGS = [
    dict(code="en", flag="🇬🇧", name="English"),
    dict(code="it", flag="🇮🇹", name="Italiano"),
]

# Versione fissa dell'embed Polar: NON usare @latest, una major nuova
# romperebbe il checkout in silenzio. Per aggiornare: alzare qui dopo aver provato.
POLAR_EMBED_VERSION = "0.6.0"

# Link di pagamento: quando ci sono i Checkout Link di Polar, incollarli qui.
# Finche' un link non e' di Polar, il pulsante apre il checkout Gumroad.
# Polar: mettere un id in POLAR_READY SOLO quando quel prodotto ha lo zip
# collegato come benefit "File downloads".
POLAR_READY = {"jade", "crimson", "sunset", "violet"}
POLAR = {
    "jade":    "https://buy.polar.sh/polar_cl_xrJ5su4bstycd9jvdefhtY0p1byj8ZMqoMDyd4QFRnJ",
    "crimson": "https://buy.polar.sh/polar_cl_9LOWhYn5CB52fQThzIYyKt6z1voi9BrL3KXEl4eAEkA",
    "sunset":  "https://buy.polar.sh/polar_cl_vR9ppXoAY1CJZ1KBy7JNF0JUZ1mfWK7sVtyvm2qUPSP",
    "violet":  "https://buy.polar.sh/polar_cl_uaeKjdr9pWf7zRiDGmNANG17QMguC8WvYJIJb1OQEtl",
}
CHECKOUT = {
    "jade":    "https://newhorizonmc.gumroad.com/l/jade-dynasty-bedwars",
    "crimson": "https://newhorizonmc.gumroad.com/l/crimson-maple-duels",
    "sunset":  "https://newhorizonmc.gumroad.com/l/sunset-lighthouse-skywars",
    "violet":  "https://newhorizonmc.gumroad.com/l/violet-drop-dropper",
}
for _k in POLAR_READY: CHECKOUT[_k] = POLAR[_k]
SUPPORT = "newhorizonmine@gmail.com"
DISCORD = "https://discord.gg/GVEZQ69FXF"
SITE = "https://mappe.newhorizonsmp.it"

P = [
 dict(id="jade", name="Jade Dynasty", mode="BedWars", price="21.99", color="#2fd29a", files=7,
  tag="Lobby + 5 maps + waiting island",
  tag_it="Lobby + 5 mappe + isola d'attesa",
  plugins="ScreamingBedWars, BedWars1058, BedWars2023",
  bullets=["Lobby 184×167 with a giant two-sided BEDWARS sign, pagodas, torii path and 5 NPC spots",
           "1v1, 2v2, 3v3, 4v4 maps + Solo map with 8 teams",
           "Shop/upgrade pavilions, diamond islands, pagoda centre with 4 emerald spots",
           "Beds left out (spots marked) so your plugin's team colours work"],
  bullets_it=["Lobby 184×167 con insegna BEDWARS gigante su due lati, pagode, viale torii e 5 posti NPC",
           "Mappe 1v1, 2v2, 3v3, 4v4 + mappa Solo a 8 squadre",
           "Padiglioni shop/upgrade, isole dei diamanti, pagoda centrale con 4 posti smeraldo",
           "Letti non piazzati (posti segnati) per usare i colori squadra del tuo plugin"]),
 dict(id="crimson", name="Crimson Maple", mode="Duels", price="19.99", color="#ff4a3d", files=21,
  tag="Lobby + 20 arenas", tag_it="Lobby + 20 arene",
  plugins="StrikePractice, Duels, ZonePractice",
  bullets=["Temple lobby 167×163 with 10 kit NPC spots, tournament dojo and leaderboard walls",
           "8 courtyard arenas with a flat 45×45 floor for every PvP kit",
           "4 sumo, 4 bridge and 4 open-terrain arenas",
           "Both spawns (with yaw), build limits and void Y for every arena"],
  bullets_it=["Lobby tempio 167×163 con 10 posti NPC per i kit, dojo dei tornei e muri classifiche",
           "8 arene cortile con pavimento piatto 45×45 per ogni kit PvP",
           "4 arene sumo, 4 bridge e 4 a terreno aperto",
           "Entrambi gli spawn (con yaw), limiti di costruzione e Y del vuoto per ogni arena"]),
 dict(id="sunset", name="Sunset Lighthouse", mode="SkyWars", price="21.99", color="#ff9b3d", files=11,
  tag="Lobby + 10 maps", tag_it="Lobby + 10 mappe",
  plugins="SkyWarsReloaded, Ultimate SkyWars, Plugily SkyWars",
  bullets=["Lobby 262×263 with a 42-block climbable lighthouse, airship and market",
           "10 themed maps: sky, volcano, jungle, nether, ice, desert, blossom, ocean, mushroom, end",
           "12 spawn islands with cages per map, 38 chests per map",
           "Every spawn and chest position in coordinates.json"],
  bullets_it=["Lobby 262×263 con faro scalabile di 42 blocchi, dirigibile e mercato",
           "10 mappe a tema: cielo, vulcano, giungla, nether, ghiaccio, deserto, fiori, oceano, funghi, end",
           "12 isole di spawn con gabbie per mappa, 38 casse per mappa",
           "Ogni spawn e ogni cassa in coordinates.json"]),
 dict(id="violet", name="Violet Drop", mode="Dropper", price="14.99", color="#b07cff", files=6,
  tag="Lobby + 5 giant maps", tag_it="Lobby + 5 mappe giganti",
  plugins="any Dropper plugin or a region/teleport setup",
  bullets=["Waiting lobby for up to 50 players with a 3D DROPPER sign and map showcases",
           "5 giant 45×45 shafts, about 165 blocks of fall, from easy to hard",
           "Every map checked with vanilla fall physics: always a free path to the water",
           "Start spawn and water level of every map in coordinates.json"],
  bullets_it=["Lobby d'attesa fino a 50 giocatori con insegna DROPPER in 3D e vetrine delle mappe",
           "5 pozzi giganti 45×45, circa 165 blocchi di caduta, da facile a difficile",
           "Ogni mappa verificata con la fisica di caduta vanilla: c'è sempre una via libera verso l'acqua",
           "Spawn di partenza e livello dell'acqua di ogni mappa in coordinates.json"]),
]

g = json.load(open(os.path.join(SRC, "gallery.json"), encoding="utf-8"))
e = html.escape


def caption(entry):
    """gallery.json: [id, en] oppure [id, en, it]. Senza it si ricade sull'inglese."""
    name, en = entry[0], entry[1]
    it = entry[2] if len(entry) > 2 and entry[2] else en
    return name, en, it


# ---------------------------------------------------------------- immagini webp
def make_webp():
    """Genera un .webp accanto a ogni .jpg. Salta quelli gia' aggiornati."""
    try:
        from PIL import Image
    except ImportError:
        print("! Pillow non installato: salto i webp (pip install Pillow)")
        return 0
    d = os.path.join(ROOT, "img")
    n = 0
    for f in sorted(os.listdir(d)):
        if not f.endswith(".jpg"):
            continue
        jpg = os.path.join(d, f)
        webp = jpg[:-4] + ".webp"
        if os.path.exists(webp) and os.path.getmtime(webp) >= os.path.getmtime(jpg):
            continue
        Image.open(jpg).save(webp, "webp", quality=82, method=6)
        n += 1
    return n


# ----------------------------------------------------------------------- logo
def make_logo():
    """Varianti del logo reale da _src/logo_master.webp."""
    try:
        from PIL import Image
    except ImportError:
        return []
    m = os.path.join(SRC, "logo_master.webp")
    if not os.path.exists(m):
        print("! _src/logo_master.webp mancante: salto il logo")
        return []
    base = Image.open(m).convert("RGBA")
    made = []
    # header (serve nitido anche su schermi 2x/3x)
    for w, out in ((192, "img/logo.webp"), (192, "img/logo.png")):
        im = base.copy(); im.thumbnail((w, w), Image.LANCZOS)
        p = os.path.join(ROOT, out)
        im.save(p, quality=90, method=6) if out.endswith("webp") else im.save(p, optimize=True)
        made.append(out)
    # icona per iOS/Android: su fondo scuro, il PNG trasparente diventa nero
    ic = Image.new("RGBA", (180, 180), (18, 13, 16, 255))
    lg = base.copy(); lg.thumbnail((164, 164), Image.LANCZOS)
    ic.paste(lg, ((180 - lg.width) // 2, (180 - lg.height) // 2), lg)
    ic.convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"), optimize=True)
    made.append("apple-touch-icon.png")
    return made


# ------------------------------------------------------------- i18n a dizionario
# Il template si scrive come sempre a coppie <tag data-en>..</tag><tag data-it>..</tag>.
# Qui le coppie vengono fuse in un solo elemento <tag data-i18n="kN"> che contiene
# l'inglese (cosi' la pagina e' leggibile e indicizzabile anche senza JS), e i testi
# finiscono in i18n/<code>.json. A runtime il JS sostituisce per chiave.
PAIR = re.compile(
    r'<(?P<tag>\w+)(?P<a1>[^>]*\sdata-en(?:\s[^>]*|))>(?P<en>.*?)</(?P=tag)>'
    r'\s*<(?P=tag)(?P<a2>[^>]*\sdata-it(?:\s[^>]*|))>(?P<it>.*?)</(?P=tag)>',
    re.S)


def extract_i18n(page):
    en, it, n = {}, {}, [0]

    def sub(m):
        n[0] += 1
        k = "k%d" % n[0]
        en[k] = m.group("en").strip()
        it[k] = m.group("it").strip()
        attrs = re.sub(r'\sdata-en(?=[\s>]|$)', '', " " + m.group("a1").strip()).rstrip()
        return f'<{m.group("tag")}{attrs} data-i18n="{k}">{en[k]}</{m.group("tag")}>'

    page = PAIR.sub(sub, page)
    left = len(re.findall(r'\sdata-(?:en|it)[\s>]', page))
    if left:
        raise SystemExit(
            f"! {left} elementi data-en/data-it non accoppiati nel template: "
            "ogni testo tradotto deve essere una coppia <tag data-en>..</tag>"
            "<tag data-it>..</tag> con lo stesso tag e adiacenti.")
    d = os.path.join(ROOT, "i18n")
    os.makedirs(d, exist_ok=True)
    for code, table in (("en", en), ("it", it)):
        with open(os.path.join(d, code + ".json"), "w", encoding="utf-8") as f:
            json.dump(table, f, ensure_ascii=False, indent=1, sort_keys=False)
    return page, len(en)


def lang_picker():
    opts = "".join(
        f'<li role="option" tabindex="-1" data-lang="{l["code"]}" aria-selected="false">'
        f'<span class="fl" aria-hidden="true">{l["flag"]}</span>{e(l["name"])}</li>'
        for l in LANGS)
    return (f'<div class="langpick"><button class="lang" id="langbtn" type="button" '
            f'aria-haspopup="listbox" aria-expanded="false" aria-label="Language / Lingua">'
            f'<span class="fl" id="langflag" aria-hidden="true">{LANGS[0]["flag"]}</span>'
            f'<span id="langname">{e(LANGS[0]["name"])}</span>'
            f'<span class="ca" aria-hidden="true">▾</span></button>'
            f'<ul class="langmenu" id="langmenu" role="listbox" '
            f'aria-label="Language / Lingua">{opts}</ul></div>')


# ------------------------------------------------------------------- JSON-LD
def jsonld():
    org = {
        "@type": "Organization",
        "@id": SITE + "/#org",
        "name": "NewHorizon Builds",
        "url": SITE + "/",
        "email": SUPPORT,
        "logo": SITE + "/favicon.svg",
        "parentOrganization": {"@type": "Organization", "name": "NewHorizon MC",
                               "url": "https://newhorizonsmp.it"},
    }
    items = []
    for n, p in enumerate(P, 1):
        first = caption(g[p["id"]][0])[0]
        items.append({
            "@type": "ListItem", "position": n,
            "item": {
                "@type": "Product",
                "@id": f"{SITE}/#{p['id']}",
                "name": f"{p['name']} – Minecraft {p['mode']} map pack",
                "description": p["tag"] + ". " + p["bullets"][0] + ".",
                "sku": p["id"],
                "image": [f"{SITE}/img/{caption(c)[0]}.jpg" for c in g[p["id"]][:3]],
                "brand": {"@id": SITE + "/#org"},
                "category": f"Minecraft {p['mode']} map pack",
                "offers": {
                    "@type": "Offer",
                    "url": f"{SITE}/#{p['id']}",
                    "price": p["price"],
                    "priceCurrency": "EUR",
                    "availability": "https://schema.org/InStock",
                    "itemCondition": "https://schema.org/NewCondition",
                    "seller": {"@id": SITE + "/#org"},
                },
            },
        })
    graph = [org, {
        "@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/",
        "name": "NewHorizon Builds", "publisher": {"@id": SITE + "/#org"},
        "inLanguage": ["en", "it"],
    }, {
        "@type": "ItemList", "@id": SITE + "/#packs",
        "name": "Minecraft minigame map packs", "numberOfItems": len(P),
        "itemListElement": items,
    }]
    data = json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + data + "</script>"


# ------------------------------------------------------------------- sitemap
def sitemap():
    pages = ["/", "/license.html", "/legal.html"]
    u = "".join(
        f"<url><loc>{SITE}{p}</loc><changefreq>monthly</changefreq>"
        f"<priority>{'1.0' if p == '/' else '0.5'}</priority></url>"
        for p in pages)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            + u + "</urlset>\n")


# --------------------------------------------------------------------- cards
def btn(pid, label_en, label_it, cls="btn buy"):
    url = CHECKOUT[pid]
    extra = ' data-polar-checkout data-polar-checkout-theme="dark"' if "polar.sh" in url else ""
    return (f'<a class="{cls}" href="{e(url)}"{extra}>'
            f'<span data-en>{label_en}</span><span data-it>{label_it}</span></a>')


def picture(name, alt, w, h, cls="", eager=False):
    """<picture> con webp + fallback jpg."""
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source srcset="img/{name}.webp" type="image/webp">'
            f'<img src="img/{name}.jpg" alt="{e(alt)}" {load} '
            f'width="{w}" height="{h}"{cls}></picture>')


cards = []
for idx, p in enumerate(P):
    imgs = [caption(c) for c in g[p["id"]]]
    thumbs = "".join(
        f'<button class="th" data-full="img/{n}.jpg" data-cap="{e(en)}" data-cap-it="{e(it)}" '
        f'aria-label="{e(en)}">'
        + picture(n + "_t", f'{p["name"]} – {en}', 320, 180)
        + "</button>"
        for n, en, it in imgs)
    li_en = "".join(f"<li>{e(b)}</li>" for b in p["bullets"])
    li_it = "".join(f"<li>{e(b)}</li>" for b in p["bullets_it"])
    hero_n, hero_en, hero_it = imgs[0]
    cards.append(f'''
<article class="pack" id="{p["id"]}" style="--c:{p["color"]}">
  <div class="hero-img"><button class="th big" data-full="img/{hero_n}.jpg" data-cap="{e(hero_en)}" data-cap-it="{e(hero_it)}" aria-label="{e(hero_en)}">{picture(hero_n, p["name"] + " lobby", 1600, 900, eager=(idx == 0))}</button></div>
  <div class="info">
    <p class="mode">{e(p["mode"])}</p>
    <h3>{e(p["name"])}</h3>
    <p class="tag"><span data-en>{e(p["tag"])}</span><span data-it>{e(p["tag_it"])}</span></p>
    <ul data-en>{li_en}</ul><ul data-it>{li_it}</ul>
    <p class="meta">{p["files"]} .schem · WorldEdit / FAWE · 1.21 (1.20.3+) · coordinates.json<br><span data-en>Works with</span><span data-it>Compatibile con</span> {e(p["plugins"])}</p>
    <div class="buyrow"><span class="price">{("€" if p["id"] in POLAR_READY else "$") + p["price"]}</span>{btn(p["id"], "Buy now", "Acquista")}</div>
  </div>
  <div class="thumbs">{thumbs}</div>
</article>''')

page = open(os.path.join(SRC, "template.html"), encoding="utf-8").read()
page = (page.replace("{{PACKS}}", "\n".join(cards))
            .replace("{{LANGPICKER}}", lang_picker())
            .replace("{{LANGS}}", json.dumps(
                [{"c": l["code"], "f": l["flag"], "n": l["name"]} for l in LANGS],
                ensure_ascii=False, separators=(",", ":")))
            .replace("{{JSONLD}}", jsonld())
            .replace("{{SUPPORT}}", SUPPORT)
            .replace("{{DISCORD}}", DISCORD)
            .replace("{{SITE}}", SITE))

uses_polar = any("polar.sh" in u for u in CHECKOUT.values())
uses_gum = any("gumroad.com" in u for u in CHECKOUT.values())
scripts = ""
if uses_polar:
    scripts += ('<script defer data-auto-init src="https://cdn.jsdelivr.net/npm/'
                f'@polar-sh/checkout@{POLAR_EMBED_VERSION}/dist/embed.global.js"></script>\n')
if uses_gum:
    scripts += '<script src="https://gumroad.com/js/gumroad.js"></script>\n'
page = page.replace("{{CHECKOUT_SCRIPTS}}", scripts)

page, nkeys = extract_i18n(page)

open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sitemap())
nw = make_webp()
nl = make_logo()
print(f"ok: index.html, sitemap.xml, {nw} webp, logo {len(nl)} file, "
      f"{nkeys} stringhe i18n x {len(LANGS)} lingue "
      f"({', '.join(l['code'] for l in LANGS)}), Polar embed {POLAR_EMBED_VERSION}")
