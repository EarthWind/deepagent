"""Generate the article's original SVG diagrams using only Python's standard library."""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"
OUT.mkdir(exist_ok=True)
INK, MUTED, BLUE, TEAL, ORANGE = "#182d47", "#526880", "#3264c8", "#087f8c", "#ba6423"


class Diagram:
    def __init__(self, title, subtitle, height=800):
        self.height = height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" fill="#70869e"/></marker></defs>
<style>text{{font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif}} .title{{font-size:32px;font-weight:700;fill:{INK}}} .sub{{font-size:18px;fill:{MUTED}}} .label{{font-size:23px;font-weight:700;fill:{INK}}} .body{{font-size:18px;fill:{MUTED}}} .small{{font-size:16px;fill:{MUTED}}}</style>
<rect width="1280" height="{height}" rx="24" fill="#f4f7fc"/>
<rect x="40" y="40" width="6" height="38" rx="3" fill="{TEAL}"/>
<text x="64" y="72" class="title">{escape(title)}</text>
<text x="64" y="108" class="sub">{escape(subtitle)}</text>''']

    def text(self, x, y, content, css="body", color=None):
        self.parts.append(f'<text x="{x}" y="{y}" class="{css}"' + (f' style="fill:{color}"' if color else '') + f'>{escape(content)}</text>')

    def box(self, x, y, w, h, title, lines=(), color=BLUE):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="white" stroke="#d7e0ec" stroke-width="1.5"/><rect x="{x}" y="{y+18}" width="4" height="28" rx="2" fill="{color}"/>')
        self.text(x+20, y+39, title, "label")
        for i, line in enumerate(lines):
            self.text(x+20, y+72+i*28, line)

    def arrow(self, points, label=None, tx=None, ty=None, dashed=False):
        coords = " ".join(f"{x},{y}" for x, y in points)
        self.parts.append(f'<polyline points="{coords}" fill="none" stroke="#70869e" stroke-width="2.2" stroke-linejoin="round" marker-end="url(#arrow)"' + (' stroke-dasharray="7 6"' if dashed else '') + '/>')
        if label:
            self.text(tx, ty, label, "small")

    def finish(self, name, foot):
        self.text(48, self.height-30, foot, "small")
        self.parts.append('</svg>')
        (OUT/name).write_text("\n".join(self.parts) + "\n", encoding="utf-8")


d = Diagram("nanobot：共享运行时的分层架构", "输入适配、会话编排、模型循环与能力扩展分别拥有自己的生命周期")
d.box(48,160,250,152,"入口与通道",["WebUI / TUI / Chat Apps","CLI / Python SDK / API","外部身份 → 会话与路由"])
d.box(364,160,250,152,"MessageBus",["inbound / outbound 队列","publish：等待本地订阅者","publish_event：排队交付"])
d.box(680,160,250,152,"AgentLoop",["恢复、命令、构建上下文","会话锁与跟进消息","保存并交付运行结果"])
d.arrow([(298,230),(364,230)])
d.arrow([(614,230),(680,230)])
d.box(680,402,250,156,"AgentRunner",["LLMRuntime + RunSpec","模型响应 → 工具 → 观察","终止条件与 checkpoint"],TEAL)
d.arrow([(805,312),(805,402)],"执行本轮",825,366)
d.box(996,365,236,132,"Providers",["模型与协议转换","重试、fallback、流式"],TEAL)
d.box(996,547,236,132,"Tools",["文件 / Shell / Web","MCP / spawn / cron"],TEAL)
d.arrow([(930,442),(996,442)])
d.arrow([(930,514),(960,514),(960,602),(996,602)])
d.box(48,402,540,156,"状态与提示词",["Session JSONL + 恢复 checkpoint + provider state","项目 AGENTS.md / Agent 身份与 Skills","归档 history.jsonl → Dream → 长期知识文件"],ORANGE)
d.arrow([(588,464),(680,464)],dashed=True)
d.box(48,615,850,92,"Gateway / SDK / API 是装配入口",["装配工具、MCP 连接、调度服务与清理逻辑；直接调用可绕过 inbound 队列。"])
d.finish("architecture.svg","源码基线 499bf903 · 实线表示主要调用或消息路径；虚线表示上下文依赖。")

d = Diagram("一轮 Agent 执行：模型只能提出调用，运行时决定是否执行", "AgentLoop 编排 turn；AgentRunner 在有限预算内推进多个模型 round",840)
for x,t,l in [(48,"1. Restore / Build",["恢复会话和工作区","冻结 LLMRuntime"]),(460,"2. Prepare request",["修复回放 / 控制 token","加载 tool schemas"]),(872,"3. Provider response",["content / tool_calls","finish_reason / usage"])]:
    d.box(x,165,360,128,t,l)
d.arrow([(408,228),(460,228)])
d.arrow([(820,228),(872,228)])
d.box(872,373,360,148,"4. 工具执行分支",["检查 should_execute_tools","awaiting_tools → 执行批次","tools_completed → 观察回填"],TEAL)
d.arrow([(1052,293),(1052,373)],"可执行 tool calls",1064,338)
d.box(460,373,360,148,"5. 新一轮",["处理用户注入与子任务结果","压缩和限流按当前状态判断","继续模型调用"],TEAL)
d.arrow([(872,446),(820,446)])
d.arrow([(640,373),(640,293)])
d.box(48,373,360,148,"6. 终止与保存",["完成 / 错误 / 空响应 / 上限","final_response checkpoint","保存 transcript，交付回复"],ORANGE)
d.arrow([(460,446),(408,446)],"结束",419,430)
d.arrow([(1232,228),(1254,228),(1254,568),(228,568),(228,521)],dashed=True)
d.text(872,593,"无工具的终态响应走保存分支", "small")
d.box(48,615,564,122,"特殊响应仍有明确规则",["length：有界续写；refusal / content_filter：不执行工具","普通调用到迭代上限：可追加一次无工具收尾"],ORANGE)
d.box(656,615,576,122,"目标续跑是额外策略",["活跃 sustained goal 可以继续，受独立续跑次数限制","maxToolIterations 约束循环，不等于总 API 请求预算"],ORANGE)
d.finish("agent-loop.svg","概念图省略 Hook 和部分重试分支；详细条件以 runner.py / turn_continuation.py 为准。")

d = Diagram("上下文工程：身份、项目与消息分开组织", "选择项目目录不会自动创建独立的 Agent 身份或记忆空间")
d.box(48,164,360,180,"Agent workspace",["SOUL.md / USER.md","memory/MEMORY.md","skills/ 与启用的插件 Skills","提供持续的个人上下文"],TEAL)
d.box(460,164,360,180,"Project workspace",["项目 AGENTS.md","文件工具的相对路径根目录","Shell cwd 与 workspace scope","承载本轮项目约束"],BLUE)
d.box(872,164,360,180,"Turn / Session",["summary + recent history","当前用户输入与附件","时间、路由、目标等运行信息","冻结的模型配置"],ORANGE)
d.arrow([(228,344),(228,388),(640,388),(640,430)])
d.arrow([(640,344),(640,430)])
d.arrow([(1052,344),(1052,388),(640,388)])
d.box(240,430,800,125,"ContextBuilder → ContextGovernor",["稳定 system 前缀 + 动态运行信息；工具定义固定排序以利于缓存","修复工具调用配对、外置过长结果、必要时压缩已接受历史"])
d.arrow([(640,555),(640,612)])
d.box(240,612,800,90,"提供给模型的有效请求",["输入预算 = contextWindowTokens − maxTokens − 1024；超限检查包含工具定义"],TEAL)
d.finish("context.svg","工作区分离是上下文与路径策略；不同 session key 仍可能共享同一 Agent 的长期记忆。")

d = Diagram("记忆不是一个文件：回放、归档、整理三个层次", "压缩解决本轮输入容量；Dream 解决跨轮知识如何沉淀",860)
d.box(48,165,360,150,"① Session transcript",["外部 sessions 目录中的 JSONL","完整记录与回放视图分离","摘要边界 + 近期消息"])
d.box(460,165,360,150,"② MemoryArchiver",["总结已被模型接受的前缀","生成可继续任务的 handoff","失败时保留有界原始归档"])
d.box(872,165,360,150,"③ history.jsonl",["cursor / timestamp / content","记录归档摘要及来源会话",".cursor：写入进度"],TEAL)
d.arrow([(408,240),(460,240)])
d.arrow([(820,240),(872,240)])
d.arrow([(1052,315),(1052,389)])
d.box(872,389,360,156,"④ Dream",["默认每 2 小时调度","读取尚未消费的归档批次","受限文件工具执行整理"],TEAL)
d.box(460,389,360,156,"⑤ 知识与技能",["SOUL.md / USER.md","memory/MEMORY.md","受限工具也允许编辑 skills/"],ORANGE)
d.arrow([(872,466),(820,466)])
d.box(48,389,360,156,"⑥ GitStore（条件启用）",["Agent workspace/.git","审计三个知识文件与消费游标","处于已有仓库时跳过初始化"],ORANGE)
d.arrow([(460,466),(408,466)])
d.box(48,634,1184,122,"完成语义决定消费进度",["Dream 正常完成才推进 .dream_cursor；没有文件变化也可以是一次成功消费。","未完成可能留下部分编辑，下一次会再次处理该批历史；文件编辑、游标和 Git 提交不是跨文件事务。"],ORANGE)
d.finish("memory.svg","GitStore 的自动跟踪范围不等于 Dream 工具的全部可写范围；图示以 memory.py 的实现为准。")

d = Diagram("并发有三个层次，隔离能力也不同", "会话调度、同轮工具批次、子 Agent 容量分别控制",840)
d.box(48,164,1184,124,"会话层：同会话串行，不同会话并发",["Session A：turn 1 → turn 2    ｜    Session B：turn 1 同时运行","可设置 NANOBOT_MAX_CONCURRENT_REQUESTS；未设置时没有全局并发上限。"])
d.box(48,345,270,150,"工具批次 1",["read_file A","read_file B","concurrency_safe → gather"],TEAL)
d.box(372,345,270,150,"工具批次 2",["edit_file","有副作用，形成屏障","等前批结束后独立执行"],ORANGE)
d.box(696,345,270,150,"工具批次 3",["web_search","read_file C","符合属性时再并发"],TEAL)
d.arrow([(318,420),(372,420)])
d.arrow([(642,420),(696,420)])
d.text(992,401,"按原始调用顺序", "body")
d.text(992,432,"回填模型上下文", "body")
d.box(48,573,560,152,"spawn(wait=false)",["后台 Task → 完成事件回到父会话","默认子 Agent 并发容量为 4","独立 Runner / messages / 工具注册表"],BLUE)
d.box(664,573,568,152,"spawn(wait=true)",["等待子 Agent 返回，将结果作为本次工具观察","默认不复制父会话全部历史","共享项目文件；不等于独立进程或文件沙盒"],ORANGE)
d.finish("concurrency.svg","图中工具名称是批次示例；是否并发由具体工具的 concurrency_safe 属性决定。")

d = Diagram("恢复边界：保存了记录，不等于可以重放副作用", "checkpoint 帮助判断已知状态；用户确认决定重启后的继续执行",820)
d.box(48,165,360,152,"awaiting_tools",["assistant 调用意图已保存","工具执行前的 checkpoint","执行中崩溃：结果可能未知"],ORANGE)
d.box(460,165,360,152,"tools_completed",["整批工具结果已保存","模型可以读取已有观察","没有逐个工具事务提交保证"],TEAL)
d.box(872,165,360,152,"final_response",["最终答案已经持久化","可恢复已保存输出","恢复本身不再调用模型"],BLUE)
d.arrow([(408,239),(460,239)])
d.arrow([(820,239),(872,239)])
d.arrow([(228,317),(228,410)])
d.arrow([(640,317),(640,410)])
d.arrow([(1052,317),(1052,410)])
d.box(48,410,772,120,"WebUI 重启恢复：awaiting_user",["工具状态未知、仅有同步 checkpoint 等情况等待确认","确认后从已有上下文继续；框架不承诺外部操作 exactly-once"],ORANGE)
d.box(872,410,360,120,"recovered",["恢复答案并更新界面状态","无需重新执行已完成工作"],TEAL)
d.box(48,612,1184,122,"落盘实现要分别看",["Session：临时文件 + os.replace；fsync 可选。高频 checkpoint 使用独立 sidecar，普通写入不强制 fsync。","Memory：常规 history 追加与整文件压缩重写走不同路径；不能把“原子替换”推导为所有写入都抗断电。"])
d.finish("recovery.svg","恢复流程主要对应 session/recovery.py 的 WebUI RecoveryCoordinator；不要外推为所有通道自动恢复。")

d = Diagram("权限边界：入口、能力、路径、进程、网络分别约束", "现有机制与部署建议分开评估；Prompt 中的限制不能替代执行层控制",850)
rows=[
 ("入口身份", "allowFrom / 配对 / WebSocket token", "决定谁能够给 Agent 下达指令", BLUE),
 ("工具能力", "Registry + scope + Dream 限定文件", "决定当前任务获得哪些工具和读写能力", BLUE),
 ("文件路径", "resolve → containment → 精确读写白名单", "应用级路径检查，不提供完整进程隔离", TEAL),
 ("Shell 进程", "可选 bwrap（Linux）/ seatbelt（macOS）", "默认 sandbox 为空；Windows 有不同退化语义", TEAL),
 ("网络出口", "URL/IP 检查 + DNS 固定 + redirect 检查", "SSRF 检查不自动覆盖所有 Shell/插件网络行为", ORANGE),
]
for i,(t,impl,meaning,c) in enumerate(rows):
    y=157+i*105
    d.box(48,y,245,86,t,[],c)
    d.text(326,y+35,impl,"label")
    d.text(326,y+67,meaning)
d.box(48,708,1184,92,"工程建议",["共享部署增加租户隔离、幂等键、资源配额和统一审计；原生 Python 插件与 stdio MCP 应按宿主代码管理。"],ORANGE)
d.finish("security.svg","以上是源码能力边界分析，不是漏洞利用验证，也不表示已完成完整安全审计。")
