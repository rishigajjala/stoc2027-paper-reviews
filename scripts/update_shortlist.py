"""Reproduce the approved 466-paper shortlist without changing reviews or ratings."""
import collections
import datetime
import json
import pathlib
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[1]
OTHERS = ('novelty', 'depth', 'exposition')

def rating_qualifies(r):
    return (r['significance'] == 5 and all(r[k] >= 4 for k in OTHERS)
            and any(r[k] == 5 for k in OTHERS))

def score(p):
    r = p['review']
    return 9*r['significance'] + 5*r['novelty'] + 3*r['depth'] + 3*r['exposition']

def order(p):
    return (-score(p), int(p['number']))

def balanced_selection(qualified, target, weights):
    ordered = sorted(qualified, key=order)
    if not 0 < target <= len(ordered):
        raise ValueError('Target must be positive and cannot exceed the qualified pool.')
    cutoff = score(ordered[target - 1])
    selected = [p for p in ordered if score(p) > cutoff]
    stronger = len(selected)
    boundary = [p for p in ordered if score(p) == cutoff]
    counts = collections.Counter(p['primary_topic'] for p in selected)
    pools = {topic: [p for p in boundary if p['primary_topic'] == topic] for topic in weights}
    # Increasing marginal costs for a separable convex objective. Rational
    # arithmetic avoids introducing platform-dependent rounding into ties.
    while len(selected) < target:
        available = [topic for topic in weights if pools[topic]]
        topic = min(available, key=lambda t: ((2*counts[t]+1-2*target*weights[t])/(target*weights[t]), t))
        selected.append(pools[topic].pop(0))
        counts[topic] += 1
    return sorted(selected, key=order), cutoff, stronger, len(boundary)

def main():
    path = ROOT/'data.json'
    data = json.loads(path.read_text())
    approved = json.loads((ROOT/'topic-balance'/'proposal.json').read_text())
    classifications = {p['number']: p['topic'] for p in approved['papers']}
    taxonomy = approved['taxonomy']
    weights = {topic: (Fraction(approved['stoc_counts'][topic], sum(approved['stoc_counts'].values()))
                       + Fraction(approved['focs_counts'][topic], sum(approved['focs_counts'].values())))/2
               for topic in taxonomy}
    target = next(s['size'] for s in approved['scenarios'] if s['key'] == 'balanced28')
    papers = data['papers']
    before = {p['number'] for p in papers if p['selected']}
    for p in papers:
        p['qualifies_ratings'] = rating_qualifies(p['review'])
        p['selected'] = False
        p['rank'] = None
        if p['qualifies_ratings']:
            if p['number'] not in classifications:
                raise ValueError(f"Primary topic must be assigned before selecting paper {p['number']}")
            p['primary_topic'] = classifications[p['number']]
    qualified = [p for p in papers if p['qualifies_ratings']]
    selected, cutoff, stronger, boundary = balanced_selection(qualified, target, weights)
    for rank, p in enumerate(selected, 1):
        p['selected'] = True
        p['rank'] = rank
    meta = data['meta']
    meta.update(
        updated=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        target=target,
        selected=len(selected),
        selected_main_proof_checked=sum(p['review']['proof_status'] == 'main-proof-checked' for p in selected),
        selected_large_proof_exceptions=sum(p['review']['proof_status'] == 'partial-large-proof' for p in selected),
        selected_pending_audit=sum(p['review']['proof_status'] == 'not-audited' for p in selected),
        selected_unresolved=sum(p['review']['proof_status'] in ('unresolved', 'incorrect') for p in selected),
        rating_qualified=len(qualified),
        rating_qualified_pending_audit=sum(p['review']['proof_status'] == 'not-audited' for p in qualified),
        rating_qualified_unresolved=sum(p['review']['proof_status'] in ('unresolved', 'incorrect') for p in qualified),
        selection_rule={'significance': 5, 'other_fields': list(OTHERS), 'other_fields_minimum': 4, 'at_least_one_other': 5, 'proof_audit_required': False, 'count_cap': target, 'topic_balance_at_cutoff': True},
        selection_policy=approved['rating_rule']+' '+approved['selection_rule'],
        topic_taxonomy=taxonomy,
        selected_primary_topics=dict(collections.Counter(p['primary_topic'] for p in selected)),
        topic_balance=approved['reference_rule'],
        topic_balance_report='topic-balance/',
        acceptance_rate_target=0.28,
        acceptance_rate_note=approved['rate_basis'],
        cutoff_score=cutoff,
        above_cutoff_selected=stronger,
        cutoff_tied_pool=boundary,
        cutoff_tied_selected=target-stronger,
        complete=meta['reviewed'] == len(papers),
    )
    meta.pop('proposal_status', None)
    after = {p['number'] for p in selected}
    change = {'before': len(before), 'after': len(after), 'retained': len(before & after),
              'added': sorted(after-before, key=int), 'removed': sorted(before-after, key=int)}
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False))
    temp.replace(path)
    print(json.dumps({'selected': len(selected), 'main': meta['selected_main_proof_checked'],
                      'partial': meta['selected_large_proof_exceptions'], 'qualifying_ratings': len(qualified),
                      'retained': change['retained'], 'added': len(change['added']), 'removed': len(change['removed'])}))
    return change

if __name__ == '__main__':
    main()
