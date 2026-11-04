# Generează site-ul de mobilă la comandă.
# Rulare: python3 build.py <folder-ieșire>
import os, sys, shutil, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from materiale_date import MAT
from sub_date import SUB, CARD_TXT
import re as _re

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))

C = {
    "nume": "Mobilă la Comandă",            # PROVIZORIU
    "sub": "Fabricăm și montăm în Timișoara și în toată România",
    "tel_afisat": "0759 324 006",
    "tel_link": "+40759324006",
    "whatsapp": "40759324006",               # numărul care primește cererile din formular
    "domeniu": "https://mobilacomandatimisoara.ro",   # gol = fără canonical și sitemap
}

def icon(name, size=26, color="currentColor"):
    p = {
        "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
        "ruler": '<path d="M3 17 17 3l4 4L7 21z"/><path d="m7 13 2 2M10 10l2 2M13 7l2 2"/>',
        "cube": '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
        "truck": '<path d="M1 4h14v12H1zM15 9h4l4 4v3h-8z"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/>',
        "tool": '<path d="M14.7 6.3a4 4 0 0 0 5 5L22 14l-8 8-2.3-2.3a4 4 0 0 0-5-5L4 12l8-8z"/>',
        "saw": '<path d="M3 21 15 9l3 3L6 24"/><path d="M15 9l4-4 2 2-4 4"/>',
        "layers": '<path d="M12 3 2 8l10 5 10-5z"/><path d="m2 13 10 5 10-5"/>',
        "map": '<path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
        "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
        "home": '<path d="M3 11 12 4l9 7v9H3z"/><path d="M9 20v-6h6v6"/>',
        "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
        "arrow": '<path d="M4 12h16M14 6l6 6-6 6"/>',
        "menu": '<path d="M3 7h18M3 12h18M3 17h18"/>',
        "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 17-5-5-9 8"/>',
    }[name]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')

# ---------- ilustrații (desen propriu, până vin pozele reale) ----------
W1, W2, W3, DK, ST = "#D9B48A", "#C29466", "#9C6B43", "#2B241F", "#EFE7DC"
def art(kind):
    g = {
        "bucatarii": f'''<rect x="20" y="40" width="260" height="52" rx="4" fill="{ST}" stroke="#D8CBB9"/>
  <g fill="{W1}" stroke="{W3}" stroke-width="1.5"><rect x="26" y="46" width="78" height="40" rx="2"/><rect x="111" y="46" width="78" height="40" rx="2"/><rect x="196" y="46" width="78" height="40" rx="2"/></g>
  <rect x="14" y="128" width="272" height="10" rx="2" fill="{DK}"/>
  <g fill="{W2}" stroke="{W3}" stroke-width="1.5"><rect x="20" y="138" width="84" height="74" rx="2"/><rect x="108" y="138" width="84" height="74" rx="2"/><rect x="196" y="138" width="84" height="74" rx="2"/></g>
  <g stroke="{DK}" stroke-width="3" stroke-linecap="round"><path d="M50 150h24M138 150h24M226 150h24M55 80h20M140 80h20M225 80h20"/></g>
  <rect x="120" y="108" width="60" height="20" rx="3" fill="#BFC5CC"/><path d="M150 108V96h10" stroke="#8A9199" stroke-width="3" fill="none"/>''',
        "dressinguri": f'''<rect x="30" y="20" width="240" height="196" rx="4" fill="{W1}" stroke="{W3}" stroke-width="1.5"/>
  <g stroke="{W3}" stroke-width="1.5"><path d="M110 20v196M190 20v196"/></g>
  <rect x="116" y="28" width="68" height="180" fill="#E9DCC9"/>
  <path d="M120 60h60" stroke="{DK}" stroke-width="3"/>
  <g fill="{W3}"><rect x="128" y="62" width="10" height="44" rx="2"/><rect x="142" y="62" width="10" height="52" rx="2"/><rect x="156" y="62" width="10" height="40" rx="2"/></g>
  <g fill="{W2}" stroke="{W3}"><rect x="120" y="150" width="60" height="22"/><rect x="120" y="176" width="60" height="22"/></g>
  <g stroke="{DK}" stroke-width="3" stroke-linecap="round"><path d="M102 100v30M198 100v30"/></g>''',
        "dormitoare": f'''<rect x="40" y="60" width="220" height="70" rx="8" fill="{W2}" stroke="{W3}" stroke-width="1.5"/>
  <rect x="34" y="128" width="232" height="58" rx="8" fill="{W1}" stroke="{W3}" stroke-width="1.5"/>
  <rect x="46" y="112" width="208" height="36" rx="10" fill="#F4EEE6" stroke="#D8CBB9"/>
  <g fill="#fff" stroke="#D8CBB9"><rect x="66" y="96" width="70" height="26" rx="10"/><rect x="164" y="96" width="70" height="26" rx="10"/></g>
  <g fill="{W2}" stroke="{W3}"><rect x="2" y="140" width="28" height="46" rx="3"/><rect x="270" y="140" width="28" height="46" rx="3"/></g>
  <rect x="34" y="186" width="10" height="16" fill="{DK}"/><rect x="256" y="186" width="10" height="16" fill="{DK}"/>''',
        "living": f'''<rect x="20" y="150" width="260" height="56" rx="4" fill="{W2}" stroke="{W3}" stroke-width="1.5"/>
  <g stroke="{W3}" stroke-width="1.5"><path d="M106 150v56M194 150v56"/></g>
  <rect x="80" y="40" width="140" height="84" rx="4" fill="{DK}"/><rect x="86" y="46" width="128" height="72" rx="2" fill="#3C4A57"/>
  <g fill="{W1}" stroke="{W3}"><rect x="20" y="60" width="44" height="12"/><rect x="236" y="60" width="44" height="12"/><rect x="20" y="96" width="44" height="12"/><rect x="236" y="96" width="44" height="12"/></g>
  <g stroke="{DK}" stroke-width="3" stroke-linecap="round"><path d="M55 176h26M138 176h26M220 176h26"/></g>''',
        "baie": f'''<rect x="70" y="30" width="160" height="80" rx="6" fill="#E7EEF2" stroke="#C9D4DB"/>
  <rect x="50" y="130" width="200" height="12" rx="3" fill="{ST}" stroke="#D8CBB9"/>
  <ellipse cx="150" cy="130" rx="44" ry="8" fill="#fff" stroke="#C9D4DB"/>
  <path d="M150 122v-14h10" stroke="#8A9199" stroke-width="3" fill="none"/>
  <g fill="{W1}" stroke="{W3}" stroke-width="1.5"><rect x="56" y="142" width="92" height="64" rx="2"/><rect x="152" y="142" width="92" height="64" rx="2"/></g>
  <g stroke="{DK}" stroke-width="3" stroke-linecap="round"><path d="M90 154h24M186 154h24"/></g>''',
        "birouri": f'''<rect x="30" y="110" width="240" height="12" rx="3" fill="{W2}" stroke="{W3}"/>
  <g fill="{W1}" stroke="{W3}" stroke-width="1.5"><rect x="36" y="122" width="70" height="86" rx="2"/></g>
  <g stroke="{W3}" stroke-width="1.5"><path d="M36 150h70M36 178h70"/></g>
  <rect x="250" y="122" width="10" height="86" fill="{DK}"/>
  <rect x="140" y="58" width="90" height="52" rx="4" fill="{DK}"/><rect x="146" y="64" width="78" height="40" rx="2" fill="#3C4A57"/>
  <g fill="{W1}" stroke="{W3}"><rect x="30" y="30" width="80" height="10"/><rect x="30" y="64" width="80" height="10"/></g>''',
    }[kind]
    return f'<svg class="art" viewBox="0 0 300 220" aria-hidden="true">{g}</svg>'

