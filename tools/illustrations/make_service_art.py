"""Draws the service illustrations in static/img/services/ (in-house artwork).

Run it again after changing a drawing:  python tools/illustrations/make_service_art.py
Each file is named after the service icon chosen in the admin.
"""
import os
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "static", "img", "services")
G, N, C, R, ND = "#006400", "#303360", "#FE7146", "#FF0000", "#1F2245"
GT, CT, NT = "#e8f3e8", "#fff1ec", "#eceef7"
SKIN = ["#8d5524", "#6b3e1f", "#a0662f", "#5a3418"]

def head(title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title>'
            '<!-- Drawn in-house for WS Market Research. Free to use and edit on this site. -->'
            '<defs><filter id="s" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#1f2245" flood-opacity=".16"/></filter></defs>')

def bg(color=NT):
    return (f'<rect width="400" height="260" rx="18" fill="{color}"/>'
            f'<circle cx="330" cy="40" r="70" fill="#fff" opacity=".45"/>'
            f'<circle cx="60" cy="230" r="60" fill="#fff" opacity=".35"/>')

def person(x, y, s=1.0, skin=0, shirt=G, hair=ND):
    # x,y = centre of head; s = scale
    r = 13 * s
    return (f'<path d="M{x-24*s} {y+52*s} a{24*s} {26*s} 0 0 1 {48*s} 0 v{6*s} h{-48*s}z" fill="{shirt}"/>'
            f'<rect x="{x-5*s}" y="{y+10*s}" width="{10*s}" height="{10*s}" fill="{SKIN[skin]}"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SKIN[skin]}"/>'
            f'<path d="M{x-r} {y-1*s} a{r} {r} 0 0 1 {2*r} 0 a{r} {r*0.55} 0 0 0 {-2*r} 0z" fill="{hair}"/>')

