"""Build original engineering figures and an offline HTML edition of the research blog.

Requires Python 3 and markdown-it-py. No browser, network, font download or JS CDN.
"""
from pathlib import Path
import html
import re
import unicodedata
from markdown_it import MarkdownIt

BASE = Path(__file__).resolve().parent
ASSETS = BASE / 'assets'
ASSETS.mkdir(exist_ok=True)
INK = '#152c46'
MUTED = '#52677e'
BLUE = '#2866bb'
TEAL = '#087f83'
VIOLET = '#7354b4'
AMBER = '#a35f13'
RED = '#b64c4b'


def esc(value):
    return html.escape(str(value), quote=True)


def wrap(text, width, size=20):
    lines, current, length = [], '', 0
    for c in text:
        unit = 1 if unicodedata.east_asian_width(c) in 'WF' else .56
        if length + unit > width / size and current:
            lines.append(current)
            current, length = '', 0
        current += c
        length += unit
    if current:
        lines.append(current)
    return lines


class Figure:
    def __init__(self, name, title, subtitle, height=780):
        self.name, self.height = name, height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-labelledby="title desc">
<title id="title">{esc(title)}</title><desc id="desc">{esc(subtitle)}</desc>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto-start-reverse"><path d="M0,1 L8,5 L0,9" fill="none" stroke="#70849a" stroke-width="1.6"/></marker></defs>
<rect width="1280" height="{height}" rx="20" fill="#f5f8fc"/>
<rect x="0" width="1280" height="8" rx="4" fill="{TEAL}"/>
<g font-family="Noto Sans CJK SC, Microsoft YaHei, PingFang SC, sans-serif">''']
        self.text(44, 58, f'OMO / ENGINEERING NOTES   •   {name[:2]}', 15, TEAL, 700)
        self.text(44, 108, title, 33, INK, 700)
        self.text(44, 140, subtitle, 18, MUTED)

    def text(self, x, y, text, size=20, color=INK, weight=400):
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}">{esc(text)}</text>')

    def rect(self, x, y, w, h, fill='white', stroke='#d7e1ed', radius=14):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

    def card(self, x, y, w, h, title, lines, color=BLUE, size=20):
        self.rect(x, y, w, h)
        self.parts.append(f'<rect x="{x}" y="{y+14}" width="5" height="{h-28}" rx="2" fill="{color}"/>')
        self.text(x + 20, y + 37, title, 23, color, 700)
        ty = y + 72
        for line in lines:
            for part in wrap(line, w - 42, size):
                self.text(x + 20, ty, part, size, INK)
                ty += 28
        if ty - 28 > y + h - 12:
            raise ValueError(f'Overflow: {self.name}: {title}')

    def arrow(self, x1, y1, x2, y2, via=None):
        points = [(x1, y1)] + (via or []) + [(x2, y2)]
        d = 'M' + ' L'.join(f'{x},{y}' for x, y in points)
        self.parts.append(f'<path d="{d}" stroke="#70849a" stroke-width="2.2" fill="none" marker-end="url(#arrow)"/>')

    def band(self, y, title, body, color=TEAL):
        self.rect(44, y, 1192, 86, '#eaf4f5', '#c6e2e4')
        self.text(66, y + 32, title, 21, color, 700)
        self.text(66, y + 62, body, 18, INK)

    def save(self, source):
        self.text(44, self.height - 25, f'原创源码示意 · bee849b228d1 · 2026-09-16  |  {source}', 14, MUTED)
        self.parts.append('</g></svg>')
        (ASSETS / f'{self.name}.svg').write_text('\n'.join(self.parts))


def figures():
    f = Figure('01-architecture', '同一套工程能力，三种宿主接入方式', '将资产与可复用机制下沉；将会话、事件、工具注册留在适配层。', 850)
    f.card(44, 180, 376, 134, 'OpenCode · Ultimate', ['TypeScript 插件 / SDK 会话', '工具 + 生命周期 Hook'], BLUE)
    f.card(452, 180, 376, 134, 'Codex · Light', ['插件清单 / 事件组件', 'Skills + MCP + 宿主协作'], VIOLET)
    f.card(860, 180, 376, 134, 'Native · Senpi Beta', ['omo-ai 启动固定 Senpi 引擎', '任务图 + 记忆扩展接线'], TEAL)
    f.parts.append('<path d="M232,315 V342 H1048 V315 M640,315 V342" stroke="#70849a" stroke-width="2.2" fill="none"/>')
    f.text(44, 365, '共享能力层', 15, MUTED)
    for x in [232, 640, 1048]:
        f.arrow(x, 343, x, 374)
    f.card(44, 378, 376, 135, '行为与路由', ['prompts-core / model-core', '角色、分类、Skill、模型候选链'], BLUE)
    f.card(452, 378, 376, 135, '执行与协作', ['team-core / delegate-core', '任务认领、消息、配额与重试'], VIOLET)
    f.card(860, 378, 376, 135, '记忆与工具', ['memory-core / hashline-core', '版本化文件、检索、编辑锚点'], TEAL)
    f.card(44, 552, 1192, 100, '宿主专用的执行系统', ['OpenCode BackgroundManager  /  Codex 原生协作  /  senpi-task 的任务与 DAG 引擎'], AMBER)
    f.band(693, '运行边界', '模型推理、基础工具与权限依赖宿主；共享包存在，不表示三个版本全部启用相同能力。')
    f.save('package.json · plugin-interface.ts · component-list.ts')

    f = Figure('02-lifecycle', 'OpenCode：装配能力，再接入事件循环', '控制流程以宿主事件为入口；Hook 的异常策略和生效条件各不相同。', 820)
    for x, title, lines, color in [
        (44, '① 配置与启动', ['读取、合并、校验、迁移', '准备宿主与运行上下文'], BLUE),
        (352, '② Managers', ['后台任务 / MCP / tmux', '明确资源生命周期'], VIOLET),
        (660, '③ Tools + Hooks', ['能力发现、注册和过滤', '依赖配置进行装配'], TEAL),
        (968, '④ 宿主接口', ['消息、工具、生命周期', '压缩与退出清理'], BLUE),
    ]:
        f.card(x, 185, 268, 155, title, lines, color, 18)
    for x in [312, 620, 928]:
        f.arrow(x, 262, x + 36, 262)
    f.arrow(1102, 340, 1102, 385)
    f.text(46, 399, '一次执行的主要接缝', 20, MUTED, 700)
    f.card(44, 425, 356, 150, '模型输入', ['消息变换 / 能力描述', '关键词、参数与上下文注入'], BLUE)
    f.card(462, 425, 356, 150, '工具调用', ['before：检查与参数处理', '宿主执行 → after：结果增强'], TEAL)
    f.card(880, 425, 356, 150, '生命周期事件', ['完成 / 错误 / idle / 压缩', '通知、恢复、继续或结束'], VIOLET)
    f.arrow(400, 495, 458, 495)
    f.arrow(818, 495, 876, 495)
    f.arrow(1058, 575, 222, 575, [(1058, 618), (222, 618)])
    f.text(478, 643, '满足继续条件时进入下一轮', 18, MUTED)
    f.band(682, '关键区分', '提示词规定工作方法；工具前 Hook 可阻止动作；底层权限和模型循环仍由宿主负责。')
    f.save('create-plugin-module.ts · plugin-interface.ts · tool-execute-before.ts')

    f = Figure('03-background', '把逻辑任务与每次执行尝试分开', '旧会话可能迟到；当前 attempt 的身份决定哪些状态可以投影回 Task。', 810)
    f.card(44, 184, 338, 170, 'Task：bg_…', ['父会话、任务描述、逻辑状态', 'currentAttemptID', '聚合尝试历史'], BLUE)
    f.card(461, 184, 354, 170, 'Attempt #1', ['模型 A → ses_old', '超时 / 错误 → 保留历史', '迟到 completed 不覆盖新任务'], AMBER)
    f.card(882, 184, 354, 170, 'Attempt #2 · 当前', ['模型 B → ses_new', 'pending → running → 终止', '只有当前尝试投影回 Task'], TEAL)
    f.arrow(382, 267, 457, 267)
    f.arrow(815, 267, 878, 267)
    f.card(44, 419, 562, 177, '接纳与队列', ['模型覆盖 → 独立 model key', '否则可使用 provider key；释放时优先交接槽位', '不是“全局 + Provider + 模型”三层共同限流'], VIOLET)
    f.card(646, 419, 590, 177, '结束与交接', ['活动 / 会话存在性检测 → 终止与资源回收', '结果通知 → 忙碌检查 / 去重 → 唤醒父会话', '父任务读取结果并继续验证'], TEAL)
    f.arrow(1059, 354, 1059, 415)
    f.band(655, '局部实测', '旧 attempt 完成后，Task 仍指向 ses_new 且为 running；配额覆盖行为也已直接调用源码验证。')
    f.save('attempt-lifecycle.ts · concurrency.ts · parent-wake-notifier.ts')

    f = Figure('04-team', '团队协作要有所有权、邮箱和集成边界', 'Team Mode 超出一次性子任务：成员会持续共享任务和交换消息。', 830)
    f.card(44, 182, 330, 146, 'Lead', ['拆分任务、确定成员职责', '协调、读取证据、最终集成'], BLUE)
    f.card(44, 381, 330, 174, 'Members', ['成员 A：接口实现', '成员 B：测试与兼容性', '成员 C：审查'], VIOLET)
    f.card(445, 182, 390, 174, '共享任务存储', ['pending → claimed + owner', '锁外检查 → 获取锁 → 锁内复查', '依赖检查 + 原子写入'], TEAL)
    f.card(445, 416, 390, 174, '成员邮箱', ['普通 / 预留消息 + 消费记录', '收件箱锁、载荷与未读字节限制', '背压、重复 ID 检查、广播权限'], BLUE)
    f.card(906, 182, 330, 174, '可选 Worktree', ['独立代码目录', '合并冲突与验收仍要处理', '文件视图隔离 ≠ 系统沙盒'], AMBER)
    f.card(906, 416, 330, 174, '可选 tmux 展示', ['查看并行会话', '面板生命周期与清理', '展示不替代任务状态'], VIOLET)
    f.arrow(374, 253, 441, 253)
    f.arrow(374, 469, 441, 469)
    f.arrow(835, 269, 902, 269)
    f.arrow(835, 505, 902, 505)
    f.band(665, '不要扩大保证范围', '任务认领原子性 ≠ 所有副作用幂等；逐收件人广播 ≠ 跨全部收件人的事务。')
    f.save('team-tasklist/claim.ts · team-mailbox/send.ts · team-worktree/manager.ts')

    f = Figure('05-dag', '依赖就绪即可推进，Wave 不再是屏障', '示意时长：A=2、B=8、C=3、D=1；至少两个槽位，忽略调度开销。', 910)
    f.card(44, 186, 265, 115, 'A · 需求', ['无依赖 / 2 个时间单位'], BLUE, 18)
    f.card(44, 330, 265, 115, 'B · 测试调查', ['无依赖 / 8 个时间单位'], VIOLET, 18)
    f.card(475, 186, 285, 115, 'C · 实现', ['dependsOn: [A] / 耗时 3'], TEAL, 18)
    f.card(951, 261, 285, 115, 'D · 验证', ['依赖 B + C / 耗时 1'], AMBER, 18)
    f.arrow(309, 242, 471, 242)
    f.arrow(760, 242, 947, 298, [(857, 242), (857, 298)])
    f.arrow(309, 386, 947, 340, [(857, 386), (857, 340)])
    f.text(390, 433, 'C 无需等待 B；D 必须等待 B 和 C 都完成。', 20, INK, 600)
    x0, unit = 246, 73
    f.text(44, 505, '理想化调度对比', 22, INK, 700)
    for t in [0, 2, 5, 8, 9, 11, 12]:
        f.text(x0 + t * unit - 5, 545, str(t), 16, MUTED)
    for y, label, bars in [
        (565, '批次屏障', [(0, 2, 'A', BLUE), (0, 8, 'B', VIOLET), (8, 3, 'C', TEAL), (11, 1, 'D', AMBER)]),
        (667, '依赖前沿', [(0, 2, 'A', BLUE), (0, 8, 'B', VIOLET), (2, 3, 'C', TEAL), (8, 1, 'D', AMBER)]),
    ]:
        f.text(44, y + 30, label, 21, INK, 600)
        for start, duration, label, color in bars:
            yy = y + (39 if label == 'B' else 0)
            f.rect(x0 + start * unit, yy, duration * unit - 5, 32, color, color, 5)
            f.text(x0 + start * unit + 12, yy + 23, label, 18, 'white', 700)
    f.band(784, '调度与数据是两份契约', 'dependsOn 只控制先后；上游结果不会自动插入下游 Prompt。以上时长是算例，不是性能实测。')
    f.save('senpi-task/dag/graph.ts · scheduler.ts · omo-senpi/task/dag-tool.ts')

    f = Figure('06-hashline', 'Hashline：让编辑引用模型刚刚读到的行', '把“定位哪里修改”与“该行是否仍可匹配”连接到工具协议。', 800)
    f.card(44, 185, 558, 156, '① 读取结果', ['1#QH|const count = 1;', '2#TK|return count;'], BLUE)
    f.card(674, 185, 562, 156, '② 编辑请求', ['op: replace   ·   pos: 1#QH', 'lines: ["const count = 2;"]'], TEAL)
    f.arrow(602, 265, 670, 265)
    f.card(44, 408, 558, 164, '③ 核心应用顺序', ['收集锚点 → 对原内容统一验证', '检查重叠 → 去重 → 从后往前编辑', '返回新内容与 no-op / 去重报告'], VIOLET)
    f.card(674, 408, 562, 164, '④ 不匹配时拒绝', ['返回变化行附近的上下文与新锚点', '模型重新读取，再构造编辑', '实验已验证 fresh 成功 / stale 拒绝'], AMBER)
    f.arrow(955, 341, 323, 404, [(955, 372), (323, 372)])
    f.arrow(602, 490, 670, 490)
    f.band(632, '能力边界 · 256 个短标识桶', 'const value = 12; 与 const value = 14; 均得到 HX。短哈希不能证明文件完整性或写入原子性。', RED)
    f.save('hash-computation.ts · validation.ts · edit-operations.ts；示例锚点来自实测')

    f = Figure('07-memory', '外部记忆：源文件、上下文视图和后台写入', '本图对应 Senpi 已接线的 memory-core；不代表其他宿主自动具备相同流程。', 880)
    f.card(44, 184, 340, 176, '版本化记忆仓库', ['Git revision / 可审计文件', 'system：身份、稳定信息', '外部主题、人物与其他记录'], TEAL)
    f.card(469, 184, 341, 176, '上下文编译', ['读取固定 revision', 'self / memory / metadata', '外部路径投影与缓存'], BLUE)
    f.card(895, 184, 341, 176, '模型输入与会话', ['当前任务 + 编译记忆', '按需召回的上下文', '记忆是外部状态，不是权重'], VIOLET)
    f.arrow(384, 270, 465, 270)
    f.arrow(810, 270, 891, 270)
    f.card(44, 437, 340, 205, '词法召回路径', ['近邻文本 → 查询规划', 'AND 词 / 短语匹配', '全扫描、排序、hidden 过滤', '不要求 embedding 索引'], BLUE)
    f.card(469, 437, 341, 205, 'Journal 与反思调度', ['对话增量 / 待处理游标', '步数 / 压缩 / 手动触发', 'active + pending 预留', '请求合并、预算与关闭处理'], VIOLET)
    f.card(895, 437, 341, 205, '反思结果集成', ['独立工作树与已验证 tip', 'writer lock / 收据检查', '干净状态检查与合并', '区分冲突、失败与已集成'], TEAL)
    f.arrow(1065, 360, 639, 433, [(1065, 399), (639, 399)])
    f.arrow(810, 539, 891, 539)
    f.arrow(214, 437, 894, 327, [(214, 388), (853, 388), (853, 327)])
    f.arrow(1065, 642, 40, 304, [(1065, 680), (25, 680), (25, 304)])
    f.text(449, 706, '已验证的变更合入后，形成新的记忆版本', 18, MUTED)
    f.band(723, '版本可追踪，不等于事实必然正确', '写入与反思影响后续模型输入；仍需要纠错、来源与过期机制。本文未测长期任务收益。')
    f.save('memory/compile · recall/planner · search/engine · reflection；omo-senpi wiring')

    f = Figure('08-adapters', '跨宿主复用机制，按宿主验收契约', '相同产品名称下，工具入口、事件协议与运行状态边界并不相同。', 830)
    cols = [(44, 'OpenCode', BLUE), (452, 'Codex', VIOLET), (860, 'Senpi / Native', TEAL)]
    data = [
        ['入口：PluginModule.server', '会话：OpenCode SDK', '任务：task + BackgroundManager', '协作：可选 team_* 工具', '上下文：消息 / 工具 / 压缩 Hook'],
        ['入口：.codex-plugin 清单', '会话：Codex 宿主', '任务：宿主原生协作', '扩展：事件脚本 + Skill + MCP', 'ultrawork：短指针 → 完整 Skill'],
        ['入口：omo-ai → 固定 Senpi', '会话：Senpi 引擎与扩展 API', '任务：senpi-task / workflow', '恢复：图日志 + 检查点', '记忆：memory-core 运行接线'],
    ]
    for (x, title, color), lines in zip(cols, data):
        f.card(x, 192, 376, 251, title, lines, color, 18)
    f.card(44, 491, 1192, 137, '需要分别验证的五个问题', ['是否能安装？资产是否能发现？Hook 是否会触发？工具调用是否执行？中断恢复是否保持语义？', '本次完成源码与局部机制验证，未把三种宿主全部安装并执行真实模型任务。'], AMBER)
    f.band(679, '实现与验收分层', 'Prompt 约定 → OMO 确定性检查 → 宿主工具权限 → 操作系统资源边界。')
    f.save('plugin-interface.ts · .codex-plugin/plugin.json · native launcher · component-list.ts')


def build_html():
    source = (BASE / 'README.md').read_text()
    marker = '<!-- GENERATED SOURCE REFERENCES -->'
    source = source.split(marker)[0].rstrip() + '\n\n' + marker + '\n\n' + (BASE / 'research/references.md').read_text()
    (BASE / 'README.md').write_text(source)
    article = re.sub(r'^---\n.*?\n---\n', '', source, count=1, flags=re.S)
    md = MarkdownIt('commonmark', {'html': True}).enable('table')
    body = md.render(article)
    # Give headings stable anchors in addition to the explicit section anchors.
    headings = []
    def heading(match):
        level, content = match.group(1), match.group(2)
        label = re.sub('<[^>]*>', '', content)
        anchor = f'heading-{len(headings) + 1}'
        headings.append((level, anchor, label))
        return f'<h{level} id="{anchor}">{content}</h{level}>'
    body = re.sub(r'<h([23])>(.*?)</h\1>', heading, body)
    body = re.sub(r'(<table>.*?</table>)', r'<div class="table-scroll">\1</div>', body, flags=re.S)
    body = re.sub(r'<img src="(assets/[^"]+)" alt="([^"]*)"\s*/?>', r'<a class="figure-link" href="\1" target="_blank" rel="noopener"><img src="\1" alt="\2" loading="lazy"></a>', body)
    toc = '\n'.join(f'<a class="level-{level}" href="#{anchor}">{esc(html.unescape(label))}</a>' for level, anchor, label in headings if level == '2')
    document = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="固定提交的 oh-my-openagent 中文源码研究：多宿主架构、Agent 编排、DAG、Hashline、上下文与记忆，附可复现源码实验。">
<title>oh-my-openagent 源码深度解析</title>
<style>
:root{--ink:#162c43;--muted:#5a6c80;--accent:#087f83;--line:#dce5ed;--paper:#fff;--bg:#f4f7fa}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:30px}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.9 system-ui,-apple-system,"Noto Sans CJK SC","Microsoft YaHei",sans-serif}
a{color:#146b9b;text-decoration:none}a:hover{text-decoration:underline}a:focus-visible{outline:3px solid #13a6b1;outline-offset:3px}
.topbar{background:#142c45;color:white;padding:18px 5vw;display:flex;gap:22px;justify-content:space-between;align-items:center}.topbar a{color:#b9ece8}.brand{font-size:13px;letter-spacing:.14em;font-weight:700}.edition{font-size:13px;color:#d6e2ec}
.layout{display:grid;grid-template-columns:250px minmax(0,1060px);gap:34px;max-width:1410px;margin:42px auto;padding:0 24px}
nav{position:sticky;top:24px;align-self:start;max-height:calc(100vh - 48px);overflow:auto;font-size:13px;padding:10px 4px 20px}nav strong{font-size:14px;color:var(--accent)}nav a{display:block;padding:8px 8px;border-left:2px solid var(--line);color:var(--muted);line-height:1.5}nav a:hover{background:#e7f1f4;color:var(--ink)}
main{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:48px 54px;min-width:0;box-shadow:0 8px 35px #18334b06}
h1{font-size:38px;line-height:1.45;letter-spacing:-.03em;margin:0 0 26px}h2{font-size:27px;line-height:1.5;margin:65px 0 22px;padding-top:22px;border-top:1px solid var(--line)}h3{font-size:21px;line-height:1.6;margin:36px 0 16px}
p{margin:19px 0}blockquote{margin:25px 0;padding:12px 22px;border-left:4px solid var(--accent);background:#eff7f7;color:#38586c;font-size:14px}blockquote p{margin:8px 0}
strong{font-weight:700;color:#152c43}img{width:100%;height:auto;display:block;margin:28px 0;border:1px solid var(--line);border-radius:12px}.figure-link{display:block}.figure-link:hover img{border-color:var(--accent)}
code{font-family:"DejaVu Sans Mono",Consolas,monospace;font-size:.86em;overflow-wrap:anywhere;background:#eff3f7;border-radius:4px;padding:2px 5px}pre{padding:22px 24px;background:#142a40;color:#e6edf5;overflow:auto;border-radius:10px;line-height:1.75;font-size:14px}pre code{background:none;color:inherit;padding:0;overflow-wrap:normal;font-size:inherit}
.table-scroll{overflow-x:auto;margin:24px 0}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.75}th{text-align:left;background:#eef4f7;color:#28465e;font-weight:700}td,th{padding:12px 14px;border:1px solid var(--line);min-width:120px}tr:nth-child(even) td{background:#fafcfd}
ul,ol{padding-left:1.5em}li{margin:10px 0}hr{border:0;border-top:1px solid var(--line);margin:45px 0}.footer{font-size:13px;color:var(--muted);text-align:center;padding:0 20px 40px}.mobile-nav{display:none}
@media(max-width:1050px){.layout{grid-template-columns:minmax(0,1fr);max-width:980px}.sidebar{display:none}.mobile-nav{display:block;padding:14px 24px;background:white;border-bottom:1px solid var(--line)}.mobile-nav nav{position:static;max-height:340px}.layout{margin-top:24px}}
@media(max-width:640px){body{font-size:16px}.topbar{padding:14px 18px;display:block}.edition{margin-top:7px}.layout{padding:0 10px;gap:0}main{padding:27px 20px;border-radius:10px}h1{font-size:28px}h2{font-size:23px;margin-top:45px}h3{font-size:19px}pre{padding:16px;font-size:12px}blockquote{padding:9px 14px}table{font-size:13px}img{border-radius:6px;margin:20px 0}}
@media print{.topbar,.sidebar,.mobile-nav{display:none}.layout{display:block;margin:0;padding:0;max-width:none}main{border:0;padding:0;box-shadow:none}body{font-size:11pt;background:white}h1{font-size:25pt}h2{break-after:avoid}img,blockquote{break-inside:avoid}pre{white-space:pre-wrap;color:#111;background:#eee}.table-scroll{overflow:visible}a{color:#164e76}}
</style></head><body>
<header class="topbar"><div class="brand">DEEP AGENT / SOURCE STUDY</div><div class="edition">2026-09-16 · bee849b228d1 · <a href="README.md">Markdown</a> · <a href="research/verification.md">验证记录</a></div></header>
<details class="mobile-nav"><summary>展开文章目录</summary><nav>__TOC__</nav></details>
<div class="layout"><nav class="sidebar" aria-label="文章目录"><strong>OH-MY-OPENAGENT</strong>__TOC__</nav><main>__BODY__</main></div>
<footer class="footer">本页离线可读，无外部字体、脚本或 CDN。点击图示可单独放大查看 SVG。源码链接需要联网。</footer>
</body></html>'''.replace('__TOC__', toc).replace('__BODY__', body)
    (BASE / 'index.html').write_text(document)


if __name__ == '__main__':
    figures()
    build_html()
    print('Built 8 SVG figures and index.html; refreshed README source references.')
