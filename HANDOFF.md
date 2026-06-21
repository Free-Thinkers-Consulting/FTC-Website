# Free Thinkers Consulting — Website Migration Handoff

Handoff doc for Claude Code. Picks up an in-progress migration of
`freethinkersconsulting.com` off WordPress to a static site.

---

## 0. Status — updated 2026-06-11

**Homepage punch-list (section 4): DONE**
- ✅ Clients rebuilt as a vanilla-JS carousel — full-color logos in white
  cards with soft shadows, pager dots, auto-advance (3.5s), pause on hover.
- ✅ 3-tile photo band added between the process and clients sections.
- ✅ Logo treatment is now full-color cards (no grayscale).
- ✅ Spacing/rhythm verified against the live site in a local preview.

**Salesforce web-to-lead form (section 5): DONE**
- Pulled the real embed from the live `/contact/` source and dropped it in,
  restyled with classes (`.sf-form`). Action, `oid` (`00Da500000I9TVx`),
  `retURL`, `lead_source`, and all field names are **unchanged** — it still
  posts to `webto.salesforce.com`. Lives on the homepage, `/contact/`, and
  `/get-started/`.

**Remaining pages (section 6): DONE** — all built with a shared
header/footer and the locked design system, using directory-style clean URLs
(`services/index.html` → `/services/`):
- `/services/` (anchors `#managedservices`, `#architect`, `#design`)
- `/industries/` (anchors `#fintech`, `#manufacture`, `#professional`)
- `/about/`, `/contact/`, `/cases/`, `/why-salesforce/`, `/get-started/`
- `/blog/` index + **all 6 posts** written from the live content. The
  `/blog/15-signs-…/` post doubles as the **post template** (see the comment at
  the top of that file).

**Assets (section 7): DONE** — all referenced images downloaded into `/assets`
and every reference rewritten to `/assets/…`. There are now **zero `i0.wp.com`
references** anywhere in the HTML/CSS. Large assets were compressed (the two big
blog JPEGs recompressed, the three case PNGs converted to JPEG) — total `/assets`
dropped from ~11MB to ~1.7MB. The site is self-contained.

### Still open
1. **Case-study detail pages.** `/cases/` cards currently link to the matching
   `/industries/#anchor`. If real case studies are wanted, build detail pages.
2. **Deploy** (section 8) — not started.

> **Note on paths:** the working repo (with git) lives in this session's
> `outputs/ftc-website`. Preview it with the `ftc-static` config in
> `.claude/launch.json`, or `python3 -m http.server 8000` from the repo root.

---

## 1. Goal & context

Replace the WordPress build with a static HTML/CSS/JS site because WordPress is
expensive to host, expensive to change (paid developer), and slow to edit.

Target outcome:
- Static site, hosted free on **Cloudflare Pages or Netlify**, auto-deploying on
  every push to `main`.
- Code lives in GitHub org **`Free-Thinkers-Consulting`** (repo: `ftc-website`).
- Owner (Olivia) is a software developer and will edit directly or via Claude.
- No CMS. Blog is ~2 posts/month, published as static pages on request.

The homepage is already built as the **canonical style reference**. Your job:
perfect the homepage to match the live site, then replicate the styling across
the remaining eight pages.

---

## 2. Current state of the repo

```
ftc-website/
├── index.html          # Homepage — DONE (style reference)
├── css/styles.css      # All styles — DONE (design system locked)
├── assets/             # Empty — TODO: localize images here
├── netlify.toml        # Deploy config (Cloudflare Pages works too)
├── README.md
└── HANDOFF.md          # This file
```

Run a local dev server to preview as you work:
```
cd ftc-website && python3 -m http.server 8000   # http://localhost:8000
```

---

## 3. Design system — pulled from the LIVE site (authoritative)

These values were extracted from the live site's computed styles. Trust them
over the brand kit PDF (the PDF lists Plus Jakarta Sans, but the live site
actually uses **EB Garamond**).

**Fonts** (Google Fonts)
- Headings + body: `"EB Garamond", serif` — headings 700 weight, `text-transform: capitalize`
- UI / nav buttons / small labels: `"Poppins", sans-serif`
- Body base size 18px, line-height ~1.6

**Colors**
| Token | Hex | Use |
|-------|-----|-----|
| Purple (primary) | `#5039FF` | links, CTAs, accents, contact section bg |
| Purple deep | `#291D8D` | gradient/hover depth |
| Navy | `#1C244B` | lead text, secondary headings |
| Ink | `#000000` | headings, body |
| Soft bg | `#f5f5fb` | alternating section background |
| Footer bg | `#000000` | footer |