def card(x, y, w, h, fill="#fff", rx=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" filter="url(#s)"/>'

def line(x, y, w, op=.8, h=7, c=N):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{c}" opacity="{op}"/>'

def pin(x, y, c=C, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 40c0 0-22-20-22-36a22 22 0 0 1 44 0c0 16-22 36-22 36z" fill="{c}" filter="url(#s)"/>'
            f'<circle cx="0" cy="4" r="8" fill="#fff"/></g>')

def check(x, y, c=G, s=1):
    return f'<path d="M{x} {y}l{5*s} {5*s} {10*s}-{11*s}" fill="none" stroke="{c}" stroke-width="{3.5*s}" stroke-linecap="round" stroke-linejoin="round"/>'

def bubble(x, y, w, h, fill="#fff", tail="left"):
    tx = x + 18 if tail == "left" else x + w - 18
    d = -1 if tail == "left" else 1
    return (f'<g filter="url(#s)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}"/>'
            f'<path d="M{tx} {y+h-1}l{8*d} 14 4-14z" fill="{fill}"/></g>')

svgs = {}

# 1 Market entry: plane route to a storefront with a pin
svgs["compass"] = head("Illustration: a route from abroad to a new shop in Cameroon, marked with a location pin") + bg(CT) + \
    '<path d="M40 70 C 120 30, 170 140, 250 110" fill="none" stroke="#303360" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round" opacity=".6"/>' + \
    f'<g transform="translate(22 52) rotate(-15)"><path d="M0 14 L40 8 L52 0 L58 3 L50 12 L70 16 L66 22 L48 20 L38 34 L30 34 L36 20 L8 22z" fill="{N}"/></g>' + \
    card(190, 120, 170, 115) + \
    f'<rect x="190" y="120" width="170" height="30" rx="12" fill="{G}"/><rect x="190" y="135" width="170" height="15" fill="{G}"/>' + \
    ''.join(f'<path d="M{190+i*17} 150h17l-2 14a7 7 0 0 1-13 0z" fill="{C if i%2==0 else "#fff"}"/>' for i in range(10)) + \
    f'<rect x="205" y="178" width="40" height="57" rx="4" fill="{NT}"/><rect x="258" y="176" width="86" height="36" rx="4" fill="{NT}"/>' + \
    line(268, 186, 50, .5) + line(268, 198, 34, .3) + f'<circle cx="238" cy="208" r="3" fill="{N}"/>' + \
    f'<text x="275" y="141" text-anchor="middle" font-family="system-ui,sans-serif" font-size="15" font-weight="700" fill="#fff">OPEN</text>' + \
    pin(300, 40, C) + \
    card(40, 150, 120, 80) + line(54, 166, 70) + line(54, 180, 46, .35) + \
    ''.join(f'<rect x="{56+i*22}" y="{214-hh}" width="14" height="{hh}" rx="3" fill="{G}" opacity="{.4+i*.2}"/>' for i, hh in enumerate([12, 20, 28, 36])) + \
    '</svg>'

# 2 Marketing research: target with arrow + customer segments
svgs["target"] = head("Illustration: a target hit by an arrow, with three customer groups and their opinions") + bg(GT) + \
    f'<circle cx="290" cy="130" r="80" fill="#fff" filter="url(#s)"/><circle cx="290" cy="130" r="60" fill="{CT}"/><circle cx="290" cy="130" r="40" fill="#fff"/><circle cx="290" cy="130" r="20" fill="{C}"/>' + \
    f'<path d="M370 50 L294 126" stroke="{N}" stroke-width="5" stroke-linecap="round"/><path d="M370 50l-4 16 12-4 4-12-12 0z" fill="{N}"/><path d="M362 46l10-10M376 60l10-10M368 52l12-4" stroke="{G}" stroke-width="4" stroke-linecap="round"/>' + \
    person(70, 120, .9, 0, G) + person(120, 132, .8, 1, C) + person(160, 120, .9, 2, N) + \
    bubble(30, 40, 82, 44) + line(42, 52, 54) + line(42, 64, 36, .35) + \
    bubble(122, 30, 90, 50, tail="right") + check(136, 50) + line(160, 46, 38, .6) + line(160, 60, 28, .3) + \
    card(40, 200, 170, 36) + f'<rect x="52" y="212" width="60" height="12" rx="6" fill="{G}"/><rect x="116" y="212" width="40" height="12" rx="6" fill="{C}"/><rect x="160" y="212" width="36" height="12" rx="6" fill="{N}"/>' + \
    '</svg>'

# 3 Business intelligence: dashboard
svgs["chart"] = head("Illustration: a dashboard with a rising trend line, bar chart and pie chart") + bg(NT) + \
    card(40, 30, 320, 200) + f'<rect x="40" y="30" width="320" height="30" rx="12" fill="{N}"/><rect x="40" y="46" width="320" height="14" fill="{N}"/>' + \
    f'<circle cx="60" cy="45" r="5" fill="{R}"/><circle cx="76" cy="45" r="5" fill="{C}"/><circle cx="92" cy="45" r="5" fill="#3aa63a"/>' + \
    card(58, 76, 180, 136, "#f6f7fb", 10) + \
    ''.join(f'<rect x="{74+i*30}" y="{196-hh}" width="20" height="{hh}" rx="4" fill="{G}" opacity="{.35+i*.13}"/>' for i, hh in enumerate([30, 46, 40, 66, 84])) + \
    f'<path d="M84 150 L114 134 L144 140 L174 112 L204 92" fill="none" stroke="{C}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="204" cy="92" r="6" fill="#fff" stroke="{C}" stroke-width="4"/>' + \
    card(252, 76, 92, 64, "#f6f7fb", 10) + f'<circle cx="298" cy="108" r="20" fill="none" stroke="{NT}" stroke-width="10"/><circle cx="298" cy="108" r="20" fill="none" stroke="{G}" stroke-width="10" stroke-dasharray="80 126" transform="rotate(-90 298 108)"/>' + \
    card(252, 150, 92, 62, "#f6f7fb", 10) + line(264, 164, 50) + f'<text x="264" y="198" font-family="system-ui,sans-serif" font-size="22" font-weight="700" fill="{G}">+18%</text>'.replace("+18%", "▲") + line(286, 186, 44, .35) + \
    f'<g filter="url(#s)"><circle cx="330" cy="210" r="28" fill="#fff" fill-opacity=".95" stroke="{N}" stroke-width="7"/><path d="M350 230l24 24" stroke="{N}" stroke-width="10" stroke-linecap="round"/></g>' + check(318, 208) + \
    '</svg>'

# 4 Consultation: two people talking, plan board
svgs["chat"] = head("Illustration: a consultant and a client discussing a plan, with speech bubbles and a checklist") + bg(CT) + \
    card(150, 28, 110, 120) + line(164, 44, 70) + ''.join(check(166, 66+i*24, G, .8) + line(186, 64+i*24, 56-i*8, .45) for i in range(3)) + \
    f'<rect x="40" y="196" width="320" height="12" rx="6" fill="{N}"/><rect x="70" y="208" width="10" height="34" fill="{N}"/><rect x="320" y="208" width="10" height="34" fill="{N}"/>' + \
    person(90, 136, 1.0, 1, G) + person(310, 136, 1.0, 2, C) + \
    bubble(30, 60, 100, 48) + line(44, 74, 60) + line(44, 88, 40, .35) + \
    bubble(270, 54, 100, 48, tail="right") + line(284, 68, 66, .6) + line(284, 82, 46, .35) + \
    card(170, 168, 60, 26, "#fff", 6) + line(180, 178, 40, .4) + \
    '</svg>'

# 5 Compliance: certificate with seal, shield
svgs["shield"] = head("Illustration: an approved licence with an official stamp, a shield and a folder of documents") + bg(GT) + \
    card(60, 70, 120, 150, "#fff", 10) + card(80, 50, 130, 160, "#fff", 10) + \
    line(98, 70, 80) + line(98, 86, 94, .3) + line(98, 98, 84, .3) + line(98, 110, 90, .3) + line(98, 122, 60, .3) + \
    f'<circle cx="172" cy="178" r="22" fill="{C}"/><circle cx="172" cy="178" r="15" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="3 3"/>' + check(164, 178, "#fff", .9) + \
    f'<path d="M160 196l-6 22 10-6 8 8 2-22z" fill="{C}"/>' + \
    f'<g filter="url(#s)"><path d="M290 40l60 22v46c0 38-26 66-60 78-34-12-60-40-60-78V62z" fill="{G}"/></g>' + \
    f'<path d="M290 58l44 16v36c0 28-19 49-44 58z" fill="#fff" opacity=".15"/>' + check(268, 116, "#fff", 2) + \
    f'<path d="M232 212h120a8 8 0 0 0 8-8v-6h-136v6a8 8 0 0 0 8 8z" fill="{N}" opacity=".9"/>' + \
    '</svg>'

# 6 Digital marketing: phone + megaphone + likes
svgs["megaphone"] = head("Illustration: a smartphone showing a social media post, a megaphone and growing likes") + bg(NT) + \
    f'<g filter="url(#s)"><rect x="140" y="20" width="120" height="224" rx="20" fill="{ND}"/></g><rect x="148" y="34" width="104" height="196" rx="12" fill="#fff"/>' + \
    f'<circle cx="164" cy="52" r="9" fill="{C}"/>' + line(178, 46, 50, .7) + line(178, 56, 30, .3) + \
    f'<rect x="156" y="70" width="88" height="70" rx="8" fill="{GT}"/><path d="M164 132l22-30 16 18 12-12 22 24z" fill="{G}"/><circle cx="224" cy="88" r="8" fill="{C}"/>' + \
    line(156, 152, 80, .6) + line(156, 164, 60, .3) + \
    f'<rect x="156" y="182" width="88" height="34" rx="8" fill="{NT}"/>' + line(166, 195, 50, .5) + \
    f'<g transform="translate(40 120)" filter="url(#s)"><path d="M0 18v24h16l44 24V-6L16 18z" fill="{C}"/><rect x="2" y="42" width="14" height="30" rx="4" fill="{N}"/></g>' + \
    f'<path d="M110 120a20 20 0 0 1 0 34M120 108a36 36 0 0 1 0 58" fill="none" stroke="{C}" stroke-width="4" stroke-linecap="round"/>' + \
    f'<g filter="url(#s)"><rect x="280" y="50" width="86" height="40" rx="20" fill="#fff"/></g><path d="M300 64c-4-5-12-2-10 4 1 4 10 10 10 10s9-6 10-10c2-6-6-9-10-4z" fill="{R}"/>' + line(318, 66, 36, .6) + \
    f'<g filter="url(#s)"><rect x="290" y="110" width="76" height="40" rx="20" fill="#fff"/></g><path d="M306 138l8-10 6 6 10-12" fill="none" stroke="{G}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>' + line(336, 126, 20, .5) + \
    f'<g filter="url(#s)"><rect x="276" y="170" width="90" height="40" rx="20" fill="#fff"/></g><circle cx="296" cy="190" r="9" fill="none" stroke="{N}" stroke-width="3"/><path d="M302 196l6 6" stroke="{N}" stroke-width="3" stroke-linecap="round"/>' + line(314, 186, 40, .5) + \
    '</svg>'

# 7 Nonprofits: community + clinic + heart + report
svgs["heart"] = head("Illustration: a community in front of a health centre, with a heart and a donor report") + bg(CT) + \
    card(30, 60, 150, 120, "#fff", 10) + f'<path d="M22 70 L105 24 L188 70z" fill="{G}" filter="url(#s)"/>' + \
    f'<rect x="92" y="72" width="26" height="26" rx="4" fill="{C}"/><path d="M105 77v16M97 85h16" stroke="#fff" stroke-width="4" stroke-linecap="round"/>' + \
    f'<rect x="90" y="132" width="30" height="48" rx="4" fill="{NT}"/><rect x="44" y="112" width="30" height="24" rx="4" fill="{NT}"/><rect x="136" y="112" width="30" height="24" rx="4" fill="{NT}"/>' + \
    person(70, 196, .75, 0, N) + person(110, 192, .85, 3, G) + person(150, 196, .75, 2, C) + \
    f'<g filter="url(#s)"><path d="M290 112s-46-26-46-58a24 24 0 0 1 46-10 24 24 0 0 1 46 10c0 32-46 58-46 58z" fill="{R}"/></g>' + \
    card(230, 140, 140, 96, "#fff", 10) + line(244, 154, 70) + \
    ''.join(f'<rect x="{248+i*22}" y="{222-hh}" width="14" height="{hh}" rx="3" fill="{G}" opacity="{.4+i*.15}"/>' for i, hh in enumerate([14, 22, 30, 40, 48])) + \
    '</svg>'

# 8 Field data collection: interviewer with tablet + respondent + map pins
svgs["clipboard"] = head("Illustration: a field interviewer with a tablet surveying a respondent, with location pins on a map") + bg(GT) + \
    f'<path d="M210 60 L360 40 L380 160 L230 190z" fill="#fff" opacity=".85" filter="url(#s)"/>' + \
    f'<path d="M236 160 C 270 120, 300 150, 330 90 S 360 70, 368 60" fill="none" stroke="{N}" stroke-width="3" stroke-dasharray="3 8" stroke-linecap="round" opacity=".5"/>' + \
    pin(250, 110, C, .8) + pin(300, 80, G, .8) + pin(346, 40, N, .8) + \
    person(80, 120, 1.0, 1, G) + person(170, 126, .95, 2, C) + \
    f'<g transform="rotate(-8 112 160)"><rect x="96" y="140" width="34" height="46" rx="5" fill="{ND}"/><rect x="100" y="145" width="26" height="34" rx="2" fill="#fff"/></g>' + \
    check(104, 156, G, .6) + check(104, 168, G, .6) + \
    bubble(140, 52, 76, 40, tail="right") + line(152, 64, 48, .6) + line(152, 76, 30, .3) + \
    card(30, 200, 210, 40, "#fff", 10) + \
    ''.join(f'<rect x="{44+i*36}" y="212" width="28" height="16" rx="4" fill="{[G,C,N,G,C][i]}" opacity="{.85 if i<3 else .3}"/>' for i in range(5)) + \
    '</svg>'

# 9 Generic research (default icon): magnifier over documents
svgs["search"] = head("Illustration: a magnifying glass over research documents and a chart") + bg(NT) + \
    card(70, 50, 150, 180, "#fff", 10) + line(88, 70, 90) + line(88, 86, 110, .3) + line(88, 98, 96, .3) + line(88, 110, 104, .3) + \
    ''.join(f'<rect x="{92+i*24}" y="{206-hh}" width="16" height="{hh}" rx="3" fill="{G}" opacity="{.4+i*.15}"/>' for i, hh in enumerate([20, 32, 44, 60])) + \
    f'<g filter="url(#s)"><circle cx="260" cy="120" r="56" fill="#fff" fill-opacity=".95" stroke="{N}" stroke-width="12"/><path d="M300 160l50 50" stroke="{N}" stroke-width="18" stroke-linecap="round"/></g>' + \
    f'<path d="M232 132l18-18 14 12 22-26" fill="none" stroke="{C}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>' + \
    '</svg>'

for k, v in svgs.items():
    open(os.path.join(OUT, f"{k}.svg"), "w").write(v)
print(list(svgs))
