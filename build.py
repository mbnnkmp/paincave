"""Builds the PainCave Guide static site. Run: python3 build.py
Pages are written to docs/, which GitHub Pages serves. Settings (Amazon tag, site URL) are at the top.
import os, re, html
from datetime import date
from urllib.parse import quote_plus

AMAZON_TAG = "paincavetips-21"
# Public address of the site. Change this if you add a custom domain.
SITE_URL = "https://mbnnkmp.github.io/paincave/"
SITE = "PainCave Guide"
UPDATED = "2 November 2026"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


def amz(query, label="Check price on Amazon"):
    url = f"https://www.amazon.co.uk/s?k={quote_plus(query)}&tag={AMAZON_TAG}"
    return (f'<a class="btn btn-amz" href="{url}" target="_blank" '
            f'rel="sponsored nofollow noopener">{label}</a>')


def shop(url, label):
    """Non-Amazon retailer link. Swap url for your affiliate link (Awin, Impact etc.) when approved."""
    return (f'<a class="btn btn-alt" href="{url}" target="_blank" '
            f'rel="sponsored nofollow noopener">{label}</a>')


NAV = [
    ("index.html", "Start"),
    ("smart-bike-vs-turbo-trainer.html", "Bike vs trainer"),
    ("best-indoor-bikes-uk.html", "Best bikes"),
    ("rocker-plates.html", "Rocker plates"),
    ("indoor-cycling-apps.html", "Apps"),
    ("indoor-cycling-accessories.html", "Accessories"),
]

PHOTOS = {
    "pc-rider-window": ("Cyclist training on a road bike on a smart trainer at home beside a window and plants", "David Hellmann", "https://unsplash.com/photos/man-riding-on-gray-rigid-bicycle-near-window-jsZ4kncM0YE", "Unsplash"),
    "pc-road-bike-on-trainer": ("Rider in cycling kit on a road bike mounted to a direct-drive smart trainer", "gabbiistudios", "https://unsplash.com/photos/man-riding-road-bike-on-trainer-61vcI5fYLg8", "Unsplash"),
    "pc-trainer-closeup": ("Close-up of a road bike drivetrain on a direct-drive trainer", "gabbiistudios", "https://unsplash.com/photos/person-cycling-on-indoor-trainer-_JSz9C5B0Bg", "Unsplash"),
    "pc-exercise-bike-home": ("Spin-style exercise bike on a rug in a bright living room", "Abhishek Dutta", "https://unsplash.com/photos/a-stationary-bike-sits-on-a-rug-in-front-of-a-curtain-2pqPojBNq0Y", "Unsplash"),
    "pc-cockpit-tablet": ("Rider's view of a handlebar with a tablet showing a virtual cycling app", "Algi", "https://unsplash.com/photos/person-in-black-shorts-sitting-on-black-and-red-stationary-bike-dCXEbN6ubR4", "Unsplash"),
    "pc-setup-tablet-stand": ("Home pain cave with a road bike on a direct-drive smart trainer, a tablet stand and a track pump", "Flo Dahm", "https://www.pexels.com/photo/black-bike-on-a-bike-stand-10347812/", "Pexels"),
    "pc-setup-tv-app": ("Road bike on a wheel-on trainer facing a wall-mounted TV showing a virtual cycling app", "Flo Dahm", "https://www.pexels.com/photo/black-and-blue-bicycle-on-white-floor-tiles-4620527/", "Pexels"),
    "pc-rocker-diagram": ("Diagram of a rocker plate seen from behind: a trainer bolted to a top deck that tilts on a centre pivot, with air balls either side", None, None, "own"),
    "pc-wahoo-closeup": ("Close-up of a Wahoo smart trainer fitted to a Bianchi road bike", "Lee Ajaye", "https://unsplash.com/photos/a-close-up-of-a-bike-with-a-logo-on-it-sLShO-2RiVI", "Unsplash"),
    "pc-studio-screen": ("Indoor bike in front of a large glowing screen in a dark training studio", "Giorgio Trovato", "https://unsplash.com/photos/man-in-black-jacket-and-black-pants-riding-bicycle-2yQX9D54Eto", "Unsplash"),
}


def credit(who, url, src):
    if src == "own":
        return "Illustration: PainCave Guide"
    return f'Photo: <a href="{url}" target="_blank" rel="noopener">{who}</a> on {src}'


def fig(name, lead=False):
    alt, who, url, src = PHOTOS[name]
    load = 'fetchpriority="high"' if lead else 'loading="lazy"'
    return (f'<figure class="photo{" lead-photo" if lead else ""}">'
            f'<img src="img/{name}.jpg" srcset="img/{name}-sm.jpg 640w, img/{name}.jpg 1400w" '
            f'sizes="(max-width: 46rem) 100vw, 46rem" width="1400" height="933" alt="{alt}" {load} decoding="async">'
            f'<figcaption>{credit(who, url, src)}</figcaption></figure>')


def thumb(name):
    alt = PHOTOS[name][0]
    return f'<img class="card-img" src="img/{name}-sm.jpg" width="640" height="427" alt="" loading="lazy" decoding="async">'


ZONES = '<div class="zones" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>'

CSS = r"""
/* Layout: one 46rem reading column with full-width bands; a six-colour power-zone strip is the site's signature. */
:root{
  --bg:#f3f5f8; --surface:#ffffff; --ink:#14181f; --muted:#556070; --line:#dde2ea;
  --accent:#1f4fd1; --accent-ink:#ffffff; --amz:#f5b324; --amz-ink:#14181f;
  --good:#1d8a4e; --bad:#c2402a;
  --z1:#8a94a3; --z2:#2f7de1; --z3:#2fa35c; --z4:#e6b818; --z5:#ee7a1c; --z6:#d6382b;
  --display:"Saira Semi Condensed","Arial Narrow",sans-serif;
  --body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0f1218; --surface:#171b23; --ink:#e8ecf2; --muted:#9aa5b5; --line:#2a313d;
  --accent:#7ea2ff; --accent-ink:#0f1218; --amz:#f5b324; --amz-ink:#14181f;
  --good:#5cc98b; --bad:#f07a63; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0f1218; --surface:#171b23; --ink:#e8ecf2; --muted:#9aa5b5; --line:#2a313d;
  --accent:#7ea2ff; --accent-ink:#0f1218; --amz:#f5b324; --amz-ink:#14181f;
  --good:#5cc98b; --bad:#f07a63; color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:1rem/1.65 var(--body)}
a{color:var(--accent)}
a:focus-visible,.btn:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.wrap{max-width:46rem;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.wide{max-width:64rem}
header.site{border-bottom:1px solid var(--line);background:var(--surface)}
header.site .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem 1.25rem;padding-block:.8rem}
.logo{font:700 1.35rem/1 var(--display);letter-spacing:.02em;text-transform:uppercase;color:var(--ink);text-decoration:none;display:flex;align-items:center;gap:.5rem}
.logo .zones{width:2.2rem;height:.7rem}
nav.main{display:flex;flex-wrap:wrap;gap:.25rem .9rem;font-size:.9rem}
nav.main a{color:var(--muted);text-decoration:none}
nav.main a[aria-current]{color:var(--ink);font-weight:600}
.zones{display:flex;height:6px;gap:2px}
.zones i{flex:1;background:var(--z1)}
.zones i:nth-child(2){background:var(--z2)}.zones i:nth-child(3){background:var(--z3)}
.zones i:nth-child(4){background:var(--z4)}.zones i:nth-child(5){background:var(--z5)}.zones i:nth-child(6){background:var(--z6)}
.disclose{font-size:.82rem;color:var(--muted);border-left:3px solid var(--z4);padding:.4rem .8rem;margin:1.2rem 0;background:var(--surface)}
main{padding-block:1.5rem 3rem}
h1,h2,h3{font-family:var(--display);line-height:1.12;text-wrap:balance;margin:0}
h1{font-size:clamp(2.1rem,6vw,3.1rem);font-weight:700;letter-spacing:-.01em}
h2{font-size:1.7rem;font-weight:700;margin-top:2.6rem}
h3{font-size:1.3rem;font-weight:600}
p{margin:.8rem 0}
.lead{font-size:1.12rem;color:var(--muted);max-width:40rem}
.meta{font:500 .78rem/1.4 var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-top:.6rem}
.eyebrow{font:600 .75rem/1 var(--mono);text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}
.tablebox{overflow-x:auto;margin:1rem 0;border:1px solid var(--line);background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:.9rem;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--line);vertical-align:top}
th{font:600 .74rem/1.3 var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted);white-space:nowrap}
tr:last-child td{border-bottom:0}
.product{background:var(--surface);border:1px solid var(--line);padding:1.2rem;margin:1.4rem 0;display:grid;gap:.6rem}
.product header{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:.3rem 1rem}
.badge{font:600 .72rem/1 var(--mono);text-transform:uppercase;letter-spacing:.08em;padding:.35rem .5rem;border-left:4px solid var(--z2);background:var(--bg)}
.badge.z3{border-color:var(--z3)}.badge.z4{border-color:var(--z4)}.badge.z5{border-color:var(--z5)}.badge.z6{border-color:var(--z6)}.badge.z1{border-color:var(--z1)}
.price{font:600 .95rem var(--mono);font-variant-numeric:tabular-nums}
.specs{display:flex;flex-wrap:wrap;gap:.3rem 1rem;font:.82rem var(--mono);color:var(--muted);margin:0;padding:0;list-style:none}
.pc{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:.4rem 1.2rem}
.pc ul{margin:.2rem 0;padding-left:1.1rem;font-size:.93rem}
.pc h4{margin:0;font:600 .74rem var(--mono);text-transform:uppercase;letter-spacing:.08em}
.pc .pro h4{color:var(--good)}.pc .con h4{color:var(--bad)}
.ctas{display:flex;flex-wrap:wrap;gap:.5rem}
.btn{display:inline-block;padding:.55rem .9rem;font:600 .88rem var(--body);text-decoration:none;border-radius:3px}
.btn-amz{background:var(--amz);color:var(--amz-ink)}
.btn-alt{background:var(--accent);color:var(--accent-ink)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr));gap:1rem;margin:1.2rem 0}
.card{background:var(--surface);border:1px solid var(--line);padding:1.1rem;text-decoration:none;color:var(--ink);display:grid;gap:.4rem;align-content:start}
.card:hover{border-color:var(--accent)}
.card p{margin:0;color:var(--muted);font-size:.93rem}
.picks{display:grid;gap:0;border:1px solid var(--line);background:var(--surface);margin:1rem 0}
.picks div{display:grid;grid-template-columns:9rem 1fr;gap:.8rem;padding:.6rem .9rem;border-bottom:1px solid var(--line)}
.picks div:last-child{border-bottom:0}
.picks b{font:600 .74rem/1.6 var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
@media (max-width:30rem){.picks div{grid-template-columns:1fr;gap:.1rem}}
.note{background:var(--surface);border:1px solid var(--line);padding:.9rem 1rem;font-size:.93rem}
.hero{padding-block:1rem .5rem}
.photo{margin:1.4rem 0;display:grid;gap:.35rem}
.photo img{width:100%;max-width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;display:block;background:var(--line)}
.photo figcaption{font:.75rem/1.4 var(--mono);color:var(--muted)}
.photo figcaption a{color:var(--muted)}
.lead-photo{margin-top:.4rem}
.card{padding:0;overflow:hidden}
.card .card-img{width:100%;max-width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;display:block;background:var(--line)}
.card .card-body{padding:1rem 1.1rem 1.1rem;display:grid;gap:.4rem}
.hero .zones{height:10px;margin-bottom:1.4rem;max-width:20rem}
footer.site{border-top:1px solid var(--line);font-size:.85rem;color:var(--muted)}
footer.site .wrap{padding-block:1.4rem;display:grid;gap:.5rem}
footer.site a{color:var(--muted)}
ol.steps li,ul.tight li{margin:.3rem 0}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600'
         '&family=IBM+Plex+Sans:ital,wght@0,400;0,600;1,400&family=Saira+Semi+Condensed:wght@600;700&display=swap">')


