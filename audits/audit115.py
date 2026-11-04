# Independent subset dynamic enumeration; avoids manuscript product-of-assignments implementation.
from functools import lru_cache
cases=[('goods',[(1,17,3,10,1,10,7,7,7,3,18)]*2+[(1,14,5,10,1,9,6,7,7,5,19)]*2),('chores',[(19,40,31,37,16,37,25,40,25,31,59)]*2+[(21,45,27,39,15,39,24,45,24,27,54)]*2)]
for mode,vs in cases:
 sums=[]
 for v in vs:
  s=[0]*2048
  for m in range(1,2048):
   b=m&-m;s[m]=s[m^b]+v[b.bit_length()-1]
  sums.append(s)
 @lru_cache(None)
 def best(i,mask):
  if i==3:return sums[i][mask]
  sub=mask;res=0 if mode=='goods' else 10000
  while True:
   other=best(i+1,mask^sub)
   res=max(res,min(sums[i][sub],other)) if mode=='goods' else min(res,max(sums[i][sub],other))
   if not sub:break
   sub=(sub-1)&mask
  return res
 print(mode,best(0,2047),best.cache_info())
