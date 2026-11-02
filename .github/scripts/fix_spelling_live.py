"""One-off: find the channel messages behind post files that used the old
Persian spelling (from the Telegram workflow's own logs) and edit them in place."""
import io, json, os, re, sys, urllib.request, urllib.error, zipfile, urllib.parse, time
REPO=os.environ['REPO']; GH=os.environ['GH_TOKEN']; CHAT=os.environ['CHAT_ID']
m=re.search(r'[0-9]{6,}:[A-Za-z0-9_-]{30,}',os.environ['TG_TOKEN']); TG=m.group(0)
files=[l.strip() for l in open('.github/scripts/fix_spelling_files.txt') if l.strip()]
def gh(path,raw=False):
    r=urllib.request.Request('https://api.github.com'+path,headers={'Authorization':'Bearer '+GH,'Accept':'application/vnd.github+json'})
    return (lambda b: b if raw else json.loads(b))(urllib.request.urlopen(r).read())
def tg(method,**p):
    d=json.dumps(p).encode(); r=urllib.request.Request(f'https://api.telegram.org/bot{TG}/{method}',d,{'Content-Type':'application/json'})
    try: return json.loads(urllib.request.urlopen(r).read())
    except urllib.error.HTTPError as e: return json.loads(e.read())
ids={}
page=1
while True:
    runs=gh(f'/repos/{REPO}/actions/workflows/telegram.yml/runs?per_page=100&page={page}')['workflow_runs']
    if not runs: break
    for run in runs:
        try: z=zipfile.ZipFile(io.BytesIO(gh(f"/repos/{REPO}/actions/runs/{run['id']}/logs",raw=True)))
        except Exception as e: continue
        for n in z.namelist():
            if '/' in n: continue          # top-level combined job logs only
            cur=None
            for line in z.read(n).decode('utf8','replace').splitlines():
                s=re.search(r'Sending (telegram/\S+\.md)',line)
                if s and 'echo' not in line: cur=s.group(1); ids.setdefault(cur,[]); continue
                s=re.search(r'"message_id":\s*(\d+)',line)
                if s and cur: ids[cur].append(int(s.group(1)))
    page+=1
out={}
for f in files:
    raw=open(f,encoding='utf8').read().rstrip('\n'); lines=raw.split('\n'); image=False
    if lines[0].startswith('image:'):
        image=True; text='\n'.join(lines[1:]).lstrip('\n')
    else: text=raw
    got=sorted(set(ids.get(f,[]))); res=[]
    if not got: out[f]={'status':'no message id in logs'}; continue
    for mid in got:
        if image and len(text)<=1000:
            r=tg('editMessageCaption',chat_id=CHAT,message_id=mid,caption=text)
        else:
            p=dict(chat_id=CHAT,message_id=mid,text=text)
            if image: p['link_preview_options']={'is_disabled':True}
            r=tg('editMessageText',**p)
        res.append({'id':mid,'ok':r.get('ok'),'err':r.get('description')})
        time.sleep(1.2)
    out[f]=res
c=tg('getChat',chat_id=CHAT).get('result',{})
out['_channel']={'title':c.get('title'),'description':c.get('description')}
json.dump(out,open('market/spelling-fix-result.json','w'),ensure_ascii=False,indent=1)
