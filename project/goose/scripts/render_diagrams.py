#!/usr/bin/env python3
"""Generate original, source-based SVG diagrams using only the standard library."""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"
COLORS = {
    "blue": ("#eaf2ff", "#2563eb"),
    "teal": ("#e5f7f3", "#087f75"),
    "amber": ("#fff4da", "#a56808"),
    "purple": ("#f2edff", "#7552be"),
    "gray": ("#edf1f6", "#56657a"),
}


class Diagram:
    def __init__(self, title, subtitle, height=850):
        self.height = height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="{height}" viewBox="0 0 1440 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,1 L8,5 L0,9" fill="none" stroke="#64748b" stroke-width="1.5"/></marker></defs>
<style>text{{font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif;fill:#192b45}} .small{{font-size:18px;fill:#526278}} .body{{font-size:20px}} .label{{font-size:19px;font-weight:600}} .heading{{font-size:25px;font-weight:700}}</style>
<rect width="1440" height="{height}" fill="#f8fafc"/>
<rect width="1440" height="10" fill="#087f75"/>''']
        self.text(54, 64, "GOOSE / ENGINEERING NOTES", 17, "#087f75", True)
        self.text(54, 111, title, 34, bold=True)
        self.text(54, 148, subtitle, 19, "#526278")

    def text(self, x, y, text, size=20, color="#192b45", bold=False, anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" style="fill:{color}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(text)}</text>')

    def box(self, x, y, w, h, title, lines=(), tone="blue"):
        fill, stroke = COLORS[tone]
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
        self.text(x + 22, y + 36, title, 23, stroke, True)
        for i, line in enumerate(lines):
            self.text(x + 22, y + 73 + i * 29, line, 19)

    def arrow(self, points, label=None, lx=None, ly=None, dashed=False):
        d = "M" + " L".join(f"{x},{y}" for x, y in points)
        dash = ' stroke-dasharray="7 6"' if dashed else ""
        self.parts.append(f'<path d="{d}" fill="none" stroke="#64748b" stroke-width="2"{dash} marker-end="url(#arrow)"/>')
        if label:
            self.text(lx, ly, label, 18, "#526278")

    def note(self, y, title, body):
        self.box(54, y, 1332, 103, title, [body], "amber")

    def save(self, name):
        self.parts.append(f'<path d="M54,{self.height-48} H1386" stroke="#d9e2ec"/>')
        self.text(54, self.height - 22, "原创工程示意图 · 源码基线 1e83e89 · 2026-09-18 · 非性能测量", 15, "#64748b")
        self.parts.append("</svg>")
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text("\n".join(self.parts) + "\n", encoding="utf-8")


def architecture():
    d = Diagram("Goose 的系统边界", "客户端连接 Agent，Agent 连接模型与能力；会话存储保留运行状态。", 940)
    d.box(54, 192, 330, 163, "客户端 / 入口", ["CLI：session / run", "Desktop：Electron + React", "IDE / SDK / 自动化"], "blue")
    d.box(456, 192, 528, 163, "接入协议与产品运行时", ["Desktop → WebSocket ACP → goose serve", "CLI 可直接进入 Agent；ACP 可接 IDE", "会话、消息流、取消、审批与交互"], "teal")
    d.box(1056, 192, 330, 163, "Provider", ["常规模型 API / 本地推理", "ACP / CLI 外部 Agent", "消息、用量与能力归一化"], "purple")
    d.arrow([(384, 267), (456, 267)])
    d.arrow([(984, 267), (1056, 267)])
    d.box(456, 416, 528, 182, "Agent 内核", ["传统 loop：CLI 无开关时默认", "状态机：Desktop 默认选择", "Prompt / Context / Inspectors / Hooks", "Tool dispatch / Steer / Cancellation"], "teal")
    d.arrow([(720, 355), (720, 416)])
    d.box(54, 416, 330, 182, "任务组织", ["Recipe：参数与配置", "Skills：按需加载方法", "Summon：独立子会话", "Scheduler：按时启动"], "blue")
    d.arrow([(384, 500), (456, 500)])
    d.box(1056, 416, 330, 182, "ExtensionManager", ["stdio / streamable_http", "builtin MCP / platform", "工具 / 资源 / prompts", "Code Mode → 工具回调"], "purple")
    d.arrow([(984, 500), (1056, 500)])
    d.box(456, 650, 528, 130, "状态与观测", ["SQLite：sessions / messages / usage_ledger", "历史可见性、扩展状态、Trace / Usage"], "gray")
    d.arrow([(720, 598), (720, 650)])
    d.text(54, 838, "边界提醒：本地 Agent 仍可能调用远端模型；MCP 连接与会话隔离不等于 OS 沙箱。", 22, "#755b25")
    d.save("architecture.svg")


def turn():
    d = Diagram("传统循环的一次工具往返", "普通模型 Provider 路径的简化时序；省略特殊命令、重试和子 Agent。", 930)
    xs = [185, 540, 930, 1260]
    for x, title in zip(xs, ["客户端", "Agent / Session", "Provider", "Tool / MCP"]):
        d.box(x - 117, 190, 234, 67, title, [], "teal" if x == 540 else "blue")
        d.parts.append(f'<path d="M{x},267 V732" stroke="#bdc9d7" stroke-dasharray="6 7"/>')
    d.arrow([(185, 294), (540, 294)], "① 用户消息 / prompt", 215, 283)
    d.text(566, 335, "保存用户输入，准备 prompt / tools", 18, "#087f75")
    d.arrow([(540, 373), (930, 373)], "② 模型可见历史 + 工具 schema", 570, 361)
    d.arrow([(930, 419), (540, 419)], "③ 流式文本 / 工具请求", 590, 407)
    d.arrow([(540, 467), (185, 467)], "④ 必要时请求确认", 223, 456)
    d.arrow([(185, 510), (540, 510)], "批准 / 拒绝", 275, 499, True)
    d.arrow([(540, 556), (1260, 556)], "⑤ 检查、pre-tool hook、dispatch；工具可能并发", 605, 544)
    d.arrow([(1260, 600), (540, 600)], "⑥ 结果 / 错误 / 进度通知", 733, 589)
    d.text(566, 640, "⑦ 组装调用与结果，常规历史随后写入 SQLite", 18, "#087f75")
    d.arrow([(540, 684), (930, 684)], "⑧ 下一轮模型调用，直至终止条件", 571, 672)
    d.note(766, "持久化边界", "传统常规工具分支不是统一的 write-ahead 日志；工具副作用与后续记录之间仍有故障窗口。")
    d.save("turn-lifecycle.svg")


def machine():
    d = Diagram("可重入状态机怎样决定下一步", "每次只采用第一个适用步骤；应用 Effect 后重新加载会话，再从列表开头检查。", 920)
    d.box(54, 197, 326, 138, "① Load session", ["SQLite → Conversation", "从历史与元数据推导状态"], "blue")
    d.box(438, 197, 552, 138, "② 按优先级检查 Operation", ["NotApplicable → 看下一个", "Applied → 停止本轮遍历"], "teal")
    d.box(1048, 197, 338, 138, "③ Apply effects", ["追加 / 替换 / 修改元数据", "持久化后决定是否 yield"], "purple")
    d.arrow([(380, 261), (438, 261)])
    d.arrow([(990, 261), (1048, 261)])
    d.arrow([(1217, 335), (1217, 380), (217, 380), (217, 335)], "④ 未 yield：重载并从头开始", 510, 373)
    d.box(54, 436, 402, 253, "高优先级控制", ["Entry hook / Slash command", "Steer / MaxTurns / BangShell", "Compaction（按 Provider 能力）", "ToolPairCompaction / Approval"], "blue")
    d.box(518, 436, 402, 253, "业务与工具操作", ["Doctor / Project / Skill / Recipe", "ToolExecution / UnknownTool", "Retry / StopHook / ExitOnError", "操作可贡献 tools / prompt parts"], "teal")
    d.box(982, 436, 404, 253, "最后的推理步骤", ["收集工具与 prompt parts", "检查重复工具名称", "Provider stream → 消息 Effect", "后续遍历处理待执行工具请求"], "purple")
    d.arrow([(456, 560), (518, 560)])
    d.arrow([(920, 560), (982, 560)])
    d.note(737, "入口默认值不同", "CLI 依赖环境开关；Desktop 默认通过 ACP 选择状态机；可恢复控制流不保证外部动作只执行一次。")
    d.save("state-machine.svg")


def code_mode():
    d = Diagram("普通工具调用与 Code Mode", "两条路径共享 ExtensionManager；内部调用经过哪些治理环节，需要分别追踪。", 900)
    d.text(54, 211, "普通路径", 23, "#087f75", True)
    d.box(54, 235, 290, 135, "LLM tool call", ["工具名 + JSON 参数", "模型决定单个调用"], "blue")
    d.box(411, 235, 290, 135, "Agent 检查", ["Inspectors / 审批", "Pre-tool hooks"], "amber")
    d.box(768, 235, 290, 135, "ExtensionManager", ["解析 owner / 名称", "available_tools 检查"], "teal")
    d.box(1125, 235, 261, 135, "工具实现", ["MCP client / server", "platform client"], "purple")
    for a, b in [(344, 411), (701, 768), (1058, 1125)]:
        d.arrow([(a, 300), (b, 300)])
    d.text(54, 421, "Code Mode 路径", 23, "#087f75", True)
    d.box(54, 445, 290, 176, "按需发现接口", ["catalog 默认：", "list_functions", "get_function_details", "execute_typescript"], "blue")
    d.box(411, 445, 290, 176, "外层执行请求", ["经过 Agent 检查", "pctx / Deno 执行", "中间结果留在脚本", "返回所需汇总"], "amber")
    d.box(768, 445, 290, 176, "函数 callback", ["回到 Tokio runtime", "直接进入工具 manager", "传递 session / cwd", "传递取消 token"], "teal")
    d.box(1125, 445, 261, 176, "工具实现", ["复用已有工具", "并非全新能力", "实际权限由执行", "进程与环境决定"], "purple")
    for a, b in [(344, 411), (701, 768), (1058, 1125)]:
        d.arrow([(a, 526), (b, 526)])
    d.note(713, "审核粒度发生变化", "外层代码获准，不代表每个 callback 都重新执行普通工具的 Inspector；这不是逐项审批等价性证明。")
    d.save("mcp-codemode.svg")


def context():
    d = Diagram("历史、上下文和记忆是不同的数据视图", "压缩改变模型输入的投影，保留用户可见历史；长期知识由独立机制提供。", 920)
    d.box(54, 194, 406, 260, "SQLite：完整会话集合", ["用户消息与 Assistant 消息", "工具请求 / 工具结果", "压缩摘要 / 控制消息", "每条消息带可见性元数据", "原历史可保留在存储中"], "gray")
    d.box(532, 194, 386, 260, "用户看到的历史", ["原消息保持原有可见性", "工具执行与交互展示", "不重复展示用户文本副本", "摘要不必成为聊天正文"], "blue")
    d.box(990, 194, 396, 260, "模型看到的上下文", ["System prompt + 工具 schema", "Agent-visible 消息投影", "摘要 + 继续提示", "必要的当前请求文本", "后续新消息"], "teal")
    d.arrow([(460, 310), (532, 310)])
    d.arrow([(256, 454), (256, 490), (1188, 490), (1188, 454)], "另一种可见性投影", 597, 482)
    d.box(54, 538, 406, 162, "降低当前窗口压力", ["自动压缩：默认阈值 0.8", "工具对摘要：本快照默认关闭", "大文本外置：默认 200,000 字符"], "amber")
    d.box(532, 538, 386, 162, "可复用上下文", ["Hints：工作区规则", "Skills：索引 → 按需正文", "Memory：显式持久知识"], "purple")
    d.box(990, 538, 396, 162, "任务工作状态", ["Todo：session extension data", "Chat Recall：检索旧会话", "MOIM：当前 turn 的动态信息"], "blue")
    d.text(54, 790, "成本计量：摘要调用的 billable usage 与压缩后 retained context token 必须分开计算。", 22, "#526278")
    d.save("context-memory.svg")


def security():
    d = Diagram("权限控制不能替代执行隔离", "授权、检查、调度与 OS 权限处于不同层级；间接调用也需要明确边界。", 940)
    d.box(54, 198, 620, 166, "普通工具：应用层决策", ["Mode → 用户规则 / 只读提示 / 模型判断", "Security / Egress / Adversary / Repetition", "检查器错误会记录并继续；注册不代表启用"], "amber")
    d.box(756, 198, 630, 166, "最终执行：系统层权限", ["执行进程 / OS 用户 / 文件系统 / 网络 / 凭据", "MCP 负责通信；沙箱策略由运行环境实现", "容器选项需逐类确认覆盖到哪些扩展"], "teal")
    d.arrow([(674, 278), (756, 278)])
    d.box(54, 422, 404, 232, "Auto 模式", ["PermissionInspector 直接 Allow", "不能解释成只放行低风险动作", "其他启用的检查仍有其分支", "运行环境决定副作用范围"], "blue")
    d.box(518, 422, 404, 232, "Code Mode", ["外层 execute_typescript 被检查", "内部 callback 直接进 manager", "并非每个函数都重新审批", "能力限制应靠最终执行边界"], "purple")
    d.box(982, 422, 404, 232, "Summon 子 Agent", ["独立 session / context", "当前显式设置 Auto", "工作目录检查不是 OS 沙箱", "父审批不等于逐个子调用审批"], "blue")
    d.note(743, "生产系统需要补充的控制", "本文建议：最小权限工具、受限凭据、隔离执行环境、幂等键和审计；不把自然语言策略当成硬约束。")
    d.save("security-boundaries.svg")


def delegation():
    d = Diagram("Recipe 与子 Agent 的组合", "配置复用、上下文分离与共享执行环境，需要分别理解。", 900)
    d.box(54, 196, 385, 232, "Recipe", ["instructions / prompt", "parameters / settings", "extensions / response schema", "sub_recipes / retry", "可手动启动，也可定时启动"], "blue")
    d.box(526, 196, 860, 155, "父 Agent / Summon", ["load：载入 source 指令到当前上下文", "delegate：创建新 Agent + 新 session，可同步或 async 返回 task ID", "load(task_id)：等待结果；peek 看进度；cancel 请求停止"], "teal")
    d.arrow([(439, 285), (526, 285)])
    d.box(526, 425, 398, 215, "子会话 A", ["独立 Conversation", "显式任务 + 参考上下文", "Provider / 扩展集合可选择", "默认 max turns = 25", "当前 mode = Auto"], "purple")
    d.box(988, 425, 398, 215, "子会话 B", ["独立 Conversation", "记录 parent_session_id", "后台任务有数量 / TTL 限制", "返回结果给父会话", "不允许继续嵌套委派"], "purple")
    d.arrow([(725, 351), (725, 425)])
    d.arrow([(1187, 351), (1187, 425)])
    d.box(54, 485, 385, 155, "共享的真实世界", ["可能共享同一工作目录和文件", "cwd 边界不限制所有路径访问", "并行写任务需要明确文件归属"], "amber")
    d.note(718, "Recipe 不是通用事务型工作流引擎", "模型仍决定如何执行；JSON schema 可检查输出形状，但外部动作的幂等、补偿与依赖仍需设计。")
    d.save("subagent-recipes.svg")


if __name__ == "__main__":
    for render in [architecture, turn, machine, code_mode, context, security, delegation]:
        render()
    print(f"Generated 7 SVG diagrams in {OUT}")
