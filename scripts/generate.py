#!/usr/bin/env python3
from pathlib import Path
import json, shutil, html
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'src'; DIST=ROOT/'dist'; DOMAIN='https://kazanamazihesaplama.com'
def render(t,v):
 for k,x in v.items(): t=t.replace('{{'+k+'}}',str(x))
 return t
def nf(n): return f'{int(round(n)):,}'.replace(',','.')
def duration(days):
 y=int(days//365.2425); m=int((days-y*365.2425)//30.44)
 return ' '.join(x for x in [f'{y} yıl' if y else '',f'{m} ay' if m else ''] if x) or f'{int(days)} gün'
def footer(): return '<footer><div class="container footer-grid"><div><strong>Kaza Namazı Hesaplama</strong><p>Yaklaşık hesaplama ve sürdürülebilir bitirme planı.</p></div><div><strong>Rehber</strong><a href="/kaza-namazi-nasil-kilinir/">Nasıl kılınır?</a><a href="/kaza-namazi-niyeti/">Niyet</a><a href="/kaza-namazi-kac-rekat/">Kaç rekât?</a></div><div><strong>Site</strong><a href="/rehber/">Tüm rehberler</a><a href="/metodoloji.html">Metodoloji</a><a href="/gizlilik.html">Gizlilik</a></div></div></footer>'
def main():
 if DIST.exists(): shutil.rmtree(DIST)
 shutil.copytree(SRC/'site',DIST)
 pages=json.loads((SRC/'data/pages.json').read_text(encoding='utf-8'))
 at=(SRC/'templates/article.template.html').read_text(encoding='utf-8'); yt=(SRC/'templates/year.template.html').read_text(encoding='utf-8'); gt=(SRC/'templates/guide-index.template.html').read_text(encoding='utf-8')
 cards=[]; urls=[DOMAIN+'/',DOMAIN+'/gizlilik.html',DOMAIN+'/metodoloji.html',DOMAIN+'/rehber/']
 for p in pages:
  content=''.join(f'<h2>{html.escape(h)}</h2><p>{html.escape(b)}</p>' for h,b in p['sections'])
  related=''.join(f'<a href="/{x["slug"]}/">{html.escape(x["title"])}</a>' for x in pages if x['slug']!=p['slug'])
  schema=json.dumps({'@context':'https://schema.org','@type':'Article','headline':p['title'],'description':p['description'],'inLanguage':'tr-TR','mainEntityOfPage':DOMAIN+'/'+p['slug']+'/'},ensure_ascii=False)
  out=render(at,{'TITLE':html.escape(p['title']),'DESCRIPTION':html.escape(p['description']),'SLUG':p['slug'],'H1':html.escape(p['h1']),'INTRO':html.escape(p['intro']),'CONTENT':content,'RELATED':related,'SCHEMA':schema,'FOOTER':footer()})
  d=DIST/p['slug']; d.mkdir(); (d/'index.html').write_text(out,encoding='utf-8'); urls.append(DOMAIN+'/'+p['slug']+'/')
  cards.append(f'<a class="guide-card" href="/{p["slug"]}/"><h2>{html.escape(p["title"])}</h2><p>{html.escape(p["description"])}</p></a>')
 years=[1,5,10,15,20,30]
 for y in years:
  days=round(y*365.2425); prayers=days*5; rakats=days*17
  rel=''.join(f'<a href="/{x}-yillik-kaza-namazi-hesaplama/">{x} yıllık hesaplama</a>' for x in years if x!=y)
  schema=json.dumps({'@context':'https://schema.org','@type':'WebPage','name':f'{y} Yıllık Kaza Namazı Hesaplama','url':f'{DOMAIN}/{y}-yillik-kaza-namazi-hesaplama/'},ensure_ascii=False)
  vals={'YEAR':y,'DAYS':nf(days),'PRAYERS':nf(prayers),'RAKATS':nf(rakats),'DURATION':duration(prayers/5),'D1':duration(prayers),'D5':duration(prayers/5),'D10':duration(prayers/10),'RELATED':rel,'SCHEMA':schema,'FOOTER':footer()}
  d=DIST/f'{y}-yillik-kaza-namazi-hesaplama'; d.mkdir(); (d/'index.html').write_text(render(yt,vals),encoding='utf-8'); urls.append(f'{DOMAIN}/{y}-yillik-kaza-namazi-hesaplama/')
 d=DIST/'rehber'; d.mkdir(); (d/'index.html').write_text(render(gt,{'CARDS':''.join(cards),'FOOTER':footer()}),encoding='utf-8')
 (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(f'<url><loc>{u}</loc><lastmod>2026-08-03</lastmod></url>' for u in urls)+'\n</urlset>',encoding='utf-8')
 print(f'Build tamamlandı: {len(pages)} rehber, {len(years)} yıl sayfası, toplam {len(urls)} URL')
if __name__=='__main__': main()
