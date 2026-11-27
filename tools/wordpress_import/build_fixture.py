"""Turn the cleaned WordPress data into a Django fixture (JSON).

Only content written by the site owner (user ID 1) is kept. All spam
posts created by the hacker accounts are dropped.
"""
import collections
import html
import json
import re
import sys

from bs4 import BeautifulSoup, Comment

SRC, OUT = sys.argv[1], sys.argv[2]
d = json.load(open(SRC))
P = {r["ID"]: r for r in d["wps8_posts"]}
META = collections.defaultdict(dict)
for m in d["wps8_postmeta"]:
    META[m["post_id"]][m["meta_key"]] = m["meta_value"]

# taxonomy lookups
TERMS = {t["term_id"]: t for t in d["wps8_terms"]}
TT = {t["term_taxonomy_id"]: t for t in d["wps8_term_taxonomy"]}
POST_TERMS = collections.defaultdict(list)
for rel in d["wps8_term_relationships"]:
    t = TT.get(rel["term_taxonomy_id"])
    if t:
        term = TERMS[t["term_id"]]
        POST_TERMS[rel["object_id"]].append(
            (t["taxonomy"], html.unescape(term["name"]), term["slug"]))

KEEP = {"h2", "h3", "h4", "h5", "p", "ul", "ol", "li", "strong", "b", "em", "i",
        "a", "blockquote", "table", "thead", "tbody", "tr", "th", "td", "img",
        "br", "hr", "figure", "figcaption"}
DROP = {"nav", "header", "footer", "script", "style", "svg", "form", "iframe",
        "button", "noscript", "input", "select", "textarea", "aside", "video"}
UPLOAD_RE = re.compile(r"https?://[^\"']*?/wp-content/uploads/")
OLD_LINK_RE = re.compile(r"^https?://(www\.)?ws-marketresearch\.com")
SHORTCODE_RE = re.compile(r"\[/?[a-zA-Z_\-]+[^\]]*\]")


def media_url(src):
    return UPLOAD_RE.sub("/media/uploads/", src)


def clean_html(raw):
    raw = SHORTCODE_RE.sub("", raw)
    soup = BeautifulSoup(raw, "html.parser")
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for tag in soup.find_all(DROP):
        tag.decompose()
    for tag in soup.find_all("h1"):
        tag.name = "h2"  # page template already shows the h1 title
    for tag in soup.find_all(True):
        if tag.name not in KEEP:
            tag.unwrap()
            continue
        attrs = {}
        if tag.name == "a" and tag.get("href"):
            href = tag["href"]
            href = OLD_LINK_RE.sub("", href) or "/"
            attrs["href"] = media_url(href)
            if href.startswith("http"):
                attrs["rel"] = "noopener"
        if tag.name == "img":
            src = tag.get("src", "")
            if "wp-content/uploads" not in src or "post-detail-" in src \
                    or "customersreviews" in src:
                tag.decompose()
                continue
            attrs = {"src": media_url(src), "alt": tag.get("alt", ""),
                     "loading": "lazy"}
        tag.attrs = attrs
    # remove empty paragraphs / headings / list items
    for _ in range(3):
        for tag in soup.find_all(["p", "h2", "h3", "h4", "h5", "li", "strong",
                                  "em", "ul", "ol", "figure", "blockquote"]):
            if not tag.get_text(strip=True) and not tag.find("img"):
                tag.decompose()
    out = str(soup)
    out = re.sub(r"\n\s*\n+", "\n", out)
    out = re.sub(r"[ \t]+", " ", out)
    return out.strip()


