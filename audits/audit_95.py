"""Reproducible numerical stress checks, supplementary to the symbolic proof review.
Not a proof or exhaustive check over metrics. NumPy floats; seed 20261104.
"""
import itertools,json,numpy as np
rng=np.random.default_rng(20261104)
def compositions(n,k):
 if k==1:yield (n,);return
 for i in range(n+1):
  for r in compositions(n-i,k-1):yield (i,)+r
def metric(n):
 d=rng.uniform(.1,10,(n,n));d=(d+d.T)/2;np.fill_diagonal(d,0)
 for i in range(n):d=np.minimum(d,d[:,i,None]+d[None,i,:])
 return d
def energy_matrix(d):
 k=len(d); c=np.zeros_like(d);np.divide(1,d,out=c,where=d>0)
 lap=np.diag(c.sum(axis=1))-c
 return np.linalg.inv(lap+np.ones((k,k))/k)-np.ones((k,k))/k
weighted=0;identity=0;min_margin=float('inf')
for k in range(2,7):
 qs=np.array(list(compositions(k,k)),dtype=float)
 for trial in range(20):
  d=metric(k);g=energy_matrix(d);cs=np.diag(g)
  u=lambda q:k*k/2*((q-1)@g@(q-1)+q@cs)
  for s in range(k):
   a=qs-(1+1/k);a[:,s]+=1;h=a@g
   flows=(h-h[:,s,None])/np.where(d[:,s]>0,d[:,s],1);flows[:,s]=0
   vals=(qs*flows).sum(axis=1)+k*qs[:,s]-1/k
   assert vals.min()>-1e-7,(k,trial,s,vals.min())
   weighted+=len(qs);min_margin=min(min_margin,float(vals.min()))
   for q,hh in zip(qs,h):
    for i in np.flatnonzero(q):
     q2=q.copy();q2[i]-=1;q2[s]+=1
     assert abs(u(q)-u(q2)-k*k*(hh[i]-hh[s]))<1e-7
     identity+=1
potential_checks=0
for k in range(2,5):
 for trial in range(15):
  d=metric(2*k+1);ys=tuple(range(k));g=energy_matrix(d[np.ix_(ys,ys)])
  assigns=np.array(list(itertools.product(range(k),repeat=k)))
  counts=np.array([np.bincount(a,minlength=k) for a in assigns],dtype=float)
  energies=k*k/2*(np.einsum('bi,ij,bj->b',counts-1,g,counts-1)+counts@np.diag(g))
  def phi(xs):return np.min(energies+k**3*d[np.array(xs)[None,:],assigns].sum(axis=1))
  for rep in range(15):
   xs=tuple(rng.integers(k,2*k+1,k));before=phi(xs)
   for s in range(k):
    total=0
    for i in range(k):
     after=list(xs);after[i]=s
     total+=(before-phi(after))/d[xs[i],s]
    assert total>=k-1e-7,(k,trial,xs,s,total)
    potential_checks+=1
print(json.dumps({'seed':20261104,'weighted_current_cases':weighted,'serving_identity_cases':identity,'full_min_assignment_service_cases':potential_checks,'smallest_weighted_margin':min_margin,'result':'all numerical checks passed; supplementary, not proof'}))