# ---------- date ----------
PRODUSE = [
    dict(slug="bucatarii-la-comanda", art="bucatarii", titlu="Bucătării la comandă", scurt="Bucătării pe măsura spațiului tău, de la colțuri înguste până la insule mari.",
         lung="Facem bucătăria pe centimetru, după măsurătorile din casa ta: corpuri suspendate până la tavan, colțuri folosite complet, loc pentru electrocasnicele încorporabile, blat și feronerie la alegere. Primești proiectul 3D înainte de producție, ca să vezi exact cum va arăta.",
         idei=["Bucătării drepte, în L sau în U", "Insulă sau peninsulă cu loc de luat masa", "Corpuri până la tavan, cu spațiu mare de depozitare", "Loc pentru cuptor, plită, frigider și mașină de spălat vase încorporabile"]),
    dict(slug="dressinguri-la-comanda", art="dressinguri", titlu="Dressinguri la comandă", scurt="Dressinguri și dulapuri încastrate care folosesc tot spațiul, de la podea la tavan.",
         lung="Un dressing făcut pe măsură folosește fiecare centimetru: nișe, mansarde, pereți strâmbi sau camere mici. Alegem împreună bare de haine, sertare, rafturi pentru pantofi și uși glisante sau batante.",
         idei=["Dressing walk-in sau dulap încastrat", "Uși glisante, cu oglindă sau fără uși", "Sertare, rafturi pentru pantofi, accesorii", "Soluții pentru mansarde și nișe"]),
    dict(slug="dormitoare-la-comanda", art="dormitoare", titlu="Dormitoare la comandă", scurt="Paturi, noptiere, comode și dulapuri, toate în același stil.",
         lung="Facem dormitorul complet, într-un singur stil: pat cu sau fără ladă, tăblie, noptiere, comodă, dulap sau dressing. Totul pe dimensiunile camerei tale și în culorile pe care le alegi.",
         idei=["Pat cu ladă de depozitare", "Tăblie tapițată sau din lemn", "Noptiere și comode asortate", "Camere pentru copii și adolescenți"]),
    dict(slug="living-la-comanda", art="living", titlu="Living la comandă", scurt="Comode TV, biblioteci și corpuri de living care se potrivesc exact peretelui tău.",
         lung="Corpuri TV, biblioteci, vitrine și rafturi suspendate, făcute pe lungimea exactă a peretelui. Ascundem cablurile, facem loc pentru boxe și console și potrivim mobila cu restul casei.",
         idei=["Comodă TV și perete de living", "Biblioteci și rafturi suspendate", "Vitrine cu iluminare", "Cabluri ascunse și loc pentru aparatură"]),
    dict(slug="mobila-baie-la-comanda", art="baie", titlu="Mobilă de baie la comandă", scurt="Mobilier de baie rezistent la umezeală, pe măsura băii tale.",
         lung="Facem mobilier de baie din materiale potrivite pentru umezeală: corpuri sub lavoar, coloane, dulapuri cu oglindă și rafturi. Potrivit și pentru băile mici, unde fiecare centimetru contează.",
         idei=["Corp sub lavoar sau sub blat", "Coloane și dulapuri suspendate", "Dulap cu oglindă", "Spații pentru mașina de spălat"]),
    dict(slug="mobila-birou-la-comanda", art="birouri", titlu="Mobilă de birou și pentru firme", scurt="Birouri, recepții, mobilier pentru magazine, restaurante și hoteluri.",
         lung="Lucrăm și pentru firme: birouri, săli de ședință, recepții, mobilier pentru magazine, restaurante, cafenele și hoteluri. Facem proiectul, producem și montăm, inclusiv pentru mai multe spații deodată.",
         idei=["Birouri de lucru și săli de ședință", "Recepții", "Mobilier pentru magazine și showroom-uri", "Mobilier pentru restaurante, cafenele și hoteluri"]),
]
ORASE = ["Timișoara", "Arad", "Oradea", "Alba Iulia", "Hunedoara", "Deva", "Lugoj", "Reșița", "Sebeș", "Caransebeș"]
def kw(href, text): return f'<a class="kw" href="{href}.html">{text}</a>'

# ---------- comune ----------

def logo_mark(size=46):
    return f'''<svg class="logo-mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true">
  <defs><linearGradient id="lgb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3D3029"/><stop offset="1" stop-color="#1C1714"/></linearGradient>
  <linearGradient id="lga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6C27A"/><stop offset="1" stop-color="#D9822B"/></linearGradient></defs>
  <rect width="48" height="48" rx="13" fill="url(#lgb)"/>
  <rect x="1" y="1" width="46" height="46" rx="12" fill="none" stroke="#F6C27A" stroke-opacity=".18"/>
  <path d="M13.5 33V15l10.5 10.5L34.5 15v18" fill="none" stroke="url(#lga)" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M11 38.5h26" stroke="#F6C27A" stroke-opacity=".55" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="24" cy="31.5" r="1.6" fill="#F6C27A"/>
</svg>'''

def logo(light=False):
    a, b = (C["nume"].split(" ", 1) + [""])[:2]
    return f'''<span class="logo{' logo-light' if light else ''}">{logo_mark()}<span class="wm"><span class="wm1">{a} <i>{b}</i></span><small>{C["sub"]}</small></span></span>'''

