#!/usr/bin/env python3
from pathlib import Path
import json, shutil, html
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'src'; DIST=ROOT/'dist'; DOMAIN='https://kazanamazihesapla.com'

# Curated internal-link graph: each page links only to the most relevant next steps.
RELATED_MAP={
 'kaza-namazi-nasil-kilinir':['kaza-namazi-niyeti','kaza-namazi-kac-rekat','kaza-namazi-ne-zaman-kilinir','kaza-namazi-ne-zaman-kilinmaz'],
 'kaza-namazi-ne-zaman-kilinir':['kaza-namazi-ne-zaman-kilinmaz','kaza-namazi-nasil-kilinir','kaza-namazi-niyeti','kaza-namazi-bitirme-plani'],
 'kaza-namazi-ne-zaman-kilinmaz':['kaza-namazi-ne-zaman-kilinir','kaza-namazi-nasil-kilinir','kaza-namazi-niyeti'],
 'kaza-namazi-niyeti':['kaza-namazi-nasil-kilinir','kaza-namazi-kac-rekat','kaza-namazi-ne-zaman-kilinir'],
 'kaza-namazi-kac-rekat':['kaza-namazi-nasil-kilinir','kaza-namazi-niyeti','kaza-namazi-nasil-hesaplanir'],
 'kaza-namazi-nasil-hesaplanir':['kadinlar-icin-kaza-namazi-hesaplama','erkekler-icin-kaza-namazi-hesaplama','kaza-namazi-bitirme-plani','kaza-namazi-cizelgesi'],
 'kadinlar-icin-kaza-namazi-hesaplama':['kaza-namazi-nasil-hesaplanir','kaza-namazi-bitirme-plani','kaza-namazi-cizelgesi'],
 'erkekler-icin-kaza-namazi-hesaplama':['kaza-namazi-nasil-hesaplanir','kaza-namazi-bitirme-plani','kaza-namazi-cizelgesi'],
 'kaza-namazi-cizelgesi':['kaza-namazi-bitirme-plani','kaza-namazi-nasil-hesaplanir','kadinlar-icin-kaza-namazi-hesaplama','erkekler-icin-kaza-namazi-hesaplama'],
 'kaza-namazi-bitirme-plani':['kaza-namazi-cizelgesi','kaza-namazi-nasil-hesaplanir','kaza-namazi-ne-zaman-kilinir'],
}
ANCHORS={
 'kaza-namazi-nasil-kilinir':'Kaza namazı nasıl kılınır?',
 'kaza-namazi-ne-zaman-kilinir':'Kaza namazı ne zaman kılınır?',
 'kaza-namazi-ne-zaman-kilinmaz':'Kaza namazı ne zaman kılınmaz?',
 'kaza-namazi-niyeti':'Kaza namazına niyet etme rehberi',
 'kaza-namazi-kac-rekat':'Vakitlere göre rekât sayıları',
 'kaza-namazi-nasil-hesaplanir':'Kaza namazı nasıl hesaplanır?',
 'kadinlar-icin-kaza-namazi-hesaplama':'Kadınlar için hesaplama rehberi',
 'erkekler-icin-kaza-namazi-hesaplama':'Erkekler için hesaplama rehberi',
 'kaza-namazi-cizelgesi':'Kaza namazı takip çizelgesi',
 'kaza-namazi-bitirme-plani':'Kaza namazı bitirme planı',
}

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
  content=p.get('content_html') or ''.join(f'<h2>{html.escape(h)}</h2><p>{html.escape(b)}</p>' for h,b in p['sections'])
  page_by_slug={x['slug']:x for x in pages}
  rel_slugs=RELATED_MAP.get(p['slug'],[])
  related=''.join(f'<a href="/{slug}/">{html.escape(ANCHORS.get(slug,page_by_slug[slug]["title"]))}</a>' for slug in rel_slugs if slug in page_by_slug)
  pathway_cards=''.join(f'<a href="/{slug}/"><strong>{html.escape(ANCHORS.get(slug,page_by_slug[slug]["title"]))}</strong><span>{html.escape(page_by_slug[slug]["description"])}</span></a>' for slug in rel_slugs[:3] if slug in page_by_slug)
  pathways=f'<section class="topic-pathways" aria-labelledby="next-reading"><span class="section-label">SONRAKİ ADIM</span><h2 id="next-reading">Konuyu tamamlayan rehberler</h2><div class="topic-pathway-grid">{pathway_cards}</div></section>'
  schema=json.dumps({'@context':'https://schema.org','@graph':[{'@type':'Article','headline':p['title'],'description':p['description'],'inLanguage':'tr-TR','mainEntityOfPage':DOMAIN+'/'+p['slug']+'/'},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Ana sayfa','item':DOMAIN+'/'},{'@type':'ListItem','position':2,'name':'Rehber','item':DOMAIN+'/rehber/'},{'@type':'ListItem','position':3,'name':p['title'],'item':DOMAIN+'/'+p['slug']+'/'}]}]},ensure_ascii=False)
  out=render(at,{'TITLE':html.escape(p['title']),'DESCRIPTION':html.escape(p['description']),'SLUG':p['slug'],'H1':html.escape(p['h1']),'INTRO':html.escape(p['intro']),'CONTENT':content,'RELATED':related,'PATHWAYS':pathways,'SCHEMA':schema,'FOOTER':footer()})
  d=DIST/p['slug']; d.mkdir(); (d/'index.html').write_text(out,encoding='utf-8'); urls.append(DOMAIN+'/'+p['slug']+'/')
  cards.append(f'<a class="guide-card" href="/{p["slug"]}/"><h2>{html.escape(p["title"])}</h2><p>{html.escape(p["description"])}</p></a>')
 years=[1,5,10,15,20,30]
 for y in years:
  days=round(y*365.2425); prayers=days*5; rakats=days*17
  idx=years.index(y); nearby=[]
  for pos in (idx-1,idx+1,idx-2,idx+2):
   if 0<=pos<len(years) and years[pos] not in nearby: nearby.append(years[pos])
  rel=''.join(f'<a href="/{x}-yillik-kaza-namazi-hesaplama/">{x} yıllık kaza namazı hesabı</a>' for x in nearby)
  guide_paths='<section class="topic-pathways" aria-labelledby="year-next-reading"><span class="section-label">HESABI PLANLA</span><h2 id="year-next-reading">Sonucunuzu uygulanabilir bir plana dönüştürün</h2><div class="topic-pathway-grid"><a href="/kaza-namazi-nasil-hesaplanir/"><strong>Hesaplama yöntemini öğrenin</strong><span>Eksik gün, vakit ve muafiyet hesabının ayrıntılarını inceleyin.</span></a><a href="/kaza-namazi-bitirme-plani/"><strong>Günlük bitirme planı oluşturun</strong><span>Günlük hedefinize göre sürdürülebilir bir program hazırlayın.</span></a><a href="/kaza-namazi-cizelgesi/"><strong>Takip çizelgesini kullanın</strong><span>Hedef ve tamamlanan vakitleri düzenli olarak kaydedin.</span></a></div></section>'
  schema=json.dumps({'@context':'https://schema.org','@graph':[{'@type':'WebPage','name':f'{y} Yıllık Kaza Namazı Hesaplama','url':f'{DOMAIN}/{y}-yillik-kaza-namazi-hesaplama/'},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Ana sayfa','item':DOMAIN+'/'},{'@type':'ListItem','position':2,'name':'Yıl bazlı hesaplamalar','item':DOMAIN+'/#yil-hesaplari'},{'@type':'ListItem','position':3,'name':f'{y} yıllık hesaplama','item':f'{DOMAIN}/{y}-yillik-kaza-namazi-hesaplama/'}]}]},ensure_ascii=False)
  vals={'YEAR':y,'DAYS':nf(days),'PRAYERS':nf(prayers),'RAKATS':nf(rakats),'DURATION':duration(prayers/5),'D1':duration(prayers),'D5':duration(prayers/5),'D10':duration(prayers/10),'RELATED':rel,'GUIDE_PATHS':guide_paths,'SCHEMA':schema,'FOOTER':footer()}
  d=DIST/f'{y}-yillik-kaza-namazi-hesaplama'; d.mkdir(); (d/'index.html').write_text(render(yt,vals),encoding='utf-8'); urls.append(f'{DOMAIN}/{y}-yillik-kaza-namazi-hesaplama/')
 d=DIST/'rehber'; d.mkdir(); (d/'index.html').write_text(render(gt,{'CARDS':''.join(cards),'FOOTER':footer()}),encoding='utf-8')
 (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(f'<url><loc>{u}</loc><lastmod>2026-08-03</lastmod></url>' for u in urls)+'\n</urlset>',encoding='utf-8')
 print(f'Build tamamlandı: {len(pages)} rehber, {len(years)} yıl sayfası, toplam {len(urls)} URL')
if __name__=='__main__': main()
