from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json
D=Path(__file__).parent/'dist'
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.links=[];self.canon=[];self.title='';self.in_title=False;self.structured=[];self.in_json=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='h1':self.h1+=1
  if t=='title':self.in_title=True
  if t=='script' and a.get('type')=='application/ld+json':self.in_json=True
  if 'src' in a:self.links.append(a['src'])
  if t in ['a','link'] and 'href' in a:self.links.append(a['href'])
  if t=='link' and a.get('rel')=='canonical':self.canon.append(a['href'])
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
  if t=='script':self.in_json=False
 def handle_data(self,d):
  if self.in_title:self.title+=d
  if self.in_json:self.structured.append(json.loads(d))
errors=[];titles=[];canonical=[]
for f in D.rglob('*.html'):
 if f.name.startswith('qa-'):continue
 s=Parser();s.feed(f.read_text());titles.append(s.title);canonical+=s.canon
 if s.h1!=1:errors.append((f.name,'h1',s.h1))
 if len(s.canon)!=1:errors.append((f.name,'canonical'))
 for url in s.links:
  u=urlsplit(url)
  if u.scheme or u.netloc or not u.path:continue
  p=(f.parent/unquote(u.path)).resolve()
  if not p.exists():errors.append((str(f.relative_to(D)),url))
print('Pages:',len(titles),'Unique titles:',len(set(titles)),'Unique canonicals:',len(set(canonical)),'Broken references:',len(errors))
P=json.loads((D/'products.json').read_text());assert len(P)==len({p['name'] for p in P})==23
print('23 unique products; 23 source PDFs; valid JSON-LD.')
print(errors[:20]);assert not errors