def header():
    return f'''<div class="live"><div class="wrap"><span class="dot"></span>Răspundem acum<span class="hide-m"> · Măsurători gratuite în Timișoara și în toată țara</span></div></div>
<header class="top"><div class="wrap">
  <a class="brand" href="index.html" aria-label="{C["nume"]}, pagina principală">
    {logo()}
  </a>
  <nav class="menu nav-desktop" aria-label="Meniu principal"><div class="wrap">
    <a href="index.html#produse">Ce facem</a><a href="index.html#lucrari">Lucrări</a><a href="materiale.html">Materiale</a>
    <a href="index.html#cum">Cum lucrăm</a><a href="index.html#intrebari">Întrebări</a><a href="index.html#oferta">Cere ofertă</a>
  </div></nav>
  <a class="call-dot" href="tel:{C["tel_link"]}" aria-label="Sună la {C["tel_afisat"]}">{icon("phone", 24, "#fff")}</a>
  <button class="menu-btn" type="button" aria-label="Meniu" aria-expanded="false" id="menu-btn">{icon("menu", 26, "#2B241F")}</button>
</div></header>'''

def footer():
    prod = "".join(f'<li><a href="{p["slug"]}.html">{p["titlu"]}</a></li>' for p in PRODUSE)
    oras = "".join(f'<li><a href="{oras_slug(o)}.html">Mobilă la comandă {o}</a></li>' for o in ORASE)
    return f'''<footer><div class="wrap">
  <div class="cols">
    <div><a href="index.html" class="f-logo" aria-label="{C["nume"]}">{logo(True)}</a><p style="margin-top:14px">Mobilă la comandă pentru casă și pentru firme. Măsurători gratuite, proiect 3D, transport și montaj incluse, în toată România.</p></div>
    <div><h4>Ce facem</h4><ul>{prod}<li><a href="materiale.html">Materiale</a></li></ul></div>
    <div><h4>Orașe</h4><ul>{oras}</ul></div>
    <div><h4>Contact</h4><ul><li><a href="tel:{C["tel_link"]}">{C["tel_afisat"]}</a></li><li><a href="index.html#oferta">Cere ofertă</a></li></ul></div>
  </div>
  <p class="legal">© 2026 {C["nume"]}. Toate drepturile rezervate.</p>
</div></footer>
<div class="sticky"><a href="tel:{C["tel_link"]}"><span class="ring">{icon("phone", 24, "#fff")}</span><span><small>Sună pentru măsurători gratuite</small><b>{C["tel_afisat"]}</b></span></a></div>
<script>
(function(){{var b=document.getElementById("menu-btn"),m=document.querySelector("nav.menu");if(!b||!m)return;
b.addEventListener("click",function(){{var o=m.classList.toggle("open");b.setAttribute("aria-expanded",o)}});
m.addEventListener("click",function(e){{if(e.target.tagName==="A"){{m.classList.remove("open");b.setAttribute("aria-expanded","false")}}}});}})();
</script>'''

def oras_slug(o):
    t = o.lower().replace("ș", "s").replace("ț", "t").replace("ă", "a").replace("â", "a").replace("î", "i").replace(" ", "-")
    return "mobila-la-comanda-" + t

# ---------- date structurate (schema.org) ----------
import json as _json, re as _ld_re
def ld_tag(obj):
    s = _json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json">{s}</script>\n'

def breadcrumb_ld(path, body):
    # Se construiește din firimiturile vizibile pe pagină, ca să spună același lucru.
    m = _ld_re.search(r'<p class="crumbs">(.*?)</p>', body, _ld_re.S)
    if not m or not C["domeniu"]: return ""
    crumbs = m.group(1)
    items = [(html.unescape(t).strip(), C["domeniu"] + "/" + ("" if h == "index.html" else h))
             for h, t in _ld_re.findall(r'<a href="([^"]+)">(.*?)</a>', crumbs)]
    last = _ld_re.sub(r"<[^>]+>", "", crumbs[crumbs.rfind("</a>") + 4:]).lstrip(" /›").strip()
    items.append((html.unescape(last), C["domeniu"] + "/" + path))
    return ld_tag({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(items, 1)]})

def site_ld(business):
    business = {"@id": C["domeniu"] + "/#firma", "url": C["domeniu"] + "/", **business}
    return ld_tag({"@context": "https://schema.org", "@graph": [business, {
        "@type": "WebSite", "@id": C["domeniu"] + "/#site", "url": C["domeniu"] + "/",
        "name": C["nume"], "inLanguage": "ro", "publisher": {"@id": C["domeniu"] + "/#firma"}}]})

def page(title, desc, path, body):
    canon = C["domeniu"] + "/" + ("" if path == "index.html" else path)
    canon_tag = f'<link rel="canonical" href="{canon}">\n' if C["domeniu"] else ""
    canon_tag += site_ld({"@type": "HomeAndConstructionBusiness", "name": C["nume"],
                          "description": "Mobilă la comandă în Timișoara și în toată România", "telephone": C["tel_link"],
                          "areaServed": [{"@type": "City", "name": "Timișoara"}, {"@type": "Country", "name": "România"}]}) if path == "index.html" else breadcrumb_ld(path, body)
    return f'''<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{canon_tag}<meta name="theme-color" content="#2B241F">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>
{header()}
<main>
{body}
</main>
{footer()}
</body>
</html>
'''

def faq_html(items): return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
def call_btn(label="Sună acum"):
    return f'<a class="btn" href="tel:{C["tel_link"]}">{icon("phone", 24, "#fff")}<span><small>{label}</small>{C["tel_afisat"]}</span></a>'

def why_block():
    return f'''<div class="why">
  <h2>Ce primești de la noi</h2>
  <ul class="checks">
    <li>Măsurători gratuite la tine acasă, oriunde în țară</li>
    <li>Proiect 3D înainte de producție, ca să vezi exact cum va arăta</li>
    <li>Lucrăm cu toate materialele: {kw("pal-melaminat","PAL melaminat")}, {kw("mdf-vopsit","MDF vopsit")}, {kw("lemn-masiv","lemn masiv")}, {kw("furnir","furnir")}</li>
    <li>Transport și montaj incluse în preț</li>
    <li>Un singur om de contact, de la măsurători până la montaj</li>
  </ul>
  <a class="btn" href="tel:{C["tel_link"]}">{icon("phone", 22, "#fff")} Sună acum {C["tel_afisat"]}</a>
</div>'''

def kwtxt(t):
    """Transformă {slug|text} în link de cuvânt-cheie."""
    return _re.sub(r"\{([a-z0-9-]+)\|([^}]+)\}", lambda m: kw(m.group(1), m.group(2)), t)

