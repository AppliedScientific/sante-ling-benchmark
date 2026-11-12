"""Validate the standalone dataset and saved analysis; no network calls."""
import hashlib,json,pathlib,subprocess,sys,tempfile
from analysis import validate,overlay
ROOT=pathlib.Path(__file__).resolve().parent

def main():
    meta=json.loads((ROOT/'dataset.json').read_text());rows=json.loads((ROOT/'data/answers.json').read_text());validate(rows)
    assert len(rows)==meta['scheduled'] and sum(r['text'] is not None for r in rows)==meta['available']
    if meta['scope']=='direct-only':assert {r['arm'] for r in rows}=={'direct'}
    by={r['record_id']:r for r in rows};seen=[];spans=0
    for path in sorted((ROOT/'assessments').glob('question-*.json')):
        for a in json.loads(path.read_text())['answers']:
            rid=a['answer_id'];assert rid in by and by[rid]['text'] is not None;seen.append(rid)
            assert a.get('text_sha256',by[rid]['text_sha256'])==by[rid]['text_sha256']
            def visit(value):
                nonlocal spans
                if isinstance(value,dict):
                    if all(k in value for k in ('start','end','text')) and isinstance(value['start'],int) and isinstance(value['end'],int):
                        assert 0<=value['start']<=value['end']<=len(by[rid]['text'])
                        assert by[rid]['text'][value['start']:value['end']]==value['text'];spans+=1
                    for x in value.values():visit(x)
                elif isinstance(value,list):
                    for x in value:visit(x)
            visit(a)
    assert len(seen)==len(set(seen))==meta['available']
    review=json.loads((ROOT/'data/returned_review.json').read_text())['entries'];revised=overlay(rows,review)
    assert len(review)==meta['returned_criteria'] and sum(r['changed'] for r in review)==meta['changed_grades']
    requests=json.loads((ROOT/'data/request_inventory.json').read_text())
    assert len(requests)==len(by) and {r['record_id'] for r in requests}==set(by)
    for r in requests:
        assert r['record_id'] in by
        for req in r['request_sequence']:
            if 'messages' in req:assert hashlib.sha256(json.dumps(req['messages'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()==req['messages_sha256']
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([sys.executable,str(ROOT/'analysis.py'),'--output',tmp],check=True,capture_output=True)
        for p in pathlib.Path(tmp).iterdir():assert p.read_bytes()==(ROOT/'results'/p.name).read_bytes(),p.name
    expected={}
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        sha,name=line.split('  ',1)
        assert name not in expected and not pathlib.PurePosixPath(name).is_absolute() and '..' not in pathlib.PurePosixPath(name).parts
        expected[name]=sha
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and not any(x in ('.git','__pycache__') for x in p.relative_to(ROOT).parts) and p.name not in ('SHA256SUMS','.DS_Store')}
    assert actual==set(expected), 'Checksum inventory differs from delivered files'
    print(json.dumps({'slots':len(rows),'exact_answers':len(seen),'matching_nested_spans':spans,'returned_criteria':len(review),
                      'analysis_reproduced':True,'integrity_not_scientific_certification':True},indent=2))

if __name__=='__main__':main()
