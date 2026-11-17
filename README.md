# PickleballRx.org

Source for [pickleballrx.org](https://pickleballrx.org), an independent pickleball paddle lab: X-rays, microscope grit images, spin testing and specs.

## How it works

- `data/` holds the lab data. `data/labs.py` writes `labs.json`, `data/xray.py` writes `xray.json`.
- `build.py` turns the data into plain HTML pages in `site/`.
- Images live in `site/assets/` (X-rays in `assets/xray/`, microscope shots in `assets/grit/`).
- Every push runs `.github/workflows/pages.yml`, which rebuilds the site and publishes `site/` to GitHub Pages.

## Build locally

```
python3 data/labs.py
python3 data/xray.py
python3 build.py
```

Then open `site/index.html`.

This repository is public. Only add results and images that are cleared for publishing.
