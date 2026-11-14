import zipfile,re,glob,html,difflib,unicodedata
z=zipfile.ZipFile('claude/tmp/vellum-export.docx'); x=z.read('word/document.xml').decode('utf-8')
paras=re.findall(r'<w:p[ >].*?</w:p>',x,flags=re.S)
V=[]  # (text, has_br, italic_text)
for p in paras:
    br='<w:br' in p and 'w:type="page"' not in p
    runs=re.findall(r'<w:r[ >].*?</w:r>',p,flags=re.S)
    t='';it=''
    for r in runs:
        s=''.join(html.unescape(m) for m in re.findall(r'<w:t[^>]*>(.*?)</w:t>',r,flags=re.S))
        if '<w:br' in r: s+='⏎'
        t+=s
        if re.search(r'<w:i(/| w:val="(true|1)")',r) or '<w:i>' in r: it+=s
    V.append((t,br,it))
print('vellum paragraphs',len(V),'with line breaks:',sum(1 for v in V if '⏎' in v[0]))
for v in V:
    if '⏎' in v[0]: print('  BR>',v[0][:150].replace('\n',' '))
def norm(s):
    s=unicodedata.normalize('NFC',s)
    s=s.replace('“','"').replace('”','"').replace('‘',"'").replace('’',"'").replace('″','"').replace('′',"'").replace(' ',' ').replace('…','...')
    s=re.sub(r'\\\*','*',s)
    return re.sub(r'\s+',' ',s).strip()
def strip_md(s):
    s=re.sub(r'~~(.*?)~~',r'\1',s); s=re.sub(r'\*\*(.*?)\*\*',r'\1',s); s=re.sub(r'(?<!\*)\*(?!\*)(.+?)\*',r'\1',s)
    return s
F=[];Fi=[]
for f in sorted(glob.glob('manuscript/chapter-*.md')):
    ch=f.split('-')[1]
    code=False
    for l in open(f,encoding='utf-8').read().split('\n'):
        if l.startswith('```'): code=not code; continue
        if not l.strip() or l.startswith('## ') or re.match(r'^\*\*(Jo|Cal)\*\*$',l) or re.match(r'^\\?\*\\?\*\\?\*$',l.strip()): continue
        its=re.findall(r'(?<!\*)\*(?!\*)(.+?)\*',l)
        F.append((ch,norm(strip_md(l)),[norm(i) for i in its]))
Vn=[norm(v[0].replace('⏎',' ')) for v in V]
fset={}
for i,(ch,t,its) in enumerate(F): fset.setdefault(t,[]).append(i)
vset=set(Vn)
missing=[(ch,t) for ch,t,its in F if t not in vset]
print('file paragraphs',len(F),'not found verbatim in Vellum:',len(missing))
# for missing ones find closest vellum para
vlist=[v for v in Vn if v]
fall=set(t for _,t,_ in F)
vextra=[v for v in vlist if v not in fall]
print('vellum paragraphs not in files:',len(vextra))
import itertools
shown=0
for ch,t in missing:
    best=difflib.get_close_matches(t,vextra,n=1,cutoff=0.6)
    if best:
        b=best[0]; sm=difflib.SequenceMatcher(None,t,b)
        diffs=[(t[i1:i2],b[j1:j2]) for tag,i1,i2,j1,j2 in sm.get_opcodes() if tag!='equal']
        print(f'[{ch}] DIFF file|vellum:',diffs[:4],'::',t[:60])
    else:
        print(f'[{ch}] MISSING in Vellum:',t[:140])
    shown+=1
    if shown>70: print('...more'); break
# italics check
vit={}
for (t,br,it),n in zip(V,Vn): vit[n]=norm(it)
lost=0
for ch,t,its in F:
    if its and t in vit:
        for i in its:
            if len(i)>2 and i not in vit[t] and not all(w in vit[t] for w in i.split()[:2]):
                lost+=1
                if lost<=40: print(f'[{ch}] ITALIC LOST:',i[:80])
print('italic spans lost:',lost)