def strip_text(raw, limit=300):
    text = " ".join(BeautifulSoup(SHORTCODE_RE.sub("", raw), "html.parser")
                    .get_text(" ").split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "…"


def featured(pid):
    tid = META[pid].get("_thumbnail_id")
    att = P.get(tid) if tid else None
    if att and "wp-content/uploads" in att["guid"]:
        return media_url(att["guid"]).lstrip("/").replace("media/", "", 1)
    return ""


def seo_desc(pid, fallback):
    return (META[pid].get("rank_math_description") or fallback)[:300]


def trim_title(t):
    # a few titles have stray words glued to the end in WordPress
    t = html.unescape(t)
    t = t.replace("OrganizationLanscape", "Organization")
    t = t.replace("CameroonConsumers and Mineral Water", "Cameroon")
    t = t.replace("Nonprofits org", "Nonprofits")
    return t.strip()


fixture = []

# ---------- Articles (owner only, published) ----------
cat_pks = {}
for r in sorted(P.values(), key=lambda r: r["post_date"]):
    if r["post_type"] != "post" or r["post_author"] != "1" \
            or r["post_status"] != "publish":
        continue
    cats = [n for (tax, n, s) in POST_TERMS[r["ID"]]
            if tax == "category" and s not in ("uncategorized", "post")]
    cat = cats[0] if cats else "Market Insights"
    if cat not in cat_pks:
        cat_pks[cat] = len(cat_pks) + 1
        fixture.append({"model": "content.category", "pk": cat_pks[cat],
                        "fields": {"name": cat,
                                   "slug": re.sub(r"[^a-z0-9]+", "-",
                                                  cat.lower()).strip("-")}})
    body = clean_html(r["post_content"])
    fixture.append({"model": "content.article", "pk": int(r["ID"]), "fields": {
        "title": trim_title(r["post_title"]),
        "slug": r["post_name"],
        "category": cat_pks[cat],
        "excerpt": strip_text(r["post_excerpt"] or r["post_content"], 240),
        "meta_description": seo_desc(r["ID"], strip_text(r["post_content"], 155)),
        "body": body,
        "featured_image": featured(r["ID"]),
        "published_at": r["post_date"].replace(" ", "T") + "+01:00",
        "is_published": True,
    }})

FILLER = ["objectively innovate", "holisticly", "procedures for reliable",
          "dramatically engage", "outside the box", "efficiently unleash",
          "quickly maximize", "dramatically maintain", "cost of supplies",
          "change the volume", "bibend auctor", "phosfluorescently"]
HEADINGS = ["h2", "h3", "h4", "h5"]

SERVICE_SUMMARIES = {
    "marketing-strategy": "Connect with your audience, increase brand visibility and drive conversions through SEO, social media and paid advertising.",
    "partnership-ecosystem": "Strategic guidance for entering a new market or scaling your operations, from one-on-one sessions to full expansion plans.",
    "new-business-innovation": "Research tailored to nonprofits: measuring social impact, donor mapping and identifying funding opportunities.",
    "marketing-research": "Deep insights into consumer preferences, competitor strategies and market trends to help you craft winning campaigns.",
    "organizational-audit": "Expert guidance through Cameroon's regulatory landscape: licences, permits and government regulations.",
    "support-function": "Transform raw data into actionable insights: data analytics, industry trend reports and custom reports.",
    "lead-generation": "Feasibility studies, competitive analysis and consumer behaviour research for a smooth entry into the Cameroonian market.",
}


def clean_service(body_html):
    soup = BeautifulSoup(body_html, "html.parser")
    # 0. tab titles saved as <a> without a link become headings; theme demo
    #    images and loose filler text go away
    for a in soup.find_all("a", recursive=False):
        if not a.get("href"):
            a.name = "h2"
            a.string = " ".join(a.get_text(" ").split())
    for img in soup.find_all("img"):
        img.decompose()
    for br in soup.find_all("br", recursive=False):
        br.decompose()
    for node in list(soup.contents):
        if isinstance(node, str) and any(f in node.lower() for f in FILLER):
            node.extract()
    for h in soup.find_all(HEADINGS):
        if "analysises" in h.get_text().lower():
            h.decompose()
    # 1. demo filler text from the WordPress theme
    for tag in soup.find_all(["li", "p"]):
        if any(f in tag.get_text(" ").lower() for f in FILLER):
            tag.decompose()
    # 2. "Have you any question or querry / GET FREE CONSULTATION / Contact us" box
    for h in soup.find_all(HEADINGS):
        if "querry" in h.get_text().lower():
            nxt = h.find_next_sibling()
            while nxt is not None and (nxt.name == "p" and "consultation" in nxt.get_text().lower()
                                       or nxt.name == "a" and "contact" in nxt.get_text().lower()):
                after = nxt.find_next_sibling()
                nxt.decompose()
                nxt = after
            h.decompose()
    for a in soup.find_all("a", recursive=False):
        if "contact us" in a.get_text().lower():
            a.decompose()
    # 3. empty lists after filler removal
    for lst in soup.find_all(["ul", "ol"]):
        if not lst.find("li"):
            lst.decompose()
    # 4. first heading repeats the title (or is theme demo text)
    first = soup.find(HEADINGS)
    if first:
        first.decompose()
    # 5. duplicate consecutive headings and headings with nothing under them
    tops = [t for t in soup.contents if getattr(t, "name", None)]
    for i, t in enumerate(tops):
        if t.name not in HEADINGS:
            continue
        nxt = tops[i + 1] if i + 1 < len(tops) else None
        if nxt is None or (nxt.name in HEADINGS and (
                nxt.get_text(strip=True).lower().rstrip(".") == t.get_text(strip=True).lower().rstrip(".")
                or int(nxt.name[1]) <= int(t.name[1]))):
            t.decompose()
    # 6. "Benefit of Service" repeats the list above it
    for h in soup.find_all(HEADINGS):
        if h.get_text(strip=True).lower() == "benefit of service":
            nxt = h.find_next_sibling()
            if nxt is not None and nxt.name in ("ul", "ol"):
                nxt.decompose()
            h.decompose()
    return re.sub(r"\n\s*\n+", "\n", str(soup)).strip()


# ---------- Services ----------
for r in sorted((r for r in P.values() if r["post_type"] == "ova_sev"
                 and r["post_status"] == "publish"),
                key=lambda r: int(META[r["ID"]].get("ova_sev_met_order_sev") or 0)):
    body = clean_service(clean_html(r["post_content"]))
    fixture.append({"model": "content.service", "pk": int(r["ID"]), "fields": {
        "title": trim_title(r["post_title"]),
        "slug": r["post_name"],
        "summary": SERVICE_SUMMARIES.get(r["post_name"], ""),
        "body": body,
        "order": int(META[r["ID"]].get("ova_sev_met_order_sev") or 0),
    }})

# ---------- Case studies ----------
for r in sorted((r for r in P.values() if r["post_type"] == "ova_portfolio"
                 and r["post_status"] == "publish"), key=lambda r: r["post_date"]):
    cats = [n for (tax, n, s) in POST_TERMS[r["ID"]] if tax == "category_portfolio"]
    fixture.append({"model": "content.casestudy", "pk": int(r["ID"]), "fields": {
        "title": trim_title(r["post_title"]),
        "slug": r["post_name"],
        "categories": ", ".join(cats),
        "summary": seo_desc(r["ID"], strip_text(r["post_content"], 200)),
        "body": clean_html(r["post_content"]),
        "featured_image": featured(r["ID"]),
        "published_at": r["post_date"].replace(" ", "T") + "+01:00",
    }})

# ---------- FAQ ----------
faq_ids = ["4040", "3893", "3115", "3110", "3104", "3098", "3088", "3077", "6128"]
for order, fid in enumerate(faq_ids, 1):
    soup = BeautifulSoup(SHORTCODE_RE.sub("", P[fid]["post_content"]), "html.parser")
    q_tag = soup.find(["h1", "h2", "h3", "h4", "h5", "h6", "strong"])
    question = " ".join(q_tag.get_text(" ").split()) if q_tag else P[fid]["post_title"]
    if q_tag:
        q_tag.decompose()
    answer = clean_html(str(soup))
    fixture.append({"model": "content.faq", "pk": order, "fields": {
        "question": question, "answer": answer, "order": order}})

json.dump(fixture, open(OUT, "w"), ensure_ascii=False, indent=1)
print(collections.Counter(x["model"] for x in fixture))