def product(name, badge, zone, price, specs, verdict, pros, cons, ctas):
    spec_html = "".join(f"<li>{s}</li>" for s in specs)
    return f"""
<article class="product">
  <header><h3>{name}</h3><span class="badge {zone}">{badge}</span></header>
  <div class="price">{price}</div>
  <ul class="specs">{spec_html}</ul>
  <p>{verdict}</p>
  <div class="pc"><div class="pro"><h4>Pros</h4><ul>{''.join(f'<li>{p}</li>' for p in pros)}</ul></div>
  <div class="con"><h4>Cons</h4><ul>{''.join(f'<li>{c}</li>' for c in cons)}</ul></div></div>
  <div class="ctas">{''.join(ctas)}</div>
</article>"""


def table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tablebox"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def page(fname, title, desc, body, h1, lead, show_disclosure=True):
    nav = "".join(
        (f'<a href="{h}" aria-current="page">{t}</a>' if h == fname else f'<a href="{h}">{t}</a>') for h, t in NAV)
    disc = ('<p class="disclose">We earn a commission if you buy through links on this page, at no extra cost to you. '
            'As an Amazon Associate we earn from qualifying purchases. Prices are UK guide prices checked on '
            f'{UPDATED}; they change often, so check the retailer before you buy. '
            '<a href="disclosure.html">How we choose products</a>.</p>') if show_disclosure else ""
    inner = f"""<header class="site"><div class="wrap wide">
<a class="logo" href="index.html">{ZONES}{SITE}</a>
<nav class="main" aria-label="Main">{nav}</nav></div></header>
<main><div class="wrap">
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<p class="meta">Updated {UPDATED}</p>
{disc}
{body}
</div></main>
<footer class="site"><div class="wrap wide">
{ZONES}
<div>{SITE} is an independent UK guide to indoor cycling. <a href="disclosure.html">Affiliate disclosure</a></div>
<div>Amazon and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates.</div>
</div></footer>"""
    full = f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE_URL}{"" if fname == "index.html" else fname}">
{FONTS}
<style>{CSS}</style></head>
<body>{inner}</body></html>"""
    return full


PAGES = {}

# ---------------------------------------------------------------- HOME
PAGES["index.html"] = dict(
    title="PainCave Guide | Indoor cycling setups for UK riders",
    desc="Independent UK guide to smart bikes, turbo trainers, rocker plates, cycling apps and accessories for your home pain cave.",
    h1="Build a pain cave that you'll actually use",
    lead="Straight answers for UK riders setting up indoor training: which bike or trainer, which app, and which accessories make the difference between three rides and three hundred.",
    body=f"""
{fig("pc-rider-window", lead=True)}
<h2>Our quick picks for winter 2026</h2>
<div class="picks">
<div><b>Best value trainer</b><span>JetBlack Victory V2 (about £399): Wahoo Kickr Core 2 numbers for £100 less. <a href="best-indoor-bikes-uk.html#trainers">Read why</a></span></div>
<div><b>Safest all-rounder</b><span>Wahoo Kickr Core 2 (£499.99 RRP), widely stocked and works with every app.</span></div>
<div><b>Best value smart bike</b><span>Zwift Ride V2 with Kickr Core 2 (£1,099.99 RRP), now with adjustable cranks.</span></div>
<div><b>Best smart bike</b><span>Wahoo Kickr Bike Pro (£3,499.99), the only one that tilts on climbs.</span></div>
<div><b>Best free app</b><span>MyWhoosh: worlds, races and training plans with no subscription.</span></div>
<div><b>First accessory</b><span>A proper fan. Heat ends more sessions than legs do.</span></div>
</div>

