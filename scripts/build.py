"""Build the editable, dependency-free shop from content/site.json."""
from pathlib import Path
from hashlib import sha256
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
style_version = sha256((ROOT / 'assets/styles.css').read_bytes()).hexdigest()[:12]
data = json.loads((ROOT / 'content/site.json').read_text())
esc = html.escape
css = []
mobile_css = []

def font_scale(value, divisor):
    return re.sub(r'([\d.]+)px', lambda m: f'{float(m[1])/divisor:.6f}cqi', value)

def node_style(node, mode):
    p = node[mode]
    divisor = 12 if mode == 'desktop' else 3.9
    font_divisor = 12 if mode == 'desktop' else 3.2
    selector = '#' + node['id']
    layout = ';'.join(f'{key}:{p[source]/divisor:.6f}cqi' for key, source in [('left','x'),('top','y'),('width','width'),('height','height')])
    result = selector + '{' + layout + '}'
    if node['kind'] == 'text':
        result += selector + ' .copy{' + f'font:{font_scale(p["font"],font_divisor)};letter-spacing:{font_scale(p["letterSpacing"],font_divisor)};text-align:{p["textAlign"]};text-transform:{p["textTransform"]};color:{p["color"]}' + '}'
    return result

def render_section(section):
    sid = section['id']
    section_label = {'preset-packages':'Photo presets','print-shop-gallery-to-darkroom':'Fine art prints','saltybabe-contact':'Get in touch','saltybabe-footer-1':'Footer'}[sid]
    css.append(f'#{sid} .canvas{{aspect-ratio:1200/{section["height"]}}}')
    mobile_css.append(f'#{sid} .canvas{{aspect-ratio:390/{section["mobileHeight"]}}}')
    output = [f'<section id="{sid}" aria-label="{section_label}"><div class="canvas">']
    for node in section['nodes']:
        css.append(node_style(node,'desktop'))
        mobile_css.append(node_style(node,'mobile'))
        attrs = f'id="{node["id"]}" class="element {node["kind"]}"'
        tag = 'a' if node['href'] else 'div'
        if node['href']:
            attrs += f' href="{esc(node["href"],quote=True)}"'
        if node['kind'] == 'image':
            label = node.get('alt','')
            if node['href'] and 'darkroom' in node['href']:
                label += ' — view print ' + node['href'].rsplit('/',1)[-1]
            inner = f'<img src="{esc(node["src"])}" alt="{esc(label)}" decoding="async">'
        elif node['kind'] == 'placeholder':
            attrs += f' role="img" aria-label="{esc(node["alt"])}"'
            inner = f'<span aria-hidden="true">{esc(node["text"])}</span>'
        elif node['kind'] == 'box':
            attrs += ' aria-hidden="true"'
            css.append(f'#{node["id"]}{{background:{node["background"]};border:{node["border"]};pointer-events:none}}')
            inner = ''
            tag = 'div'
        else:
            text_tag = 'h2' if sid=='preset-packages' and node['id'].endswith(('-0','-1')) else 'p'
            inner = f'<{text_tag} class="copy">'+esc(node['text']).replace('\n','<br>')+f'</{text_tag}>'
        output.append(f'<{tag} {attrs}>{inner}</{tag}>')
    output.append('</div></section>')
    return '\n'.join(output)

nav = ''.join(f'<a href="{esc(item["href"])}">{esc(item["label"])}</a>' for item in data['navigation'])
social = ''.join(f'<a href="{esc(item["href"])}" aria-label="{label}">{item["svg"]}</a>' for item,label in zip(data['social'],['Instagram','Pinterest','TikTok']))
sections = {s['id']:render_section(s) for s in data['sections']}
strip = ''.join(f'<div class="gallery-photo"><img src="{esc(photo["src"])}" alt="{esc(photo["alt"])}" decoding="async"></div>' for photo in data['footerPhotos'])
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="description" content="Salty Babe photography shop recreation: ocean presets and fine art prints.">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self'; font-src 'self'; style-src 'self'; script-src 'self'; connect-src 'none'; object-src 'none'; frame-src 'none'; base-uri 'self'; form-action 'none'">
<title>Salty Babe Shop</title>
<link rel="stylesheet" href="assets/fonts.css">
<link rel="stylesheet" href="assets/styles.css?v={style_version}">
<link rel="stylesheet" href="assets/layout.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to shop</a>
<nav class="mobile-nav" aria-label="Mobile navigation">
<details class="mobile-menu">
<summary aria-label="Menu"><svg class="menu-icon" viewBox="0 0 50 32" aria-hidden="true"><path d="M0 1h50M0 16h50M0 31h50"></path></svg><span class="menu-label" aria-hidden="true">menu</span></summary>
<div class="mobile-menu-links">{nav}</div>
</details>
<a class="mobile-inquire" href="{esc(data['navigation'][-1]['href'])}">Inquire<svg viewBox="0 0 32 20" aria-hidden="true"><path d="M1 10h29M22 2l8 8-8 8"></path></svg></a>
</nav>
<header class="masthead">
<p class="tagline">underwater<br>photographer</p>
<a class="header-brand" href="./"><span class="wordmark">SALTY BABE</span><span class="photo-co">PHOTO CO</span></a>
<div class="social-links">{social}</div>
</header>
<nav class="site-nav" aria-label="Main navigation"><div>{nav}</div></nav>
<main id="main">
<section class="hero" aria-label="Shop and collection">
<img class="hero-photo" src="assets/images/group_8_4.png" alt="Snorkeler swimming with sharks in clear blue ocean water" fetchpriority="high">
<h1>Dive In</h1>
<p>Shop &amp; Collection</p>
<a class="dive-arrow" href="#preset-packages" aria-label="Explore photo presets"><img src="assets/images/icons8-down-arrow-100_1.png" alt=""></a>
</section>
{sections['preset-packages']}
{sections['print-shop-gallery-to-darkroom']}
{sections['saltybabe-contact']}
<div class="social-spacer"></div>
<div class="instagram-strip" role="group" aria-label="Photography collection"><div>{strip}</div></div>
</main>
<footer>{sections['saltybabe-footer-1']}</footer>
<script src="assets/mobile-menu.js" defer></script>
</body>
</html>
'''
(ROOT/'index.html').write_text(page)
(ROOT/'assets/layout.css').write_text('/* Generated by scripts/build.py from the editable content file. */\n'+'\n'.join(css)+'\n@media(max-width:767px){\n'+'\n'.join(mobile_css)+'\n}\n')
print(f'Built index.html and layout.css with {len(data["sections"])} sections.')
