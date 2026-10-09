"""Outline the site's local typefaces into portable SVG wordmarks.
Requires fonttools and brotli; no fonts or code are fetched by the preview.
"""
from pathlib import Path
from html import escape
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.varLib.instancer import instantiateVariableFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
serif = TTFont(ROOT / 'assets/fonts/noiretblanc-webfont.woff')
sans = instantiateVariableFont(TTFont(ROOT / 'assets/fonts/josefin-sans-2.woff2'), {'wght': 600})

def line(text, font, cap_height, tracking=0):
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    h = BoundsPen(glyphs)
    glyphs[cmap[ord('H')]].draw(h)
    scale = cap_height / (h.bounds[3] - h.bounds[1])
    cursor, shapes, boxes = 0, [], []
    for char in text:
        name = cmap[ord(char)]
        path, bounds = SVGPathPen(glyphs), BoundsPen(glyphs)
        glyphs[name].draw(path)
        glyphs[name].draw(bounds)
        if bounds.bounds:
            x0, y0, x1, y1 = bounds.bounds
            boxes.append((cursor+x0*scale, y0*scale, cursor+x1*scale, y1*scale))
            shapes.append((cursor, path.getCommands()))
        cursor += font['hmtx'][name][0]*scale + tracking
    box = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
    return {'shapes':shapes,'box':box,'scale':scale,'width':box[2]-box[0],'height':box[3]-box[1]}

def draw(row, x, y):
    x0, _, _, y1 = row['box']
    return ''.join(f'<path transform="translate({x+cursor-x0:.4f} {y+y1:.4f}) scale({row["scale"]:.7f} {-row["scale"]:.7f})" d="{d}"/>' for cursor,d in row['shapes'])

def export(name, title, rows, gap, subtitle_gap, subtitle_height, subtitle_tracking):
    subtitle = line('PHOTO CO', sans, subtitle_height, subtitle_tracking)
    width = max(row['width'] for row in rows)
    pad = 42
    height = sum(row['height'] for row in rows) + gap*(len(rows)-1) + subtitle_gap + subtitle['height']
    shapes, y = [], pad
    for row in rows:
        shapes.append(draw(row, pad+(width-row['width'])/2, y))
        y += row['height'] + gap
    y += subtitle_gap-gap
    shapes.append(draw(subtitle, pad+(width-subtitle['width'])/2, y))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width+2*pad:.4f} {height+2*pad:.4f}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<g fill="#111111">{''.join(shapes)}</g>
</svg>\n'''
    (HERE/name).write_text(svg)
    print(name, f'{width+2*pad:.1f} x {height+2*pad:.1f}')

export('salty-babe-horizontal.svg','Salty Babe Photo Co — horizontal logo',[line('SALTY BABE',serif,180)],0,34,19,9)
first, second = line('SALTY',serif,160), line('BABE',serif,160)
width = max(first['width'],second['width'])
first = line('SALTY',serif,160,(width-first['width'])/4)
second = line('BABE',serif,160,(width-second['width'])/3)
export('salty-babe-stacked.svg','Salty Babe Photo Co — stacked logo',[first,second],13,31,17,8)
