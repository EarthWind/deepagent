"""Capture source fingerprints and generate permanent links; no network or mutations upstream."""
import csv
import hashlib
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(sys.argv[1]).resolve()
PIN = 'bee849b228d1cb076a8f2ac839335f43399febe1'
gitdir = ROOT / '.git'
if not gitdir.is_dir():
    raise SystemExit('Pass a normal git clone with a .git directory.')
head = (gitdir / 'HEAD').read_text().strip()
if head.startswith('ref: '):
    ref = head[5:]
    loose = gitdir / ref
    if loose.exists():
        head = loose.read_text().strip()
    else:
        refs = (gitdir / 'packed-refs').read_text().splitlines()
        head = next(line.split(' ')[0] for line in refs if line.endswith(' ' + ref))
if head != PIN:
    raise SystemExit(f'Wrong source revision: {head}; expected {PIN}')
URL = f'https://github.com/code-yeongyu/oh-my-openagent/blob/{PIN}/'
records = []
with (BASE / 'source-map.tsv').open() as f:
    for row in csv.DictReader(f, delimiter='\t'):
        data = (ROOT / row['path']).read_bytes()
        records.append({**row, 'url': URL + row['path'], 'sha256': hashlib.sha256(data).hexdigest(), 'lines': len(data.splitlines())})
package = json.loads((ROOT / 'package.json').read_text())
snapshot = {
    'repository': 'https://github.com/code-yeongyu/oh-my-openagent.git',
    'research_date': '2026-09-16',
    'timezone': 'Asia/Shanghai',
    'branch_at_capture': 'dev',
    'commit': PIN,
    'commit_time': '2026-09-16T23:46:32+09:00',
    'root_package_name': package['name'],
    'root_package_version': package['version'],
    'native_version': json.loads((ROOT / 'packages/omo-native/package.json').read_text())['version'],
    'workspace_count': len(package['workspaces']),
    'evidence_files': records,
}
(BASE / 'snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n')
md = ['# 固定提交源码索引', '', f'所有链接均固定在 `{PIN}`。文件 SHA-256 和行数见 [snapshot.json](snapshot.json)。', '', '下列文件用于交叉核对正文；这是一组有选择的源码阅读记录，不代表逐行审计整个项目。', '', '| 标识 | 源码 | 阅读重点 |', '| --- | --- | --- |']
for row in records:
    md.append(f"| `{row['id']}` | [{row['path']}]({row['url']}) | {row['说明']} |")
(BASE / 'sources.md').write_text('\n'.join(md) + '\n')
(BASE / 'references.md').write_text('\n'.join(f"[{row['id']}]: {row['url']}" for row in records) + '\n')
print(f'Captured {len(records)} source fingerprints; {len(package["workspaces"])} workspace declarations.')
