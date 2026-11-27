# PickleballRx.org

Source for [pickleballrx.org](https://pickleballrx.org), an independent pickleball paddle lab: X-rays, microscope grit images, spin testing and specs.

## How it works

- `data/` holds the lab data. `data/labs.py` writes `labs.json`, `data/xray.py` writes `xray.json`.
- `build.py` turns the data into plain HTML pages in `site/`.
- Images live in `site/assets/` (X-rays in `assets/xray/`, microscope shots in `assets/grit/`).
- SEO is handled in `page()` and `write()` in `build.py`: each page gets its own title and description (`desc=`), a canonical URL, Open Graph and Twitter share tags (`image=` for a page-specific share image, default `assets/og-image.jpg`), JSON-LD structured data and breadcrumbs (`crumbs=`). Pages passed `noindex=True` (sample reviews, 404) stay out of search. `sitemap.xml` (with `lastmod`, which only moves when a page's content changes, and the X-ray images) and `robots.txt` are written at the end of the build. Search Console / Bing verification tags go in `GOOGLE_SITE_VERIFICATION` / `BING_SITE_VERIFICATION` in `build.py` (home page only). Each X-ray page doubles as the paddle's review page (title "<Paddle> Review & X-Ray"), and `best-pickleball-paddles-for-tennis-elbow.html` is built from `data/vibration.json`. The site description lives in `TAGLINE` / `SITE_DESC`.
- Every push runs `.github/workflows/pages.yml`, which rebuilds the site and publishes `site/` to GitHub Pages.

## Build locally

```
python3 data/labs.py
python3 data/xray.py
python3 build.py
```

Then open `site/index.html`.

This repository is public. Only add results and images that are cleared for publishing.
