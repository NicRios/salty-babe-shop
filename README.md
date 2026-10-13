# Salty Babe Shop recreation

Editable recreation of [availethphoto.com/salty-babe-shop](https://availethphoto.com/salty-babe-shop), captured October 8, 2026, with the Ocean Glow and Sun & Sand product pages captured October 12. Purchases continue to the original Stripe checkout links.

- **Live page:** https://nicrios.github.io/salty-babe-shop/
- **Local preview:** `python3 -m http.server 4174 --bind 127.0.0.1`
- **Desktop reference:** `references/salty-babe-desktop-1510.jpg` (1510 × 1000 viewport, full page)
- **Mobile reference:** `references/salty-babe-mobile-390.jpg` (390 × 844 viewport, full page)

## Editing

Text, image paths, links, and the original desktop/mobile positions live in `content/site.json`. Rebuild the HTML and position rules with `python3 scripts/build.py`. The masthead, navigation and hero are in that script's template; their styles live in `assets/styles.css`. At widths through 767px, a menu and Inquire link sit above the logo; the menu contains Home, Photo Presets, Print Shop and Inquire. Tablet and desktop retain their four-link navigation. Presets and prints jump to their page sections; Inquire retains the original contact destination. The native disclosure menu works without JavaScript; the local `assets/mobile-menu.js` closes it on link selection, outside clicks, Escape, and a switch to a wider layout. The six-photo strip above the footer is controlled by `footerPhotos`: six columns on desktop and three columns by two rows at 1024px and below. The supplied photos are stored locally as optimized WebP files; the separate footer portrait uses its original local image.

Photographs and decorative images are in `assets/images/`; all fonts are in `assets/fonts/`. No scripts, CSS, fonts, images, analytics, or embeds load from another host. A Content Security Policy enforces same-origin resources. Shop buttons open the local product pages; their purchase links retain the original checkout destinations.

Product copy and comparison photographs are configured in `content/products.json`, with their original source URLs recorded there. The pages are `shop-product-ocean-glow.html` and `sun-and-sand.html`; their responsive layout is in `assets/products.css`. Both use the same generated masthead, navigation, six-photo strip and footer as the index. Product navigation returns Home, Photo Presets and Print Shop to the index; mobile displays the title and first two comparison images before the description, purchase button and remaining photographs. The copied pages end at the shared footer, without the original Ocean Glow page's trailing blank space. Sun & Sand retains the contact section.

The masthead and footer use the supplied transparent `salty babe logo (1).png`, copied unchanged to `assets/images/salty-babe-logo.png` (1158 × 555). The lettering and subtitle are one image, preserving the approved spacing and natural aspect ratio. In the desktop footer, the logo and photographer tagline are centered together between the photo and menu panels; the earlier starfish is removed.

The footer background uses the accepted seashell brand artwork from the portfolio case study, copied unchanged into `assets/images/`: `sbs-shell-pattern-wide.png` for desktop/tablet and the supplied portrait `sbs-shell-pattern.jpg` for mobile. The artwork appears at its original opacity, without a transparency adjustment.

The desktop navigation spans a centered 70% of the viewport with equal gaps between its four semibold links. Mobile menu links use the same semibold weight.

The two preset purchase buttons and Contact Me use a shared action-button style: menu green `#909683`, white lettering, matching type and border treatment, and horizontally and vertically centered labels. Each is one full clickable link instead of separate text and outline layers. The navigation styles are independent.

The desktop/tablet hero uses `hero-desktop-centered-photo.png` (1586 × 992), with a 2:1 `hero-desktop-wide-centered-photo.png` (1774 × 887) at 2000px and above. These are AI-refined versions of the existing hero photographs, made with the built-in image generation tool to improve photographic detail and center the swimmer; the exact prompts are in `references/hero-photo-refinement-prompts.txt`. CSS scales each photograph to 105% of its cover size and aligns the subject's horizontal center with the frame center. At desktop and tablet widths, the heading, subtitle, and arrow form one group centered horizontally and positioned 5px above the hero's vertical center, keeping their existing type sizes and 12px/16px gaps. The hero frame, wave, and mobile photograph and text retain their existing layout. Earlier hero assets are preserved.

The contact section and footer scale together within their own canvases: up to 390px wide in the stacked layout (through 767px viewport width), then up to the existing 1200px desktop canvas. This caps their type, artwork, controls and spacing without changing the navigation or gallery.

Run `python3 scripts/check.py` to verify local resource paths. For visual changes, review the page at 1510px and 390px, including the header, gallery, footer, and overflow. The initial recreation was checked in the Codex app browser at both sizes.

## Publishing

Changes use a feature branch and pull request. After merge to `main`, `.github/workflows/pages.yml` deploys `index.html`, both product HTML files and `assets/` to GitHub Pages. The content model, reference captures, and project scripts are not included in the deployed pages.

## Reference provenance

Original photography, branding, copy, and fonts are retained from the reference site for this requested recreation; they are not newly created assets. Source URLs are documented in `references/asset-sources.json`. The recreated page is marked `noindex` while it is being adapted.
