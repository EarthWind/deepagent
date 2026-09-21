"""原创源码工程图。Python 标准库生成可离线阅读的 SVG。"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INK, MUTED = "#152d42", "#557084"
TEAL, BLUE, AMBER, RED = "#087e88", "#4a61ba", "#a56b16", "#af4d4b"


class Diagram:
    def __init__(self, title, subtitle, height=720):
        self.height = height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title><desc>{escape(subtitle)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/></marker></defs>
<style>text{{font-family:'Noto Sans CJK SC','Microsoft YaHei',sans-serif;fill:{INK}}}</style>
<rect width="1280" height="{height}" fill="#f3f7fa"/>
<rect width="10" height="{height}" fill="{TEAL}"/>''']
        self.text(48, 53, title, 28, INK, 700)
        self.text(48, 89, subtitle, 16, MUTED)

    def text(self, x, y, value, size=17, color=INK, weight=400, anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" style="fill:{color}">{escape(value)}</text>')

    def box(self, x, y, width, height, title, lines=(), color=TEAL):
        self.parts.append(f'<g data-card="true"><rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" fill="white" stroke="#d3dfe8" stroke-width="1.5"/><rect x="{x}" y="{y+14}" width="5" height="{height-28}" rx="2" fill="{color}"/>')
        self.text(x+20, y+33, title, 21, color, 700)
        for i, line in enumerate(lines):
            self.text(x+20, y+65+i*27, line, 16)
        self.parts.append('</g>')

    def arrow(self, x1, y1, x2, y2, label="", dashed=False):
        dash = ' stroke-dasharray="7 5"' if dashed else ""
        self.parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#arrow)"{dash}/>')
        if label:
            self.text((x1+x2)/2, (y1+y2)/2-10, label, 15, MUTED, anchor="middle")

    def line(self, x, y1, y2):
        self.parts.append(f'<path d="M{x} {y1} L{x} {y2}" stroke="#bdcddd" stroke-dasharray="5 6"/>')

    def save(self, filename, note):
        self.text(48, self.height-26, note, 15, MUTED)
        (ROOT / filename).write_text("\n".join(self.parts)+"\n</svg>\n")


d = Diagram("Cline：共享执行内核，客户端注入宿主能力", "固定源码 4a56a43f39c2 · VS Code 的 backendMode 为 local；Hub / Remote 是其他可选后端。", 770)
d.box(48, 130, 572, 110, "VS Code", ["React Webview → SdkController → VscodeSessionHost", "注入审批、Diff、工作空间读取、终端执行器"], BLUE)
d.box(660, 130, 572, 110, "CLI / Desktop / 自定义应用", ["通过 Core 接口组织会话", "可以选择 local / hub / remote / auto"], TEAL)
d.arrow(334, 240, 334, 286)
d.arrow(946, 240, 946, 286)
d.box(48, 286, 1184, 115, "@cline/sdk → @cline/core", ["ClineCore / RuntimeHost / SessionRuntime：会话、工具、上下文、持久化、扩展", "VS Code 本地主机调用执行器；Hub 模式把客户端连接与执行生命周期拆开"], BLUE)
d.arrow(350, 401, 350, 449)
d.arrow(940, 401, 940, 449)
d.box(48, 449, 572, 120, "@cline/agents", ["Agent = AgentRuntime", "模型流 → 调用准备与审批 → 工具反馈 → 再生成"], TEAL)
d.box(660, 449, 572, 120, "@cline/llms", ["Gateway / Provider handlers / Model catalog", "消息格式、推理参数、工具流、usage 与错误归一化"], AMBER)
d.arrow(620, 509, 660, 509)
d.box(48, 619, 1184, 80, "@cline/shared：消息、工具、策略、事件、hooks 与通用基础契约", [], TEAL)
d.save("01-architecture.svg", "内核本身不提供文件系统或 shell；能力来自 Core 与宿主的显式装配。")

d = Diagram("一次用户请求：审批是执行链上的等待点", "示例展示一个需要审批的工具调用；循环可包含多次模型请求、多个工具与更多用户输入。", 790)
for x, title in [(155, "Webview"), (465, "SDK 适配器"), (785, "Core / Agent"), (1100, "模型 / 执行器")]:
    d.box(x-112, 125, 224, 68, title, color=BLUE)
    d.line(x, 205, 701)
d.arrow(155, 228, 465, 228, "用户请求 / RPC")
d.arrow(465, 289, 785, 289, "start / send")
d.arrow(785, 350, 1100, 350, "请求模型事件流")
d.arrow(1100, 411, 785, 411, "完整工具参数", True)
d.arrow(785, 472, 465, 472, "requestToolApproval")
d.arrow(465, 533, 155, 533, "虚拟 Diff + ask 消息")
d.arrow(155, 594, 465, 594, "用户批准 / 拒绝", True)
d.arrow(465, 643, 785, 643, "解决审批 Promise", True)
d.arrow(785, 692, 1100, 692, "批准后执行 / 结果回到模型")
d.save("02-request-sequence.svg", "返回 UI：Agent 事件 → Core 事件 → message translator → partial-message / state 订阅。")

d = Diagram("AgentRuntime：生成、工具执行与终止条件", "iteration 是循环计数；一次 iteration 内可以包含 provider 重试或 overflow 恢复请求。", 755)
d.box(48, 135, 342, 137, "开始 run", ["重置本轮状态与 usage", "保留历史；追加输入", "beforeRun / run-started"], BLUE)
d.box(469, 135, 342, 137, "准备并请求模型", ["prepareTurn → beforeModel", "stream：文本 / 工具 / usage", "完成后组装 assistant message"], TEAL)
d.box(890, 135, 342, 137, "检查工具与完成状态", ["无工具：结束或追加提醒", "截断 / 空响应：错误分支", "有工具：进入执行管道"], AMBER)
d.arrow(390, 203, 469, 203)
d.arrow(811, 203, 890, 203)
d.arrow(1060, 272, 1060, 340)
d.box(890, 340, 342, 144, "准备与执行工具", ["beforeTool → policy → approval", "顺序执行 / 相邻并行组", "异常转换为 tool-result error"], TEAL)
d.box(469, 340, 342, 144, "写回结果", ["按调用顺序追加 tool results", "再追加 hook 上下文", "非终止工具 → 下一 iteration"], BLUE)
d.arrow(890, 412, 811, 412)
d.arrow(640, 340, 640, 272, "继续")
d.box(48, 340, 342, 144, "其他停止条件", ["abort / hook stop → aborted", "迭代上限 / 不可恢复错 → failed", "成功完成工具 → completed"], RED)
d.box(48, 543, 1184, 125, "本次固定源码的 VS Code 默认", ["maxIterations 未设置；不暴露旧式完成工具，最终文字响应可结束本轮。", "completed 只表示运行时完成；需求验收仍需要测试、产物与实际观察。"], AMBER)
d.save("03-agent-loop.svg", "离线实验覆盖：参数组装、拒绝、异常、并行屏障、迭代上限、完成工具、投影、恢复与 restore。")

d = Diagram("工具审批：默认策略与宿主策略分层", "该顺序来自 prepareToolExecution；本批工具先逐个完成准备，再进入实际执行分组。", 750)
d.box(48, 136, 356, 139, "① 解析 / 前置 hook", ["坏 JSON → skip", "beforeTool 可修改 input / policy", "Plan guard 可在审批之前阻断"], BLUE)
d.box(462, 136, 356, 139, "② 合并与检查 policy", ["通配 * → 单工具 → hook override", "enabled=false → 拒绝执行", "autoApprove=false → 请求审批"], TEAL)
d.box(876, 136, 356, 139, "③ requestToolApproval", ["宿主检查最新配置 / 展示 UI", "无 callback 或拒绝 → 错误结果", "批准 → 执行器"], AMBER)
d.arrow(404, 204, 462, 204)
d.arrow(818, 204, 876, 204)
d.box(48, 342, 560, 150, "底层 Agent 默认", ["未列出工具：enabled / auto-approved", "没有自动具备文件访问边界", "自定义应用需明确配置权限策略"], RED)
d.box(652, 342, 580, 150, "VS Code 适配层", ["UI 管理的工具设 autoApprove=false", "每次都经过 callback，再读取当前开关", "无需重新建会话，也能响应自动批准设置变化"], TEAL)
d.arrow(1054, 275, 1054, 342)
d.box(48, 558, 1184, 100, "执行权的最终边界", ["工具策略决定是否调用；executor 决定访问什么；进程 / 容器 / 服务端权限决定实际可达范围。"], BLUE)
d.save("04-approval.svg", "拒绝工具会形成 tool-result error 并反馈给模型，不自动等同于取消整个任务。")

d = Diagram("编辑文件：先展示虚拟 Diff，批准后才落盘", "当前 SdkDiffEditCoordinator 路径；完整参数在审批点可用，预览本身不修改真实文件。", 730)
d.box(48, 135, 350, 144, "模型提出编辑", ["editor：path / old_text / new_text", "apply_patch：结构化 patch 文本", "生成完成后得到完整参数"], BLUE)
d.box(465, 135, 350, 144, "虚拟文档预览", ["左右两侧均为虚拟文档", "拒绝 / 取消：关闭预览", "预览失败：仍可继续普通审批"], TEAL)
d.box(882, 135, 350, 144, "宿主审批", ["人工 Approve / Reject", "或最新自动批准设置", "后台编辑可省略预览"], AMBER)
d.arrow(398, 207, 465, 207)
d.arrow(815, 207, 882, 207)
d.arrow(1057, 279, 1057, 350, "批准")
d.box(668, 350, 564, 147, "真实 executor", ["唯一文本匹配；CRLF / LF 规范化", "writeFile / patch 应用 → 返回结果", "失败进入工具反馈；成功后展示实际文件"], TEAL)
d.box(48, 350, 566, 147, "检查边界", ["restrictToCwd 限制相对路径逃逸", "绝对路径在该实现中被明确接受", "预览与写入之间不构成全局文件事务"], RED)
d.box(48, 558, 1184, 88, "生产扩展建议：realpath 允许目录、写入前版本校验、路径锁、受限执行环境。", [], BLUE)
d.save("05-file-edit.svg", "实际实验：保留 CRLF、拒绝重复匹配、拒绝相对越界、允许绝对路径（仅在临时夹具内测试）。")

d = Diagram("上下文：持久记录、请求投影和压缩各有职责", "prepareTurn 返回本次模型请求的 messages；它不会直接替换底层 AgentRuntime 的历史消息。", 765)
d.box(48, 133, 354, 148, "对话记录", ["用户 / assistant / tool results", "用于继续运行、回放与审计", "snapshot / restore 管理消息状态"], BLUE)
d.box(463, 133, 354, 148, "本次请求投影", ["prepareTurn → beforeModel", "system + messages + tools", "模型实际看到的输入"], TEAL)
d.box(878, 133, 354, 148, "预算判断", ["模型输入限制 / 上下文窗口", "字符估算 + 上次真实 input usage", "system / tools 同样消耗预算"], AMBER)
d.arrow(402, 207, 463, 207)
d.arrow(817, 207, 878, 207)
d.arrow(1055, 281, 1055, 346)
d.box(668, 346, 564, 156, "Core 压缩管道（需启用）", ["agentic：模型摘要 + 近期内容", "basic：确定性投影 / 裁剪 / 活动摘要", "维护 compaction state；失败有回退路径"], TEAL)
d.box(48, 346, 564, 156, "provider 超限恢复", ["每 run 最多一次自动恢复", "请求必须实际变小，再次超限则失败", "系统提示和当前输入过大时可能无历史可压缩"], RED)
d.arrow(668, 424, 612, 424)
d.box(48, 560, 1184, 116, "预算常量不能直接当作完整算法", ["trigger ratio=0.9；普通 target ratio=0.7；近期默认保留预算 20k，实际受目标限制。", "压缩有信息损失；限制附件和工具输出、按需读文件仍然必要。"], BLUE)
d.save("06-context.svg", "离线验证了请求投影与已分类 overflow 分支；未调用真实总结模型或供应商 tokenizer。")

d = Diagram("恢复：会话状态与工作树快照分开管理", "当前 SDK 检查点在新用户轮次首次模型请求前创建；不是每次工具结束后自动创建独立快照。", 760)
d.box(48, 132, 568, 175, "会话层", ["SQLite：session / agent / parent / status", "消息与其他工件：通过路径关联", "初始化 SQLite 失败可回退文件服务", "消息回退与 workspace 回退可分别控制"], BLUE)
d.box(664, 132, 568, 175, "Git 检查点层", ["stash 兼容 snapshot + 未忽略的 untracked", "refs/cline/checkpoints/{session}/{runCount}", "scratch index 位于 Cline 数据目录", "干净或退化情形可记录 HEAD"], TEAL)
d.box(48, 373, 568, 140, "对象内 restore", ["恢复消息，重置 run 状态 / usage", "保留工具、hooks、model、listeners", "不恢复终端进程或远端系统"], AMBER)
d.box(664, 373, 568, 140, "工作树 restore", ["先保护用户后来创建的提交", "核对 HEAD 与 checkpoint 基准", "按快照类型执行 Git 恢复操作"], RED)
d.arrow(332, 307, 332, 373)
d.arrow(948, 307, 948, 373)
d.box(48, 577, 1184, 92, "外部副作用不在 Git 快照中：HTTP 请求、数据库更新、远端部署、邮件与其他进程。", [], RED)
d.save("07-recovery.svg", "本图按固定源码绘制；官方产品文档的 shadow Git / per-tool 描述与当前 SDK 路径存在版本差异。")

d = Diagram("Hub 与团队：在循环之外增加协调层", "该图表示可选部署能力；当前 VS Code 使用 local，并显式关闭 spawn-agent 与 agent-teams。", 760)
d.box(48, 132, 330, 147, "客户端 / 触发源", ["CLI / Desktop / 应用", "会话命令、用户输入、审批", "连接与 UI 可独立断开"], BLUE)
d.box(458, 132, 364, 147, "Hub 服务", ["会话 / run / approval handlers", "执行会话不依赖单个面板", "客户端按 sequence 订阅事件"], TEAL)
d.box(902, 132, 330, 147, "事件日志", ["广播前持久化", "全局递增 sequence", "sinceSequence → 分页重放"], AMBER)
d.arrow(378, 205, 458, 205)
d.arrow(822, 205, 902, 205)
d.arrow(640, 279, 640, 350)
d.box(458, 350, 774, 153, "可选团队与委派", ["Core 的 spawn_agent / delegated agent / multi-agent", "成员、任务、消息、运行队列与持久状态", "工具权限、审批、预算与工作目录竞争需要独立管理"], BLUE)
d.box(48, 350, 330, 153, "每个执行实例", ["AgentRuntime", "Model + tools + hooks", "各自的消息与运行状态"], TEAL)
d.arrow(458, 426, 378, 426)
d.box(48, 569, 1184, 100, "UI 事件重放 ≠ 再次执行工具；框架支持团队 ≠ 每个客户端默认启用团队。", [], RED)
d.save("08-hub-team.svg", "Hub 日志有保留与分页语义；持久事件流不是对工具副作用的 exactly-once 保证。")
print("Generated 8 SVG diagrams")
