"""Offline descriptive analysis. Python 3 standard library; no model/network calls."""
import argparse
import collections
import hashlib
import json
import pathlib
import random
import statistics
import copy
import itertools
from fractions import Fraction

SANTE='inclusionai/ling-3.0-flash-sante'
BASE='inclusionai/ling-3.0-flash'
def mean(xs):
    return statistics.mean(xs) if xs else None
def score(r,partial=0):
    return None if r['facets'] is None else 100*(r['facets'].count('C')+partial*r['facets'].count('P'))/len(r['facets'])
def validate(rows):
    assert len(rows) in (240,480),'Expected complete direct or full grid'
    keys={(r['question_no'],r['model'],r['arm']) for r in rows}
    models={r['model'] for r in rows}
    assert len(models)==6 and SANTE in models and BASE in models
    assert keys=={(q,m,a) for q in range(1,41) for m in models for a in sorted({r['arm'] for r in rows})},'Duplicate or absent slot'
    for r in rows:
        if r['text'] is None:
            assert r['facets'] is None and r['text_sha256'] is None,'Missing answer must remain unscored'
            assert r['status'] not in ['completed','partial','format_failed']
        else:
            assert hashlib.sha256(r['text'].encode()).hexdigest()==r['text_sha256'],'Answer hash mismatch'
            assert len(r['facets'])==len(r['facet_ids'])>0 and set(r['facets'])<=set('CPIN')
            assert r['status'] in ['completed','partial','format_failed']
    assert sum(r['text'] is not None for r in rows)==(237 if len(rows)==240 else 472)

def paired(rows,arm,case=None,family=None,partial=0,completed_only=False):
    sub=[r for r in rows if r['arm']==arm and (case is None or r['case']==case) and (family is None or r['family']==family)]
    a={r['question_no']:r for r in sub if r['model']==SANTE}
    b={r['question_no']:r for r in sub if r['model']==BASE}
    pairs=[]
    for q in sorted(a):
        if score(a[q]) is None or score(b[q]) is None:continue
        if completed_only and any(x['status']!='completed' for x in [a[q],b[q]]):continue
        pairs.append(dict(question_no=q,family=a[q]['family'],sante=score(a[q],partial),base=score(b[q],partial),
                          difference_pp=score(a[q],partial)-score(b[q],partial)))
    dif=[x['difference_pp'] for x in pairs]
    groups=collections.defaultdict(list)
    for x in pairs:groups[x['family']].append(x['difference_pp'])
    loo={f:mean([x['difference_pp'] for x in pairs if x['family']!=f]) for f in groups}
    ci=None
    if len(groups)>1:
        # Resample entire drug families. The interval is exploratory, not a
        # population claim; only five families per case were selected.
        rng=random.Random(20261108);families=sorted(groups);draws=[]
        for _ in range(10000):
            selected=rng.choices(families,k=len(families))
            draws.append(mean([v for f in selected for v in groups[f]]))
        draws.sort();ci=[draws[249],draws[9749]]
    return dict(arm=arm,case=case,family=family,partial_weight=partial,completed_only=completed_only,
                matched_n=len(pairs),sante_pct=mean([x['sante'] for x in pairs]),base_pct=mean([x['base'] for x in pairs]),
                difference_pp=mean(dif),wins=sum(x>1e-9 for x in dif),ties=sum(abs(x)<1e-9 for x in dif),losses=sum(x< -1e-9 for x in dif),
                family_cluster_bootstrap_95_interval_pp=ci,leave_one_family_out=loo,questions=pairs)

