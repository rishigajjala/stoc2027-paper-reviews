from itertools import product
from math import sqrt
m=3;U=range(1<<m);checked=0
for mask in range(1,1<<(1<<m)):
 F=[f for f in U if (mask>>f)&1]
 rad={D:sum(max(sum((1 if not (e>>p)&1 else -1)*(1 if not (f>>p)&1 else -1) for p in range(m) if (D>>p)&1) for f in F) for e in U)/8 for D in U}
 for v in U:
  rho=min(bin(v^f).count("1") for f in F)
  w=[]
  for p in range(m):
   w.append(sum(1 for T in U if not (T>>p)&1 and ((v^min(F,key=lambda f:bin((v^f)&T).count("1")))>>p)&1)/4)
  for D in U:
   assert sum(w[p] for p in range(m) if (D>>p)&1)<=rho+rad[D]+1e-12
   checked+=1
print('Class-dependent inequality exhaustive cube-dimension-3 cases:',checked)
print('Hall numeric constant:',120*sqrt(3601)+1,'<7202')
print('Weighted degree coefficient:',(2+1/7202)/(1-(900/3601)*(2+1/7202)))
print('Validation fixed-point factor:',704*784)
