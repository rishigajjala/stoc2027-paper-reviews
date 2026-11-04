import random,itertools,math,json
r=random.Random(980);counts={}
for n in range(2,8):
 done=0
 for _ in range(10000):
  ys=[r.randint(-10000,10000)for i in range(n-1)];ys.append(-sum(ys));den=r.randint(5000,30000)
  if len(set(ys))<n or 0 in ys or any(sum(ys[i]for i in S)==0 for k in range(1,n)for S in itertools.combinations(range(n),k)):continue
  for v in range(n):
   t=-ys[v];z=0
   if 0<t<den:
    for pi in itertools.permutations([i for i in range(n)if i!=v]):
     u=ys[pi[0]];prod=1
     for i in pi[1:]:prod*=int(-t<ys[i]<0)-int(0<u<t);u+=ys[i]
     z+=prod
   s=sum(y>0 for y in ys)
   expected=(-1)**(s-1)*math.factorial(s)*math.factorial(n-1-s)if ys[v]==min(ys)and ys[v]>-den else 0
   assert z==expected,(n,ys,v,z,expected)
  done+=1
  if done==50:break
 counts[n]=done
open('check980-results.json','w').write(json.dumps(counts));print(counts)