def prod_cards():
    return "".join(f'''<div class="pcard"><a class="pimg" href="{p["slug"]}.html" tabindex="-1" aria-hidden="true">{art(p["art"])}</a>
  <div class="pbody"><h3>{kw(p["slug"], p["titlu"])}</h3><p>{kwtxt(CARD_TXT[p["slug"]])}</p><a class="more" href="{p["slug"]}.html">Detalii {icon("arrow", 20)}</a></div></div>''' for p in PRODUSE)

PROIECTE = [
    dict(titlu="Bucătărie albă cu lemn închis", sub="Fețe albe fără mânere, corpuri sus și placare în decor de lemn, iluminare LED",
         poze=[("alba-1", "Bucătărie liniară: fețe albe fără mânere, corpuri suspendate și placare în decor de lemn închis, bandă LED sub corpuri, coloană pentru cuptor și cuptor cu microunde încorporabile", 1600, 1200)]),
    dict(titlu="Bucătărie bej cu raft deschis", sub="Corpuri până la cornișă, raft deschis și sertare mari",
         poze=[("bucatarie-1", "Corpuri suspendate și raft deschis pentru căni și farfurii", 4080, 3072),
               ("bucatarie-2", "Corpuri suspendate pe toată lungimea peretelui, până la cornișă", 4080, 3072),
               ("bucatarie-3", "Corpuri jos cu sertare mari și picioare reglabile", 4080, 3072),
               ("bucatarie-4", "Coloană cu nișă pentru cuptorul cu microunde și dulap înalt", 2467, 3935)]),
]
def galerie():
    out = ""
    for pr in PROIECTE:
        tiles = ""
        for i, (f, alt, w, h) in enumerate(pr["poze"]):
            cls = "ph ph-big" if i == 0 else ("ph ph-tall" if h > w else "ph")
            tiles += (f'<a class="{cls}" href="lucrari/{f}.jpg" data-cap="{alt}">'
                      f'<img src="lucrari/{f}-mic.jpg" srcset="lucrari/{f}-mic.jpg 720w, lucrari/{f}.jpg 1600w" '
                      f'sizes="(min-width:900px) 60vw, 100vw" alt="{pr["titlu"]}: {alt[0].lower() + alt[1:]}" loading="lazy" width="{w}" height="{h}">'
                      f'<span class="ph-cap">{alt}</span></a>')
        one = " one" if len(pr["poze"]) == 1 else ""
        out += f'''<div class="project">
  <div class="project-head"><h3>{pr["titlu"]}</h3><p>{pr["sub"]}</p></div>
  <div class="photos{one}">{tiles}</div>
</div>
'''
    return out + f'''<div class="lb" id="lb" hidden><button class="lb-x" type="button" aria-label="Închide">×</button><button class="lb-p" type="button" aria-label="Poza anterioară">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-n" type="button" aria-label="Poza următoare">›</button></div>
<script>
(function(){{
  var lb=document.getElementById("lb"); if(!lb) return;
  var links=[].slice.call(document.querySelectorAll(".photos a")), img=lb.querySelector("img"), cap=lb.querySelector("figcaption"), i=0;
  function show(k){{ i=(k+links.length)%links.length; img.src=links[i].href; img.alt=links[i].querySelector("img").alt; cap.textContent=links[i].dataset.cap; }}
  function close(){{ lb.hidden=true; document.body.style.overflow=""; }}
  links.forEach(function(a,k){{ a.addEventListener("click",function(e){{ e.preventDefault(); show(k); lb.hidden=false; document.body.style.overflow="hidden"; lb.querySelector(".lb-x").focus(); }}); }});
  lb.querySelector(".lb-x").onclick=close; lb.querySelector(".lb-p").onclick=function(){{show(i-1)}}; lb.querySelector(".lb-n").onclick=function(){{show(i+1)}};
  lb.addEventListener("click",function(e){{ if(e.target===lb||e.target.tagName==="FIGURE") close(); }});
  document.addEventListener("keydown",function(e){{ if(lb.hidden) return; if(e.key==="Escape") close(); if(e.key==="ArrowLeft") show(i-1); if(e.key==="ArrowRight") show(i+1); }});
  var x0=null; lb.addEventListener("touchstart",function(e){{x0=e.touches[0].clientX}},{{passive:true}});
  lb.addEventListener("touchend",function(e){{ if(x0===null) return; var dx=e.changedTouches[0].clientX-x0; if(Math.abs(dx)>40) show(dx<0?i+1:i-1); x0=null; }});
}})();
</script>'''

STEPS = [
    ("Ne suni sau ceri ofertă", "Ne spui ce mobilă vrei și în ce oraș ești. Îți răspundem în aceeași zi.", "Răspuns rapid"),
    ("Măsurători gratuite", "Venim la tine, măsurăm exact și discutăm ce materiale și culori îți plac.", "Gratuit, oriunde în țară"),
    ("Proiect 3D și ofertă", "Primești proiectul 3D și prețul final. Modificăm până arată cum vrei.", "Vezi totul înainte"),
    ("Producție", "Fabricăm mobila pe dimensiunile măsurate, cu materialele alese de tine.", "Pe centimetru"),
    ("Transport și montaj", "Aducem mobila și o montăm. Plecăm doar după ce totul e la locul lui.", "Incluse în preț"),
]
def steps_html():
    return '<div class="steps">' + "".join(f'<div class="step"><div><h3>{t}</h3><p>{d}</p><span class="tag">{g}</span></div></div>' for t, d, g in STEPS) + "</div>"

# ---------- formular cerere ofertă ----------
WA_ICON = '<svg width="22" height="22" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'