<h2>Start here</h2>
<div class="cards">
<a class="card" href="smart-bike-vs-turbo-trainer.html">{thumb("pc-road-bike-on-trainer")}<div class="card-body"><span class="eyebrow">Decide</span><h3>Smart bike or turbo trainer?</h3><p>Costs, space, noise and wear compared, with a simple way to choose.</p></div></a>
<a class="card" href="best-indoor-bikes-uk.html">{thumb("pc-trainer-closeup")}<div class="card-body"><span class="eyebrow">Buy</span><h3>Best indoor bikes and trainers UK</h3><p>Twelve setups from £280 to £3,500, with UK prices and who each suits.</p></div></a>
<a class="card" href="rocker-plates.html">{thumb("pc-rocker-diagram")}<div class="card-body"><span class="eyebrow">Comfort</span><h3>Rocker plates and alternatives</h3><p>Why riders add movement, and cheaper ways to get most of the benefit.</p></div></a>
<a class="card" href="indoor-cycling-apps.html">{thumb("pc-setup-tv-app")}<div class="card-body"><span class="eyebrow">Ride</span><h3>Zwift, Rouvy, MyWhoosh and more</h3><p>What each app is good at and what it costs after Zwift bought Rouvy.</p></div></a>
<a class="card" href="indoor-cycling-accessories.html">{thumb("pc-setup-tablet-stand")}<div class="card-body"><span class="eyebrow">Kit</span><h3>Accessories that matter</h3><p>Fans, mats, sweat guards, laptop stands and the small parts people forget.</p></div></a>
</div>

<h2>The four decisions, in order</h2>
<ol class="steps">
<li><b>Where will it live?</b> A spare room, garage or living room changes everything: noise, heat and whether it can stay set up.</li>
<li><b>Bike or trainer?</b> If you already own a road bike and have under £600, a direct-drive trainer is the answer. <a href="smart-bike-vs-turbo-trainer.html">Full comparison</a>.</li>
<li><b>Which app?</b> Try MyWhoosh free first, then pay for Zwift, Rouvy or TrainerRoad if you want what they add.</li>
<li><b>Cooling, floor and screen.</b> Budget £100 to £200 for a fan, mat and stand. They decide whether you keep riding.</li>
</ol>
<p class="note">How we work: these guides are built from manufacturer specifications, UK retailer listings and independent tests by established cycling publications. Where we have ridden a product ourselves we say so in the review.</p>
""")

# ---------------------------------------------------------------- BIKE VS TRAINER
PAGES["smart-bike-vs-turbo-trainer.html"] = dict(
    title="Smart Bike vs Turbo Trainer: Pros, Cons and Costs (UK 2026)",
    desc="Should you buy a smart bike or a turbo trainer for your own bike? Prices, noise, space, wear and app compatibility compared for UK riders.",
    h1="Smart bike vs turbo trainer",
    lead="A smart trainer turns the bike you already own into an indoor bike. A smart bike is a dedicated indoor machine. Here is how to choose between them, and where exercise bikes such as Peloton fit.",
    body=f"""
{fig("pc-road-bike-on-trainer", lead=True)}
<h2>The short answer</h2>
<p>Buy a <b>direct-drive smart trainer</b> if you own a road or gravel bike, ride mostly on your own, and want the best ride for the money: good ones start around £400. Buy a <b>smart bike</b> if several people will share it, you want it permanently set up with zero fuss, or you want to stop wearing out your outdoor bike. Expect to pay at least £1,100.</p>

<h2>The four types of indoor bike</h2>
{table(["Type","How it works","UK price range","Best for"],[
["Wheel-on trainer","Your rear tyre presses on a roller","£150–£350","Trying indoor riding on a budget"],
["Direct-drive smart trainer","Rear wheel off; chain runs on the trainer's cassette","£280–£1,600","Most cyclists who own a bike"],
["Smart bike","Complete indoor bike with built-in resistance and virtual gears","£1,100–£3,500+","Shared households, set-and-forget"],
["Exercise / spin bike","Gym-style bike, often tied to a class app","£300–£2,500 plus subscription","Fitness classes rather than cycling"],
])}

<h2>Direct-drive smart trainer: pros and cons</h2>
<div class="pc"><div class="pro"><h4>Pros</h4><ul>
<li>Much cheaper: the Wahoo Kickr Core 2 is £499.99 and the JetBlack Victory V2 about £399</li>
<li>You ride your own bike, with your exact fit and contact points</li>
<li>Accurate power (±1–2%) and ERG mode for structured workouts</li>
<li>Works with every major app</li>
<li>Small enough to store in a cupboard or take to races for warm-ups</li>
</ul></div><div class="con"><h4>Cons</h4><ul>
<li>Wears your chain, cassette and frame; sweat is corrosive</li>
<li>Setup time each ride if the bike also goes outside</li>
<li>You may need a cassette (£40–£80) and thru-axle adapters</li>
<li>Different family members need saddle and bar changes</li>
<li>Carbon frames are fine on direct-drive trainers, but check your brand's guidance</li>
</ul></div></div>

