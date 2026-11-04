import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(696)
max_identity=0.;min_slack=1e10;count=0
for n in range(2,16):
 C=np.eye(n)-np.ones((n,n))/n
 for k in range(1,n):
  for z in range(10):
   Q,_=np.linalg.qr(C@rng.normal(size=(n,k)));P=Q@Q.T;d=np.diag(P);a=d[:,None]+d[None,:]-2*P
   M=a-1;np.fill_diagonal(M,0);v=C@M@np.ones(n);cap=1-abs(M);np.fill_diagonal(cap,0)
   ident=((a*a-(d[:,None]-d[None,:])**2).sum()/4)-k*(k+1)
   max_identity=max(max_identity,abs(ident));min_slack=min(min_slack,(cap*cap).sum()-2*np.dot(v,v)/n)
   assert abs(ident)<1e-8
   assert (cap*cap).sum()+1e-8>=2*np.dot(v,v)/n
   assert np.maximum(M,0).sum()<=k*(k+1)+1e-8
   for r in range(1,n):
    A=(M>=0).astype(float);A[r:,r:]=0;A[:r,:r]=1;np.fill_diagonal(A,0);L=np.diag(A.sum(1))-A
    assert abs(v[:r].sum()+abs(M[:r,r:]).sum()+np.trace((L-r*C)@(C-2*P)))<1e-8
   count+=1
out={'cases':count,'max_projection_identity_residual':max_identity,'minimum_routing_quadratic_slack':min_slack,'status':'passed; numerical sanity checks, not proof'}
Path('audit696.json').write_text(json.dumps(out,indent=2));print(out)
