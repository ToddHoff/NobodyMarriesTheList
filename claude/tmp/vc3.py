import zipfile,re,glob,html,unicodedata
z=zipfile.ZipFile('claude/tmp/vellum-export.docx'); x=z.read('word/document.xml').decode('utf-8')
def norm(s):
    s=unicodedata.normalize('NFC',s)
    s=s.replace('“','"').replace('”','"').replace('‘',"'").replace('’',"'").replace('″','"').replace('′',"'").replace(' ',' ')
    return re.sub(r'\s+',' ',re.sub(r'\\\*','*',s)).strip()
def strip_md(s):
    s=re.sub(r'~~(.*?)~~',r'\1',s); s=re.sub(r'\*\*(.*?)\*\*',r'\1',s); s=re.sub(r'(?<!\*)\*(?!\*)(.+?)\*',r'\1',s); return s
paras=re.findall(r'<w:p[ >].*?</w:p>',x,flags=re.S)
vit={}; allv=[]
for p in paras:
    note=bool(re.search(r'<w:pStyle w:val="(VellumWrittenNote|VellumVerse)"',p))
    t='';it=''
    for r in re.findall(r'<w:r[ >].*?</w:r>',p,flags=re.S):
        s=''.join(html.unescape(m) for m in re.findall(r'<w:t[^>]*>(.*?)</w:t>',r,flags=re.S))
        t+=s
        if re.search(r'<w:i\s*/>',r) or note: it+=s
    n=norm(t); allv.append(n)
    vit[n]=vit.get(n,'')+' '+norm(it)
allf=set(); lost=[]
for f in sorted(glob.glob('manuscript/*.md')):
    ch=f.split('/')[-1][:10]
    for ln,l in enumerate(open(f,encoding='utf-8').read().split('\n'),1):
        l2=re.sub(r'^(#+ |\d+\. |- )','',l)
        for c in (l,l2): allf.add(norm(strip_md(c)))
        t=norm(strip_md(l))
        if t in vit:
            for i in re.findall(r'(?<!\*)\*(?!\*)(.+?)\*',l):
                i=norm(re.sub(r'~~','',i))
                if len(i)>1 and i not in vit[t]: lost.append((ch,ln,i))
print('italic spans in files missing italics in Vellum:',len(lost))
for ch,ln,i in lost[:60]: print(' ',ch,ln,i[:90])
ex=[t for t in allv if t and t not in allf and t!='* * *' and not t.startswith('<w:')]
print('extras',len(ex))
for t in ex[:45]: print('  >',t[:120])
