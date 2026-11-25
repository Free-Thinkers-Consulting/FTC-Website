#!/usr/bin/env python3
"""Build the free guide pages: /free/ (hub) and /free/<slug>/ (one per guide).

Each guide is a JSON file in scripts/free-guides/. Shared settings (the course
offer, social links) live in scripts/free-guides/_site.json. Hub cards that
point to free resources built elsewhere (e.g. /scorecard/) live in
scripts/free-guides/_links.json.

The site header and footer are copied from ai-readiness/index.html so they stay
byte-identical with the rest of the site.

Usage:  python3 scripts/build-free-pages.py
"""
import html
import json
import pathlib
import re
from urllib.parse import urlencode

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "free-guides"
SITE = json.loads((SRC / "_site.json").read_text())
OFFER = SITE["offer"]
REF = (ROOT / "ai-readiness" / "index.html").read_text()
CSS_VER = "16"
FREE_CSS_VER = "5"
BASE = "https://freethinkersconsulting.com"
# Shared logomark share card (see /assets/og/); 2400x1260, crop-safe.
OG_IMAGE = f"{BASE}/assets/og/ftc-logomark.png"


def e(s):
    return html.escape(s, quote=True)


def grab(pattern):
    m = re.search(pattern, REF, re.S)
    if not m:
        raise SystemExit(f"Could not find {pattern!r} in ai-readiness/index.html")
    return m.group(0)


HEADER = grab(r'  <header class="site-header".*?</header>').replace('src="/assets/image.png"', 'src="/assets/Freethinker-Logo.webp"', 1)
FOOTER = grab(r'  <footer class="site-footer">.*?</footer>')
GTAG = grab(r'  <!-- Google tag \(gtag.js\) -->.*?</script>\s*<script>.*?</script>')
NAV_SCRIPT = grab(r'  <script>\s*\(function \(\) \{\s*document.getElementById\("year"\).*?</script>')


def checkout(campaign, medium):
    q = urlencode({"utm_source": "free-guide", "utm_medium": medium, "utm_campaign": campaign})
    return f'{OFFER["checkout_url"]}?{q}'


def head(title, desc, path):
    url = f"{BASE}{path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{GTAG}
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="Free Thinkers Consulting" />
  <meta property="og:image" content="{OG_IMAGE}" />
  <meta property="og:image:secure_url" content="{OG_IMAGE}" />
  <meta property="og:image:width" content="2400" />
  <meta property="og:image:height" content="1260" />
  <meta property="og:image:type" content="image/png" />
  <meta property="og:image:alt" content="Free Thinkers Consulting, Salesforce Solutions" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{e(title)}" />
  <meta name="twitter:description" content="{e(desc)}" />
  <meta name="twitter:image" content="{OG_IMAGE}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&family=Anton&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/styles.css?v={CSS_VER}" />
  <link rel="stylesheet" href="/css/free.css?v={FREE_CSS_VER}" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
</head>
<body class="free-page">
"""


def promo_bar(campaign):
    return f"""  <div class="promo-bar">
    <span>{e(OFFER["bar_text"])}</span>
    <a class="promo-btn" href="{e(checkout(campaign, "top-bar"))}" data-track="bar">{e(OFFER["bar_button"])} &rarr;</a>
  </div>
"""


def price_line():
    return (f'<span class="offer-price"><s>{e(OFFER["list_price"])}</s>{e(OFFER["price"])}</span> '
            f'{e(OFFER["price_note"].lower())}. {e(OFFER["guarantee"])}.')


def guide_page(g):
    slug = g["slug"]
    path = f"/free/{slug}/"
    out = [head(g["meta_title"], g["meta_description"], path), promo_bar(slug), HEADER, "\n\n  <main>\n"]

    out.append(f"""    <section class="guide-hero">
      <div class="container">
        <a class="guide-back" href="/free/">&larr; Back to all free guides</a>
        <p class="guide-byline"><span>A free guide by</span> <strong>{e(SITE["author"])}</strong>
          <a href="{e(SITE["instagram"])}" target="_blank" rel="noopener">&#8599; Instagram</a>
          <a href="{e(SITE["tiktok"])}" target="_blank" rel="noopener">&#8599; TikTok</a></p>
        <h1>{e(g["title_main"])}<span class="accent">{e(g["title_accent"])}</span></h1>
        <p class="guide-sub">{e(g["sub"])}</p>
      </div>
    </section>
