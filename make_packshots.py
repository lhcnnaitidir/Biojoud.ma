from pathlib import Path
import json,base64,html,textwrap
from PIL import Image
from io import BytesIO
D=Path(__file__).parent/'dist'; A=D/'assets'; O=A/'packshots-original';O.mkdir(exist_ok=True)
# Reuse the supplied artwork. The two clipping regions omit only the tagline.
im=Image.open(A/'logo-original.png');buf=BytesIO();im.thumbnail((1073,366));im.save(buf,format='WEBP',quality=96);uri='data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()
logo=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 30 1073 315"><defs><clipPath id="mark"><rect x="0" y="0" width="291" height="366"/><rect x="289" y="0" width="784" height="248"/></clipPath></defs><image href="{uri}" width="1073" height="366" clip-path="url(#mark)"/></svg>'
(A/'logo-wordmark.svg').write_text(logo)
P=json.loads((D/'products.json').read_text());esc=lambda x:html.escape(x,quote=True)
colors={'Nutrition du sol':'#45682f','Nutrition végétale':'#678326','Biostimulation':'#21775e','Protection des cultures':'#536852','Adjuvants':'#9a7924'}
def lines(text,width):return textwrap.wrap(text,width=width,break_long_words=False,break_on_hyphens=False)
def text_lines(text,y,size,width,color='#214534',weight='400'):
 ls=lines(text,width)
 return ''.join(f'<text x="220" y="{y+i*(size*1.3)}" text-anchor="middle" fill="{color}" font-size="{size}" font-weight="{weight}">{esc(t)}</text>' for i,t in enumerate(ls))
for p in P:
 c=colors[p['cat']];isbag=p['package']=='bag';isbottle=p['package']=='bottle'
 defs='''<defs><linearGradient id="plastic" x1="0" x2="1"><stop stop-color="#ced3cb"/><stop offset=".12" stop-color="#f7f8f2"/><stop offset=".5" stop-color="#fffef9"/><stop offset=".85" stop-color="#eeefe9"/><stop offset="1" stop-color="#c7cec2"/></linearGradient><linearGradient id="cap" x1="0" x2="1"><stop stop-color="#113f2a"/><stop offset=".5" stop-color="#356a44"/><stop offset="1" stop-color="#123523"/></linearGradient><linearGradient id="paper" x1="0" x2="1"><stop stop-color="#edece2"/><stop offset=".17" stop-color="#fffef8"/><stop offset=".85" stop-color="#f9f8f0"/><stop offset="1" stop-color="#dcdfd2"/></linearGradient><filter id="shadow" x="-30%" y="-50%" width="160%" height="200%"><feGaussianBlur stdDeviation="8"/></filter><mask id="bodymask"><rect width="440" height="560" fill="white"/><rect x="227" y="74" width="92" height="36" rx="14" fill="black"/></mask></defs>'''
 if isbag:
  body='''<path d="M73 55 Q220 69 367 55 L352 98 Q369 270 354 458 L366 518 Q220 503 74 518 L86 458 Q70 269 87 98Z" fill="url(#paper)" stroke="#d1d5c9" stroke-width="2"/><path d="M84 65Q220 78 356 65M83 508Q220 496 357 508" fill="none" stroke="#b9c1b1" stroke-width="2" stroke-dasharray="3 2"/><path d="M88 104Q111 296 89 459M352 104Q328 296 352 459" fill="none" stroke="#d9ddcf" stroke-width="3" opacity=".7"/>'''
  label=(100,112,240,355)
 elif isbottle:
  body='''<path d="M170 80H270V125Q275 148 299 173Q313 194 313 221V479Q313 512 284 516H156Q127 512 127 479V221Q127 194 141 173Q165 148 170 125Z" fill="url(#plastic)" stroke="#d2d7cb" stroke-width="2"/><rect x="166" y="53" width="108" height="55" rx="9" fill="url(#cap)"/><path d="M176 61V95M187 61V95M198 61V95M209 61V95M220 61V95M231 61V95M242 61V95M253 61V95M264 61V95" stroke="#6e9268" opacity=".55"/><path d="M143 232V473Q143 492 161 497" fill="none" stroke="white" stroke-width="4" opacity=".7"/>'''
  label=(140,224,160,237)
 else:
  body='''<path d="M120 103Q124 88 141 89H195L220 54Q227 44 245 44H315Q336 44 341 67L353 122Q365 138 365 167V476Q365 515 335 521H105Q75 515 75 476V174Q75 148 92 130Z M241 74H305Q319 74 319 88V96Q319 110 305 110H241Q227 110 227 96V88Q227 74 241 74Z" fill="url(#plastic)" fill-rule="evenodd" stroke="#cbd1c5" stroke-width="2"/><path d="M99 174H341M97 482H343" stroke="#b9c3b4" stroke-width="4" opacity=".6"/><rect x="92" y="187" width="256" height="280" rx="19" fill="none" stroke="#fff" stroke-width="3" opacity=".8"/><rect x="118" y="57" width="78" height="45" rx="9" fill="url(#cap)"/><path d="M126 63V93M137 63V93M148 63V93M159 63V93M170 63V93M181 63V93M189 63V93" stroke="#83a576" opacity=".45"/>'''
  label=(103,198,234,257)
 x,y,w,h=label
 # Fit the complete supplied PDF artwork to the front face, preserving its aspect ratio.
 # No text substitution, crop, perspective warp or stretch is applied to the label.
 original=D/p['label']; original_image=Image.open(original);iw,ih=original_image.size
 scale=min(w/iw,h/ih);fw,fh=iw*scale,ih*scale;lx=x+(w-fw)/2;ly=y+(h-fh)/2
 label_uri='data:image/webp;base64,'+base64.b64encode(original.read_bytes()).decode()
 content=f'<rect x="{lx:.3f}" y="{ly:.3f}" width="{fw:.3f}" height="{fh:.3f}" fill="#fffdf6" stroke="#d1d6c8" stroke-width=".7"/><image x="{lx:.3f}" y="{ly:.3f}" width="{fw:.3f}" height="{fh:.3f}" href="{label_uri}" preserveAspectRatio="xMidYMid meet"/>'
 assert lx>=x-.001 and ly>=y-.001 and lx+fw<=x+w+.001 and ly+fh<=y+h+.001
 assert abs(fw/fh-iw/ih)<.0001
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="440" height="560" viewBox="0 0 440 560"><title>{esc(p["name"])} — présentation BIOJOUD</title>{defs}<ellipse cx="220" cy="535" rx="137" ry="10" fill="#204830" opacity=".12" filter="url(#shadow)"/>{body}{content}</svg>'
 (O/(p['slug']+'.svg')).write_text(svg);p['packshot']='assets/packshots-original/'+p['slug']+'.webp'
(D/'products.json').write_text(json.dumps(P,ensure_ascii=False,indent=2))
print('23 original PDF labels placed without cropping or distortion.')

# Raster output avoids SVG decoder differences across browsers and keeps dimensions fixed.
import cairosvg
for source in O.glob('*.svg'):
 rendered=cairosvg.svg2png(url=str(source),output_width=880,output_height=1120)
 Image.open(BytesIO(rendered)).save(source.with_suffix('.webp'),quality=94)
