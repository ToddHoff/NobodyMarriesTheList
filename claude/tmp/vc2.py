import zipfile,re,glob,html,unicodedata
z=zipfile.ZipFile('claude/tmp/vellum-export.docx'); x=z.read('word/document.xml').decode('utf-8')
i=x.find('querida'); print(re.sub(r'\s+',' ',x[i-700:i+60])[-520:]); print('----')
st=z.read('word/styles.xml').decode('utf-8')
print(sorted(set(re.findall(r'<w:rStyle w:val="([^"]+)"',x))), sorted(set(re.findall(r'<w:pStyle w:val="([^"]+)"',x))))
def norm(s):
    s=unicodedata.normalize('NFC',s)
    s=s.replace('“','"').replace('”','"').replace('‘',"'").replace('’',"'").replace('″','"').replace('′',"'").replace(' ',' ')
    return re.sub(r'\s+',' ',re.sub(r'\\\*','*',s)).strip()
def strip_md(s):
    s=re.sub(r'~~(.*?)~~',r'\1',s); s=re.sub(r'\*\*(.*?)\*\*',r'\1',s); s=re.sub(r'(?<!\*)\*(?!\*)(.+?)\*',r'\1',s); return s
allf=set()
for f in glob.glob('manuscript/*.md'):
    for l in open(f,encoding='utf-8').read().split('\n'):
        l2=re.sub(r'^(#+ |\d+\. |- )','',l)
        for c in (l,l2): allf.add(norm(strip_md(c)))
paras=re.findall(r'<w:p[ >].*?</w:p>',x,flags=re.S)
ex=[]
for p in paras:
    t=norm(''.join(html.unescape(m) for m in re.findall(r'<w:t[^>]*>(.*?)</w:t>',p,flags=re.S)))
    if t and t not in allf: ex.append(t)
print('extras',len(ex))
for t in ex[:60]: print('  >',t[:110])
