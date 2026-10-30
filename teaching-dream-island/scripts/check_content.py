"""Validate semantic content invariants; not a substitute for browser acceptance."""
from pathlib import Path
from urllib.parse import urlparse
import argparse,json,subprocess,shutil

def check(project,release=False):
    root=Path(project);node=shutil.which('node')
    if not node:return ['Node.js is required to validate Markdown sources.']
    result=subprocess.run([node,str(root/'site/scripts/sync-materials.mjs'),'--check'],capture_output=True,text=True,encoding='utf-8')
    if result.returncode:return [result.stderr.strip() or result.stdout.strip()]
    d=json.loads((root/'site/data/content.json').read_text(encoding='utf8'));problems=[]
    def need(ok,message):
        if not ok:problems.append(message)
    courses=d['courses'];ids=[c['id'] for c in courses]
    need(len(set(ids))==len(ids),'Duplicate course IDs');need([c['order'] for c in courses]==list(range(1,len(courses)+1)),'Course order must be consecutive')
    need(ids==[f'island-{i+1:02}' for i in range(len(courses))],'Scene expects island-01 consecutive IDs')
    need(d['center']['name']==d['site']['title'],'Center name differs from site title')
    quiz_ids=[]
    for c in courses:
        need(bool(c['blocks']) and all(b.get('title') and b.get('text') for b in c['blocks']),c['id']+': missing lesson content')
        need(len(c['quiz'])==4,c['id']+': needs four questions')
        for q in c['quiz']:
            quiz_ids.append(q['id']);options=[o['id'] for o in q['options']]
            need(len(options)==4 and len(set(options))==4,q['id']+': needs four distinct option IDs')
            need(q['answer'] in options and bool(q['explanation']),q['id']+': invalid answer/explanation')
        for l in c['links']:need(urlparse(l['url']).scheme in ['https','http'],c['id']+': unsafe/missing URL')
        need('worksheet' not in c,c['id']+': worksheet feature must not return')
    need(len(set(quiz_ids))==len(quiz_ids),'Question IDs must be globally unique')
    people=d['residents'];need(len(people)==14,'Requires fourteen residents')
    for key in ['id','name','concept']:need(len({r[key] for r in people})==14,'Residents need distinct '+key)
    for r in people:
        need(r['island'] in ids,r['id']+': missing course')
        if r['island'] in ids:need(0<=r['topic']<len(courses[ids.index(r['island'])]['blocks']),r['id']+': missing source topic')
    speaker=d.get('speaker')
    if speaker and speaker.get('image'):need((root/'site'/speaker['image']).is_file(),'Speaker image missing')
    if release:
        need('示意教材：此內容僅供模板操作測試' not in d.get('editorialNote',''),'Replace template content before release')
        need(all('自編示意第' not in q['question'] for c in courses for q in c['quiz']),'Replace demonstration questions before release')
        need(all('本課練習「' not in b['text'] or not b['text'].startswith('示意｜') for c in courses for b in c['blocks']),'Replace demonstration lesson blocks before release')
    return problems

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');p.add_argument('--release',action='store_true');a=p.parse_args();errors=check(a.project,a.release)
    if errors:p.exit(1,'\n'.join(errors)+'\n')
    print('PASS content structure; browser and source verification still required.')
