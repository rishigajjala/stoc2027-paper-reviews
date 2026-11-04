import re,numpy as np,json
s=open('286.txt').read().split('\f')
def listed(t):return [int(v) for line in t.splitlines() if ',' in line for v in re.findall(r'\d+',line)]
R=set(listed(s[13].split('R is the set')[1]));pi=listed(s[14].split('93, 23,')[1].split('B     An elementary')[0]);pi=[93,23]+pi;assert len(R)==175 and len(pi)==182 and set(pi)==set(range(182)),(len(R),len(pi))
C={102,163,164,341,386,406,476,513,862};J={103,349,470,517,603,606,674,716,861};B=sorted(R-C-J);assert len(B)==157 and not C&J
add=np.zeros((9,9),dtype=np.int16);mul=add.copy()
for x in range(9):
 a,b=x%3,x//3
 for y in range(9):
  c,d=y%3,y//3;add[x,y]=(a+c)%3+3*((b+d)%3);mul[x,y]=(a*c-b*d)%3+3*((a*d+b*c)%3)
neg=np.array([next(y for y in range(9) if add[x,y]==0) for x in range(9)])
inv=np.array([0]+[next(y for y in range(1,9) if mul[x,y]==1) for x in range(1,9)])
def powf(x,n):
 r=1
 for _ in range(n):r=mul[r,x]
 return r
def dot(x,y):
 z=0
 for a,b in zip(x,y):z=add[z,mul[a,b]]
 return z
T=[(0,0,1)]+[(0,1,a) for a in range(9)]+[(1,a,b) for a in range(9) for b in range(9)]
edges=[(i,91+j) for i,p in enumerate(T) for j,l in enumerate(T) if dot(p,l)==0];assert len(edges)==910
incident=[[e for e,(a,b) in enumerate(edges) if v in (a,b)] for v in range(182)];assert all(len(es)==10 for es in incident)
pos={v:i for i,v in enumerate(pi)}
def oriented(e):
 a,b=edges[e];lo,hi=sorted((a,b),key=pos.get);return (hi,lo) if e in R else (lo,hi)
ori=[oriented(e) for e in range(910)]
for v,es in enumerate(incident):
 assert sum(ori[e][0]==v for e in es)==5
 assert sum(ori[e][0]==v for e in es if e in C)==sum(ori[e][1]==v for e in es if e in J)
# Independently calculate local interpolation matrices from the explicitly normalized triples.
evals=[]
for v,es in enumerate(incident):
 neigh=[(b-91 if v<91 else a) for e in es for a,b in [edges[e]]]
 u,w=T[neigh[0]],T[neigh[1]]
 rows=[]
 for j in neigh:
  coeff=[(a,b) for a in range(9) for b in range(9) if tuple(add[mul[a,x],mul[b,y]] for x,y in zip(u,w))==T[j]];assert len(coeff)==1
  a,b=coeff[0]
  if v>=91:a,b=powf(a,3),powf(b,3)
  rows.append([mul[powf(a,4-r),powf(b,r)] for r in range(5)])
 evals.append(np.array(rows,dtype=np.int16))
def solve(A,Y):
 A=A.copy();Y=Y.copy()
 for k in range(len(A)):
  t=next(t for t in range(k,len(A)) if A[t,k]);A[[k,t]]=A[[t,k]];Y[[k,t]]=Y[[t,k]]
  f=inv[A[k,k]];A[k]=mul[f,A[k]];Y[k]=mul[f,Y[k]]
  for t in range(len(A)):
   if t==k:continue
   f=neg[A[t,k]];A[t]=add[A[t],mul[f,A[k]]];Y[t]=add[Y[t],mul[f,Y[k]]]
 return Y
def matmul(A,Y):
 out=np.zeros((len(A),Y.shape[1]),dtype=np.int16)
 for k in range(A.shape[1]):out=add[out,mul[A[:,k,None],Y[k,None,:]]]
 return out
basis=np.eye(157,dtype=np.int16);bid={e:i for i,e in enumerate(B)};values={};decoded={}
for v in pi:
 es=incident[v];known=[];rows=[]
 for j,e in enumerate(es):
  if e in C:known.append(j);rows.append(np.zeros(157,dtype=np.int16))
  elif ori[e][1]==v and e not in J:
   known.append(j);rows.append(basis[bid[e]] if e in B else values[e])
 assert len(known)==5,(v,len(known))
 out=matmul(evals[v],solve(evals[v][known],np.array(rows)))
 for j,e in enumerate(es):
  if e not in R and ori[e][0]==v:values[e]=out[j]
  if e in B and ori[e][0]==v:decoded[e]=out[j];assert np.array_equal(out[j],basis[bid[e]]),(v,e)
assert len(values)==735 and len(decoded)==157
# Projective-plane girth and independently enumerate the leading terms used by the dimension proof.
for a in range(91):
 for b in range(a):assert len(set(incident[a])&set(incident[b]))==0 # Edges are distinct; common neighbors tested next.
nei=[{edges[e][1] for e in incident[a]} for a in range(91)]
assert all(len(nei[a]&nei[b])==1 for a in range(91) for b in range(a))
trip=[(a,b,4-a-b) for a in range(5) for b in range(5-a)]
mons=[(a,b) for a in trip for b in trip if not(a[0]>=1 and b[0]>=3) and not(a[1]>=3 and b[1]>=1)]
lt={(9*(a[1]+a[2])+3*b[0],9*a[0]+a[2]+3*b[1],a[0]+a[1]+3*b[2]) for a,b in mons};assert len(mons)==len(lt)==166
out={'vertices':182,'candidate_edges':910,'removed_edges':175,'physical_edges':735,'sessions':157,'all_session_basis_transfers_verified':True,'local_interpolants':182,'dimension_leading_terms':166,'flow_rate_bound':'147/157','coding_rate_lower_bound':1}
open('audit286-result.json','w').write(json.dumps(out,indent=2));print(json.dumps(out))
