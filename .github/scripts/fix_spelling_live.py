"""One-off: restore the large image preview on older posts, and fix the welcome post."""
import json, os, re, time, urllib.request, urllib.error
CHAT=os.environ['CHAT_ID']; TG=re.search(r'[0-9]{6,}:[A-Za-z0-9_-]{30,}',os.environ['TG_TOKEN']).group(0)
def tg(method,**p):
    d=json.dumps(p).encode(); r=urllib.request.Request(f'https://api.telegram.org/bot{TG}/{method}',d,{'Content-Type':'application/json'})
    try: return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e: return json.loads(e.read())
out={}
for mid,f in [(28,'2026-10-29-03-welcome'),(29,'2026-10-29-04-dtcc'),(33,'2026-10-29-06-google500b'),(34,'2026-10-30-01-binance-hack'),(41,'2026-10-30-04-tokenised-money')]:
    lines=open(f'telegram/{f}.md',encoding='utf8').read().rstrip('\n').split('\n')
    image=lines[0].split(':',1)[1].strip(); text='\n'.join(lines[1:]).lstrip('\n')
    r=tg('editMessageText',chat_id=CHAT,message_id=mid,text=text,link_preview_options={'url':f'https://ditoman.com/{image}?v=spell1','prefer_large_media':True,'show_above_text':True})
    res=r.get('result') or {}
    out[f]={'id':mid,'ok':r.get('ok'),'err':r.get('description'),'preview':res.get('link_preview_options')}
    time.sleep(1.5)
json.dump(out,open('market/spelling-fix-result-2.json','w'),ensure_ascii=False,indent=1)
