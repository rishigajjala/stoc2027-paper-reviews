import itertools,json
cycles=[['a','b','c'],['a','d','e','f'],['b','g','h','i'],['c','j','k','l'],['j','m','n']]
edges={tuple(sorted((C[t],C[(t+1)%len(C)]))) for C in cycles for t in range(len(C))}
V=sorted({x for e in edges for x in e})
found={}
for length in (3,4):
 sets=[]
 for S in itertools.combinations(V,length):
  es=[e for e in edges if set(e)<=set(S)]
  if len(es)==length and all(sum(v in e for e in es)==2 for v in S):sets.append(list(S))
 found[length]=sets
X=found[3];Y=found[4]
conflicts=[(x,y) for x in range(len(X)) for y in range(len(Y)) if set(X[x])&set(Y[y])]
feasible=[(x,y) for x in range(len(X)) for y in range(len(Y)) if not(set(X[x])&set(Y[y]))]
# Under the paper's permitted smallest-delta tie selecting C3 and first clone abc:
chosen=X.index(['a','b','c']);blocked=[y for x,y in conflicts if x==chosen]
assert len(blocked)==len(Y) and feasible
assert all(any(a==x for a,b in conflicts) for x in range(len(X)))
assert all(any(b==y for a,b in conflicts) for y in range(len(Y)))
out={'host_edges':sorted(edges),'triangles':X,'squares':Y,'conflicts':conflicts,'feasible_disjoint_pairs':feasible,'trace':'All clones have positive degree, so preliminary isolated-clone rule does nothing. One host component gives delta_C3=delta_C4=1. Select C3 (allowed tie), clone abc. It conflicts with all three C4 clones; deleting them empties Delta_C4. Step 5 sees delta_C3=1 and exits without trying the other C3 clone. Nevertheless jmn with adef is disjoint, indeed no host edges join these chosen sets.'}
open('audit488.json','w').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
