"""Build original SVG diagrams and a self-contained, offline HTML blog.
Requires Python 3 and markdown-it-py==3.0.0. No CDN or remote image assets.
"""
from pathlib import Path
import html
import json
import re
import unicodedata
from markdown_it import MarkdownIt

BASE = Path(__file__).resolve().parent.parent
ASSETS = BASE / 'assets'
INK, MUTED, TEAL, BLUE, AMBER, RED = '#183443', '#566a76', '#087e83', '#4269ae', '#a36321', '#b2484e'
checks = []

def esc(value):
    return html.escape(str(value), quote=True)

def wrap(text, width, size):
    result, line, units = [], '', 0
    for char in text:
        step = 1 if unicodedata.east_asian_width(char) in 'WF' else .58
        if units + step > width / size and line:
            result.append(line)
            line, units = '', 0
        line += char
        units += step
    if line:
        result.append(line)
    return result

class Figure:
    def __init__(self, name, title, subtitle, height=810):
        self.name, self.height = name, height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title><desc id="desc">{esc(subtitle)}</desc>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M1,1 L8,4.5 L1,8" fill="none" stroke="#788e99" stroke-width="1.5"/></marker></defs>
<rect width="1280" height="{height}" rx="18" fill="#f4f8f8"/>
<path d="M18 0 H1262 Q1280 0 1280 18 V8 H0 V18 Q0 0 18 0" fill="{TEAL}"/>
<g font-family="Noto Sans CJK SC, Microsoft YaHei, PingFang SC, sans-serif">''']
        self.text(44, 48, 'RUFLO  /  SOURCE NOTES     '+name[:2], 15, TEAL, 700)
        self.text(44, 97, title, 31, INK, 700)
        self.text(44, 133, subtitle, 18, MUTED)

    def text(self, x, y, text, size=20, color=INK, weight=400):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{esc(text)}</text>')

    def rect(self,x,y,w,h,fill='white',stroke='#d3e0e4'):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}"/>')

    def card(self,x,y,w,h,title,lines,color=BLUE,size=20):
        self.parts.append(f'<g data-card="{esc(title)}" data-x="{x}" data-y="{y}" data-w="{w}" data-h="{h}">')
        self.rect(x,y,w,h)
        self.parts.append(f'<rect x="{x}" y="{y+16}" width="4" height="{h-32}" rx="2" fill="{color}"/>')
        title_lines=wrap(title,w-40,23)
        ty=y+36
        for line in title_lines:
            self.text(x+20,ty,line,23,color,700);ty+=30
        ty+=5
        for line in lines:
            for part in wrap(line,w-42,size):
                self.text(x+20,ty,part,size);ty+=29
        if ty-29 > y+h-12:
            raise ValueError(f'card overflow {self.name} {title}: {ty-29} > {y+h-12}')
        self.parts.append('</g>')
        checks.append({'figure':self.name,'card':title,'vertical_fit':True})

    def arrow(self,x1,y1,x2,y2,via=None):
        points=[(x1,y1)]+(via or [])+[(x2,y2)]
        d='M'+' L'.join(f'{x},{y}' for x,y in points)
        self.parts.append(f'<path d="{d}" fill="none" stroke="#788e99" stroke-width="2" marker-end="url(#arrow)"/>')

    def band(self,y,title,body,color=TEAL):
        self.rect(44,y,1192,88,'#e8f2f2','#c6dcdf')
        self.text(65,y+32,title,22,color,700)
        self.text(65,y+62,body,19,INK)

    def save(self,source):
        self.text(44,self.height-26,'原创源码示意 · 6f0ed7112873 · 2026-09-17  |  '+source,14,MUTED)
        self.parts.append('</g></svg>')
        (ASSETS/(self.name+'.svg')).write_text('\n'.join(self.parts))


def figures():
    f=Figure('01-architecture','Ruflo 的系统边界：从宿主扩展到执行基础设施','读取默认入口与可选模块，避免把整个仓库画成一个必经的运行引擎。',880)
    f.card(44,172,372,135,'行为资产',['Agents / Skills / Commands','CLAUDE.md 与项目约定'],TEAL)
    f.card(454,172,372,135,'宿主运行时',['Claude Code / Codex','会话、原生工具、子 Agent'],BLUE)
    f.card(864,172,372,135,'集成入口',['CLI / MCP / Hooks','初始化、事件与工具调用'],TEAL)
    f.arrow(416,235,454,235);f.arrow(826,235,864,235)
    f.arrow(1050,307,1050,353);f.arrow(640,307,640,353)
    f.card(44,356,1192,138,'Ruflo 控制与状态',['Agent / Swarm / Workflow 记录  ·  策略授权  ·  模型路由  ·  记忆检索  ·  反馈','MCP handler 将调用连接到具体实现；部分 CLI 命令也直接调用服务。'],TEAL)
    for x in (230,640,1050):f.arrow(x,494,x,534)
    f.card(44,538,372,165,'宿主进程执行',['原生子 Agent','claude -p / codex exec','有工具的编码执行'],BLUE)
    f.card(454,538,372,165,'直接 Provider 请求',['agent_execute','文本输入 → 文本结果','本路径无工具调用循环'],AMBER)
    f.card(864,538,372,165,'独立 / 可选模块',['Swarm 库与 Federation','AgentDB / RuVector','WASM / 云运行时'],BLUE)
    f.band(732,'状态与依赖并非单一后端','JSON 协调记录  +  SQLite / AgentDB  +  路由经验  +  宿主工作目录')
    f.save('wrapper · mcp-client · agent-execute-core · codex/dual-mode')

    f=Figure('02-hooks','Hooks：让宿主生命周期连接工程反馈','下列为 CLI 设置生成器中的主要映射；是否安装取决于组件与事件配置。',875)
    columns=[44,376,788]
    for x,label in zip(columns,['宿主事件','本地 helper','作用']):f.text(x,178,label,18,TEAL,700)
    rows=[
        ('SessionStart','session-restore + import','恢复会话与自动记忆'),
        ('UserPromptSubmit','route','注入上下文、输出角色建议'),
        ('PreToolUse','pre-bash / pre-edit','工具执行前检查与处理'),
        ('PostToolUse','post-edit / post-bash','记录结果、区分成功与失败'),
        ('SubagentStop','post-task','记录子任务完成线索'),
        ('PreCompact','compact + session-end','保存压缩前的上下文线索'),
        ('Stop / SessionEnd','sync / session-end','同步记忆、持久化会话'),
    ]
    for i,row in enumerate(rows):
        y=201+i*70
        f.rect(44,y,1192,54)
        for x,t in zip(columns,row):f.text(x+14,y+35,t,20)
    f.band(720,'反馈边界','工具正常返回只是代理信号；任务正确性还需要测试、审查或用户验收。',AMBER)
    f.save('init/settings-generator.ts · helpers-generator.ts · hook-handler.cjs')

    f=Figure('03-execution','Agent 注册记录与执行运行时是两件事','agent_spawn 持久化身份；agent_execute 与宿主子 Agent 分别承担不同类型的执行。',830)
    f.card(44,179,350,160,'agent_spawn',['校验参数、选择模型','写 Agent JSON 记录','返回 registered；记录 idle'],TEAL)
    f.card(464,179,340,160,'agent_execute',['读取记录 → busy','taskCount 增加','调用 Provider'],BLUE)
    f.card(874,179,362,160,'文本 Provider',['system + user message','本路径不发送 tools','返回 text + usage'],AMBER)
    f.arrow(394,259,464,259);f.arrow(804,259,874,259)
    f.arrow(1055,339,1055,393);f.arrow(1055,393,636,393);f.arrow(636,393,636,432)
    f.card(464,436,772,144,'持久化执行结果',['busy → idle；成功时保存 lastResult','尽力记录路由反馈；API 成功不等于任务通过验收'],TEAL)
    f.card(44,436,350,144,'宿主子 Agent',['原生 Task / 外部 CLI','工具调用与文件操作','需要单独执行链'],BLUE)
    f.band(621,'本次实测','注册产生 0 次模型请求；执行产生 1 次 fixture 请求；请求体无 tools。')
    f.text(44,758,'实验不调用真实 LLM，不评估输出正确性或端到端编码完成率。',19,MUTED)
    f.save('mcp-tools/agent-tools.ts · agent-execute-core.ts')

    f=Figure('04-swarm','Swarm 有三层：状态、调度、传输','这三层可以组合，但 CLI 初始化一条协调记录并不自动等于启动分布式集群。',820)
    f.card(44,178,1192,125,'① CLI Swarm 状态工具',['swarm_init → swarm-state.json；记录 topology / agents / tasks / config','这一入口没有直接实例化 UnifiedSwarmCoordinator。'],TEAL)
    f.card(44,338,1192,172,'② 独立 UnifiedSwarmCoordinator',['AgentPool + TopologyManager + MessageBus + ConsensusEngine','任务 → 能力 / 负载 / 健康评分 → task_assign → Worker → completion','运行期包含队列、心跳、健康检查与任务状态更新。'],BLUE)
    f.card(44,548,575,145,'③ 默认 LocalTransport',['同一 Node 进程的 registry','节点消息与可观测事件分离','可注入测试与签名辅助机制'],BLUE)
    f.card(661,548,575,145,'③ 可选 FederationTransport',['跨进程 / 节点传输适配','需要身份、网络和 Worker 接线','不能从拓扑配置推断已启用'],AMBER)
    f.arrow(334,510,334,548);f.arrow(949,510,949,548)
    f.text(44,747,'共识一致性解决状态协调；模型答案正确性仍依赖外部验证。',22,TEAL,700)
    f.save('swarm-tools · unified-coordinator · consensus/transport')

    f=Figure('05-memory','一次记忆检索：先确认走了哪条路径','存储可用、向量存在、语义正确、索引启用，是四种不同的状态。',985)
    f.card(44,175,1192,110,'入口：memory search / searchEntries',['按 namespace / provenance 等条件检索；首先尝试 AgentDB bridge。'],TEAL)
    f.arrow(334,285,334,329);f.arrow(949,285,949,329)
    f.card(44,333,575,208,'A · Bridge 可用就直接返回',['最近更新的 1,000 条候选','逐条 cosine + BM25 + 关键词覆盖','加权融合、阈值过滤、排序','这一实现不是全库 HNSW 或 RRF'],BLUE)
    f.card(661,333,575,208,'B · Bridge 不可用时回退',['sql.js SQLite 路径','尝试 RaBitQ 候选与精排','再尝试 HNSW，继续回退搜索','是否命中索引由运行状态决定'],BLUE)
    f.card(44,578,1192,132,'可选 SmartRetrieval 包装层',['多查询扩展 → RRF → 时间加权 → MMR → session 多样性','SearchFn 可来自不同原始后端；CLI --smart 需要相应包接口可用。'],TEAL)
    f.band(746,'嵌入链路必须独立检查','真实模型不可用 → hash-fallback / backend: mock；不能当作可靠语义检索。',AMBER)
    f.text(44,886,'RUFLO_REQUIRE_REAL_EMBEDDINGS=1 可拒绝 hash 兜底。',22,AMBER,700)
    f.save('memory-initializer · memory-bridge · memory/smart-retrieval')

    f=Figure('06-learning','“自学习”需要回答：谁被更新，依据是什么？','默认路由与局部经验更新可工作；远端基础模型权重并未因此被训练。',850)
    f.card(44,180,372,166,'角色建议',['Hook 静态关键词规则','命中 confidence = 0.6','未命中默认 coder / 0.3'],BLUE)
    f.card(454,180,372,166,'模型路由',['启发式复杂度 + bandit','Beta(α, β) 先验','神经路由另有开关与依赖'],BLUE)
    f.card(864,180,372,166,'局部经验',['轨迹与 ReasoningBank','模式 confidence 更新','可选局部向量适配'],TEAL)
    f.arrow(640,346,640,401)
    f.card(44,405,1192,138,'实际闭环：选择模型 → Provider 请求 → 记录 outcome → 更新路由经验',['agent_execute 当前将 API 成功作为正反馈；轨迹质量信号较粗。','代码是否正确、测试是否通过、用户是否接受，需要额外证据。'],TEAL)
    f.arrow(640,543,640,584)
    f.card(44,588,575,136,'已观察到的更新对象',['JSON 经验、局部统计与模式','局部适配器 / 可选外部后端'],BLUE)
    f.card(661,588,575,136,'仍需独立评价的目标',['任务通过率与成本收益','记忆污染、过拟合和错误奖励'],AMBER)
    f.save('helpers-generator · model-router · intelligence · lora-adapter')

    f=Figure('07-federation','Federation：消息可信与任务可执行要分别授权','以下是概念调用路径；会话 HMAC、节点签名和具体 transport 属于不同实现层。',866)
    f.card(44,181,372,164,'出站控制',['节点 active / session 检查','消息类型与信任策略','预算、跳数、累计花费'],TEAL)
    f.card(454,181,372,164,'消息处理',['PII 转换或阻断','构造 envelope / nonce','调用签名与路由接口'],BLUE)
    f.card(864,181,372,164,'传输适配',['会话与目标节点','发送结果与错误','审计 sent / rejected'],BLUE)
    f.arrow(416,263,454,263);f.arrow(826,263,864,263)
    f.arrow(1050,345,1050,402);f.arrow(1050,402,230,402);f.arrow(230,402,230,442)
    f.card(44,446,575,168,'入站 Dispatcher',['检查来源节点、active 状态与签名','根据配置执行授权并写入审计','通过门禁后发出类型化事件'],TEAL)
    f.card(661,446,575,168,'业务集成方 / Worker',['接收事件后决定是否执行任务','独立检查执行能力与资源预算','返回结果，并补充质量证据'],BLUE)
    f.arrow(619,530,661,530)
    f.band(658,'信任不是任务执行权限的替代物','历史成功率、在线率、威胁与完整性共同评分；最高级升级包含人工批准要求。',AMBER)
    f.save('federation-coordinator · routing-service · inbound-dispatcher · trust-evaluator')

    f=Figure('08-workflow','Workflow：已经接线的执行与尚未完成的语义','此图仅描述 CLI workflow_execute 处理器，不代表所有独立编排模块。',840)
    f.card(44,180,372,174,'已执行的类型',['task → executeAgentTask','wait → 有界等待','condition → 有限条件与跳转'],TEAL)
    f.card(454,180,372,174,'尚未执行的类型',['parallel → skipped','loop → skipped','整体仍可能返回 completed'],AMBER)
    f.card(864,180,372,174,'状态与变量',['每步前后保存进度','步骤间检查暂停 / 取消','task 结果写入变量'],BLUE)
    f.card(44,404,1192,131,'复现 ① 自动步骤 ID 的插值不匹配',['{{lastStepOutput}} → fixture-output-2','{{step-1.output}} → 原样保留；正则匹配范围不含连字符'],AMBER)
    f.card(44,573,1192,131,'复现 ② 无活动 runner 时，resume 只改变状态',['paused → workflow_resume → running','随后 workflow_execute → Workflow already running；没有自动重启 runner'],AMBER)
    f.text(44,760,'研究用 fixture 实验；未修改上游实现，也未运行真实模型。',20,MUTED)
    f.save('mcp-tools/workflow-tools.ts · examples/probe.mjs')
    (BASE/'research/diagram-layout-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')


def blog():
    raw=(BASE/'README.md').read_text()
    body=re.sub(r'^---\n.*?\n---\n','',raw,count=1,flags=re.S)
    md=MarkdownIt('commonmark',{'html':True}).enable('table')
    rendered=md.render(body)
    headings=[]
    count=0
    def heading(match):
        nonlocal count
        count+=1
        text=re.sub('<[^>]+>','',match.group(1))
        slug='section-'+str(count)
        headings.append((slug,text))
        return f'<h2 id="{slug}">{match.group(1)}</h2>'
    rendered=re.sub(r'<h2>(.*?)</h2>',heading,rendered)
    rendered=re.sub(r'<table>(.*?)</table>',r'<div class="table-scroll"><table>\1</table></div>',rendered,flags=re.S)
    rendered=re.sub(r'<p><img src="(assets/[^"]+)" alt="([^"]*)" /></p>',r'<figure><a href="\1" target="_blank" title="打开原尺寸架构图"><img src="\1" alt="\2" loading="lazy" /></a><figcaption>\2 · 点击查看原图</figcaption></figure>',rendered)
    nav=''.join(f'<a href="#{slug}">{esc(text)}</a>' for slug,text in headings)
    css='''
