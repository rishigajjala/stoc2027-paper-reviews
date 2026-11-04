from itertools import product
cnt=0
for r in range(2,23,2):
 P=[0]+list(range(1,r,2));F=[i for i in range(r) if i not in P]
 for bits in product([0,1],repeat=len(P)):
  D={p for p,b in zip(P,bits) if b}
  if not D:continue
  for p in D:
   q=[(i,1 if i in D else 0) for i in range(r)];v=[(i,0)for i in range(r)]
   edges=[(v[0],v[1],1)]+[(v[i],v[i+1],0)for i in range(2,r,2)]
   if p==0:edges +=[(q[i],q[i+1],0)for i in range(1,r-1,2)]
   elif p==1 and r>2:edges +=[(q[0],q[2],0)]+[(q[i],q[i+1],0)for i in range(3,r-1,2)]
   elif p>=3:
    edges +=[(q[0],q[1],1)]+[(q[i],q[i+1],0)for i in range(2,p-1,2)]
    if p<r-1:edges +=[(q[p-1],q[p+1],1)]+[(q[i],q[i+1],0)for i in range(p+2,r-1,2)]
   adj={x:[]for x in set(q+v)-{q[p]}}
   for x,y,t in edges:adj[x].append((y,t));adj[y].append((x,t))
   color={q[p]:0}
   for x in adj:
    if x in color:continue
    color[x]=1;stack=[x]
    while stack:
     x=stack.pop()
     for y,t in adj[x]:
      c=3-color[x] if t else color[x]
      if y in color:assert color[y]==c
      else:color[y]=c;stack.append(y)
   def fold(z):
    a=color[z[0]]
    for x in z[1:]:
     b=color[x];assert a!=b;a=3-a-b
    return a
   assert fold(v)==0 and fold(q)!=0
   cnt+=1
print('All',cnt,'overlap patterns through chain length 22 satisfy compatible folds.')
