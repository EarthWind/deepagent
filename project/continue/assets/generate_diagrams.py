"""Original SVG engineering diagrams; stdlib only, no external fonts or scripts."""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent
INK = "#16362f"
MUTED = "#58706a"
GREEN = "#147a60"
BLUE = "#3462a3"
AMBER = "#a26918"


class Diagram:
    def __init__(self, number, title, subtitle, height=720):
        self.number, self.height = number, height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="none" stroke="#739487" stroke-width="1.5"/></marker></defs>
<style>text{{font-family:system-ui,'Noto Sans CJK SC','Microsoft YaHei',sans-serif;fill:{INK}}}.small{{font-size:16px;fill:{MUTED}}}.body{{font-size:19px}}.label{{font-size:17px;font-weight:650}}.card-title{{font-size:23px;font-weight:750}}</style>
<rect width="1280" height="{height}" fill="#f5f8f3"/>
<rect x="0" y="0" width="1280" height="10" fill="{GREEN}"/>
<text x="44" y="53" font-size="14" font-weight="750" letter-spacing="2" fill="{GREEN}">CONTINUE / SOURCE NOTES / {number:02}</text>
<text x="44" y="101" font-size="32" font-weight="800">{escape(title)}</text>
<text x="44" y="135" class="small">{escape(subtitle)}</text>''']

    def text(self, x, y, text, cls="body", fill=None):
        color = f' style="fill:{fill}"' if fill else ""
        self.parts.append(f'<text x="{x}" y="{y}" class="{cls}"{color}>{escape(text)}</text>')

    def box(self, x, y, w, h, title, lines=(), accent=GREEN):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="white" stroke="#ccdcd0"/><rect x="{x}" y="{y+16}" width="5" height="30" rx="2" fill="{accent}"/>')
        self.text(x + 20, y + 40, title, "card-title", accent)
        for i, line in enumerate(lines):
            self.text(x + 20, y + 77 + i * 29, line)

    def line(self, points, label=None, lx=None, ly=None, dashed=False):
        coords = " ".join(f"{x},{y}" for x, y in points)
        dash = ' stroke-dasharray="7 5"' if dashed else ""
        self.parts.append(f'<polyline points="{coords}" fill="none" stroke="#739487" stroke-width="2.5"{dash} marker-end="url(#arrow)"/>')
        if label:
            self.text(lx, ly, label, "label")

    def note(self, text):
        y = self.height - 91
        self.parts.append(f'<rect x="44" y="{y}" width="1192" height="45" rx="8" fill="#e4eee4"/>')
        self.text(62, y + 29, text, "small")

    def save(self, filename, refs):
        self.text(44, self.height - 18, f"原创源码关系图 · 5522c6f44ca0 · {refs} · 非产品截图 / 非性能测量", "small")
        self.parts.append("</svg>")
        (OUT / filename).write_text("\n".join(self.parts))


d = Diagram(1, "三个客户端，两条 Agent 编排主线", "IDE 复用 GUI + Core；CLI 复用基础模块，但拥有独立的循环、权限和会话服务。", 800)
d.box(44, 182, 340, 170, "VS Code", ["React Webview / Redux", "VsCodeMessenger 消息桥", "Core + VsCodeIde 同进程"])
d.box(44, 382, 340, 170, "JetBrains", ["共享 GUI / Kotlin 宿主", "IPC → 独立 Core binary", "开发模式可使用 TCP"])
d.box(470, 182, 340, 370, "IDE 执行链", ["GUI 决定下一轮何时开始", "streamNormalInput", "工具状态 / 审批 / Diff", "", "Core 提供服务", "模型调用 / 上下文 / 索引", "MCP / 工具 / 历史"], BLUE)
d.box(896, 182, 340, 370, "CLI · cn", ["Commander + React / Ink", "TUI / Headless", "", "streamChatResponse", "独立 while 循环", "服务容器 / 权限 / 压缩", "CLI 文件与终端工具"], BLUE)
d.line([(384, 262), (470, 262)])
d.line([(384, 467), (470, 467)])
d.box(44, 590, 1192, 90, "共享基础设施", ["类型与配置 · openai-adapters · 编辑算法 · 部分 Core 工具函数 · 本地 JSON 历史"])
d.line([(640, 552), (640, 590)])
d.line([(1066, 552), (1066, 590)])
d.note("阅读重点：Core 的一次 llm/streamChat 调用，不等于完整 Agent 循环；CLI 也不是 Core 的简单命令行外壳。")
d.save("01-architecture.svg", "S02–S04 / S06 / S13")

d = Diagram(2, "IDE Agent：流式生成与工具状态协同", "Redux thunk 串联决策；Core 执行服务；编辑工具还要等待宿主 Diff 生命周期。", 840)
d.box(44, 180, 330, 145, "① 构造请求", ["模式 → 可见工具 → overrides", "历史 + Rules → compileChat"])
d.box(474, 180, 330, 145, "② 消费模型流", ["原生 tool_calls / 文本协议", "增量参数 → generating"], BLUE)
d.box(904, 180, 330, 145, "③ 预处理与策略", ["生成完成 → generated", "解析参数，再计算权限"], AMBER)
d.line([(374, 251), (474, 251)])
d.line([(804, 251), (904, 251)])
d.box(904, 393, 330, 174, "④ 执行或等待", ["自动执行 / 审批等待", "Core 工具 / GUI 编辑工具", "calling → done / errored"], AMBER)
d.box(474, 393, 330, 174, "⑤ 写回工具结果", ["关联 toolCallId", "确认这一批工具都已完成", "拒绝后续跑受配置控制"], BLUE)
d.box(44, 393, 330, 174, "⑥ 下一轮 / 停止", ["有结果 → 再次生成", "无工具 → 本轮停止", "取消信号可中断生成"])
d.line([(1069, 325), (1069, 393)])
d.line([(904, 480), (804, 480)])
d.line([(474, 480), (374, 480)])
d.line([(209, 393), (209, 325)], "下一轮", 229, 367)
d.box(44, 615, 1192, 99, "并发与等待的细节", ["全自动分支可 Promise.all；存在审批时先运行可自动批准的内建只读工具，其余等待。"])
d.note("状态结束只说明这一轮停止，不证明代码正确；验证仍需终端测试、Diff 观察和明确的验收条件。")
d.save("02-ide-loop.svg", "S06–S10 / S41")

d = Diagram(3, "CLI Agent：一次 while 迭代的真实结构", "每轮重新获取系统提示与工具；压缩发生在请求前、工具后和常规阈值检查处。", 810)
items = [(44, 185, "读取运行状态", ["历史服务 / 当前模式", "系统提示 / 本轮工具"]),
         (466, 185, "请求前预算检查", ["必要时先压缩", "校验消息 + system + tools"]),
         (888, 185, "生成并组装调用", ["适配器流 → 内容 / usage", "index 与 id 映射参数增量"]),
         (888, 410, "审批与工具执行", ["逐个检查，获准即启动", "并发完成后整理结果"]),
         (466, 410, "工具后预算检查", ["可能压缩，避免结果过大", "再进行常规阈值判断"]),
         (44, 410, "继续或返回", ["有工具调用 → 继续", "无调用且无续跑 → 返回"])]
for i, (x, y, title, lines) in enumerate(items):
    d.box(x, y, 348, 155, title, lines, BLUE if i % 2 else GREEN)
d.line([(392, 263), (466, 263)])
d.line([(814, 263), (888, 263)])
d.line([(1062, 340), (1062, 410)])
d.line([(888, 487), (814, 487)])
d.line([(466, 487), (392, 487)])
d.line([(218, 410), (218, 340)], "重新迭代", 232, 381)
d.box(44, 610, 1192, 92, "压缩后的自动续跑", ["若本轮发生压缩且原本准备停止，可追加 continue；随后清除标志，防止仅因该标志无限续跑。"], AMBER)
d.note("工具异常通常成为模型可见结果；Headless 若出现工具拒绝，可在该批处理后提前返回。")
d.save("03-cli-loop.svg", "S13–S15 / S27")

d = Diagram(4, "上下文是一条编译管道", "模型看到的消息列表，与 UI 展示和磁盘保存的完整历史，并不是同一个视图。", 820)
for y, title, lines in [(180, "任务和显式上下文", ["用户输入 / 文件 / 选区"]), (322, "历史与工具状态", ["toolCallStates / 工具结果"]), (464, "规则与技能", ["Rules 条件匹配 / 按需读 Skill"])]:
    d.box(44, y, 340, 113, title, lines)
d.box(471, 180, 340, 397, "constructMessages", ["1. 从最近摘要之后取历史", "2. ContextItems 放入用户消息", "3. 按工具状态重建 tool 消息", "4. 选择适用 Rules", "5. 摘要拼入系统消息", "", "保持调用与结果的对应关系"], BLUE)
for y in [237, 378, 520]:
    d.line([(384, y), (471, y)])
d.box(898, 180, 338, 397, "compileChatMessages", ["估算 system / tools / 历史", "保护最后一组用户或工具消息", "预留输出与计数缓冲", "必要时从旧历史开始裁剪", "", "保留项都放不下 → 报错", "随后交给模型适配器"], AMBER)
d.line([(811, 375), (898, 375)])
d.box(44, 620, 1192, 95, "IDE 预算：history ≤ C − safety − min(1000, maxTokens) − system − tools − protected tail", ["这是编译阶段的最小输出预留；不能把它解释成始终保留完整 maxTokens。"])
d.note("Skills 的正文通常在调用 read_skill 后进入工具结果；技能目录的名字和描述已占用工具定义预算。")
d.save("04-context.svg", "S19–S27")

d = Diagram(5, "旧 RAG：增量索引与混合召回", "@Codebase 已弃用，但索引和检索实现仍保留；当前默认工具链不能等同于这个流程。", 820)
d.text(44, 185, "离线 / 后台索引", "label", GREEN)
for x, title, lines in [(44, "文件变更", ["目录 / 分支 / ignore", "内容摘要与缓存键"]), (466, "增量操作", ["compute / delete", "addTag / removeTag"]), (888, "按依赖构建", ["Chunk / FTS / Snippets", "LanceDB 向量"] )]:
    d.box(x, 207, 348, 136, title, lines)
d.line([(392, 275), (466, 275)])
d.line([(814, 275), (888, 275)])
d.text(44, 400, "查询时召回", "label", BLUE)
d.box(44, 420, 348, 188, "候选来源", ["最近编辑 + 关键词 FTS", "可选向量召回", "Repo map 请求文件"], BLUE)
d.box(466, 420, 348, 188, "过滤与排序", ["目录过滤 → 去重", "有 reranker：打分取前 nFinal", "无 reranker：直接返回候选"], BLUE)
d.box(888, 420, 348, 188, "ContextItem", ["文件路径 / 行号 / 内容", "放入后续模型上下文", "不保证全仓完整覆盖"], BLUE)
d.line([(392, 514), (466, 514)])
d.line([(814, 514), (888, 514)])
d.line([(1062, 343), (1062, 376), (218, 376), (218, 420)], dashed=True)
d.note("当前 nFinal 默认 min(25, C / 512 / 2)；启用重排时 nRetrieve 默认 2 × nFinal，勿套用旧文档 25 → 5。")
d.save("05-retrieval.svg", "S29–S34")

d = Diagram(6, "编辑工具的终点，是宿主确认后的真实文件", "IDE 与 CLI 共用部分字符串编辑算法，但审批、写盘和完成时机不同。", 860)
d.text(44, 185, "IDE 路径", "label", GREEN)
d.box(44, 207, 348, 162, "读取与计算", ["重新读取当前文件", "重新校验 MultiEdit", "计算新内容，提交 apply"])
d.box(466, 207, 348, 162, "ApplyManager", ["SEARCH/REPLACE → 即时 Diff", "代码块 → 确定性 / Diff / LLM", "保留原始内容供审阅"])
d.box(888, 207, 348, 162, "Diff 生命周期", ["streaming → done → closed", "接受 / 拒绝 / 自动接受", "closed 后写结果，再续跑"])
d.line([(392, 288), (466, 288)])
d.line([(814, 288), (888, 288)])
d.text(44, 428, "CLI 路径", "label", BLUE)
d.box(44, 450, 348, 162, "preprocess", ["路径 realpath + 曾读取检查", "在原内容上顺序计算编辑", "生成 Diff 预览"], BLUE)
d.box(466, 450, 348, 162, "权限检查", ["允许 / 询问 / 排除", "预计算内容等待审批", "用户可在等待时改动文件"], AMBER)
d.box(888, 450, 348, 162, "run / writeFileSync", ["写入预计算的新内容", "结果写入调用状态", "模型进入下一轮"], BLUE)
d.line([(392, 531), (466, 531)])
d.line([(814, 531), (888, 531)])
d.box(44, 658, 1192, 89, "二次开发建议：写入前核对版本或内容摘要，并按文件串行化写操作", ["字符串级 all-or-error 不等于磁盘原子写入、跨文件事务或对并发修改的保护。"], AMBER)
d.note("编辑成功与测试通过是两种证据；应让测试输出和最终 Diff 一起进入任务验收。")
d.save("06-editing.svg", "S38–S43 / S56–S57")

d = Diagram(7, "Autocomplete 是独立的低延迟系统", "它处理光标前缀与后缀，不经过聊天 Agent 的多步工具循环。", 770)
for x, title, lines in [(44, "触发与过滤", ["光标 / 文件 / AbortSignal", "安全文件检查 / debounce", "HelperVars / prefilter"]), (466, "上下文与预算", ["导入定义 / 最近编辑和访问", "最近打开文件 / 剪贴板", "prefix + suffix + snippets"]), (888, "生成与后处理", ["缓存命中或流式生成", "按模型选择补全方式", "过滤 / 后处理 / 返回结果"])]:
    d.box(x, 190, 348, 207, title, lines)
d.line([(392, 295), (466, 295)])
d.line([(814, 295), (888, 295)])
d.box(44, 446, 560, 171, "当前实际启用边界", ["主路径调用 getAllSnippetsWithoutRace", "ideSnippets 和 diffSnippets 当前关闭", "最近打开文件仍有逐文件 80ms 截止"], BLUE)
d.box(652, 446, 584, 171, "不要混淆 Next Edit", ["NextEditProvider 预测下一处编辑", "结合编辑轨迹、预取与光标跳转", "与传统插入式 Tab 补全有独立实现"], AMBER)
d.note("工程取舍：上下文收益必须抵得上读取、检索、组装、首 token 与渲染延迟；本文未进行延迟基准测试。")
d.save("07-autocomplete.svg", "S02 / S44–S45")

d = Diagram(8, "模式和审批的实际边界", "工具描述表达意图；策略决定工具可见性和执行许可；系统隔离必须由宿主另行提供。", 850)
d.box(44, 186, 570, 362, "IDE", ["Chat：不暴露工具", "Plan：过滤内建非 readonly 工具", "第三方 MCP 工具不受同样的过滤", "", "动态权限原则上只能收紧", "编辑工具将审阅交给 Diff 生命周期", "工作区外文件访问可提升为需审批"])
d.box(660, 186, 576, 362, "CLI", ["Plan：排除 Edit / MultiEdit / Write", "Bash 与 MCP 通配仍可 allow", "Headless：仅暴露 allow 的工具", "", "策略首个匹配项生效", "动态 disabled 始终优先", "动态 ask 不覆盖静态 allow"], BLUE)
d.box(44, 590, 1192, 146, "实验性 Subagent：需要单独审查的共享状态", ["默认 beta 关闭；启用后会临时覆盖全局权限、系统提示方法和历史服务 ready 行为。", "它不是独立进程或隔离容器；并发重入、权限继承和异常恢复需要专门验证。"], AMBER)
d.note("结论：Plan / readonly / 工具审批 ≠ 完整只读文件系统；Shell 与 MCP 的副作用要由真实执行边界约束。")
d.save("08-permissions.svg", "S09–S10 / S46–S52")

d = Diagram(9, "会话恢复与任务恢复，是不同层次", "Continue 保存会话 JSON 与摘要；恢复消息不能自动重建进程、网络请求和文件副作用。", 760)
d.box(44, 188, 348, 304, "持久化的内容", ["sessionId / title / workspace", "history / toolCallStates", "conversationSummary", "模型信息 / usage（若有）", "", "单个会话 JSON + sessions.json"])
d.box(466, 188, 348, 304, "恢复后再次生成", ["读取历史", "依据摘要构造模型视图", "重新装配配置和工具", "发起新一轮模型请求", "", "上下文连续性"], BLUE)
d.box(888, 188, 348, 304, "外部环境要重新确认", ["文件是否又被修改", "终端进程是否仍在运行", "命令是否已经执行", "MCP 外部操作是否成功", "", "副作用与幂等性"], AMBER)
d.line([(392, 330), (466, 330)])
d.line([(814, 330), (888, 330)], "检查", 831, 313)
d.box(44, 542, 1192, 111, "建议的生产增强：执行日志 + 原子会话写入 + 工具幂等键 + 文件版本检查 + 验收记录", ["这些是本文的工程建议，不应被误读为 Continue 当前已经实现的 durable workflow 能力。"])
d.note("观测重点：任务成功率、工具错误率、审批等待、上下文开销、编辑接受率和最终测试结果。")
d.save("09-persistence.svg", "S26–S27 / S53–S55")

print("Generated 9 original SVG diagrams")