def analyze(rows):
    validate(rows);cells=[]
    for model in sorted({r['model'] for r in rows}):
        for arm in sorted({r['arm'] for r in rows}):
            for case in [None,1,2]:
                rs=[r for r in rows if r['model']==model and r['arm']==arm and (case is None or r['case']==case)]
                have=[r for r in rs if r['facets'] is not None]
                cells.append(dict(model=model,arm=arm,case=case,scheduled=len(rs),available=len(have),missing=len(rs)-len(have),
                    strict_pct=mean([score(r) for r in have]),partial_half_credit_pct=mean([score(r,.5) for r in have]),
                    delivered_credit_pct=sum(score(r) or 0 for r in rs)/len(rs),
                    answers_with_incorrect_facet=sum('I' in r['facets'] for r in have),
                    no_facet_addressed=sum(set(r['facets'])=={'N'} for r in have),
                    addressed_facet_pct=mean([100*(len(r['facets'])-r['facets'].count('N'))/len(r['facets']) for r in have]),
                    statuses=dict(collections.Counter(r['status'] for r in rs))))
    contrasts=[paired(rows,arm,c,partial=p,completed_only=complete) for arm in sorted({r['arm'] for r in rows})
               for c in [None,1,2] for p,complete in [(0,False),(.5,False),(0,True)]]
    families=[paired(rows,arm,family=f) for arm in sorted({r['arm'] for r in rows}) for f in sorted({r['family'] for r in rows})]
    common=[]
    for arm in sorted({r['arm'] for r in rows}):
        for case in [None,1,2]:
            qq=[q for q in range(1,41) if (case is None or (1 if q<=20 else 2)==case) and
                all(r['text'] is not None for r in rows if r['question_no']==q and r['arm']==arm)]
            for m in sorted({r['model'] for r in rows}):
                rs=[r for r in rows if r['model']==m and r['arm']==arm and r['question_no'] in qq]
                common.append(dict(model=m,arm=arm,case=case,n=len(rs),strict_pct=mean([score(r) for r in rs]),
                                   answers_with_incorrect_facet=sum('I' in r['facets'] for r in rs)))
    return dict(status='Exploratory reanalysis of locked AI judgments; not human validation',
                scope='All two case strata and all ten pre-existing drug families are reported. No outcome-selected question exclusions.',
                uncertainty='Descriptive family bootstrap: 10000 draws, seed 20261108; five families per case. Not confirmatory, not corrected for multiple comparisons, not representative of medicine.',
                cells=cells,contrasts=contrasts,families=families,common_all_models=common)

NAMES={'inclusionai/ling-3.0-flash-sante':'Santé','inclusionai/ling-3.0-flash':'Base Ling',
       'moonshotai/kimi-k2.6':'Kimi','deepseek/deepseek-v4.1-flash':'DeepSeek',
       'qwen/qwen3.8-flash':'Qwen','mistralai/mistral-small-2603':'Mistral'}

def overlay(rows,entries):
    result=copy.deepcopy(rows);by_id={r['record_id']:r for r in result};seen=set()
    for e in entries:
        key=e['record_id'],e['facet_id'];assert key not in seen;seen.add(key)
        r=by_id[e['record_id']];assert r['text_sha256']==e['canonical_answer_sha256']
        i=r['facet_ids'].index(e['facet_id']);assert r['facets'][i]==e['original_grade']
        assert e['returned_grade'] in ('C','P','I','N');r['facets'][i]=e['returned_grade']
    return result

def clinical_tests(rows):
    tests=[]
    for arm in sorted({r['arm'] for r in rows}):
        a={r['question_no']:r for r in rows if r['model']==SANTE and r['arm']==arm and r['case']==2}
        b={r['question_no']:r for r in rows if r['model']==BASE and r['arm']==arm and r['case']==2}
        groups=collections.defaultdict(list)
        for q in a:
            if a[q]['facets'] is not None and b[q]['facets'] is not None:
                groups[a[q]['family']].append(Fraction(a[q]['facets'].count('C'),len(a[q]['facets']))-Fraction(b[q]['facets'].count('C'),len(b[q]['facets'])))
        totals=[sum(v,Fraction()) for v in groups.values()];observed=sum(totals,Fraction())
        draws=[sum((t*s for t,s in zip(totals,signs)),Fraction()) for signs in itertools.product([-1,1],repeat=len(totals))]
        tests.append({'setting':arm,'families':len(totals),'nonzero_families':sum(t!=0 for t in totals),
                      'two_sided_p':sum(abs(d)>=abs(observed) for d in draws)/len(draws)})
    return tests