def oferta_section():
    tipuri = "".join(f"<option>{p['titlu']}</option>" for p in PRODUSE)
    oras_opts = "".join(f"<option>{o}</option>" for o in ORASE)
    return f'''
<section id="oferta" class="order-sec"><div class="wrap">
  <div class="head"><span class="eyebrow pill">Cere ofertă</span><h2>Cere o ofertă sau programează măsurătorile</h2>
  <p>Completează câteva detalii și apasă butonul: cererea se deschide gata scrisă în WhatsApp, iar tu doar o trimiți. Măsurătorile sunt gratuite, iar oferta nu te obligă la nimic.</p></div>
  <form id="of-form" class="order" novalidate>
    <fieldset class="fs">
      <legend><span class="n">{icon("user", 20, "#fff")}</span>Datele tale</legend>
      <div class="row2">
        <label>Numele tău <em>*</em><input name="Nume" required autocomplete="name"></label>
        <label>Telefonul tău <em>*</em><input name="Telefon" id="f-tel" type="tel" required autocomplete="tel" placeholder="+40 7xx xxx xxx"><span class="err-txt" id="tel-err" hidden>Scrie un număr de telefon valid, ca să te putem suna.</span></label>
      </div>
      <div class="row2">
        <label>Orașul / localitatea <em>*</em><input name="Oraș" required list="orase" autocomplete="address-level2"><datalist id="orase">{oras_opts}</datalist></label>
        <label>Județul<input name="Județ"></label>
      </div>
    </fieldset>
    <fieldset class="fs">
      <legend><span class="n">{icon("cube", 20, "#fff")}</span>Ce mobilă vrei</legend>
      <div class="row2">
        <label>Tip de mobilă <em>*</em><select name="Tip mobilă" required><option value="">Alege...</option>{tipuri}<option>Altceva / mai multe</option></select></label>
        <label>Material preferat<select name="Material"><option>Nu știu încă, vreau recomandare</option><option>PAL melaminat</option><option>MDF vopsit</option><option>Lemn masiv</option><option>Furnir</option></select></label>
      </div>
      <label>Dimensiuni aproximative <small>(opțional)</small><input name="Dimensiuni" placeholder="de ex. perete de 3,2 m, tavan 2,6 m"></label>
      <label>Descriere <small>(opțional)</small><textarea name="Descriere" rows="3" placeholder="Ce îți dorești: culori, stil, electrocasnice, orice detaliu ne ajută"></textarea></label>
      <label>Când ți-ar conveni măsurătorile <small>(opțional)</small><input name="Dată măsurători" placeholder="de ex. sâmbătă dimineața, săptămâna viitoare"></label>
    </fieldset>
    <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <label class="agree"><input type="checkbox" required> Sunt de acord să fiu contactat telefonic sau pe WhatsApp pentru această cerere.</label>
    <button class="btn btn-wa" type="submit" id="of-submit">{WA_ICON} Trimite cererea pe WhatsApp</button>
    <div id="of-msg" class="order-msg err" role="alert" hidden></div>
  </form>
  <div id="of-ok" class="order-ok" tabindex="-1" hidden>
    <div class="ok-ic"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>
    <h3>Vă mulțumim!</h3>
    <p class="ok-thanks">Cererea ta e gata în WhatsApp.</p>
    <div class="ok-sum" id="ok-sum"></div>
    <p class="ok-next"><b>Ultimul pas:</b> în WhatsApp, apasă <b>Trimite</b>. Dacă WhatsApp nu s-a deschis, apasă butonul de mai jos.</p>
    <p style="margin-top:16px"><a class="btn btn-wa" id="wa-again" href="https://wa.me/{C["whatsapp"]}" target="_blank" rel="noopener">{WA_ICON} Deschide WhatsApp</a></p>
    <p class="ok-urgent">Dacă vrei să vorbim acum: <a href="tel:{C["tel_link"]}">{C["tel_afisat"]}</a></p>
    <button type="button" class="btn ghost" id="ok-again">Trimite altă cerere</button>
  </div>
</div></section>
<script>
(function(){{
  var f=document.getElementById("of-form"); if(!f) return;
  var tel=document.getElementById("f-tel"), btn=document.getElementById("of-submit"), msg=document.getElementById("of-msg");
  tel.addEventListener("input",function(){{ tel.setCustomValidity(""); document.getElementById("tel-err").hidden=true; }});
  document.getElementById("ok-again").addEventListener("click",function(){{ document.getElementById("of-ok").hidden=true; f.hidden=false; f.scrollIntoView({{block:"start",behavior:"smooth"}}); }});
  var esc=function(x){{ return String(x).replace(/[&<>"]/g,function(c){{ return {{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]; }}); }};
  f.addEventListener("submit",function(e){{
    e.preventDefault();
    var cifre=(tel.value.match(/\\d/g)||[]).length;
    tel.setCustomValidity(cifre>=9 && cifre<=15 ? "" : "Scrie un număr de telefon valid.");
    document.getElementById("tel-err").hidden=tel.validity.valid;
    if(!f.checkValidity()){{ f.reportValidity(); return; }}
    var d={{}}; new FormData(f).forEach(function(v,k){{ d[k]=v; }});
    var ordine=["Nume","Telefon","Oraș","Județ","Tip mobilă","Material","Dimensiuni","Descriere","Dată măsurători"];
    var txt="Bună ziua! Aș dori o ofertă pentru mobilă la comandă.\\n";
    ordine.forEach(function(k){{ var v=(d[k]||"").trim(); if(v) txt+="\\n"+k+": "+v; }});
    var url="https://wa.me/{C["whatsapp"]}?text="+encodeURIComponent(txt);
    document.getElementById("wa-again").href=url;
    document.getElementById("ok-sum").innerHTML="<div><span>Mobilă</span><b>"+esc(d["Tip mobilă"])+"</b></div><div><span>Oraș</span><b>"+esc(d["Oraș"])+"</b></div><div><span>Material</span><b>"+esc(d["Material"])+"</b></div>";
    f.reset(); msg.hidden=true; f.hidden=true;
    var ok=document.getElementById("of-ok"); ok.hidden=false; ok.scrollIntoView({{block:"center",behavior:"smooth"}});
    var w=window.open(url,"_blank"); if(!w) window.location.href=url;
  }});
}})();
</script>'''

FAQ = [
    ("Cât costă mobila la comandă?", "Prețul depinde de dimensiuni, materiale și feronerie. După măsurători primești proiectul 3D și prețul final, cu transportul și montajul incluse. Nu plătești nimic pentru măsurători și ofertă."),
    ("Măsurătorile sunt chiar gratuite?", "Da, venim gratuit la măsurători, oriunde în România. Sună-ne și stabilim o zi care ți se potrivește."),
    ("În cât timp e gata mobila?", "Depinde de ce comanzi și de materialele alese. Termenul exact ți-l spunem în ofertă, înainte să începem."),
    ("Pot vedea cum arată înainte să comand?", "Da. Primești un proiect 3D cu mobila în camera ta, cu culorile și materialele alese. Îl modificăm până arată cum vrei."),
    ("Transportul și montajul se plătesc separat?", "Nu, sunt incluse în preț, oriunde în țară."),
    ("Lucrați și pentru firme?", f"Da. Facem mobilier pentru birouri, magazine, restaurante și hoteluri. Vezi {kw('mobila-birou-la-comanda','mobilă de birou și pentru firme')}."),
]

