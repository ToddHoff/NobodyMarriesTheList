import re,glob,datetime
files=sorted(glob.glob('manuscript/chapter-*.md'))+sorted(glob.glob('manuscript/back-0[1-4]*.md'))
def short(f): return f.split('/')[-1].replace('chapter-','').replace('.md','')[:6]
T={f:open(f,encoding='utf-8').read() for f in files}
print("== straight dq lines in curly files")
for f in files:
    if short(f)[:2] in('01','06','30'):
        for n,l in enumerate(T[f].split('\n'),1):
            if '"' in l: print(short(f),n,l[:110])
print("== stale refs")
for pat in ["roasting pan","thirteenth","billing","tow truck","Starbucks","Eichler on a corner","every other Saturday","and what I owe","where it goes","where it doesn","piano man","meteor","down the margin","didn.t fit","did not fit","kitchen lunch","account manager","February"]:
    hits=[(short(f),n) for f in files for n,l in enumerate(T[f].split('\n'),1) if re.search(pat,l,re.I)]
    print(pat,len(hits),hits[:10])
print("== overused phrase counts (whole book)")
for pat in [r"\bquiet(ly)?\b",r"stopped talking",r"in the file",r"the shape of",r"something shifted",r"\ba kind of\b",r"(^|[.”] )As (if|though)\b",r"(^|[.”] )And yet\b",r"not just\b",r" of it\.",r"hand flat|flat on",r"for a long time",r"didn.t say anything|did not say anything|said nothing",r"\bnodded\b",r"\bwaited\b",r"looked at (me|him|her)\b",r"turned (it|the \w+) over",r"the way (I|he|she|you) ",r"\bsquared\b",r"went (hot|cold|quiet|still)",r"I let (him|her|it)\b",r"did not look (up|away|at)|didn.t look (up|away|at)",r"A plane went",r"My watch tapped",r"\bleaned\b"]:
    per=[(short(f)[:2],len(re.findall(pat,T[f],re.I|re.M))) for f in files]
    tot=sum(c for _,c in per); top=sorted([p for p in per if p[1]],key=lambda x:-x[1])[:6]
    print(f"{pat[:38]:40}",tot,top)
print("== weekday/date check")
mon={m:i+1 for i,m in enumerate("January February March April May June July August September October November December".split())}
wd="Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
pats=[re.compile(r"\b("+"|".join(wd)+r")(?: (?:night|morning|afternoon|evening))?,? (?:the )?("+"|".join(mon)+r") (\d{1,2})(?:st|nd|rd|th)?(?:, (\d{4}))?"),
      re.compile(r"\b("+"|".join(mon)+r") (\d{1,2})(?:, (\d{4}))?, (?:a|the|on a) ("+"|".join(wd)+")")]
for f in files[:38]:
    ch=int(short(f)[:2]); dy=2026 if ch<=36 else 2027
    for n,l in enumerate(T[f].split('\n'),1):
        for m in pats[0].finditer(l):
            y=int(m.group(4) or dy); d=datetime.date(y,mon[m.group(2)],int(m.group(3)))
            if wd[d.weekday()]!=m.group(1): print(short(f),n,m.group(0),'-> actually',wd[d.weekday()],y)
        for m in pats[1].finditer(l):
            y=int(m.group(3) or dy); d=datetime.date(y,mon[m.group(1)],int(m.group(2)))
            if wd[d.weekday()]!=m.group(4): print(short(f),n,m.group(0),'-> actually',wd[d.weekday()],y)