<h2>Smart bike: pros and cons</h2>
<div class="pc"><div class="pro"><h4>Pros</h4><ul>
<li>Always ready: get on and ride in under a minute</li>
<li>Quick fit changes, so a household can share it</li>
<li>No wear on your outdoor bike</li>
<li>Virtual shifting that mimics Shimano, SRAM or Campagnolo</li>
<li>Often quieter and more stable than a bike on a trainer</li>
</ul></div><div class="con"><h4>Cons</h4><ul>
<li>Expensive: £1,099.99 for a Zwift Ride V2, £3,499.99 for a Kickr Bike Pro</li>
<li>Heavy (most weigh 40kg or more) and takes permanent floor space</li>
<li>Fit is close to your road bike, never identical</li>
<li>If it breaks, the whole bike goes back for repair</li>
<li>Some, like the Zwift Ride, work best with one app</li>
</ul></div></div>

<h2>What about Peloton-style exercise bikes?</h2>
{fig("pc-exercise-bike-home")}
<p>They are built for instructor-led classes, not for cycling training. They usually lock you into one app: Peloton's All-Access membership costs £45 a month, against £17.99 for Zwift. Most can't change resistance automatically from third-party apps, and few have a freewheel. If you think of yourself as a cyclist, a smart trainer or smart bike will suit you better. If you want classes and never ride outside, an exercise bike is a reasonable choice.</p>

<h2>Three-year cost of ownership</h2>
<p>Rough UK figures, using a Zwift subscription at £17.99 a month (about £648 over three years) for every option.</p>
{table(["Setup","Hardware","Extras over 3 years","Total"],[
["JetBlack Victory V2 + your bike","£399","£120 chain and cassette wear","about £1,170"],
["Wahoo Kickr Core 2 + your bike","£500","£120 chain and cassette wear","about £1,270"],
["Zwift Ride V2 (with Kickr Core 2)","£1,100","minimal wear parts","about £1,750"],
["Wattbike Proton (free Wattbike Hub app)","£1,795","none if you skip Zwift","£1,795 to £2,440"],
["Wahoo Kickr Bike Pro","£3,500","minimal","about £4,150"],
])}
<p>The trainer wins on cost unless you would otherwise buy a second bike just for indoor use. A used road bike dedicated to the trainer (£200–£400) plus a Kickr Core 2 still costs well under a Zwift Ride.</p>

