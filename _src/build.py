# Genera il sito statico dello store NewHorizon Builds in ./site
# Uso: python3 build.py   (rilanciare dopo aver cambiato CHECKOUT o i testi)
import json, shutil, os, html

# Link di pagamento: quando ci sono i Checkout Link di Polar, incollarli qui.
# Finche' un link non e' di Polar, il pulsante apre il checkout Gumroad.
# Polar (da attivare quando il prodotto ha lo zip come benefit "File downloads"):
#   jade: https://buy.polar.sh/polar_cl_FvXt7g4Al5p6b8tSTH9dHgSQ0sj1Tq2NUmHFe4F4FDF
CHECKOUT = {
    "jade":    "https://newhorizonmc.gumroad.com/l/jade-dynasty-bedwars",
    "crimson": "https://newhorizonmc.gumroad.com/l/crimson-maple-duels",
    "sunset":  "https://newhorizonmc.gumroad.com/l/sunset-lighthouse-skywars",
    "violet":  "https://newhorizonmc.gumroad.com/l/violet-drop-dropper",
}
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

g = json.load(open("gallery.json"))
e = html.escape

def btn(pid, label_en, label_it, cls="btn buy"):
    url = CHECKOUT[pid]
    extra = ' data-polar-checkout data-polar-checkout-theme="dark"' if "polar.sh" in url else ""
    return f'<a class="{cls}" href="{e(url)}"{extra}><span data-en>{label_en}</span><span data-it>{label_it}</span></a>'

cards = []
for p in P:
    imgs = g[p["id"]]
    thumbs = "".join(
        f'<button class="th" data-full="img/{n}.jpg" data-cap="{e(c)}" aria-label="{e(c)}"><img src="img/{n}_t.jpg" alt="{e(p["name"]+" – "+c)}" loading="lazy" width="320" height="180"></button>'
        for n, c in imgs)
    li_en = "".join(f"<li>{e(b)}</li>" for b in p["bullets"])
    li_it = "".join(f"<li>{e(b)}</li>" for b in p["bullets_it"])
    cards.append(f'''
<article class="pack" id="{p["id"]}" style="--c:{p["color"]}">
  <div class="hero-img"><button class="th big" data-full="img/{imgs[0][0]}.jpg" data-cap="{e(imgs[0][1])}"><img src="img/{imgs[0][0]}.jpg" alt="{e(p["name"])} lobby" loading="lazy" width="1600" height="900"></button></div>
  <div class="info">
    <p class="mode">{e(p["mode"])}</p>
    <h3>{e(p["name"])}</h3>
    <p class="tag"><span data-en>{e(p["tag"])}</span><span data-it>{e(p["tag_it"])}</span></p>
    <ul data-en>{li_en}</ul><ul data-it>{li_it}</ul>
    <p class="meta">{p["files"]} .schem · WorldEdit / FAWE · 1.21 (1.20.3+) · coordinates.json<br><span data-en>Works with</span><span data-it>Compatibile con</span> {e(p["plugins"])}</p>
    <div class="buyrow"><span class="price">${p["price"]}</span>{btn(p["id"], "Buy now", "Acquista")}</div>
  </div>
  <div class="thumbs">{thumbs}</div>
</article>''')

page = open("template.html").read()
page = page.replace("{{PACKS}}", "\n".join(cards)).replace("{{SUPPORT}}", SUPPORT).replace("{{DISCORD}}", DISCORD).replace("{{SITE}}", SITE)
uses_polar = any("polar.sh" in u for u in CHECKOUT.values())
uses_gum = any("gumroad.com" in u for u in CHECKOUT.values())
scripts = ""
if uses_polar:
    scripts += '<script defer data-auto-init src="https://cdn.jsdelivr.net/npm/@polar-sh/checkout@latest/dist/embed.global.js"></script>\n'
if uses_gum:
    scripts += '<script src="https://gumroad.com/js/gumroad.js"></script>\n'
page = page.replace("{{CHECKOUT_SCRIPTS}}", scripts)

out = "site"
if os.path.exists(out): shutil.rmtree(out)
os.makedirs(out)
shutil.copytree("img", out + "/img")
open(out + "/index.html", "w").write(page)
for extra in ["license.html", "legal.html", "favicon.svg", "robots.txt"]:
    if os.path.exists(extra):
        open(out + "/" + extra, "w").write(open(extra).read().replace("{{SUPPORT}}", SUPPORT).replace("{{DISCORD}}", DISCORD).replace("{{SITE}}", SITE))
print("ok", os.listdir(out))
