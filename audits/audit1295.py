from itertools import product,combinations
import json
labels='AABBCCxy'; N=256
pc=lambda s:bin(s).count('1')
def val(i,s,exc=True):
 if not s:return 0
 goods=[labels[j] for j in range(8) if s>>j&1]; T='ABC'[i]; other=set('ABC')-{T}
 if exc and 'x' in goods and other<=set(goods):return 7
 if len(goods)==1:return 1
 out=1
 for a,b in combinations(goods,2):
  p=set([a,b]);r=1
  if p=={T,'y'}:r=6
  elif p==other:r=5
  elif p=={T,'x'}:r=4
  elif 'y' in p and p&other:r=3
  elif T in p and p&other:r=2
  out=max(out,r)
 return out
U=[[val(i,s,False) for s in range(N)] for i in range(3)]; V=[[val(i,s) for s in range(N)] for i in range(3)]
def efx(a,tab):
 return all(tab[i][a[i]]>=tab[i][a[j]^(1<<g)] for i in range(3) for j in range(3) if i!=j for g in range(8) if a[j]>>g&1)
counts=[0,0,0];W=[];meta=[]
for i in range(3):
 strict=[100*V[i][s]+pc(s) for s in range(N)]; rank={v:j for j,v in enumerate(sorted(set(strict)))};k=[rank[v] for v in strict];q=max(k);F=[256**(q-x) for x in k]; omega=[]
 for t in range(255):
  w=sum((-1)**pc(r^t)*F[r] for r in range(N) if r&t==t);assert w>0;omega.append(w)
 w=[sum(omega[t] for t in range(255) if s&(~t&255)) for s in range(N)]
 assert all(w[s]==F[0]-F[s] for s in range(N));W.append(w)
 meta.append({'ranks':q+1,'features':len(omega),'min_positive_weight':str(min(omega))})
for assignment in product(range(3),repeat=8):
 a=[sum(1<<g for g,j in enumerate(assignment) if j==i) for i in range(3)]
 for j,tab in enumerate([U,V,W]):counts[j]+=efx(a,tab)
assert counts[1:]==[0,0]
result={'allocations':3**8,'efx_counts_u_v_weighted_coverage':counts,'strictification':'100*v(S)+|S|','base':256,'coverage':meta}
open('1295-audit.json','w').write(json.dumps(result,indent=2));print(result)
