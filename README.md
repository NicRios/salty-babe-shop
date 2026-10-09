# Salty Babe Shop recreation

Editable recreation of [availethphoto.com/salty-babe-shop](https://availethphoto.com/salty-babe-shop), captured October 8, 2026. This first version follows the shop page's existing composition, photography, text, and destination links. It does not recreate the other destination pages or process purchases.

- **Live page:** https://nicrios.github.io/salty-babe-shop/
- **Local preview:** `python3 -m http.server 4174 --bind 127.0.0.1`
- **Desktop reference:** `references/salty-babe-desktop-1510.jpg` (1510 × 1000 viewport, full page)
- **Mobile reference:** `references/salty-babe-mobile-390.jpg` (390 × 844 viewport, full page)

## Editing

Text, image paths, links, and the original desktop/mobile positions live in `content/site.json`. Rebuild the HTML and position rules with `python3 scripts/build.py`. The masthead and hero are in that script's template; their styles live in `assets/styles.css`. The header navigation has been removed on desktop and mobile; the page no longer loads runtime JavaScript.

Photographs and decorative images are in `assets/images/`; all fonts are in `assets/fonts/`. No scripts, CSS, fonts, images, analytics, or embeds load from another host. A Content Security Policy enforces same-origin resources. Ordinary navigation and product links retain their original destinations.

Run `python3 scripts/check.py` to verify local resource paths. For visual changes, review the page at 1510px and 390px, including the header, gallery, footer, and overflow. The initial recreation was checked in the Codex app browser at both sizes.

## Publishing

Changes use a feature branch and pull request. After merge to `main`, `.github/workflows/pages.yml` deploys only `index.html` and `assets/` to GitHub Pages. The content model, reference captures, and project scripts are not included in the deployed page.

## Reference provenance

Original photography, branding, copy, and fonts are retained from the reference site for this requested recreation; they are not newly created assets. Source URLs are documented in `references/asset-sources.json`. The recreated page is marked `noindex` while it is being adapted.
