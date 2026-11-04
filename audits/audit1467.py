import random,itertools,json,pathlib
rng=random.Random(1467);total=0
for trial in range(240):
 n=rng.randint(3,7);k=rng.randint(2,min(4,n));d=[[0 if i==j else rng.randint(1,20) for j in range(n)] for i in range(n)]
 for i in range(n):
  for j in range(i):d[i][j]=d[j][i]
 for z in range(n):
  for i in range(n):
   for j in range(n):d[i][j]=min(d[i][j],d[i][z]+d[z][j])
 cs=list(itertools.combinations(range(n),k));idx={c:i for i,c in enumerate(cs)}
 def dist(x,y):return min(sum(d[a][b] for a,b in zip(x,p)) for p in itertools.permutations(y))
 def clique(c):return sum(d[a][b] for a,b in itertools.combinations(c,2))
 initial=cs[rng.randrange(len(cs))];cur=initial;w=[dist(initial,c) for c in cs];cost=ext=0
 for step in range(40):
  r=rng.randrange(n);nw=[]
  for c in cs:
   nw.append(min(w[idx[tuple(sorted(set(c)-{x}|{r}))]]+d[r][x] for x in c if len(set(c)-{x}|{r})==k))
  cand=[c for c in cs if r in c and set(c)<=set(cur)|{r}];best=min(nw[idx[c]]+dist(cur,c) for c in cand);nxt=rng.choice([c for c in cand if nw[idx[c]]+dist(cur,c)==best]);cost+=dist(cur,nxt);ext+=max(b-a for a,b in zip(w,nw));cur=nxt;w=nw;opt=min(w);cmax=max(clique(c) for c,v in zip(cs,w) if v==opt)
  assert cost<=k*opt+clique(initial)-cmax,(trial,step,'cost')
  assert ext<=(k+1)*opt+clique(initial)-cmax,(trial,step,'ext')
  total+=1
res={'random_integer_metric_instances':240,'checked_prefixes':total,'n_range':[3,7],'k_range':[2,4],'all_passed':True,'limitation':'Checks theorem inequalities using exact DP; does not establish general correctness or algebraic potential.'}
pathlib.Path('1467-audit.json').write_text(json.dumps(res,indent=2));print(res)