""")

    total = sum(len(s["steps"]) for s in g["sections"])
    if g.get("checklist"):
        out.append(f"""    <div class="progress" aria-live="polite">
      <div class="progress-inner">
        <div class="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
        <span class="progress-text"><span id="progress-count">0</span> of {total} done</span>
      </div>
    </div>
""")

    out.append('    <article class="guide-body">\n')
    for p in g.get("intro", []):
        out.append(f"      <p>{e(p)}</p>\n")

    b = g.get("before")
    if b:
        items = "".join(f"<li><strong>{e(t)}</strong> {e(d)}</li>" for t, d in b["items"])
        out.append(f'      <div class="callout"><p class="callout-label">{e(b["label"])}</p><ol>{items}</ol></div>\n')

    n = 0
    for s in g["sections"]:
        out.append(f'      <section class="guide-section">\n        <p class="guide-section-label">{e(s["label"])}</p>\n        <h2>{e(s["title"])}</h2>\n')
        for st in s["steps"]:
            n += 1
            num = f"{n:02d}"
            body = f'<p>{e(st["text"])}</p>'
            if st.get("list"):
                body += "<ul>" + "".join(f"<li>{e(x)}</li>" for x in st["list"]) + "</ul>"
            if st.get("prompt"):
                body += (f'<div class="copy-block"><div class="copy-head"><span>Prompt</span>'
                         f'<button type="button" class="copy-btn">Copy</button></div>'
                         f'<pre class="copy-text">{e(st["prompt"])}</pre></div>')
            if st.get("link"):
                href = st["link"]["href"]
                if href.startswith("/"):  # page on this site: same tab
                    body += f'<p class="step-link"><a href="{e(href)}">{e(st["link"]["text"])} &rarr;</a></p>'
                else:
                    body += (f'<p class="step-link"><a href="{e(href)}" target="_blank" rel="noopener">'
                             f'{e(st["link"]["text"])} &#8599;</a></p>')
            done = ""
            if g.get("checklist"):
                done = (f'<label class="step-done"><input type="checkbox" data-step="{n}" /> '
                        f'Mark day {n} done</label>')
            label = f"Day {num}" if g.get("checklist") else num
            out.append(f'        <div class="step-card" id="step-{n}"><p class="day-num">{label}</p>'
                       f'<h3>{e(st["title"])}</h3>{body}{done}</div>\n')
        out.append("      </section>\n")

    if g.get("closing"):
        out.append(f'      <p class="guide-closing">{e(g["closing"])}</p>\n')
    out.append(f'      <p class="guide-sign">{e(SITE["author"])} &middot; Founder, Free Thinkers Consulting</p>\n')
    out.append("    </article>\n")

    o = g["offer"]
    out.append(f"""
    <section class="offer-card">
      <p class="eyebrow">{e(o["label"])}</p>
      <h2>{e(o.get("card_headline", o["headline"]))}</h2>
      <p>{e(o["body"])} {price_line()}</p>
      <a class="btn btn-light btn-xl" href="{e(checkout(slug, "end-card"))}" data-track="card">{e(OFFER["button"])} <span class="arrow">&rarr;</span></a>
    </section>
  </main>

  <div class="offer-modal" id="offer-modal" role="dialog" aria-modal="true" aria-labelledby="offer-title" hidden>
    <div class="offer-backdrop" data-close></div>
    <div class="offer-box">
      <button type="button" class="offer-close" aria-label="Close" data-close>&times;</button>
      <p class="offer-label">{e(o["label"])}</p>
      <h2 id="offer-title">{e(o["headline"])}</h2>
      <p>{e(o["body"])}</p>
      <p>{price_line()}</p>
      <a class="offer-cta" href="{e(checkout(slug, "popup"))}" data-track="popup">{e(OFFER["button"])}</a>
      <button type="button" class="offer-later" data-close>Maybe later</button>
    </div>
  </div>