<h2>Which should you choose?</h2>
<ul class="tight">
<li><b>You own one good bike and ride outdoors at weekends:</b> trainer, plus a cheap second-hand bike that stays on it.</li>
<li><b>Two or more people will ride it:</b> smart bike. The Wattbike Proton fits riders from 4ft 6in to 6ft 6in.</li>
<li><b>You only ride Zwift:</b> Zwift Ride V2 is the best-value smart bike.</li>
<li><b>You train seriously with structured plans:</b> a high-accuracy trainer such as the Kickr V6 or Elite Justo 2, or the Tacx Neo Bike Plus if budget allows.</li>
<li><b>You live in a flat:</b> any direct-drive trainer or smart bike plus a thick mat; avoid wheel-on trainers, which are noisier.</li>
</ul>
<p><a class="btn btn-alt" href="best-indoor-bikes-uk.html">See our ranked list of bikes and trainers</a></p>
""")

# ---------------------------------------------------------------- BEST BIKES
smart_bikes = [
    product("Zwift Ride V2 with Wahoo Kickr Core 2", "Best value smart bike", "z3",
            "£1,099.99 RRP · often discounted to £899–£990",
            ["1,800W max", "16% max gradient", "±2% power", "Cranks 160–175mm", "Riders 152–198cm"],
            "Zwift's smart frame sits on a Kickr Core 2 trainer, which does the measuring and resistance. The V2, launched in September 2026, added adjustable cranks, more saddle setback and a smaller frame at the same price. It is by far the cheapest way to get a smart bike, and since Zwift bought Rouvy the controls also work in Rouvy.",
            ["Half the price of most smart bikes", "Built-in Zwift controls and virtual shifting", "Light and easy to move", "The trainer can be used with a normal bike later"],
            ["Controls designed for Zwift; other apps need workarounds", "Button feel is not as good as dedicated shifters", "Max resistance and gradient lower than premium bikes"],
            [shop("https://uk.zwift.com/", "Check price at Zwift UK"), amz("Wahoo Kickr Core 2", "Kickr Core 2 on Amazon")]),
    product("Wattbike Proton", "Best for families", "z2",
            "£1,795 from Wattbike",
            ["1,800W max", "0–25% gradient", "Fixed 170mm cranks", "Riders 137–198cm", "48kg"],
            "The British-made Proton is designed to be shared. Its step-through frame and tool-free adjusters suit riders from 4ft 6in to 6ft 6in, and the free Wattbike Hub app includes hundreds of workouts and training plans without a subscription. It connects to Zwift and other apps over Bluetooth and ANT+.",
            ["Hundreds of free workouts", "Pedalling technique analysis", "Very wide fit range, step-through frame", "Strong UK support"],
            ["Noisier at high cadence", "Lower peak resistance than rivals", "Fixed crank length; supplied pedals have straps"],
            [shop("https://wattbike.com/gb/", "Check price at Wattbike")]),
    product("Wattbike Atom (Next Generation)", "Best for pedalling analysis", "z2",
            "Around £2,395 RRP",
            ["2,500W max", "±1% power", "Near-silent belt drive", "22 virtual gears"],
            "The Atom is the more serious Wattbike: higher resistance, tighter accuracy and an almost silent drive. Cyclingnews found it smooth and quiet, but noted resistance takes a few seconds to come back if you stop pedalling mid-workout in ERG mode.",
            ["Very quiet, good for flats", "Works with all major apps", "Huge range of bar height adjustment"],
            ["No on-bike gear display", "Slow to recover resistance after stopping in ERG", "Fixed crank length"],
            [shop("https://wattbike.com/gb/", "Check price at Wattbike"), amz("Wattbike Atom")]),
    product("Wahoo Kickr Bike Shift", "Best mid-price smart bike", "z4",
            "Seen from £1,795 at UK retailers · RRP higher",
            ["Electromagnetic resistance", "Adjustable cranks", "Programmable shifters", "Wi-Fi, Bluetooth, ANT+"],
            "The Shift drops the Kickr Bike Pro's tilting and keeps the things most riders use: quick fit adjustment, adjustable cranks, shifters that mimic Shimano, SRAM or Campagnolo, and tight integration with Wahoo's apps. It is also quieter than the Pro.",
            ["Quiet and smooth", "Fit can be matched to your road bike", "Adjustable cranks at this price"],
            ["No tilting", "No tablet holder", "Function over looks"],
            [amz("Wahoo Kickr Bike Shift")]),
    product("Wahoo Kickr Bike Pro", "Best smart bike overall", "z5",
            "£3,499.99 RRP",
            ["2,500W max", "Tilts −15% to +20%", "±1% power", "Adjustable cranks", "Wi-Fi + Race Mode"],
            "The only smart bike here that physically tilts up for climbs and down for descents. Wahoo's 2025 update added redesigned shifters with steering buttons, a Fizik saddle and Wi-Fi with Race Mode for faster data. Cyclingnews rates it the best smart bike overall.",
            ["Most realistic climbing", "Copies the gearing of any major groupset", "Excellent fit adjustment"],
            ["Very expensive", "Heavy and hard to move", "No side-to-side movement"],
            [amz("Wahoo Kickr Bike Pro")]),
    product("Tacx Neo Bike Plus", "Best for training and racing", "z6",
            "Premium price · check Garmin UK",
            ["2,200W max", "25% max gradient", "±1% power", "Cranks 165–175mm", "Works without mains power"],
            "Garmin's smart bike simulates a 125kg flywheel, so sprints and surges feel very real. Built-in fans, a gear display, two USB ports and a tablet holder are included, and it can run off your own pedalling if it's not plugged in.",
            ["Built-in fans and display", "Dual-sided power and pedal analysis", "Low step-through frame"],
            ["Some assembly needed", "Limited crank adjustment steps", "Premium price"],
            [shop("https://www.garmin.com/en-GB/", "Check price at Garmin UK"), amz("Tacx Neo Bike Plus")]),
]

trainers = [
    product("Van Rysel D100 with Zwift Cog and Click", "Best budget", "z1",
            "£279.99 at Decathlon",
            ["600W max", "6% gradient", "±5% power", "10.5kg"],
            "The cheapest sensible direct-drive trainer. Fine for steady endurance rides and easy intervals, but the 600W ceiling and 6% gradient limit sprinting, steep virtual climbs and racing.",
            ["Very low price", "Folding legs, easy to store", "Zwift Cog fits most bikes"],
            ["600W limit", "Less accurate power", "No built-in cadence"],
            [shop("https://www.decathlon.co.uk/p/d100-home-trainer-with-zwift-cog-and-click/355194/m8883242", "Check price at Decathlon")]),
    product("JetBlack Victory V2 with Zwift Cog and Click", "Best value", "z3",
            "£399",
            ["1,800W max", "16% gradient", "±2% power", "Wi-Fi"],
            "BikeRadar's best overall smart trainer. On paper it matches the Kickr Core 2 for £100 less, and testers found the power data and ride feel convincing. One quirk: power smoothing is always on, so your graphs look tidier than your effort.",
            ["Kickr Core 2 performance for less", "Wi-Fi built in", "Comes with Cog and Click"],
            ["Smoothing can't be turned off", "Smaller UK support network than Wahoo"],
            [shop("https://www.jetblackcycling.co.uk/indoor-cycle-trainers-and-accessories/victory-smart-trainer/", "Check price at JetBlack"), amz("JetBlack Victory smart trainer")]),
    product("Wahoo Kickr Core 2", "Best all-rounder", "z2",
            "£499.99 RRP · deals from about £400",
            ["1,800W max", "16% gradient", "±2% power", "Wi-Fi + Race Mode", "5.4kg flywheel"],
            "The default recommendation for most riders. It's widely stocked, works with every app, and testers at Cyclingnews and BikeRadar found its power credible and ride feel polished. Available with an 11-speed cassette or Zwift Cog and Click.",
            ["Proven and widely supported", "Wi-Fi and automatic calibration", "Frequent discounts"],
            ["Awkward to carry", "Costs more than the Victory for similar numbers"],
            [amz("Wahoo Kickr Core 2"), shop("https://uk.wahoofitness.com/devices/indoor-cycling/bike-trainers/kickr-buy", "Check price at Wahoo")]),
    product("Wahoo Kickr V6", "Best for racing", "z5",
            "£774.99 with 11-speed cassette",
            ["2,200W max", "20% gradient", "±1% power", "Axis feet movement"],
            "The step up for riders who race on Zwift or do lots of threshold work. Tighter accuracy, a higher ceiling and some side-to-side movement through its feet.",
            ["±1% accuracy", "Some built-in movement", "Fast, reliable data"],
            ["Big jump in price over the Core 2", "Heavy"],
            [amz("Wahoo Kickr V6 smart trainer")]),
    product("Elite Justo 2", "Best for data", "z4",
            "£1,099.99 with 12-speed cassette",
            ["2,300W max", "24% gradient", "<1% power", "Ethernet + Wi-Fi", "Flex Feet"],
            "A specialist trainer for people who train indoors a lot. Swappable Flex Feet let you choose how much it moves, and a wired Ethernet option removes dropouts.",
            ["Excellent accuracy", "Adjustable movement", "Wired connection option"],
            ["Expensive", "Awkward carry handle"],
            [amz("Elite Justo 2 smart trainer")]),
    product("Tacx Neo 3M", "Best road feel", "z6",
            "£1,599.99 from Garmin",
            ["2,200W max", "25% gradient", "Within 1% power", "Multidirectional movement", "Road surface simulation"],
            "The Neo 3M simulates cobbles and gravel and moves in several directions. BikeRadar praised its accuracy and ERG behaviour but questioned the price, and most riders won't feel enough extra to justify it.",
            ["Superb resistance control", "Built-in movement", "Very quiet"],
            ["Very expensive", "Movement not always better when sprinting", "Check derailleur clearance"],
            [shop("https://www.garmin.com/en-GB/p/885302/", "Check price at Garmin UK"), amz("Tacx Neo 3M")]),
]

PAGES["best-indoor-bikes-uk.html"] = dict(
    title="Best Indoor Bikes and Smart Trainers UK (2026)",
    desc="The best smart bikes and direct-drive turbo trainers in the UK for 2026, from £280 to £3,500, with UK prices, specs, pros and cons.",
    h1="Best indoor bikes and smart trainers in the UK",
    lead="Six smart bikes and six turbo trainers, ranked by who they suit. Prices are UK guide prices from manufacturers and UK retailers at the end of October 2026.",
    body=f"""
{fig("pc-trainer-closeup", lead=True)}
<p class="note">Not sure which type you need? Read <a href="smart-bike-vs-turbo-trainer.html">smart bike vs turbo trainer</a> first.</p>
<h2>At a glance</h2>
{table(["Model","Type","UK price","Max power","Gradient","Accuracy"],[
["Van Rysel D100","Trainer","£279.99","600W","6%","±5%"],
["JetBlack Victory V2","Trainer","£399","1,800W","16%","±2%"],
["Wahoo Kickr Core 2","Trainer","£499.99","1,800W","16%","±2%"],
["Wahoo Kickr V6","Trainer","£774.99","2,200W","20%","±1%"],
["Elite Justo 2","Trainer","£1,099.99","2,300W","24%","&lt;1%"],
["Zwift Ride V2 + Core 2","Smart bike","£1,099.99","1,800W","16%","±2%"],
["Tacx Neo 3M","Trainer","£1,599.99","2,200W","25%","within 1%"],
["Wattbike Proton","Smart bike","£1,795","1,800W","25%","n/k"],
["Wattbike Atom","Smart bike","~£2,395","2,500W","n/k","±1%"],
["Wahoo Kickr Bike Pro","Smart bike","£3,499.99","2,500W","+20% / −15%","±1%"],
])}
<p class="meta">n/k = not published by the maker in the sources we checked</p>

