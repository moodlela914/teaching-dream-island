"""Copy the runnable template into a new project without touching input material."""
from pathlib import Path
import argparse, json, shutil, re
from copy import deepcopy
from sync_content import sync

def create(output,title,author,slug,count,theme='nature'):
    target=Path(output).resolve()
    if target.exists(): raise ValueError('Output already exists; choose a new project directory.')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug): raise ValueError('Slug must use lowercase letters, numbers and hyphens.')
    if not isinstance(count,int) or count<1: raise ValueError('Course count must be a positive integer chosen from the teaching content.')
    if theme not in ['nature','ocean','space','halloween','custom']:raise ValueError('Choose a supplied theme or custom, then adapt appearance and decorations to the material.')
    template=Path(__file__).resolve().parents[1]/'assets/site-template'
    shutil.copytree(template,target/'site',ignore=shutil.ignore_patterns('islands'))
    (target/'scripts').mkdir();shutil.copyfile(Path(__file__).with_name('serve.cjs'),target/'scripts/serve.cjs')
    (target/'materials').mkdir();(target/'_shots').mkdir()
    file=target/'site/data/content.json';data=json.loads(file.read_text(encoding='utf8'))
    data['site'].update(title=title,author=author,slug=slug)
    data['center']['name']=title
    seed=data['courses'];data['courses']=[]
    for i in range(count):
        c=deepcopy(seed[i%len(seed)]);c['id']=f'island-{i+1:02}';c['order']=i+1
        if i>=len(seed):c['name']=f'主題探索島 {i+1:02}（示意）'
        for j,q in enumerate(c['quiz']):q['id']=f'{c["id"]}-q{j+1}'
        data['courses'].append(c)
    label={'nature':'自然探索','ocean':'海洋探險','space':'星際探索','halloween':'可愛萬聖節','custom':'自訂主題'}[theme]
    data['appearance']={'theme':theme,'label':label,'colors':{}}
    data['themes']['style']=label
    for i,person in enumerate(data['residents']):
        c=data['courses'][i%count];person['island']=c['id'];person['topic']=i%len(c['blocks'])
    file.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    spec={'name':title,'author':author,'slug':slug,'courseCount':count,'courses':[{'id':c['id'],'name':c['name'],'source':None} for c in data['courses']],'appearance':data['appearance'],'residentCount':14,'certificate':{'allRead':True,'minimumScore':75,'worksheetsRequired':False},'publishMaterials':False,'deployment':{'platform':None,'authorized':False,'policy':'先本機確認；僅於使用者主動提出本次發布後部署；歷史授權不沿用'},'contentStatus':'示意模板，須依教材完整替換'}
    (target/'project.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    sync(target,initialize=True)
    return target

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True);p.add_argument('--title',default='教學夢幻島');p.add_argument('--author',default='教材作者（示意）');p.add_argument('--slug',default='teaching-dream-island');p.add_argument('--courses',type=int,required=True);p.add_argument('--theme',choices=['nature','ocean','space','halloween','custom'],default='nature')
    a=p.parse_args()
    try: print(create(a.output,a.title,a.author,a.slug,a.courses,a.theme))
    except ValueError as e:p.exit(2,str(e)+'\n')
