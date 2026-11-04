"""Apply the approved rating-only shortlist rule to data.json."""
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OTHERS = ('novelty', 'depth', 'exposition')

def rating_qualifies(r):
    return (r['significance'] == 5 and all(r[k] >= 4 for k in OTHERS)
            and any(r[k] == 5 for k in OTHERS))

def order(p):
    r = p['review']
    score = 9*r['significance'] + 5*r['novelty'] + 3*r['depth'] + 3*r['exposition']
    return (-score, int(p['number']))

def main():
    path = ROOT/'data.json'
    data = json.loads(path.read_text())
    papers = data['papers']
    before = {p['number'] for p in papers if p['selected']}
    for p in papers:
        p['qualifies_ratings'] = rating_qualifies(p['review'])
        p['selected'] = p['qualifies_ratings']
        p['rank'] = None
    selected = sorted((p for p in papers if p['selected']), key=order)
    for rank, p in enumerate(selected, 1):
        p['rank'] = rank
    qualified = [p for p in papers if p['qualifies_ratings']]
    meta = data['meta']
    meta.update(
        updated=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        target=None,
        selected=len(selected),
        selected_main_proof_checked=sum(p['review']['proof_status'] == 'main-proof-checked' for p in selected),
        selected_large_proof_exceptions=sum(p['review']['proof_status'] == 'partial-large-proof' for p in selected),
        rating_qualified=len(qualified),
        rating_qualified_pending_audit=sum(p['review']['proof_status'] == 'not-audited' for p in qualified),
        rating_qualified_unresolved=sum(p['review']['proof_status'] in ('unresolved', 'incorrect') for p in qualified),
        selection_rule={'significance': 5, 'other_fields': list(OTHERS), 'other_fields_minimum': 4, 'at_least_one_other': 5, 'proof_audit_required': False, 'count_cap': None},
        selection_policy='Ratings only: significance 5; novelty, depth and exposition each at least 4; at least one of those three equals 5. No proof-audit prerequisite and no fixed count cap. Proof notes are informational. Display order: weighted merit score, then submission number.',
        complete=meta['reviewed'] == len(papers),
    )
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
