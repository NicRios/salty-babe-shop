"""Check that published resources exist locally and links remain explicit."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json,re
root=Path(__file__).resolve().parents[1]
errors=[]
class Page(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  resource=a.get('src') if tag in ('img','script','video','audio','source','iframe') else a.get('href') if tag=='link' else None
  if resource:
   if urlparse(resource).scheme or resource.startswith('//'): errors.append('External resource: '+resource)
   elif not (root/resource.split('#')[0].split('?')[0]).is_file(): errors.append('Missing resource: '+resource)
  if tag=='a' and not a.get('href'):errors.append('Link without destination')
Page().feed((root/'index.html').read_text())
for css in (root/'assets').glob('*.css'):
 text=css.read_text()
 for value in re.findall(r'url\(([^)]+)\)',text):
  path=value.strip('\"\' ')
  if urlparse(path).scheme or path.startswith('//'):errors.append('External CSS resource: '+path)
  elif not (css.parent/path).is_file():errors.append('Missing CSS resource: '+path)
 if re.search(r'@import',text):errors.append('Unexpected stylesheet import: '+str(css))
site=json.loads((root/'content/site.json').read_text())
for section in site['sections']:
 for node in section['nodes']:
  if node['kind']=='image' and not (root/node['src']).is_file():errors.append('Missing content image: '+node['src'])
for error in errors: print(error)
if errors:raise SystemExit(1)
print('PASS: Every image, font, script and stylesheet resolves locally; content images and link destinations are present.')
