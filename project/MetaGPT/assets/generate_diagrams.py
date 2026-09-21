"""生成博客原创 SVG 工程图：Python 标准库，无外部字体或网络依赖。"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INK, MUTED, TEAL, BLUE, AMBER, RED = "#142d44", "#547084", "#087f8c", "#4666cc", "#a56812", "#b74846"


class Diagram:
    def __init__(self, title, subtitle, height=700):
        self.height = height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title><desc>{escape(subtitle)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#547084"/></marker></defs>
<style>text {{ font-family: 'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif; fill:{INK}; }} .muted {{fill:{MUTED};}}</style>
<rect width="1280" height="{height}" fill="#f5f8fc"/>
<rect x="0" y="0" width="12" height="{height}" fill="{TEAL}"/>
''']
        self.text(48, 53, title, 29, weight=700)
        self.text(48, 88, subtitle, 16, color=MUTED)

    def text(self, x, y, text, size=18, color=INK, weight=400, anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" style="fill:{color}">{escape(text)}</text>')

    def box(self, x, y, w, h, title, lines=(), color=TEAL):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="white" stroke="#d4e0eb" stroke-width="1.5"/><rect x="{x}" y="{y+14}" width="5" height="{h-28}" rx="2" fill="{color}"/>')
        self.text(x + 20, y + 34, title, 21, color, 700)
        for i, line in enumerate(lines):
            self.text(x + 20, y + 64 + i * 27, line, 16)

    def arrow(self, x1, y1, x2, y2, label="", dashed=False):
        dash = ' stroke-dasharray="7 5"' if dashed else ""
        self.parts.append(f'<path d="M {x1} {y1} L {x2} {y2}" fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#arrow)"{dash}/>')
        if label:
            self.text((x1+x2)/2, (y1+y2)/2 - 10, label, 15, MUTED, anchor="middle")

    def line(self, x1, y1, x2, y2):
        self.parts.append(f'<path d="M {x1} {y1} L {x2} {y2}" stroke="#bdcddb" stroke-width="1.5" stroke-dasharray="5 6"/>')

    def note(self, text):
        self.text(48, self.height - 28, text, 15, MUTED)

    def save(self, name):
        (ROOT / name).write_text("\n".join(self.parts) + "\n</svg>\n", encoding="utf-8")


d = Diagram("MetaGPT：两条执行路径，共享一组运行时抽象", "固定源码 11cdf466d042 · 蓝色：当前 CLI 默认 · 青色：经典 SOP · 原创源码示意", 740)
d.box(48, 128, 1184, 100, "入口与团队生命周期", ["software_company.generate_repo → Team.hire / invest / run → Environment；Context 提供配置与成本管理"], BLUE)
d.arrow(340, 228, 340, 274)
d.arrow(940, 228, 940, 274)
d.box(48, 274, 572, 172, "MGX 动态团队（默认）", ["Team(use_mgx=True) → MGXEnv → TeamLeader", "Alice / Bob / Alex(Engineer2) / David(DataAnalyst)", "RoleZero：计划 + 消息上下文 + JSON 命令执行"], BLUE)
d.box(656, 274, 576, 172, "经典文档驱动 SOP（显式装配）", ["Team(use_mgx=False) → Environment", "ProductManager → Architect → ProjectManager", "Engineer ↔ QaEngineer；前三者启用 use_fixed_sop"], TEAL)
d.arrow(340, 446, 340, 490)
d.arrow(940, 446, 940, 490)
d.box(48, 490, 365, 160, "通信与状态", ["Message / MessageQueue", "RoleContext / Memory", "Plan / Task / 快照"], TEAL)
d.box(441, 490, 365, 160, "生成与工具", ["Action / ActionNode", "工具 Schema / 执行映射", "Provider / LLM"], BLUE)
d.box(834, 490, 398, 160, "项目与执行环境", ["ProjectRepo / 文档依赖", "Editor / Browser / Terminal", "Notebook：代码执行与反馈"], AMBER)
d.note("Environment 是协作环境；它的名称不意味着进程、文件系统或网络已被安全隔离。")
d.save("01-architecture.svg")

d = Diagram("经典 SOP：让交接物成为接口", "这条流水线需要显式选择经典角色和固定 SOP；不是当前默认 CLI 的精确时序。", 670)
xs = [48, 294, 540, 786, 1032]
items = [("产品经理", "WritePRD", "需求 / 用户故事"), ("架构师", "WriteDesign", "接口 / Mermaid"), ("项目经理", "WriteTasks", "任务 / 依赖"), ("工程师", "WriteCode", "代码 / Review"), ("QA", "WriteTest", "运行 / 调试")]
for i, (role, action, artifact) in enumerate(items):
    d.box(xs[i], 148, 200, 150, role, [action, artifact], TEAL if i < 3 else BLUE)
    if i < 4:
        d.arrow(xs[i]+200, 225, xs[i+1], 225)
d.box(48, 359, 1184, 110, "共享项目文件：交付可追踪、修改可定位", ["docs/prd → docs/system_design → docs/task → 源码与测试；FileRepository.save 记录已声明的文件依赖"], AMBER)
for x in xs:
    d.arrow(x+100, 298, x+100, 359)
d.box(48, 510, 560, 94, "控制流", ["cause_by → watch：上游 Action 类型决定谁响应"], TEAL)
d.box(640, 510, 592, 94, "数据流", ["Message + instruct_content + 文件路径：交付物内容"], BLUE)
d.note("失败反馈驱动修复；Schema 合法、生成成功、测试通过和需求满足是不同层级的结果。")
d.save("02-classic-sop.svg")

d = Diagram("消息传播有两道门：先投递，再决定是否行动", "Environment.publish_message → Role.msg_buffer → Role._observe；下方给出四种实际语义。", 720)
d.box(48, 145, 318, 151, "Message", ["send_to：接收地址", "cause_by：生产动作类型", "sent_from：发送者"], BLUE)
d.box(420, 145, 357, 151, "门 1：地址路由", ["is_send_to(message, addresses)", "命中角色地址，或含 <all>", "成功 → 放入该角色队列"], TEAL)
d.box(832, 145, 400, 151, "门 2：行动触发", ["cause_by ∈ watch，或名字 ∈ send_to", "并且不在已记住的消息中", "成功 → rc.news → react"], BLUE)
d.arrow(366, 220, 420, 220)
d.arrow(777, 220, 832, 220)
d.box(48, 342, 571, 119, "广播 + 订阅匹配", ["所有角色可收到；只有匹配的角色进入 news。", "例：WritePRD → watch={WritePRD} 的架构师。"], TEAL)
d.box(655, 342, 577, 119, "定向到角色名字", ["显式 send_to={Bob} 可绕过 watch 类型筛选。", "定向到类地址本身不具有这个名字特例。"], BLUE)
d.box(48, 497, 571, 119, "仅仅知情", ["observe_all_msg_from_buffer=True：保存整批消息。", "未匹配的消息可进入 memory，仍不进入 news。"], AMBER)
d.box(655, 497, 577, 119, "去重的边界", ["按 Message 对象相等性过滤，不是内容语义去重。", "相同文本换一个消息 ID，仍可能成为新事件。"], RED)
d.note("本图对应普通 Environment 与基类 _observe；MGX 还会增加 TeamLeader 收件人和公开广播。")
d.save("03-message-routing.svg")

d = Diagram("MGX 一次委派：TeamLeader 组织工作，成员执行任务", "示例为可能的一条路径；具体成员选择与任务内容由模型决定，箭头不代表固定业务顺序。", 750)
for x, title in [(145, "用户"), (460, "MGXEnv"), (775, "Mike / Leader"), (1090, "Alex / Engineer2")]:
    d.box(x-104, 128, 208, 65, title, color=BLUE)
    d.line(x, 206, x, 658)
d.arrow(145, 235, 460, 235, "需求消息")
d.arrow(460, 290, 775, 290, "追加 Mike；公开消息可被其他成员知悉")
d.box(615, 330, 320, 103, "规划 / 选择负责人", ["JSON 命令 → publish_team_message"], BLUE)
d.arrow(775, 465, 460, 465, "send_to=Alex；Leader 暂停等待")
d.arrow(460, 515, 1090, 515, "地址与 _observe 检查后触发")
d.box(956, 550, 276, 83, "编辑 / 终端 / 检查", ["内部可能执行多次模型循环"], TEAL)
d.arrow(1090, 665, 775, 665, "结果经环境送回 Leader；继续下一次决策", True)
d.note("公开聊天默认打开。可见性 ≠ 行动权；Leader 也不保证实现多租户授权或全局任务事务。")
d.save("04-mgx-delegation.svg")

d = Diagram("RoleZero：一轮角色执行包含一个工具决策闭环", "默认 max_react_loop=50；Engineer2=40；TeamLeader=3。环境轮次与模型请求次数不是同一个计数。", 700)
d.box(48, 144, 340, 127, "观察与上下文", ["吸收新消息 / 当前计划", "最近 memory_k=200 条消息"], TEAL)
d.box(469, 144, 342, 127, "模型决策", ["角色指令 + 工具 Schema", "aask → 文本形式的 JSON 命令"], BLUE)
d.box(892, 144, 340, 127, "解析与修复", ["parse_commands / JSON repair", "过滤部分互斥编辑命令"], AMBER)
d.arrow(388, 207, 469, 207)
d.arrow(811, 207, 892, 207)
d.arrow(1060, 271, 1060, 365)
d.box(892, 365, 340, 153, "顺序执行命令", ["tool_execution_map → callable", "异常 / 未知命令停止本批后续", "已执行副作用不会自动回滚"], RED)
d.box(469, 365, 342, 153, "工具反馈写回记忆", ["记录模型命令与工具输出", "进入下一次观察与决策", "end → 清除 todo，结束循环"], TEAL)
d.arrow(892, 441, 811, 441)
d.arrow(640, 365, 640, 271, "继续")
d.box(48, 365, 340, 153, "前置 / 终止分支", ["简单问题可走 quick_think", "大循环到上限可询问用户", "最终响应再次通过环境发布"], BLUE)
d.box(48, 565, 1184, 74, "工具 Schema 是能力说明；实际执行映射与系统权限才决定可执行范围。", [], AMBER)
d.note("RoleZero 的这条主路径不依赖供应商原生 tool_calls；Provider 层另有 function/tool 调用支持。")
d.save("05-rolezero-loop.svg")

d = Diagram("记忆与恢复：区分状态的保存位置和恢复能力", "默认基础记忆是 Python 对象；可选检索记忆、团队快照与 Notebook 内核状态属于不同层。", 730)
d.box(48, 140, 563, 174, "进程内角色状态", ["msg_buffer：尚未消费的消息队列", "memory：已见消息；working_memory：当前任务轨迹", "state / todo / news：当前执行状态", "RoleContext 的队列、todo、news 不进入默认快照"], TEAL)
d.box(649, 140, 583, 174, "可选长期检索", ["role_zero.enable_longterm_memory 默认 False", "超出窗口后写入 Chroma / RAG；检索有触发条件", "memory_k 限制近期上下文，不等于删除旧 storage", "exp_pool 另有开关，默认也未启用"], BLUE)
d.box(48, 365, 563, 174, "Team.serialize / deserialize", ["team.json + Context kwargs / 成本序列化数据", "异常包装器可触发保存；不是每步事务提交", "恢复需要重新构造对象与工具", "latest_observed_msg 支持重新观察最后消息"], AMBER)
d.box(649, 365, 583, 174, "外部执行状态", ["文件修改、Shell 进程、浏览器、Notebook kernel", "这些状态不由团队 JSON 完整恢复", "重放可能重复执行已经完成的外部操作", "生产系统需独立的副作用日志与幂等键"], RED)
d.arrow(330, 314, 330, 365)
d.arrow(920, 314, 920, 365, "不等同")
d.box(48, 589, 1184, 70, "恢复角色对象 ≠ 恢复运行中的进程 ≠ 保证外部副作用恰好执行一次", [], RED)
d.note("这里的生产化措施是作者建议；它们不是上游默认承诺。")
d.save("06-memory-recovery.svg")

d = Diagram("Data Interpreter：用真实执行结果修正生成代码", "DataInterpreter 的 plan_and_act 路径；当前 MGX 的 DataAnalyst 则把类似能力封装成可调用工具。", 670)
d.box(48, 143, 280, 146, "Planner", ["WritePlan → 校验 / 确认", "Task 依赖排序", "选择 current_task"], BLUE)
d.box(373, 143, 300, 146, "WriteAnalysisCode", ["任务 + 已完成工作", "工具说明 + 数据状态", "失败后可加入反思"], TEAL)
d.box(719, 143, 273, 146, "ExecuteNbCode", ["NotebookClient", "持久内核 / cell 执行", "捕获输出与异常"], AMBER)
d.box(1037, 143, 195, 146, "结果", ["result", "is_success", "code"], BLUE)
d.arrow(328, 216, 373, 216)
d.arrow(673, 216, 719, 216)
d.arrow(992, 216, 1037, 216)
d.box(373, 364, 859, 108, "失败 → 反馈 → 再生成", ["working_memory 保留本任务代码与错误；单次写码执行默认最多尝试 3 次"], RED)
d.arrow(1130, 289, 1130, 364)
d.arrow(520, 364, 520, 289)
d.box(48, 516, 1184, 83, "成功后确认任务，再处理后续任务；Notebook 变量可以跨 cell 使用。", ["执行成功只说明运行未报错；数据泄漏、统计方法、指标定义仍需另设验收条件。"], TEAL)
d.note("Notebook 内核是真实代码执行环境，设置 workspace 路径并不形成安全沙盒。")
d.save("07-data-interpreter.svg")

print("Generated 7 SVG diagrams.")