def report(result):
    lines=['# Reproduced results','',
           'Current view: submitted labels applied only to their specified facets. Other labels remain first AI judgments. Original results are retained in results.json. These are exploratory coverage scores, not clinical accuracy.','',
           '| Model | Setting | Available / scheduled | Strict C | Delivered C |','| --- | --- | --- | --- | --- |']
    for r in result['current']['cells']:
        if r['case'] is None:lines.append(f"| {NAMES[r['model']]} | {r['arm']} | {r['available']} / {r['scheduled']} | {r['strict_pct']:.2f}% | {r['delivered_credit_pct']:.2f}% |")
    lines+=['','## Matched Santé and base Ling','',
            '| Setting | Task | Pairs | Santé C | Ling C | Gap, pp | Family-bootstrap interval, pp |',
            '| --- | --- | --- | --- | --- | --- | --- |']
    for r in result['current']['contrasts']:
        if r['case'] and not r['partial_weight'] and not r['completed_only']:
            lo,hi=r['family_cluster_bootstrap_95_interval_pp']
            lines.append(f"| {r['arm']} | {'Historical' if r['case']==1 else 'Clinical'} | {r['matched_n']} | {r['sante_pct']:.2f}% | {r['base_pct']:.2f}% | {r['difference_pp']:+.2f} | {lo:+.2f} to {hi:+.2f} |")
    lines+=['','Intervals resample whole families (10,000 draws, seed 20261108); five selected families per task. They are descriptive and do not establish superiority or equivalence.','',
            '## Common-question comparison','',
            '| Model | Setting | Task | Common questions | Strict C | Answers with at least one I |',
            '| --- | --- | --- | --- | --- | --- |']
    for r in result['current']['common_all_models']:
        if r['case']:lines.append(f"| {NAMES[r['model']]} | {r['arm']} | {'Historical' if r['case']==1 else 'Clinical'} | {r['n']} | {r['strict_pct']:.2f}% | {r['answers_with_incorrect_facet']} |")
    lines+=['','## Clinical family sign-flip sensitivity','']
    for t in result['clinical_tests']:lines.append(f"- {t['setting']}: two-sided p = {t['two_sided_p']:.3f}; {t['nonzero_families']} nonzero families of {t['families']}.")
    lines+=['','The full study considered two clinical setting tests; its Holm-adjusted values were both 1.000. The direct-only subset does not redefine that testing family. No significance claim is made.','',
            'The current direct clinical gap depends on Q36 and Q37; those decisive facets were not in the returned review. Other-model labels remain AI grades.','']
    return '\n'.join(lines)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path,default=pathlib.Path(__file__).parent/'results');args=p.parse_args()
    root=pathlib.Path(__file__).resolve().parent
    rows=json.loads((root/'data/answers.json').read_text());entries=json.loads((root/'data/returned_review.json').read_text())['entries']
    current=overlay(rows,entries)
    result={'original':analyze(rows),'current':analyze(current),'clinical_tests':clinical_tests(current),
            'returned_entries':len(entries),'changed_grades':sum(r['changed'] for r in entries),
            'limitations':'Targeted review; unnamed reviewer; unchecked facets remain AI grades. No new model calls.'}
    result['current']['status']='Partial returned-review overlay; other labels remain first AI judgments.'
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    (args.output/'TABLES.md').write_text(report(result))
    print(json.dumps({'slots':len(rows),'displayed':sum(r['text'] is not None for r in rows),'returned_entries':len(entries),'paid_calls':0}))

if __name__=='__main__':main()
