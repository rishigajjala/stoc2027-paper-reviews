import random,itertools,functools,json
random.seed(725)
def closure(n,R):
 R=set(R)
 for k in range(n):
  for i in range(n):
   for j in range(n):
    if (i,k) in R and (k,j) in R:R.add((i,j))
 return R

def ordinary(n,R):
 pred=[sum(1<<i for i in range(n) if (i,j) in R) for j in range(n)]
 @functools.lru_cache(None)
 def f(I):
  if I==(1<<n)-1:return 1
  return sum(f(I|1<<j) for j in range(n) if not I>>j&1 and pred[j]&I==pred[j])
 return f(0)

def deadline(n,R,B):
 X=sorted(set(range(n))-set(B));D={v:{x for x in X if (x,v) in R} for v in B};S={v:{x for x in X if (v,x) in R} for v in B}
 active=[v for v in B if S[v]];Y=sorted(set().union(*S.values())) if B else [];labels=Y+[-1];total=0
 for vals in itertools.product(*(S[v] for v in active)):
  g=dict(zip(active,vals));Q=closure(n,R|{(g[v],y) for v in active for y in S[v] if y!=g[v]})
  if any((v,v) in Q for v in range(n)):continue
  dl={v:g.get(v,-1) for v in B}
  def A(I,c):return sum(dl[v]==c and all(I>>x&1 for x in D[v]) for v in B)
  @functools.lru_cache(None)
  def f(I,q):
   if I==sum(1<<x for x in X) and not any(q):return 1
   ans=0
   for i,c in enumerate(labels):
    if q[i]:
     qq=list(q);qq[i]-=1;ans+=q[i]*f(I,tuple(qq))
   for x in X:
    if I>>x&1 or any((y,x) in Q and not I>>y&1 for y in X):continue
    if x in Y and q[labels.index(x)]:continue
    J=I|1<<x;qq=tuple(q[i]+A(J,c)-A(I,c) for i,c in enumerate(labels));ans+=f(J,qq)
   return ans
  total+=f(0,tuple(A(0,c) for c in labels))
 return total
checks=0
for n in range(1,8):
 for trial in range(70):
  R=closure(n,{(i,j) for i in range(n) for j in range(i+1,n) if random.random()<.25})
  candidates=[tuple(i for i in range(n) if b>>i&1) for b in range(1<<n) if all(not (b>>i&1 and b>>j&1) for i,j in R)]
  for B in random.sample(candidates,min(3,len(candidates))):
   a=ordinary(n,R);b=deadline(n,R,B);assert a==b,(n,R,B,a,b);checks+=1
out={'random_posets':490,'antichain_DP_checks':checks,'all_passed':True,'purpose':'Finite validation of deadline grouping and pattern partition, not a substitute for the general proof.'}
print(json.dumps(out));open('audit725.json','w').write(json.dumps(out,indent=2))
