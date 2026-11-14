import re,glob,datetime,collections
files=sorted(glob.glob('manuscript/chapter-*.md'))+sorted(glob.glob('manuscript/back-0[1-4]*.md'))
def short(f): return f.split('/')[-1].replace('chapter-','').replace('.md','')
print("== dashes / quotes / words")
tot=0
for f in files:
    s=open(f,encoding='utf-8').read(); w=len(s.split()); tot+=w
    em=s.count('—')+s.count('–'); st=s.count('"'); cu=s.count('“')+s.count('”'); sa=s.count("'"); ca=s.count('’')
    flag=[]
    if em: flag.append(f"dash={em}")
    if st and cu: flag.append(f"MIXED dq straight={st} curly={cu}")
    if sa and ca: flag.append(f"MIXED apos straight={sa} curly={ca}")
    if cu==0 and st: flag.append("straight")
    if flag: print(short(f),w,flag)
print("total words",tot)
print("== heading format")
for f in files[:38]:
    L=open(f,encoding='utf-8').read().split('\n')
    if not re.match(r'## Chapter \d+: ',L[0]) or not any(re.match(r'\*\*(Jo|Cal)\*\*',x) for x in L[1:4]): print(short(f),L[:3])
print("== Cal contractions (narration + 'I said' lines)")
con=re.compile(r"\b\w+(n['’]t|['’]ll|['’]ve|['’]re|['’]m|['’]d)\b|\b(it|that|there|he|she|what|let|who|here|where)['’]s\b",re.I)
for f in files[:38]:
    if '-cal' not in f: continue
    for n,l in enumerate(open(f,encoding='utf-8').read().split('\n'),1):
        if l.startswith('*') and l.endswith('*'): continue
        nar=re.sub(r'[“"][^”"]*[”"]','',l)
        nar=re.sub(r'\*[^*]*\*','',nar)
        m=con.search(nar)
        if m: print(short(f),n,'NARR',m.group(0),'|',nar.strip()[:90])
        if re.search(r'[”"],? I (said|asked|told)',l) or re.search(r'I (said|asked)[,.] [“"]',l):
            for q in re.findall(r'[“"]([^”"]*)[”"]',l):
                m=con.search(q)
                if m: print(short(f),n,'CALSAYS',m.group(0),'|',q[:90])
print("== Jo chapters: narration lacking contractions is fine; skip")
print("== typos")
for f in files:
    for n,l in enumerate(open(f,encoding='utf-8').read().split('\n'),1):
        for pat,name in [(r'  +\S','dblspace'),(r' [,.;:?!](\s|$)','space-before-punct'),(r'\b(\w+) \1\b','repeat'),(r'[a-z]\.[A-Z]','nospace'),(r',,|\.\.(?!\.)|\?\.|!\.','punct')]:
            m=re.search(pat,l)
            if m and not (name=='repeat' and m.group(1).lower() in ('had','that','very','no','so','three','ha','two','on','in','bye','her','it','go','one')) and not (name=='dblspace' and l.startswith(' ')):
                print(short(f),n,name,repr(l[max(0,m.start()-25):m.end()+25]))
        q=l.count('“')-l.count('”')
        if q!=0 and not (q==1 and True): print(short(f),n,'quote-balance',q,l[:60])
        if l.count('"')%2: print(short(f),n,'odd-straight-quotes',l[:70])
        if l.count('*')%2 and not l.startswith('***') and '\\*' not in l: print(short(f),n,'odd-asterisks',l[:70])