""")
    out.append(FOOTER + "\n\n" + NAV_SCRIPT + "\n")
    out.append(page_script(slug, total, bool(g.get("checklist"))))
    out.append("</body>\n</html>\n")
    return path, "".join(out)


def page_script(slug, total, checklist):
    return f"""  <script>
    (function () {{
      var SLUG = {json.dumps(slug)}, TOTAL = {total}, CHECKLIST = {str(checklist).lower()};
      var DELAY = {int(OFFER["popup_delay_seconds"])} * 1000, SCROLL = {int(OFFER["popup_scroll_percent"])} / 100;
      function track(name, extra) {{
        try {{ if (window.gtag) gtag("event", name, Object.assign({{ guide: SLUG }}, extra || {{}})); }} catch (err) {{}}
      }}
      function load(k) {{ try {{ return JSON.parse(localStorage.getItem(k) || "null"); }} catch (err) {{ return null; }} }}
      function save(k, v) {{ try {{ localStorage.setItem(k, JSON.stringify(v)); }} catch (err) {{}} }}

      /* Keep the progress bar just under the sticky site header */
      var hdr = document.querySelector(".site-header");
      function setHdr() {{ if (hdr) document.documentElement.style.setProperty("--hdr-h", hdr.offsetHeight + "px"); }}
      setHdr(); window.addEventListener("resize", setHdr);

      /* Checklist progress, saved in this browser */
      if (CHECKLIST) {{
        var key = "ftc-free-" + SLUG, done = load(key) || {{}};
        var boxes = document.querySelectorAll(".step-done input");
        var fill = document.getElementById("progress-fill"), count = document.getElementById("progress-count");
        function paint() {{
          var n = 0;
          boxes.forEach(function (b) {{
            var on = !!done[b.dataset.step]; b.checked = on;
            b.closest(".step-card").classList.toggle("is-done", on); if (on) n++;
          }});
          count.textContent = n; fill.style.width = (100 * n / TOTAL) + "%";
          return n;
        }}
        boxes.forEach(function (b) {{
          b.addEventListener("change", function () {{
            if (b.checked) done[b.dataset.step] = 1; else delete done[b.dataset.step];
            save(key, done);
            var n = paint();
            if (b.checked) track("guide_step_done", {{ step: Number(b.dataset.step), done_count: n }});
          }});
        }});
        paint();
      }}

      /* Copy buttons */
      document.querySelectorAll(".copy-btn").forEach(function (btn) {{
        btn.addEventListener("click", function () {{
          var t = btn.closest(".copy-block").querySelector(".copy-text").innerText;
          var ok = function () {{ btn.textContent = "Copied!"; setTimeout(function () {{ btn.textContent = "Copy"; }}, 1800); }};
          if (navigator.clipboard) navigator.clipboard.writeText(t).then(ok, function () {{}});
          track("guide_copy_prompt");
        }});
      }});

      /* Course pop-up: once per visit, after a delay or partway down the page */
      var modal = document.getElementById("offer-modal"), shown = false, lastFocus = null;
      function seen() {{ try {{ return sessionStorage.getItem("ftc-offer-seen") === "1"; }} catch (err) {{ return shown; }} }}
      function markSeen() {{ try {{ sessionStorage.setItem("ftc-offer-seen", "1"); }} catch (err) {{}} }}
      function openModal(why) {{
        if (shown || seen()) return;
        shown = true; markSeen(); lastFocus = document.activeElement;
        modal.hidden = false; modal.classList.add("open");
        modal.querySelector(".offer-cta").focus();
        track("offer_popup_open", {{ trigger: why }});
      }}
      function closeModal() {{
        modal.classList.remove("open"); modal.hidden = true;
        if (lastFocus) lastFocus.focus();
        track("offer_popup_close");
      }}
      modal.querySelectorAll("[data-close]").forEach(function (el) {{ el.addEventListener("click", closeModal); }});
      document.addEventListener("keydown", function (ev) {{ if (ev.key === "Escape" && modal.classList.contains("open")) closeModal(); }});
      setTimeout(function () {{ openModal("time"); }}, DELAY);
      window.addEventListener("scroll", function () {{
        var h = document.documentElement, max = h.scrollHeight - h.clientHeight;
        if (max > 0 && h.scrollTop / max >= SCROLL) openModal("scroll");
      }}, {{ passive: true }});

      document.querySelectorAll("[data-track]").forEach(function (a) {{
        a.addEventListener("click", function () {{ track("offer_click", {{ placement: a.dataset.track }}); }});
      }});
    }})();
  </script>