**Type scale (live values)**
- Hero H1 "We Help You": EB Garamond 700, ~75px desktop (use `clamp()`), black
- Rotating headline: same size, purple `#5039FF`, wrapped in brackets `[ … ]`
- Section titles: EB Garamond 700, capitalize, ~2–2.8rem
- Lead paragraph: EB Garamond 500, ~1.45rem, navy `#1C244B`

**Buttons**
- Outline ("Learn More"): transparent bg, 1px `#5039FF` border, purple text,
  `border-radius: 36px` (pill), trailing arrow `→`
- Filled ("Get Started"): solid `#5039FF`, white text, pill
- Form "Send" button on live site: solid `#5039FF`, `border-radius: 3px`, Poppins

**Hero treatment**
- Full-bleed background photo: `uploads/2026/03/businesspeople-meeting-plan-analysis-graph-company-finance-strat-1.webp`
- Left-to-right white fade overlay so left-side text stays readable
- Salesforce Partner badge floats on the right
  (`uploads/2023/03/Salesforce_Partner_Badge_RGB.png`)

---

## 4. Punch-list — known differences to fix on the homepage

The homepage captures the design language but these details still differ from
the live site (visible in side-by-side screenshots):

1. **Clients = carousel, not static strip.** Live site is a sliding logo
   carousel: each logo sits in a **white card with a soft shadow**, with pager
   **dots** below and auto-advance. Current build is a static grayscale flex row.
   Rebuild as a carousel (vanilla JS, no heavy deps).
2. **Photo band above clients.** Live site has a 3-tile photo strip (notebook/pen,
   a network-graphic image, a person at a desk) between the process section and
   the clients section. Add it.
3. **Logo treatment.** Live logos are full-color inside white cards (not the
   grayscale-until-hover treatment currently used).
4. **Verify spacing/rhythm** against live site once a dev server is running and
   you can screenshot — match section padding and the hero height.

---

## 5. Salesforce web-to-lead form — DO NOT change behavior

The "Speak with an Expert" contact form is a **Salesforce web-to-lead** embed
that syncs leads directly into Salesforce. This must keep working exactly as-is.

- In `index.html`, the contact section has a placeholder div marked
  `SALESFORCE WEB-TO-LEAD FORM`.
- Get the exact existing embed/iframe markup from the current live site (view
  source on the WordPress contact section, or ask Olivia) and paste it in,
  styled to fit. **Do not rebuild the form or repoint where it submits.**

---

## 6. Remaining pages to build (replicate homepage styling)

Match the live site's content and the design system above:
- `/services/` (anchors: #managedservices, #design, #architect)
- `/industries/` (anchors: #manufacture, #fintech, #professional)
- `/about/`
- `/contact/`
- `/cases/` (Case Studies)
- `/why-salesforce/`
- `/get-started/`
- `/blog/` (index + post template; ~2 posts/month, static, published on request)

Use a shared header/footer. Since this is static, either duplicate the markup or
introduce a tiny build step / HTML includes — keep it simple and dependency-light.

---

## 7. Assets — localize off WordPress

The homepage currently references images from the WordPress CDN
(`i0.wp.com/freethinkersconsulting.com/...`). Before going live, download clean
copies into `/assets` and update paths, so the new site has **zero dependency on
WordPress**. Brand-kit source files (logos, EB Garamond, color palette) live in
Olivia's Google Drive "FTC Branding Kit" folder.

---

## 8. Deploy plan

1. Push repo to `github.com/Free-Thinkers-Consulting/ftc-website` (`main`).
2. Connect repo to Cloudflare Pages or Netlify — build command: none, publish
   dir: root (`/`).
3. Stage at the temporary `*.pages.dev` / `*.netlify.app` URL; review against
   live site.
4. Only after sign-off, point `freethinkersconsulting.com` DNS at the new host
   (zero-downtime cutover).
5. Once stable, decommission WordPress hosting + plugin licenses (WP Rocket, etc.).

---

## 9. First steps for Claude Code

1. Read `index.html` and `css/styles.css` to absorb the design system.
2. Start a dev server and screenshot the homepage next to the live site.
3. Work the section 4 punch-list (carousel, photo band, logo cards, spacing).
4. Get the Salesforce web-to-lead embed in and styled.
5. Build the remaining pages (section 6) with shared header/footer.
6. Localize assets (section 7), then deploy (section 8).
