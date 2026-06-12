# Free Thinkers Consulting — Website

Static site replacing the WordPress build. No database, no plugins — just HTML/CSS/JS.
Hosts free on Cloudflare Pages or Netlify; every `git push` auto-deploys.

## Structure

```
ftc-website/
├── index.html          # Homepage
├── css/
│   └── styles.css      # All site styles
├── assets/             # Local logos/images (brand kit) — TODO: localize
├── netlify.toml        # Netlify deploy config (Cloudflare Pages works too)
└── README.md
```

## Brand

- Gradient: `#4F38FF → #291D8D`  ·  Solid: `#4F38FF`
- Font: Plus Jakarta Sans (loaded from Google Fonts)

## Contact form

The "Speak with an Expert" section contains a placeholder div marked
`SALESFORCE WEB-TO-LEAD FORM` in `index.html`. Paste the existing Salesforce
web-to-lead embed/iframe there — it keeps syncing leads to Salesforce, unchanged.

## Local preview

Just open `index.html` in a browser, or run a static server:

```
python3 -m http.server 8000
# visit http://localhost:8000
```

## Push to GitHub

```
git init
git add .
git commit -m "Initial static site"
git branch -M main
git remote add origin git@github.com:<your-org>/ftc-website.git
git push -u origin main
```

## Deploy (free)

**Cloudflare Pages** or **Netlify** → connect the GitHub repo → build command: none,
publish directory: `/` (root). Auto-deploys on every push to `main`.

## Status

- [x] Homepage
- [ ] Services
- [ ] Industries
- [ ] About
- [ ] Contact
- [ ] Case Studies
- [ ] Blog (2 posts/month, published on request)
- [ ] Why Salesforce
- [ ] Get Started
- [ ] Localize images into `/assets` (currently referencing live CDN URLs)
