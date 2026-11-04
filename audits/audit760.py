import math,itertools,json
alpha=3/(2*math.e)
v=lambda r:max(r-1/12,0)
def gain(rs,j,b):
 z=list(rs);p=min(z[j],b);g=p-alpha*(v(z[j])-v(z[j]-p));z[j]-=p;return tuple(z),g
maximum=-1;bad=[]
for rs in itertools.product([0,.25,1],repeat=4):
 best=0
 for a in range(4):
  r1,g1=gain(rs,a,1)
  for b in range(4):
   r2,g2=gain(r1,b,.5)
   eg3=sum(max(0,max(gain(r2,c,.5)[1] for c in side)) for side in [(0,1),(2,3)])/2
   best=max(best,g1+g2+eg3)
 maximum=max(maximum,best)
 bound=2*(1-11*alpha/12)-alpha/24
 if best>bound+1e-12:bad.append((rs,best,bound))
d=90;gap=15/(8*d)-(11/12)*math.log(d/(d-2))
out={'middle_phase_budget_vectors_checked':81,'violations':len(bad),'maximum_gain':maximum,'stated_bound':bound,'gap_per_H_at_d90':gap,'claimed_lower_gap_per_H':1/4320,'d90_constant_valid':gap>1/4320,'qualification':'Last removal preserves potential only after a WLOG optimal final allocation, or use the resulting nonpositive drop as an inequality.'}
assert not bad and out['d90_constant_valid'];print(json.dumps(out));open('audit760.json','w').write(json.dumps(out,indent=2))