# ---------- pagini ----------
def index():
    orase = ", ".join(kw(oras_slug(o), o) for o in ORASE[:6])
    body = f'''
<div class="hx">
  <div class="hx-bg" aria-hidden="true"><img src="lucrari/alba-1.jpg" alt="" width="1600" height="1200" fetchpriority="high"></div>
  <div class="wrap hx-in">
    <span class="eyebrow pill pill-glass">Fabricăm și montăm · Timișoara, Arad, Oradea, Alba, Hunedoara</span>
    <h1>Mobilă la comandă în <em>Timișoara</em>, făcută pe centimetru pentru casa ta</h1>
    <p class="lead">Facem {kw("bucatarii-la-comanda","bucătării")}, {kw("dressinguri-la-comanda","dressinguri")}, {kw("dormitoare-la-comanda","dormitoare")}, {kw("living-la-comanda","mobilă de living")}, {kw("mobila-baie-la-comanda","mobilă de baie")} și {kw("mobila-birou-la-comanda","mobilier pentru firme")}, din {kw("pal-melaminat","PAL melaminat")}, {kw("mdf-vopsit","MDF vopsit")} sau {kw("lemn-masiv","lemn masiv")}. Lucrăm în {orase} și oriunde în țară.</p>
    <div class="cta-row">{call_btn()}<a class="btn ghost ghost-light" href="#oferta">Cere ofertă gratuită</a></div>
    <p class="hx-cap">{icon("image", 16, "#F3B46B")} Bucătărie realizată și montată de echipa noastră</p>
  </div>
</div>
<div class="wrap"><div class="trust">
  <div class="t-item"><span class="t-ic">{icon("ruler", 24, "#fff")}</span><div><b>Măsurători gratuite</b><span>venim la tine acasă</span></div></div>
  <div class="t-item"><span class="t-ic">{icon("cube", 24, "#fff")}</span><div><b>Proiect 3D</b><span>vezi totul înainte</span></div></div>
  <div class="t-item"><span class="t-ic">{icon("truck", 24, "#fff")}</span><div><b>Transport inclus</b><span>în prețul ofertei</span></div></div>
  <div class="t-item"><span class="t-ic">{icon("tool", 24, "#fff")}</span><div><b>Montaj inclus</b><span>plecăm când e gata</span></div></div>
</div></div>

<section id="produse"><div class="wrap">
  <div class="head"><span class="eyebrow pill">Ce facem</span><h2>Mobilă la comandă pentru fiecare cameră</h2><p>Alege ce te interesează ca să vezi detalii și idei.</p></div>
  <div class="pgrid">{prod_cards()}</div>
</div></section>

<section id="lucrari" class="band"><div class="wrap">
  <div class="head"><span class="eyebrow pill pill-dark">Lucrări</span><h2>Din lucrările noastre</h2><p>Poze reale de la clienții noștri. Apasă pe o poză ca să o vezi mare.</p></div>
  {galerie()}
  <div class="cta-row"><a class="btn" href="#oferta">Vreau și eu o ofertă</a></div>
</div></section>

<section id="cum"><div class="wrap">
  <div class="head"><span class="eyebrow pill">Cum lucrăm</span><h2>Cinci pași, de la idee până la mobila montată</h2></div>
  {steps_html()}
</div></section>

<section class="dark"><div class="wrap">
  <div class="head"><span class="eyebrow pill pill-dark">Materiale</span><h2>Lucrăm cu toate materialele</h2><p>Te ajutăm să alegi materialul potrivit pentru buget și pentru cum folosești mobila.</p></div>
  <div class="mat-grid">{"".join(f'<a class="mat" href="{m["slug"]}.html"><h3><span class="kw">{m["nume"]}</span></h3><p>{m["scurt"]}</p><span class="mat-more">Află mai multe {icon("arrow", 18)}</span></a>' for m in MAT)}</div>
  <div class="cta-row"><a class="btn" href="materiale.html">Detalii despre materiale</a></div>
</div></section>

<section class="cta-band"><div class="wrap cta-in">
  <div><h2>Programează măsurătorile gratuite</h2><p>Venim la tine, măsurăm și îți facem proiectul 3D. Abia apoi decizi.</p></div>
  <div class="cta-row">{call_btn()}<a class="btn ghost ghost-light" href="#oferta">Completează cererea</a></div>
</div></section>

{oferta_section()}

<section><div class="wrap">{why_block()}</div></section>

<section id="intrebari"><div class="wrap">
  <div class="head"><span class="eyebrow pill">Întrebări frecvente</span><h2>Mobilă la comandă: întrebări și răspunsuri</h2></div>
  <div class="faq">{faq_html(FAQ)}</div>
</div></section>

<section id="contact" class="final"><div class="wrap">
  <span class="eyebrow pill">Contact</span>
  <h2>Vrei mobilă pe măsură? Sună acum.</h2>
  <p style="margin-top:12px;color:var(--muted)">Stabilim împreună ziua pentru măsurătorile gratuite.</p>
  <a class="phone-big" href="tel:{C["tel_link"]}">{C["tel_afisat"]}</a>
</div></section>
'''
    return page(f"Mobilă la comandă în Timișoara: bucătării, dressinguri | {C['nume']}",
                "Mobilă la comandă în Timișoara: bucătării, dressinguri, dormitoare, living, baie și birouri. Măsurători gratuite, proiect 3D, transport și montaj incluse. Lucrăm și în restul României.",
                "index.html", body)

def galerie_prod(p):
    if p["art"] != "bucatarii": return ""
    return f'''<section class="band"><div class="wrap">
  <div class="head"><span class="eyebrow pill pill-dark">Lucrări</span><h2>Bucătării făcute de noi</h2><p>Apasă pe o poză ca să o vezi mare.</p></div>
  {galerie()}
  <div class="cta-row"><a class="btn" href="index.html#oferta">Vreau și eu o bucătărie</a></div>
</div></section>'''