<h2 id="smart-bikes">Best smart bikes</h2>
{fig("pc-studio-screen")}
{''.join(smart_bikes)}

<h2 id="trainers">Best direct-drive smart trainers</h2>
{fig("pc-wahoo-closeup")}
<p>Every trainer below is direct drive: you remove the rear wheel and fit the bike to the trainer. Check your axle (quick release, 12×142mm or 12×148mm Boost) and cassette before ordering.</p>
{''.join(trainers)}

<h2>How to choose</h2>
<ul class="tight">
<li><b>Compatibility first:</b> axle standard, freehub (Shimano HG, SRAM XDR, Campagnolo) and whether you want a cassette or Zwift Cog.</li>
<li><b>App:</b> Zwift Cog and Click virtual shifting works fully in Zwift and now in Rouvy; check others before buying.</li>
<li><b>Accuracy:</b> ±2% is fine for most people. Repeatability matters more than the headline number.</li>
<li><b>Noise:</b> all direct-drive trainers are quieter than wheel-on ones; your chain and fan will be the loudest parts.</li>
<li><b>Budget for extras:</b> a fan, mat and sweat cover add £80–£200. See <a href="indoor-cycling-accessories.html">accessories</a>.</li>
</ul>
<h2>Sources</h2>
<p class="meta">Specs and prices from manufacturers and UK retailers; independent test findings from <a href="https://www.cyclingnews.com/features/best-smart-bikes/" rel="nofollow noopener" target="_blank">Cyclingnews</a>, <a href="https://procyclinguk.com/best-smart-turbo-trainers-uk-2026/" rel="nofollow noopener" target="_blank">ProCyclingUK</a> and <a href="https://bikeradar.com/advice/buyers-guides/best-smart-trainer" rel="nofollow noopener" target="_blank">BikeRadar</a>.</p>
""")

# ---------------------------------------------------------------- ROCKER PLATES
plates = [
    product("KOM Cycling Rocker Plate", "Best budget plate", "z3",
            "Budget · check Amazon",
            ["Side-to-side", "Adjustable contact points", "Fits most trainers"],
            "A simple side-to-side plate that suits most direct-drive trainers. It's the one most readers can buy from Amazon with quick delivery.",
            ["Affordable", "Easy setup", "Broad compatibility"],
            ["No fore-aft motion", "Less refined than UK-made plates"],
            [amz("KOM Cycling rocker plate")]),
    product("Turborocks Realplate React", "Best full-motion plate", "z5",
            "Roughly £349–£579 depending on model",
            ["Side-to-side", "Fore-aft (React)", "UK made"],
            "Often rated the best full-motion plate available. The React version adds fore-aft movement, which takes the jolt out of each pedal stroke; the standard Realplate is cheaper and side-to-side only.",
            ["Full motion", "Very well made", "UK maker and support"],
            ["Expensive", "Takes floor space and lifts the bike"],
            []),
    product("Omnirocker", "UK alternative", "z2",
            "Roughly £379–£579",
            ["Side-to-side", "Fore-aft options", "UK made"],
            "Another British-made plate with full-motion options. Worth comparing with Turborocks on lead time and the specific trainer you use.",
            ["Full motion options", "UK made"],
            ["Premium price", "Sold direct, not on Amazon"],
            []),
    product("Saris MP1 Nfinity platform", "Most natural motion", "z6",
            "Premium · check Amazon",
            ["Side-to-side", "Fore-aft", "Large platform"],
            "A big platform with natural fore-aft and lateral movement. Very expensive and large, but the closest a plate gets to riding on the road.",
            ["Very natural feel", "Room for the rider to stand"],
            ["Very expensive", "Huge footprint"],
            [amz("Saris MP1 Nfinity")]),
    product("Rocker feet adapters (tennis-ball type)", "Cheapest way in", "z1",
            "Usually under £40",
            ["About 10° side-to-side", "Fits trainer legs"],
            "Cups that slip under your trainer's legs, often with tennis or rubber balls. They add a little lateral sway for very little money. Check they fit your trainer's legs before ordering.",
            ["Very cheap", "No extra floor space"],
            ["Small movement only", "Can feel vague when sprinting", "Fit varies by trainer"],
            [amz("indoor cycling rocker feet trainer")]),
]

PAGES["rocker-plates.html"] = dict(
    title="Best Rocker Plates UK and Cheaper Alternatives (2026)",
    desc="Do you need a rocker plate for your turbo trainer? The best rocker plates in the UK, plus rocker feet, trainers with built-in movement and rollers.",
    h1="Rocker plates and the alternatives",
    lead="A rocker plate lets your bike and trainer sway as you pedal. Riders say it makes long sessions more comfortable. Here's whether you need one, the best options, and cheaper ways to add movement.",
    body=f"""
{fig("pc-rocker-diagram", lead=True)}
<h2>What a rocker plate does</h2>
<p>Outdoors, your bike moves under you. On a fixed trainer it can't, so your body absorbs every pedal stroke at the saddle, hands and lower back. A rocker plate sits under the trainer and lets it tilt side to side; full-motion plates also slide forwards and back.</p>
<div class="pc"><div class="pro"><h4>Pros</h4><ul>
<li>Less saddle pressure and numbness on long rides</li>
<li>More natural feel when standing to climb or sprint</li>
<li>Less stress on your frame</li>
<li>Many riders find it reduces back and shoulder ache</li>
</ul></div><div class="con"><h4>Cons</h4><ul>
<li>Costs £150–£600 on top of your trainer</li>
<li>Raises the bike, so you need a step and more ceiling height</li>
<li>Takes up more floor space</li>
<li>Can feel strange at first and some riders never like it</li>
</ul></div></div>

