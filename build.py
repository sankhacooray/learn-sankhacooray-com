"""Builds public/index.html from template.html + projects.json.

Run:  python3 build.py
Everything lands in static HTML so link-preview crawlers and search engines see it.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "projects.json")))
tpl = open(os.path.join(HERE, "template.html")).read()
e = html.escape

ICONS = {
    "android": ("Android", '<path fill="currentColor" d="M5.2 2.1a.4.4 0 01.55.13l.7 1.12A5 5 0 018 3.1c.55 0 1.07.09 1.55.25l.7-1.12a.4.4 0 11.68.42l-.66 1.06A4.4 4.4 0 0112.5 7H3.5a4.4 4.4 0 012.23-3.29l-.66-1.06a.4.4 0 01.13-.55zM6 5.4a.55.55 0 100 1.1.55.55 0 000-1.1zm4 0a.55.55 0 100 1.1.55.55 0 000-1.1zM3.5 8h9v4.5a1 1 0 01-1 1h-7a1 1 0 01-1-1V8z"/>'),
    "ios": ("iPhone", '<path fill="currentColor" d="M11.2 8.5c0-1.5 1.2-2.2 1.3-2.3-.7-1-1.8-1.2-2.2-1.2-.9-.1-1.8.6-2.3.6s-1.2-.5-2-.5c-1 0-2 .6-2.5 1.6-1.1 1.9-.3 4.6.8 6.1.5.7 1.1 1.6 1.9 1.5.8 0 1-.5 2-.5s1.2.5 2 .5 1.3-.8 1.8-1.5c.6-.8.8-1.6.8-1.7 0 0-1.6-.6-1.6-2.6zM9.7 4c.4-.5.7-1.2.6-1.9-.6 0-1.4.4-1.8.9-.4.4-.7 1.1-.6 1.8.7.1 1.4-.3 1.8-.8z"/>'),
    "web": ("Web", '<g fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="8" cy="8" r="6"/><path d="M2 8h12M8 2c1.7 1.8 2.5 3.8 2.5 6S9.7 12.2 8 14M8 2C6.3 3.8 5.5 5.8 5.5 8s.8 4.2 2.5 6"/></g>'),
}


def plats(ps):
    return "".join(
        f'<svg class="pi pi-{k}" viewBox="0 0 16 16" role="img" aria-label="{ICONS[k][0]}"><title>{ICONS[k][0]}</title>{ICONS[k][1]}</svg>'
        for k in ps if k in ICONS)


KIND = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="6.5" y="2.5" width="11" height="19" rx="2.2"/><path d="M10.5 18.5h3"/></svg>',
    "browser": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2.5" y="4" width="19" height="16" rx="2"/><path d="M2.5 8.5h19M5.5 6.3h.01M7.8 6.3h.01"/></svg>',
    "service": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="3.5" y="4" width="17" height="6.5" rx="1.6"/><rect x="3.5" y="13.5" width="17" height="6.5" rx="1.6"/><path d="M7 7.25h.01M7 16.75h.01M11 7.25h6M11 16.75h6"/></svg>',
}


def kind(p):
    if {"ios", "android"} & set(p["plat"]):
        return "phone"
    return "browser" if "web" in p["plat"] else "service"


def initials(name):
    words = [w for w in name.replace("@", " ").split() if w[0].isalnum()]
    return "".join(w[0] for w in words[:2]).upper()


def card(p):
    if p.get("thumb"):
        art = f'<div class="art"><img src="/thumbs/{e(p["thumb"])}" alt="{e(p["name"])}" loading="lazy" width="800" height="500"></div>'
    else:
        art = f'<div class="art blank" aria-hidden="true">{KIND[kind(p)]}</div>'
    link = ""
    if p.get("url"):
        link = f'<a class="open" href="{e(p["url"])}" target="_blank" rel="noopener">{e(p.get("urlLabel", "Open"))}</a>'
    role = data["roles"][p["role"]]
    return (f'<article class="card">{art}<div class="cbody"><div class="ctop"><h3>{e(p["name"])}</h3>'
            f'<span class="role {p["role"]}">{role}</span></div><p>{e(p["desc"])}</p>'
            f'<div class="cfoot"><span class="plats">{plats(p["plat"])}</span><span class="org">{e(p["org"])}</span>{link}</div></div></article>')


FOOTER = open(os.path.join(HERE, "footer.html")).read()
groups, nav = [], []
for i, g in enumerate(data["groups"]):
    n = len(g["projects"])
    last = i == len(data["groups"]) - 1
    groups.append(
        f'  <section class="group{" last" if last else ""}" id="{g["id"]}"><div class="wrap">\n'
        f'    <div class="ghead"><div><h2>{e(g["title"])}</h2><p>{e(g["lede"])}</p></div>'
        f'<div class="ctx">{e(g["context"])} · <span class="n">{n}</span> project{"s" if n != 1 else ""}</div></div>\n'
        f'    <div class="cards">{"".join(card(p) for p in g["projects"])}</div>\n'
        f'  </div>\n{FOOTER if last else ""}  </section>')
NAV = {"science": "Science", "spark": "Microlearning", "content": "AI content", "children": "Children", "ice": "ICE"}
for g in data["groups"]:
    nav.append(f'<a href="#{g["id"]}">{NAV.get(g["id"], g["title"])}</a>')

allp = [p for g in data["groups"] for p in g["projects"]]
live = sum(1 for p in allp if p.get("url"))
stats = (f'<span class="stat"><b>{len(allp)}</b> projects</span>'
         f'<span class="stat"><b>{len(data["groups"])}</b> research areas</span>'
         f'<span class="stat"><b>{live}</b> live links</span>')

desc = ("Learning projects by Sankha Cooray: Kiwrious science sensors, SPARK microlearning at NUS CHILL, "
        "Scratch GPT for children, and design-thinking programmes.")
assert 120 <= len(desc) <= 160, len(desc)

out = (tpl.replace("{{GROUPS}}", "\n".join(groups)).replace("{{NAV}}", "".join(nav))
       .replace("{{STATS}}", stats)
       .replace("{{DESC}}", e(desc)))
os.makedirs(os.path.join(HERE, "public"), exist_ok=True)
open(os.path.join(HERE, "public", "index.html"), "w").write(out)
print("built public/index.html:", len(allp), "projects,", live, "live")
