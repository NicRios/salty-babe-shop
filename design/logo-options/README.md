# Salty Babe logo options

Open `index.html` through the local site preview to compare the two compositions.

- `salty-babe-horizontal.svg`: Salty Babe on one line, with Photo Co below.
- `salty-babe-stacked.svg`: Salty above Babe, aligned to the same width through tracking, with Photo Co below.

Both use the existing Noir Et Blanc wordmark and Josefin Sans supporting type. All lettering is outlined; the SVG files need no installed fonts or external resources and have transparent backgrounds. These are design options, not an applied homepage change.

`build_logos.py` regenerates the SVGs from the site's local fonts using Python with fonttools and brotli.

## Horizontal color exports

- `salty-babe-black.svg` and `.png`: pure black (#000000), without Photo Co.
- `salty-babe-white.svg` and `.png`: pure white (#FFFFFF), without Photo Co.

The two versions share identical wordmark geometry and transparent backgrounds. PNG files are 3600px wide with an alpha channel. Checkerboards exist only on the comparison page, not in the image files. `export_pngs.cjs` creates and checks the PNGs using Node and sharp.
