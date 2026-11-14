import re,glob,sys
L,R='“','”'
out=[]
for f in sorted(glob.glob('manuscript/chapter-*.md')):
    ch=f.split('-')[1]
    ps=[p.strip() for p in open(f,encoding='utf-8').read().split('\n\n') if p.strip()]
    for i in range(1,len(ps)):
        a,b=ps[i-1],ps[i]
        if not b.startswith(L): continue
        qs=re.findall(L+'([^'+R+']*)'+R,a)
        if not qs or not qs[-1].rstrip().endswith('?'): continue
        sp=re.findall(L+'([^'+R+']*)'+R,b)
        said=' '.join(sp)
        n=len(said.split())
        if n>12 or said.rstrip().endswith('?'): continue
        if re.fullmatch(r"(Yes|No|Yeah|Nope|Okay|Sure)[.,!]?\s*",said): continue
        out.append(f"{ch}|{qs[-1][-90:]} >> {b[:140]}")
print(len(out))
open('claude/tmp/facts.txt','w',encoding='utf-8').write('\n'.join(out))
