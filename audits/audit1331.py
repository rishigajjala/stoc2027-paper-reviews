from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations
import random,json
@lru_cache(None)
def log_interval(x):
 x=F(x);k=0
 while x>=2:x/=2;k+=1
 while x<1:x*=2;k-=1
 z=(x-1)/(x+1);s=sum((2*z**(2*h+1)/F(2*h+1) for h in range(64)),F(0));err=2*z**129/(129*(1-z*z))
 if k:
  lo2,hi2=log_interval(F(2)) if x!=1 or k!=1 else (None,None)
  if lo2 is None:
   z=F(1,3);lo2=sum((2*z**(2*h+1)/F(2*h+1) for h in range(64)),F(0));hi2=lo2+2*z**129/(129*(1-z*z))
  return (s+k*(lo2 if k>=0 else hi2),s+err+k*(hi2 if k>=0 else lo2))
 return s,s+err
r=1;mass=F(0);params=[];margin=F(1)
for j in range(1,281):
 a=F(11,100) if j==1 else F(1,r*(j+13));c=F(100,89) if j==1 else 2-F(2,3*r)
 assert 1<c<2 and 0<a<F(1,2)<1/c
 lc=log_interval(c);lm=log_interval(c-1);la=log_interval(a);lb=log_interval(1-a);l2=log_interval(F(2))
 assert lc[0]+(r-1)*lm[0]>0
 U=(lc[1]-a*la[0]-(1-a)*lb[0]-a*lm[0])/l2[0]
 assert 0<U<1-F(1,10**38);margin=min(margin,1-U)
 mass+=(2 if j==1 else r-prev)*a;prev=r;params.append([r,str(a),str(c)]);r=(4*r+2)//3
assert F(1001,1000)<mass and prev<10**36
print('parameters',len(params),'cutoff',prev,'mass',float(mass),'min exponent gap',float(margin),flush=True)

def perm(A):return sum(__import__('functools').reduce(lambda z,i:z*A[i][p[i]],range(len(A)),1) for p in permutations(range(len(A))))
def solve(A):
 n=len(A);R=(1,2,4);alpha=(F(3,5),F(1,5),F(1,20));full=(1<<n)-1;out=0
 for ri,r in enumerate(R):
  @lru_cache(None)
  def gadget(d):
   @lru_cache(None)
   def step(j,a,k,nu):
    if a==0 and k==0:
     if j==n-1:return int(nu[ri]<=alpha[ri]*n and all(nu[t]>alpha[t]*n for t in range(ri+1,len(R))))
     return step(j+1,d[j+1],0,nu)
    val=0
    if k==0 and a:val+=step(j,a-1,1,nu)
    if k and a:
     nxt=tuple(v+int(R[t]==k and t>=ri) for t,v in enumerate(nu));val-=a*step(j,a-1,k+1,nxt)
    if k>r:val+=step(j,a,0,nu)
    return val
   return step(0,d[0],0,(0,0,0))
  @lru_cache(None)
  def dp(S,d,k,j):
   if S==full and k==0:return gadget(d)
   ans=0
   if k:
    ans+=dp(S,d,0,0)
    if k<r:
     for i in range(n):
      if not S>>i&1:ans-=A[i][j]*dp(S|1<<i,d,k+1,j)
   else:
    i=next(i for i in range(n) if not S>>i&1)
    for q in range(n):
     ans+=A[i][q]*dp(S|1<<i,d,1,q)
     dd=list(d);dd[q]+=1
     if sum(x>0 for x in dd)<=alpha[ri]*n:ans+=A[i][q]*dp(S|1<<i,tuple(dd),0,0)
   return ans
  out+=dp(0,(0,)*n,0,0)
 return out
random.seed(1331);cases=0
for n in range(1,8):
 for t in range(5):
  A=[[random.randrange(-2,3) for j in range(n)] for i in range(n)];v=solve(A);w=perm(A);assert v==w,(n,t,v,w);cases+=1
print('DP cases',cases,flush=True)
open('1331-audit.json','w').write(json.dumps({'parameter_count':280,'max_cutoff':prev,'mass':float(mass),'min_exponent_gap':float(margin),'exact_rational_parameters_verified':True,'small_matrix_cases':cases,'sizes':'1..7','entries':'-2..2','cutoffs':[1,2,4],'budgets':['3/5','1/5','1/20']},indent=2))