<h2>Do you need one?</h2>
<p>Probably not if you ride under an hour at a time. Consider one if you ride indoors for two hours or more, get saddle sores indoors but not outside, or race and sprint on Zwift. Try cheaper fixes first: a better saddle position, standing every 10 minutes, and good cooling.</p>

<h2>Best rocker plates</h2>
{''.join(plates)}

<h2>Alternatives to a rocker plate</h2>
{table(["Option","What you get","Rough cost","Best for"],[
["Rocker feet adapters","A little side-to-side sway","Under £40","Trying the idea cheaply"],
["Trainer with movement feet","Kickr V6 Axis feet, Elite Justo 2 Flex Feet","Included","Buying a new trainer anyway"],
["Wahoo Kickr Move","Built-in fore-aft and side-to-side motion","Premium","Movement without a plate"],
["Tacx Neo 3M","Multidirectional movement built in","£1,599.99","Premium all-in-one"],
["Smart rollers (e.g. Wahoo Kickr Rollr)","Your bike moves freely","Mid to premium","Balance and smooth pedalling"],
["DIY plate","Plywood and inflatable balls or bearings","£50–£100","Confident DIYers"],
])}
<div class="ctas">{amz("Wahoo Kickr Move")}{amz("Wahoo Kickr Axis feet","Kickr Axis feet on Amazon")}{amz("Elite smart rollers","Rollers on Amazon")}</div>
<p class="note">Safety: on any plate, make sure the trainer is bolted or strapped down and the plate sits on a flat, non-slip mat. Check your trainer maker's warranty terms before fitting one.</p>
""")

# ---------------------------------------------------------------- APPS
apps = [
    ("Zwift", "Best overall", "z5", "£17.99/month",
     "The biggest community, the busiest group rides and the best-organised racing. Virtual worlds are game-like, and structured workouts and plans are built in. Zwift bought Rouvy in April 2026, but both apps still run separately with separate subscriptions.",
     ["Always someone to ride with", "Best racing scene", "Works with Zwift Ride and Cog and Click"],
     ["Price has risen over the years", "Training analysis less deep than TrainerRoad"],
     "https://www.zwift.com/uk"),
    ("Rouvy", "Best real-world routes", "z3", "Around £17.99/month · group plans available",
     "Ride filmed real-world roads with augmented-reality riders on screen, from Alpine climbs to Ironman courses. Rouvy now also owns FulGaz's route videos and Bkool. A group account lets up to five riders share one subscription, and Zwift hardware now works in Rouvy.",
     ["Real roads and famous climbs", "Group account for families", "Good for previewing races"],
     ["Fewer riders around you than Zwift", "Video quality depends on your connection"],
     "https://rouvy.com/"),
    ("MyWhoosh", "Best free app", "z2", "Free",
     "Virtual worlds, workouts, training plans and races with no subscription. It hosts the UCI Cycling Esports World Championships through 2026. Graphics are good; the community is smaller than Zwift's.",
     ["Completely free", "Proper training plans", "Prize races"],
     ["Quieter roads", "Some users report bugs after updates"],
     "https://www.mywhoosh.com/"),
    ("TrainerRoad", "Best for getting faster", "z6", "Around £/$20/month",
     "No virtual world: just power graphs and very well designed training plans that adapt to how your sessions go. Popular with time triallists and racers who want results rather than entertainment.",
     ["Best adaptive training plans", "Plans work outdoors too", "Excellent analysis"],
     ["Little entertainment", "Among the priciest apps"],
     "https://www.trainerroad.com/"),
    ("Wahoo SYSTM", "Best all-round training", "z4", "Check current price",
     "Wahoo's training app, built from The Sufferfest, combines structured workouts with yoga, strength and mental training, and uses a four-number fitness profile rather than just FTP.",
     ["Strength and yoga included", "Detailed fitness test", "Entertaining video workouts"],
     ["No open-world riding", "Smaller community"],
     "https://www.wahoofitness.com/"),
    ("TrainingPeaks Virtual", "Best if you use TrainingPeaks", "z1", "Included with TrainingPeaks Premium",
     "The former IndieVelo, now part of TrainingPeaks. A clean virtual world with racing and group rides, included in a Premium plan rather than sold separately.",
     ["No extra cost for Premium users", "Coach-friendly", "Improving quickly"],
     ["Fewer routes", "Rough edges"],
     "https://www.trainingpeaks.com/"),
]
app_html = "".join(
    product(n, b, z, p, [], v, pr, co, [shop(u, f"Visit {n}")]).replace('<ul class="specs"></ul>', "")
    for n, b, z, p, v, pr, co, u in apps)

PAGES["indoor-cycling-apps.html"] = dict(
    title="Best Indoor Cycling Apps UK: Zwift, Rouvy, MyWhoosh and More (2026)",
    desc="Zwift vs Rouvy vs MyWhoosh vs TrainerRoad: prices, pros and cons of the best indoor cycling apps for UK riders in 2026.",
    h1="The best indoor cycling apps",
    lead="Your app matters as much as your trainer: it decides whether indoor riding feels like a game, a real road or a training lab. Here's what each one does well and what it costs in the UK.",
    body=f"""
{fig("pc-setup-tv-app", lead=True)}
<h2>Which app suits you?</h2>
{table(["You want","Choose"],[
["Racing and riding with others","Zwift, or MyWhoosh for free"],
["Real roads and famous climbs","Rouvy"],
["A plan that makes you faster","TrainerRoad"],
["Training plus strength and yoga","Wahoo SYSTM"],
["To pay nothing","MyWhoosh"],
["One subscription for a family","Rouvy group account"],
["Classes with an instructor","Peloton (closed ecosystem, £45/month All-Access)"],
])}
<p class="note">News: Zwift bought Rouvy on 29 April 2026. Both apps continue independently, and Zwift Ready trainers and the Zwift Ride now work in Rouvy. If you're choosing between them, decide on riding style, not price.</p>

<h2>The apps reviewed</h2>
{fig("pc-cockpit-tablet")}
{app_html}

