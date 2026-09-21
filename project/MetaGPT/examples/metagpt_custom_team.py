"""实际 MetaGPT API 的自定义团队示例；需安装固定版本，本文只做语法与静态接口核对。"""
import asyncio
import json

from metagpt.actions import Action, UserRequirement
from metagpt.context import Context
from metagpt.roles import Role
from metagpt.team import Team


class Draft(Action):
    async def run(self, messages):
        return await self._aask(
            "根据需求编写简短实现计划，包含接口和可自动验证的验收条件。\n"
            + "\n".join(message.content for message in messages)
        )


class Review(Action):
    async def run(self, messages):
        return await self._aask(
            "评审下列计划的接口与验收条件，列出遗漏、风险及建议。\n"
            + "\n".join(message.content for message in messages)
        )


async def main():
    context = Context()
    # 当前 Team 默认 use_mgx=True；基础 Role 示例显式选择普通 Environment。
    team = Team(context=context, use_mgx=False)
    team.hire([
        Role(name="Writer", profile="规划工程师", actions=[Draft], watch=[UserRequirement], context=context),
        Role(name="Reviewer", profile="评审工程师", actions=[Review], watch=[Draft], context=context),
    ])
    team.invest(1.0)  # 轮次边界预算检查，不保证调用中途按美元精确停止。
    history = await team.run(n_round=4, idea="为待办事项应用设计新增、完成和列表接口", auto_archive=False)
    if history is None:
        raise RuntimeError("Team.run 没有返回 history；请检查异常日志和恢复快照。")
    print(json.dumps([message.model_dump(mode="json") for message in history.get()], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
