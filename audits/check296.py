import numpy as np,json
from itertools import product
V=np.array([[7,6,3,3,1,1,2,1],[6,7,1,3,3,1,1,2],[7,6,1,1,3,3,2,1],[6,7,3,1,1,3,1,2]])
A=np.array(list(product(range(4),repeat=8)),dtype=np.uint8)
U=np.stack([(V[i]*(A==i)).sum(axis=1) for i in range(4)],axis=1)
efx=np.ones(len(A),dtype=bool)
for i in range(4):
 for j in range(4):
  if i==j:continue
  vals=V[i]*(A==j)
  smallest=np.where(A==j,V[i],1000000).min(axis=1)
  efx &= U[:,i]>=vals.sum(axis=1)-smallest
inds=np.flatnonzero(efx)
unmatched=[]
for a in inds:
 if not np.any(np.all(U>=U[a],axis=1)&np.any(U>U[a],axis=1)):unmatched.append(int(a))
r={'allocations':len(A),'efx':len(inds),'pareto_optimal_efx':len(unmatched),'all_efx_dominated':not unmatched}
print(json.dumps(r));open('check296.json','w').write(json.dumps(r))
