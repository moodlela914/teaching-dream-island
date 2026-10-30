"""Synchronize canonical Markdown to JSON, branding and text alternative."""
from pathlib import Path
import subprocess,sys,shutil,json

def sync(project,initialize=False):
    root=Path(project).resolve();node=shutil.which('node')
    if not node:raise RuntimeError('Node.js is required; locate the bundled runtime or install it before continuing.')
    command=[node,str(root/'site/scripts/sync-materials.mjs')]
    if initialize:command.append('--init')
    result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
    if result.returncode:raise ValueError(result.stderr.strip() or result.stdout.strip())
    return len(json.loads((root/'site/data/content.json').read_text(encoding='utf-8'))['courses'])

if __name__=='__main__':
    try:print('Synchronized',sync(Path(sys.argv[1]).resolve()),'courses from Markdown.')
    except (ValueError,RuntimeError) as e:sys.exit(str(e))