<h2>Other apps worth knowing</h2>
<ul class="tight">
<li><b>FulGaz:</b> high-definition real-world routes, now owned by Rouvy.</li>
<li><b>Kinomap:</b> large library of user-filmed videos, also for rowing and running.</li>
<li><b>Wattbike Hub:</b> free with Wattbike bikes, with hundreds of workouts.</li>
<li><b>TrainerDay:</b> a free or low-cost workout library and builder.</li>
</ul>
<p>Every app here syncs your rides to Strava. Most offer a free trial: ride two apps for a week each before you commit.</p>
<p class="meta">Subscription prices change often and vary by plan; check each app's site. Sources include <a href="https://www.cyclingnews.com/features/best-smart-bikes/" rel="nofollow noopener" target="_blank">Cyclingnews</a> and <a href="https://bicycleretailer.com/industry-news/2026/04/29/zwift-acquires-fellow-indoor-platform-rouvy" rel="nofollow noopener" target="_blank">Bicycle Retailer</a>.</p>
""")

# ---------------------------------------------------------------- ACCESSORIES
def acc(name, why, picks):
    items = "".join(f"<li>{p_name} {amz(q)}</li>" for p_name, q in picks)
    return f'<article class="product"><header><h3>{name}</h3></header><p>{why}</p><ul class="tight acc">{items}</ul></article>'

PAGES["indoor-cycling-accessories.html"] = dict(
    title="Best Indoor Cycling Accessories UK (2026)",
    desc="The indoor cycling accessories that matter: fans, trainer mats, sweat guards, laptop stands, heart rate monitors and more, with Amazon UK links.",
    h1="Indoor cycling accessories that matter",
    lead="In order of importance. A fan and a mat will improve your sessions more than an expensive trainer upgrade.",
    body=f"""
{fig("pc-setup-tablet-stand", lead=True)}
<style>.acc li{{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.4rem 1rem;padding:.4rem 0;border-bottom:1px solid var(--line);list-style:none}}.acc{{padding:0}}.acc li:last-child{{border-bottom:0}}</style>
{acc("1. A powerful fan", "Indoors there's no airflow, so your core temperature climbs fast and power drops. Point one strong fan at your face and chest; add a second from the side for hard sessions.", [
 ("<b>Wahoo Kickr Headwind</b> · smart fan that speeds up with your heart rate or speed", "Wahoo Kickr Headwind"),
 ("<b>Vornado air circulator</b> · strong, focused airflow, quiet", "Vornado 660 air circulator"),
 ("<b>High-velocity floor fan</b> · best airflow for the money", "high velocity floor fan 20 inch"),
])}
{acc("2. Trainer mat", "Protects the floor from sweat, stops the trainer creeping and cuts vibration noise, which matters in flats. Look for at least 6mm thick and 180cm long.", [
 ("<b>Tacx trainer mat</b> · foldable, grippy", "Tacx trainer mat"),
 ("<b>Wahoo or Elite trainer mat</b> · fits under most trainers", "Elite turbo trainer mat"),
 ("<b>Thick gym floor mat</b> · cheaper, for garages and concrete", "thick exercise equipment mat 6mm"),
])}
{acc("3. Sweat guard and towels", "Sweat corrodes headsets, bolts and frames. A sweat net between your bars and saddle catches most of it.", [
 ("<b>Tacx sweat cover</b> · with phone pocket", "Tacx sweat cover"),
 ("<b>Universal bike sweat guard</b> · budget option", "turbo trainer sweat guard bike"),
 ("<b>Microfibre gym towels</b> · one for the bars, one for you", "microfibre gym towel pack"),
])}
{acc("4. Laptop, tablet or TV setup", "You'll stare at the screen for hours, so put it at eye level and within reach. A standing desk on wheels doubles as a work desk.", [
 ("<b>Wahoo Kickr Desk</b> · height-adjustable, made for trainers", "Wahoo Kickr Desk"),
 ("<b>Mobile laptop stand on wheels</b> · cheaper alternative", "mobile laptop stand adjustable height wheels"),
 ("<b>Handlebar tablet mount</b> · for iPad or phone", "bike handlebar tablet holder"),
])}
{acc("5. Heart rate monitor", "Essential for training zones and for smart fans that follow your heart rate. Chest straps are more accurate than wrist sensors.", [
 ("<b>Garmin HRM-Dual</b> · Bluetooth and ANT+", "Garmin HRM-Dual"),
 ("<b>Wahoo Tickr</b> · reliable, simple", "Wahoo Tickr heart rate monitor"),
])}
{acc("6. Front wheel riser block", "Levels your bike on the trainer and stops the front wheel rolling. Cheap and easy to forget.", [
 ("<b>Front wheel riser block</b>", "front wheel riser block turbo trainer"),
])}
{acc("7. Cadence sensor", "Some trainers don't measure cadence. A small sensor on the crank fixes that.", [
 ("<b>Wahoo RPM or Garmin cadence sensor</b>", "bike cadence sensor bluetooth ANT+"),
])}
{acc("8. Comfort extras", "Small things for long sessions.", [
 ("<b>Chamois cream</b> · indoor rides cause more chafing", "chamois cream cycling"),
 ("<b>Large bottles</b> · you'll drink 750ml an hour or more", "cycling water bottle 750ml"),
 ("<b>Wireless earbuds</b> · for music and Zwift chat", "sport wireless earbuds sweat resistant"),
 ("<b>Dehumidifier</b> · stops a garage or spare room from getting damp", "dehumidifier 12l"),
])}
<p class="note">Amazon links above go to search results so you can compare current sellers and prices. Check that a mat or riser block fits your specific trainer before ordering.</p>
""")

# ---------------------------------------------------------------- DISCLOSURE
CREDITS = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{w}</a> on {src}: {a}</li>' for a, w, u, src in PHOTOS.values() if src != "own")

PAGES["disclosure.html"] = dict(
    title="Affiliate Disclosure | PainCave Guide",
    desc="How PainCave Guide makes money and how we choose products.",
    h1="Affiliate disclosure",
    lead="How this site is funded and how we choose what to recommend.",
    show_disclosure=False,
    body="""
<p>PainCave Guide is reader-supported. When you buy through some links on this site we may earn a commission, at no extra cost to you. As an Amazon Associate we earn from qualifying purchases. We may also earn from other retailers and brands.</p>
<p>Commission never decides what we recommend. Our guides are based on manufacturer specifications, UK retailer listings and independent tests by established cycling publications, which we link to. Where we have tested a product ourselves we say so.</p>
<p>Prices are guides checked on the date shown on each page. They change often, especially in November and January, so always check the retailer before you buy.</p>
<h2>Photo credits</h2>
<p>Photos are from <a href="https://unsplash.com/license" target="_blank" rel="noopener">Unsplash</a> and <a href="https://www.pexels.com/license/" target="_blank" rel="noopener">Pexels</a> and used under their licences, which allow free commercial use. Diagrams are our own. We credit each photographer:</p>
<ul class="tight">""" + CREDITS + """</ul>
""")


def build():
    os.makedirs(OUT, exist_ok=True)
    for fname, p in PAGES.items():
        doc = page(fname, p["title"], p["desc"], p["body"], p["h1"], p["lead"], p.get("show_disclosure", True))
        with open(os.path.join(OUT, fname), "w") as f:
            f.write(doc)
    urls = "".join(
        f"<url><loc>{SITE_URL}{'' if f == 'index.html' else f}</loc><lastmod>{date.today().isoformat()}</lastmod></url>"
        for f in PAGES)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                 + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        fh.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print("built", len(PAGES), "pages to", OUT)


if __name__ == "__main__":
    build()