def produs_page(p):
    alte = ", ".join(kw(x["slug"], x["titlu"].lower()) for x in PRODUSE if x is not p)
    idei = "".join(f"<li>{i}</li>" for i in p["idei"])
    orase = ", ".join(kw(oras_slug(o), o) for o in ORASE)
    body = f'''
<div class="hero hero-k"><div class="wrap">
  <p class="crumbs"><a href="index.html">Acasă</a> / {p["titlu"]}</p>
  <div class="hk" style="margin-top:14px">
    <div>
      <span class="eyebrow pill">Măsurători gratuite · Montaj inclus</span>
      <h1>{p["titlu"]}</h1>
      <p class="lead" style="margin-top:12px">{p["scurt"]} {p["lung"]}</p>
      <div class="cta-row">{call_btn()}<a class="btn ghost" href="index.html#oferta">Cere ofertă</a></div>
    </div>
    <div class="hk-img">{'<img class=\"hero-photo\" src=\"lucrari/alba-1-hero.jpg\" alt=\"Bucătărie la comandă albă cu lemn închis, realizată de noi\" width=\"1100\" height=\"825\">' if p["art"] == "bucatarii" else art(p["art"])}</div>
  </div>
</div></div>
<section><div class="wrap"><div class="two">
  <div class="prose">
    <h2 style="margin-top:0">Ce putem face</h2>
    <ul class="ticks-l">{idei}</ul>
    {variante(p)}
    <h2>Materiale</h2>
    <p>Lucrăm cu {kw("pal-melaminat","PAL melaminat")}, {kw("mdf-vopsit","MDF vopsit")}, {kw("lemn-masiv","lemn masiv")} și {kw("furnir","furnir")}, cu {kw("feronerie-mobila","feronerie")} cu închidere lină{", plus " + kw("blaturi-bucatarie","blaturi de bucătărie") + " din PAL, compact, cuarț sau piatră" if p["art"] in ("bucatarii","baie") else ""}. La măsurători îți arătăm mostre și te ajutăm să alegi. Vezi {kw("materiale","toate materialele")}.</p>
    <h2>Cum lucrăm</h2>
    <p>Venim gratuit la măsurători, îți facem proiectul 3D și oferta, producem mobila și o montăm. Transportul și montajul sunt incluse în preț.</p>
    <h2>Unde lucrăm</h2>
    <p>În toată România, inclusiv în {orase}.</p>
    <h2>Mai facem</h2>
    <p>{alte[0].upper() + alte[1:] if alte else ""}.</p>
  </div>
  {why_block()}
</div></div></section>
{galerie_prod(p)}'''
    return page(f"{p['titlu']}: măsurători gratuite, montaj inclus | {C['nume']}",
                f"{p['titlu']} în toată România. {p['scurt']} Măsurători gratuite, proiect 3D, transport și montaj incluse.",
                p["slug"] + ".html", body)

def materiale_page():
    det = "".join(f'<h2>{kw(m["slug"], m["nume"])}</h2><p>{m["scurt"]} {m["ce"]}</p><p><a class="more-l" href="{m["slug"]}.html">Tot despre {m["nume"].lower()} →</a></p>' for m in MAT)
    body = f'''
<div class="hero"><div class="wrap">
  <p class="crumbs"><a href="index.html">Acasă</a> / Materiale</p>
  <span class="eyebrow pill" style="margin-top:14px">Materiale</span>
  <h1>Materiale pentru <em>mobila la comandă</em></h1>
  <p class="lead" style="margin-top:12px">Lucrăm cu toate materialele. Alegerea depinde de buget, de cameră și de cât de intens folosești mobila. La {kw("bucatarii-la-comanda","bucătării")} contează mult {kw("blaturi-bucatarie","blatul")}ul și fețele, iar la {kw("mobila-baie-la-comanda","baie")}, rezistența la umezeală.</p>
  <div class="cta-row">{call_btn()}</div>
</div></div>
<section><div class="wrap"><div class="two">
  <div class="prose">{det}<h2>Nu știi ce să alegi?</h2><p>La măsurători aducem mostre și îți spunem sincer ce merită pentru bugetul tău.</p></div>
  {why_block()}
</div></div></section>
'''
    return page(f"Materiale pentru mobilă la comandă: PAL, MDF, lemn masiv | {C['nume']}",
                "PAL melaminat, MDF vopsit, lemn masiv, furnir, blaturi și feronerie: cum alegi materialul potrivit pentru mobila la comandă.",
                "materiale.html", body)

def oras_page(o):
    prod = ", ".join(kw(p["slug"], p["titlu"].replace(" la comandă", "").lower()) for p in PRODUSE)
    alte = ", ".join(kw(oras_slug(x), x) for x in ORASE if x != o)
    body = f'''
<div class="hero hero-k"><div class="wrap">
  <p class="crumbs"><a href="index.html">Acasă</a> / Mobilă la comandă {o}</p>
  <span class="eyebrow pill" style="margin-top:14px">Măsurători gratuite în {o}</span>
  <h1>Mobilă la comandă <em>{o}</em></h1>
  <p class="lead" style="margin-top:12px">Facem mobilă la comandă pentru casele și firmele din {o} și împrejurimi: {prod}. Venim gratuit la măsurători, îți facem proiectul 3D, iar transportul și montajul sunt incluse.</p>
  <div class="cta-row">{call_btn()}<a class="btn ghost" href="index.html#oferta">Cere ofertă</a></div>
</div></div>
<section><div class="wrap"><div class="two">
  <div class="prose">
    <h2 style="margin-top:0">Cum lucrăm în {o}</h2>
    <p>Ne suni sau ne lași o cerere, stabilim o zi și venim la tine pentru măsurători. Primești proiectul 3D și prețul final. După producție aducem mobila și o montăm, fără costuri în plus pentru transport.</p>
    <h2>Lucrăm și în alte orașe</h2>
    <p>{alte} și oriunde în România.</p>
  </div>
  {why_block()}
</div></div></section>
'''
    return page(f"Mobilă la comandă {o}: măsurători gratuite, montaj inclus | {C['nume']}",
                f"Mobilă la comandă în {o}: bucătării, dressinguri, dormitoare, living, baie și birouri. Măsurători gratuite, proiect 3D, transport și montaj incluse.",
                oras_slug(o) + ".html", body)