:root{--paper:#fbfcfa;--ink:#173342;--muted:#59717c;--accent:#087e83;--border:#dce5e7;--panel:#eff5f4;--code:#16313e}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:32px}body{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Sans CJK SC","Microsoft YaHei",system-ui,sans-serif;line-height:1.85;font-size:16px}
a{color:var(--accent);text-underline-offset:4px}a:hover{color:#b06b26}.top{background:#102e3a;color:#d9e8eb;padding:34px max(28px,calc((100vw - 1390px)/2));border-bottom:5px solid #169293}.brand{letter-spacing:3px;font-size:13px;font-weight:750}.top p{margin:10px 0 0;color:#a9c4cc;font-size:14px}.top a{color:#d9e8eb}
.layout{max-width:1450px;margin:auto;display:grid;grid-template-columns:260px minmax(0,1fr);gap:52px;padding:44px 32px 100px}aside{align-self:start;position:sticky;top:26px;max-height:calc(100vh - 55px);overflow:auto;font-size:13px;scrollbar-width:thin}aside strong{display:block;letter-spacing:2px;color:var(--muted);font-size:12px;margin-bottom:16px}aside a{display:block;text-decoration:none;border-left:2px solid var(--border);padding:7px 14px;color:var(--muted);line-height:1.55}aside a:hover{border-color:var(--accent);background:var(--panel)}main{min-width:0;max-width:1050px}h1{font-size:clamp(28px,3.1vw,43px);line-height:1.4;letter-spacing:-.8px;margin:0 0 30px;font-weight:800}h2{font-size:28px;line-height:1.45;margin:72px 0 24px;padding-top:26px;border-top:1px solid var(--border);letter-spacing:-.4px}h3{font-size:21px;margin:36px 0 16px;line-height:1.6}p{margin:18px 0}blockquote{margin:26px 0;background:var(--panel);border-left:4px solid var(--accent);padding:8px 24px;font-size:14px;color:#476471}blockquote p{margin:12px 0}strong{font-weight:750}ul,ol{padding-left:25px}li{margin:8px 0}pre{background:var(--code);color:#e0edf1;padding:22px 25px;overflow:auto;border-radius:10px;line-height:1.75;font-size:13px;tab-size:2}code{font-family:"DejaVu Sans Mono",Consolas,monospace;font-size:.88em;overflow-wrap:anywhere;background:#eaf0ef;padding:2px 5px;border-radius:4px}pre code{background:none;padding:0;color:inherit;overflow-wrap:normal;font-size:inherit}.table-scroll{overflow-x:auto;margin:24px 0;border:1px solid var(--border);border-radius:10px}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.75}th{text-align:left;background:#e9f1f1;color:#1a5963;font-weight:700}th,td{padding:14px 16px;border-bottom:1px solid var(--border);vertical-align:top}tr:last-child td{border-bottom:0}tr:nth-child(even) td{background:#f5f8f7}figure{margin:32px 0}figure img{display:block;width:100%;height:auto;border-radius:12px;border:1px solid var(--border)}figcaption{font-size:12px;color:var(--muted);margin:10px 2px;line-height:1.6}footer{border-top:1px solid var(--border);padding:32px;color:var(--muted);font-size:13px;text-align:center}::selection{background:#bae3df}
@media(max-width:1080px){.layout{grid-template-columns:205px minmax(0,1fr);gap:28px;padding:30px 24px}.layout aside{font-size:12px}h2{font-size:25px}}
@media(max-width:760px){.layout{display:block;padding:28px 18px 65px}aside{position:static;max-height:none;display:none}h1{font-size:29px}h2{font-size:23px;margin-top:52px}body{font-size:15px}blockquote{padding:5px 15px}th,td{padding:10px 12px;min-width:120px}pre{padding:17px}figure{margin-left:0;margin-right:0}.top{padding:25px 18px}}
@media print{aside,.top,footer{display:none}.layout{display:block;padding:0}main{max-width:none}body{font-size:11pt;background:white}h2{break-after:avoid;margin-top:25px}figure,pre{break-inside:avoid}a{color:inherit;text-decoration:none}.table-scroll{overflow:visible}pre{white-space:pre-wrap}h1{font-size:25pt}}
'''
    output=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="基于 Ruflo 3.42.0 固定源码提交的中文工程博客，包含八张原创架构图、调用链分析和可复现实验。"><title>Ruflo 源码深度解读 · Agent 工程笔记</title><style>{css}</style></head><body><header class="top"><div class="brand">AGENT ENGINEERING / SOURCE NOTES</div><p>RUFLO 3.42.0 · 2026.09.17 · 6f0ed7112873 &nbsp; / &nbsp; <a href="README.md">Markdown</a> · <a href="research/verification.md">实验记录</a></p></header><div class="layout"><aside aria-label="文章目录"><strong>阅读目录</strong>{nav}</aside><main>{rendered}</main></div><footer>固定源码快照 · 8 张原创架构图 · 7 组源码实验 · 离线可读，无外部脚本或字体依赖</footer></body></html>'''
    (BASE/'index.html').write_text(output)

if __name__=='__main__':
    ASSETS.mkdir(exist_ok=True)
    figures()
    blog()
    print('Built 8 diagrams and index.html; card layout checks:',len(checks))
