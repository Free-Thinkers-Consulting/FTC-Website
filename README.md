# Free Thinkers Consulting — Website

Static site replacing the WordPress build. No database, no plugins — just HTML/CSS/JS.
Hosts free on Cloudflare Pages or Netlify; every `git push` auto-deploys.

## Structure

```
ftc-website/
├── index.html                  # Homepage — "Start With Why" (WHY → HOW → WHAT → logos
│                               #   → testimonials → final CTA), dark theme
├── services/index.html         # /services/   (#managedservices, #architect, #design)
├── industries/index.html       # /industries/ (#fintech, #manufacture, #professional)
├── about/index.html            # /about/
├── contact/index.html          # /contact/    (Salesforce web-to-lead form)
├── cases/index.html            # /cases/
├── why-salesforce/index.html   # /why-salesforce/
├── get-started/index.html      # /get-started/ (Salesforce web-to-lead form)
├── blog/
│   ├── index.html              # /blog/  (post grid)
│   └── 15-signs-…/index.html   # a published post — also the POST TEMPLATE
├── css/styles.css              # All site styles (design system)
├── assets/                     # All images, localized off WordPress
├── netlify.toml                # Netlify deploy config (Cloudflare Pages works too)
└── HANDOFF.md                  # Migration notes + status
```

Pages use a **directory structure** (`services/index.html`) so clean URLs like
`/services/` work on any static host with zero config. All internal links and
asset paths are **root-absolute** (`/css/styles.css`, `/assets/logo.png`).

The header and footer markup is **duplicated** in each page (no build step). If
you change one, change them all — they're intentionally byte-identical.

## Brand / design system (dark)

- Typeface: **Plus Jakarta Sans** (headings, body, UI, buttons) — Google Fonts.
- Background `#0B0B14` · Surface `#16141F` · Purple accent `#6C4DFF`.
- Purple gradient `#6C4DFF → #3A2EFF → #1D1FBF` used on CTAs / accents / hero glow.
- Text stays high-contrast: white `#FFFFFF` / light lavender — no low-contrast gray.
- Tokens + components live in `css/styles.css`: `.btn`/`.btn-primary`/`.btn-outline`,
  the homepage `.why`/`.how`/`.what`/`.logos`/`.testimonials`/`.final-cta`,
  `.page-hero`, `.feature-card` / `.card-grid`, `.feature-row`, `.steps`,
  `.case-card`, `.blog-card`, `.cta-band`, `.sf-form`, etc.
- The stylesheet is linked with `?v=` for cache-busting — bump it when CSS changes.

## Contact form (Salesforce web-to-lead)

The contact form is the real Salesforce web-to-lead embed (on the homepage,
`/contact/`, and `/get-started/`). It posts to `webto.salesforce.com` with
`oid=00Da500000I9TVx`. **Do not change** the `action`, `oid`, `retURL`,
`lead_source`, or field names — only styling is custom.

## Publishing a blog post

1. Copy `blog/15-signs-…/index.html` to `blog/<your-slug>/index.html`.
2. Update the `<title>`, meta tags, the `.article-hero` (date + `<h1>`), and the
   `.article-body` content.
3. Add a `<a class="blog-card">` for it to the grid in `blog/index.html`.

## Local preview

Open `index.html` directly, or run a static server from the repo root:

```
python3 -m http.server 8000   # visit http://localhost:8000
```

## Push to GitHub

```
git add .
git commit -m "Build out site"
git branch -M main
git remote add origin git@github.com:Free-Thinkers-Consulting/ftc-website.git
git push -u origin main
```

## Deploy (free)

**Cloudflare Pages** or **Netlify** → connect the GitHub repo → build command: none,
publish directory: `/` (root). Auto-deploys on every push to `main`.

## Status

- [x] Homepage — "Start With Why": WHY → HOW → WHAT → client logos → testimonials → final CTA
- [x] Services
- [x] Industries
- [x] About
- [x] Contact
- [x] Case Studies
- [x] Why Salesforce
- [x] Get Started
- [x] Blog index + all 6 posts (the 15-signs post doubles as the template)
- [x] Images localized into `/assets` (zero WordPress dependency)
- [x] Compressed large images (~11MB → ~1.7MB total; case PNGs converted to JPEG)
- [ ] Deploy to Cloudflare Pages / Netlify