"""


def hub_card(href, tag, title, desc, cta):
    return f"""        <a class="free-card" href="{e(href)}">
          <span class="free-tag">{e(tag)}</span>
          <h3>{e(title)}</h3>
          <p>{e(desc)}</p>
          <span class="free-go">{e(cta)} &rarr;</span>
        </a>
"""


def hub_page(guides, links=()):
    path = "/free/"
    title = "Free Guides and Resources | Olivia Porter, Free Thinkers Consulting"
    desc = "Every free guide, checklist, and resource from Olivia Porter's videos, in one place. CRMs, AI, and getting your time back."
    entries = [(g.get("order", 99), f"/free/{g['slug']}/", g.get("tag", "Free guide"), g["card_title"], g["card_desc"], "Read guide")
               for g in guides]
    entries += [(l.get("order", 99), l["href"], l["tag"], l["card_title"], l["card_desc"], l["cta"]) for l in links]
    entries.sort(key=lambda x: x[0])
    cards = "".join(hub_card(*x[1:]) for x in entries)
    body = f"""

  <main>
    <section class="guide-hero">
      <div class="container">
        <p class="guide-byline"><span>Free guides by</span> <strong>{e(SITE["author"])}</strong>
          <a href="{e(SITE["instagram"])}" target="_blank" rel="noopener">&#8599; Instagram</a>
          <a href="{e(SITE["tiktok"])}" target="_blank" rel="noopener">&#8599; TikTok</a></p>
        <h1>Free Guides<span class="accent">and resources</span></h1>
        <p class="guide-sub">Everything I promise in my videos lives here. Free, no download, no PDF.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="free-grid">
{cards}        </div>
      </div>
    </section>
  </main>

"""
    return path, head(title, desc, path) + promo_bar("hub") + HEADER + body + FOOTER + "\n\n" + NAV_SCRIPT + "\n</body>\n</html>\n"


def update_sitemap(paths):
    sm = ROOT / "sitemap.xml"
    text = sm.read_text()
    added = []
    for p in paths:
        loc = f"{BASE}{p}"
        if f"<loc>{loc}</loc>" not in text:
            entry = f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n"
            text = text.replace("</urlset>", entry + "</urlset>")
            added.append(loc)
    sm.write_text(text)
    return added


if __name__ == "__main__":
    import datetime
    TODAY = datetime.date.today().isoformat()
    guides = sorted((json.loads(f.read_text()) for f in SRC.glob("*.json") if not f.name.startswith("_")),
                    key=lambda g: (g.get("order", 99), g["slug"]))
    written = []
    for g in guides:
        path, page = guide_page(g)
        dest = ROOT / path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page)
        written.append(path)
    links_file = SRC / "_links.json"
    links = json.loads(links_file.read_text())["links"] if links_file.exists() else []
    path, page = hub_page(guides, links)
    (ROOT / "free").mkdir(exist_ok=True)
    (ROOT / "free" / "index.html").write_text(page)
    written.insert(0, path)
    added = update_sitemap(written)
    print("Built:", ", ".join(written))
    print("Sitemap added:", ", ".join(added) or "nothing new")
