#!/usr/bin/env python3
"""Rebuild the article's original vector diagrams. Standard library only."""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"
OUT.mkdir(parents=True, exist_ok=True)
INK, MUTED, TEAL, BLUE, ORANGE = "#152c40", "#566a7c", "#087e82", "#3764ad", "#b75c27"


class Figure:
    def __init__(self, number, title, subtitle, height=800):
        self.h = height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto-start-reverse"><path d="M1 1 L8 5 L1 9" fill="none" stroke="#73879a" stroke-width="1.5"/></marker></defs>
<style>text{{font-family:'Noto Sans CJK SC','Microsoft YaHei',sans-serif}} .mono{{font-family:'DejaVu Sans Mono',monospace}}</style>
<rect width="1280" height="{height}" rx="20" fill="#f5f8fb"/>
<rect x="0" y="0" width="1280" height="8" fill="{TEAL}"/>
''']
        self.text(48, 49, f"ECC  /  SOURCE STUDY  /  {number:02d}", 14, TEAL, 700)
        self.text(48, 99, title, 32, INK, 700)
        self.text(48, 133, subtitle, 17, MUTED)

    def text(self, x, y, text, size=18, color=INK, weight=400, anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(text)}</text>')

    def rect(self, x, y, w, h, fill="#fff", stroke="#d9e3ec", radius=14):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

    def card(self, x, y, w, h, title, lines, accent=TEAL, dark=False):
        self.rect(x, y, w, h, INK if dark else "#fff", INK if dark else "#d9e3ec")
        self.parts.append(f'<rect x="{x}" y="{y+18}" width="4" height="28" rx="2" fill="{accent}"/>')
        self.text(x+22, y+43, title, 22, "#fff" if dark else accent, 700)
        for i, line in enumerate(lines):
            self.text(x+22, y+79+i*28, line, 17, "#dce7f0" if dark else MUTED)

    def arrow(self, points, dashed=False):
        coords = " ".join(f"{x},{y}" for x, y in points)
        dash = ' stroke-dasharray="7 5"' if dashed else ''
        self.parts.append(f'<polyline points="{coords}" fill="none" stroke="#73879a" stroke-width="2"{dash} marker-end="url(#arrow)"/>')

    def label(self, x, y, text, color=TEAL):
        self.text(x, y, text, 15, color, 600)

    def finish(self, name, note):
        self.parts.append(f'<path d="M48 {self.h-58} H1232" stroke="#d9e3ec"/>')
        self.text(48, self.h-27, note, 14, MUTED)
        self.text(1232, self.h-27, "8321021 · 2026-09-15", 14, MUTED, anchor="end")
        self.parts.append('</svg>')
        (OUT / name).write_text("\n".join(self.parts), encoding="utf-8")


def architecture():
    f = Figure(1, "ECC：围绕宿主 Agent 组织工程能力", "能力资产影响模型行为；事件脚本处理确定性动作；持久化为后续任务提供线索。", 864)
    for x, title, lines in [
        (48, "Rules", ["长期规范与技术栈约定", "rules/common + language"]),
        (350, "Skills", ["任务方法与辅助资源", "SKILL.md + scripts"]),
        (652, "Commands", ["显式调用与兼容入口", "由宿主解析和发现"]),
        (954, "Agents", ["专业角色与工具范围", "由宿主实例化或选择"]),
    ]:
        f.card(x, 176, 278, 150, title, lines)
    f.arrow([(640, 330), (640, 370)])
    f.card(48, 388, 744, 180, "宿主 Agent：Claude Code / Codex / 其他客户端", ["用户输入 → 模型推理 → 工具执行 → 结果反馈", "主循环、权限、模型连接和交互由具体宿主管理", "ECC 的主流插件路径在这些能力周围增加工作方法与运行机制"], dark=True)
    f.card(824, 388, 408, 180, "适配层", ["事件 JSON ↔ 宿主返回协议", "目录布局、插件缓存与安装状态", "每个宿主具备的能力并不相同"], BLUE)
    f.arrow([(395, 572), (395, 604)])
    f.arrow([(1028, 572), (1028, 604)])
    f.card(48, 622, 376, 150, "运行 Hook", ["检查、拦截、编辑积累", "同步与异步事件处理"], TEAL)
    f.card(452, 622, 376, 150, "知识与经验", ["会话摘要 / Instinct / Vault", "按范围和预算重新读取"], BLUE)
    f.card(856, 622, 376, 150, "操作与证据", ["worktree、会话、指标", "日志、收据与评估边界"], ORANGE)
    f.finish('01-architecture.svg', '原创源码示意 · 核心关系图，不表示所有模块默认启用')


def installation():
    f = Figure(2, "安装也是工程系统：计划、写入与文件归属", "图中为 ECC 管理安装路径；原生插件由宿主管理其安装生命周期。", 826)
    f.card(48, 186, 350, 164, "01  选择能力", ["target + install profile", "components / modules", "安装 minimal 不含 hooks-runtime"])
    f.card(465, 186, 350, 164, "02  生成计划", ["解析清单与依赖", "由 target adapter 决定目录", "copy-file / merge-json / settings"], BLUE)
    f.card(882, 186, 350, 164, "03  检查边界", ["Hook 安装条件", "可信根目录和已有 install-state", "写入前检查用户文件归属"], ORANGE)
    f.arrow([(400, 268), (453, 268)])
    f.arrow([(817, 268), (870, 268)])
    f.arrow([(1058, 354), (1058, 418)])
    f.card(690, 434, 542, 146, "执行写入 → 记录 install-state", ["记录来源、目标路径、管理归属与内容摘要", "doctor / repair / uninstall 使用同一份归属线索"], dark=True)
    f.card(48, 434, 578, 146, "遇到未归属 ECC 的已有文件", ["跳过并报告；不覆盖，也不在 state 中认领", "规划后新出现的用户文件：写入前再次拒绝"], ORANGE)
    f.arrow([(882, 349), (840, 393), (337, 393), (337, 420)], True)
    f.card(48, 620, 1184, 110, "两个 Profile 是两个维度", ["安装 Profile 选择模块；Hook Profile 选择运行项。安装成功、宿主发现、Hook 执行需要分别验证。"], BLUE)
    f.finish('02-installation.svg', '依据 install-manifests / install/plan / install/apply / ownership-guard')


def lifecycle():
    f = Figure(3, "一次响应的事件时间线", "以下按 Claude Hook 注册整理；模型工作流由宿主与模型推进，事件项不构成固定业务 DAG。", 908)
    lanes = [(48, 254, "宿主生命周期", INK), (326, 535, "ECC 同步处理", TEAL), (886, 346, "异步 / 持久化", BLUE)]
    for x, w, title, color in lanes:
        f.rect(x, 171, w, 48, color, color, 10)
        f.text(x+18, 203, title, 20, '#fff', 700)
    rows = [
        (242, 'SessionStart', ['匹配会话与项目', '预算内注入摘要 / Instinct'], ['恢复的是线索', '需要核对工作区真实状态']),
        (355, 'PreToolUse', ['配置保护 / Bash 检查 / GateGuard', '允许、提示或阻止本次工具调用'], ['观察 tool_start', '受入口与开关条件影响']),
        (468, 'PostToolUse', ['编辑文件积累、诊断与活动跟踪', '同步 dispatcher'], ['异步 dispatcher', '观察、质量反馈、记录']),
        (581, 'Stop', ['批量 formatter / typecheck', '一轮响应结束即可触发'], ['session-end.js 保存摘要', '成本累计快照等']),
        (694, 'SessionEnd', ['会话关闭的独立事件', '与 Stop 分开理解'], ['session-end-marker.js', '结束标记']),
    ]
    for y, event, sync, async_ in rows:
        f.rect(48, y, 254, 90)
        f.text(67, y+38, event, 23, INK, 700)
        f.rect(326, y, 535, 90)
        f.rect(886, y, 346, 90, '#eef5fc')
        for i, t in enumerate(sync): f.text(344, y+34+i*29, t, 18, MUTED)
        for i, t in enumerate(async_): f.text(904, y+34+i*29, t, 17, MUTED)
    f.text(48, 829, 'PreCompact：在宿主压缩前尝试持久化摘要；该事件可插入实际会话过程。', 17, ORANGE, 600)
    f.finish('03-lifecycle.svg', '依据 hooks/hooks.json · “异步”指注册方式，不承诺无损送达')


def memory_layers():
    f = Figure(4, "三种知识存储，三种不同用途", "控制平面数据库另管会话与操作状态；不能把所有持久化统一叫作向量记忆。", 846)
    xs = [48, 454, 860]
    titles = ['会话摘要', 'Instinct 经验', 'Memory Vault']
    colors = [TEAL, BLUE, ORANGE]
    for x, title, color in zip(xs, titles, colors):
        f.rect(x, 178, 372, 57, color, color)
        f.text(x+22, 215, title, 23, '#fff', 700)
    contents = [
        ('从哪里来', [['宿主 JSONL transcript', '机械提取 / 条件性 LLM 摘要'], ['Pre / Post 工具观察', '显式启用 Observer 后提炼'], ['CLI / MCP 显式写入', '结构化 Markdown 文档']]),
        ('主要保存', [['任务线索、工具与文件', '项目、分支、worktree'], ['trigger / action / evidence', 'confidence + scope'], ['decision / fact / handoff 等', 'source / target / links / trust']]),
        ('如何使用', [['SessionStart 匹配历史记录', '默认上下文总预算 8,000 字符'], ['筛选与排序后注入少量经验', 'evolve 产生待使用的资产'], ['显式 search → read', '词法排序 + 目标宿主过滤']]),
    ]
    for idx, (label, columns) in enumerate(contents):
        y = 253+idx*161
        for x, lines, color in zip(xs, columns, colors):
            f.card(x, y, 372, 141, label, lines, color)
    f.label(48, 775, '上下文线索 ≠ 完整事件事实；confidence ≠ 正确概率；unreviewed ≠ 已验证。', ORANGE)
    f.finish('04-memory-layers.svg', '依据 session-start/end、continuous-learning-v2、memory-vault')


def learning():
    f = Figure(5, "持续学习：外部经验改变后续工作", "观察、后台分析、注入和演化是不同阶段；其中 Observer 默认关闭。", 876)
    f.card(48, 183, 350, 172, "01  事件观察", ["tool_start / tool_complete", "项目识别、截断、常见值脱敏", "observations.jsonl"])
    f.card(465, 183, 350, 172, "02  Observer 分析", ["需显式启用，默认 enabled=false", "默认 haiku + Read / Write", "轮次、超时与自身观察跳过"], ORANGE)
    f.card(882, 183, 350, 172, "03  原子 Instinct", ["触发条件、行动、证据", "项目 / 全局作用域", "confidence 是排序信号"], BLUE)
    f.arrow([(400, 269), (453, 269)])
    f.arrow([(817, 269), (870, 269)])
    f.arrow([(1057, 360), (1057, 400), (332, 400), (332, 441)])
    f.arrow([(1057, 400), (952, 400), (952, 441)])
    f.card(48, 460, 565, 191, "A  下次 SessionStart 注入", ["先筛 confidence ≥ 0.7，再去重和排序", "项目范围 +0.25，技术栈匹配 +0.2", "默认最多 6 条，受总字符预算约束", "收益需用后续真实任务衡量"], TEAL)
    f.card(651, 460, 581, 191, "B  evolve 生成能力候选", ["英文关键词重叠系数 ≥ 0.5", "至少共享 2 个词；簇核心更新为交集", "默认预览；--generate 写入 evolved 目录", "文件生成后仍需审核与配置发现"], BLUE)
    f.rect(48, 691, 1184, 90, '#fff4e9', '#eed6be')
    f.text(70, 727, '源码实测：英文相关触发句得到 1 个簇；对应纯中文触发句得到 0 个簇。', 20, ORANGE, 700)
    f.text(70, 758, '当前 evolve 使用 ASCII 分词；这项局限属于聚类实现，不是模型中文理解能力。', 17, MUTED)
    f.finish('05-learning.svg', '外部经验复用链路 · 不涉及基础模型权重训练')


def vault():
    f = Figure(6, "Memory Vault：受约束的写入与可解释检索", "project / team / user 范围由目录组织；MCP 服务端再限制允许范围与来源宿主。", 891)
    f.card(48, 180, 347, 168, "memory_save", ["AJV 参数校验", "sourceHarness 由服务端确定", "trust 始终为 unreviewed"])
    f.card(465, 180, 347, 168, "规范化与路径检查", ["字段上限、ID 与枚举", "常见密钥模式检测", "可信根目录 / 文件身份校验"], ORANGE)
    f.card(882, 180, 350, 168, "create-only 发布", ["临时文件 → write → fsync", "hard link → 最终目标", "已有同路径目标时拒绝覆盖"], BLUE)
    f.arrow([(400, 264), (450, 264)])
    f.arrow([(817, 264), (868, 264)])
    f.card(48, 404, 1184, 112, "Markdown Vault  /  ecc.memory.v1", ["kind · scope · source_harness · target_harnesses · tags · links · status · created_at · body"], dark=True)
    f.arrow([(1057, 352), (1057, 390)])
    f.arrow([(320, 520), (320, 558)])
    f.arrow([(945, 520), (945, 558)])
    f.card(48, 577, 565, 176, "memory_search → memory_read", ["有界文件扫描 + active / target 过滤", "标题、标签、元数据、正文加权词法排序", "先摘要检索，再按 ID 读全文和 backlinks"], TEAL)
    f.card(651, 577, 581, 176, "memory_doctor", ["报告格式损坏、重复 ID、断链和符号链接", "查询不完整时不能假装记录不存在", "诊断不自动把知识提升为 trusted"], ORANGE)
    f.label(48, 807, '当前实现没有 embedding / 向量索引；team scope 本身不提供团队账号、云同步或多租户隔离。', ORANGE)
    f.finish('06-vault.svg', '依据 memory-mcp.mjs / memory-vault.js / memory-vault-format.js')


def evaluation():
    f = Figure(7, "记录一致性、执行安全与业务效果是不同问题", "这张图分开展示 Node 证据系统与 Rust Alpha 的 recorded-measurements 门控。", 839)
    f.card(48, 184, 350, 166, "执行轨迹与产物引用", ["事件 envelope", "受限内容与确定性序列化", "来源与任务关联"])
    f.card(465, 184, 350, 166, "Capsule", ["追加 journal.ndjson", "parent_hash 链接前序记录", "可重建 projection"], BLUE)
    f.card(882, 184, 350, 166, "Receipt", ["绑定日志与产物摘要", "离线检查一致性", "无外部锚点时仍可整体替换"], TEAL)
    f.arrow([(400, 269), (451, 269)])
    f.arrow([(817, 269), (868, 269)])
    f.card(48, 407, 565, 218, "Node Gate：执行不可用", ["gate run → requireSupportedIsolation()", "缺少经验证的 OS 隔离后端", "退出 1：gate.isolation_required", "静态 tripwire 与摘要检查仍然存在", "不能把它描述成已运行候选性能评估"], ORANGE)
    f.card(651, 407, 581, 218, "Rust ecc2：本地记录分数门控", ["候选配置 SHA-256 + 相同 seed 的基线", "样本数、均值差与 win rate 条件", "SQLite active pointer + 审计记录", "分数 / health / evidence 由操作员提供", "active pointer 不自动部署到宿主"], BLUE)
    f.rect(48, 665, 1184, 81, '#eaf5f3', '#c7e2de')
    f.text(70, 700, '真正的改进验收还需要真实任务对照：完成率、回归、返工、成本、时延与知识质量。', 20, TEAL, 700)
    f.text(70, 728, '本文通过源码与局部测试确认机制，不将其转换成未经测量的模型性能结论。', 17, MUTED)
    f.finish('07-evaluation.svg', '依据 eval-harness 与 ecc2/README.md · 两条实现路径分开描述')


for draw in [architecture, installation, lifecycle, memory_layers, learning, vault, evaluation]:
    draw()
print(f"Generated 7 SVG diagrams in {OUT}")