def material_page(m):
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    tipuri = ""
    if m.get("tipuri"):
        tipuri = "<h2>Variante</h2>" + "".join(f'<div class="vrow"><b>{t}</b><span>{d}</span></div>' for t, d in m["tipuri"])
    alte = ", ".join(kw(x["slug"], x["nume"].lower() if x["slug"] not in ("pal-melaminat","mdf-vopsit") else x["nume"]) for x in MAT if x is not m)
    unde_links = f'Folosim {m["nume"].lower() if m["slug"] not in ("pal-melaminat","mdf-vopsit") else m["nume"]} la {kw("bucatarii-la-comanda","bucătării")}, {kw("dressinguri-la-comanda","dressinguri")}, {kw("dormitoare-la-comanda","dormitoare")}, {kw("living-la-comanda","living")}, {kw("mobila-baie-la-comanda","baie")} și {kw("mobila-birou-la-comanda","mobilier pentru firme")}, după caz.'
    body = f"""
<div class="hero hero-k"><div class="wrap">
  <p class="crumbs"><a href="index.html">Acasă</a> / <a href="materiale.html">Materiale</a> / {m["nume"]}</p>
  <span class="eyebrow pill" style="margin-top:14px">Materiale pentru mobilă</span>
  <h1>{m["nume"]}: <em>ce trebuie să știi</em></h1>
  <p class="lead" style="margin-top:12px">{m["scurt"]} Mai jos găsești avantajele, dezavantajele și unde se potrivește, ca să alegi în cunoștință de cauză.</p>
  <div class="cta-row">{call_btn()}<a class="btn ghost" href="index.html#oferta">Cere ofertă</a></div>
</div></div>
<section><div class="wrap"><div class="two">
  <div class="prose">
    <h2 style="margin-top:0">Ce este {m["nume"].lower() if m["slug"] not in ("pal-melaminat","mdf-vopsit") else m["nume"]}</h2>
    <p>{m["ce"]}</p>
    {tipuri}
    <div class="pm">
      <div class="pm-col pm-plus"><h3>Avantaje</h3><ul>{li(m["plus"])}</ul></div>
      <div class="pm-col pm-minus"><h3>De ținut cont</h3><ul>{li(m["minus"])}</ul></div>
    </div>
    <h2>Unde se potrivește</h2>
    <p>{m["unde"]} {unde_links}</p>
    <h2>Întreținere</h2>
    <p>{m["intretinere"]}</p>
    <h2>Compară cu alte materiale</h2>
    <p>Vezi și {alte}, sau toate {kw("materiale","materialele")} pe scurt. La măsurători îți aducem mostre și te ajutăm să alegi.</p>
  </div>
  {why_block()}
</div></div></section>
"""
    return page(f"{m['nume']} pentru mobilă la comandă: avantaje și dezavantaje | {C['nume']}",
                f"{m['nume']} pentru mobilă la comandă: ce este, avantaje, dezavantaje, unde se potrivește și cum se întreține. Măsurători gratuite, montaj inclus.",
                m["slug"] + ".html", body)


def variante(p):
    subs = [x for x in SUB if x["parinte"] == p["slug"]]
    if not subs: return ""
    return "<h2>Variante</h2>" + "".join(f'<div class="vrow"><b>{kw(x["slug"], x["titlu"])}</b><span>{x["scurt"]}</span></div>' for x in subs)

def sub_page(x):
    par = next(p for p in PRODUSE if p["slug"] == x["parinte"])
    frati = [y for y in SUB if y["parinte"] == x["parinte"] and y is not x]
    idei = "".join(f"<li>{i}</li>" for i in x["idei"])
    paras = "".join(f"<p>{t}</p>" for t in x["p"])
    mats = f'{kw("pal-melaminat","PAL melaminat")}, {kw("mdf-vopsit","MDF vopsit")}, {kw("lemn-masiv","lemn masiv")} sau {kw("furnir","furnir")}'
    orase = ", ".join(kw(oras_slug(o), o) for o in ORASE[:6])
    frati_txt = (" Vezi și " + ", ".join(kw(y["slug"], y["titlu"].lower()) for y in frati) + ".") if frati else ""
    body = f"""
<div class="hero hero-k"><div class="wrap">
  <p class="crumbs"><a href="index.html">Acasă</a> / <a href="{par["slug"]}.html">{par["titlu"]}</a> / {x["titlu"]}</p>
  <div class="hk" style="margin-top:14px">
    <div>
      <span class="eyebrow pill">Măsurători gratuite · Montaj inclus</span>
      <h1>{x["titlu"]}</h1>
      <p class="lead" style="margin-top:12px">{x["scurt"]} Parte din {kw(par["slug"], par["titlu"].lower())}, făcute pe centimetru, cu proiect 3D, transport și montaj incluse.</p>
      <div class="cta-row">{call_btn()}<a class="btn ghost" href="index.html#oferta">Cere ofertă</a></div>
    </div>
    <div class="hk-img">{art(x["art"])}</div>
  </div>
</div></div>
<section><div class="wrap"><div class="two">
  <div class="prose">
    <h2 style="margin-top:0">Cum o facem</h2>
    {paras}
    <h2>Ce putem face</h2>
    <ul class="ticks-l">{idei}</ul>
    <h2>Materiale</h2>
    <p>O facem din {mats}, cu {kw("feronerie-mobila","feronerie")} cu închidere lină. La măsurători îți arătăm mostre.</p>
    <h2>Unde lucrăm</h2>
    <p>În {orase} și în orașele din jur.</p>
    <h2>Mai multe idei</h2>
    <p>Vezi toate {kw(par["slug"], par["titlu"].lower())}.{frati_txt}</p>
  </div>
  {why_block()}
</div></div></section>
"""
    return page(f"{x['titlu']}: măsurători gratuite, montaj inclus | {C['nume']}",
                f"{x['titlu']} la comandă: {x['scurt'][0].lower() + x['scurt'][1:]} Măsurători gratuite, proiect 3D, transport și montaj incluse.",
                x["slug"] + ".html", body)

# ---------- scriere ----------
os.makedirs(OUT, exist_ok=True)
files = {"index.html": index(), "materiale.html": materiale_page()}
for p in PRODUSE: files[p["slug"] + ".html"] = produs_page(p)
for o in ORASE: files[oras_slug(o) + ".html"] = oras_page(o)
for m in MAT: files[m["slug"] + ".html"] = material_page(m)
for x in SUB: files[x["slug"] + ".html"] = sub_page(x)
for n, c in files.items():
    with open(os.path.join(OUT, n), "w", encoding="utf-8") as f: f.write(c)
shutil.copy(os.path.join(HERE, "style.css"), os.path.join(OUT, "style.css"))
shutil.copytree(os.path.join(HERE, "lucrari"), os.path.join(OUT, "lucrari"), dirs_exist_ok=True)
if C["domeniu"]:
    urls = "".join(f"  <url><loc>{C['domeniu']}/{'' if n == 'index.html' else n}</loc></url>\n" for n in files)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write("User-agent: *\nAllow: /\n" + (f"\nSitemap: {C['domeniu']}/sitemap.xml\n" if C["domeniu"] else ""))
with open(os.path.join(OUT, "favicon.svg"), "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6C27A"/><stop offset="1" stop-color="#D9822B"/></linearGradient></defs><rect width="48" height="48" rx="13" fill="#2B241F"/><path d="M13.5 33V15l10.5 10.5L34.5 15v18" fill="none" stroke="url(#a)" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M11 38.5h26" stroke="#F6C27A" stroke-opacity=".6" stroke-width="2.4" stroke-linecap="round"/></svg>')
print(len(files), "pagini")
