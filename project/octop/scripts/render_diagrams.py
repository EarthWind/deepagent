#!/usr/bin/env python3
"""Original source-based engineering diagrams. Standard library only."""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets"
PALETTE = {
    "blue": ("#eaf1ff", "#275dcc"),
    "teal": ("#e6f6f1", "#137b6d"),
    "purple": ("#f0ebfb", "#7052aa"),
    "amber": ("#fff4df", "#95631a"),
    "gray": ("#edf1f6", "#506279"),
}


class Diagram:
    def __init__(self, number, title, subtitle, height=920):
        self.height = height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="{height}" viewBox="0 0 1440 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9" fill="none" stroke="#73849b" stroke-width="1.5"/></marker></defs>
<style>text{{font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif}}</style>
<rect width="1440" height="{height}" fill="#f8fafc"/><rect width="1440" height="8" fill="#137b6d"/>''']
        self.text(54, 51, f"OCTOP / SOURCE NOTES / {number:02}", 17, "#137b6d", True)
        self.text(54, 106, title, 34, bold=True)
        self.text(54, 148, subtitle, 19, "#56677e")

    def text(self, x, y, text, size=20, color="#20324a", bold=False):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}">{escape(text)}</text>')

    def box(self, x, y, w, h, title, lines=(), tone="blue"):
        fill, stroke = PALETTE[tone]
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>')
        self.text(x + 20, y + 35, title, 23, stroke, True)
        for i, line in enumerate(lines):
            self.text(x + 20, y + 71 + i * 29, line, 19)

    def arrow(self, points, label=None, lx=0, ly=0, dashed=False):
        d = "M" + " L".join(f"{x},{y}" for x, y in points)
        dash = ' stroke-dasharray="7 6"' if dashed else ""
        self.parts.append(f'<path d="{d}" fill="none" stroke="#73849b" stroke-width="2"{dash} marker-end="url(#arrow)"/>')
        if label:
            self.text(lx, ly, label, 18, "#56677e")

    def note(self, y, title, body):
        self.box(54, y, 1332, 106, title, [body], "amber")

    def save(self, name):
        self.parts.append(f'<path d="M54,{self.height - 49} H1386" stroke="#d6dfe9"/>')
        self.text(54, self.height - 23, "原创源码示意图 · Octop 757fd12 + 锁定依赖 · 2026-09-20 · 非官方截图 / 非性能实测", 15, "#627389")
        self.parts.append("</svg>")
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text("\n".join(self.parts) + "\n")


def architecture():
    d = Diagram(1, "Octop：单进程中的产品控制层与 Agent 运行时", "当前源码使用全局 AgentManager；用户权限由资源归属与每次请求的身份共同确定。", 1010)
    d.box(54, 192, 382, 163, "用户入口", ["Dashboard / CLI / IM", "HTTP + WebSocket", "入站 ACP"], "blue")
    d.box(522, 192, 420, 163, "Octop 控制与消息层", ["FastAPI / 身份与资源权限", "Gateway / ChannelManager", "GlobalProcessor / ThreadRegistry"], "teal")
    d.box(1028, 192, 358, 163, "主动任务", ["CronManager / APScheduler", "CronDeliveryService", "会话锁 → runtime.stream"], "purple")
    d.arrow([(436, 270), (522, 270)])
    d.arrow([(1028, 310), (974, 310), (974, 451), (942, 451)])
    d.box(522, 414, 420, 216, "AgentManager（全局）", ["DB 行 → HarnessAgentConfig", "HarnessAgentManager", "每 Agent：workspace / tools", "graph / memory / checkpoint", "模型、连接器、生命周期"], "teal")
    d.arrow([(732, 355), (732, 414)])
    d.box(54, 414, 382, 216, "持久化与目录", ["SQLite / PostgreSQL 控制面", "用户、Agent、会话、用量", "workspace 内容 backend", "Memory / checkpoint", "知识库本地 SQLite 索引"], "gray")
    d.arrow([(522, 520), (436, 520)])
    d.box(1028, 414, 358, 216, "Harness 依赖层", ["harness-agent", "deepagents / LangGraph", "harness-memory", "harness-gateway", "harness-browser"], "purple")
    d.arrow([(942, 545), (1028, 545)])
    d.box(54, 690, 382, 135, "模型服务", ["远端 API / 本地推理", "模型路由、重试与用量"], "blue")
    d.box(522, 690, 420, 135, "工具与执行环境", ["文件 / Shell / 浏览器 / MCP", "本机、Docker 或远程 backend"], "teal")
    d.box(1028, 690, 358, 135, "协作与外部 Agent", ["ask_agent / 内存 inbox", "task 子 Agent / 出站 ACP"], "purple")
    d.arrow([(620, 630), (620, 658), (245, 658), (245, 690)])
    d.arrow([(732, 630), (732, 690)])
    d.arrow([(850, 630), (850, 658), (1207, 658), (1207, 690)])
    d.text(54, 897, "单进程指核心服务的部署形态；Shell、浏览器、ACP runner 仍可启动子进程或连接远端。", 22, "#506279")
    d.save("01-architecture.svg")


def turn():
    d = Diagram(2, "一条 Dashboard 消息如何完成工具往返", "WebSocket 负责双向消息；队列、会话锁、运行时和历史各自拥有不同职责。", 1040)
    for x, w, title in [(54, 260, "Dashboard"), (388, 310, "Gateway / Processor"), (772, 292, "Harness / Graph"), (1138, 248, "模型 / 工具")]:
        d.box(x, 192, w, 64, title, tone="teal" if x == 772 else "blue")
        mid = x + w / 2
        d.parts.append(f'<path d="M{mid},265 V810" stroke="#b9c7d7" stroke-dasharray="6 7"/>')
    d.arrow([(184, 303), (543, 303)], "① JWT + user_turn + thread", 209, 290)
    d.text(402, 350, "鉴权 → 入队 → 同会话锁", 18, "#137b6d")
    d.arrow([(543, 397), (918, 397)], "② ChatRequest / configurable", 565, 382)
    d.text(794, 440, "记忆 / Skills / 选工具 / 路由", 18, "#137b6d")
    d.arrow([(918, 480), (1262, 480)], "③ model call", 985, 466)
    d.arrow([(1262, 522), (918, 522)], "④ tool_calls", 985, 508)
    d.text(794, 565, "工具检查，必要时 HITL 暂停", 18, "#95631a")
    d.arrow([(918, 604), (1262, 604)], "⑤ 执行获准工具", 977, 590)
    d.arrow([(1262, 647), (918, 647)], "⑥ observation", 985, 633)
    d.arrow([(918, 690), (1262, 690)], "⑦ 带结果继续模型调用", 947, 676)
    d.arrow([(918, 750), (543, 750)], "⑧ token / tool_result / usage", 565, 735)
    d.arrow([(543, 802), (184, 802)], "⑨ WS 推送；历史 / 用量记录", 205, 787)
    d.note(858, "断线与重启要分开理解", "断开 WS 不取消当前任务；重连订阅后续帧不等于完整事件重放，进程重启也不会恢复内存队列。")
    d.save("02-turn-lifecycle.svg")


def assembly():
    d = Diagram(3, "Agent 的能力来自组装，而不是一个巨型 Prompt", "简化的中间件分组；顺序以 HarnessAgent._build_middleware 与 deepagents 构图为准。", 940)
    d.box(54, 197, 402, 180, "① Octop 产品配置", ["AgentRow + Provider / 模型", "全局安全策略 + Agent override", "Connector / Plugin / Skills", "Cron / Knowledge / 配额"], "blue")
    d.box(518, 197, 402, 180, "② HarnessAgentConfig", ["backend + workspace", "tools + middleware", "memory + checkpointer", "bootstrap / ACP / 运行限制"], "teal")
    d.box(982, 197, 404, 180, "③ deepagents 图", ["create_deep_agent", "模型 → 工具 → 模型", "文件 / 计划 / task 子 Agent", "摘要压缩 / HITL / LangGraph"], "purple")
    d.arrow([(456, 278), (518, 278)])
    d.arrow([(920, 278), (982, 278)])
    d.text(54, 439, "每次模型调用前后的策略链", 23, "#137b6d", True)
    d.box(54, 468, 402, 225, "请求与访问控制", ["Bootstrap → ModelRouter", "ModelSettings / SessionHeader", "SkillFilter / ToolGuard", "FilesystemGuard / MCP 选择", "Retry / PII / 大媒体卸载"], "blue")
    d.box(518, 468, 402, 225, "状态与产品中间件", ["CheckpointTs / Memory", "TokenQuota / Reasoning", "KnowledgeSearchHint", "BrowserProfile / 附件读取", "WorkspaceImage / 产物记录"], "teal")
    d.box(982, 468, 404, 225, "最终工具与上下文", ["PeerAgentMiddleware", "ToolsFilter", "ToolSearch（条件挂载）", "task 排序 / ContextUsage", "向模型发送最终请求"], "purple")
    d.arrow([(456, 574), (518, 574)])
    d.arrow([(920, 574), (982, 574)])
    d.note(755, "工程意义", "工具过滤应先于工具搜索；显示给模型的能力列表与真正执行时的身份、权限检查都需要成立。")
    d.save("03-agent-assembly.svg")


def memory():
    d = Diagram(4, "上下文、长期记忆与知识库：三种不同的数据路径", "Checkpoint 保存对话执行状态；长期记忆从经历中提炼；知识库从用户文档中检索。", 990)
    d.box(54, 195, 402, 218, "运行上下文 / Checkpoint", ["当前 thread 的消息与图状态", "恢复对话、HITL 与后续调用", "Memory 可兼任 checkpointer", "无 Memory 时回退 SQLite saver", "另有 UI 历史投影 / JSONL"], "blue")
    d.box(518, 195, 402, 218, "长期记忆 / harness-memory", ["L0 原始事件 → L1 候选", "L2 原子事实 → L3 实体页", "另有 episode / 日记层", "FTS 默认；可选向量来源", "按 Agent namespace 分区"], "teal")
    d.box(982, 195, 404, 218, "知识库 / Octop RAG", ["用户上传的文档", "解析 → 分块 → embedding", "每 KB 一份 index.sqlite", "Agent 调用 search_knowledge", "权限过滤、片段与引用"], "purple")
    d.box(54, 481, 402, 186, "压缩：控制窗口大小", ["识别模型 max_input_tokens", "通常 85% 触发，保留 10%", "无 profile 使用另一组阈值", "摘要 + 近期消息 + 历史卸载"], "blue")
    d.box(518, 481, 402, 186, "召回：冻结本轮证据", ["新用户消息触发 recall", "快照写入消息元数据", "API 消息副本重放快照", "工具续轮复用；后台 capture"], "teal")
    d.box(982, 481, 404, 186, "检索：按需找文档证据", ["本轮可见 KB 目录", "模型选择 query 与 k", "返回 Top-k + 字符预算", "检索失败不等于没有答案"], "purple")
    d.arrow([(255, 413), (255, 481)])
    d.arrow([(719, 413), (719, 481)])
    d.arrow([(1184, 413), (1184, 481)])
    d.box(298, 724, 844, 102, "最终模型请求", ["稳定系统提示 + 压缩后的历史 + 固定召回快照 + 工具结果"], "gray")
    d.arrow([(255, 667), (255, 775), (298, 775)])
    d.arrow([(719, 667), (719, 724)])
    d.arrow([(1184, 667), (1184, 775), (1142, 775)])
    d.text(54, 893, "迁移不能只复制 SOUL.md：还要考虑控制面、Memory、知识库索引、附件与所选 backend。", 22, "#506279")
    d.save("04-context-memory.svg")


def team():
    d = Diagram(5, "后台协作的真实语义：一个内存 inbox，串行完成两次调用", "ask_agent(background) 返回 job_id；最终答复由 source Agent 结合父 thread 再生成。", 945)
    d.box(54, 196, 402, 168, "主对话 / source Agent", ["识别需要的专家", "ask_agent(mode=background)", "收到 queued 后继续当前对话"], "blue")
    d.box(518, 196, 402, 168, "TeamManager / Inbox", ["目标归属与可调用性检查", "dict + asyncio.Queue", "单 worker，非持久任务队列"], "teal")
    d.box(982, 196, 404, 168, "target Agent", ["自己的配置、工具与记忆", "关联的 peer thread", "生成结果或失败原因"], "purple")
    d.arrow([(456, 275), (518, 275)])
    d.arrow([(920, 275), (982, 275)])
    d.box(54, 440, 402, 169, "① running", ["target.call(message)", "等待子任务结果", "同 inbox 后续任务继续排队"], "purple")
    d.box(518, 440, 402, 169, "② replying", ["compose_followup(result / error)", "source.call(source_thread_id)", "合成回复写入父对话 checkpoint"], "teal")
    d.box(982, 440, 404, 169, "③ on_reply", ["IM：Gateway.push_text", "Dashboard：未读 / 活跃时间", "完成条目会从内存字典移除"], "blue")
    d.arrow([(456, 520), (518, 520)])
    d.arrow([(920, 520), (982, 520)])
    d.note(672, "不要混为一谈", "同级 ask_agent、deepagents 的 task 子 Agent、外部 ACP runner 是三条不同的协作路径。")
    d.text(54, 832, "@专家在此版本由 PeerAgentMiddleware 注入名单与指引，交由模型选择调用；不是确定性 fan-out。", 20, "#506279")
    d.save("05-team-inbox.svg")


def rag():
    d = Diagram(6, "知识库：轻量存储与按需工具检索", "这是源码中的实际检索路径；图中不包含尚未实现的 ANN 索引或独立 reranker。", 950)
    d.text(54, 206, "写入路径", 23, "#137b6d", True)
    d.box(54, 232, 402, 167, "上传 / 文档状态", ["pending → processing", "解析文本、可选 OCR", "索引任务并发上限 2"], "blue")
    d.box(518, 232, 402, 167, "分块与 embedding", ["默认 800 字符 / 重叠 120", "size / overlap 可配置", "本地或远端 embedding"], "teal")
    d.box(982, 232, 404, 167, "index.sqlite", ["每个 KB 独立 sidecar", "文本、doc_id、float32 向量", "事务替换文档 chunks → ready"], "purple")
    d.arrow([(456, 315), (518, 315)])
    d.arrow([(920, 315), (982, 315)])
    d.text(54, 468, "读取路径", 23, "#137b6d", True)
    d.box(54, 494, 402, 192, "模型调用 search_knowledge", ["本轮已选择且可见的 KB", "query + k（默认 8）", "无 KB 时隐藏检索工具", "执行时再次过滤可见性"], "blue")
    d.box(518, 494, 402, 192, "查询向量与排序", ["query embedding", "取出每个 KB 的全部 chunks", "Python 余弦相似度 + 排序", "只接受 ready 文档，合并 Top-k"], "teal")
    d.box(982, 494, 404, 192, "片段 → 模型回答", ["默认正文预算 6000 字符", "文档名、段号与引用元数据", "作为 tool result 进入上下文", "模型基于证据组织回答"], "purple")
    d.arrow([(456, 590), (518, 590)])
    d.arrow([(920, 590), (982, 590)])
    d.arrow([(1184, 399), (1184, 435), (719, 435), (719, 494)], dashed=True)
    d.note(753, "扩展性边界", "搜索要遍历并排序向量，成本随 chunks 数增长；切换 PostgreSQL 控制面不会自动替换这个索引。")
    d.save("06-knowledge-rag.svg")


def security():
    d = Diagram(7, "安全要逐层检查：登录、资源、工具与执行环境", "提供安全组件不代表所有组件默认阻断；以下默认值来自固定源码及其锁定依赖。", 1030)
    d.box(54, 195, 633, 215, "① 身份与资源权限", ["HTTP / WS：JWT → User", "Agent：所有者 / 共享 / 管理员规则", "Thread：订阅、取消与访问校验", "CLI：信任本机数据目录访问权", "共享 Agent 的 thread 与 workspace 边界需分别审视"], "blue")
    d.box(753, 195, 633, 215, "② 模型可见能力", ["MCP 本轮选择 / ToolsFilter / ToolSearch", "知识库目录只包含可见且选中的条目", "凭据解密与工具调用由宿主负责", "PII 默认启用 mask；并非全面的数据外泄防护", "Plugin 加载的是 Python 能力，属于宿主信任边界"], "teal")
    d.box(54, 470, 633, 215, "③ 工具执行策略", ["HITL：默认关闭", "ToolGuard：默认 enabled + warn", "敏感路径规则：默认启用", "warn 记录告警，匹配命令仍可执行", "ACP permission_request 有自己的挂起 / 响应流程"], "amber")
    d.box(753, 470, 633, 215, "④ OS / 容器边界", ["POSIX 默认 backend：local_shell，root_dir=/", "workspace 提示词不能形成 OS 隔离", "Docker / OpenSandbox 是可选执行 backend", "bwrap 仅在满足平台与配置条件时使用", "远程内容存储不自动隔离 Shell、浏览器或网络"], "purple")
    d.note(748, "部署判断", "多用户逻辑权限不等于不可信租户的强隔离；默认本机模式应按宿主账号可访问的资源评估权限。")
    d.text(54, 921, "工程建议：显式选择 backend、审批策略与凭据边界，再验证文件、Shell、MCP、ACP 等具体执行路径。", 20, "#506279")
    d.save("07-security-boundaries.svg")


def recovery():
    d = Diagram(8, "哪些状态能恢复，哪些只是当前进程里的对象", "“有数据库”“有 checkpoint”“任务可靠投递”是三个不同的承诺。", 950)
    d.box(54, 195, 402, 197, "控制面 · 持久化", ["Agent / User / Provider / Cron", "启动时重建管理器和计划", "SQLite 或 PostgreSQL", "不记录每个工具动作的事务"], "teal")
    d.box(518, 195, 402, 197, "对话状态 · 持久化", ["Memory / LangGraph checkpoint", "UI history / JSONL 等辅助记录", "可以继续读取与推进对话", "不能回滚已发生的外部副作用"], "teal")
    d.box(982, 195, 404, 197, "知识库 · 状态驱动恢复", ["文档状态保存在控制面", "本地索引按文档原子替换", "启动扫描 pending / 中断任务", "重新安排解析与索引"], "teal")
    d.box(54, 454, 402, 197, "Gateway 队列 · 内存", ["每 channel 默认 4 workers", "默认 queue_maxsize=1000", "同 session 串行，跨会话并发", "队列满可能丢弃；重启无重放"], "amber")
    d.box(518, 454, 402, 197, "Teams inbox · 内存", ["单 worker 串行处理", "job_id 与状态存于字典", "无持久确认 / 租约 / 重试表", "完成清理，重启丢失未完成任务"], "amber")
    d.box(982, 454, 404, 197, "WS 订阅 · 内存", ["连接断开不取消运行中的 turn", "重连可订阅后续 chunks", "漏失帧不承诺逐条 replay", "已保存历史用于页面校正"], "amber")
    d.note(723, "可靠性改造的方向（作者建议）", "若要承诺跨重启执行，应增加持久任务状态、幂等键、确认与重试；不要仅把 SQLite 换成 PostgreSQL。")
    d.save("08-recovery.svg")


if __name__ == "__main__":
    for render in [architecture, turn, assembly, memory, team, rag, security, recovery]:
        render()
    print("Rendered 8 original SVG diagrams.")
