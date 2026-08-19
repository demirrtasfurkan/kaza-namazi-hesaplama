#!/usr/bin/env python3
from pathlib import Path
import json, shutil, html, re
from markdown_renderer import render_markdown
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'src'; DIST=ROOT/'dist'; DOMAIN='https://kazanamazihesapla.com'
def render(t,v):
 for k,x in v.items(): t=t.replace('{{'+k+'}}',str(x))
 return t
def nf(n): return f'{int(round(n)):,}'.replace(',','.')
def duration(days):
 y=int(days//365.2425); m=int((days-y*365.2425)//30.44)
 return ' '.join(x for x in [f'{y} yıl' if y else '',f'{m} ay' if m else ''] if x) or f'{int(days)} gün'
def footer(description='Yaklaşık borç hesabı ve sürdürülebilir günlük plan oluşturma aracı.'):
 return '<footer><div class="container footer-grid"><div><strong>Kaza Namazı Hesaplama</strong><p>'+html.escape(description)+'</p></div><div><strong>Rehber</strong><a href="/kaza-namazi-nedir/">Kaza namazı nedir?</a><a href="/kaza-namazi-nasil-kilinir/">Nasıl kılınır?</a><a href="/kaza-namazi-nasil-hesaplanir/">Nasıl hesaplanır?</a></div><div><strong>Site</strong><a href="/rehber/">Tüm rehberler</a><a href="/metodoloji">Metodoloji</a><a href="/gizlilik">Gizlilik</a></div></div></footer>'

def article_content(page):
 body=render_markdown(page.get('content_markdown',''))
 faqs=page.get('faqs') or []
 if faqs:
  details=''.join('<details><summary>'+html.escape(x.get('question',''))+'</summary>'+render_markdown(x.get('answer',''),include_toc=False)+'</details>' for x in faqs)
  body+='<section class="article-faq"><h2>Sık sorulan sorular</h2>'+details+'</section>'
 sources=page.get('sources') or []
 note=page.get('source_note') or ''
 if sources or note:
  links=''.join('<li><a href="'+html.escape(x.get('url',''),quote=True)+'" target="_blank" rel="noopener noreferrer">'+html.escape(x.get('label',''))+'</a></li>' for x in sources)
  body+='<section class="article-sources"><h2>Kaynaklar ve önemli not</h2>'
  if links: body+='<ul>'+links+'</ul>'
  if note: body+='<p>'+html.escape(note)+'</p>'
  body+='</section>'
 return body

def update_homepage(home):
 path=DIST/'index.html'; text=path.read_text(encoding='utf-8')
 def replace(pattern,replacement):
  nonlocal text
  text,count=re.subn(pattern,replacement,text,count=1,flags=re.S)
  if count!=1: raise RuntimeError('Ana sayfa alanı bulunamadı: '+pattern)
 replace(r'<title>.*?</title>','<title>'+html.escape(home['seo_title'])+'</title>')
 replace(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+html.escape(home['meta_description'],quote=True)+'">')
 replace(r'(<h1 class="calculator-page-title">).*?(</h1>)',r'\g<1>'+html.escape(home['h1'])+r'\g<2>')
 faq_items=''.join('<details><summary><h3>'+html.escape(x['question'])+'</h3><span class="faq-icon" aria-hidden="true"></span></summary><p>'+html.escape(x['answer'])+'</p></details>' for x in home.get('faqs',[]))
 faq_section='<section class="content-section" id="sss"><div class="container content-wide"><div class="editorial-body"><h2>'+html.escape(home['faq_heading'])+'</h2>'+faq_items+'</div></div></section>'
 replace(r'<section class="content-section" id="sss">.*?</section>',faq_section)
 faq_schema=json.dumps({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':x['question'],'acceptedAnswer':{'@type':'Answer','text':x['answer']}} for x in home.get('faqs',[])]},ensure_ascii=False)
 replace(r'<script type="application/ld\+json">\{[^\n]*?"FAQPage"[^\n]*?</script>','<script type="application/ld+json">'+faq_schema+'</script>')
 replace(r'(<a class="brand footer-brand".*?</a><p>).*?(</p>)',r'\g<1>'+html.escape(home['footer_description'])+r'\g<2>')
 path.write_text(text,encoding='utf-8')
def main():
 if DIST.exists(): shutil.rmtree(DIST)
 shutil.copytree(SRC/'site',DIST)
 page_data=json.loads((SRC/'data/pages.json').read_text(encoding='utf-8'))
 pages=page_data['pages'] if isinstance(page_data,dict) else page_data
 home=json.loads((SRC/'data/homepage.json').read_text(encoding='utf-8'))
 update_homepage(home)
 at=(SRC/'templates/article.template.html').read_text(encoding='utf-8'); yt=(SRC/'templates/year.template.html').read_text(encoding='utf-8'); gt=(SRC/'templates/guide-index.template.html').read_text(encoding='utf-8')
 cards=[]; urls=[DOMAIN+'/',DOMAIN+'/gizlilik',DOMAIN+'/metodoloji',DOMAIN+'/rehber/']
 for p in pages:
  content=article_content(p)
  related_map={
   'kaza-namazi-nedir':['kaza-namazi-nasil-kilinir','kaza-namazi-nasil-hesaplanir','kaza-namazi-ne-zaman-kilinir','kaza-namazi-kac-rekat'],
   'kaza-namazi-nasil-kilinir':['kaza-namazi-niyeti','kaza-namazi-kac-rekat','kaza-namazi-ne-zaman-kilinir','kaza-namazi-nedir'],
   'kaza-namazi-ne-zaman-kilinir':['kaza-namazi-ne-zaman-kilinmaz','kaza-namazi-nasil-kilinir','kaza-namazi-nedir'],
   'kaza-namazi-ne-zaman-kilinmaz':['kaza-namazi-ne-zaman-kilinir','kaza-namazi-nasil-kilinir','kaza-namazi-nedir'],
   'kaza-namazi-niyeti':['kaza-namazi-nasil-kilinir','kaza-namazi-kac-rekat','kaza-namazi-nedir'],
   'kaza-namazi-kac-rekat':['kaza-namazi-nasil-kilinir','kaza-namazi-niyeti','kaza-namazi-nasil-hesaplanir'],
   'kaza-namazi-nasil-hesaplanir':['kadinlar-icin-kaza-namazi-hesaplama','erkekler-icin-kaza-namazi-hesaplama','kaza-namazi-cizelgesi','kaza-namazi-bitirme-plani'],
   'kadinlar-icin-kaza-namazi-hesaplama':['kaza-namazi-nasil-hesaplanir','kaza-namazi-cizelgesi','kaza-namazi-bitirme-plani'],
   'erkekler-icin-kaza-namazi-hesaplama':['kaza-namazi-nasil-hesaplanir','kaza-namazi-cizelgesi','kaza-namazi-bitirme-plani'],
   'kaza-namazi-cizelgesi':['kaza-namazi-bitirme-plani','kaza-namazi-nasil-hesaplanir','kaza-namazi-nedir'],
   'kaza-namazi-bitirme-plani':['kaza-namazi-cizelgesi','kaza-namazi-nasil-hesaplanir','kaza-namazi-kac-rekat']}
  targets=related_map.get(p['slug'],[])
  related=''.join(f'<a href="/{x["slug"]}/">{html.escape(x["title"])}</a>' for x in pages if x['slug'] in targets)
  schema=json.dumps({'@context':'https://schema.org','@type':'Article','headline':p['title'],'description':p['description'],'inLanguage':'tr-TR','mainEntityOfPage':DOMAIN+'/'+p['slug']+'/'},ensure_ascii=False)
  out=render(at,{'TITLE':html.escape(p['title']),'DESCRIPTION':html.escape(p['description']),'SLUG':p['slug'],'H1':html.escape(p['h1']),'INTRO':html.escape(p['intro']),'CONTENT':content,'RELATED':related,'SCHEMA':schema,'FOOTER':footer(home['footer_description'])})
  d=DIST/p['slug']; d.mkdir(); (d/'index.html').write_text(out,encoding='utf-8'); urls.append(DOMAIN+'/'+p['slug']+'/')
  cards.append(f'<a class="guide-card" href="/{p["slug"]}/"><h2>{html.escape(p["title"])}</h2><p>{html.escape(p["description"])}</p></a>')
 years=[1,5,10,15,20,30]
 for y in years:
  days=round(y*365.2425); prayers=days*5; rakats=days*17
  neighbors={1:[5],5:[1,10],10:[5,15],15:[10,20],20:[15,30],30:[20]}; rel=''.join(f'<a href="/{x}-yillik-kaza-namazi-hesaplama/">{x} yıllık hesaplama</a>' for x in neighbors[y]) + '<a href="/kaza-namazi-nasil-hesaplanir/">Hesaplama yöntemi</a><a href="/kaza-namazi-bitirme-plani/">Bitirme planı</a>'
  schema=json.dumps({'@context':'https://schema.org','@type':'WebPage','name':f'{y} Yıllık Kaza Namazı Hesaplama','url':f'{DOMAIN}/{y}-yillik-kaza-namazi-hesaplama/'},ensure_ascii=False)
  vals={'YEAR':y,'DAYS':nf(days),'PRAYERS':nf(prayers),'RAKATS':nf(rakats),'DURATION':duration(prayers/5),'D1':duration(prayers),'D5':duration(prayers/5),'D10':duration(prayers/10),'RELATED':rel,'SCHEMA':schema,'FOOTER':footer(home['footer_description'])}
  d=DIST/f'{y}-yillik-kaza-namazi-hesaplama'; d.mkdir(); (d/'index.html').write_text(render(yt,vals),encoding='utf-8'); urls.append(f'{DOMAIN}/{y}-yillik-kaza-namazi-hesaplama/')
 d=DIST/'rehber'; d.mkdir(); (d/'index.html').write_text(render(gt,{'CARDS':''.join(cards),'FOOTER':footer(home['footer_description'])}),encoding='utf-8')
 (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(f'<url><loc>{u}</loc><lastmod>2026-08-14</lastmod></url>' for u in urls)+'\n</urlset>',encoding='utf-8')
 print(f'Build tamamlandı: {len(pages)} rehber, {len(years)} yıl sayfası, toplam {len(urls)} URL')
if __name__=='__main__': main()
