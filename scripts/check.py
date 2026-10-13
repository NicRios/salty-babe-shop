"""Check that published resources exist locally and links remain explicit."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json,re
root=Path(__file__).resolve().parents[1]
errors=[]
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__()
  self.path=path
  self.ids=set()
  self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):
   if a['id'] in self.ids:errors.append(f'Duplicate id in {self.path.name}: '+a['id'])
   self.ids.add(a['id'])
  resource=a.get('src') if tag in ('img','script','video','audio','source','iframe') else a.get('href') if tag=='link' else None
  if resource:
   if urlparse(resource).scheme or resource.startswith('//'): errors.append('External resource: '+resource)
   elif not (root/resource.split('#')[0].split('?')[0]).is_file(): errors.append('Missing resource: '+resource)
  if tag=='a' and not a.get('href'):errors.append('Link without destination')
  if tag=='a' and a.get('href'):self.links.append(a['href'])
pages={}
for path in root.glob('*.html'):
 page=Page(path)
 page.feed(path.read_text())
 pages[path.resolve()]=page
for path,page in pages.items():
 for href in page.links:
  url=urlparse(href)
  if url.scheme or url.netloc:continue
  target=(path.parent/unquote(url.path)).resolve() if url.path else path
  if target.is_dir():target=target/'index.html'
  if not target.is_file():errors.append(f'Missing local destination in {path.name}: '+href)
  elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:errors.append(f'Missing anchor in {path.name}: '+href)
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
print(f'PASS: Resources resolve locally across {len(pages)} pages; local destinations, anchors, and unique IDs are valid.')
